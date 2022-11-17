// Package dloader implements functionality to download resources into AIS cluster from external source.
/*
 * Copyright (c) 2018-2021, NVIDIA CORPORATION. All rights reserved.
 */
package dloader

import (
	"regexp"
	"sync"
	"time"

	"github.com/NVIDIA/aistore/cmn/debug"
	"github.com/NVIDIA/aistore/cmn/kvdb"
	"github.com/NVIDIA/aistore/hk"
)

var (
	// global downloader info store
	db          kvdb.Driver
	dlStore     *infoStore
	dlStoreOnce sync.Once
)

// TODO: stored only in memory, should be persisted at some point (powercycle)
type infoStore struct {
	*downloaderDB
	dljobs map[string]*dljob
	sync.RWMutex
}

func SetDB(dbdrv kvdb.Driver) { db = dbdrv }

func initInfoStore(db kvdb.Driver) {
	dlStoreOnce.Do(func() {
		dlStore = newInfoStore(db)
	})
}

func newInfoStore(driver kvdb.Driver) *infoStore {
	db := newDownloadDB(driver)
	is := &infoStore{
		downloaderDB: db,
		dljobs:       make(map[string]*dljob),
	}
	hk.Reg("downloader"+hk.NameSuffix, is.housekeep, hk.DayInterval)
	return is
}

func (is *infoStore) getJob(id string) (*dljob, error) {
	is.RLock()
	defer is.RUnlock()

	if ji, ok := is.dljobs[id]; ok {
		return ji, nil
	}
	return nil, errJobNotFound
}

func (is *infoStore) getList(descRegex *regexp.Regexp) (jobs []*dljob) {
	is.RLock()
	for _, dji := range is.dljobs {
		if descRegex == nil || descRegex.MatchString(dji.Description) {
			jobs = append(jobs, dji)
		}
	}
	is.RUnlock()
	return
}

func (is *infoStore) setJob(job jobif, xactID string) {
	dljob := &dljob{
		ID:          job.ID(),
		XactID:      xactID,
		Total:       job.Len(),
		Description: job.Description(),
		StartedTime: time.Now(),
	}
	is.Lock()
	is.dljobs[job.ID()] = dljob
	is.Unlock()
}

func (is *infoStore) incFinished(id string) {
	dljob, err := is.getJob(id)
	debug.AssertNoErr(err)
	dljob.FinishedCnt.Inc()
}

func (is *infoStore) incSkipped(id string) {
	dljob, err := is.getJob(id)
	debug.AssertNoErr(err)
	dljob.SkippedCnt.Inc()
	dljob.FinishedCnt.Inc()
}

func (is *infoStore) incScheduled(id string) {
	dljob, err := is.getJob(id)
	debug.AssertNoErr(err)
	dljob.ScheduledCnt.Inc()
}

func (is *infoStore) incErrorCnt(id string) {
	dljob, err := is.getJob(id)
	debug.AssertNoErr(err)
	dljob.ErrorCnt.Inc()
}

func (is *infoStore) setAllDispatched(id string, dispatched bool) {
	dljob, err := is.getJob(id)
	debug.AssertNoErr(err)
	dljob.AllDispatched.Store(dispatched)
}

func (is *infoStore) markFinished(id string) error {
	dljob, err := is.getJob(id)
	if err != nil {
		debug.AssertNoErr(err)
		return err
	}
	dljob.FinishedTime.Store(time.Now())
	return dljob.valid()
}

func (is *infoStore) setAborted(id string) {
	dljob, err := is.getJob(id)
	debug.AssertNoErr(err)
	dljob.Aborted.Store(true)
	// NOTE: Don't set `FinishedTime` yet as we are not fully done.
	//       The job now can be removed but there's no guarantee
	//       that all tasks have been stopped and all resources were freed.
}

func (is *infoStore) delJob(id string) {
	delete(is.dljobs, id)
	is.downloaderDB.delete(id)
}

func (is *infoStore) housekeep() time.Duration {
	const interval = hk.DayInterval

	is.Lock()
	for id, dljob := range is.dljobs {
		if time.Since(dljob.FinishedTime.Load()) > interval {
			is.delJob(id)
		}
	}
	is.Unlock()

	return interval
}
