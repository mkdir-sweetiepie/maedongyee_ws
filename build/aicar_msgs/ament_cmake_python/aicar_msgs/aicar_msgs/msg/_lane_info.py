# generated from rosidl_generator_py/resource/_idl.py.em
# with input from aicar_msgs:msg/LaneInfo.idl
# generated code does not contain a copyright notice

# This is being done at the module level and not on the instance level to avoid looking
# for the same variable multiple times on each instance. This variable is not supposed to
# change during runtime so it makes sense to only look for it once.
from os import getenv

ros_python_check_fields = getenv('ROS_PYTHON_CHECK_FIELDS', default='')


# Import statements for member types

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_LaneInfo(type):
    """Metaclass of message 'LaneInfo'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('aicar_msgs')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'aicar_msgs.msg.LaneInfo')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__lane_info
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__lane_info
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__lane_info
            cls._TYPE_SUPPORT = module.type_support_msg__msg__lane_info
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__lane_info

            from std_msgs.msg import Header
            if Header.__class__._TYPE_SUPPORT is None:
                Header.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class LaneInfo(metaclass=Metaclass_LaneInfo):
    """Message class 'LaneInfo'."""

    __slots__ = [
        '_header',
        '_left_detect',
        '_left_x',
        '_left_angle',
        '_right_detect',
        '_right_x',
        '_right_angle',
        '_left_pixel_count',
        '_right_pixel_count',
        '_check_fields',
    ]

    _fields_and_field_types = {
        'header': 'std_msgs/Header',
        'left_detect': 'boolean',
        'left_x': 'float',
        'left_angle': 'float',
        'right_detect': 'boolean',
        'right_x': 'float',
        'right_angle': 'float',
        'left_pixel_count': 'int32',
        'right_pixel_count': 'int32',
    }

    # This attribute is used to store an rosidl_parser.definition variable
    # related to the data type of each of the components the message.
    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['std_msgs', 'msg'], 'Header'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('int32'),  # noqa: E501
        rosidl_parser.definition.BasicType('int32'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        if 'check_fields' in kwargs:
            self._check_fields = kwargs['check_fields']
        else:
            self._check_fields = ros_python_check_fields == '1'
        if self._check_fields:
            assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
                'Invalid arguments passed to constructor: %s' % \
                ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        from std_msgs.msg import Header
        self.header = kwargs.get('header', Header())
        self.left_detect = kwargs.get('left_detect', bool())
        self.left_x = kwargs.get('left_x', float())
        self.left_angle = kwargs.get('left_angle', float())
        self.right_detect = kwargs.get('right_detect', bool())
        self.right_x = kwargs.get('right_x', float())
        self.right_angle = kwargs.get('right_angle', float())
        self.left_pixel_count = kwargs.get('left_pixel_count', int())
        self.right_pixel_count = kwargs.get('right_pixel_count', int())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.get_fields_and_field_types().keys(), self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    if self._check_fields:
                        assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.header != other.header:
            return False
        if self.left_detect != other.left_detect:
            return False
        if self.left_x != other.left_x:
            return False
        if self.left_angle != other.left_angle:
            return False
        if self.right_detect != other.right_detect:
            return False
        if self.right_x != other.right_x:
            return False
        if self.right_angle != other.right_angle:
            return False
        if self.left_pixel_count != other.left_pixel_count:
            return False
        if self.right_pixel_count != other.right_pixel_count:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def header(self):
        """Message field 'header'."""
        return self._header

    @header.setter
    def header(self, value):
        if self._check_fields:
            from std_msgs.msg import Header
            assert \
                isinstance(value, Header), \
                "The 'header' field must be a sub message of type 'Header'"
        self._header = value

    @builtins.property
    def left_detect(self):
        """Message field 'left_detect'."""
        return self._left_detect

    @left_detect.setter
    def left_detect(self, value):
        if self._check_fields:
            assert \
                isinstance(value, bool), \
                "The 'left_detect' field must be of type 'bool'"
        self._left_detect = value

    @builtins.property
    def left_x(self):
        """Message field 'left_x'."""
        return self._left_x

    @left_x.setter
    def left_x(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'left_x' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'left_x' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._left_x = value

    @builtins.property
    def left_angle(self):
        """Message field 'left_angle'."""
        return self._left_angle

    @left_angle.setter
    def left_angle(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'left_angle' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'left_angle' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._left_angle = value

    @builtins.property
    def right_detect(self):
        """Message field 'right_detect'."""
        return self._right_detect

    @right_detect.setter
    def right_detect(self, value):
        if self._check_fields:
            assert \
                isinstance(value, bool), \
                "The 'right_detect' field must be of type 'bool'"
        self._right_detect = value

    @builtins.property
    def right_x(self):
        """Message field 'right_x'."""
        return self._right_x

    @right_x.setter
    def right_x(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'right_x' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'right_x' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._right_x = value

    @builtins.property
    def right_angle(self):
        """Message field 'right_angle'."""
        return self._right_angle

    @right_angle.setter
    def right_angle(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'right_angle' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'right_angle' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._right_angle = value

    @builtins.property
    def left_pixel_count(self):
        """Message field 'left_pixel_count'."""
        return self._left_pixel_count

    @left_pixel_count.setter
    def left_pixel_count(self, value):
        if self._check_fields:
            assert \
                isinstance(value, int), \
                "The 'left_pixel_count' field must be of type 'int'"
            assert value >= -2147483648 and value < 2147483648, \
                "The 'left_pixel_count' field must be an integer in [-2147483648, 2147483647]"
        self._left_pixel_count = value

    @builtins.property
    def right_pixel_count(self):
        """Message field 'right_pixel_count'."""
        return self._right_pixel_count

    @right_pixel_count.setter
    def right_pixel_count(self, value):
        if self._check_fields:
            assert \
                isinstance(value, int), \
                "The 'right_pixel_count' field must be of type 'int'"
            assert value >= -2147483648 and value < 2147483648, \
                "The 'right_pixel_count' field must be an integer in [-2147483648, 2147483647]"
        self._right_pixel_count = value
