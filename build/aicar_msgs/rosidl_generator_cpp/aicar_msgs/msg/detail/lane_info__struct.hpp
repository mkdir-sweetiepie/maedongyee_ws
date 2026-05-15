// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from aicar_msgs:msg/LaneInfo.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "aicar_msgs/msg/lane_info.hpp"


#ifndef AICAR_MSGS__MSG__DETAIL__LANE_INFO__STRUCT_HPP_
#define AICAR_MSGS__MSG__DETAIL__LANE_INFO__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__aicar_msgs__msg__LaneInfo __attribute__((deprecated))
#else
# define DEPRECATED__aicar_msgs__msg__LaneInfo __declspec(deprecated)
#endif

namespace aicar_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct LaneInfo_
{
  using Type = LaneInfo_<ContainerAllocator>;

  explicit LaneInfo_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->left_detect = false;
      this->left_x = 0.0f;
      this->left_angle = 0.0f;
      this->right_detect = false;
      this->right_x = 0.0f;
      this->right_angle = 0.0f;
      this->left_pixel_count = 0l;
      this->right_pixel_count = 0l;
    }
  }

  explicit LaneInfo_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->left_detect = false;
      this->left_x = 0.0f;
      this->left_angle = 0.0f;
      this->right_detect = false;
      this->right_x = 0.0f;
      this->right_angle = 0.0f;
      this->left_pixel_count = 0l;
      this->right_pixel_count = 0l;
    }
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _left_detect_type =
    bool;
  _left_detect_type left_detect;
  using _left_x_type =
    float;
  _left_x_type left_x;
  using _left_angle_type =
    float;
  _left_angle_type left_angle;
  using _right_detect_type =
    bool;
  _right_detect_type right_detect;
  using _right_x_type =
    float;
  _right_x_type right_x;
  using _right_angle_type =
    float;
  _right_angle_type right_angle;
  using _left_pixel_count_type =
    int32_t;
  _left_pixel_count_type left_pixel_count;
  using _right_pixel_count_type =
    int32_t;
  _right_pixel_count_type right_pixel_count;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__left_detect(
    const bool & _arg)
  {
    this->left_detect = _arg;
    return *this;
  }
  Type & set__left_x(
    const float & _arg)
  {
    this->left_x = _arg;
    return *this;
  }
  Type & set__left_angle(
    const float & _arg)
  {
    this->left_angle = _arg;
    return *this;
  }
  Type & set__right_detect(
    const bool & _arg)
  {
    this->right_detect = _arg;
    return *this;
  }
  Type & set__right_x(
    const float & _arg)
  {
    this->right_x = _arg;
    return *this;
  }
  Type & set__right_angle(
    const float & _arg)
  {
    this->right_angle = _arg;
    return *this;
  }
  Type & set__left_pixel_count(
    const int32_t & _arg)
  {
    this->left_pixel_count = _arg;
    return *this;
  }
  Type & set__right_pixel_count(
    const int32_t & _arg)
  {
    this->right_pixel_count = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    aicar_msgs::msg::LaneInfo_<ContainerAllocator> *;
  using ConstRawPtr =
    const aicar_msgs::msg::LaneInfo_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<aicar_msgs::msg::LaneInfo_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<aicar_msgs::msg::LaneInfo_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      aicar_msgs::msg::LaneInfo_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<aicar_msgs::msg::LaneInfo_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      aicar_msgs::msg::LaneInfo_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<aicar_msgs::msg::LaneInfo_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<aicar_msgs::msg::LaneInfo_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<aicar_msgs::msg::LaneInfo_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__aicar_msgs__msg__LaneInfo
    std::shared_ptr<aicar_msgs::msg::LaneInfo_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__aicar_msgs__msg__LaneInfo
    std::shared_ptr<aicar_msgs::msg::LaneInfo_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const LaneInfo_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->left_detect != other.left_detect) {
      return false;
    }
    if (this->left_x != other.left_x) {
      return false;
    }
    if (this->left_angle != other.left_angle) {
      return false;
    }
    if (this->right_detect != other.right_detect) {
      return false;
    }
    if (this->right_x != other.right_x) {
      return false;
    }
    if (this->right_angle != other.right_angle) {
      return false;
    }
    if (this->left_pixel_count != other.left_pixel_count) {
      return false;
    }
    if (this->right_pixel_count != other.right_pixel_count) {
      return false;
    }
    return true;
  }
  bool operator!=(const LaneInfo_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct LaneInfo_

// alias to use template instance with default allocator
using LaneInfo =
  aicar_msgs::msg::LaneInfo_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace aicar_msgs

#endif  // AICAR_MSGS__MSG__DETAIL__LANE_INFO__STRUCT_HPP_
