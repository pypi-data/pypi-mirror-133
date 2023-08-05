# coding: utf-8

"""
    

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)

    OpenAPI spec version: beta
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat

from six import iteritems


class DataStats(object):
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
        'pk': 'DataStatsPK',
        'stats': 'dict(str, object)',
        'extra_as_json': 'str'
    }

    attribute_map = {
        'pk': 'pk',
        'stats': 'stats',
        'extra_as_json': 'extraAsJson'
    }

    def __init__(self, pk=None, stats=None, extra_as_json=None):
        """
        DataStats - a model defined in Swagger
        """

        self._pk = None
        self._stats = None
        self._extra_as_json = None

        self.pk = pk
        self.stats = stats
        if extra_as_json is not None:
          self.extra_as_json = extra_as_json

    @property
    def pk(self):
        """
        Gets the pk of this DataStats.

        :return: The pk of this DataStats.
        :rtype: DataStatsPK
        """
        return self._pk

    @pk.setter
    def pk(self, pk):
        """
        Sets the pk of this DataStats.

        :param pk: The pk of this DataStats.
        :type: DataStatsPK
        """
        if pk is None:
            raise ValueError("Invalid value for `pk`, must not be `None`")

        self._pk = pk

    @property
    def stats(self):
        """
        Gets the stats of this DataStats.
        Statistics of the data as a map between measure names and their value as double

        :return: The stats of this DataStats.
        :rtype: dict(str, object)
        """
        return self._stats

    @stats.setter
    def stats(self, stats):
        """
        Sets the stats of this DataStats.
        Statistics of the data as a map between measure names and their value as double

        :param stats: The stats of this DataStats.
        :type: dict(str, object)
        """
        if stats is None:
            raise ValueError("Invalid value for `stats`, must not be `None`")

        self._stats = stats

    @property
    def extra_as_json(self):
        """
        Gets the extra_as_json of this DataStats.
        If relevant exta non double measures or metadata can be added as a valid JSON string

        :return: The extra_as_json of this DataStats.
        :rtype: str
        """
        return self._extra_as_json

    @extra_as_json.setter
    def extra_as_json(self, extra_as_json):
        """
        Sets the extra_as_json of this DataStats.
        If relevant exta non double measures or metadata can be added as a valid JSON string

        :param extra_as_json: The extra_as_json of this DataStats.
        :type: str
        """

        self._extra_as_json = extra_as_json

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
        if not isinstance(other, DataStats):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
