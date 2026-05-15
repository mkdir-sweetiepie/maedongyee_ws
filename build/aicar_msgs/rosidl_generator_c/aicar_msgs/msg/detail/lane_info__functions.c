// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from aicar_msgs:msg/LaneInfo.idl
// generated code does not contain a copyright notice
#include "aicar_msgs/msg/detail/lane_info__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"

bool
aicar_msgs__msg__LaneInfo__init(aicar_msgs__msg__LaneInfo * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    aicar_msgs__msg__LaneInfo__fini(msg);
    return false;
  }
  // left_detect
  // left_x
  // left_angle
  // right_detect
  // right_x
  // right_angle
  // left_pixel_count
  // right_pixel_count
  return true;
}

void
aicar_msgs__msg__LaneInfo__fini(aicar_msgs__msg__LaneInfo * msg)
{
  if (!msg) {
    return;
  }
  // header
  std_msgs__msg__Header__fini(&msg->header);
  // left_detect
  // left_x
  // left_angle
  // right_detect
  // right_x
  // right_angle
  // left_pixel_count
  // right_pixel_count
}

bool
aicar_msgs__msg__LaneInfo__are_equal(const aicar_msgs__msg__LaneInfo * lhs, const aicar_msgs__msg__LaneInfo * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__are_equal(
      &(lhs->header), &(rhs->header)))
  {
    return false;
  }
  // left_detect
  if (lhs->left_detect != rhs->left_detect) {
    return false;
  }
  // left_x
  if (lhs->left_x != rhs->left_x) {
    return false;
  }
  // left_angle
  if (lhs->left_angle != rhs->left_angle) {
    return false;
  }
  // right_detect
  if (lhs->right_detect != rhs->right_detect) {
    return false;
  }
  // right_x
  if (lhs->right_x != rhs->right_x) {
    return false;
  }
  // right_angle
  if (lhs->right_angle != rhs->right_angle) {
    return false;
  }
  // left_pixel_count
  if (lhs->left_pixel_count != rhs->left_pixel_count) {
    return false;
  }
  // right_pixel_count
  if (lhs->right_pixel_count != rhs->right_pixel_count) {
    return false;
  }
  return true;
}

bool
aicar_msgs__msg__LaneInfo__copy(
  const aicar_msgs__msg__LaneInfo * input,
  aicar_msgs__msg__LaneInfo * output)
{
  if (!input || !output) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__copy(
      &(input->header), &(output->header)))
  {
    return false;
  }
  // left_detect
  output->left_detect = input->left_detect;
  // left_x
  output->left_x = input->left_x;
  // left_angle
  output->left_angle = input->left_angle;
  // right_detect
  output->right_detect = input->right_detect;
  // right_x
  output->right_x = input->right_x;
  // right_angle
  output->right_angle = input->right_angle;
  // left_pixel_count
  output->left_pixel_count = input->left_pixel_count;
  // right_pixel_count
  output->right_pixel_count = input->right_pixel_count;
  return true;
}

aicar_msgs__msg__LaneInfo *
aicar_msgs__msg__LaneInfo__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aicar_msgs__msg__LaneInfo * msg = (aicar_msgs__msg__LaneInfo *)allocator.allocate(sizeof(aicar_msgs__msg__LaneInfo), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(aicar_msgs__msg__LaneInfo));
  bool success = aicar_msgs__msg__LaneInfo__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
aicar_msgs__msg__LaneInfo__destroy(aicar_msgs__msg__LaneInfo * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    aicar_msgs__msg__LaneInfo__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
aicar_msgs__msg__LaneInfo__Sequence__init(aicar_msgs__msg__LaneInfo__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aicar_msgs__msg__LaneInfo * data = NULL;

  if (size) {
    data = (aicar_msgs__msg__LaneInfo *)allocator.zero_allocate(size, sizeof(aicar_msgs__msg__LaneInfo), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = aicar_msgs__msg__LaneInfo__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        aicar_msgs__msg__LaneInfo__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
aicar_msgs__msg__LaneInfo__Sequence__fini(aicar_msgs__msg__LaneInfo__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      aicar_msgs__msg__LaneInfo__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

aicar_msgs__msg__LaneInfo__Sequence *
aicar_msgs__msg__LaneInfo__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aicar_msgs__msg__LaneInfo__Sequence * array = (aicar_msgs__msg__LaneInfo__Sequence *)allocator.allocate(sizeof(aicar_msgs__msg__LaneInfo__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = aicar_msgs__msg__LaneInfo__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
aicar_msgs__msg__LaneInfo__Sequence__destroy(aicar_msgs__msg__LaneInfo__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    aicar_msgs__msg__LaneInfo__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
aicar_msgs__msg__LaneInfo__Sequence__are_equal(const aicar_msgs__msg__LaneInfo__Sequence * lhs, const aicar_msgs__msg__LaneInfo__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!aicar_msgs__msg__LaneInfo__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
aicar_msgs__msg__LaneInfo__Sequence__copy(
  const aicar_msgs__msg__LaneInfo__Sequence * input,
  aicar_msgs__msg__LaneInfo__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(aicar_msgs__msg__LaneInfo);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    aicar_msgs__msg__LaneInfo * data =
      (aicar_msgs__msg__LaneInfo *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!aicar_msgs__msg__LaneInfo__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          aicar_msgs__msg__LaneInfo__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!aicar_msgs__msg__LaneInfo__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
