// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from aicar_msgs:msg/LaneInfo.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "aicar_msgs/msg/lane_info.h"


#ifndef AICAR_MSGS__MSG__DETAIL__LANE_INFO__STRUCT_H_
#define AICAR_MSGS__MSG__DETAIL__LANE_INFO__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

// Constants defined in the message

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.h"

/// Struct defined in msg/LaneInfo in the package aicar_msgs.
typedef struct aicar_msgs__msg__LaneInfo
{
  std_msgs__msg__Header header;
  /// Left lane info
  bool left_detect;
  /// x position at bottom of BEV
  float left_x;
  /// line angle, 90 = vertical
  float left_angle;
  /// Right lane info
  bool right_detect;
  float right_x;
  float right_angle;
  /// Quality (optional debug)
  int32_t left_pixel_count;
  int32_t right_pixel_count;
} aicar_msgs__msg__LaneInfo;

// Struct for a sequence of aicar_msgs__msg__LaneInfo.
typedef struct aicar_msgs__msg__LaneInfo__Sequence
{
  aicar_msgs__msg__LaneInfo * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} aicar_msgs__msg__LaneInfo__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // AICAR_MSGS__MSG__DETAIL__LANE_INFO__STRUCT_H_
