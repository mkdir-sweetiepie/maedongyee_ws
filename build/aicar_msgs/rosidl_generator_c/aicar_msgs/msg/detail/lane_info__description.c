// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from aicar_msgs:msg/LaneInfo.idl
// generated code does not contain a copyright notice

#include "aicar_msgs/msg/detail/lane_info__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_aicar_msgs
const rosidl_type_hash_t *
aicar_msgs__msg__LaneInfo__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x79, 0x10, 0xf8, 0xdd, 0xe3, 0x69, 0xdf, 0x62,
      0x50, 0x50, 0x6c, 0x12, 0x0e, 0xd7, 0xe7, 0x34,
      0x51, 0x62, 0x10, 0xd2, 0xec, 0x4c, 0x8d, 0xf1,
      0x33, 0xac, 0x20, 0x25, 0x51, 0x7f, 0x6d, 0x58,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types
#include "std_msgs/msg/detail/header__functions.h"
#include "builtin_interfaces/msg/detail/time__functions.h"

// Hashes for external referenced types
#ifndef NDEBUG
static const rosidl_type_hash_t builtin_interfaces__msg__Time__EXPECTED_HASH = {1, {
    0xb1, 0x06, 0x23, 0x5e, 0x25, 0xa4, 0xc5, 0xed,
    0x35, 0x09, 0x8a, 0xa0, 0xa6, 0x1a, 0x3e, 0xe9,
    0xc9, 0xb1, 0x8d, 0x19, 0x7f, 0x39, 0x8b, 0x0e,
    0x42, 0x06, 0xce, 0xa9, 0xac, 0xf9, 0xc1, 0x97,
  }};
static const rosidl_type_hash_t std_msgs__msg__Header__EXPECTED_HASH = {1, {
    0xf4, 0x9f, 0xb3, 0xae, 0x2c, 0xf0, 0x70, 0xf7,
    0x93, 0x64, 0x5f, 0xf7, 0x49, 0x68, 0x3a, 0xc6,
    0xb0, 0x62, 0x03, 0xe4, 0x1c, 0x89, 0x1e, 0x17,
    0x70, 0x1b, 0x1c, 0xb5, 0x97, 0xce, 0x6a, 0x01,
  }};
#endif

static char aicar_msgs__msg__LaneInfo__TYPE_NAME[] = "aicar_msgs/msg/LaneInfo";
static char builtin_interfaces__msg__Time__TYPE_NAME[] = "builtin_interfaces/msg/Time";
static char std_msgs__msg__Header__TYPE_NAME[] = "std_msgs/msg/Header";

// Define type names, field names, and default values
static char aicar_msgs__msg__LaneInfo__FIELD_NAME__header[] = "header";
static char aicar_msgs__msg__LaneInfo__FIELD_NAME__left_detect[] = "left_detect";
static char aicar_msgs__msg__LaneInfo__FIELD_NAME__left_x[] = "left_x";
static char aicar_msgs__msg__LaneInfo__FIELD_NAME__left_angle[] = "left_angle";
static char aicar_msgs__msg__LaneInfo__FIELD_NAME__right_detect[] = "right_detect";
static char aicar_msgs__msg__LaneInfo__FIELD_NAME__right_x[] = "right_x";
static char aicar_msgs__msg__LaneInfo__FIELD_NAME__right_angle[] = "right_angle";
static char aicar_msgs__msg__LaneInfo__FIELD_NAME__left_pixel_count[] = "left_pixel_count";
static char aicar_msgs__msg__LaneInfo__FIELD_NAME__right_pixel_count[] = "right_pixel_count";

static rosidl_runtime_c__type_description__Field aicar_msgs__msg__LaneInfo__FIELDS[] = {
  {
    {aicar_msgs__msg__LaneInfo__FIELD_NAME__header, 6, 6},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {std_msgs__msg__Header__TYPE_NAME, 19, 19},
    },
    {NULL, 0, 0},
  },
  {
    {aicar_msgs__msg__LaneInfo__FIELD_NAME__left_detect, 11, 11},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_BOOLEAN,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {aicar_msgs__msg__LaneInfo__FIELD_NAME__left_x, 6, 6},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {aicar_msgs__msg__LaneInfo__FIELD_NAME__left_angle, 10, 10},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {aicar_msgs__msg__LaneInfo__FIELD_NAME__right_detect, 12, 12},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_BOOLEAN,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {aicar_msgs__msg__LaneInfo__FIELD_NAME__right_x, 7, 7},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {aicar_msgs__msg__LaneInfo__FIELD_NAME__right_angle, 11, 11},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {aicar_msgs__msg__LaneInfo__FIELD_NAME__left_pixel_count, 16, 16},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_INT32,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {aicar_msgs__msg__LaneInfo__FIELD_NAME__right_pixel_count, 17, 17},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_INT32,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
};

static rosidl_runtime_c__type_description__IndividualTypeDescription aicar_msgs__msg__LaneInfo__REFERENCED_TYPE_DESCRIPTIONS[] = {
  {
    {builtin_interfaces__msg__Time__TYPE_NAME, 27, 27},
    {NULL, 0, 0},
  },
  {
    {std_msgs__msg__Header__TYPE_NAME, 19, 19},
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
aicar_msgs__msg__LaneInfo__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {aicar_msgs__msg__LaneInfo__TYPE_NAME, 23, 23},
      {aicar_msgs__msg__LaneInfo__FIELDS, 9, 9},
    },
    {aicar_msgs__msg__LaneInfo__REFERENCED_TYPE_DESCRIPTIONS, 2, 2},
  };
  if (!constructed) {
    assert(0 == memcmp(&builtin_interfaces__msg__Time__EXPECTED_HASH, builtin_interfaces__msg__Time__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[0].fields = builtin_interfaces__msg__Time__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&std_msgs__msg__Header__EXPECTED_HASH, std_msgs__msg__Header__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[1].fields = std_msgs__msg__Header__get_type_description(NULL)->type_description.fields;
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "std_msgs/Header header\n"
  "\n"
  "# Left lane info\n"
  "bool   left_detect\n"
  "float32 left_x        # x position at bottom of BEV [pixels]\n"
  "float32 left_angle    # line angle [degrees], 90 = vertical\n"
  "\n"
  "# Right lane info\n"
  "bool   right_detect\n"
  "float32 right_x\n"
  "float32 right_angle\n"
  "\n"
  "# Quality (optional debug)\n"
  "int32   left_pixel_count\n"
  "int32   right_pixel_count";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
aicar_msgs__msg__LaneInfo__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {aicar_msgs__msg__LaneInfo__TYPE_NAME, 23, 23},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 335, 335},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
aicar_msgs__msg__LaneInfo__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[3];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 3, 3};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *aicar_msgs__msg__LaneInfo__get_individual_type_description_source(NULL),
    sources[1] = *builtin_interfaces__msg__Time__get_individual_type_description_source(NULL);
    sources[2] = *std_msgs__msg__Header__get_individual_type_description_source(NULL);
    constructed = true;
  }
  return &source_sequence;
}
