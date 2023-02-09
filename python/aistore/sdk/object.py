#
# Copyright (c) 2022-2023, NVIDIA CORPORATION. All rights reserved.
#
from io import BufferedWriter
from typing import NewType
import requests

from aistore.sdk.const import (
    DEFAULT_CHUNK_SIZE,
    HTTP_METHOD_DELETE,
    HTTP_METHOD_GET,
    HTTP_METHOD_HEAD,
    HTTP_METHOD_PUT,
    QParamArchpath,
    QParamETLName,
    ACT_PROMOTE,
    HTTP_METHOD_POST,
)

from aistore.sdk.types import ObjStream, ActionMsg, PromoteOptions, PromoteAPIArgs

Header = NewType("Header", requests.structures.CaseInsensitiveDict)


# pylint: disable=unused-variable
# pylint: disable=consider-using-with
class Object:
    """
    A class representing an object of a bucket bound to a client.

    Args:
        bucket (Bucket): Bucket to which this object belongs
        obj_name (str): name of object

    """

    def __init__(self, bucket: "Bucket", name: str):
        self._bucket = bucket
        self._client = bucket.client
        self._bck_name = bucket.name
        self._qparams = bucket.qparam
        self._name = name

    @property
    def bucket(self):
        """Bucket to which this object belongs"""
        return self._bucket

    @property
    def name(self):
        """Name of this object"""
        return self._name

    def head(self) -> Header:
        """
        Requests object properties.

        Returns:
            Response header with the object properties.

        Raises:
            requests.RequestException: "There was an ambiguous exception that occurred while handling..."
            requests.ConnectionError: Connection error
            requests.ConnectionTimeout: Timed out connecting to AIStore
            requests.ReadTimeout: Timed out waiting response from AIStore
            requests.exceptions.HTTPError(404): The object does not exist
        """
        return self._client.request(
            HTTP_METHOD_HEAD,
            path=f"objects/{ self._bck_name}/{ self.name }",
            params=self._qparams,
        ).headers

    def get(
        self,
        archpath: str = "",
        chunk_size: int = DEFAULT_CHUNK_SIZE,
        etl_name: str = None,
        writer: BufferedWriter = None,
    ) -> ObjStream:
        """
        Reads an object

        Args:
            archpath (str, optional): If the object is an archive, use `archpath` to extract a single file
                from the archive
            chunk_size (int, optional): chunk_size to use while reading from stream
            etl_name (str, optional): Transforms an object based on ETL with etl_name
            writer (BufferedWriter, optional): User-provided writer for writing content output.
                User is responsible for closing the writer

        Returns:
            The stream of bytes to read an object or a file inside an archive.

        Raises:
            requests.RequestException: "There was an ambiguous exception that occurred while handling..."
            requests.ConnectionError: Connection error
            requests.ConnectionTimeout: Timed out connecting to AIStore
            requests.ReadTimeout: Timed out waiting response from AIStore
        """
        params = self._qparams.copy()
        params[QParamArchpath] = archpath
        if etl_name:
            params[QParamETLName] = etl_name
        resp = self._client.request(
            HTTP_METHOD_GET,
            path=f"objects/{ self._bck_name }/{ self.name }",
            params=params,
            stream=True,
        )
        obj_stream = ObjStream(
            stream=resp,
            response_headers=resp.headers,
            chunk_size=chunk_size,
        )
        if writer:
            writer.writelines(obj_stream)
        return obj_stream

    def put(self, path: str = None, content: bytes = None) -> Header:
        """
        Puts a local file or bytes as an object to a bucket in AIS storage.

        Args:
            path (str): path to local file or bytes.
            content (bytes): bytes to put as an object.

        Returns:
            Object properties

        Raises:
            requests.RequestException: "There was an ambiguous exception that occurred while handling..."
            requests.ConnectionError: Connection error
            requests.ConnectionTimeout: Timed out connecting to AIStore
            requests.ReadTimeout: Timed out waiting response from AIStore
            ValueError: Path and content are mutually exclusive
        """
        if path and content:
            raise ValueError("path and content are mutually exclusive")

        url = f"/objects/{ self._bck_name }/{ self.name }"
        if path:
            with open(path, "rb") as reader:
                data = reader.read()
        else:
            data = content
        return self._client.request(
            HTTP_METHOD_PUT,
            path=url,
            params=self._qparams,
            data=data,
        ).headers

    def promote(self, path: str, promote_options: PromoteOptions = None) -> Header:
        """
        Promotes a file or folder an AIS target can access to a bucket in AIS storage.
        These files can be either on the physical disk of an AIS target itself or on a network file system
        the cluster can access.
        See more info here: https://aiatscale.org/blog/2022/03/17/promote

        Args:
            path (str): Path to file or folder the AIS cluster can reach
            promote_options (PromoteOptions, optional): Object containing additional options for promoting files

        Returns:
            Object properties

        Raises:
            requests.RequestException: "There was an ambiguous exception that occurred while handling..."
            requests.ConnectionError: Connection error
            requests.ConnectionTimeout: Timed out connecting to AIStore
            requests.ReadTimeout: Timed out waiting response from AIStore
            AISError: Path does not exist on the AIS cluster storage
        """
        url = f"/objects/{ self._bck_name }"
        if promote_options is None:
            value = PromoteAPIArgs(source_path=path, object_name=self.name).get_json()
        else:
            value = PromoteAPIArgs(
                target_id=promote_options.target_id,
                source_path=path,
                object_name=self.name,
                recursive=promote_options.recursive,
                overwrite_dest=promote_options.overwrite_dest,
                delete_source=promote_options.delete_source,
                src_not_file_share=promote_options.src_not_file_share,
            ).get_json()
        json_val = ActionMsg(action=ACT_PROMOTE, name=path, value=value).dict()

        return self._client.request(
            HTTP_METHOD_POST, path=url, params=self._qparams, json=json_val
        ).headers

    def delete(self):
        """
        Delete an object from a bucket.

        Returns:
            None

        Raises:
            requests.RequestException: "There was an ambiguous exception that occurred while handling..."
            requests.ConnectionError: Connection error
            requests.ConnectionTimeout: Timed out connecting to AIStore
            requests.ReadTimeout: Timed out waiting response from AIStore
            requests.exceptions.HTTPError(404): The object does not exist
        """
        self._client.request(
            HTTP_METHOD_DELETE,
            path=f"objects/{ self._bck_name }/{ self.name }",
            params=self._qparams,
        )
