# coding: utf-8

"""
    

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)

    OpenAPI spec version: beta
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat

from six import iteritems


class ProcessLineage(object):
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
        'name': 'str',
        'operation_logic': 'str',
        'pk': 'ProcessLineagePK'
    }

    attribute_map = {
        'name': 'name',
        'operation_logic': 'operationLogic',
        'pk': 'pk'
    }

    def __init__(self, name=None, operation_logic=None, pk=None):
        """
        ProcessLineage - a model defined in Swagger
        """

        self._name = None
        self._operation_logic = None
        self._pk = None

        self.name = name
        if operation_logic is not None:
          self.operation_logic = operation_logic
        self.pk = pk

    @property
    def name(self):
        """
        Gets the name of this ProcessLineage.

        :return: The name of this ProcessLineage.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this ProcessLineage.

        :param name: The name of this ProcessLineage.
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")

        self._name = name

    @property
    def operation_logic(self):
        """
        Gets the operation_logic of this ProcessLineage.
        data update operation logic, e.g. 'REPLACE', 'UPDATE', 'APPEND'. Default is 'REPLACE'.

        :return: The operation_logic of this ProcessLineage.
        :rtype: str
        """
        return self._operation_logic

    @operation_logic.setter
    def operation_logic(self, operation_logic):
        """
        Sets the operation_logic of this ProcessLineage.
        data update operation logic, e.g. 'REPLACE', 'UPDATE', 'APPEND'. Default is 'REPLACE'.

        :param operation_logic: The operation_logic of this ProcessLineage.
        :type: str
        """

        self._operation_logic = operation_logic

    @property
    def pk(self):
        """
        Gets the pk of this ProcessLineage.

        :return: The pk of this ProcessLineage.
        :rtype: ProcessLineagePK
        """
        return self._pk

    @pk.setter
    def pk(self, pk):
        """
        Sets the pk of this ProcessLineage.

        :param pk: The pk of this ProcessLineage.
        :type: ProcessLineagePK
        """
        if pk is None:
            raise ValueError("Invalid value for `pk`, must not be `None`")

        self._pk = pk

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
        if not isinstance(other, ProcessLineage):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
