// generated from rosidl_typesupport_fastrtps_c/resource/idl__rosidl_typesupport_fastrtps_c.h.em
// with input from aicar_msgs:msg/LaneInfo.idl
// generated code does not contain a copyright notice
#ifndef AICAR_MSGS__MSG__DETAIL__LANE_INFO__ROSIDL_TYPESUPPORT_FASTRTPS_C_H_
#define AICAR_MSGS__MSG__DETAIL__LANE_INFO__ROSIDL_TYPESUPPORT_FASTRTPS_C_H_


#include <stddef.h>
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_interface/macros.h"
#include "aicar_msgs/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "aicar_msgs/msg/detail/lane_info__struct.h"
#include "fastcdr/Cdr.h"

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_aicar_msgs
bool cdr_serialize_aicar_msgs__msg__LaneInfo(
  const aicar_msgs__msg__LaneInfo * ros_message,
  eprosima::fastcdr::Cdr & cdr);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_aicar_msgs
bool cdr_deserialize_aicar_msgs__msg__LaneInfo(
  eprosima::fastcdr::Cdr &,
  aicar_msgs__msg__LaneInfo * ros_message);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_aicar_msgs
size_t get_serialized_size_aicar_msgs__msg__LaneInfo(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_aicar_msgs
size_t max_serialized_size_aicar_msgs__msg__LaneInfo(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_aicar_msgs
bool cdr_serialize_key_aicar_msgs__msg__LaneInfo(
  const aicar_msgs__msg__LaneInfo * ros_message,
  eprosima::fastcdr::Cdr & cdr);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_aicar_msgs
size_t get_serialized_size_key_aicar_msgs__msg__LaneInfo(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_aicar_msgs
size_t max_serialized_size_key_aicar_msgs__msg__LaneInfo(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_aicar_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, aicar_msgs, msg, LaneInfo)();

#ifdef __cplusplus
}
#endif

#endif  // AICAR_MSGS__MSG__DETAIL__LANE_INFO__ROSIDL_TYPESUPPORT_FASTRTPS_C_H_
