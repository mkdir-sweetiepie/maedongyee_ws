// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from aicar_msgs:msg/LaneInfo.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "aicar_msgs/msg/lane_info.hpp"


#ifndef AICAR_MSGS__MSG__DETAIL__LANE_INFO__TRAITS_HPP_
#define AICAR_MSGS__MSG__DETAIL__LANE_INFO__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "aicar_msgs/msg/detail/lane_info__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"

namespace aicar_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const LaneInfo & msg,
  std::ostream & out)
{
  out << "{";
  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
    out << ", ";
  }

  // member: left_detect
  {
    out << "left_detect: ";
    rosidl_generator_traits::value_to_yaml(msg.left_detect, out);
    out << ", ";
  }

  // member: left_x
  {
    out << "left_x: ";
    rosidl_generator_traits::value_to_yaml(msg.left_x, out);
    out << ", ";
  }

  // member: left_angle
  {
    out << "left_angle: ";
    rosidl_generator_traits::value_to_yaml(msg.left_angle, out);
    out << ", ";
  }

  // member: right_detect
  {
    out << "right_detect: ";
    rosidl_generator_traits::value_to_yaml(msg.right_detect, out);
    out << ", ";
  }

  // member: right_x
  {
    out << "right_x: ";
    rosidl_generator_traits::value_to_yaml(msg.right_x, out);
    out << ", ";
  }

  // member: right_angle
  {
    out << "right_angle: ";
    rosidl_generator_traits::value_to_yaml(msg.right_angle, out);
    out << ", ";
  }

  // member: left_pixel_count
  {
    out << "left_pixel_count: ";
    rosidl_generator_traits::value_to_yaml(msg.left_pixel_count, out);
    out << ", ";
  }

  // member: right_pixel_count
  {
    out << "right_pixel_count: ";
    rosidl_generator_traits::value_to_yaml(msg.right_pixel_count, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const LaneInfo & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: header
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "header:\n";
    to_block_style_yaml(msg.header, out, indentation + 2);
  }

  // member: left_detect
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "left_detect: ";
    rosidl_generator_traits::value_to_yaml(msg.left_detect, out);
    out << "\n";
  }

  // member: left_x
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "left_x: ";
    rosidl_generator_traits::value_to_yaml(msg.left_x, out);
    out << "\n";
  }

  // member: left_angle
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "left_angle: ";
    rosidl_generator_traits::value_to_yaml(msg.left_angle, out);
    out << "\n";
  }

  // member: right_detect
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "right_detect: ";
    rosidl_generator_traits::value_to_yaml(msg.right_detect, out);
    out << "\n";
  }

  // member: right_x
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "right_x: ";
    rosidl_generator_traits::value_to_yaml(msg.right_x, out);
    out << "\n";
  }

  // member: right_angle
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "right_angle: ";
    rosidl_generator_traits::value_to_yaml(msg.right_angle, out);
    out << "\n";
  }

  // member: left_pixel_count
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "left_pixel_count: ";
    rosidl_generator_traits::value_to_yaml(msg.left_pixel_count, out);
    out << "\n";
  }

  // member: right_pixel_count
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "right_pixel_count: ";
    rosidl_generator_traits::value_to_yaml(msg.right_pixel_count, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const LaneInfo & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace aicar_msgs

namespace rosidl_generator_traits
{

[[deprecated("use aicar_msgs::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const aicar_msgs::msg::LaneInfo & msg,
  std::ostream & out, size_t indentation = 0)
{
  aicar_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use aicar_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const aicar_msgs::msg::LaneInfo & msg)
{
  return aicar_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<aicar_msgs::msg::LaneInfo>()
{
  return "aicar_msgs::msg::LaneInfo";
}

template<>
inline const char * name<aicar_msgs::msg::LaneInfo>()
{
  return "aicar_msgs/msg/LaneInfo";
}

template<>
struct has_fixed_size<aicar_msgs::msg::LaneInfo>
  : std::integral_constant<bool, has_fixed_size<std_msgs::msg::Header>::value> {};

template<>
struct has_bounded_size<aicar_msgs::msg::LaneInfo>
  : std::integral_constant<bool, has_bounded_size<std_msgs::msg::Header>::value> {};

template<>
struct is_message<aicar_msgs::msg::LaneInfo>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // AICAR_MSGS__MSG__DETAIL__LANE_INFO__TRAITS_HPP_
