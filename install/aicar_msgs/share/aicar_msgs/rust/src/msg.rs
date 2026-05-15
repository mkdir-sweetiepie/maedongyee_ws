#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



// Corresponds to aicar_msgs__msg__LaneInfo

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct LaneInfo {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::Header,

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
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::LaneInfo::default())
  }
}

impl rosidl_runtime_rs::Message for LaneInfo {
  type RmwMsg = super::msg::rmw::LaneInfo;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Owned(msg.header)).into_owned(),
        left_detect: msg.left_detect,
        left_x: msg.left_x,
        left_angle: msg.left_angle,
        right_detect: msg.right_detect,
        right_x: msg.right_x,
        right_angle: msg.right_angle,
        left_pixel_count: msg.left_pixel_count,
        right_pixel_count: msg.right_pixel_count,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Borrowed(&msg.header)).into_owned(),
      left_detect: msg.left_detect,
      left_x: msg.left_x,
      left_angle: msg.left_angle,
      right_detect: msg.right_detect,
      right_x: msg.right_x,
      right_angle: msg.right_angle,
      left_pixel_count: msg.left_pixel_count,
      right_pixel_count: msg.right_pixel_count,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      header: std_msgs::msg::Header::from_rmw_message(msg.header),
      left_detect: msg.left_detect,
      left_x: msg.left_x,
      left_angle: msg.left_angle,
      right_detect: msg.right_detect,
      right_x: msg.right_x,
      right_angle: msg.right_angle,
      left_pixel_count: msg.left_pixel_count,
      right_pixel_count: msg.right_pixel_count,
    }
  }
}


