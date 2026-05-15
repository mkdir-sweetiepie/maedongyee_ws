// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from aicar_msgs:msg/LaneInfo.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "aicar_msgs/msg/detail/lane_info__rosidl_typesupport_introspection_c.h"
#include "aicar_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "aicar_msgs/msg/detail/lane_info__functions.h"
#include "aicar_msgs/msg/detail/lane_info__struct.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/header.h"
// Member `header`
#include "std_msgs/msg/detail/header__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void aicar_msgs__msg__LaneInfo__rosidl_typesupport_introspection_c__LaneInfo_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  aicar_msgs__msg__LaneInfo__init(message_memory);
}

void aicar_msgs__msg__LaneInfo__rosidl_typesupport_introspection_c__LaneInfo_fini_function(void * message_memory)
{
  aicar_msgs__msg__LaneInfo__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember aicar_msgs__msg__LaneInfo__rosidl_typesupport_introspection_c__LaneInfo_message_member_array[9] = {
  {
    "header",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aicar_msgs__msg__LaneInfo, header),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "left_detect",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aicar_msgs__msg__LaneInfo, left_detect),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "left_x",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aicar_msgs__msg__LaneInfo, left_x),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "left_angle",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aicar_msgs__msg__LaneInfo, left_angle),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "right_detect",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aicar_msgs__msg__LaneInfo, right_detect),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "right_x",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aicar_msgs__msg__LaneInfo, right_x),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "right_angle",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aicar_msgs__msg__LaneInfo, right_angle),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "left_pixel_count",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aicar_msgs__msg__LaneInfo, left_pixel_count),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "right_pixel_count",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aicar_msgs__msg__LaneInfo, right_pixel_count),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers aicar_msgs__msg__LaneInfo__rosidl_typesupport_introspection_c__LaneInfo_message_members = {
  "aicar_msgs__msg",  // message namespace
  "LaneInfo",  // message name
  9,  // number of fields
  sizeof(aicar_msgs__msg__LaneInfo),
  false,  // has_any_key_member_
  aicar_msgs__msg__LaneInfo__rosidl_typesupport_introspection_c__LaneInfo_message_member_array,  // message members
  aicar_msgs__msg__LaneInfo__rosidl_typesupport_introspection_c__LaneInfo_init_function,  // function to initialize message memory (memory has to be allocated)
  aicar_msgs__msg__LaneInfo__rosidl_typesupport_introspection_c__LaneInfo_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t aicar_msgs__msg__LaneInfo__rosidl_typesupport_introspection_c__LaneInfo_message_type_support_handle = {
  0,
  &aicar_msgs__msg__LaneInfo__rosidl_typesupport_introspection_c__LaneInfo_message_members,
  get_message_typesupport_handle_function,
  &aicar_msgs__msg__LaneInfo__get_type_hash,
  &aicar_msgs__msg__LaneInfo__get_type_description,
  &aicar_msgs__msg__LaneInfo__get_type_description_sources,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_aicar_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aicar_msgs, msg, LaneInfo)() {
  aicar_msgs__msg__LaneInfo__rosidl_typesupport_introspection_c__LaneInfo_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, std_msgs, msg, Header)();
  if (!aicar_msgs__msg__LaneInfo__rosidl_typesupport_introspection_c__LaneInfo_message_type_support_handle.typesupport_identifier) {
    aicar_msgs__msg__LaneInfo__rosidl_typesupport_introspection_c__LaneInfo_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &aicar_msgs__msg__LaneInfo__rosidl_typesupport_introspection_c__LaneInfo_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
