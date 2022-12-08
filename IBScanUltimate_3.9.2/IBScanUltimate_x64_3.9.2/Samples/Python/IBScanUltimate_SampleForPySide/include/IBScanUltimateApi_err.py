from ctypes import *

'''
****************************************************************************************************
* IBScanUltimateApi_err.h
*
* DESCRIPTION:
*     Error codes for IBScanUltimate.
*     http://www.integratedbiometrics.com
*
* NOTES:
*     Copyright (c) Integrated Biometrics, 2009-2021
*
* HISTORY:
*     2012/04/06  1.0.0  Created.
*     2012/09/05  1.3.0  Added error and warning codes (IBSU_ERR_DEVICE_ENABLED_POWER_SAVE_MODE,
*                            IBSU_WRN_CHANNEL_IO_SLEEP_STATUS, IBSU_WRN_BGET_IMAGE)
*     2012/11/06  1.4.1  Added warning codes (IBSU_WRN_ROLLING_NOT_RUNNING)
*     2013/03/20  1.6.0  Added error and warning codes to support IBScanMatcher integration
*                            (IBSU_ERR_NBIS_NFIQ_FAILED, IBSU_WRN_EMPTY_IBSM_RESULT_IMAGE)
*     2013/08/03  1.6.9  Reformatted.
*     2013/10/14  1.7.0  Added error codes to check update firmware, invalid overlay handle
*                            (IBSU_ERR_DEVICE_NEED_UPDATE_FIRMWARE,IBSU_ERR_INVALID_OVERLAY_HANDLE )
*                        Added warning codes to deprecate API functions and detect no finger/
*                        incorrect fingers/smear in result image.
*                            (IBSU_WRN_API_DEPRECATED, IBSU_WRN_NO_FINGER, IBSU_WRN_INCORRECT_FINGERS,
*                             IBSU_WRN_ROLLING_SMEAR)
*     2014/02/25  1.7.1  Added warning to check incorrect fingers/smear
*                            (IBSU_WRN_ROLLING_SHIFTED_HORIZONTALLY,IBSU_WRN_ROLLING_SHIFTED_VERTICALLY )
*     2014/07/23  1.8.0  Added error codes for WSQ
*                            (IBSU_ERR_NBIS_WSQ_ENCODE_FAILED,IBSU_ERR_NBIS_WSQ_DECODE_FAILED )
*     2014/09/17  1.8.1  Added error codes for JPEG2000 and PNG
*                            (IBSU_ERR_NBIS_PNG_ENCODE_FAILED,IBSU_ERR_NBIS_JP2_ENCODE_FAILED )
*     2015/04/07  1.8.4  Added error codes
*                            (IBSU_ERR_LIBRARY_UNLOAD_FAILED )
*                        Added warning codes
*                            (IBSU_WRN_ALREADY_ENHANCED_IMAGE )
*     2017/04/27  1.9.7  Added warning codes
*                            (IBSU_WRN_QUALITY_INVALID_AREA, IBSU_WRN_INVALID_BRIGHTNESS_FINGERS,
*                             IBSU_WRN_WET_FINGERS)
*     2017/06/16  1.9.8  Added error codes
*                            (IBSU_ERR_DEVICE_NEED_CALIBRATE_TOF, IBSU_WRN_MULTIPLE_FINGERS_DURING_ROLL)
*     2018/04/27  2.0.1  Added error codes
*                            (IBSU_ERR_DEVICE_INVALID_CALIBRATION_DATA, IBSU_ERR_DUPLICATE_EXTRACTION_FAILED,
*                             IBSU_ERR_DUPLICATE_ALREADY_USED, IBSU_ERR_DUPLICATE_SEGMENTATION_FAILED,
*                             IBSU_ERR_DUPLICATE_MATCHING_FAILED)
*     2019/02/19  2.1.0  Added error codes
*                            (IBSU_ERR_DEVICE_HIGHER_SDK_REQUIRED)
*     2020/01/09  3.2.0  Added warning codes
*                            (IBSU_WRN_SPOOF_DETECTED)
*     2020/04/01  3.3.0  Added warning codes
*                            (IBSU_WRN_ROLLING_SLIP_DETECTED)
*     2020/04/01  3.3.0  Added warning codes
*                            (IBSU_WRN_SPOOF_INIT_FAILED)
*     2020/10/06  3.7.0  Added error codes
*                            (IBSU_ERR_DEVICE_LOCK_INVALID_BUFF, IBSU_ERR_DEVICE_LOCK_INFO_EMPTY,
*                             IBSU_ERR_DEVICE_LOCK_INFO_NOT_MATCHED, IBSU_ERR_DEVICE_LOCK_INVALID_CHECKSUM,
*                             IBSU_ERR_DEVICE_LOCK_INVALID_KEY, IBSU_ERR_DEVICE_LOCK_LOCKED,
*                             IBSU_ERR_DEVICE_LOCK_ILLEGAL_DEVICE)
*     2021/06/23  3.7.2  Added error codes
*                            (IBSU_ERR_DEVICE_LOCK_INVALID_SERIAL_FORMAT, IBSU_ERR_PAD_PROPERTY_DISABLED)
****************************************************************************************************
'''

'''
****************************************************************************************************
* GENERIC ERROR CODES
****************************************************************************************************
'''
IBSU_STATUS_OK                              = 0  #/* Function completed successfully. */
IBSU_ERR_INVALID_PARAM_VALUE                = -1  #/* Invalid parameter value. */
IBSU_ERR_MEM_ALLOC                          = -2  #/* Insufficient memory. */
IBSU_ERR_NOT_SUPPORTED                      = -3  #/* Requested functionality isn't supported. */
IBSU_ERR_FILE_OPEN                          = -4  #/* File (USB handle, pipe, or image file) open failed. */
IBSU_ERR_FILE_READ                          = -5  #/* File (USB handle, pipe, or image file) read failed. */
IBSU_ERR_RESOURCE_LOCKED                    = -6  #/* Failure due to a locked resource. */
IBSU_ERR_MISSING_RESOURCE                   = -7  #/* Failure due to a missing resource (e.g. DLL file). */
IBSU_ERR_INVALID_ACCESS_POINTER             = -8  #/* Invalid access pointer address. */
IBSU_ERR_THREAD_CREATE                      = -9  #/* Thread creation failed. */
IBSU_ERR_COMMAND_FAILED                     = -10  #/* Generic command execution failed. */
IBSU_ERR_LIBRARY_UNLOAD_FAILED              = -11  #/* The library unload failed. */

'''
****************************************************************************************************
* LOW-LEVEL I/O ERROR CODES
****************************************************************************************************
'''
IBSU_ERR_CHANNEL_IO_COMMAND_FAILED        = -100  #/* Command execution failed. */
IBSU_ERR_CHANNEL_IO_READ_FAILED           = -101  #/* Input communication failed. */
IBSU_ERR_CHANNEL_IO_WRITE_FAILED          = -102  #/* Output communication failed. */
IBSU_ERR_CHANNEL_IO_READ_TIMEOUT          = -103  #/* Input command execution timed out, but device communication is alive. */
IBSU_ERR_CHANNEL_IO_WRITE_TIMEOUT         = -104  #/* Output command execution timed out, but device communication is alive. */
IBSU_ERR_CHANNEL_IO_UNEXPECTED_FAILED     = -105  #/* Unexpected communication failed. (Only used on IBTraceLogger.) */
IBSU_ERR_CHANNEL_IO_INVALID_HANDLE        = -106  #/* I/O handle state is invalid; reinitialization (close then open) required. */
IBSU_ERR_CHANNEL_IO_WRONG_PIPE_INDEX      = -107  #/* I/O pipe index is invalid; reinitialization (close then open) required. */

'''
****************************************************************************************************
* DEVICE-RELATED ERROR CODES
****************************************************************************************************
'''
IBSU_ERR_DEVICE_IO                        = -200  #/* Device communication failed. */
IBSU_ERR_DEVICE_NOT_FOUND                 = -201  #/* No device is detected/active. */
IBSU_ERR_DEVICE_NOT_MATCHED               = -202  #/* No matching device is detected. */
IBSU_ERR_DEVICE_ACTIVE                    = -203  #/* Initialization failed because it is in use by another thread/process. */
IBSU_ERR_DEVICE_NOT_INITIALIZED           = -204  #/* Device needs to be initialized. */
IBSU_ERR_DEVICE_INVALID_STATE             = -205  #/* Device state is invalid; reinitialization (exit then initialization) required. */
IBSU_ERR_DEVICE_BUSY                      = -206  #/* Another thread is currently using device functions. */
IBSU_ERR_DEVICE_NOT_SUPPORTED_FEATURE     = -207  #/* No hardware support for requested function. */
IBSU_ERR_INVALID_LICENSE                  = -208  #/* The license is invalid or does not match to the device. */
IBSU_ERR_USB20_REQUIRED                   = -209  #/* Device is connected to a full-speed USB port but high-speed is required. */
IBSU_ERR_DEVICE_ENABLED_POWER_SAVE_MODE   = -210  #/* Device is enabled the power save mode. */
IBSU_ERR_DEVICE_NEED_UPDATE_FIRMWARE      = -211  #/* Need to update firmware. */
IBSU_ERR_DEVICE_NEED_CALIBRATE_TOF        = -212  #/* Need to calibrate TOF. */
IBSU_ERR_DEVICE_INVALID_CALIBRATION_DATA  = -213  #/* Invalid calibration data from the device. */
IBSU_ERR_DEVICE_HIGHER_SDK_REQUIRED	      = -214  #/* Device is required to connect higher SDK version for runnging */
IBSU_ERR_DEVICE_LOCK_INVALID_BUFF	      = -215  #/* The Lock-info Buff is not valid.*/
IBSU_ERR_DEVICE_LOCK_INFO_EMPTY           = -216  #/* The Lock-info Buff is empty.*/
IBSU_ERR_DEVICE_LOCK_INFO_NOT_MATCHED     = -217  #/* When the Customer Key to the devices is not registered.*/
IBSU_ERR_DEVICE_LOCK_INVALID_CHECKSUM	  = -218  #/* Checksums between buffer and calculated are different. */
IBSU_ERR_DEVICE_LOCK_INVALID_KEY	      = -219  #/* When Customer key is invalid. */
IBSU_ERR_DEVICE_LOCK_LOCKED	              = -220  #/* When the device is locked. */
IBSU_ERR_DEVICE_LOCK_ILLEGAL_DEVICE       = -221  #/* When the device is not valid from the license file */
IBSU_ERR_DEVICE_LOCK_INVALID_SERIAL_FORMAT= -222  #/* When the serial number format is not valid */

'''
****************************************************************************************************
* IMAGE CAPTURE-RELATED ERROR CODES
****************************************************************************************************
'''
IBSU_ERR_CAPTURE_COMMAND_FAILED           = -300  #/* Image acquisition failed. */
IBSU_ERR_CAPTURE_STOP                     = -301  #/* Stop capture failed. */
IBSU_ERR_CAPTURE_TIMEOUT                  = -302  #/* Timeout during capturing. */
IBSU_ERR_CAPTURE_STILL_RUNNING            = -303  #/* A capture is still running. */
IBSU_ERR_CAPTURE_NOT_RUNNING              = -304  #/* A capture is not running. */
IBSU_ERR_CAPTURE_INVALID_MODE             = -305  #/* Capture mode is not valid or not supported. */
IBSU_ERR_CAPTURE_ALGORITHM                = -306  #/* Generic algorithm processing failure. */
IBSU_ERR_CAPTURE_ROLLING                  = -307  #/* Image processing failure at rolled finger print processing. */
IBSU_ERR_CAPTURE_ROLLING_TIMEOUT          = -308  #/* No roll start detected within a defined timeout period. */

'''
****************************************************************************************************
* CLIENT WINDOW-RELATED ERROR CODES
****************************************************************************************************
'''
IBSU_ERR_CLIENT_WINDOW                    = -400  #/* Generic client window failure. */
IBSU_ERR_CLIENT_WINDOW_NOT_CREATE         = -401  #/* No client window has been created. */
IBSU_ERR_INVALID_OVERLAY_HANDLE           = -402  #/* Invalid overlay handle. */

'''
****************************************************************************************************
* NBIS-RELATED ERROR CODES
****************************************************************************************************
'''
IBSU_ERR_NBIS_NFIQ_FAILED                 = -500  #/* Getting NFIQ score failed. */
IBSU_ERR_NBIS_WSQ_ENCODE_FAILED           = -501  #/* WSQ encode failed. */
IBSU_ERR_NBIS_WSQ_DECODE_FAILED           = -502  #/* WSQ decode failed. */
IBSU_ERR_NBIS_PNG_ENCODE_FAILED           = -503  #/* PNG encode failed. */
IBSU_ERR_NBIS_JP2_ENCODE_FAILED           = -504  #/* JP2 encode failed. */

'''
****************************************************************************************************
* DUPLICATE-RELATED ERROR CODES
****************************************************************************************************
'''
IBSU_ERR_DUPLICATE_EXTRACTION_FAILED      = -600	#/* When the extraction from the fingerimage is faild in IBSU_ADDFingerImage and DLL_IsFingerDuplicated */
IBSU_ERR_DUPLICATE_ALREADY_USED           = -601  #/* When the image of the fingerposition is already in use. in IBSU_ADDFingerImage */
IBSU_ERR_DUPLICATE_SEGMENTATION_FAILED    = -602  #/* When found segment fingercounts are not two and more in IBSU_IsValidFingerGeometry */
IBSU_ERR_DUPLICATE_MATCHING_FAILED    	  = -603  #/* When found small extrations in IBSM_MatchingTemplate */

'''
****************************************************************************************************
* PAD-RELATED ERROR CODES
****************************************************************************************************
'''
IBSU_ERR_PAD_PROPERTY_DISABLED		       = -700	#/* When PAD Property is not enabled. */

'''
****************************************************************************************************
* STANDARD FORMAT-RELATED ERROR CODES
****************************************************************************************************
'''
IBSU_ERR_INCORRECT_STANDARD_FORMAT	       = -800	# /* When Standard data(ISO or ANSI) is incorrect. */


'''
****************************************************************************************************
* WARNING CODES
****************************************************************************************************
'''
IBSU_WRN_CHANNEL_IO_FRAME_MISSING          = 100  #/* Missing an image frame. (Only used on IBTraceLogger.) */
IBSU_WRN_CHANNEL_IO_CAMERA_WRONG           = 101  #/* Camera work is wrong. reset is requied (Only used on IBTraceLogger.) */
IBSU_WRN_CHANNEL_IO_SLEEP_STATUS           = 102
IBSU_WRN_OUTDATED_FIRMWARE                 = 200  #/* Device firmware version outdated. */
IBSU_WRN_ALREADY_INITIALIZED               = 201  #/* Device/component has already been initialized and is ready to be used. */
IBSU_WRN_API_DEPRECATED                    = 202  #/* API function was deprecated. */
IBSU_WRN_ALREADY_ENHANCED_IMAGE            = 203  #/* Image has already been enhanced. */
IBSU_WRN_BGET_IMAGE                        = 300  #/* Device still has not gotten the first image frame. */
IBSU_WRN_ROLLING_NOT_RUNNING               = 301  #/* Rolling has not started. */
IBSU_WRN_NO_FINGER                         = 302  #/* No finger detected in result image. */
IBSU_WRN_INCORRECT_FINGERS                 = 303  #/* Incorrect fingers detected in result image. */
IBSU_WRN_ROLLING_SMEAR                     = 304  #/* Smear detected in rolled result image. */
IBSU_WRN_EMPTY_IBSM_RESULT_IMAGE           = 400  #/* Empty result image. */
IBSU_WRN_QUALITY_INVALID_AREA	    	   = 512  #/* When a finger is located on the invalid area */
IBSU_WRN_INVALID_BRIGHTNESS_FINGERS		   = 600  #/* When a finger doesn't meet image brightness criteria */
IBSU_WRN_WET_FINGERS					   = 601  #/* When detected wet finger */
IBSU_WRN_MULTIPLE_FINGERS_DURING_ROLL	   = 602  #/* When detected multiple fingers during roll */
IBSU_WRN_SPOOF_DETECTED	   				   = 603  #/* When detected spoof finger */
IBSU_WRN_ROLLING_SLIP_DETECTED			   = 604  #/* When detected slip finger */
IBSU_WRN_SPOOF_INIT_FAILED	   			   = 605  #/* When Spoof initalize failed */
'''
****************************************************************************************************
* WARNING CODES FOR SMEAR
* note this value is added to WRN_ROLLING_SMEAR code 304
* 305 is smear shifted horizontally, 306 is shifted vertically, 307 is shifted both horizontally and vertically
****************************************************************************************************
'''
IBSU_WRN_ROLLING_SHIFTED_HORIZONTALLY	    = (IBSU_WRN_ROLLING_SMEAR | 1)	#/* Rolled finger was shifted horizontally. */
IBSU_WRN_ROLLING_SHIFTED_VERTICALLY		    = (IBSU_WRN_ROLLING_SMEAR | 2)	#/* Rolled finger was shifted vertically. */

'''
****************************************************************************************************
* WARNING CODES FOR INVALID AREA
****************************************************************************************************
'''
IBSU_WRN_QUALITY_INVALID_AREA_HORIZONTALLY			= (IBSU_WRN_QUALITY_INVALID_AREA | 1)  #/* Finger was located on the horizontal invalid area */
IBSU_WRN_QUALITY_INVALID_AREA_VERTICALLY			= (IBSU_WRN_QUALITY_INVALID_AREA | 2)  #/* Finger was located on the vertical invalid area */

