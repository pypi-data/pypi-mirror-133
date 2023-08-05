# coding: utf-8

"""
    

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)

    OpenAPI spec version: beta
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat

from six import iteritems


class DataSourceRef(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """


    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'by_guid': 'str',
        'by_pk': 'DataSourcePK'
    }

    attribute_map = {
        'by_guid': 'byGUID',
        'by_pk': 'byPK'
    }

    def __init__(self, by_guid=None, by_pk=None):
        """
        DataSourceRef - a model defined in Swagger
        """

        self._by_guid = None
        self._by_pk = None

        if by_guid is not None:
          self.by_guid = by_guid
        if by_pk is not None:
          self.by_pk = by_pk

    @property
    def by_guid(self):
        """
        Gets the by_guid of this DataSourceRef.
        Identify an entity by a server-generated globally-unique-identifier

        :return: The by_guid of this DataSourceRef.
        :rtype: str
        """
        return self._by_guid

    @by_guid.setter
    def by_guid(self, by_guid):
        """
        Sets the by_guid of this DataSourceRef.
        Identify an entity by a server-generated globally-unique-identifier

        :param by_guid: The by_guid of this DataSourceRef.
        :type: str
        """

        self._by_guid = by_guid

    @property
    def by_pk(self):
        """
        Gets the by_pk of this DataSourceRef.
        Identify an entity by it's primary key

        :return: The by_pk of this DataSourceRef.
        :rtype: DataSourcePK
        """
        return self._by_pk

    @by_pk.setter
    def by_pk(self, by_pk):
        """
        Sets the by_pk of this DataSourceRef.
        Identify an entity by it's primary key

        :param by_pk: The by_pk of this DataSourceRef.
        :type: DataSourcePK
        """

        self._by_pk = by_pk

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in iteritems(self.swagger_types):
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
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        if not isinstance(other, DataSourceRef):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
