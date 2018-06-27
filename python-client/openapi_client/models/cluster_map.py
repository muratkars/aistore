# coding: utf-8

"""
    DFC

    DFC is a scalable object-storage based caching system with Amazon and Google Cloud backends.  # noqa: E501

    OpenAPI spec version: 1.1.0
    Contact: dfcdev@exchange.nvidia.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six


class ClusterMap(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'tmap': 'dict(str, DaemonInfo)',
        'pmap': 'dict(str, DaemonInfo)',
        'proxy_si': 'DaemonInfo',
        'version': 'int'
    }

    attribute_map = {
        'tmap': 'tmap',
        'pmap': 'pmap',
        'proxy_si': 'proxy_si',
        'version': 'version'
    }

    def __init__(self, tmap=None, pmap=None, proxy_si=None, version=None):  # noqa: E501
        """ClusterMap - a model defined in OpenAPI"""  # noqa: E501

        self._tmap = None
        self._pmap = None
        self._proxy_si = None
        self._version = None
        self.discriminator = None

        if tmap is not None:
            self.tmap = tmap
        if pmap is not None:
            self.pmap = pmap
        if proxy_si is not None:
            self.proxy_si = proxy_si
        if version is not None:
            self.version = version

    @property
    def tmap(self):
        """Gets the tmap of this ClusterMap.  # noqa: E501


        :return: The tmap of this ClusterMap.  # noqa: E501
        :rtype: dict(str, DaemonInfo)
        """
        return self._tmap

    @tmap.setter
    def tmap(self, tmap):
        """Sets the tmap of this ClusterMap.


        :param tmap: The tmap of this ClusterMap.  # noqa: E501
        :type: dict(str, DaemonInfo)
        """

        self._tmap = tmap

    @property
    def pmap(self):
        """Gets the pmap of this ClusterMap.  # noqa: E501


        :return: The pmap of this ClusterMap.  # noqa: E501
        :rtype: dict(str, DaemonInfo)
        """
        return self._pmap

    @pmap.setter
    def pmap(self, pmap):
        """Sets the pmap of this ClusterMap.


        :param pmap: The pmap of this ClusterMap.  # noqa: E501
        :type: dict(str, DaemonInfo)
        """

        self._pmap = pmap

    @property
    def proxy_si(self):
        """Gets the proxy_si of this ClusterMap.  # noqa: E501


        :return: The proxy_si of this ClusterMap.  # noqa: E501
        :rtype: DaemonInfo
        """
        return self._proxy_si

    @proxy_si.setter
    def proxy_si(self, proxy_si):
        """Sets the proxy_si of this ClusterMap.


        :param proxy_si: The proxy_si of this ClusterMap.  # noqa: E501
        :type: DaemonInfo
        """

        self._proxy_si = proxy_si

    @property
    def version(self):
        """Gets the version of this ClusterMap.  # noqa: E501


        :return: The version of this ClusterMap.  # noqa: E501
        :rtype: int
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this ClusterMap.


        :param version: The version of this ClusterMap.  # noqa: E501
        :type: int
        """

        self._version = version

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ClusterMap):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
