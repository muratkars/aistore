// Package commands provides the set of CLI commands used to communicate with the AIS cluster.
// This file provides aliases to frequently used commands that are inside other top level commands.
/*
 * Copyright (c) 2021, NVIDIA CORPORATION. All rights reserved.
 */
package commands

import (
	"fmt"

	"github.com/urfave/cli"
)

var aliasCmds = []cli.Command{
	makeAlias(objectCmdGet, "ais object get", false),
	makeAlias(objectCmdPut, "ais object put", false),
	makeAlias(bucketCmdList, "ais bucket ls", false),
}

// makeAlias returns a copy of cmd with some changes:
// 1. command name is changed if provided.
// 2. category set to "ALIASES" if specified.
// 3. "alias for" message added to usage if not a silent alias.
func makeAlias(cmd cli.Command, aliasFor string, silentAlias bool, newName ...string) cli.Command {
	if len(newName) != 0 {
		cmd.Name = newName[0]
	}
	if !silentAlias {
		cmd.Category = "ALIASES"
		cmd.Usage = fmt.Sprintf("(alias for \"%s\") %s", aliasFor, cmd.Usage)
	}
	cmd.HideHelp = true // help is already added to the original command
	return cmd
}
