/*
****************************************************************************************************
* ReservedApi.h
*
* DESCRIPTION:
*     Private API for IBScanUltimate.
*     http://www.integratedbiometrics.com
*
* NOTES:
*     Copyright (c) Integrated Biometrics, 2009-2017
*
* HISTORY:
*     2013/02/03  1.x.x  Created.
*     2013/08/03  1.6.9  Reformatted.
*     2013/10/14  1.7.0  Add a function to read EEPROM.
*     2015/03/26  1.8.4  Added API function to enhance the preview image
*                        (RESERVED_GetEnhancedImage)
*     2016/09/22  1.9.4  Added enumeration value to RESERVED_DeviceInfo
*                        (reserved1)
*     2017/04/27  1.9.7  Added enumeration value to RESERVED_DeviceInfo
*                        (reserved2)
*     2017/08/22  1.9.9  Added API function to get final image by native for Columbo
*                        (RESERVED_GetFinalImageByNative)
*     2020/01/09  3.2.0  Added API function and enumerations to support Spoof
*                         (RESERVED_GetSpoofScore)
*     2020/10/06  3.7.0  Added API function to support locking feature
****************************************************************************************************
*/

#pragma once

#include "IBScanUltimateApi_defs.h"
#include "IBScanUltimateApi_err.h"
#include "IBScanUltimate.h"

#ifdef __cplusplus
extern "C" { 
#endif

/*
****************************************************************************************************
* GLOBAL DEFINES
****************************************************************************************************
*/

/* Minimum LE voltage value. */
#define RESERVED_MIN_LE_VOLTAGE_VALUE   0

/* Maximum LE voltage value. */
#define RESERVED_MAX_LE_VOLTAGE_VALUE  15

/*
****************************************************************************************************
* GLOBAL TYPES
****************************************************************************************************
*/

/*
****************************************************************************************************
* RESERVED_DeviceInfo
*
* DESCRIPTION:
*     Container for device information.
****************************************************************************************************
*/
typedef struct tagRESERVED_DeviceInfo
{
    /* Serial number. */
    char serialNumber[IBSU_MAX_STR_LEN];
    
    /* Product name. */
    char productName[IBSU_MAX_STR_LEN];
    
    /* Interface type (USB). */
    char interfaceType[IBSU_MAX_STR_LEN];
    
    /* Firmare version. */
    char fwVersion[IBSU_MAX_STR_LEN];
    
    /* Revision. */
    char devRevision[IBSU_MAX_STR_LEN];
    
    /* Device handle. */
    int  handle;
    
    /* Indicates whether device is open. */
    BOOL IsHandleOpened;
    
    /* Manufacturer identifier. */
    char vendorID[IBSU_MAX_STR_LEN];
    
    /* Production date. */
    char productionDate[IBSU_MAX_STR_LEN];
    
    /* Last service date. */
    char serviceDate[IBSU_MAX_STR_LEN];

	/* Reserved 1 */
	char reserved1[IBSU_MAX_STR_LEN];

	/* Reserved 2 */
	char reserved2[IBSU_MAX_STR_LEN];
}
RESERVED_DeviceInfo;

/*
****************************************************************************************************
* GLOBAL FUNCTIONS
****************************************************************************************************
*/

/*
****************************************************************************************************
* RESERVED_GetDeviceInfo()
* 
* DESCRIPTION:
*     Retrieve detailed device information about a particular scanner by its logical index.
*
* ARGUMENTS:
*     deviceIndex   Zero-based index of the scanner.
*     pReservedKey  Key to unlock reserved functionality.
*     pDeviceInfo   Pointer to structure that will receive description of device.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
*/
int WINAPI RESERVED_GetDeviceInfo
    (const int            deviceIndex,
     const char          *pReservedKey,
     RESERVED_DeviceInfo *pDeviceInfo);

/*
****************************************************************************************************
* RESERVED_OpenDevice()
* 
* DESCRIPTION:
*     Initialize a device and obtain a handle for subsequent function calls.  Any initialized device
*     must be released with IBSU_CloseDevice() or IBSU_CloseAllDevice() before shutting down the 
*     application.
*
* ARGUMENTS:
*     deviceIndex   Zero-based index of the scanner.
*     pReservedKey  Key to unlock reserved functionality.
*     pHandle       Pointer to variable that will receive device handle for subsequent function calls.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
*/
int WINAPI RESERVED_OpenDevice
    (const int   deviceIndex,
     const char *pReservedKey,
     int        *pHandle);

/*
****************************************************************************************************
* RESERVED_WriteEEPROM()
* 
* DESCRIPTION:
*     Write to Cypress EEPROM.
*
* ARGUMENTS:
*     handle        Device handle.
*     pReservedKey  Key to unlock reserved functionality.
*     addr          Address of EEPROM.
*     pData         Pointer to data buffer.
*     len           Length of data buffer.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
*/
int WINAPI RESERVED_WriteEEPROM
    (const int   handle,
     const char *pReservedKey,
     const WORD  addr,
     const BYTE *pData,
     const int   len);

/*
****************************************************************************************************
* RESERVED_ReadEEPROM()
* 
* DESCRIPTION:
*     Read from Cypress EEPROM.
*
* ARGUMENTS:
*     handle        Device handle.
*     pReservedKey  Key to unlock reserved functionality.
*     addr          Address of EEPROM.
*     pData         Pointer to data buffer.
*     len           Length of data buffer.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
*/
int WINAPI RESERVED_ReadEEPROM
    (const int   handle,
     const char *pReservedkey,
     const WORD  addr,
     BYTE       *pData,
     const int   len);

/*
****************************************************************************************************
* RESERVED_SetProperty()
* 
* DESCRIPTION:
*     Set the value of a property for a device.  For descriptions of properties and values, see 
*     definition of 'IBSU_PropertyId'.  This function can set reserved properties such as serial 
*     number, production date, and service date.
*
* ARGUMENTS:
*     handle         Device handle.
*     pReservedKey   Key to unlock reserved functionality.
*     propertyId     Property for which value will be set.
*     propertyValue  Value of property to set.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
*/
int WINAPI RESERVED_SetProperty
    (const int             handle,
     const char           *pReservedKey,
     const IBSU_PropertyId propertyId,
     LPCSTR                propertyValue);

/*
****************************************************************************************************
* RESERVED_GetLEVoltage()
* 
* DESCRIPTION:
*     Get the LE voltage value for a device.
*
* ARGUMENTS:
*     handle         Device handle.
*     pReservedKey   Key to unlock reserved functionality.
*     pVoltageValue  Pointer to variable that will receive LE voltage value.  Value will be between
*                    RESERVED_MIN_LE_VOLTAGE_VALUE and RESERVED_MAX_LE_VOLTAGE_VALUE, inclusive.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
*/
int WINAPI RESERVED_GetLEVoltage
    (const int   handle,
     const char *pReservedKey,
     int        *pVoltageValue);

/*
****************************************************************************************************
* RESERVED_SetLEVoltage()
* 
* DESCRIPTION:
*     Set the LE voltage value for a device.
*
* ARGUMENTS:
*     handle        Device handle.
*     pReservedKey  Key to unlock reserved functionality.
*     voltageValue  LE voltage value.  Value must be between RESERVED_MIN_LE_VOLTAGE_VALUE and 
*                   RESERVED_MAX_LE_VOLTAGE_VALUE, inclusive.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
*/
int WINAPI RESERVED_SetLEVoltage
    (const int   handle,
     const char *pReservedKey,
     const int   voltageValue);

/*
****************************************************************************************************
* IBSU_BeginCaptureImage()
* 
* DESCRIPTION:
*     Begin acquiring an image from a device, without using capture thread.
*
* ARGUMENTS:
*     handle           Device handle.
*     pReservedKey     Key to unlock reserved functionality.
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
****************************************************************************************************
*/
int WINAPI RESERVED_BeginCaptureImage
    (const int                  handle,
     const char                *pReservedKey,
     const IBSU_ImageType       imageType,
     const IBSU_ImageResolution imageResolution,
     const DWORD                captureOptions);

/*
****************************************************************************************************
* RESERVED_GetOneFrameImage()
* 
* DESCRIPTION:
*     Get image from a device, without using capture thread.
*
* ARGUMENTS:
*     handle        Device handle.
*     pReservedKey  Key to unlock reserved functionality.
*     pRawImage     Pointer to buffer that will receive raw image data.
*     imageLength   Length of image buffer.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
*/
int WINAPI RESERVED_GetOneFrameImage
    (const int      handle,
     const char    *pReservedKey,
     unsigned char *pRawImage,
     const int      imageLength);

/*
****************************************************************************************************
* RESERVED_GetFpgaRegister()
* 
* DESCRIPTION:
*     Get the value of an FPGA register for a device.
*
* ARGUMENTS:
*     handle        Device handle.
*     pReservedKey  Key to unlock reserved functionality.
*     address       Address of FPGA register.
*     pValue        Pointer to variable that will receive FPGA register value.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
*/
int WINAPI RESERVED_GetFpgaRegister
    (const int           handle,
     const char         *pReservedKey,
     const unsigned char address,
     unsigned char      *pValue);

/*
****************************************************************************************************
* RESERVED_SetFpgaRegister()
* 
* DESCRIPTION:
*     Set the value of an FPGA register for a device.
*
* ARGUMENTS:
*     handle        Device handle.
*     pReservedKey  Key to unlock reserved functionality.
*     address       Address FPGA register.
*     value         FPGA register value.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
*/
int WINAPI RESERVED_SetFpgaRegister
    (const int           handle,
     const char         *pReservedKey,
     const unsigned char address,
     const unsigned char value);

/*
****************************************************************************************************
* RESERVED_CreateClientWindow()
* 
* DESCRIPTION:
*     Create client window associated with device.  (Available only on Windows.)
*
* ARGUMENTS:
*     handle        Device handle.
*     pReservedKey  Key to unlock reserved functionality.
*     hWindow       Windows handle to draw.
*     left          Coordinate of left edge of rectangle.
*     top           Coordinate of top edge of rectangle.
*     right         Coordinate of right edge of rectangle.
*     bottom        Coordinate of bottom edge of rectangle.
*     rawImgWidth   Width of raw image.
*     rawImgHeight  Height of raw image.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
*/
int WINAPI RESERVED_CreateClientWindow
    (const int       handle,
     const char     *pReservedKey,
     const IBSU_HWND hWindow,
     const DWORD     left,
     const DWORD     top,
     const DWORD     right,
     const DWORD     bottom,
     const DWORD     rawImgWidth,
     const DWORD     rawImgHeight);

/*
****************************************************************************************************
* RESERVED_DrawClientWindow()
* 
* DESCRIPTION:
*     Draw image on client window associated with device.  (Available only on Windows.)
*
* ARGUMENTS:
*     handle        Device handle.
*     pReservedKey  Key to unlock reserved functionality.
*     drawImage     Pointer to buffer containing image to draw.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
*/
int WINAPI RESERVED_DrawClientWindow
    (const int      handle,
     const char    *pReservedKey,
     unsigned char *drawImage);

/*
****************************************************************************************************
* RESERVED_UsbBulkOutIn()
* 
* DESCRIPTION:
*     Perform raw USB bulk transaction to device.
*
* ARGUMENTS:
*     handle        Device handle.
*     pReservedKey  Key to unlock reserved functionality.
*     outEp         OUT endpoint to send data to.
*     uiCommand     Command to send.
*     outData       Pointer to buffer with data to send.  To send no data, pass NULL.
*     outDataLen    Length of data to send.
*     inEp          IN endpoint to receive data from.
*     inData        Pointer to buffer which will receive data.  To receive no data, pass NULL.
*     inDataLen     Length of data to receive.
*     nBytesRead    Pointer to variable that will receive number of bytes received.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
*/
int WINAPI RESERVED_UsbBulkOutIn
    (const int           handle,
     const char         *pReservedKey,
     const int           outEp,
     const unsigned char uiCommand,
     unsigned char      *outData,
     const int           outDataLen,
     const int           inEp,
     unsigned char      *inData,
     const int           inDataLen,
     int                *nBytesRead);

/*
****************************************************************************************************
* RESERVED_InitializeCamera()
* 
* DESCRIPTION:
*     Initialize camera on device.
*
* ARGUMENTS:
*     handle        Device handle.
*     pReservedKey  Key to unlock reserved functionality.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
*/
int WINAPI RESERVED_InitializeCamera
    (const int   handle,
     const char *pReservedKey);

/*
****************************************************************************************************
* RESERVED_GetEnhancedImage()
* 
* DESCRIPTION:
*     Enhanced image from the input preview image.
*
* ARGUMENTS:
*     handle                 Device handle.
*     pReservedKey           Key to unlock reserved functionality.
*     inImage                Input image data which is returned from preview callback.
*     enhandedImage          Pointer to structure that will receive data of enhanced preview image.
*                            The buffer in this structure points to an internal image buffer; the
*                            data should be copied to an application buffer if desired for future processing.
*     segmentImageArrayCount Pointer to variable that will receive number of finger images split from input image.
*     segmentImageArray     The buffer in this structure points to an internal image buffer; the
*                            data should be copied to an application buffer if desired for future processing.
*     segmentPositionArray  Array of structures with position data for individual fingers split from input image.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
*/
int WINAPI RESERVED_GetEnhancedImage
    (const int              handle,
     const char            *pReservedKey,
     const IBSU_ImageData   inImage,
     IBSU_ImageData        *enhancedImage,
     int                   *segmentImageArrayCount,
     IBSU_ImageData        *segmentImageArray,
     IBSU_SegmentPosition  *segmentPositionArray);


/*
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
*/
int WINAPI RESERVED_GetFinalImageByNative
    (const int              handle,
     const char            *pReservedKey,
     IBSU_ImageData        *finalImage);


/*
****************************************************************************************************
* RESERVED_GetSpoofScore()
* 
* DESCRIPTION:
*     get a spoof score for the finger.
*
* ARGUMENTS:
*     pReservedKey           Key to unlock reserved functionality.
*     deviceID               Device ID captured the image.
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
*/
int WINAPI RESERVED_GetSpoofScore
    (const char            *pReservedKey,
     const BYTE            *pImage,
     const int             Width,
	 const int             Height,
	 const int             Pitch,
	 int                   *pScore);

/*
****************************************************************************************************
* RESERVED_GetEncyptedImage()
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
*/
int WINAPI RESERVED_GetEncryptedImage
    (const int          handle,
     const char         *pReservedKey,
     unsigned char      *pEncKey,
     IBSU_ImageData     *pRawEncImage);

/*
****************************************************************************************************
* RESERVED_ConvetToDecryptImage()
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
*/
int WINAPI RESERVED_ConvertToDecryptImage
    (const char         *pReservedKey,
     unsigned char      *pEncKey,
     IBSU_ImageData     rawEncImage,
     IBSU_ImageData     *pRawDecImage);
/*
****************************************************************************************************
* RESERVED_GetHashCode()
* 
* DESCRIPTION:
*     Get Hash Code From the PlainText
* 
* ARGUMENTS:
*     pReservedKey        Key to unlock reserved functionality.
*     nHashType           Type of Hash
*     pPlainText          PlainText to get hash code
*     nPlainTextSize      size of the PlainText
*     pHashCode           Hash code result
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
*/
int WINAPI RESERVED_GetHashCode
    (const char         *pReservedKey,
     const int          nHashType,
     const char         *pPlainText,
     const int          nPlainTextSize,
     char               *pHashCode);

/*
****************************************************************************************************
* RESERVED_Set_DeviceLockInfo()
* 
* DESCRIPTION:
*     It writes lock information to a device. After this, use IBSU_Set_DeviceLock to lock the device.
* 
* ARGUMENTS:
*     handle              Handle for device associated with this event (if appropriate).
*     pReservedKey        Key to unlock reserved functionality.
*     nHashType           Type of Hash
*     pCustomerKey        Customer Key to match lock info written in the locked device.
*     pHashCode           Hash Code
*     pCustomerString     Customer String to return when Customer Key is matched after opendevice
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
*/
int WINAPI RESERVED_Set_DeviceLockInfo
    (const int              handle,
     const char             *pReservedKey,
     const int              nHashType,
     const char             *pCustomerKey,
     const unsigned char    *pHashCode,
     const char             *pCustomerString);

/*
****************************************************************************************************
* RESERVED_Erase_DeviceLockInfo()
* 
* DESCRIPTION:
*     It erases lock information of device.
* 
* ARGUMENTS:
*     handle              Handle for device associated with this event (if appropriate).
*     pReservedKey        Key to unlock reserved functionality.
*     nHashType           Type of Hash
*     pCustomerKey        Customer Key to match lock info written in the locked device.
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
*/
int WINAPI RESERVED_Erase_DeviceLockInfo
    (const int             handle,
     const char            *pReservedKey,
     const int             nHashType,
     const char*           pCustomerKey);



/*
****************************************************************************************************
* RESERVED_Set_DeviceLock()
* 
* DESCRIPTION:
*     It locks or unlocks a device.
* 
* ARGUMENTS:
*     handle              Handle for device associated with this event (if appropriate).
*     pReservedKey        Key to unlock reserved functionality.
*     nHashType           Type of Hash
*     pCustomerKey        Customer Key to match lock info written in the locked device.
*     bLock               Lock(TRUE) or Unlock(FALSE) 
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
*/
int WINAPI RESERVED_Set_DeviceLock
    (const int            handle,
     const char           *pReservedKey,
     const int            nHashType,
     const char*          pCustomerKey,
     const BOOL           bLock);



/*
****************************************************************************************************
* RESERVED_SetAdminMode()
* 
* DESCRIPTION:
*     It sets Administrator mode for Locking Kojak.
* 
* ARGUMENTS:
*     pReservedKey        Key to unlock reserved functionality.
*     bEnable             Enable(TRUE) or Disable(FALSE) 
*
* RETURNS:
*     IBSU_STATUS_OK, if successful.
*     Error code < 0, otherwise.  See error codes in 'IBScanUltimateApi_err'.
****************************************************************************************************
*/
int WINAPI RESERVED_SetAdminMode
    (const char           *pReservedKey,
     const BOOL           bEnable);


int WINAPI RESERVED_GetSpoofScoreEx
    (const char            *pReservedKey,
     const BYTE            *pImage,
     const int             Width,
	 const int             Height,
	 const int             Pitch,
     const int             bgWidth, 
     const int             bgHeight,
	 int                   *pScore);
#ifdef __cplusplus
} // extern "C"
#endif
