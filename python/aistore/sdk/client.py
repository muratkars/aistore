#
# Copyright (c) 2018-2022, NVIDIA CORPORATION. All rights reserved.
#

from __future__ import annotations  # pylint: disable=unused-variable

from aistore.sdk.bucket import Bucket
from aistore.sdk.const import (
    ProviderAIS,
)
from aistore.sdk.cluster import Cluster
from aistore.sdk.request_client import RequestClient
from aistore.sdk.types import Namespace
from aistore.sdk.job import Job
from aistore.sdk.etl import Etl


# pylint: disable=unused-variable
class Client:
    """
    AIStore client for managing buckets, objects, ETL jobs

    Args:
        endpoint (str): AIStore endpoint
    """

    def __init__(self, endpoint: str):
        self._request_client = RequestClient(endpoint)

    def bucket(self, bck_name: str, provider: str = ProviderAIS, ns: Namespace = None):
        """
        Factory constructor for bucket object.
        Does not make any HTTP request, only instantiates a bucket object.

        Args:
            bck_name (str): Name of bucket
            provider (str): Provider of bucket, one of "ais", "aws", "gcp", ... (optional, defaults to ais)
            ns (Namespace): Namespace of bucket (optional, defaults to None)

        Returns:
            The bucket object created.
        """
        return Bucket(
            client=self._request_client, name=bck_name, provider=provider, ns=ns
        )

    def cluster(self):
        """
        Factory constructor for cluster object.
        Does not make any HTTP request, only instantiates a cluster object.

        Returns:
            The cluster object created.
        """
        return Cluster(client=self._request_client)

    def job(self):
        """
        Factory constructor for job object, which contains job-related functions.
        Does not make any HTTP request, only instantiates a job object.

        Returns:
            The job object created.
        """
        return Job(client=self._request_client)

    def etl(self):
        """
        Factory constructor for ETL object.
        Contains APIs related to AIStore ETL operations.
        Does not make any HTTP request, only instantiates an ETL object.

        Returns:
            The ETL object created.
        """
        return Etl(client=self._request_client)