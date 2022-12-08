import sys
from ctypes import *
from include.IBScanUltimateApi_defs import *
from include.IBScanUltimateApi_err import *
from include.IBScanUltimate import *

'''
****************************************************************************************************
* IBScanUltimateApi.h
*
* DESCRIPTION:
*     API functions for IBScanUltimate.
*     http://www.integratedbiometrics.com
*
* NOTES:
*     Copyright (c) Integrated Biometrics, 2009-2017
*
* HISTORY:
*     2012/04/06  1.0.0  Created.
*     2012/05/29  1.1.0  Added blocking API functions (IBSU_AsyncOpenDevice(), IBSU_BGetImage(),
*                            IBSU_BGetInitProgress(), IBSU_BGetClearPlatenAtCapture()).
*     2012/11/06  1.4.1  Added rolling and extended open API functions (IBSU_BGetRollingInfo(),
*                            IBSU_OpenDeviceEx()).
*     2013/03/20  1.6.0  Added API function to support IBScanMatcher integration
*                            (IBSU_GetIBSM_ResultImageInfo(), IBSU_GetNFIQScore()).
*     2013/04/05  1.6.2  Added API function to enable or disable trace log at run-time
*                            (IBSU_EnableTraceLog()).
*     2013/08/03  1.6.9  Reformatted.
*     2013/10/14  1.7.0  Added API functions to acquire an image from a device (blocking for resultEx),
*                        deregister a callback function, show (or remove) an overlay object,
*                        show (or remove) all overlay objects, add an overlay text, modify an existing
*                        overlay text, add an overlay line, modify an existing line, add an overlay
*                        quadrangle, modify an existing quadrangle, add an overlay shape, modify an
*                        overlay shape, save image to bitmap memory
*                        (IBSU_BGetImageEx(), IBSU_ReleaseCallbacks(), IBSU_ShowOverlayObject,
*                         IBSU_ShowAllOverlayObject(), IBSU_RemoveOverlayObject(), IBSU_RemoveAllOverlayObject(),
*                         IBSU_AddOverlayText(), IBSU_ModifyOverlayText(), IBSU_AddOverlayLine(),
*                         IBSU_ModifyOverlayLine(), IBSU_AddOverlayQuadrangle(), IBSU_ModifyOverlayQuadrangle(),
*                         IBSU_AddOverlayShape(), IBSU_ModifyOverlayShape(), IBSU_SaveBitmapMem())
*     2014/07/23  1.8.0  Added API functions are relelated to WSQ
*                        (IBSU_WSQEncodeMem, IBSU_WSQEncodeToFile, IBSU_WSQDecodeMem,
*                         IBSU_WSQDecodeFromFile, IBSU_FreeMemory)
*     2014/09/17  1.8.1  Added API functions are relelated to JPEG2000 and PNG
*                        (IBSU_SavePngImage, IBSU_SaveJP2Image)
*     2015/03/04  1.8.3  Reformatted to support UNICODE for WinCE
*                        Added API function is relelated to ClientWindow
*                        (IBSU_RedrawClientWindow)
*                        Bug Fixed, Added new parameter (pitch) to WSQ functions
*                        (IBSU_WSQEncodeMem, IBSU_WSQEncodeToFile, IBSU_WSQDecodeMem,
*                         IBSU_WSQDecodeFromFile)
*     2015/04/07  1.8.4  Added API function to unload the library manually
*                        (IBSU_UnloadLibrary)
*     2015/08/05  1.8.5  Added API function to combine two image into one
*                        (IBSU_CombineImage)
*     2015/12/11  1.9.0  Added API function to support Kojak device
*                        (IBSU_GetOperableBeeper, IBSU_SetBeeper)
*     2017/04/27  1.9.7  Added API function to support improved feature for CombineImage
*                        (IBSU_CombineImageEx)
*     2017/06/17  1.9.8  Added API function to support improved feature for CombineImage
*                        (IBSU_CheckWetFinger, IBSU_BGetRollingInfoEx, IBSU_GetImageWidth,
*                         IBSU_IsWritableDirectory)
*     2017/08/22  1.9.9  Added API function to get final image by native for Columbo
*                        (RESERVED_GetFinalImageByNative)
*     2018/03/06  2.0.0  Added API function to improve dispaly speed on Embedded System
*                        (IBSU_GenerateDisplayImage)
*     2018/04/27  2.0.1  Added API function to improve dispaly speed on Embedded System
*                        (IBSU_RemoveFingerImage, IBSU_AddFingerImage, IBSU_IsFingerDuplicated,
*                         IBSU_IsValidFingerGeometry)
*                        Deprecated API function about IBScanMater(IBSM)
*                        (IBSU_GetIBSM_ResultImageInfo)
*     2019/02/19  2.1.0  Added API function
*                        (IBSU_GetRequiredSDKVersion)
*     2019/06/21  3.0.0  Added API function
*                        (IBSU_SetEncryptionKey, RESERVED_GetEncryptedImage, RESERVED_ConvertToDecryptImage)
*     2020/10/06  3.7.0  Added API function to support new locking feature
*                        (IBSU_SetCustomerKey, IBSU_GetErrorString)
*     2021/08/04  3.7.2  Added API function to enhance NFIQ function and support new Spoof(PAD) function
*                        (IBSU_GetNFIQScoreEx, IBSU_IsSpoofFingerDetected)
*     2022/04/13  3.9.0  Added API function to ISO(ISO 19794, ANSI/INCITS) template create
*                        (IBSU_ConvertImageToISOANSI)
****************************************************************************************************
'''

if (sys.platform.startswith("win")):
    libIBScanUltimate = WinDLL('IBScanUltimate.dll')
else:
    libIBScanUltimate = cdll.LoadLibrary('libIBScanUltimate.so')

'''
****************************************************************************************************
* GLOBAL FUNCTIONS
****************************************************************************************************
'''

'''
****************************************************************************************************
* IBSU_GetSDKVersion()
*
* DESCRIPTION:
*     Obtain product and software version information.
*
* ARGUMENTS:
*     pVerinfo  Pointer to structure that will receive SDK version information.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_GetSDKVersion = libIBScanUltimate.IBSU_GetSDKVersion
IBSU_GetSDKVersion.restype = c_int
IBSU_GetSDKVersion.argtype = POINTER(IBSU_SdkVersion)


'''
****************************************************************************************************
* IBSU_GetDeviceCount()
*
* DESCRIPTION:
*     Retrieve count of connected IB USB scanner devices.
*
* ARGUMENTS:
*     pDeviceCount  Pointer to variable that will receive count of connected IB USB scanner devices.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_GetDeviceCount = libIBScanUltimate.IBSU_GetDeviceCount
IBSU_GetDeviceCount.restype = c_int
IBSU_GetDeviceCount.argtype = POINTER(c_int)


'''
****************************************************************************************************
* IBSU_GetDeviceDescription()
*
* DESCRIPTION:
*     Retrieve detailed device information about a particular scanner by its logical index.
*
* ARGUMENTS:
*     deviceIndex  Zero-based index of the scanner.
*     pDeviceDesc  Pointer to structure that will receive description of device.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_GetDeviceDescription = libIBScanUltimate.IBSU_GetDeviceDescription
IBSU_GetDeviceDescription.restype = c_int
IBSU_GetDeviceDescription.argtypes = (c_int, POINTER(IBSU_DeviceDesc))


'''
****************************************************************************************************
* IBSU_EnableTraceLog()
*
* DESCRIPTION:
*     Enable or disable trace log at run-time.  The trace log is enabled by default on Windows and
*     Android and disabled by default on Linux.
*
* ARGUMENTS:
*     on  Indicates whether trace log should be turned on or off.  TRUE to turn log on; FALSE to
*         turn log off.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_EnableTraceLog = libIBScanUltimate.IBSU_EnableTraceLog
IBSU_EnableTraceLog.restype = c_int
IBSU_EnableTraceLog.argtype = c_bool


'''
****************************************************************************************************
* IBSU_RegisterCallbacks()
*
* DESCRIPTION:
*     Register a callback function for an event type.  These asynchronous notifications enable
*     event-driven management of scanner processes.  For more information about a particular
*     event or the signature of its callback, see the definition of 'IBSU_Events'.
*
* ARGUMENTS:
*     handle             Handle for device associated with this event (if appropriate).
*     event              Event for which the callback is being registered.
*     pCallbackFunction  Pointer to the callback function.
*     pContext           Pointer to user context that will be passed to callback function.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_RegisterCallbacks = libIBScanUltimate.IBSU_RegisterCallbacks
IBSU_RegisterCallbacks.restype = c_int
IBSU_RegisterCallbacks.argtypes = (c_int, c_int, c_void_p, c_void_p)


'''
****************************************************************************************************
* IBSU_OpenDevice()
*
* DESCRIPTION:
*     Initialize a device and obtain a handle for subsequent function calls.  Any initialized device
*     must be released with IBSU_CloseDevice() or IBSU_CloseAllDevice() before shutting down the
*     application.
*
* ARGUMENTS:
*     deviceIndex  Zero-based index of the scanner.
*     pHandle      Pointer to variable that will receive device handle for subsequent function calls.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_OpenDevice = libIBScanUltimate.IBSU_OpenDevice
IBSU_OpenDevice.restype = c_int
IBSU_OpenDevice.argtypes = (c_int, POINTER(c_int))


'''
****************************************************************************************************
* IBSU_AsyncOpenDevice()
*
* DESCRIPTION:
*     Initialize a device asynchronously.  The handle will be delivered to the application with a
*     ENUM_IBSU_ESSENTIAL_EVENT_ASYNC_OPEN_DEVICE callback or with IBSU_BGetInitProgress().  Any
*     initialized device must be released with IBSU_CloseDevice() or IBSU_CloseAllDevice() before
*     shutting down the application.
*
* ARGUMENTS:
*     deviceIndex  Zero-based index of the scanner.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_AsyncOpenDevice = libIBScanUltimate.IBSU_AsyncOpenDevice
IBSU_AsyncOpenDevice.restype = c_int
IBSU_AsyncOpenDevice.argtype = c_int


'''
****************************************************************************************************
* IBSU_OpenDeviceEx()
*
* DESCRIPTION:
*     Initialize a device and obtain a handle for subsequent function calls.  The uniformity mask
*     will be loaded from a file to speed up initialization.  Any initialized device must be
*     released with IBSU_CloseDevice() or IBSU_CloseAllDevice() before shutting down the
*     application.
*
* ARGUMENTS:
*     deviceIndex         Zero-based index of the scanner.
*     uniformityMaskPath  Path at which uniformity mask file is located.  If file does not exist,
*                         it will be created to accelerate subsequent initializations.
*     ayncnOpen           Indicates whether initialization will be performed synchronously or
*                         asynchronously.
*     pHandle             Pointer to variable that will receive device handle for subsequent
*                         function calls, if 'asyncOpen' is FALSE.  Otherwise, handle will be
*                         delivered to the application with a ENUM_IBSU_ESSENTIAL_EVEN_ASYNC_OPEN_DEVICE
*                         callback or with IBSU_BGetInitProgress().
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_OpenDeviceEx = libIBScanUltimate.IBSU_OpenDeviceEx
IBSU_OpenDeviceEx.restype = c_int
IBSU_OpenDeviceEx.argtypes = (c_int, c_char_p, c_bool, POINTER(c_int))


'''
****************************************************************************************************
* IBSU_BGetInitProgress()
*
* DESCRIPTION:
*     Get initialization progress of a device.  If initialization is complete, the handle for
*     subsequent function calls will be returned to the application.
*
* ARGUMENTS:
*     deviceIndex     Zero-based index of the scanner.
*     pIsComplete     Pointer to variable that will receive indicator of initialization completion.
*     pHandle         Pointer to variable that will receive device handle for subsequent function
*                     calls, if 'pIsComplete' receives the value TRUE.
*     pProgressValue  Pointer to variable that will receive initialize progress, as a percentage
*                     between 0 and 100, inclusive.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_BGetInitProgress = libIBScanUltimate.IBSU_BGetInitProgress
IBSU_BGetInitProgress.restype = c_int
IBSU_BGetInitProgress.argtypes = (c_int, POINTER(c_bool), POINTER(c_int), POINTER(c_int))


'''
****************************************************************************************************
* IBSU_CloseDevice()
*
* DESCRIPTION:
*     Release all resources for a device.
*
* ARGUMENTS:
*     handle  Device handle.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
*         IBSU_ERR_RESOURCE_LOCKED: A callback is still active.
*         IBSU_ERR_DEVICE_NOT_INITIALIZED: Device has already been released or is unknown.
****************************************************************************************************
'''
IBSU_CloseDevice = libIBScanUltimate.IBSU_CloseDevice
IBSU_CloseDevice.restype = c_int
IBSU_CloseDevice.argtype = c_int


'''
****************************************************************************************************
* IBSU_CloseAllDevice()
*
* DESCRIPTION:
*     Release all resources for all open devices.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
*         IBSU_ERR_RESOURCE_LOCKED: A callback is still active.
****************************************************************************************************
'''
IBSU_CloseAllDevice = libIBScanUltimate.IBSU_CloseAllDevice
IBSU_CloseAllDevice.restype = c_int
IBSU_CloseAllDevice.argtype = None


'''
****************************************************************************************************
* IBSU_IsDeviceOpened()
*
* DESCRIPTION:
*     Check whether a device is open/initialized.
*
* ARGUMENTS:
*     handle  Device handle.
*
* RETURNS:
*     IBSU_STATUS_OK, if device is open/initialized.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
*         IBSU_ERR_INVALID_PARAM_VALUE: Handle value is out of range.
*         IBSU_ERR_DEVICE_NOT_INITIALIZED: Device has not been initialized.
*         IBSU_ERR_DEVICE_IO: Device has been initialized, but there was a communication problem.
****************************************************************************************************
'''
IBSU_IsDeviceOpened = libIBScanUltimate.IBSU_IsDeviceOpened
IBSU_IsDeviceOpened.restype = c_int
IBSU_IsDeviceOpened.argtype = c_int


'''
****************************************************************************************************
* IBSU_GetProperty()
*
* DESCRIPTION:
*     Get the value of a property for a device.  For descriptions of properties and values, see
*     definition of 'IBSU_PropertyId'.
*
* ARGUMENTS:
*     handle          Device handle.
*     propertyId      Property for which value will be set.
*     propertyValue   Buffer in which value of property will be stored.  This buffer should be
*                     able to hold IBSU_MAX_STR_LEN characters.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_GetProperty = libIBScanUltimate.IBSU_GetProperty
IBSU_GetProperty.restype = c_int
IBSU_GetProperty.argtypes = (c_int, c_int, POINTER(c_char))


'''
****************************************************************************************************
* IBSU_SetProperty()
*
* DESCRIPTION:
*     Set the value of a property for a device.  For descriptions of properties and values, see
*     definition of 'IBSU_PropertyId'.
*
* ARGUMENTS:
*     handle         Device handle.
*     propertyId     Property for which value will be set.
*     propertyValue  Value of property to set.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_SetProperty = libIBScanUltimate.IBSU_SetProperty
IBSU_SetProperty.restype = c_int
IBSU_SetProperty.argtypes = (c_int, c_int, c_char_p)


'''
****************************************************************************************************
* IBSU_IsCaptureAvailable()
*
* DESCRIPTION:
*     Check whether capture mode is supported by a device.
*
* ARGUMENTS:
*     handle           Device handle.
*     imageType        Type of capture.
*     imageResolution  Resolution of capture.
*     pIsAvailable     Pointer to variable that will receive indicator of support.  Will be set to
*                      TRUE if mode is supported.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_IsCaptureAvailable = libIBScanUltimate.IBSU_IsCaptureAvailable
IBSU_IsCaptureAvailable.restype = c_int
IBSU_IsCaptureAvailable.argtypes = (c_int, c_int, c_int, POINTER(c_bool))


'''
****************************************************************************************************
* IBSU_BeginCaptureImage()
*
* DESCRIPTION:
*     Begin acquiring an image from a device.
*
* ARGUMENTS:
*     handle           Device handle.
*     imageType        Type of capture.
*     imageResolution  Resolution of capture.
*     captureOptions   Bit-wise OR of capture options:
*                          IBSU_OPTION_AUTO_CONTRAST - automatically adjust contrast to optimal value
*                          IBSU_OPTION_AUTO_CAPTURE - complete capture automatically when a good-
*                              quality image is available
*                          IBSU_OPTION_IGNORE_FINGER_COUNT - ignore finger count when deciding to
*                              complete capture
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
*         IBSU_ERR_CAPTURE_STILL_RUNNING - An acquisition is currently executing and must complete
*             before another capture can be started.
*         IBSU_ERR_CAPTURE_INVALID_MODE - Capture mode is not supported by this device.
****************************************************************************************************
'''
IBSU_BeginCaptureImage = libIBScanUltimate.IBSU_BeginCaptureImage
IBSU_BeginCaptureImage.restype = c_int
IBSU_BeginCaptureImage.argtypes = (c_int, c_int, c_int, c_uint)


'''
****************************************************************************************************
* IBSU_CancelCaptureImage()
*
* DESCRIPTION:
*     Abort acquisition on a device.
*
* ARGUMENTS:
*     handle  Device handle.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
*         IBSU_ERR_CAPTURE_NOT_RUNNING - Acquisition is not active.
****************************************************************************************************
'''
IBSU_CancelCaptureImage = libIBScanUltimate.IBSU_CancelCaptureImage
IBSU_CancelCaptureImage.restype = c_int
IBSU_CancelCaptureImage.argtype = c_int


'''
****************************************************************************************************
* IBSU_IsCaptureActive()
*
* DESCRIPTION:
*     Determine whether acquisition is active for a device.
*
* ARGUMENTS:
*     handle     Device handle.
*     pIsActive  Pointer to variable that will receive indicator of activity.  TRUE if a acquisition
*                is in progress.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_IsCaptureActive = libIBScanUltimate.IBSU_IsCaptureActive
IBSU_IsCaptureActive.restype = c_int
IBSU_IsCaptureActive.argtypes = (c_int, POINTER(c_bool))


'''
****************************************************************************************************
* IBSU_TakeResultImageManually()
*
* DESCRIPTION:
*     Begin acquiring an image from a device with image gain manually set.
*
* ARGUMENTS:
*     handle  Device handle.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_TakeResultImageManually = libIBScanUltimate.IBSU_TakeResultImageManually
IBSU_TakeResultImageManually.restype = c_int
IBSU_TakeResultImageManually.argtype = c_int


'''
****************************************************************************************************
* IBSU_GetContrast()
*
* DESCRIPTION:
*     Get the contrast value for a device.
*
* ARGUMENTS:
*     handle          Device handle.
*     pContrastValue  Pointer to variable that will receive contrast value.  Value will be between
*                     IBSU_MIN_CONTRAST_VALUE and IBSU_MAX_CONTRAST_VALUE, inclusive.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_GetContrast = libIBScanUltimate.IBSU_GetContrast
IBSU_GetContrast.restype = c_int
IBSU_GetContrast.argtypes = (c_int, POINTER(c_int))


'''
****************************************************************************************************
* IBSU_SetContrast()
*
* DESCRIPTION:
*     Set the contrast value for a device.
*
* ARGUMENTS:
*     handle         Device handle.
*     contrastValue  Contrast value.  Value must be between IBSU_MIN_CONTRAST_VALUE and
*                    IBSU_MAX_CONTRAST_VALUE, inclusive.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_SetContrast = libIBScanUltimate.IBSU_SetContrast
IBSU_SetContrast.restype = c_int
IBSU_SetContrast.argtypes = (c_int, c_int)


'''
****************************************************************************************************
* IBSU_SetLEOperationMode()
*
* DESCRIPTION:
*     Set the light-emitting (LE) film operation mode for a device.
*
* ARGUMENTS:
*     handle           Device handle.
*     leOperationMode  LE film operation mode.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_SetLEOperationMode = libIBScanUltimate.IBSU_SetLEOperationMode
IBSU_SetLEOperationMode.restype = c_int
IBSU_SetLEOperationMode.argtypes = (c_int, c_int)


'''
****************************************************************************************************
* IBSU_GetLEOperationMode()
*
* DESCRIPTION:
*     Get the light-emitting (LE) film operation mode for a device.
*
* ARGUMENTS:
*     handle            Device handle.
*     pLeOperationMode  Pointer to variable that will receive LE film operation mode.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_GetLEOperationMode = libIBScanUltimate.IBSU_GetLEOperationMode
IBSU_GetLEOperationMode.restype = c_int
IBSU_GetLEOperationMode.argtypes = (c_int, POINTER(c_int))


'''
****************************************************************************************************
* IBSU_IsTouchedFinger()
*
* DESCRIPTION:
*     Determine whether a finger is on a scanner's surface.  This function queries the proximity
*     detector only integrated into some sensors.
*
* ARGUMENTS:
*     handle         Device handle.
*     pTouchInValue  Pointer to variable that will receive touch input value.  0 if no finger is
*                    touching the surface, 1 if one or more fingers are touching the surface.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_IsTouchedFinger = libIBScanUltimate.IBSU_IsTouchedFinger
IBSU_IsTouchedFinger.restype = c_int
IBSU_IsTouchedFinger.argtypes = (c_int, POINTER(c_int))


'''
****************************************************************************************************
* IBSU_GetOperableLEDs()
*
* DESCRIPTION:
*     Get characteristics of operable LEDs on a device.
*
* ARGUMENTS:
*     handle         Device handle.
*     pLedType       Pointer to variable that will receive type of LEDs.
*     pLedCount      Pointer to variable that will receive count of LEDs.
*     pOperableLEDs  Pointer to variable that will receive bit-pattern of operable LEDs.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_GetOperableLEDs = libIBScanUltimate.IBSU_GetOperableLEDs
IBSU_GetOperableLEDs.restype = c_int
IBSU_GetOperableLEDs.argtypes = (c_int, POINTER(c_int), POINTER(c_int), POINTER(c_uint))


'''
****************************************************************************************************
* IBSU_GetLEDs()
*
* DESCRIPTION:
*     Get the value of LEDs on a device.
*
* ARGUMENTS:
*     handle       Device handle.
*     pActiveLEDs  Pointer to variable that will receive bit-pattern of LED values.  Set bits
*                  indicate LEDs that are on; clear bits indicate LEDs that are off.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_GetLEDs = libIBScanUltimate.IBSU_GetLEDs
IBSU_GetLEDs.restype = c_int
IBSU_GetLEDs.argtypes = (c_int, POINTER(c_uint))


'''
****************************************************************************************************
* IBSU_SetLEDs()
*
* DESCRIPTION:
*     Set the value of LEDs on a device.
*
* ARGUMENTS:
*     handle      Device handle.
*     activeLEDs  Bit-pattern of LED values.  Set bits indicate LEDs to turn on; clear bits indicate
*                 LEDs to turn off.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_SetLEDs = libIBScanUltimate.IBSU_SetLEDs
IBSU_SetLEDs.restype = c_int
IBSU_SetLEDs.argtypes = (c_int, c_uint)


'''
****************************************************************************************************
* IBSU_BGetImage()
*
* DESCRIPTION:
*     Acquire an image from a device, blocking for result.  The split image array will only be
*     populated if the image is a result image, i.e., if the 'IsFinal' member of 'pImage' is set to
*     TRUE.
*
* ARGUMENTS:
*     handle                 Device handle.
*     pImage                 Pointer to structure that will receive data of preview or result image.
*                            The buffer in this structure points to an internal image buffer; the
*                            data should be copied to an application buffer if desired for future
*                            processing.
*     pImageType             Pointer to variable that will receive image type.
*     pSplitImageArray       Pointer to array of four structures that will receive individual finger
*                            images split from result image.  The buffers in these structures point
*                            to internal image buffers; the data should be copied to application
*                            buffers if desired for future processing.
*     pSplitImageArrayCount  Pointer to variable that will receive number of finger images split
*                            from result images.
*     pFingerCountState      Pointer to variable that will receive finger count state.
*     pQualityArray          Pointer to array of four variables that will receive quality states for
*                            finger images.
*     pQualityArrayCount     Pointer to variable that will receive number of finger qualities.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_BGetImage = libIBScanUltimate.IBSU_BGetImage
IBSU_BGetImage.restype = c_int
IBSU_BGetImage.argtypes = (c_int, POINTER(IBSU_ImageData), POINTER(c_int), POINTER(IBSU_ImageData), POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int))


'''
****************************************************************************************************
* IBSU_BGetImageEx()
*
* DESCRIPTION:
*     Acquire an image from a device, blocking for result.  The segment image array will only be
*     populated if the image is a result image, i.e., if the 'IsFinal' member of 'pImage' is set to
*     TRUE.
*
* ARGUMENTS:
*     handle                    Device handle.
*     pImageStatus              Pointer to variable that will receive status from result image acquisition.
*                               See error codes in 'IBScanUltimateApi_err'.
*     pImage                    Pointer to structure that will receive data of preview or result image.
*                               The buffer in this structure points to an internal image buffer; the
*                               data should be copied to an application buffer if desired for future
*                               processing.
*     pImageType                Pointer to variable that will receive image type.
*     pDetectedFingerCount      Pointer to variable that will receive detected finger count.
*     pSegmentImageArray        Pointer to array of four structures that will receive individual finger
*                               image segments from result image.  The buffers in these structures point
*                               to internal image buffers; the data should be copied to application
*                               buffers if desired for future processing.
*     pSegmentPositionArray     Pointer to array of four structures that will receive position data for
*                               individual fingers split from result image.
*     pSegmentImageArrayCount   Pointer to variable that will receive number of finger images split
*                               from result image.
*     pFingerCountState         Pointer to variable that will receive finger count state.
*     pQualityArray             Pointer to array of four variables that will receive quality states for
*                               finger images.
*     pQualityArrayCount        Pointer to variable that will receive number of finger qualities.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_BGetImageEx = libIBScanUltimate.IBSU_BGetImageEx
IBSU_BGetImageEx.restype = c_int
IBSU_BGetImageEx.argtypes = (c_int, POINTER(c_int), POINTER(IBSU_ImageData), POINTER(c_int), POINTER(c_int), POINTER(IBSU_ImageData), POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int))


'''
****************************************************************************************************
* IBSU_BGetClearPlatenAtCapture()
*
* DESCRIPTION:
*     Determine whether the platen was clear when capture was started or has since become clear.
*
* ARGUMENTS:
*     handle        Device handle.
*     pPlatenState  Pointer to variable that will receive platen state.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_BGetClearPlatenAtCapture = libIBScanUltimate.IBSU_BGetClearPlatenAtCapture
IBSU_BGetClearPlatenAtCapture.restype = c_int
IBSU_BGetClearPlatenAtCapture.argtypes = (c_int, POINTER(c_int))


'''
****************************************************************************************************
* IBSU_BGetRollingInfo()
*
* DESCRIPTION:
*     Get information about the status of the rolled print capture for a device.
*
* ARGUMENTS:
*     handle         Device handle.
*     pRollingState  Pointer to variable that will receive rolling state.
*     pRollingLineX  Pointer to variable that will receive x-coordinate of current "rolling line"
*                    for display as a guide.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_BGetRollingInfo = libIBScanUltimate.IBSU_BGetRollingInfo
IBSU_BGetRollingInfo.restype = c_int
IBSU_BGetRollingInfo.argtypes = (c_int, POINTER(c_int), POINTER(c_int))


'''
****************************************************************************************************
* IBSU_BGetRollingInfoEx()
*
* DESCRIPTION:
*     Get information about the status of the rolled print capture for a device.
*
* ARGUMENTS:
*     handle         Device handle.
*     pRollingState  Pointer to variable that will receive rolling state.
*     pRollingLineX  Pointer to variable that will receive x-coordinate of current "rolling line"
*                    for display as a guide.
*     pRollDirection Pointer to variable that will receive rolling direction
*                    0 : can't determin yet
*                    1 : left to right  --->
*                    2 : right to left  <---
*     pRollWidth     Pointer to vairable that will receive rolling width (mm)
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_BGetRollingInfoEx = libIBScanUltimate.IBSU_BGetRollingInfoEx
IBSU_BGetRollingInfoEx.restype = c_int
IBSU_BGetRollingInfoEx.argtypes = (c_int, POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int))

'''
****************************************************************************************************
* IBSU_GetIBSM_ResultImageInfo() (deprecated)
* 
* DESCRIPTION:
*     Get result image information.
*
* ARGUMENTS:
*     handle                  Device handle.
*     fingerPosition          Finger position.
*     pResultImage            Pointer to structure that will receive data of preview or result image.   
*                             The buffer in this structure points to an internal image buffer; the 
*                             data should be copied to an application buffer if desired for future 
*                             processing.
*     pSplitResultImage       Pointer to array of four structures that will receive individual finger 
*                             images split from result image.  The buffers in these structures point
*                             to internal image buffers; the data should be copied to application 
*                             buffers if desired for future processing.
*     pSplitResultImageCount  Pointer to variable that will receive number of finger images split 
*                             from result image.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_GetIBSM_ResultImageInfo = libIBScanUltimate.IBSU_GetIBSM_ResultImageInfo
IBSU_GetIBSM_ResultImageInfo.restype = c_int
IBSU_GetIBSM_ResultImageInfo.argtypes = (c_int, c_int, POINTER(IBSM_ImageData), POINTER(IBSM_ImageData), POINTER(c_int))


'''
****************************************************************************************************
* IBSU_CreateClientWindow()
*
* DESCRIPTION:
*     Create client window associated with device.  (Available only on Windows.)
*
* ARGUMENTS:
*     handle   Device handle.
*     hWindow  Windows handle to draw.
*     left     Coordinate of left edge of rectangle.
*     top      Coordinate of top edge of rectangle.
*     right    Coordinate of right edge of rectangle.
*     bottom   Coordinate of bottom edge of rectangle.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_CreateClientWindow = libIBScanUltimate.IBSU_CreateClientWindow
IBSU_CreateClientWindow.restype = c_int
IBSU_CreateClientWindow.argtypes = (c_int, c_int, c_uint, c_uint, c_uint, c_uint)


'''
****************************************************************************************************
* IBSU_DestroyClientWindow()
*
* DESCRIPTION:
*     Destroy client window associated with device.  (Available only on Windows.)
*
* ARGUMENTS:
*     handle             Device handle.
*     clearExistingInfo  Indicates whether the existing display information, including display
*                        properties and overlay text, will be cleared.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_DestroyClientWindow = libIBScanUltimate.IBSU_DestroyClientWindow
IBSU_DestroyClientWindow.restype = c_int
IBSU_DestroyClientWindow.argtypes = (c_int, c_bool)


'''
****************************************************************************************************
* IBSU_GetClientWindowProperty()
*
* DESCRIPTION:
*     Get the value of a property for the client window associated with a device.  For descriptions
*     of properties and values, see definition of 'IBSU_ClientWindowPropertyId'.  (Available only on
*     Windows.)
*
* ARGUMENTS:
*     handle          Device handle.
*     propertyId      Property for which value will be set.
*     propertyValue   Buffer in which value of property will be stored.  This buffer should be
*                     able to hold IBSU_MAX_STR_LEN characters.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_GetClientWindowProperty = libIBScanUltimate.IBSU_GetClientWindowProperty
IBSU_GetClientWindowProperty.restype = c_int
IBSU_GetClientWindowProperty.argtypes = (c_int, c_int, POINTER(c_char))


'''
****************************************************************************************************
* IBSU_SetClientDisplayProperty()
*
* DESCRIPTION:
*     Set the value of a property for the client window associated with a device.  For descriptions
*     of properties and values, see definition of 'IBSU_ClientWindowPropertyId'.  (Available only on
*     Windows.)
*
* ARGUMENTS:
*     handle          Device handle.
*     propertyId      Property for which value will be set.
*     propertyValue   Value of property to set.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_SetClientDisplayProperty = libIBScanUltimate.IBSU_SetClientDisplayProperty
IBSU_SetClientDisplayProperty.restype = c_int
IBSU_SetClientDisplayProperty.argtypes = (c_int, c_int, c_char_p)


'''
****************************************************************************************************
* IBSU_SetClientWindowOverlayText()
*
* DESCRIPTION:
*     Set the overlay text for the client window associated with a device.  (Available only on
*     Windows.)  (Deprecated.)
*
* ARGUMENTS:
*     handle     Device handle.
*     fontName   Font name.
*     fontSize   Font size.
*     fontBold   Indicates whether font will be bold.
*     text       Text to display.
*     posX       X-coordinate of text.
*     poxY       Y-coordinate of text.
*     textColor  Color of text.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_SetClientWindowOverlayText = libIBScanUltimate.IBSU_SetClientWindowOverlayText
IBSU_SetClientWindowOverlayText.restype = c_int
IBSU_SetClientWindowOverlayText.argtypes = (c_int, c_char_p, c_int, c_bool, c_char_p, c_int, c_int, c_uint)


'''
****************************************************************************************************
* IBSU_GenerateZoomOutImage()
*
* DESCRIPTION:
*     Generate scaled version of image.
*
* ARGUMENTS:
*     inImage     Original image.
*     outImage    Pointer to buffer that will receive output image.  This buffer must hold at least
*                 'outWidth' x 'outHeight' bytes.
*     outWidth    Width of output image.
*     outHeight   Height of output image.
*     bkColor     Background color of output image.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_GenerateZoomOutImage = libIBScanUltimate.IBSU_GenerateZoomOutImage
IBSU_GenerateZoomOutImage.restype = c_int
IBSU_GenerateZoomOutImage.argtypes = (POINTER(IBSU_ImageData), POINTER(c_char), c_int, c_int, c_byte)


'''
****************************************************************************************************
* IBSU_GenerateZoomOutImageEx()
*
* DESCRIPTION:
*     Generate scaled version of image.
*
* ARGUMENTS:
*     inImage     Original image data.
*     inWidth     Width of input image.
*     in Height   Height of input image.
*     outImage    Pointer to buffer that will receive output image.  This buffer must hold at least
*                 'outWidth' x 'outHeight' bytes.
*     outWidth    Width of output image.
*     outHeight   Height of output image.
*     bkColor     Background color of output image.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_GenerateZoomOutImageEx = libIBScanUltimate.IBSU_GenerateZoomOutImageEx
IBSU_GenerateZoomOutImageEx.restype = c_int
IBSU_GenerateZoomOutImageEx.argtypes = (c_void_p, c_int, c_int, POINTER(c_char), c_int, c_int, c_byte)


'''
****************************************************************************************************
* IBSU_SaveBitmapImage()
*
* DESCRIPTION:
*     Save image to bitmap file.
*
* ARGUMENTS:
*     filePath   Path of file for output image.
*     imgBuffer  Pointer to image buffer.
*     width      Image width (in pixels).
*     height     Image height (in pixels).
*     pitch      Image line pitch (in bytes).  A positive value indicates top-down line order; a
*                negative value indicates bottom-up line order.
*     resX       Horizontal image resolution (in pixels/inch).
*     resY       Vertical image resolution (in pixels/inch).
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_SaveBitmapImage = libIBScanUltimate.IBSU_SaveBitmapImage
IBSU_SaveBitmapImage.restype = c_int
IBSU_SaveBitmapImage.argtypes = (c_char_p, c_void_p, c_uint, c_uint, c_int, c_double, c_double)


'''
****************************************************************************************************
* IBSU_GetNFIQScore()
*
* DESCRIPTION:
*     Calculate NFIQ score for image.
*
* ARGUMENTS:
*     handle        Device handle.
*     imgBuffer     Pointer to image buffer.
*     width         Image width (in pixels).
*     height        Image height (in pixels).
*     bitsPerPixel  Bits per pixel.
*     pScore        Pointer to variable that will receive NFIQ score.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_GetNFIQScore = libIBScanUltimate.IBSU_GetNFIQScore
IBSU_GetNFIQScore.restype = c_int
IBSU_GetNFIQScore.argtypes = (c_int, c_void_p, c_uint, c_uint, c_byte, POINTER(c_int))


'''
****************************************************************************************************
* IBSU_ReleaseCallbacks()
*
* DESCRIPTION:
*     Unregister a callback function for a particular event.
*
* ARGUMENTS:
*     handle  Handle for device associated with this event (if appropriate).
*     event   Event for which the callback is being unregistered.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_ReleaseCallbacks = libIBScanUltimate.IBSU_ReleaseCallbacks
IBSU_ReleaseCallbacks.restype = c_int
IBSU_ReleaseCallbacks.argtypes = (c_int, c_uint)


'''
****************************************************************************************************
* IBSU_SaveBitmapMem()
*
* DESCRIPTION:
*     Save image to bitmap memory.
*
* ARGUMENTS:
*     inImage           Point to image data (gray scale image).
*     inWidth           Image width (in pixels).
*     inHeight          Image height (in pixels).
*     inPitch           Image line pitch (in bytes).  A positive value indicates top-down line order; a
*                       negative value indicates bottom-up line order.
*     inResX            Horizontal image resolution (in pixels/inch).
*     inResY            Vertical image resolution (in pixels/inch).
*     outBitmapBuffer   Pointer to output image data buffer which is set image format and zoom-out factor.
*                       Required memory buffer size depends upon the output image format (outImageFormat):
*                           for IBSU_IMG_FORMAT_GRAY:  IBSU_BMP_GRAY_HEADER_LEN  + outWidth * outHeight bytes
*                           for IBSU_IMG_FORMAT_RGB24: IBSU_BMP_RGB24_HEADER_LEN + 3 * outWidth * outHeight bytes
*                           for IBSU_IMG_FORMAT_RGB32: IBSU_BMP_RGB32_HEADER_LEN + 4 * outWidth * outHeight bytes
*     outImageFormat    Set Image color format for output image
*     outWidth          Width for zoom-out image
*     outHeight         Height for zoom-out image
*     bkColor           Background color for remain area from zoom-out image
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_SaveBitmapMem = libIBScanUltimate.IBSU_SaveBitmapMem
IBSU_SaveBitmapMem.restype = c_int
IBSU_SaveBitmapMem.argtypes = (c_void_p, c_uint, c_uint, c_int, c_double, c_double, POINTER(c_byte), c_int, c_uint, c_uint, c_byte)


'''
****************************************************************************************************
* IBSU_ShowOverlayObject()
*
* DESCRIPTION:
*     Show or hide an overlay object.
*
* ARGUMENTS:
*     handle        Handle for device associated with this event (if appropriate).
*     overlayHandle Overlay handle obtained by overlay functions.
*     show          If TRUE, the overlay will be shown on client window.
*                   If FALSE, the overlay will be hidden on client window.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_ShowOverlayObject = libIBScanUltimate.IBSU_ShowOverlayObject
IBSU_ShowOverlayObject.restype = c_int
IBSU_ShowOverlayObject.argtypes = (c_int, c_int, c_bool)


'''
****************************************************************************************************
* IBSU_ShowAllOverlayObject()
*
* DESCRIPTION:
*     Show or hide all overlay objects.
*
* ARGUMENTS:
*     handle  Handle for device associated with this event (if appropriate).
*     show    If TRUE, the overlay will be shown on client window.
*             If FALSE, the overlay will be hidden on client window.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_ShowAllOverlayObject = libIBScanUltimate.IBSU_ShowAllOverlayObject
IBSU_ShowAllOverlayObject.restype = c_int
IBSU_ShowAllOverlayObject.argtypes = (c_int, c_bool)


'''
****************************************************************************************************
* IBSU_RemoveOverlayObject()
*
* DESCRIPTION:
*     Remove an overlay object.
*
* ARGUMENTS:
*     handle         Handle for device associated with this event (if appropriate).
*     overlayHandle  Overlay handle obtained by overlay functions.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_RemoveOverlayObject = libIBScanUltimate.IBSU_RemoveOverlayObject
IBSU_RemoveOverlayObject.restype = c_int
IBSU_RemoveOverlayObject.argtypes = (c_int, c_int)


'''
****************************************************************************************************
* IBSU_RemoveAllOverlayObject()
*
* DESCRIPTION:
*     Remove all overlay objects.
*
* ARGUMENTS:
*     handle  Handle for device associated with this event (if appropriate).
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_RemoveAllOverlayObject = libIBScanUltimate.IBSU_RemoveAllOverlayObject
IBSU_RemoveAllOverlayObject.restype = c_int
IBSU_RemoveAllOverlayObject.argtype = c_int


'''
****************************************************************************************************
* IBSU_AddOverlayText()
*
* DESCRIPTION:
*     Add an overlay text for display on window.
*
* ARGUMENTS:
*     handle         Handle for device associated with this event (if appropriate).
*     pOverlayHandle Function returns overlay handle to be used for client windows function call.
*     fontName       Name of font.
*     fontSize       Font size.
*     fontBold       Indicates whether font is bold.
*     text           Text for display on window.
*     posX           X coordinate of text for display on window.
*     posY           Y coordinate of text for display on window.
*     textColor      Text color.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_AddOverlayText = libIBScanUltimate.IBSU_AddOverlayText
IBSU_AddOverlayText.restype = c_int
IBSU_AddOverlayText.argtypes = (c_int, POINTER(c_int), c_char_p, c_int, c_bool, c_char_p, c_int, c_int, c_uint)


'''
****************************************************************************************************
* IBSU_ModifyOverlayText()
*
* DESCRIPTION:
*     Modify an existing overlay text for display on window.
*
* ARGUMENTS:
*     handle         Handle for device associated with this event (if appropriate).
*     overlayHandle  Handle of overlay to modify.
*     fontName       Name of font.
*     fontSize       Font size.
*     fontBold       Indicates whether font is bold.
*     text           Text for display on window.
*     posX           X coordinate of text for display on window.
*     posY           Y coordinate of text for display on window.
*     textColor      Text color.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_ModifyOverlayText = libIBScanUltimate.IBSU_ModifyOverlayText
IBSU_ModifyOverlayText.restype = c_int
IBSU_ModifyOverlayText.argtypes = (c_int, c_int, c_char_p, c_int, c_bool, c_char_p, c_int, c_int, c_uint)


'''
****************************************************************************************************
* IBSU_AddOverlayLine()
*
* DESCRIPTION:
*     Add an overlay line for display on window.
*
* ARGUMENTS:
*     handle          Handle for device associated with this event (if appropriate).
*     pOverlayHandle  Function returns overlay handle to be used for client windows function calls.
*     x1              X coordinate of start point of line.
*     y1              Y coordinate of start point of line.
*     x2              X coordinate of end point of line.
*     y2              Y coordinate of end point of line.
*     lineWidth       Line width.
*     lineColor       Line color.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_AddOverlayLine = libIBScanUltimate.IBSU_AddOverlayLine
IBSU_AddOverlayLine.restype = c_int
IBSU_AddOverlayLine.argtypes = (c_int, POINTER(c_int), c_int, c_int, c_int, c_int, c_int, c_uint)


'''
****************************************************************************************************
* IBSU_ModifyOverlayLine()
*
* DESCRIPTION:
*     Modify an existing line for display on window
*
* ARGUMENTS:
*     handle         Handle for device associated with this event (if appropriate).
*     overlayHandle  Handle of overlay to modify.
*     x1             X coordinate of start point of line.
*     y1             Y coordinate of start point of line.
*     x2             X coordinate of end point of line.
*     y2             Y coordinate of end point of line.
*     lineWidth      Line width.
*     lineColor      Line color.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_ModifyOverlayLine = libIBScanUltimate.IBSU_ModifyOverlayLine
IBSU_ModifyOverlayLine.restype = c_int
IBSU_ModifyOverlayLine.argtypes = (c_int, c_int, c_int, c_int, c_int, c_int, c_int, c_uint)


'''
****************************************************************************************************
* IBSU_AddOverlayQuadrangle()
*
* DESCRIPTION:
*     Add an overlay quadrangle for display on window
*
* ARGUMENTS:
*     handle          Handle for device associated with this event (if appropriate).
*     pOverlayHandle  Function returns overlay handle to be used for client windows function calls.
*     x1              X coordinate of 1st vertex of quadrangle.
*     y1              Y coordinate of 1st vertex of quadrangle.
*     x2              X coordinate of 2nd vertex of quadrangle.
*     y2              Y coordinate of 2nd vertex of quadrangle.
*     x3              X coordinate of 3rd vertex of quadrangle.
*     y3              Y coordinate of 3rd vertex of quadrangle.
*     x4              X coordinate of 4th vertex of quadrangle.
*     y4              Y coordinate of 4th vertex of quadrangle.
*     lineWidth       Line width.
*     lineColor       Line color.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_AddOverlayQuadrangle = libIBScanUltimate.IBSU_AddOverlayQuadrangle
IBSU_AddOverlayQuadrangle.restype = c_int
IBSU_AddOverlayQuadrangle.argtypes = (c_int, POINTER(c_int), c_int, c_int, c_int, c_int, c_int, c_int, c_int, c_int, c_int, c_uint)


'''
****************************************************************************************************
* IBSU_ModifyOverlayQuadrangle()
*
* DESCRIPTION:
*     Modify an existing quadrangle for display on window
*
* ARGUMENTS:
*     handle         Handle for device associated with this event (if appropriate).
*     overlayHandle  Handle of overlay to be modified.
*     x1             X coordinate of 1st vertex of quadrangle.
*     y1             Y coordinate of 1st vertex of quadrangle.
*     x2             X coordinate of 2nd vertex of quadrangle.
*     y2             Y coordinate of 2nd vertex of quadrangle.
*     x3             X coordinate of 3rd vertex of quadrangle.
*     y3             Y coordinate of 3rd vertex of quadrangle.
*     x4             X coordinate of 4th vertex of quadrangle.
*     y4             Y coordinate of 4th vertex of quadrangle.
*     lineWidth      Line width.
*     lineColor      Line color.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_ModifyOverlayQuadrangle = libIBScanUltimate.IBSU_ModifyOverlayQuadrangle
IBSU_ModifyOverlayQuadrangle.restype = c_int
IBSU_ModifyOverlayQuadrangle.argtypes = (c_int, c_int, c_int, c_int, c_int, c_int, c_int, c_int, c_int, c_int, c_int, c_uint)


'''
****************************************************************************************************
* IBSU_AddOverlayShape()
*
* DESCRIPTION:
*     Add an overlay shape for display on window
*
* ARGUMENTS:
*     handle          Handle for device associated with this event (if appropriate).
*     pOverlayHandle  Function returns overlay handle to be used for client windows function calls.
*     shapePattern    Pattern of shape.  If ENUM_IBSU_OVERLAY_SHAPE_ARROW, reserved_1 should be
*                     the width (in pixels) of the full base of the arrowhead, and reserved_1
*                     should be the angle (in radians) at the arrow tip between the two sides
*                     of the arrowhead.
*     x1              X coordinate of start point of overlay shape.
*     y1              Y coordinate of start point of overlay shape.
*     x2              X coordinate of end point of overlay shape.
*     y2              Y coordinate of end point of overlay shape.
*     lineWidth       Line width.
*     lineColor       Line color.
*     reserved_1      X reserved.
*     reserved_2      Y reserved.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_AddOverlayShape = libIBScanUltimate.IBSU_AddOverlayShape
IBSU_AddOverlayShape.restype = c_int
IBSU_AddOverlayShape.argtypes = (c_int, POINTER(c_int), c_int, c_int, c_int, c_int, c_int, c_int, c_uint, c_int, c_int)


'''
****************************************************************************************************
* IBSU_ModifyOverlayShape()
*
* DESCRIPTION:
*     Modify an overlay shape for display on window
*
* ARGUMENTS:
*     handle         Handle for device associated with this event (if appropriate).
*     overlayHandle  Handle of overlay to modify.
*     shapePattern   Pattern of shape.  If ENUM_IBSU_OVERLAY_SHAPE_ARROW, reserved_1 should be
*                    the width (in pixels) of the full base of the arrowhead, and reserved_1
*                    should be the angle (in radians) at the arrow tip between the two sides
*                    of the arrowhead.
*     x1             X coordinate of start point of overlay shape.
*     y1             Y coordinate of start point of overlay shape.
*     x2             X coordinate of end point of overlay shape.
*     y2             Y coordinate of end point of overlay shape.
*     lineWidth      Line width.
*     lineColor      Line color.
*     reserved_1     X reserved.
*     reserved_2     Y reserved.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_ModifyOverlayShape = libIBScanUltimate.IBSU_ModifyOverlayShape
IBSU_ModifyOverlayShape.restype = c_int
IBSU_ModifyOverlayShape.argtypes = (c_int, c_int, c_int, c_int, c_int, c_int, c_int, c_int, c_uint, c_int, c_int)


'''
****************************************************************************************************
* IBSU_WSQEncodeMem()
*
* DESCRIPTION:
*     WSQ compresses grayscale fingerprint image.
*
* ARGUMENTS:
*     image             Original image.
*     width             Width of original image (in pixels).
*     height            Height of original image (in pixels).
*     pitch             Image line pitch (in bytes).  A positive value indicates top-down line order; a
*                       negative value indicates bottom-up line order.
*     bitsPerPixel      Bits per pixel of original image.
*     pixelPerInch      Pixel per inch of original image.
*     bitRate           Determines the amount of lossy compression.
                        Suggested settings:
                        bitRate = 2.25 yields around 5:1 compression
                        bitRate = 0.75 yields around 15:1 compression
*     commentText       Comment to write compressed data.
*     compressedData    Pointer of image which is compressed from original image by WSQ compression.
*                       This pointer is deallocated by IBSU_FreeMemory() after using it.
*     compressedLength  Length of image which is compressed from original image by WSQ compression.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_WSQEncodeMem = libIBScanUltimate.IBSU_WSQEncodeMem
IBSU_WSQEncodeMem.restype = c_int
IBSU_WSQEncodeMem.argtypes = (c_void_p, c_int, c_int, c_int, c_int, c_int, c_double, c_char_p, POINTER(POINTER(c_byte)), POINTER(c_int))


'''
****************************************************************************************************
* IBSU_WSQEncodeToFile()
*
* DESCRIPTION:
*     Save WSQ compresses grayscale fingerprint image to specific file path.
*
* ARGUMENTS:
*     filePath          File path to save image which is compressed from original image by WSQ compression.
*     image             Original image.
*     width             Width of original image (in pixels).
*     height            Height of original image (in pixels).
*     pitch             Image line pitch (in bytes).  A positive value indicates top-down line order; a
*                       negative value indicates bottom-up line order.
*     bitsPerPixel      Bits per pixel of original image.
*     pixelPerInch      Pixel per inch of original image.
*     bitRate           Determines the amount of lossy compression.
                        Suggested settings:
                        bitRate = 2.25 yields around 5:1 compression
                        bitRate = 0.75 yields around 15:1 compression
*     commentText       Comment to write compressed data.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_WSQEncodeToFile = libIBScanUltimate.IBSU_WSQEncodeToFile
IBSU_WSQEncodeToFile.restype = c_int
IBSU_WSQEncodeToFile.argtypes = (c_char_p, c_void_p, c_int, c_int, c_int, c_int, c_int, c_double, c_char_p)


'''
****************************************************************************************************
* IBSU_WSQDecodeMem()
*
* DESCRIPTION:
*     Decompress a WSQ-encoded grayscale fingerprint image.
*
* ARGUMENTS:
*     compressedImage   WSQ-encoded image.
*     compressedLength  Length of WSQ-encoded image.
*     decompressedImage Pointer of image which is decompressed from WSQ-encoded image.
*                       This pointer is deallocated by IBSU_FreeMemory() after using it.
*     outWidth          Width of decompressed image (in pixels).
*     outHeight         Height of decompressed image (in pixels).
*     outPitch          Image line pitch (in bytes).  A positive value indicates top-down line order; a
*                       negative value indicates bottom-up line order.
*     outBitsPerPixel   Bits per pixel of decompressed image.
*     outPixelPerInch   Pixel per inch of decompressed image.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_WSQDecodeMem = libIBScanUltimate.IBSU_WSQDecodeMem
IBSU_WSQDecodeMem.restype = c_int
IBSU_WSQDecodeMem.argtypes = (c_void_p, c_int, POINTER(POINTER(c_byte)), POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int))


'''
****************************************************************************************************
* IBSU_WSQDecodeFromFile()
*
* DESCRIPTION:
*     Decompress a WSQ-encoded grayscale fingerprint image from specific file path.
*
* ARGUMENTS:
*     filePath          File path of WSQ-encoded image.
*     decompressedImage Pointer of image which is decompressed from WSQ-encoded image.
*                       This pointer is deallocated by IBSU_FreeMemory() after using it.
*     outWidth          Width of decompressed image (in pixels).
*     outHeight         Height of decompressed image (in pixels).
*     outPitch          Image line pitch (in bytes).  A positive value indicates top-down line order; a
*                       negative value indicates bottom-up line order.
*     outBitsPerPixel   Bits per pixel of decompressed image.
*     outPixelPerInch   Pixel per inch of decompressed image.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_WSQDecodeFromFile = libIBScanUltimate.IBSU_WSQDecodeFromFile
IBSU_WSQDecodeFromFile.restype = c_int
IBSU_WSQDecodeFromFile.argtypes = (c_char_p, POINTER(POINTER(c_byte)), POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int))


'''
****************************************************************************************************
* IBSU_FreeMemory()
*
* DESCRIPTION:
*     Release the allocated memory block on the internal heap of library.
*     This is obtained by IBSU_WSQEncodeMem(), IBSU_WSQDecodeMem, IBSU_WSQDecodeFromFile() and other API functions.
*
* ARGUMENTS:
*     memblock          Previously allocated memory block to be freed.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_FreeMemory = libIBScanUltimate.IBSU_FreeMemory
IBSU_FreeMemory.restype = c_int
IBSU_FreeMemory.argtype = c_void_p


'''
****************************************************************************************************
* IBSU_SavePngImage()
*
* DESCRIPTION:
*     Save image to PNG file.
*
* ARGUMENTS:
*     filePath   Path of file for output image.
*     imgBuffer  Pointer to image buffer.
*     width      Image width (in pixels).
*     height     Image height (in pixels).
*     pitch      Image line pitch (in bytes).  A positive value indicates top-down line order; a
*                negative value indicates bottom-up line order.
*     resX       Horizontal image resolution (in pixels/inch).
*     resY       Vertical image resolution (in pixels/inch).
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_SavePngImage = libIBScanUltimate.IBSU_SavePngImage
IBSU_SavePngImage.restype = c_int
IBSU_SavePngImage.argtypes = (c_char_p, c_void_p, c_uint, c_uint, c_int, c_double, c_double)


'''
****************************************************************************************************
* IBSU_SaveJP2Image()
*
* DESCRIPTION:
*     Save image to JPEG-2000 file.
*
* ARGUMENTS:
*     filePath   Path of file for output image.
*     imgBuffer  Pointer to image buffer.
*     width      Image width (in pixels).
*     height     Image height (in pixels).
*     pitch      Image line pitch (in bytes).  A positive value indicates top-down line order; a
*                negative value indicates bottom-up line order.
*     resX       Horizontal image resolution (in pixels/inch).
*     resY       Vertical image resolution (in pixels/inch).
*     fQuality   Quality level for JPEG2000, the valid range is between 0 and 100
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_SaveJP2Image = libIBScanUltimate.IBSU_SaveJP2Image
IBSU_SaveJP2Image.restype = c_int
IBSU_SaveJP2Image.argtypes = (c_char_p, c_void_p, c_uint, c_uint, c_int, c_double, c_double, c_int)

'''
****************************************************************************************************
* IBSU_RedrawClientWindow()
*
* DESCRIPTION:
*     Update the specified client window which is defined by IBSU_CreateClientWindow().  (Available only on Windows.)
*
* ARGUMENTS:
*     handle          Device handle.
*     flags           Bit-pattern of redraw flags.  See flag codes in 'IBScanUltimateApi_def
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_RedrawClientWindow = libIBScanUltimate.IBSU_RedrawClientWindow
IBSU_RedrawClientWindow.restype = c_int
IBSU_RedrawClientWindow.argtype = c_int


'''
****************************************************************************************************
* IBSU_UnloadLibrary()
*
* DESCRIPTION:
*     The library is unmapped from the address space manually, and the library is no longer valid
*     So APIs will not be worked correctly after calling
*     Some platform SDKs (Windows Mobile, Android)
*     can be needed to call IBSU_UnloadLibrary() before shutting down the application.
*
* ARGUMENTS:
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_UnloadLibrary = libIBScanUltimate.IBSU_UnloadLibrary
IBSU_UnloadLibrary.restype = c_int


'''
****************************************************************************************************
* IBSU_CombineImage()
*
* DESCRIPTION:
*     Combine two images (2 flat fingers) into a single image (left/right hands)
*
* ARGUMENTS:
*     inImage1		  Pointer to IBSU_ImageData ( index and middle finger )
*     inImage2		  Pointer to IBSU_ImageData ( ring and little finger )
*	  whichHand		  Information of left or right hand
*     outImage		  Pointer to IBSU_ImageData ( 1600 x 1500 fixed size image )
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_CombineImage = libIBScanUltimate.IBSU_CombineImage
IBSU_CombineImage.restype = c_int
IBSU_CombineImage.argtypes = (IBSU_ImageData, IBSU_ImageData, c_int, POINTER(IBSU_ImageData))


'''
****************************************************************************************************
* IBSU_CombineImageEx()
*
* DESCRIPTION:
*     Combine two images (2 flat fingers) into a single image (left/right hands)
*     and return segment information as well
*
* ARGUMENTS:
*     inImage1					Pointer to IBSU_ImageData ( index and middle finger )
*     inImage2					Pointer to IBSU_ImageData ( ring and little finger )
*	  whichHand					Information of left or right hand
*     outImage					Pointer to IBSU_ImageData ( 1600 x 1500 fixed size image )
*     pSegmentImageArray        Pointer to array of four structures that will receive individual finger
*                               image segments from output image.  The buffers in these structures point
*                               to internal image buffers; the data should be copied to application
*                               buffers if desired for future processing.
*     pSegmentPositionArray     Pointer to array of four structures that will receive position data for
*                               individual fingers split from output image.
*     pSegmentImageArrayCount   Pointer to variable that will receive number of finger images split
*                               from output image.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_CombineImageEx = libIBScanUltimate.IBSU_CombineImageEx
IBSU_CombineImageEx.restype = c_int
IBSU_CombineImageEx.argtypes = (IBSU_ImageData, IBSU_ImageData, c_int, POINTER(IBSU_ImageData), POINTER(IBSU_ImageData), POINTER(IBSU_SegmentPosition), POINTER(c_int))


'''
/****************************************************************************************************
* IBSU_GetOperableBeeper()
*
* DESCRIPTION:
*     Get characteristics of operable Beeper on a device.
*
* ARGUMENTS:
*     handle         Device handle.
*     pBeeperType    Pointer to variable that will receive type of Beeper.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_GetOperableBeeper = libIBScanUltimate.IBSU_GetOperableBeeper
IBSU_GetOperableBeeper.restype = c_int
IBSU_GetOperableBeeper.argtypes = (c_int, POINTER(c_int))


'''
****************************************************************************************************
* IBSU_SetBeeper()
*
* DESCRIPTION:
*     Set the value of Beeper on a device.
*
* ARGUMENTS:
*     handle          Device handle.
*     beepPattern     Pattern of beep.
*     soundTone       The frequency of the sound, in specific value. The parameter must be
*                     in the range 0 through 2.
*     duration        The duration of the sound, in 25 miliseconds. The parameter must be
*                     in the range 1 through 200 at ENUM_IBSU_BEEP_PATTERN_GENERIC,
*                     in the range 1 through 7 at ENUM_IBSU_BEEP_PATTERN_REPEAT.
*     reserved_1      Reserved
*     reserved_2      Reserved
*                     If you set beepPattern to ENUM_IBSU_BEEP_PATTERN_REPEAT
*                     reserved_1 can use the sleep time after duration of the sound, in 25 miliseconds.
*                     The parameter must be in the range 1 through 8
*                     reserved_2 can use the operation(start/stop of pattern repeat), 1 to start; 0 to stop
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_SetBeeper = libIBScanUltimate.IBSU_SetBeeper
IBSU_SetBeeper.restype = c_int
IBSU_SetBeeper.argtypes = (c_int, c_int, c_uint, c_uint, c_uint, c_uint)


'''
****************************************************************************************************
* IBSU_CheckWetFinger()
*
* DESCRIPTION:
*     Check if the image is wet or not.
*
* ARGUMENTS:
*     handle                 Device handle.
*     inImage                Input image data which is returned from result callback.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See warning codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_CheckWetFinger = libIBScanUltimate.IBSU_CheckWetFinger
IBSU_CheckWetFinger.restype = c_int
IBSU_CheckWetFinger.argtypes = (c_int, c_int, c_uint, c_uint, c_uint, c_uint)


'''
****************************************************************************************************
* IBSU_GetImageWidth()
*
* DESCRIPTION:
*     Get the image width of input image by millimeter(mm).
*
* ARGUMENTS:
*     handle                 Device handle.
*     inImage                Input image data which is returned from result callback.
*     Width_MM				 Output millimeter (width) of Input image.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See warning codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_GetImageWidth = libIBScanUltimate.IBSU_GetImageWidth
IBSU_GetImageWidth.restype = c_int
IBSU_GetImageWidth.argtypes = (c_int, IBSU_ImageData, POINTER(c_int))


'''
****************************************************************************************************
* IBSU_IsWritableDirectory()
*
* DESCRIPTION:
*     Check whether a directory is writable.
*
* ARGUMENTS:
*     dirpath                Directory path.
*     needCreateSubFolder	 Check whether need to create subfolder into the directory path.
*
* RETURNS:
*     IBSU_STATUS_OK, if a directory is writable.
*     Error code < 0, otherwise.  See warning codes in 'IBScanUltimateApi_err'.
*         IBSU_ERR_CHANNEL_IO_WRITE_FAILED: Directory does not writable.
****************************************************************************************************
'''
IBSU_IsWritableDirectory = libIBScanUltimate.IBSU_IsWritableDirectory
IBSU_IsWritableDirectory.restype = c_int
IBSU_IsWritableDirectory.argtypes = (c_char_p, c_bool)


'''
****************************************************************************************************
* RESERVED_GetFinalImageByNative()
* 
* DESCRIPTION:
*     get a native image for the final capture.
*
* ARGUMENTS:
*     handle                 Device handle.
*     pReservedKey           Key to unlock reserved functionality.
*     finalImage             Pointer to structure that will receive data of final image by native
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
RESERVED_GetFinalImageByNative = libIBScanUltimate.IBSU_GenerateDisplayImage
RESERVED_GetFinalImageByNative.restype = c_int
RESERVED_GetFinalImageByNative.argtypes = (c_int, POINTER(c_char), POINTER(IBSU_ImageData))
     
     
'''
****************************************************************************************************
* IBSU_GenerateDisplayImage()
* 
* DESCRIPTION:
*     Generate scaled image in various formats for fast image display on canvas.
*     You can use instead of IBSU_GenerateZoomOutImageEx()
*
* ARGUMENTS:
*     inImage     Original grayscale image data.
*     inWidth     Width of input image.
*     in Height   Height of input image.
*     outImage    Pointer to buffer that will receive output image.  This buffer must hold at least
*                 'outWidth' x 'outHeight' x 'bitsPerPixel' bytes.
*     outWidth    Width of output image.
*     outHeight   Height of output image.
*     outBkColor     Background color of output image.
*     outFormat   IBSU_ImageFormat of output image.
*     outQualityLevel  Image quality of output image. The parameter must be in the range 0 through 2
*     outVerticalFlip  Enable/disable vertical flip of output image.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_GenerateDisplayImage = libIBScanUltimate.IBSU_GenerateDisplayImage
IBSU_GenerateDisplayImage.restype = c_int
IBSU_GenerateDisplayImage.argtypes = (c_void_p, c_int, c_int, POINTER(c_char), c_int, c_int, c_byte, c_int, c_int, c_bool)


'''
****************************************************************************************************
* IBSU_RemoveFingerImages()
* 
* DESCRIPTION:
*     Remove finger images.
* 
* ARGUMENTS:
*     handle              Handle for device associated with this event (if appropriate).
*     fIndex              Bit-pattern of finger index of input image. 
*                         ex) IBSU_FINGER_LEFT_LITTLE | IBSU_FINGER_LEFT_RING in IBScanUltimateApi_defs.h
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_RemoveFingerImage = libIBScanUltimate.IBSU_RemoveFingerImage
IBSU_RemoveFingerImage.restype = c_int
IBSU_RemoveFingerImage.argtypes = (c_int, c_uint)


'''
****************************************************************************************************
* IBSU_AddFingerImage()
* 
* DESCRIPTION:
*     Add an finger image for the fingerprint duplicate check and roll to slap comparison.
*     It can have only ten prints 
* 
* ARGUMENTS:
*     handle              Handle for device associated with this event (if appropriate).
*     image               input image data.
*     fIndex              Bit-pattern of finger index of input image. 
*                         ex) IBSU_FINGER_LEFT_LITTLE | IBSU_FINGER_LEFT_RING in IBScanUltimateApi_defs.h
*     imageType           Image type of input image.
*     flagForce           Indicates whether input image should be saved even if another image is already stord or not.  TRUE to be stored force; FALSE to 
*                         be not stored force.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_AddFingerImage = libIBScanUltimate.IBSU_AddFingerImage
IBSU_AddFingerImage.restype = c_int
IBSU_AddFingerImage.argtypes = (c_int, IBSU_ImageData, c_uint, c_int, c_bool)


'''
****************************************************************************************************
* IBSU_IsFingerDuplicated()
* 
* DESCRIPTION:
*     Checks for the fingerprint duplicate from the stored prints by IBSU_AddFingerImage(). 
* 
* ARGUMENTS:
*     handle              Handle for device associated with this event (if appropriate).
*     image               input image data for the fingerprint duplicate check.
*     fIndex              Bit-pattern of finger index of input image. 
*                         ex) IBSU_FINGER_LEFT_LITTLE | IBSU_FINGER_LEFT_RING in IBScanUltimateApi_defs.h
*     imageType           Image type of input image.
*     securityLevel       security level for the duplicate checks.
*     pMatchedPosition    Pointer to variable that will receive result of duplicate.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_IsFingerDuplicated = libIBScanUltimate.IBSU_IsFingerDuplicated
IBSU_IsFingerDuplicated.restype = c_int
IBSU_IsFingerDuplicated.argtypes = (c_int, IBSU_ImageData, c_uint, c_int, c_int, POINTER(c_uint))


'''
****************************************************************************************************
* IBSU_IsValidFingerGeometry()
* 
* DESCRIPTION:
*     Check for hand and finger geometry whether it is correct or not. 
* 
* ARGUMENTS:
*     handle              Handle for device associated with this event (if appropriate).
*     image               input image data for roll to slap comparison.
*     fIndex              Bit-pattern of finger index of input image. 
*                         ex) IBSU_FINGER_LEFT_LITTLE | IBSU_FINGER_LEFT_RING in IBScanUltimateApi_defs.h
*     imageType           Image type of input image.
*     pValid              Pointer to variable that will receive whether it is valid or not.  TRUE to valid; FALSE to invalid.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_IsValidFingerGeometry = libIBScanUltimate.IBSU_IsValidFingerGeometry
IBSU_IsValidFingerGeometry.restype = c_int
IBSU_IsValidFingerGeometry.argtypes = (c_int, IBSU_ImageData, c_uint, c_int, POINTER(c_bool))


'''
****************************************************************************************************
* IBSU_GetRequiredSDKVersion()
* 
* DESCRIPTION:
*     Get minimum SDK version required for running 
* 
* ARGUMENTS:
*     deviceIndex         Device index
*     minSDKVersion       Minimum SDK Version to be returned
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_GetRequiredSDKVersion = libIBScanUltimate.IBSU_GetRequiredSDKVersion
IBSU_GetRequiredSDKVersion.restype = c_int
IBSU_GetRequiredSDKVersion.argtypes = (c_int, POINTER(c_char))

'''
****************************************************************************************************
* IBSU_SetEncryptionKey()
* 
* DESCRIPTION:
*     Set encryption key and mode
* 
* ARGUMENTS:
*     handle              Handle for device associated with this event (if appropriate).
*     pEncyptionKey       input data for encryption key (should be 32 bytes).
*     encMode             input data for encryption mode. (defualt, random, custom)
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_SetEncryptionKey = libIBScanUltimate.IBSU_SetEncryptionKey
IBSU_SetEncryptionKey.restype = c_int
IBSU_SetEncryptionKey.argtypes = (c_int, POINTER(c_char), c_int)

'''
****************************************************************************************************
* IBSU_SetCustomerKey()
* 
* DESCRIPTION:
*     Set CustomoerKey to use locked devices, This is must perfomed on locked devices before IBSU_OpenDevice.
* 
* ARGUMENTS:
*     deviceIndex         Device index
*     nHashType           Type of Hash
*     pCustomerKey        Customer Key to match lock info written in the locked device.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_SetCustomerKey = libIBScanUltimate.IBSU_SetCustomerKey
IBSU_SetCustomerKey.restype = c_int
IBSU_SetCustomerKey.argtypes = (c_int, c_int, c_char_p)

'''
****************************************************************************************************
* IBSU_GetErrorString()
* 
* DESCRIPTION:
*     Returns a string description of the error code.
* 
* ARGUMENTS:
*     errorCode       error code
*     propertyValue   Buffer in which value of error string description will be stored.  This buffer should be 
*                     able to hold IBSU_MAX_STR_LEN characters.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_GetErrorString = libIBScanUltimate.IBSU_GetErrorString
IBSU_GetErrorString.restype = c_int
IBSU_GetErrorString.argtypes = (c_int, POINTER(c_char))

'''
****************************************************************************************************
* IBSU_GetNFIQScoreEx()
* 
* DESCRIPTION:
*     Calculate NFIQ score for image. (Pitch argument added)
*
* ARGUMENTS:
*     handle        Device handle.
*     imgBuffer     Pointer to image buffer.
*     width         Image width (in pixels).
*     height        Image height (in pixels).
*     pitch         Image pitch (in pixels).
*     bitsPerPixel  Bits per pixel.
*     pScore        Pointer to variable that will receive NFIQ score.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_GetNFIQScoreEx = libIBScanUltimate.IBSU_GetNFIQScoreEx
IBSU_GetNFIQScoreEx.restype = c_int
IBSU_GetNFIQScoreEx.argtypes = (c_int, c_void_p, c_uint, c_uint, c_int, c_byte, POINTER(c_int))

'''
****************************************************************************************************
* IBSU_IsSpoofFingerDetected()
* 
* DESCRIPTION:
*     Detect the finger print is Live of Fake
* 
* ARGUMENTS:
*     handle          Handle for device associated with this event (if appropriate).
*     image           input image data.
*     pIsSpoof        Pointer to variable that will receive whether it is Spoof or Live.  TRUE to Spoof; FALSE to Live.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_IsSpoofFingerDetected = libIBScanUltimate.IBSU_IsSpoofFingerDetected
IBSU_IsSpoofFingerDetected.restype = c_int
IBSU_IsSpoofFingerDetected.argtypes = (c_int, IBSU_ImageData, POINTER(c_int))

'''
****************************************************************************************************
* IBSU_ConvertImageToISOANSI()
* 
* DESCRIPTION:
*     Convert Image Data to Standard Format for write file.
*     (ISO 19794-2:2005, ISO 19794-4:2005, ISO 19794-2:2011, ISO 19794-4:2011, ANSI/INCITS 378:2004, ANSI/INCITS 381:2004)
* 
* ARGUMENTS:
*     handle              Handle for device associated with this event (if appropriate).
*     image               input image data for roll to slap comparison.
*     imageCount          Number of image.
*     imageFormat         Image compression format of output data
*     STDformat           ISO format of output data
*     pdata               Pointer to output data
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
IBSU_ConvertImageToISOANSI = libIBScanUltimate.IBSU_ConvertImageToISOANSI
IBSU_ConvertImageToISOANSI.restype = c_int
IBSU_ConvertImageToISOANSI.argtypes = (c_int, POINTER(IBSM_ImageData), c_int, c_int, c_int, POINTER(IBSM_StandardFormatData))

'''
****************************************************************************************************
* RESERVED_GetSpoofScore()
* 
* DESCRIPTION:
*     get a spoof score for the finger.
*
* ARGUMENTS:
*     pReservedKey           Key to unlock reserved functionality.
*     pImage                 Pointer to fingerprint image
*     Width                  Width of pImage
*     Height                 Height of pImage
*     Pitch                  Image line pitch (in bytes).  A positive value indicates top-down line order; a
*                            negative value indicates bottom-up line order.
*     pScore                 Pointer to return spoof score (the score range is from 0 to 1000)
*                            The closer to 1000 score, it means Live finger.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************

RESERVED_GetSpoofScore = libIBScanUltimate.RESERVED_GetSpoofScore
RESERVED_GetSpoofScore.restype = c_int
RESERVED_GetSpoofScore.argtypes = (c_char_p, c_void_p, c_int, c_int, c_int, POINTER(c_int))
'''

'''
****************************************************************************************************
* RESERVED_GetEncryptedImage()
* 
* DESCRIPTION:
*     Get encrypted image from a device, without using capture thread.
*
* ARGUMENTS:
*     handle        Device handle.
*     pReservedKey  Key to unlock reserved functionality.
*     pEncKey       Key to be encrypted.
*     pEncRawImage  Pointer to structure that will receive raw encrypted image data.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
RESERVED_GetEncryptedImage = libIBScanUltimate.RESERVED_GetEncryptedImage
RESERVED_GetEncryptedImage.restype = c_int
RESERVED_GetEncryptedImage.argtypes = (c_int, c_char_p, POINTER(c_char), POINTER(IBSU_ImageData))

'''
****************************************************************************************************
* RESERVED_ConvertToDecryptImage()
* 
* DESCRIPTION:
*     Convert to decrypted image from an encrypted image.
*
* ARGUMENTS:
*     pReservedKey  Key to unlock reserved functionality.
*     pEncKey       Key to be encrypted.
*     pEncRawImage  Pointer to structure that was received raw encrypted image data.
*     pDecRawImage  Decrypted image from an encrypted image.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
'''
RESERVED_ConvertToDecryptImage = libIBScanUltimate.RESERVED_ConvertToDecryptImage
RESERVED_ConvertToDecryptImage.restype = c_int
RESERVED_ConvertToDecryptImage.argtypes = (c_char_p, POINTER(c_char), IBSU_ImageData, POINTER(IBSU_ImageData))
