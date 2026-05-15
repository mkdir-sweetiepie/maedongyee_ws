// generated from rosidl_typesupport_fastrtps_c/resource/idl__type_support_c.cpp.em
// with input from aicar_msgs:msg/LaneInfo.idl
// generated code does not contain a copyright notice
#include "aicar_msgs/msg/detail/lane_info__rosidl_typesupport_fastrtps_c.h"


#include <cassert>
#include <cstddef>
#include <limits>
#include <string>
#include "rosidl_typesupport_fastrtps_c/identifier.h"
#include "rosidl_typesupport_fastrtps_c/serialization_helpers.hpp"
#include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "aicar_msgs/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "aicar_msgs/msg/detail/lane_info__struct.h"
#include "aicar_msgs/msg/detail/lane_info__functions.h"
#include "fastcdr/Cdr.h"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

// includes and forward declarations of message dependencies and their conversion functions

#if defined(__cplusplus)
extern "C"
{
#endif

#include "std_msgs/msg/detail/header__functions.h"  // header

// forward declare type support functions

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_aicar_msgs
bool cdr_serialize_std_msgs__msg__Header(
  const std_msgs__msg__Header * ros_message,
  eprosima::fastcdr::Cdr & cdr);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_aicar_msgs
bool cdr_deserialize_std_msgs__msg__Header(
  eprosima::fastcdr::Cdr & cdr,
  std_msgs__msg__Header * ros_message);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_aicar_msgs
size_t get_serialized_size_std_msgs__msg__Header(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_aicar_msgs
size_t max_serialized_size_std_msgs__msg__Header(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_aicar_msgs
bool cdr_serialize_key_std_msgs__msg__Header(
  const std_msgs__msg__Header * ros_message,
  eprosima::fastcdr::Cdr & cdr);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_aicar_msgs
size_t get_serialized_size_key_std_msgs__msg__Header(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_aicar_msgs
size_t max_serialized_size_key_std_msgs__msg__Header(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_aicar_msgs
const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, std_msgs, msg, Header)();


using _LaneInfo__ros_msg_type = aicar_msgs__msg__LaneInfo;


ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_aicar_msgs
bool cdr_serialize_aicar_msgs__msg__LaneInfo(
  const aicar_msgs__msg__LaneInfo * ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Field name: header
  {
    cdr_serialize_std_msgs__msg__Header(
      &ros_message->header, cdr);
  }

  // Field name: left_detect
  {
    cdr << (ros_message->left_detect ? true : false);
  }

  // Field name: left_x
  {
    cdr << ros_message->left_x;
  }

  // Field name: left_angle
  {
    cdr << ros_message->left_angle;
  }

  // Field name: right_detect
  {
    cdr << (ros_message->right_detect ? true : false);
  }

  // Field name: right_x
  {
    cdr << ros_message->right_x;
  }

  // Field name: right_angle
  {
    cdr << ros_message->right_angle;
  }

  // Field name: left_pixel_count
  {
    cdr << ros_message->left_pixel_count;
  }

  // Field name: right_pixel_count
  {
    cdr << ros_message->right_pixel_count;
  }

  return true;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_aicar_msgs
bool cdr_deserialize_aicar_msgs__msg__LaneInfo(
  eprosima::fastcdr::Cdr & cdr,
  aicar_msgs__msg__LaneInfo * ros_message)
{
  // Field name: header
  {
    cdr_deserialize_std_msgs__msg__Header(cdr, &ros_message->header);
  }

  // Field name: left_detect
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message->left_detect = tmp ? true : false;
  }

  // Field name: left_x
  {
    cdr >> ros_message->left_x;
  }

  // Field name: left_angle
  {
    cdr >> ros_message->left_angle;
  }

  // Field name: right_detect
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message->right_detect = tmp ? true : false;
  }

  // Field name: right_x
  {
    cdr >> ros_message->right_x;
  }

  // Field name: right_angle
  {
    cdr >> ros_message->right_angle;
  }

  // Field name: left_pixel_count
  {
    cdr >> ros_message->left_pixel_count;
  }

  // Field name: right_pixel_count
  {
    cdr >> ros_message->right_pixel_count;
  }

  return true;
}  // NOLINT(readability/fn_size)


ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_aicar_msgs
size_t get_serialized_size_aicar_msgs__msg__LaneInfo(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _LaneInfo__ros_msg_type * ros_message = static_cast<const _LaneInfo__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Field name: header
  current_alignment += get_serialized_size_std_msgs__msg__Header(
    &(ros_message->header), current_alignment);

  // Field name: left_detect
  {
    size_t item_size = sizeof(ros_message->left_detect);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: left_x
  {
    size_t item_size = sizeof(ros_message->left_x);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: left_angle
  {
    size_t item_size = sizeof(ros_message->left_angle);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: right_detect
  {
    size_t item_size = sizeof(ros_message->right_detect);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: right_x
  {
    size_t item_size = sizeof(ros_message->right_x);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: right_angle
  {
    size_t item_size = sizeof(ros_message->right_angle);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: left_pixel_count
  {
    size_t item_size = sizeof(ros_message->left_pixel_count);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: right_pixel_count
  {
    size_t item_size = sizeof(ros_message->right_pixel_count);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}


ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_aicar_msgs
size_t max_serialized_size_aicar_msgs__msg__LaneInfo(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;

  // Field name: header
  {
    size_t array_size = 1;
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_std_msgs__msg__Header(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Field name: left_detect
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  // Field name: left_x
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Field name: left_angle
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Field name: right_detect
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  // Field name: right_x
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Field name: right_angle
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Field name: left_pixel_count
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Field name: right_pixel_count
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }


  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = aicar_msgs__msg__LaneInfo;
    is_plain =
      (
      offsetof(DataType, right_pixel_count) +
      last_member_size
      ) == ret_val;
  }
  return ret_val;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_aicar_msgs
bool cdr_serialize_key_aicar_msgs__msg__LaneInfo(
  const aicar_msgs__msg__LaneInfo * ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Field name: header
  {
    cdr_serialize_key_std_msgs__msg__Header(
      &ros_message->header, cdr);
  }

  // Field name: left_detect
  {
    cdr << (ros_message->left_detect ? true : false);
  }

  // Field name: left_x
  {
    cdr << ros_message->left_x;
  }

  // Field name: left_angle
  {
    cdr << ros_message->left_angle;
  }

  // Field name: right_detect
  {
    cdr << (ros_message->right_detect ? true : false);
  }

  // Field name: right_x
  {
    cdr << ros_message->right_x;
  }

  // Field name: right_angle
  {
    cdr << ros_message->right_angle;
  }

  // Field name: left_pixel_count
  {
    cdr << ros_message->left_pixel_count;
  }

  // Field name: right_pixel_count
  {
    cdr << ros_message->right_pixel_count;
  }

  return true;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_aicar_msgs
size_t get_serialized_size_key_aicar_msgs__msg__LaneInfo(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _LaneInfo__ros_msg_type * ros_message = static_cast<const _LaneInfo__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;

  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Field name: header
  current_alignment += get_serialized_size_key_std_msgs__msg__Header(
    &(ros_message->header), current_alignment);

  // Field name: left_detect
  {
    size_t item_size = sizeof(ros_message->left_detect);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: left_x
  {
    size_t item_size = sizeof(ros_message->left_x);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: left_angle
  {
    size_t item_size = sizeof(ros_message->left_angle);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: right_detect
  {
    size_t item_size = sizeof(ros_message->right_detect);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: right_x
  {
    size_t item_size = sizeof(ros_message->right_x);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: right_angle
  {
    size_t item_size = sizeof(ros_message->right_angle);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: left_pixel_count
  {
    size_t item_size = sizeof(ros_message->left_pixel_count);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: right_pixel_count
  {
    size_t item_size = sizeof(ros_message->right_pixel_count);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_aicar_msgs
size_t max_serialized_size_key_aicar_msgs__msg__LaneInfo(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;
  // Field name: header
  {
    size_t array_size = 1;
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_key_std_msgs__msg__Header(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Field name: left_detect
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  // Field name: left_x
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Field name: left_angle
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Field name: right_detect
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  // Field name: right_x
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Field name: right_angle
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Field name: left_pixel_count
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Field name: right_pixel_count
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = aicar_msgs__msg__LaneInfo;
    is_plain =
      (
      offsetof(DataType, right_pixel_count) +
      last_member_size
      ) == ret_val;
  }
  return ret_val;
}


static bool _LaneInfo__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const aicar_msgs__msg__LaneInfo * ros_message = static_cast<const aicar_msgs__msg__LaneInfo *>(untyped_ros_message);
  (void)ros_message;
  return cdr_serialize_aicar_msgs__msg__LaneInfo(ros_message, cdr);
}

static bool _LaneInfo__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  aicar_msgs__msg__LaneInfo * ros_message = static_cast<aicar_msgs__msg__LaneInfo *>(untyped_ros_message);
  (void)ros_message;
  return cdr_deserialize_aicar_msgs__msg__LaneInfo(cdr, ros_message);
}

static uint32_t _LaneInfo__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_aicar_msgs__msg__LaneInfo(
      untyped_ros_message, 0));
}

static size_t _LaneInfo__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_aicar_msgs__msg__LaneInfo(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_LaneInfo = {
  "aicar_msgs::msg",
  "LaneInfo",
  _LaneInfo__cdr_serialize,
  _LaneInfo__cdr_deserialize,
  _LaneInfo__get_serialized_size,
  _LaneInfo__max_serialized_size,
  nullptr
};

static rosidl_message_type_support_t _LaneInfo__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_LaneInfo,
  get_message_typesupport_handle_function,
  &aicar_msgs__msg__LaneInfo__get_type_hash,
  &aicar_msgs__msg__LaneInfo__get_type_description,
  &aicar_msgs__msg__LaneInfo__get_type_description_sources,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, aicar_msgs, msg, LaneInfo)() {
  return &_LaneInfo__type_support;
}

#if defined(__cplusplus)
}
#endif
