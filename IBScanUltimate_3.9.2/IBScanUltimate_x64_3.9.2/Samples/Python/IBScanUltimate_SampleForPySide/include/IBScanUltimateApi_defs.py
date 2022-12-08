import sys
from ctypes import *
from enum import Enum
from include.IBScanUltimate import *

'''
****************************************************************************************************
* IBScanUltimateApi_defs.h
*
* DESCRIPTION:
*     API structures and constants for IBScanUltimate.
*     http://www.integratedbiometrics.com
*
* NOTES:
*     Copyright (c) Integrated Biometrics, 2009-2017
*
* HISTORY:
*     2012/04/06  1.0.0  Created.
*     2012/05/29  1.1.0  Added callback function (IBSU_CallbackAsyncOpenDevice).
*     2012/09/05  1.3.0  Added enumeration value to IBSU_PropertyId
*                            (ENUM_IBSU_PROPERTY_ENABLE_POWER_SAVE_MODE)
*                        Modified IBSU_DeviceDesc structure for Android.
*     2012/11/06  1.4.1  Added enumeration for RollingState (IBSU_RollingState).
*     2013/02/01  1.5.0  Added enumeration value to IBSU_ImageType (ENUM_IBSU_FLAT_FOUR_FINGERS)
*                        Added enumeration value to IBSU_PropertyId
*                            (ENUM_IBSU_PROPERTY_RETRY_WRONG_COMMUNICATION)
*                        Added callback function (IBSU_CallbackNotifyMessage)
*     2013/03/20  1.6.0  Added new enumerations & structures to support IBScanMatcher integration
*                            (IBSM_ImageFormat, IBSM_ImpressionType, IBSM_FingerPosition,
*                             IBSM_CaptureDeviceTechID, IBSM_CaptureDeviceTypeID,
*                             IBSM_CaptureDeviceVendorID, IBSM_ImageData)
*     2013/07/31  1.6.8  Added new defines to support Curve (TBN240) LEDs (IBSU_LED_SCAN_CURVE_RED,
*                             IBSU_LED_SCAN_CURVE_GREEN, IBSU_LED_SCAN_CURVE_BLUE)
*     2013/08/03  1.6.9  Reformatted.
*     2013/10/14  1.7.0  Added new defines to support image segmentation and bitmap header.
*                            (IBSU_MAX_SEGMENT_COUNT, IBSU_BMP_GRAY_HEADER_LEN, IBSU_BMP_RGB24_HEADER_LEN,
*                             IBSU_BMP_RGB32_HEADER_LEN)
*                        Added a new structure to support image segmentation.
*                            (IBSU_SegmentPosition)
*                        Added new items in existing enumerations to support capture timeout,
*                        roll-figerprint's width, draw arrow, getting the scale of the displayed
*                        image, getting the left/top margin of the display, showing invalid finger
*                        position area of top/left/right, and identifying the extended result image
*                        available callback.
*                        Added new enumeration to make overlay object on client window.
*                            (IBSU_OverlayShapePattern)
*                        Added new callback function (IBSU_CallbackResultImageEx)
*     2014/02/25  1.7.1  Added enumeration value to IBSU_PropertyId
*                            (ENUM_IBSU_PROPERTY_ROLL_MODE,ENUM_IBSU_PROPERTY_ROLL_LEVEL )
*     2014/06/19  1.7.3  Added enumeration value to IBSU_ClientWindowPropertyId
*                            (ENUM_IBSU_WINDOW_PROPERTY_ROLL_GUIDE_LINE_WIDTH )
*     2015/03/04  1.8.3  Reformatted to support UNICODE for WinCE
*                        Added enumeration value to IBSU_PropertyId
*                            (ENUM_IBSU_PROPERTY_CAPTURE_AREA_THRESHOLD, ENUM_IBSU_PROPERTY_ENABLE_DECIMATION )
*                        Added enumeration value to IBSU_ClientWindowPropertyId
*                            (ENUM_IBSU_WINDOW_PROPERTY_SCALE_FACTOR_EX )
*                        Added reserved feature on ENUM_IBSU_PROPERTY_RESERVED_1
*     2015/04/07  1.8.4  Added enumeration value to IBSU_PropertyId
*                            (ENUM_IBSU_PROPERTY_ENABLE_CAPTURE_ON_RELEASE, ENUM_IBSU_PROPERTY_DEVICE_INDEX,
*                             ENUM_IBSU_PROPERTY_DEVICE_ID )
*                        Added reserved enumeration value to IBSU_PropertyId
*                            (ENUM_IBSU_PROPERTY_RESERVED_IMAGE_PROCESS_THRESHOLD )
*     2015/08/05  1.8.5  Added enumeration value to IBSU_ClientWindowPropertyId
*                            (ENUM_IBSU_WINDOW_PROPERTY_KEEP_REDRAW_LAST_IMAGE )
*                        Added new enumerations to support Image combine
*                            (IBSU_CombineImageWhichHand )
*     2015/12/11  1.9.0  Added additional LED definitions for Kojak.
*                        Added enumeration value to IBSU_ImageType
*                            (ENUM_IBSU_FLAT_THREE_FINGERS )
*                        Added enumeration value to IBSU_PropertyId
*                            (ENUM_IBSU_PROPERTY_SUPER_DRY_MODE )
*                        Added enumeration value to IBSU_LedType
*                            (ENUM_IBSU_LED_TYPE_FSCAN )
*                        Added enumeration for beeper
*                            (IBSU_BeeperType, IBSU_BeepPattern )
*                        Added enumeration value to IBSM_CaptureDeviceTypeID
*                            (IBSM_CAPTURE_DEVICE_TYPE_ID_KOJAK )
*                        Added new callback function (IBSU_CallbackKeyButtons)
*     2016/01/21  1.9.2  Added enumeration value to IBSU_PropertyId
*                            (ENUM_IBSU_PROPERTY_MIN_CAPTURE_TIME_IN_SUPER_DRY_MODE )
*     2016/04/20  1.9.3  Added enumeration value to IBSU_PropertyId
*                            (ENUM_IBSU_PROPERTY_ROLLED_IMAGE_WIDTH, ENUM_IBSU_PROPERTY_ROLLED_IMAGE_HEIGHT )
*     2016/09/22  1.9.4  Added enumeration value to IBSU_PropertyId
*                            (ENUM_IBSU_PROPERTY_NO_PREVIEW_IMAGE, ENUM_IBSU_PROPERTY_ROLL_IMAGE_OVERRIDE )
*     2017/04/27  1.9.7  Added enumeration value to IBSU_PropertyId
*                            (ENUM_IBSU_PROPERTY_WARNING_MESSAGE_INVALID_AREA, ENUM_IBSU_PROPERTY_ENABLE_WET_FINGER_DETECT,
*                             ENUM_IBSU_PROPERTY_WET_FINGER_DETECT_LEVEL)
*                        Added enumeration value to IBSU_FingerQualityState
*                            (ENUM_IBSU_QUALITY_INVALID_AREA_BOTTOM )
*     2017/06/16  1.9.8  Added enumeration value to IBSU_PropertyId
*                            (ENUM_IBSU_PROPERTY_WET_FINGER_DETECT_LEVEL_THRESHOLD,
*                             ENUM_IBSU_PROPERTY_START_POSITION_OF_ROLLING_AREA,
*	                          ENUM_IBSU_PROPERTY_START_ROLL_WITHOUT_LOCK,
*                             ENUM_IBSU_PROPERTY_ENABLE_TOF,
*                             ENUM_IBSU_PROPERTY_RESERVED_ENABLE_TOF_FOR_ROLL,
*                             ENUM_IBSU_PROPERTY_RESERVED_CAPTURE_BRIGHTNESS_THRESHOLD_FOR_FLAT,
*                             ENUM_IBSU_PROPERTY_RESERVED_CAPTURE_BRIGHTNESS_THRESHOLD_FOR_ROLL,
*                             ENUM_IBSU_PROPERTY_RESERVED_ENHANCED_RESULT_IMAGE)
*     2017/12/05  1.10.0 Added enumeration value to IBSU_PropertyId
*                            (ENUM_IBSU_PROPERTY_ENABLE_ENCRYPTION) 
*     2018/04/27  2.0.1  Deprecated enumeration
*                            (IBSM_FingerPosition)
*     2019/06/21  3.0.0  Added IBSU_EncryptionMode.
*     					 Added enumeration value to IBSU_PropertyId
*							 (ENUM_IBSU_PROPERTY_VIEW_ENCRYPTION_IMAGE_MODE)
*     2019/10/25  3.1.1  Added enumeration value to IBSU_PropertyId
*                            (ENUM_IBSU_PROPERTY_FINGERPRINT_SEGMENTATION_MODE)
*     2020/01/09  3.2.0  Added enumeration value to IBSU_PropertyId
*                            (ENUM_IBSU_PROPERTY_IS_SPOOF_SUPPORTED,
*							  ENUM_IBSU_PROPERTY_ENABLE_SPOOF,
*							  ENUM_IBSU_PROPERTY_SPOOF_LEVEL)
*     2020/04/01  3.3.0  Added enumeration value to IBSU_PropertyId
*                            (ENUM_IBSU_PROPERTY_ROLL_METHOD,
*							  ENUM_IBSU_PROPERTY_RENEWAL_OPPOSITE_IMGAE_LEVEL,
*                             ENUM_IBSU_PROPERTY_PREVIEW_IMAGE_QUALITY_FOR_KOJAK,
*							  ENUM_IBSU_PROPERTY_RESERVED_ENHANCED_RESULT_IMAGE_LEVEL,
*							  ENUM_IBSU_PROPERTY_RESERVED_ENABLE_SLIP_DETECTION,
*							  ENUM_IBSU_PROPERTY_RESERVED_SLIP_DETECTION_LEVEL)
*     2020/04/01  3.3.0  Added enumeration value to IBSU_PropertyId
*                            (ENUM_IBSU_PROPERTY_RESERVED_ENABLE_TRICK_CAPTURE)
*     2020/08/21  3.5.0  Added enumeration value to IBSU_PropertyId
*                            (ENUM_IBSU_PROPERTY_ADAPTIVE_CAPTURE_MODE,
*                             ENUM_IBSU_PROPERTY_ENABLE_KOJAK_BEHAVIOR_2_6)
*     2020/10/06  3.7.0  Modified IBSU_DeviceDesc structure for new locking feature.
*                        Added IBSU_HashType
*     2021/07/16  3.7.2  Added enumeration value to IBSU_PropertyId
*                            (ENUM_IBSU_PROPERTY_VERTICAL_DIRECTION_SEGMENT,
*                             ENUM_IBSU_PROPERTY_RESERVED_SPOOF_LEVEL_THRESHOLD)
*	  2022/02/18  3.8.1  Modified enumeration name changed from 
*                            ENUM_IBSU_PROPERTY_VERTICAL_DIRECTION_SEGMENT to
*                            ENUM_IBSU_PROPERTY_DISABLE_SEGMENT_ROTATION
*                        ENUM_IBSU_PROPERTY_ADAPTIVE_CAPTURE_MODE 
*                            property value set not permitted		
*     2022/04/13  3.9.0  Added new enumerations & structures to support ISO/ANSI template integration
*                            (IBSM_TemplateVersion, IBSM_Template, IBSM_StandardFormat, 
*                             IBSM_StandardFormatData)
*     2022/05/30  3.9.1  Removed ENUM_IBSU_PROPERTY_RESERVED_SPOOF_LEVEL_THRESHOLD
****************************************************************************************************
'''


'''
****************************************************************************************************
* GLOBAL DEFINES
****************************************************************************************************
'''

# /* Required length of buffer for return string parameters. */
IBSU_MAX_STR_LEN = 128

# /* Minimum value of contrast. */
IBSU_MIN_CONTRAST_VALUE = 0

# /* Maximum value of contrast. */
IBSU_MAX_CONTRAST_VALUE = 34

# /* Required buffer length for segment parameters. */
IBSU_MAX_SEGMENT_COUNT = 4                  
# /* Required buffer length for the 8bit bitmap header. */
IBSU_BMP_GRAY_HEADER_LEN = 1078               
# /* Required buffer length for the 24bit bitmap header. */
IBSU_BMP_RGB24_HEADER_LEN = 54                
# /* Required buffer length for the 32bit bitmap header. */
IBSU_BMP_RGB32_HEADER_LEN = 54                

# /* Capture options.  For more information, see IBSU_BeginCaptureImage(). */
IBSU_OPTION_AUTO_CONTRAST = 1
IBSU_OPTION_AUTO_CAPTURE = 2
IBSU_OPTION_IGNORE_FINGER_COUNT = 4

# /* LED bit defines. */
IBSU_LED_NONE               = 0x00000000  # /* All LEDs off. */
IBSU_LED_ALL                = 0xFFFFFFFF  # /* All LEDs on. */
IBSU_LED_INIT_BLUE          = 0x00000001  # /* Reserved for vendor (user cannot control it). */
IBSU_LED_SCAN_GREEN         = 0x00000002  # /* OK key - green blink phase 1. */
IBSU_LED_SCAN_CURVE_RED     = 0x00000010  # /* Red LED for Curve (TBN240). */
IBSU_LED_SCAN_CURVE_GREEN   = 0x00000020  # /* Green LED for Curve (TBN240). */
IBSU_LED_SCAN_CURVE_BLUE    = 0x00000040  # /* Blue LED for Curve (TBN240). */

# /* Specific LED bit defines with LED type = ENUM_IBSU_LED_TYPE_FSCAN (e.g four finger scanner, Kojak). */
IBSU_LED_F_BLINK_GREEN             = 0x10000000  #/* All Green LEDs blink. */
IBSU_LED_F_BLINK_RED               = 0x20000000  #/* All Red LEDs blink. */
IBSU_LED_F_LEFT_LITTLE_GREEN       = 0x01000000  #/* Green LED for left little finger. */
IBSU_LED_F_LEFT_LITTLE_RED         = 0x02000000  #/* Red LED for left little finger. */
IBSU_LED_F_LEFT_RING_GREEN         = 0x04000000  #/* Green LED for left ring finger. */
IBSU_LED_F_LEFT_RING_RED           = 0x08000000  #/* Red LED for left ring finger. */
IBSU_LED_F_LEFT_MIDDLE_GREEN       = 0x00100000  #/* Green LED for left middle finger. */
IBSU_LED_F_LEFT_MIDDLE_RED         = 0x00200000  #/* Red LED for left middle finger. */
IBSU_LED_F_LEFT_INDEX_GREEN        = 0x00400000  #/* Green LED for left index finger. */
IBSU_LED_F_LEFT_INDEX_RED          = 0x00800000  #/* Red LED for left index finger. */
IBSU_LED_F_LEFT_THUMB_GREEN        = 0x00010000  #/* Green LED for left thumb finger. */
IBSU_LED_F_LEFT_THUMB_RED          = 0x00020000  #/* Red LED for left thumb finger. */
IBSU_LED_F_RIGHT_THUMB_GREEN       = 0x00040000  #/* Green LED for right thumb finger. */
IBSU_LED_F_RIGHT_THUMB_RED         = 0x00080000  #/* Red LED for right thumb finger. */
IBSU_LED_F_RIGHT_INDEX_GREEN       = 0x00001000  #/* Green LED for right index finger. */
IBSU_LED_F_RIGHT_INDEX_RED         = 0x00002000  #/* Red LED for right index finger. */
IBSU_LED_F_RIGHT_MIDDLE_GREEN      = 0x00004000  #/* Green LED for right middle finger. */
# /* 0x00008000 cannot be used at VB6 (Negative value) */
IBSU_LED_F_RIGHT_MIDDLE_RED        = 0x40000000  #/* Red LED for right middle finger. */
IBSU_LED_F_RIGHT_RING_GREEN        = 0x00000100  #/* Green LED for right ring finger. */
IBSU_LED_F_RIGHT_RING_RED          = 0x00000200  #/* Red LED for right ring finger. */
IBSU_LED_F_RIGHT_LITTLE_GREEN      = 0x00000400  #/* Green LED for right little finger. */
IBSU_LED_F_RIGHT_LITTLE_RED        = 0x00000800  #/* Red LED for right little finger. */
IBSU_LED_F_PROGRESS_ROLL           = 0x00000010  #/* LED for the roll indicator. */
IBSU_LED_F_PROGRESS_LEFT_HAND      = 0x00000020  #/* LED for the left hand indicator. */
IBSU_LED_F_PROGRESS_TWO_THUMB      = 0x00000040  #/* LED for the two thumb indicator. */
IBSU_LED_F_PROGRESS_RIGHT_HAND     = 0x00000080  #/* LED for the right hand indicator. */


# /* Bit-pattern of finger index for IBSU_RemoveFingerImage, IBSU_AddFingerImage, IBSU_IsFingerDuplicated and IBSU_IsValidFingerGeometry */
IBSU_FINGER_NONE            	   = 0x00000000
IBSU_FINGER_LEFT_LITTLE            = 0x00000001
IBSU_FINGER_LEFT_RING              = 0x00000002
IBSU_FINGER_LEFT_MIDDLE            = 0x00000004
IBSU_FINGER_LEFT_INDEX             = 0x00000008
IBSU_FINGER_LEFT_THUMB             = 0x00000010
IBSU_FINGER_RIGHT_THUMB            = 0x00000020
IBSU_FINGER_RIGHT_INDEX            = 0x00000040
IBSU_FINGER_RIGHT_MIDDLE           = 0x00000080
IBSU_FINGER_RIGHT_RING             = 0x00000100
IBSU_FINGER_RIGHT_LITTLE           = 0x00000200
IBSU_FINGER_LEFT_HAND              = (IBSU_FINGER_LEFT_INDEX  | IBSU_FINGER_LEFT_MIDDLE  | IBSU_FINGER_LEFT_RING  | IBSU_FINGER_LEFT_LITTLE)
IBSU_FINGER_RIGHT_HAND             = (IBSU_FINGER_RIGHT_INDEX | IBSU_FINGER_RIGHT_MIDDLE | IBSU_FINGER_RIGHT_RING | IBSU_FINGER_RIGHT_LITTLE)
IBSU_FINGER_BOTH_THUMBS						 = (IBSU_FINGER_RIGHT_THUMB | IBSU_FINGER_LEFT_THUMB)
IBSU_FINGER_ALL                    = (IBSU_FINGER_LEFT_HAND   | IBSU_FINGER_RIGHT_HAND   | IBSU_FINGER_BOTH_THUMBS)
IBSU_FINGER_LEFT_LITTLE_RING			 = (IBSU_FINGER_LEFT_LITTLE | IBSU_FINGER_LEFT_RING)
IBSU_FINGER_LEFT_MIDDLE_INDEX			 = (IBSU_FINGER_LEFT_MIDDLE | IBSU_FINGER_LEFT_INDEX)
IBSU_FINGER_RIGHT_INDEX_MIDDLE		 = (IBSU_FINGER_RIGHT_INDEX | IBSU_FINGER_RIGHT_MIDDLE)
IBSU_FINGER_RIGHT_RING_LITTLE			 = (IBSU_FINGER_RIGHT_RING  | IBSU_FINGER_RIGHT_LITTLE)

# /* Maximum value of Minutiae size. (For support ISO Template control) */
IBSU_MAX_MINUTIAE_SIZE = 257

'''
****************************************************************************************************
* GLOBAL TYPES
****************************************************************************************************
'''

'''
****************************************************************************************************
* IBSU_SdkVersion
*
* DESCRIPTION:
*     Container to hold SDK version.
****************************************************************************************************
'''
class IBSU_SdkVersion(Structure):
	_fields_ = [
		("Product", c_char*IBSU_MAX_STR_LEN),
		("File", c_char*IBSU_MAX_STR_LEN)
	]

'''
****************************************************************************************************
* IBSU_DeviceDesc
*
* DESCRIPTION:
*     Basic device description.
****************************************************************************************************
'''
class IBSU_DeviceDesc(Structure):
	_fields_ = [
		("serialNumber", c_char*IBSU_MAX_STR_LEN),
		("productName", c_char*IBSU_MAX_STR_LEN),
		("interfaceType", c_char*IBSU_MAX_STR_LEN),
		("fwVersion", c_char*IBSU_MAX_STR_LEN),
		("devRevision", c_char*IBSU_MAX_STR_LEN),
		("handle", c_int),
		("IsHandleOpened", c_int),
		("IsDeviceLocked", c_int),
		("customerString", c_char*IBSU_MAX_STR_LEN)
	]

'''
****************************************************************************************************
* IBSU_SegmentPosition
*
* DESCRIPTION:
*     Container to hold segment information.
****************************************************************************************************
'''
class IBSU_SegmentPosition(Structure):
	_fields_ = [
		("x1", c_short),    # /* X coordinate of starting point of the finger segment. */
		("y1", c_short),    # /* Y coordinate of starting point of the finger segment. */
		("x2", c_short),    # /* X coordinate of 1st corner of the finger segment. */
		("y2", c_short),    # /* Y coordinate of 1st corner of the finger segment. */
		("x3", c_short),    # /* X coordinate of 2nd corner of the finger segment. */
		("y3", c_short),    # /* Y coordinate of 2nd corner of the finger segment. */
		("x4", c_short),    # /* X coordinate of 3rd corner of the finger segment. */
		("y4", c_short),    # /* Y coordinate of 3rd corner of the finger segment. */
	]

'''
****************************************************************************************************
* IBSU_ImageType
*
* DESCRIPTION:
*     Enumeration of image types.  The image type is passed as a parameter to API functions 
*     IBSU_BeginCaptureImage() and IBSU_IsCaptureAvailable().
****************************************************************************************************
'''
class IBSU_ImageType(Enum):
	# /* Unspecified type. */
	ENUM_IBSU_TYPE_NONE=0

	# /* One-finger rolled fingerprint. */
	ENUM_IBSU_ROLL_SINGLE_FINGER=1

	# /* One-finger flat fingerprint. */
	ENUM_IBSU_FLAT_SINGLE_FINGER=2

	# /* Two-finger flat fingerprint. */
	ENUM_IBSU_FLAT_TWO_FINGERS=3

	# /* Four-finger flat fingerprint. */
	ENUM_IBSU_FLAT_FOUR_FINGERS=4

	# /* Three-finger flat fingerprint. */
	ENUM_IBSU_FLAT_THREE_FINGERS=5

'''
****************************************************************************************************
* IBSU_ImageResolution
*
* DESCRIPTION:
*     Enumeration of image resolutions.  The image resolution is passed as a parameter to API  
*     functions IBSU_BeginCaptureImage() and IBSU_IsCaptureAvailable().
****************************************************************************************************
'''
class IBSU_ImageResolution(Enum):
	ENUM_IBSU_IMAGE_RESOLUTION_500  = 500
	ENUM_IBSU_IMAGE_RESOLUTION_1000 = 1000


'''
****************************************************************************************************
* IBSU_PropertyId
*
* DESCRIPTION:
*     Enumeration of property IDs.  Properties can be gotten with IBSU_GetProperty(); some properties
*     can also be set with IBSU_SetProperty().
****************************************************************************************************
'''
class IBSU_PropertyId(Enum):
	# /* Product name string (e.g., "Watson").  [Get only.] */
	ENUM_IBSU_PROPERTY_PRODUCT_ID=0

	# /* Serial number string.  [Get only.] */
	ENUM_IBSU_PROPERTY_SERIAL_NUMBER=1

	# /* Device manufacturer identifier.  [Get only.] */
	ENUM_IBSU_PROPERTY_VENDOR_ID=2

	# /* IBIA vendor ID.  [Get only.] */
	ENUM_IBSU_PROPERTY_IBIA_VENDOR_ID=3

	# /* IBIA version information.  [Get only.] */
	ENUM_IBSU_PROPERTY_IBIA_VERSION=4

	# /* IBIA device ID.  [Get only.] */
	ENUM_IBSU_PROPERTY_IBIA_DEVICE_ID=5

	# /* Firmware version string.  [Get only.] */
	ENUM_IBSU_PROPERTY_FIRMWARE=6

	# /* Device revision string.  [Get only.] */
	ENUM_IBSU_PROPERTY_REVISION=7

	# /* Production date string.  [Get only.] */
	ENUM_IBSU_PROPERTY_PRODUCTION_DATE=8

	# /* Last service date string.  [Get only.] */
	ENUM_IBSU_PROPERTY_SERVICE_DATE=9

	# /* Image width value.  [Get only.] */
	ENUM_IBSU_PROPERTY_IMAGE_WIDTH=10

	# /* Image height value.  [Get only.] */
	ENUM_IBSU_PROPERTY_IMAGE_HEIGHT=11

	# /* Time to acquire fingerprint in the auto capture regardless of number of fingers.  The option
	#  * IBSU_OPTION_AUTO_CAPTURE must be used.  The valid range is between 2000- and 4000-ms,
	#  * inclusive, with the default of 4000-ms. [Get and set.] */
	ENUM_IBSU_PROPERTY_IGNORE_FINGER_TIME=12

	# /* Auto contrast level value. [Get and set.] */
	ENUM_IBSU_PROPERTY_RECOMMENDED_LEVEL=13

	# /* Polling time for IBSU_BGetImage(). [Get only.] */
	ENUM_IBSU_PROPERTY_POLLINGTIME_TO_BGETIMAGE=14

	# /* Enable power save mode (TRUE to enable or FALSE to disable). [Get and set.] */
	ENUM_IBSU_PROPERTY_ENABLE_POWER_SAVE_MODE=15

	# /* Retry count for communication error.  The valid range is between 0 and 120, inclusive, with
	#  * the default of 6. [Get and set.] */
	ENUM_IBSU_PROPERTY_RETRY_WRONG_COMMUNICATION=16

	# /* The maximum wait time for image capture, in seconds.  Must use IBSU_CallbackResultImageEx instead
	#  * of IBSU_CallbackResultImage.  If -1, the timeout is infinite.  Otherwise, the valid
	#  * range is between 10- and 3600-seconds, inclusive.  The default is -1.  [Get and set.] */
	ENUM_IBSU_PROPERTY_CAPTURE_TIMEOUT=17

	# /* Minimum distance of rolled fingerprint, in millimeters.  The valid range is between 10-
	#  * and 30-mm, inclusive.  The default is 15-mm.  [Get and set.] */
	ENUM_IBSU_PROPERTY_ROLL_MIN_WIDTH=18

	# /* roll mode. The valid range is between 0 ~ 1.  The default is 1.  [Get and set.]
	#  * 0 : no use smear
	#    1 : use notice */
	ENUM_IBSU_PROPERTY_ROLL_MODE=19

	# /* roll level. The valid range is between 0 ~ 2.  The default is 1.  [Get and set.]
	#  * 0 : low level
	#    1 : medium level
	#    2 : high level */
	ENUM_IBSU_PROPERTY_ROLL_LEVEL=20

	# /* The area threshold for image capture for flat fingers and
	#  * The area threshold for beginning rolled finger.
	#  * The valid range is between 0 and 12, inclusive, with the default of 6. [Get and set.] */
	ENUM_IBSU_PROPERTY_CAPTURE_AREA_THRESHOLD=21

	# /* Enable decimation mode (TRUE to enable or FALSE to disable).
	#  * Some of devices (or firmware version) does not support this feature.	[Get and set.]*/
	ENUM_IBSU_PROPERTY_ENABLE_DECIMATION=22

	# /* Enable capture on release (TRUE to enable or FALSE to disable). The default is FALSE.  [Get and set.]
	#  * TRUE  : the result callback will be called when user release the finger from the sensor.
	#  * FALSE : the result callback will be called when the quality of finger become good */
	ENUM_IBSU_PROPERTY_ENABLE_CAPTURE_ON_RELEASE=23

	# /* The device index. [Get only.] */
	ENUM_IBSU_PROPERTY_DEVICE_INDEX=24

	# /* The device ID which has same information with UsbDevice class of Android. [Get only.] */
	ENUM_IBSU_PROPERTY_DEVICE_ID=25

	# /* It can be used for dry finger
	#  * Some of devices (or firmware version) does not support this feature.
	#  * The default is FALSE. [Get and set.]
	#  * TRUE  : Enable dry mode.
	#  * FALSE : Disable dry mode */
	ENUM_IBSU_PROPERTY_SUPER_DRY_MODE=26

	# /* It is a minimum capture time when the dry mode is enabled with the property ENUM_IBSU_PROPERTY_SUPER_DRY_MODE
	#  * Some of devices (or firmware version) does not support this feature.
	#  * The valid range is between 600- and 3000-ms,
	#  * inclusive, with the default of 2000-ms. [Get and set.]*/
	ENUM_IBSU_PROPERTY_MIN_CAPTURE_TIME_IN_SUPER_DRY_MODE=27

	# /* Rolled image width value.  [Get only.] */
	ENUM_IBSU_PROPERTY_ROLLED_IMAGE_WIDTH=28

	# /* Rolled image height value.  [Get only.] */
	ENUM_IBSU_PROPERTY_ROLLED_IMAGE_HEIGHT=29

	# /* Enable the drawing for preview image (TRUE to enable or FALSE to disable).
	#  * The default is TRUE.  [Get and set.] */
	ENUM_IBSU_PROPERTY_NO_PREVIEW_IMAGE=30

	# /* Enable to override roll image (TRUE to enable or FALSE to disable).
	#  * The default is FALSE.  [Get and set.] */
	ENUM_IBSU_PROPERTY_ROLL_IMAGE_OVERRIDE=31

	# /* Enable the warning message for invalid area for result image (TRUE to enable or FALSE to disable).
	#  * The default is FALSE.  [Get and set.] */
	ENUM_IBSU_PROPERTY_WARNING_MESSAGE_INVALID_AREA=32

	# /* Enable wet detect function.
	#  * The default is FALSE.  [Get and set.] */
	ENUM_IBSU_PROPERTY_ENABLE_WET_FINGER_DETECT=33

	# /* Change wet detect level.
	#  * The valid range is between 1 and 5. The default is 3.  [Get and set.]
	#  * 1 : Lowest level for detect wet finger : less sensitive
	#  * 5 : Highest level for detect wet finger : more sensitive */
	ENUM_IBSU_PROPERTY_WET_FINGER_DETECT_LEVEL=34

	# /* Change threshold for each wet detect level.
	#  * The valid range is between 10 and 1000. The default is "50 100 150 200 250"  [Get and set.]
	#  * 50 : Threshold of lowest level for detect wet finger
	#  * 250 : Threshold of highest level for detect wet finger */
	ENUM_IBSU_PROPERTY_WET_FINGER_DETECT_LEVEL_THRESHOLD=35

	# /* Control rolling area vertically.
	#  * The valid range is between 0 and 9. The default is 0.  [Get and set.]
	#  * 0 : minimum position
	#  * 9 : maximum position */
	ENUM_IBSU_PROPERTY_START_POSITION_OF_ROLLING_AREA=36

	# /* Enable rolling without lock.
	#  * The default is FALSE.  [Get and set.] */
	ENUM_IBSU_PROPERTY_START_ROLL_WITHOUT_LOCK=37

	# /* Enable TOF function.
	#  * The default is set depending on the devices.  [Get and set.] */
	ENUM_IBSU_PROPERTY_ENABLE_TOF=38

	# /* Enable Encryption for capture images
	#  * The default is FALSE.  [Get and set.] */
	ENUM_IBSU_PROPERTY_ENABLE_ENCRYPTION=39

	# /* Check if the device supprort spoof function or not */
	ENUM_IBSU_PROPERTY_IS_SPOOF_SUPPORTED=40

	# /* Enable spoof function
	#  * The default is FALSE.  [Get and set.] */
	ENUM_IBSU_PROPERTY_ENABLE_SPOOF=41
	
	# The valid range is between 1 and 5. The default is 3.  [Get and set.]
	# * The default sensitivity of 3 provides the best results through a range of test environments.
	# * The default value of 3 should be used as baseline sensitivity when tuning application performance.
	# *
	# * An INCREASE in spoof level sensitivity (> 3) will increase the number of false rejections for
	# * live fingers while decreasing the liklihood of false acceptance of spoof prints.
	# *
	# * A DECREASE in spoof level sensitivity (< 3) will reduce false rejections but increases the liklihood
	# * of false acceptance of spoof prints.
	# *
	# * Spoof sensitivity is the scale for algorithm thresholds that determine the liklihood that a fingerprint
	# * is fake, or spoof The feature is designed so that the algorithm returns a warning callback when a
	# * spoof is detected */
	ENUM_IBSU_PROPERTY_SPOOF_LEVEL=42
    
	# /* View encrypt Image
	#  * The default is FALSE.  [Get and set.] */
	ENUM_IBSU_PROPERTY_VIEW_ENCRYPTION_IMAGE_MODE=43

	# /* Select fingerprint segmentation mode
	#  * The default is 0.  [Get and set.] */
	ENUM_IBSU_PROPERTY_FINGERPRINT_SEGMENTATION_MODE=44
	
	# /* Enhanced roll Method
 	#  * The default values are 0.  [Get and set.] */
	ENUM_IBSU_PROPERTY_ROLL_METHOD=45

	# /* Select a level of oppisite image value during roll
	#  * The default values are 0.  [Get and set.] 
	#  * 0 : No use
	#  * 1 : renewal if roll image is moved as 1.2mm.
	#  * 2 : renewal if roll image is moved as 2.4mm.
	#  * 3 : renewal if roll image is moved as 3.6mm.
	#  */
	ENUM_IBSU_PROPERTY_RENEWAL_OPPOSITE_IMGAE_LEVEL=46

	# /* Enable to High quality preview image for Kojak
	#  * The default values are 0.  [Get and set.] */
	ENUM_IBSU_PROPERTY_PREVIEW_IMAGE_QUALITY_FOR_KOJAK=47
	
	#/* Enable Adaptive Capture
    # * The default values are TRUE. [Get only.] */
	ENUM_IBSU_PROPERTY_ADAPTIVE_CAPTURE_MODE=48

	#/* Enable to Kojak 2.6 behavior
    # * The default values are FALSE.  [Get and set.] */
	ENUM_IBSU_PROPERTY_ENABLE_KOJAK_BEHAVIOR_2_6=49
	
	# /* Enable to Horizontalize Segment Rectangles
    # * The default values are FALSE.  [Get and set.] */
	ENUM_IBSU_PROPERTY_DISABLE_SEGMENT_ROTATION=50
	
	# /* Reserved for manufacturer strings. [Need a reserve code]*/
	ENUM_IBSU_PROPERTY_RESERVED_1 = 200
	ENUM_IBSU_PROPERTY_RESERVED_2=201
	ENUM_IBSU_PROPERTY_RESERVED_100=202

	# /* The previmage processing threshold. [Need a partner or reserve code]
	#  * The valid range is between 0 and 2, inclusive,
	#  * with the default of 0 on embedded processor (ARM, Android and Windows Mobile),
	#  * and with the default of 2 on PC. [Get and set.]
	#  * 0  : IMAGE_PROCESS_LOW
	#  * 1  : IMAGE_PROCESS_MEDIUM
	#  * 2  : IMAGE_PROCESS_HIGH */
	ENUM_IBSU_PROPERTY_RESERVED_IMAGE_PROCESS_THRESHOLD = 400

	# /* Enable TOF for roll capture
	#  * The default is FALSE.  [Get and set.] */
	ENUM_IBSU_PROPERTY_RESERVED_ENABLE_TOF_FOR_ROLL=401

	# /* Change brightness threshold for flat capture
	#  * The default values are depending on the scanner.  [Get and set.] */
	ENUM_IBSU_PROPERTY_RESERVED_CAPTURE_BRIGHTNESS_THRESHOLD_FOR_FLAT=402

	# /* Change brightness threshold for roll capture
	#  * The default values are depending on the scanner.  [Get and set.] */
	ENUM_IBSU_PROPERTY_RESERVED_CAPTURE_BRIGHTNESS_THRESHOLD_FOR_ROLL=403

	# /* Change result image to be enhanced
	#  * The default values are FALSE.  [Get and set.] */
	ENUM_IBSU_PROPERTY_RESERVED_ENHANCED_RESULT_IMAGE=404
	
	# /* Select a level of image processing
	#  * The default values are 0.  [Get and set.] 
	#  0 : Minimum enhancement
	#  5 : Maximum enhancement */
	ENUM_IBSU_PROPERTY_RESERVED_ENHANCED_RESULT_IMAGE_LEVEL=405

	# /* Enable Slip detection
	#  * The default values are FALSE. [Get and set.] */
	ENUM_IBSU_PROPERTY_RESERVED_ENABLE_SLIP_DETECTION=406

	# /* Change level of Slip detection
	#  * The default values are 3. The Ragne is from 1 to 10.  [Get and set.] */
	ENUM_IBSU_PROPERTY_RESERVED_SLIP_DETECTION_LEVEL=407
	# /* Enable Trick Capture
	#  * The default values are TRUE. [Get and set.] */
	ENUM_IBSU_PROPERTY_RESERVED_ENABLE_TRICK_CAPTURE=408
    
'''
****************************************************************************************************
* IBSU_ClientWindowPropertyId
*
* DESCRIPTION:
*     Enumeration of client window property IDs.  Properties can be gotten with IBSU_GetClientWindowProperty(); 
*     some properties can also be set with IBSU_SetClientWindowProperty().
****************************************************************************************************
'''
class IBSU_ClientWindowPropertyId(Enum):
	# /* Background color of display window.  The valid range is between 0x00000000 and 0xFFFFFFFF,
	#  * inclusive, with the default of 0x00D8E9EC (the button face color on Windows). [Get and set.] */
	ENUM_IBSU_WINDOW_PROPERTY_BK_COLOR=0

	# /* Indicates whether guide line should be drawn for rolling print capture (TRUE or FALSE).  The
	#  * default is TRUE.  [Get and set.] */
	ENUM_IBSU_WINDOW_PROPERTY_ROLL_GUIDE_LINE=1

	# /* Draw arrow to display invalid area (TRUE or FALSE).  The default is FALSE.  [Get and set.] */
	ENUM_IBSU_WINDOW_PROPERTY_DISP_INVALID_AREA=2

	# /* Get the scale of the display image on client window, as a floating point value.  */
	ENUM_IBSU_WINDOW_PROPERTY_SCALE_FACTOR=3

	# /* Get the left margin of the displayed image in relation to the client window, as an integer. */
	ENUM_IBSU_WINDOW_PROPERTY_LEFT_MARGIN=4

	# /* Get the top margin of the displayed image in relation to the client window, as an integer. */
	ENUM_IBSU_WINDOW_PROPERTY_TOP_MARGIN=5

	# /* Thickness of ENUM_IBSU_WINDOW_PROPERTY_ROLL_GUIDE_LINE The valid range is between 1 and 6 pixels,
	#  * inclusive, with the default of 2 pixels.  [Get and set.] */
	ENUM_IBSU_WINDOW_PROPERTY_ROLL_GUIDE_LINE_WIDTH=6

	# /* Get the extended scale of the display image on client window, as a integer value.  */
	ENUM_IBSU_WINDOW_PROPERTY_SCALE_FACTOR_EX=7

	# /* Keep the last image for redrawing of the display image when calling IBSU_RedrawClientWindow.
	# (TRUE to enable or FALSE to disable).  The default is TRUE.  [Get and set.]  */
	ENUM_IBSU_WINDOW_PROPERTY_KEEP_REDRAW_LAST_IMAGE=8

'''
****************************************************************************************************
* IBSU_FingerCountState
*
* DESCRIPTION:
*     Enumeration of finger count states.
****************************************************************************************************
'''
class IBSU_FingerCountState(Enum):
	ENUM_IBSU_FINGER_COUNT_OK=0
	ENUM_IBSU_TOO_MANY_FINGERS=1
	ENUM_IBSU_TOO_FEW_FINGERS=2
	ENUM_IBSU_NON_FINGER=3

'''
****************************************************************************************************
* IBSU_FingerQualityState
*
* DESCRIPTION:
*     Enumeration of finger quality states.
****************************************************************************************************
'''
class IBSU_FingerQualityState(Enum):
	ENUM_IBSU_FINGER_NOT_PRESENT=0
	ENUM_IBSU_QUALITY_GOOD=1
	ENUM_IBSU_QUALITY_FAIR=2
	ENUM_IBSU_QUALITY_POOR=3
	# /* Finger position is not valid on top side. */
	ENUM_IBSU_QUALITY_INVALID_AREA_TOP=4
	# /* Finger position is not valid on left side. */
	ENUM_IBSU_QUALITY_INVALID_AREA_LEFT=5
	# /* Finger position is not valid on right side. */
	ENUM_IBSU_QUALITY_INVALID_AREA_RIGHT=6
	# /* Finger position is not valid on bottom side. */
	ENUM_IBSU_QUALITY_INVALID_AREA_BOTTOM=7

'''
****************************************************************************************************
* IBSU_LEOperationMode
*
* DESCRIPTION:
*     Enumeration of light emitting (LE) file operation modes.
****************************************************************************************************
'''
class IBSU_LEOperationMode(Enum):
	ENUM_IBSU_LE_OPERATION_AUTO=0
	ENUM_IBSU_LE_OPERATION_ON=1
	ENUM_IBSU_LE_OPERATION_OFF=2

'''
****************************************************************************************************
* IBSU_PlatenState
*
* DESCRIPTION:
*     Enumeration of platen states.
****************************************************************************************************
'''
class IBSU_PlatenState(Enum):
	ENUM_IBSU_PLATEN_CLEARD=0
	ENUM_IBSU_PLATEN_HAS_FINGERS=1

'''
****************************************************************************************************
* IBSU_Events
*
* DESCRIPTION:
*     Enumeration of events that can trigger callbacks.
****************************************************************************************************
'''
class IBSU_Events(Enum):
	# /* Callback when device count changes. */
	ENUM_IBSU_ESSENTIAL_EVENT_DEVICE_COUNT=0

	# /* Callback when communication with a device is interrupted. */
	ENUM_IBSU_ESSENTIAL_EVENT_COMMUNICATION_BREAK=1

	# /* Callback when a new preview image is available from a device. */
	ENUM_IBSU_ESSENTIAL_EVENT_PREVIEW_IMAGE=2

	# /* Callback for rolled print acquisition when rolling should begin. */
	ENUM_IBSU_ESSENTIAL_EVENT_TAKING_ACQUISITION=3

	# /* Callback for rolled print acquisition when rolling completes. */
	ENUM_IBSU_ESSENTIAL_EVENT_COMPLETE_ACQUISITION=4

	# /* Callback when result image is available for a capture (deprecated). */
	ENUM_IBSU_ESSENTIAL_EVENT_RESULT_IMAGE=5

	# /* Callback when a finger quality changes. */
	ENUM_IBSU_OPTIONAL_EVENT_FINGER_QUALITY=6

	# /* Callback when the finger count changes. */
	ENUM_IBSU_OPTIONAL_EVENT_FINGER_COUNT=7

	# /* Callback when initialization progress changes for a device. */
	ENUM_IBSU_ESSENTIAL_EVENT_INIT_PROGRESS=8

	# /* Callback when the platen was not clear when capture started or has since become clear. */
	ENUM_IBSU_OPTIONAL_EVENT_CLEAR_PLATEN_AT_CAPTURE=9

	# /* Callback when asynchronous device initialization completes. */
	ENUM_IBSU_ESSENTIAL_EVENT_ASYNC_OPEN_DEVICE=10

	# /* Callback when a warning message is generated. */
	ENUM_IBSU_OPTIONAL_EVENT_NOTIFY_MESSAGE=11

	# /* Callback when result image is available for a capture (with extended information). */
	ENUM_IBSU_ESSENTIAL_EVENT_RESULT_IMAGE_EX=12

	# /* Callback when key buttons are pressed */
	ENUM_IBSU_ESSENTIAL_EVENT_KEYBUTTON=13

'''
****************************************************************************************************
* IBSU_LedType
*
* DESCRIPTION:
*     Enumeration of LED types.
****************************************************************************************************
'''
class IBSU_LedType(Enum):
	# /* No LED field. */
	ENUM_IBSU_LED_TYPE_NONE=0

	# /* Two-scanner type (e.g., Watson). */
	ENUM_IBSU_LED_TYPE_TSCAN=1

	# /* four-scanner type (e.g., Kojak). */
	ENUM_IBSU_LED_TYPE_FSCAN=2

'''
****************************************************************************************************
* IBSU_RollingState
*
* DESCRIPTION:
*     Enumeration of rolling print acquisition states.
****************************************************************************************************
'''
class IBSU_RollingState(Enum):
	ENUM_IBSU_ROLLING_NOT_PRESENT=0
	ENUM_IBSU_ROLLING_TAKE_ACQUISITION=1
	ENUM_IBSU_ROLLING_COMPLETE_ACQUISITION=2
	ENUM_IBSU_ROLLING_RESULT_IMAGE=3

'''
****************************************************************************************************
* IBSU_OverlayShapePattern
*
* DESCRIPTION:
*     Enumeration of the shape pattern to use for the overlay on client window.
****************************************************************************************************
*/
'''
class IBSU_OverlayShapePattern(Enum):
	ENUM_IBSU_OVERLAY_SHAPE_RECTANGLE=0
	ENUM_IBSU_OVERLAY_SHAPE_ELLIPSE=1
	ENUM_IBSU_OVERLAY_SHAPE_CROSS=2
	ENUM_IBSU_OVERLAY_SHAPE_ARROW=3

'''
/*
****************************************************************************************************
* IBSU_CombineImageWhichHand
*
* DESCRIPTION:
*     Enumeration of hand to use for combining two images into one.
****************************************************************************************************
*/
'''
class IBSU_CombineImageWhichHand(Enum):

	ENUM_IBSU_COMBINE_IMAGE_LEFT_HAND=0
	ENUM_IBSU_COMBINE_IMAGE_RIGHT_HAND=1



'''
****************************************************************************************************
* IBSU_BeeperType
*
* DESCRIPTION:
*     Enumeration of Beeper types.
****************************************************************************************************
'''
class IBSU_BeeperType(Enum):
	# /* No Beeper field. */
	ENUM_IBSU_BEEPER_TYPE_NONE=0

	# /* Monotone type. */
	ENUM_IBSU_BEEPER_TYPE_MONOTONE=1


'''
****************************************************************************************************
* IBSU_BeepPattern
*
* DESCRIPTION:
*     Enumeration of the beep pattern.
****************************************************************************************************
'''
class IBSU_BeepPattern(Enum):
	# /* Generic type. */
	ENUM_IBSU_BEEP_PATTERN_GENERIC=0

	# /* Repeat type. */
	ENUM_IBSU_BEEP_PATTERN_REPEAT=1

'''
****************************************************************************************************
* IBSU_EncryptionMode
*
* DESCRIPTION:
*     Enumeration of the encryption mode.
****************************************************************************************************
'''
class IBSU_EncryptionMode(Enum):
	# /* Random Key generated by own library. */
  ENUM_IBSU_ENCRYPTION_KEY_RANDOM=0

  # /* Custom Key provided by user. */
  ENUM_IBSU_ENCRYPTION_KEY_CUSTOM=1

'''
****************************************************************************************************
* IBSU_HashType
*
* DESCRIPTION:
*     Enumeration of the hash type.
****************************************************************************************************
'''
class IBSU_HashType(Enum):
    # /* SHA256 */
    ENUM_IBSU_HASH_TYPE_SHA256=0

    # /* Reserved */
    ENUM_IBSU_HASH_TYPE_RESERVED=1

'''
****************************************************************************************************
* IBSM_ImageFormat
*
* DESCRIPTION:
*     Enumeration of image formats to support IBScanMatcher integration.
****************************************************************************************************
'''
class IBSM_ImageFormat(Enum):
	IBSM_IMG_FORMAT_NO_BIT_PACKING=0
	IBSM_IMG_FORMAT_BIT_PACKED=1
	IBSM_IMG_FORMAT_WSQ=2
	IBSM_IMG_FORMAT_JPEG_LOSSY=3
	IBSM_IMG_FORMAT_JPEG2000_LOSSY=4
	IBSM_IMG_FORMAT_JPEG2000_LOSSLESS=5
	IBSM_IMG_FORMAT_PNG=6
	IBSM_IMG_FORMAT_UNKNOWN=7

'''
****************************************************************************************************
* IBSM_ImpressionType
*
* DESCRIPTION:
*     Enumeration of image impression types to support IBScanMatcher integration.
****************************************************************************************************
'''
class IBSM_ImpressionType(Enum):
	IBSM_IMPRESSION_TYPE_LIVE_SCAN_PLAIN=0
	IBSM_IMPRESSION_TYPE_LIVE_SCAN_ROLLED=1
	IBSM_IMPRESSION_TYPE_NONLIVE_SCAN_PLAIN=2
	IBSM_IMPRESSION_TYPE_NONLIVE_SCAN_ROLLED=3
	IBSM_IMPRESSION_TYPE_LATENT_IMPRESSION=4
	IBSM_IMPRESSION_TYPE_LATENT_TRACING=5
	IBSM_IMPRESSION_TYPE_LATENT_PHOTO=6
	IBSM_IMPRESSION_TYPE_LATENT_LIFT=7
	IBSM_IMPRESSION_TYPE_LIVE_SCAN_SWIPE=8
	IBSM_IMPRESSION_TYPE_LIVE_SCAN_VERTICAL_ROLL=9
	IBSM_IMPRESSION_TYPE_LIVE_SCAN_PALM=10
	IBSM_IMPRESSION_TYPE_NONLIVE_SCAN_PALM=11
	IBSM_IMPRESSION_TYPE_LATENT_PALM_IMPRESSION=12
	IBSM_IMPRESSION_TYPE_LATENT_PALM_TRACING=13
	IBSM_IMPRESSION_TYPE_LATENT_PALM_PHOTO=14
	IBSM_IMPRESSION_TYPE_LATENT_PALM_LIFT=15
	IBSM_IMPRESSION_TYPE_LIVE_SCAN_OPTICAL_CONTRCTLESS_PLAIN=24
	IBSM_IMPRESSION_TYPE_OTHER=28
	IBSM_IMPRESSION_TYPE_UNKNOWN=29

'''
****************************************************************************************************
* IBSM_FingerPosition (Deprecated)
*
* DESCRIPTION:
*     Enumeration of finger positions to support IBScanMatcher integration.
****************************************************************************************************
'''
class IBSM_FingerPosition(Enum):
	IBSM_FINGER_POSITION_UNKNOWN=0
	IBSM_FINGER_POSITION_RIGHT_THUMB=1
	IBSM_FINGER_POSITION_RIGHT_INDEX_FINGER=2
	IBSM_FINGER_POSITION_RIGHT_MIDDLE_FINGER=3
	IBSM_FINGER_POSITION_RIGHT_RING_FINGER=4
	IBSM_FINGER_POSITION_RIGHT_LITTLE_FINGER=5
	IBSM_FINGER_POSITION_LEFT_THUMB=6
	IBSM_FINGER_POSITION_LEFT_INDEX_FINGER=7
	IBSM_FINGER_POSITION_LEFT_MIDDLE_FINGER=8
	IBSM_FINGER_POSITION_LEFT_RING_FINGER=9
	IBSM_FINGER_POSITION_LEFT_LITTLE_FINGER=10
	IBSM_FINGER_POSITION_PLAIN_RIGHT_FOUR_FINGERS=13
	IBSM_FINGER_POSITION_PLAIN_LEFT_FOUR_FINGERS=14
	IBSM_FINGER_POSITION_PLAIN_THUMBS=15
	IBSM_FINGER_POSITION_UNKNOWN_PALM=20
	IBSM_FINGER_POSITION_RIGHT_FULL_PALM=21
	IBSM_FINGER_POSITION_RIGHT_WRITERS_PALM=22
	IBSM_FINGER_POSITION_LEFT_FULL_PALM=23
	IBSM_FINGER_POSITION_LEFT_WRITERS_PALM=24
	IBSM_FINGER_POSITION_RIGHT_LOWER_PALM=25
	IBSM_FINGER_POSITION_RIGHT_UPPER_PALM=26
	IBSM_FINGER_POSITION_LEFT_LOWER_PALM=27
	IBSM_FINGER_POSITION_LEFT_UPPER_PALM=28
	IBSM_FINGER_POSITION_RIGHT_OTHER=29
	IBSM_FINGER_POSITION_LEFT_OTHER=30
	IBSM_FINGER_POSITION_RIGHT_INTERDIGITAL=31
	IBSM_FINGER_POSITION_RIGHT_THENAR=32
	IBSM_FINGER_POSITION_RIGHT_HYPOTHENAR=33
	IBSM_FINGER_POSITION_LEFT_INTERDIGITAL=34
	IBSM_FINGER_POSITION_LEFT_THENAR=35
	IBSM_FINGER_POSITION_LEFT_HYPOTHENAR=36
	IBSM_FINGER_POSITION_RIGHT_INDEX_AND_MIDDLE=40
	IBSM_FINGER_POSITION_RIGHT_MIDDLE_AND_RING=41
	IBSM_FINGER_POSITION_RIGHT_RING_AND_LITTLE=42
	IBSM_FINGER_POSITION_LEFT_INDEX_AND_MIDDLE=43
	IBSM_FINGER_POSITION_LEFT_MIDDLE_AND_RING=44
	IBSM_FINGER_POSITION_LEFT_RING_AND_LITTLE=45
	IBSM_FINGER_POSITION_RIGHT_INDEX_AND_LEFT_INDEX=46
	IBSM_FINGER_POSITION_RIGHT_INDEX_AND_MIDDLE_AND_RING=47
	IBSM_FINGER_POSITION_RIGHT_MIDDLE_AND_RING_AND_LITTLE=48
	IBSM_FINGER_POSITION_LEFT_INDEX_AND_MIDDLE_AND_RING=49
	IBSM_FINGER_POSITION_LEFT_MIDDLE_AND_RING_AND_LITTLE=50

'''
****************************************************************************************************
* IBSM_CaptureDeviceTechID (Deprecated)
*
* DESCRIPTION:
*     Enumeration of finger positions to support IBScanMatcher integration.
****************************************************************************************************
'''
class IBSM_CaptureDeviceTechID(Enum):
	IBSM_CAPTURE_DEVICE_UNKNOWN_OR_UNSPECIFIED=0
	IBSM_CAPTURE_DEVICE_WHITE_LIGHT_OPTICAL_TIR=1
	IBSM_CAPTURE_DEVICE_WHITE_LIGHT_OPTICAL_DIRECT_VIEW_ON_PLATEN=2
	IBSM_CAPTURE_DEVICE_WHITE_LIGHT_OPTICAL_TOUCHLESS=3
	IBSM_CAPTURE_DEVICE_MONOCHROMATIC_VISIBLE_OPTICAL_TIR=4
	IBSM_CAPTURE_DEVICE_MONOCHROMATIC_VISIBLE_OPTICAL_DIRECT_VIEW_ON_PLATEN=5
	IBSM_CAPTURE_DEVICE_MONOCHROMATIC_VISIBLE_OPTICAL_TOUCHLESS=6
	IBSM_CAPTURE_DEVICE_MONOCHROMATIC_IR_OPTICAL_TIR=7
	IBSM_CAPTURE_DEVICE_MONOCHROMATIC_IR_OPTICAL_DIRECT_VIEW_ON_PLATEN=8
	IBSM_CAPTURE_DEVICE_MONOCHROMATIC_IR_OPTICAL_TOUCHLESS=9
	IBSM_CAPTURE_DEVICE_MULTISPECTRAL_OPTICAL_TIR=10
	IBSM_CAPTURE_DEVICE_MULTISPECTRAL_OPTICAL_DIRECT_VIEW_ON_PLATEN=11
	IBSM_CAPTURE_DEVICE_MULTISPECTRAL_OPTICAL_TOUCHLESS=12
	IBSM_CAPTURE_DEVICE_ELECTRO_LUMINESCENT=13
	IBSM_CAPTURE_DEVICE_SEMICONDUCTOR_CAPACITIVE=14
	IBSM_CAPTURE_DEVICE_SEMICONDUCTOR_RF=15
	IBSM_CAPTURE_DEVICE_SEMICONDUCTOR_THEMAL=16
	IBSM_CAPTURE_DEVICE_PRESSURE_SENSITIVE=17
	IBSM_CAPTURE_DEVICE_ULTRASOUND=18
	IBSM_CAPTURE_DEVICE_MECHANICAL=19
	IBSM_CAPTURE_DEVICE_GLASS_FIBER=20

'''
****************************************************************************************************
* IBSM_CaptureDeviceTypeID (Deprecated)
*
* DESCRIPTION:
*     Enumeration of finger positions to support IBScanMatcher integration.
****************************************************************************************************
'''
class IBSM_CaptureDeviceTypeID(Enum):
	IBSM_CAPTURE_DEVICE_TYPE_ID_UNKNOWN=0x0000
	IBSM_CAPTURE_DEVICE_TYPE_ID_CURVE=0x1004
	IBSM_CAPTURE_DEVICE_TYPE_ID_WATSON=0x1005
	IBSM_CAPTURE_DEVICE_TYPE_ID_SHERLOCK=0x1010
	IBSM_CAPTURE_DEVICE_TYPE_ID_WATSON_MINI=0x1020
	IBSM_CAPTURE_DEVICE_TYPE_ID_COLUMBO=0x1100
	IBSM_CAPTURE_DEVICE_TYPE_ID_HOLMES=0x1200
	IBSM_CAPTURE_DEVICE_TYPE_ID_KOJAK=0x1300
	IBSM_CAPTURE_DEVICE_TYPE_ID_FIVE0=0x1500

'''
****************************************************************************************************
* IBSM_CaptureDeviceVendorID (Deprecated)
*
* DESCRIPTION:
*     Enumeration of finger positions to support IBScanMatcher integration.
****************************************************************************************************
'''
class IBSM_CaptureDeviceVendorID(Enum):
	IBSM_CAPTURE_DEVICE_VENDOR_ID_UNREPORTED=0x0000
	IBSM_CAPTURE_DEVICE_VENDOR_INTEGRATED_BIOMETRICS=0x113F

'''
****************************************************************************************************
* IBSM_ImageData
*
* DESCRIPTION:
*     Container for image information to support IBScanMatcher integration.
****************************************************************************************************
'''
class IBSM_ImageData(Structure):
	_fields_ = [
		("ImageFormat", c_int),
		("ImpressionType", c_int),
		("FingerPosition", c_int),
		("CaptureDeviceTechID", c_int),
		("CaptureDeviceVendorID", c_short),
		("CaptureDeviceTypeID", c_short),
		("ScanSamplingX", c_short),
		("ScanSamplingY", c_short),
		("ImageSamplingX", c_short),
		("ImageSamplingY", c_short),
		("ImageSizeX", c_short),
		("ImageSizeY", c_short),
		("ScaleUnit", c_char),
		("BitDepth", c_char),
		("ImageDataLength", c_uint),
		("ImageData", c_void_p)
	]

'''
****************************************************************************************************
* IBSM_TemplateVersion
*
* DESCRIPTION:
*     Enumeration of Template versions to support ISO/ANSI integration.
****************************************************************************************************
'''
class IBSM_TemplateVersion(Enum):
    IBSM_TEMPLATE_VERSION_IBISDK_0=0x00    # // TEMPLATE_OLD_VERSION
    IBSM_TEMPLATE_VERSION_IBISDK_1=0x01         # // TEMPLATE_MIX_VERSION
    IBSM_TEMPLATE_VERSION_IBISDK_2=0x02         # // TEMPLATE_FAST_VERSION
    IBSM_TEMPLATE_VERSION_IBISDK_3=0x03         # // Secuest 1nd Algorithm
    IBSM_TEMPLATE_VERSION_NEW_0=0x10        # // IBSM_NEW_TEMPLATE

'''
****************************************************************************************************
* IBSM_Template
*
* DESCRIPTION:
*     Container for Template information to support ISO/ANSI integration.
****************************************************************************************************
'''
class IBSM_Template(Structure):
	_fields_ = [
		("Version", c_int),
		("FingerPosition", c_int),
		("ImpressionType", c_int),
		("CaptureDeviceTechID", c_int),
		("CaptureDeviceVendorID", c_short),
		("CaptureDeviceTypeID", c_short),
		("ImageSamplingX", c_short),
		("ImageSamplingY", c_short),
		("ImageSizeX", c_short),
		("ImageSizeY", c_short),
		("Minutiae", c_uint*IBSU_MAX_MINUTIAE_SIZE),
		("Reserved", c_uint)
	]

'''
****************************************************************************************************
* IBSM_ImageData
*
* DESCRIPTION:
*     Enumeration of Template versions to support ISO/ANSI integration.
****************************************************************************************************
'''
class IBSM_StandardFormat(Enum):
    # /* ISO 19794-2:2005 */
    ENUM_IBSM_STANDARD_FORMAT_ISO_19794_2_2005=0

	# /* ISO 19794-4:2005 */
    ENUM_IBSM_STANDARD_FORMAT_ISO_19794_4_2005=1

	# /* ISO 19794-2:2011 */
    ENUM_IBSM_STANDARD_FORMAT_ISO_19794_2_2011=2

	# /* ISO 19794-4:2011 */
    ENUM_IBSM_STANDARD_FORMAT_ISO_19794_4_2011=3

	# /* ANSI/INCITS 378:2004 */
    ENUM_IBSM_STANDARD_FORMAT_ANSI_INCITS_378_2004=4

	# /* ANSI/INCITS 381:2004 */
    ENUM_IBSM_STANDARD_FORMAT_ANSI_INCITS_381_2004=5

'''
****************************************************************************************************
* IBSM_StandardFormatData
*
* DESCRIPTION:
*     Container for Standard format data information to support ISO/ANSI integration.
****************************************************************************************************
'''
class IBSM_StandardFormatData(Structure):
	_fields_ = [
		# /* Pointer to data buffer.  If this structure is supplied by a callback function, this pointer 
		# * must not be retained; the data should be copied to an application buffer for any processing
		# * after the callback returns. */
		("Data", c_void_p),
		# /* Data Length (in bytes). */
		("DataLength", c_uint),
		# /* Standard Format (ISO 19794-2:2005, ISO 19794-4:2005, ISO 19794-2:2011, ISO 19794-4:2011, ANSI/INCITS 378:2004, ANSI/INCITS 381:2004) */
		("Format", c_int)
	]


'''
****************************************************************************************************
* CALLBACK FUNCTION TYPES
****************************************************************************************************
'''

'''
****************************************************************************************************
* IBSU_Callback()
*
* DESCRIPTION:
*     Callback for ENUM_IBSU_ESSENTIAL_EVENT_COMMUNICATION_BREAK, called when communication with a
*     device is interrupted.
*
* ARGUMENTS:
*     deviceHandle  Device handle.
*     pContext      User context.
****************************************************************************************************
'''
if (sys.platform.startswith("win")):
	IBSU_Callback = WINFUNCTYPE(None, c_int, c_void_p)
else:
	IBSU_Callback = CFUNCTYPE(None, c_int, c_void_p)

'''
****************************************************************************************************
* IBSU_CallbackPreviewImage()
*
* DESCRIPTION:
*     Callback for ENUM_IBSU_ESSENTIAL_EVENT_PREVIEW_IMAGE, called when a preview image is available.
*
* ARGUMENTS:
*     deviceHandle  Device handle.
*     pContext      User context.
*     image         Preview image data.  This structure, including the buffer, is valid only 
*                   within the function context.  If required for later use, any data must be 
*                   copied to another structure.
****************************************************************************************************
'''
if (sys.platform.startswith("win")):
	IBSU_CallbackPreviewImage = WINFUNCTYPE(None, c_int, c_void_p, IBSU_ImageData)
else:
	IBSU_CallbackPreviewImage = CFUNCTYPE(None, c_int, c_void_p, IBSU_ImageData)


'''
****************************************************************************************************
* IBSU_CallbackFingerCount()
*
* DESCRIPTION:
*     Callback for ENUM_IBSU_OPTIONAL_EVENT_FINGER_COUNT, called when the finger count changes.
*
* ARGUMENTS:
*     deviceHandle      Device handle.
*     pContext          User context.
*     fingerCountState  Finger count state.
****************************************************************************************************
'''
if (sys.platform.startswith("win")):
	IBSU_CallbackFingerCount = WINFUNCTYPE(None, c_int, c_void_p, c_int)
else:
	IBSU_CallbackFingerCount = CFUNCTYPE(None, c_int, c_void_p, c_int)

''''
****************************************************************************************************
* IBSU_CallbackFingerQuality()
*
* DESCRIPTION:
*     Callback for ENUM_IBSU_OPTIONAL_EVENT_FINGER_QUALITY, called when a finger quality changes.
*
* ARGUMENTS:
*     deviceHandle       Device handle.
*     pContext           User context.
*     pQualityArray      Array of finger qualities.
*     qualityArrayCount  Number of qualities in array.
****************************************************************************************************
'''
if (sys.platform.startswith("win")):
	IBSU_CallbackFingerQuality = WINFUNCTYPE(None, c_int, c_void_p, POINTER(c_int), c_int)
else:
	IBSU_CallbackFingerQuality = CFUNCTYPE(None, c_int, c_void_p, POINTER(c_int), c_int)

'''
****************************************************************************************************
* IBSU_CallbackDeviceCount()
*
* DESCRIPTION:
*     Callback for ENUM_IBSU_ESSENTIAL_EVENT_DEVICE_COUNT, called when the number of detected
*     devices changes.
*
* ARGUMENTS:
*     detectedDevices  Number of detected devices.
*     pContext         User context.
****************************************************************************************************
'''
if (sys.platform.startswith("win")):
	IBSU_CallbackDeviceCount = WINFUNCTYPE(None, c_int, c_void_p)
else:
	IBSU_CallbackDeviceCount = CFUNCTYPE(None, c_int, c_void_p)

'''
****************************************************************************************************
* IBSU_CallbackInitProgress()
*
* DESCRIPTION:
*     Callback for ENUM_IBSU_ESSENTIAL_EVENT_INIT_PROGRESS, called when the initialization progress
*     changes for a device.
*
* ARGUMENTS:
*     deviceIndex    Zero-based index of device.
*     pContext       User context.
*     progressValue  Initialization progress, as a percent, between 0 and 100, inclusive.
****************************************************************************************************
'''
if (sys.platform.startswith("win")):
	IBSU_CallbackInitProgress = WINFUNCTYPE(None, c_int, c_void_p, c_int)
else:
	IBSU_CallbackInitProgress = CFUNCTYPE(None, c_int, c_void_p, c_int)

'''
****************************************************************************************************
* IBSU_CallbackTakingAcquisition()
*
* DESCRIPTION:
*     Callback for ENUM_IBSU_ESSENTIAL_EVENT_TAKING_ACQUISITION, called for a rolled print
*     acquisition when the rolling should begin.
*
* ARGUMENTS:
*     deviceHandle  Device handle.
*     pContext      User context.
*     imageType     Type of image being acquired.
****************************************************************************************************
'''
if (sys.platform.startswith("win")):
	IBSU_CallbackTakingAcquisition = WINFUNCTYPE(None, c_int, c_void_p, c_int)
else:
	IBSU_CallbackTakingAcquisition = CFUNCTYPE(None, c_int, c_void_p, c_int)

'''
****************************************************************************************************
* IBSU_CallbackCompleteAcquisition()
*
* DESCRIPTION:
*     Callback for ENUM_IBSU_ESSENTIAL_EVENT_COMPLETE_ACQUISITION, called for a rolled print
*     acquisition when the rolling capture has completed.
*
* ARGUMENTS:
*     deviceHandle  Device handle.
*     pContext      User context.
*     imageType     Type of image being acquired.
****************************************************************************************************
'''
if (sys.platform.startswith("win")):
	IBSU_CallbackCompleteAcquisition = WINFUNCTYPE(None, c_int, c_void_p, c_int)
else:
	IBSU_CallbackCompleteAcquisition = CFUNCTYPE(None, c_int, c_void_p, c_int)

'''
****************************************************************************************************
* IBSU_CallbackResultImage()
*
* DESCRIPTION:
*     Callback for ENUM_IBSU_ESSENTIAL_EVENT_RESULT_IMAGE, called when the result image is 
*     available.
*
* ARGUMENTS:
*     deviceHandle          Device handle.
*     pContext              User context.
*     image                 Data of preview or result image.  The buffer in this structure points to 
*                           an internal image buffer; the data should be copied to an application 
*                           buffer if desired for future processing.
*     imageType             Image type.
*     pSplitImageArray      Array of four structures with data of individual finger images split
*                           from result image.  The buffers in these structures point to internal
*                           image buffers; the data should be copied to application buffers if
*                           desired for future processing.
*     splitImageArrayCount  Number of finger images split from result images.
****************************************************************************************************
'''
if (sys.platform.startswith("win")):
	IBSU_CallbackResultImage = WINFUNCTYPE(None, c_int, c_void_p, IBSU_ImageData, c_int, POINTER(IBSU_ImageData), c_int)
else:
	IBSU_CallbackResultImage = CFUNCTYPE(None, c_int, c_void_p, IBSU_ImageData, c_int, POINTER(IBSU_ImageData), c_int)
'''
****************************************************************************************************
* IBSU_CallbackResultImageEx()
*
* DESCRIPTION:
*     Callback for ENUM_IBSU_ESSENTIAL_EVENT_RESULT_IMAGE_EX, called when the result image is 
*     available, with extended information.
*
* ARGUMENTS:
*     deviceHandle            Device handle.
*     pContext                User context.
*     imageStatus             Status from result image acquisition.  See error codes in 
*                             'IBScanUltimateApi_err'.
*     image                   Data of preview or result image.  The buffer in this structure points to 
*                             an internal image buffer; the data should be copied to an application 
*                             buffer if desired for future processing.
*     imageType               Image type.
*     detectedFingerCount     Number of detected fingers.
*     segmentImageArrayCount  Number of finger images split from result images.
*     pSegmentImageArray      Array of structures with data of individual finger images split from
*                             result image.  The buffers in these structures point to internal image 
*                             buffers; the data should be copied to application buffers if desired 
*                             for future processing.
*     pSegmentPositionArray   Array of structures with position data for individual fingers split 
*                             from result image.
****************************************************************************************************
'''
if (sys.platform.startswith("win")):
	IBSU_CallbackResultImageEx = WINFUNCTYPE(None, c_int, c_void_p, c_int, IBSU_ImageData,
											 c_int, c_int, c_int, POINTER(IBSU_ImageData), POINTER(IBSU_SegmentPosition))
else:
	IBSU_CallbackResultImageEx = CFUNCTYPE(None, c_int, c_void_p, c_int, IBSU_ImageData,
										   c_int, c_int, c_int, POINTER(IBSU_ImageData), POINTER(IBSU_SegmentPosition))

'''
****************************************************************************************************
* IBSU_CallbackClearPlatenAtCapture()
*
* DESCRIPTION:
*     Callback for ENUM_IBSU_OPTIONAL_EVENT_CLEAR_PLATEN_AT_CAPTURE, called when the platen was not 
*     clear when capture started or has since become clear.
*
* ARGUMENTS:
*     deviceHandle  Device handle.
*     pContext      User context.
*     platenState   Platen state.
****************************************************************************************************
'''
if (sys.platform.startswith("win")):
	IBSU_CallbackClearPlatenAtCapture = WINFUNCTYPE(None, c_int, c_void_p, c_int)
else:
	IBSU_CallbackClearPlatenAtCapture = CFUNCTYPE(None, c_int, c_void_p, c_int)

'''
****************************************************************************************************
* IBSU_CallbackAsyncOpenDevice()
*
* DESCRIPTION:
*     Callback for ENUM_IBSU_ESSENTIAL_EVENT_ASYNC_OPEN_DEVICE, called asynchronous device 
*     initialization completes
*
* ARGUMENTS:
*     deviceIndex   Zero-based index of device.
*     pContext      User context.
*     deviceHandle  Handle for subsequent function calls.
*     errorCode     Error that prevented initialization from completing.
****************************************************************************************************
'''
if (sys.platform.startswith("win")):
	IBSU_CallbackAsyncOpenDevice = WINFUNCTYPE(None, c_int, c_void_p, c_int, c_int)
else:
	IBSU_CallbackAsyncOpenDevice = CFUNCTYPE(None, c_int, c_void_p, c_int, c_int)

'''
****************************************************************************************************
* IBSU_CallbackNotifyMessage()
*
* DESCRIPTION:
*     Callback for ENUM_IBSU_OPTIONAL_EVENT_NOTIFY_MESSAGE, called when a warning message is 
*     generated.
*
* ARGUMENTS:
*     deviceHandle   Device handle.
*     pContext       User context.
*     notifyMessage  Status code as defined in IBScanUltimateApi_err.h.
****************************************************************************************************
'''
if (sys.platform.startswith("win")):
	IBSU_CallbackNotifyMessage = WINFUNCTYPE(None, c_int, c_void_p, c_int)
else:
	IBSU_CallbackNotifyMessage = CFUNCTYPE(None, c_int, c_void_p, c_int)

'''
****************************************************************************************************
* IBSU_CallbackKeyButtons()
*
* DESCRIPTION:
*     Callback for ENUM_IBSU_ESSENTIAL_EVENT_KEYBUTTON, called when the key button of device was chicked.
*
* ARGUMENTS:
*     deviceHandle       Device handle.
*     pContext           User context.
*     pressedKeyButtons  The key button index which is pressed.
****************************************************************************************************
'''
if (sys.platform.startswith("win")):
	IBSU_CallbackKeyButtons = WINFUNCTYPE(None, c_int, c_void_p, c_int)
else:
	IBSU_CallbackKeyButtons = CFUNCTYPE(None, c_int, c_void_p, c_int)
