// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from aicar_msgs:msg/LaneInfo.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "aicar_msgs/msg/lane_info.hpp"


#ifndef AICAR_MSGS__MSG__DETAIL__LANE_INFO__BUILDER_HPP_
#define AICAR_MSGS__MSG__DETAIL__LANE_INFO__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "aicar_msgs/msg/detail/lane_info__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace aicar_msgs
{

namespace msg
{

namespace builder
{

class Init_LaneInfo_right_pixel_count
{
public:
  explicit Init_LaneInfo_right_pixel_count(::aicar_msgs::msg::LaneInfo & msg)
  : msg_(msg)
  {}
  ::aicar_msgs::msg::LaneInfo right_pixel_count(::aicar_msgs::msg::LaneInfo::_right_pixel_count_type arg)
  {
    msg_.right_pixel_count = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aicar_msgs::msg::LaneInfo msg_;
};

class Init_LaneInfo_left_pixel_count
{
public:
  explicit Init_LaneInfo_left_pixel_count(::aicar_msgs::msg::LaneInfo & msg)
  : msg_(msg)
  {}
  Init_LaneInfo_right_pixel_count left_pixel_count(::aicar_msgs::msg::LaneInfo::_left_pixel_count_type arg)
  {
    msg_.left_pixel_count = std::move(arg);
    return Init_LaneInfo_right_pixel_count(msg_);
  }

private:
  ::aicar_msgs::msg::LaneInfo msg_;
};

class Init_LaneInfo_right_angle
{
public:
  explicit Init_LaneInfo_right_angle(::aicar_msgs::msg::LaneInfo & msg)
  : msg_(msg)
  {}
  Init_LaneInfo_left_pixel_count right_angle(::aicar_msgs::msg::LaneInfo::_right_angle_type arg)
  {
    msg_.right_angle = std::move(arg);
    return Init_LaneInfo_left_pixel_count(msg_);
  }

private:
  ::aicar_msgs::msg::LaneInfo msg_;
};

class Init_LaneInfo_right_x
{
public:
  explicit Init_LaneInfo_right_x(::aicar_msgs::msg::LaneInfo & msg)
  : msg_(msg)
  {}
  Init_LaneInfo_right_angle right_x(::aicar_msgs::msg::LaneInfo::_right_x_type arg)
  {
    msg_.right_x = std::move(arg);
    return Init_LaneInfo_right_angle(msg_);
  }

private:
  ::aicar_msgs::msg::LaneInfo msg_;
};

class Init_LaneInfo_right_detect
{
public:
  explicit Init_LaneInfo_right_detect(::aicar_msgs::msg::LaneInfo & msg)
  : msg_(msg)
  {}
  Init_LaneInfo_right_x right_detect(::aicar_msgs::msg::LaneInfo::_right_detect_type arg)
  {
    msg_.right_detect = std::move(arg);
    return Init_LaneInfo_right_x(msg_);
  }

private:
  ::aicar_msgs::msg::LaneInfo msg_;
};

class Init_LaneInfo_left_angle
{
public:
  explicit Init_LaneInfo_left_angle(::aicar_msgs::msg::LaneInfo & msg)
  : msg_(msg)
  {}
  Init_LaneInfo_right_detect left_angle(::aicar_msgs::msg::LaneInfo::_left_angle_type arg)
  {
    msg_.left_angle = std::move(arg);
    return Init_LaneInfo_right_detect(msg_);
  }

private:
  ::aicar_msgs::msg::LaneInfo msg_;
};

class Init_LaneInfo_left_x
{
public:
  explicit Init_LaneInfo_left_x(::aicar_msgs::msg::LaneInfo & msg)
  : msg_(msg)
  {}
  Init_LaneInfo_left_angle left_x(::aicar_msgs::msg::LaneInfo::_left_x_type arg)
  {
    msg_.left_x = std::move(arg);
    return Init_LaneInfo_left_angle(msg_);
  }

private:
  ::aicar_msgs::msg::LaneInfo msg_;
};

class Init_LaneInfo_left_detect
{
public:
  explicit Init_LaneInfo_left_detect(::aicar_msgs::msg::LaneInfo & msg)
  : msg_(msg)
  {}
  Init_LaneInfo_left_x left_detect(::aicar_msgs::msg::LaneInfo::_left_detect_type arg)
  {
    msg_.left_detect = std::move(arg);
    return Init_LaneInfo_left_x(msg_);
  }

private:
  ::aicar_msgs::msg::LaneInfo msg_;
};

class Init_LaneInfo_header
{
public:
  Init_LaneInfo_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_LaneInfo_left_detect header(::aicar_msgs::msg::LaneInfo::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_LaneInfo_left_detect(msg_);
  }

private:
  ::aicar_msgs::msg::LaneInfo msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::aicar_msgs::msg::LaneInfo>()
{
  return aicar_msgs::msg::builder::Init_LaneInfo_header();
}

}  // namespace aicar_msgs

#endif  // AICAR_MSGS__MSG__DETAIL__LANE_INFO__BUILDER_HPP_
