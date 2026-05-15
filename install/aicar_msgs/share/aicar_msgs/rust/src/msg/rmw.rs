#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};


#[link(name = "aicar_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__aicar_msgs__msg__LaneInfo() -> *const std::ffi::c_void;
}

#[link(name = "aicar_msgs__rosidl_generator_c")]
extern "C" {
    fn aicar_msgs__msg__LaneInfo__init(msg: *mut LaneInfo) -> bool;
    fn aicar_msgs__msg__LaneInfo__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<LaneInfo>, size: usize) -> bool;
    fn aicar_msgs__msg__LaneInfo__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<LaneInfo>);
    fn aicar_msgs__msg__LaneInfo__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<LaneInfo>, out_seq: *mut rosidl_runtime_rs::Sequence<LaneInfo>) -> bool;
}

// Corresponds to aicar_msgs__msg__LaneInfo
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct LaneInfo {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::rmw::Header,

    /// Left lane info
    pub left_detect: bool,

    /// x position at bottom of BEV
    pub left_x: f32,

    /// line angle, 90 = vertical
    pub left_angle: f32,

    /// Right lane info
    pub right_detect: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub right_x: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub right_angle: f32,

    /// Quality (optional debug)
    pub left_pixel_count: i32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub right_pixel_count: i32,

}



impl Default for LaneInfo {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !aicar_msgs__msg__LaneInfo__init(&mut msg as *mut _) {
        panic!("Call to aicar_msgs__msg__LaneInfo__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for LaneInfo {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aicar_msgs__msg__LaneInfo__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aicar_msgs__msg__LaneInfo__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aicar_msgs__msg__LaneInfo__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for LaneInfo {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for LaneInfo where Self: Sized {
  const TYPE_NAME: &'static str = "aicar_msgs/msg/LaneInfo";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__aicar_msgs__msg__LaneInfo() }
  }
}


