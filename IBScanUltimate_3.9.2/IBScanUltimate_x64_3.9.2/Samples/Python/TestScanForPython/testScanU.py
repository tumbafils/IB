import sys
import time
import os.path
from os import path
from ctypes import *
from include.IBScanUltimateApi import *

'''
/*******************************************************************************
 * LOCAL VARIABLES
 ******************************************************************************/
'''
#/* Start time of capture to calculate the frame rate. */
m_startTime = time.time()

#/* Counter for number of preview images to calculate the frame rate. */
m_previewCount = 0

#/* The handle of the currently-opened device. */
m_deviceHandle = c_int(-1)

#/* Dummy variable for registering callbacks. */
m_context = c_uint(0)

#/* The last finger count state, to detect changes. */
m_SavedFingerCountState = c_int(-1)

#/* Options 0=save Bitmap and WSQ, 1=calculate NFIQ score , 2=Preview, 3=Spoof ON,OFF , 4=Spoof Threshold(0~10) */
m_options = [0,0,1,0,3]

m_devDesc = IBSU_DeviceDesc()

'''
/*******************************************************************************
 * GetConfiguration()
 *
 * DESCRIPTION:
 *     Get the number of attached scanners.
 ******************************************************************************/
'''
def GetConfiguration():
    devCount = c_int(0)

    nRc = IBSU_GetDeviceCount(byref(devCount))
    if (nRc < IBSU_STATUS_OK):
        print("Error %d Retrieving device count" % nRc)
        return 0
    
    print("Found %d devices attached" % devCount.value)
    return devCount


'''
/*******************************************************************************
 * OnPreviewImageAvailable()
 * 
 * DESCRIPTION:
 *     The callback that is invoked when a preview image is available.
 ******************************************************************************/
 '''
def OnPreviewImageAvailable(deviceHandle, pContext, image):
    global m_previewCount

    sys.stdout.write("C")
    sys.stdout.flush()
    m_previewCount += 1

_c_callbackPreviewImage = IBSU_CallbackPreviewImage(OnPreviewImageAvailable)


'''
/*******************************************************************************
 * OnFingerCountChange()
 *
 * DESCRIPTION:
 *     The callback that is invoked when the number of fingers on the platen 
 *     changes.
 ******************************************************************************/
'''
def OnFingerCountChange(deviceHandle, pContext, fingerCountState):
    global m_SavedFingerCountState

    if (m_SavedFingerCountState != fingerCountState):
        if (fingerCountState == IBSU_FingerCountState.ENUM_IBSU_FINGER_COUNT_OK.value):
            pcState = "FINGER_COUNT_OK"
        elif (fingerCountState == IBSU_FingerCountState.ENUM_IBSU_TOO_MANY_FINGERS.value):
            pcState = "TOO_MANY_FINGERS"
        elif (fingerCountState == IBSU_FingerCountState.ENUM_IBSU_TOO_FEW_FINGERS.value):
            pcState = "TOO_FEW_FINGERS"
        elif (fingerCountState == IBSU_FingerCountState.ENUM_IBSU_NON_FINGER.value):
            pcState = "NON-FINGER"
        else:
            pcState = "UNKNOWN"

        print("\n-- Finger count changed -- Device= %d, State= %s" % (deviceHandle, pcState))
        sys.stdout.flush()

        m_SavedFingerCountState = fingerCountState

_c_callbackFingerCount = IBSU_CallbackFingerCount(OnFingerCountChange)


'''
/*******************************************************************************
 * OnFingerQualityChange()
 *
 * DESCRIPTION:
 *     The callback that is invoked when the quality of fingers on the platen 
 *     changes.
 ******************************************************************************/
'''
def OnFingerQualityChange(deviceHandle, pContext, pQualityArray, qualityArrayCount):
    sys.stdout.write("\n-- Finger quality changed -- Device= %d, Qualities= " % deviceHandle)
    for i in range(0,4):
        if (pQualityArray[i] == IBSU_FingerQualityState.ENUM_IBSU_FINGER_NOT_PRESENT.value):
            pcQuality = "NOT_PRESENT"
        elif (pQualityArray[i] == IBSU_FingerQualityState.ENUM_IBSU_QUALITY_GOOD.value):
            pcQuality = "GOOD"
        elif (pQualityArray[i] == IBSU_FingerQualityState.ENUM_IBSU_QUALITY_FAIR.value):
            pcQuality = "FAIR"
        elif (pQualityArray[i] == IBSU_FingerQualityState.ENUM_IBSU_QUALITY_POOR.value):
            pcQuality = "POOR"
        elif (pQualityArray[i] == IBSU_FingerQualityState.ENUM_IBSU_QUALITY_INVALID_AREA_TOP.value):
            pcQuality = "INVALID_AREA_TOP"
        elif (pQualityArray[i] == IBSU_FingerQualityState.ENUM_IBSU_QUALITY_INVALID_AREA_LEFT.value):
            pcQuality = "INVALID_AREA_LEFT"
        elif (pQualityArray[i] == IBSU_FingerQualityState.ENUM_IBSU_QUALITY_INVALID_AREA_RIGHT.value):
            pcQuality = "INVALID_AREA_RIGHT"
        else:
            pcQuality = "UNKNOWN"

        if (i != 0):
            sys.stdout.write(", ")
        sys.stdout.write(pcQuality)
    sys.stdout.write("\n")

_c_callbackFingerQuality = IBSU_CallbackFingerQuality(OnFingerQualityChange)


'''
/*******************************************************************************
 * OnDeviceCountChange()
 *
 * DESCRIPTION:
 *     The callback that is invoked when the number of attached scanners 
 *     changes.
 ******************************************************************************/
'''
def OnDeviceCountChange(detectedDevices, context):
    print ("\nDeviceCountChange: now %d devices" % detectedDevices)
    sys.stdout.flush()

_c_callbackDeviceCount = IBSU_CallbackDeviceCount(OnDeviceCountChange)


'''
/*******************************************************************************
 * OnInitProgressChange()
 *
 * DESCRIPTION:
 *     The callback that is invoked when the initialization progresses of a 
 *     scanner being opened.
 ******************************************************************************/
'''
def OnInitProgressChange(deviceIndex, context, progressValue):
    print ("\nInitializing device... %d%%" % progressValue)
    sys.stdout.flush()

_c_callbackInitProgress = IBSU_CallbackInitProgress(OnInitProgressChange)


'''
/*******************************************************************************
 * OnDeviceCommunicationBreak()
 *
 * DESCRIPTION:
 *     The callback that is invoked when the communication with a scanner is
 *     broken.
 ******************************************************************************/
'''
def OnDeviceCommunicationBreak(deviceHandle, context):
    global m_deviceHandle

    print("\nDevice Communications break")
    nRc = IBSU_CloseDevice(deviceHandle)
    if (nRc < IBSU_STATUS_OK):
        print("Error %d closing device" % nRc)
        if (deviceHandle == m_deviceHandle):
            m_deviceHandle = -1
            sys.stdout.flush()

_c_callbackCommunicationBreak = IBSU_Callback(OnDeviceCommunicationBreak)


'''
/*******************************************************************************
 * OnTakingAcquisition()
 *
 * DESCRIPTION:
 *     The callback that is invoked when rolling acquisition begins.
 ******************************************************************************/
'''
def OnTakingAcquisition(deviceHandle, context, imageType):
    if (imageType == IBSU_ImageType.ENUM_IBSU_ROLL_SINGLE_FINGER.value):
        print("\nWhen done remove finger from sensor!")
        sys.stdout.flush()

_c_callbackTakingAcquisition = IBSU_CallbackTakingAcquisition(OnTakingAcquisition)


'''
/*******************************************************************************
 * OnCompleteAcquisition()
 *
 * DESCRIPTION:
 *     The callback that is invoked when rolling acquisition completes.
 ******************************************************************************/
'''
def OnCompleteAcquisition(deviceHandle, context, imageType):
    print("\nCompleteAcquisition")
    sys.stdout.flush()

_c_callbackCompleteAcquisition = IBSU_CallbackCompleteAcquisition(OnCompleteAcquisition)


'''
/*******************************************************************************
 * OnPressedKeyButtons()
 *
 * DESCRIPTION:
 *     The callback that is invoked when rolling acquisition completes.
 ******************************************************************************/
'''
def OnPressedKeyButtons(deviceHandle, context, pressedKeyButtons):
    print("\nPressedKeyButtons = %d" % pressedKeyButtons)
    sys.stdout.flush()

_c_callbackPressedKeyButtons = IBSU_CallbackKeyButtons(OnPressedKeyButtons)


'''
/*******************************************************************************
 * OnResultImageAvailableEx()
 *
 * DESCRIPTION:
 *     The callback that is invoked when the extended result image is available.
 ******************************************************************************/
'''
def OnResultImageAvailableEx(deviceHandle, context, imageStatus, image,
                             imageType, detectedFingercount, segmentImageArrayCount,
                             pSegmentImageArray, pSegmentPositionArray):
    nfiqScore = c_int()
    isSpoof = c_int()

    #/* Calculate preview frames captured per second during scan. */
    framesPerSecond = FramesPerSecond()
    print("\nStopped. %1.1f frames per second" % framesPerSecond)

    #/* Inform user that acquisition is complete. */
    pszImgTypeName = "Unknown"
    if (imageStatus == IBSU_STATUS_OK):
        if (imageType == IBSU_ImageType.ENUM_IBSU_ROLL_SINGLE_FINGER.value):
            pszImgTypeName = "Rolling single finger"
        elif (imageType == IBSU_ImageType.ENUM_IBSU_FLAT_SINGLE_FINGER.value):
            pszImgTypeName = "Flat single finger"
        elif (imageType == IBSU_ImageType.ENUM_IBSU_FLAT_TWO_FINGERS.value):
            pszImgTypeName = "Flat two fingers"
        elif (imageType == IBSU_ImageType.ENUM_IBSU_FLAT_FOUR_FINGERS.value):
            pszImgTypeName = "Flat four fingers"
        elif (imageType == IBSU_ImageType.ENUM_IBSU_FLAT_THREE_FINGERS.value):
            pszImgTypeName = "Flat three fingers"
        else:
            pszImgTypeName = "Unknown"

        print("\n%s Image acquisition complete" % pszImgTypeName)
    else:
        print("\nImage acquisition completed with status %d" % imageStatus)

    if (m_options[0] == 1):
        #/* Save result image. */
        print("\nSaving bitmap,WSQ, PNG and JPEG-2000 images...")
        sys.stdout.flush()
        saveFileName = "ResultImage_%s.bmp" % pszImgTypeName
        nRc = IBSU_SaveBitmapImage(create_string_buffer(saveFileName.encode("utf-8")), image.Buffer, image.Width,
                                   image.Height, image.Pitch, image.ResolutionX, image.ResolutionY)
        if (nRc != IBSU_STATUS_OK):
            print("Failed to save bitmap image!")
            return

        print("-- Saved %s" % saveFileName)
        sys.stdout.flush()

        saveFileName = "ResultImage_%s.wsq" % pszImgTypeName
        comment = ""
        nRc = IBSU_WSQEncodeToFile(create_string_buffer(saveFileName.encode("utf-8")), image.Buffer, image.Width,
                                   image.Height, image.Pitch, image.BitsPerPixel, c_int(500),
                                   c_double(0.75), create_string_buffer(comment.encode("utf-8")))
        if (nRc != IBSU_STATUS_OK):
            print("Failed to save WSQ image!")
            return

        print("-- Saved %s" % saveFileName)
        sys.stdout.flush()

        saveFileName = "ResultImage_%s.png" % pszImgTypeName
        nRc = IBSU_SavePngImage(create_string_buffer(saveFileName.encode("utf-8")), image.Buffer, image.Width,
                                image.Height, image.Pitch, image.ResolutionX, image.ResolutionY)
        if (nRc != IBSU_STATUS_OK):
            print("Failed to save PNG image!")
            return

        print("-- Saved %s" % saveFileName)
        sys.stdout.flush()

        saveFileName = "ResultImage_%s.jp2" % pszImgTypeName
        nRc = IBSU_SaveJP2Image(create_string_buffer(saveFileName.encode("utf-8")), image.Buffer, image.Width,
                                image.Height, image.Pitch, image.ResolutionX, image.ResolutionY, c_int(80))
        if (nRc != IBSU_STATUS_OK):
            print("Failed to save JPEG-2000 image!")
            return

        print("-- Saved %s" % saveFileName)
        sys.stdout.flush()

        #/* Save each image segment for multi-finger scan. */
        if (segmentImageArrayCount > 1):
            for i in range(0, segmentImageArrayCount):
                saveFileName = "ResultImage__Segment_%02d.bmp" % i
                nRc = IBSU_SaveBitmapImage(create_string_buffer(saveFileName.encode("utf-8")), pSegmentImageArray[i].Buffer,
                                           pSegmentImageArray[i].Width, pSegmentImageArray[i].Height,
                                           pSegmentImageArray[i].Pitch,
                                           pSegmentImageArray[i].ResolutionX, pSegmentImageArray[i].ResolutionY)

                if (nRc != IBSU_STATUS_OK):
                    print("Failed to save segment image!")
                    return

                print("-- Saved %s" % saveFileName)
                sys.stdout.flush()

                saveFileName = "ResultImage__Segment_%02d.wsq" % i
                nRc = IBSU_WSQEncodeToFile(create_string_buffer(saveFileName.encode("utf-8")), pSegmentImageArray[i].Buffer,
                                           pSegmentImageArray[i].Width, pSegmentImageArray[i].Height,
                                           pSegmentImageArray[i].Pitch,
                                           pSegmentImageArray[i].BitsPerPixel, c_int(500),
                                           c_double(0.75), create_string_buffer(comment.encode("utf-8")))
                if (nRc != IBSU_STATUS_OK):
                    print("Failed to save segment WSQ image!")
                    return

                print("-- Saved %s" % saveFileName)
                sys.stdout.flush()

    if (m_options[3] == 1): # If PAD enabled
        print("\nCheck Spoof fingers...")
        sys.stdout.flush()
        # PAD check for multiple finger(Segment based)
        isSpoofTotal = ["","","",""]
        for i in range(0, segmentImageArrayCount):
            nRc = IBSU_IsSpoofFingerDetected(deviceHandle,pSegmentImageArray[i], byref(isSpoof))
            if (nRc != IBSU_STATUS_OK):
                errorString = create_string_buffer(IBSU_MAX_STR_LEN)
                IBSU_GetErrorString(nRc, errorString)
                errorStringConv = bytes(errorString.value).decode('ascii')
                print(errorStringConv)
            else: # if nRc == 0,
                if (isSpoof.value == 1):
                    isSpoofStr = "FAKE"
                else:
                    isSpoofStr = "LIVE"
                isSpoofTotal[i] = isSpoofStr

        if (segmentImageArrayCount == 1):
            print('{0}'.format(isSpoofTotal[0]))
        elif (segmentImageArrayCount == 2):
            print('{0}-{1}'.format(isSpoofTotal[0], isSpoofTotal[1]))
        elif (segmentImageArrayCount == 4):
            print('{0}-{1}-{2}-{3}'.format(isSpoofTotal[0], isSpoofTotal[1], isSpoofTotal[2], isSpoofTotal[3]))

    if (m_options[1] == 1):
        print("\nCalculating NFIQ score...")
        sys.stdout.flush()
        #/* Calculate NFIQ score for result image. */
        nRc = IBSU_GetNFIQScore(deviceHandle, image.Buffer, image.Width,
                                image.Height, image.BitsPerPixel, byref(nfiqScore))
        if (nRc == IBSU_STATUS_OK):
            print("-- NFIQ score is %d" % nfiqScore.value)
        else:
            print("Failed to get NFIQ score")

    print("\n\nPress enter!")
    sys.stdout.flush()

_c_callbackResultImageEx = IBSU_CallbackResultImageEx(OnResultImageAvailableEx)


'''
/*******************************************************************************
 * OpenCaptureDevice()
 *
 * DESCRIPTION:
 *     Open a capture device and register callbacks.
 ******************************************************************************/
'''
def OpenCaptureDevice():
    #/* Open the device. */
    global m_deviceHandle
    uniformityMaskPath = "./"

    nRc = IBSU_OpenDeviceEx(0, c_char_p(uniformityMaskPath.encode('utf-8')), False, byref(m_deviceHandle))
    if (nRc < IBSU_STATUS_OK):
        if (nRc == IBSU_ERR_DEVICE_ACTIVE):
            strMessage = "[Error code = %d] Device initialization failed because in use by another thread/process." % nRc
        elif (nRc == IBSU_ERR_USB20_REQUIRED):
            strMessage = "[Error code = %d] Device initialization failed because SDK only works with USB 2.0." % nRc
        elif (nRc == IBSU_ERR_DEVICE_HIGHER_SDK_REQUIRED):
            minSDKVersion = create_string_buffer(IBSU_MAX_STR_LEN)
            IBSU_GetRequiredSDKVersion(0, minSDKVersion)
            strMessage = "[Error code = %d] Devcie initialization failed because SDK Version %s is required at least." % (nRc, bytes(minSDKVersion.value).decode("ascii"))
        else:
            strMessage = "[Error code = %d] Device initialization failed" % nRc
    
        print(strMessage)
        m_deviceHandle = -1
        return False

    #/* Register callbacks for device events. */
    nRc = IBSU_RegisterCallbacks(m_deviceHandle, IBSU_Events.ENUM_IBSU_ESSENTIAL_EVENT_PREVIEW_IMAGE.value,
                                 _c_callbackPreviewImage, _c_callbackPreviewImage)
    if (nRc < IBSU_STATUS_OK):
        print("Problem registering preview image callback: %d" % nRc)
        return False

    nRc = IBSU_RegisterCallbacks(m_deviceHandle, IBSU_Events.ENUM_IBSU_OPTIONAL_EVENT_FINGER_COUNT.value,
                                 _c_callbackFingerCount, _c_callbackFingerCount)
    if (nRc < IBSU_STATUS_OK) :
        print("Problem registering finger count callback: %d" % nRc)
        return False

    nRc = IBSU_RegisterCallbacks(m_deviceHandle, IBSU_Events.ENUM_IBSU_OPTIONAL_EVENT_FINGER_QUALITY.value,
                                _c_callbackFingerQuality, _c_callbackFingerQuality)
    if (nRc < IBSU_STATUS_OK):
       print("Problem registering finger quality callback: %d" % nRc)
       return False

    nRc = IBSU_RegisterCallbacks(m_deviceHandle, IBSU_Events.ENUM_IBSU_ESSENTIAL_EVENT_COMMUNICATION_BREAK.value,
                                 _c_callbackCommunicationBreak, _c_callbackCommunicationBreak)
    if (nRc < IBSU_STATUS_OK):
        print("Problem registering communication break callback: %d" % nRc)
        return False

    nRc = IBSU_RegisterCallbacks(m_deviceHandle, IBSU_Events.ENUM_IBSU_ESSENTIAL_EVENT_TAKING_ACQUISITION.value,
                                 _c_callbackTakingAcquisition, _c_callbackTakingAcquisition)
    if (nRc < IBSU_STATUS_OK):
        print("Problem registering taking acquisition callback: %d" % nRc)
        return False

    nRc = IBSU_RegisterCallbacks(m_deviceHandle, IBSU_Events.ENUM_IBSU_ESSENTIAL_EVENT_COMPLETE_ACQUISITION.value,
                                 _c_callbackCompleteAcquisition, _c_callbackCompleteAcquisition)
    if (nRc < IBSU_STATUS_OK):
        print("Problem registering complete acquisition callback: %d" % nRc)
        return False

    nRc = IBSU_RegisterCallbacks(m_deviceHandle, IBSU_Events.ENUM_IBSU_ESSENTIAL_EVENT_RESULT_IMAGE_EX.value,
                                 _c_callbackResultImageEx, _c_callbackResultImageEx)
    if (nRc < IBSU_STATUS_OK):
        print("Problem registering extended result image callback: %d" % nRc)
        return False

    nRc = IBSU_RegisterCallbacks(m_deviceHandle, IBSU_Events.ENUM_IBSU_ESSENTIAL_EVENT_KEYBUTTON.value,
                                 _c_callbackPressedKeyButtons, _c_callbackPressedKeyButtons)
    if (nRc < IBSU_STATUS_OK):
        print("Problem registering key button callback: %d" % nRc)
        return False


'''
/*******************************************************************************
 * FramesPerSecond()
 *
 * DESCRIPTION:
 *     Calculate the number of preview frames captured per second.
 ******************************************************************************/
''' 
def FramesPerSecond():
    global m_startTime
    global m_previewCount

    elapsed = time.time() - m_startTime
    return (m_previewCount / elapsed)


'''
/*******************************************************************************
 * StartCapture()
 *
 * DESCRIPTION:
 *     Start capture for the specified image type. 
 ******************************************************************************/
 '''
def StartCapture(imageType):
    global m_deviceHandle
    global m_previewCount
    global m_startTime
    global m_devDesc
    isAvailable = c_bool()

    if (m_devDesc.IsDeviceLocked):
        strKey = input(" Please enter Customer Key >> ")
        nRc = IBSU_SetCustomerKey(0, IBSU_HashType.ENUM_IBSU_HASH_TYPE_SHA256.value, create_string_buffer(strKey.encode("utf-8")))
        if (nRc != IBSU_STATUS_OK):
            print("Customer Key failed : %d" % nRc)
            return False

    if (OpenCaptureDevice() == False):
        print("Problem OpenCaptureDevice")
        return False

    #/* Determine whether capture mode is available for scanner. */
    IBSU_IsCaptureAvailable(m_deviceHandle, imageType,
                            IBSU_ImageResolution.ENUM_IBSU_IMAGE_RESOLUTION_500.value, byref(isAvailable))
    if (isAvailable == False):
        if (imageType == IBSU_ImageType.ENUM_IBSU_FLAT_SINGLE_FINGER.value):
            print("Capture mode FLAT_SINGLE_FINGER not available")
        elif (imageType == IBSU_ImageType.ENUM_IBSU_FLAT_TWO_FINGERS.value):
            print("Capture mode FLAT_TWO_FINGERS not available")
        elif (imageType == IBSU_ImageType.ENUM_IBSU_ROLL_SINGLE_FINGER.value):
            print("Capture mode ROLL_SINGLE_FINGER not available")
        else:
            print("Invalid capture mode")

        return False

    #/* Format capture options. */
    captureOptions  = 0
    captureOptions |= IBSU_OPTION_AUTO_CONTRAST
    captureOptions |= IBSU_OPTION_AUTO_CAPTURE
    
    #/* Set Spoof property. */
    if (m_options[3] == 1): # Spoof Enable
        nPropRc = 0
        propertyValue = "TRUE"
        nPropRc = IBSU_SetProperty(m_deviceHandle, IBSU_PropertyId.ENUM_IBSU_PROPERTY_ENABLE_SPOOF.value, create_string_buffer(propertyValue.encode("utf-8")))
		# Disable segment rotation for the better PAD perfomance
		nPropRc = IBSU_SetProperty(self.m_nDevHandle, IBSU_PropertyId.ENUM_IBSU_PROPERTY_DISABLE_SEGMENT_ROTATION.value, create_string_buffer(propertyValue.encode("utf-8")))
        if (nPropRc == IBSU_STATUS_OK):
            propertyValue = str(m_options[4]) # Spoof Level
            IBSU_SetProperty(m_deviceHandle, IBSU_PropertyId.ENUM_IBSU_PROPERTY_SPOOF_LEVEL.value, create_string_buffer(propertyValue.encode("utf-8")))
        else:
            get_propertyValue = create_string_buffer(IBSU_MAX_STR_LEN)
            IBSU_GetErrorString(nPropRc, get_propertyValue)
            get_propertyValueStr = bytes(get_propertyValue.value).decode('ascii')
            print(get_propertyValueStr)
    else:
        propertyValue = "FALSE"
        IBSU_SetProperty(m_deviceHandle, IBSU_PropertyId.ENUM_IBSU_PROPERTY_ENABLE_SPOOF.value, create_string_buffer(propertyValue.encode("utf-8")))

    #/* Begin image capture. */
    nRc = IBSU_BeginCaptureImage(m_deviceHandle, imageType,
                                 IBSU_ImageResolution.ENUM_IBSU_IMAGE_RESOLUTION_500.value, captureOptions)
    if (nRc < IBSU_STATUS_OK):
        print("Problem starting capture: %d" % nRc)
        return False

    print("Setting up for scan with callback...Displayed 'C'=Image callback.")

    #/* Iniitialize variables for calculating framerate. */
    m_previewCount = 0
    m_startTime = time.time()

    return True


'''
/*******************************************************************************
 * Main_menu()
 *
 * DESCRIPTION:
 *     Display the menu, accept a character, and perform the associated action.
 ******************************************************************************/
'''
def DisplayManu():
    global m_deviceHandle
    global m_options

    # os.system("clear")
    print("\nReady.   Enter choice:\n"
           "\t1. Start capture for flat single finger.\n"
           "\t2. Start capture for flat two fingers.\n"
           "\t3. Start capture for rolling single finger.\n"
           "\t4. Start capture for flat four fingers.\n"
           "\t5. Abort Capture\n"
           "\t6. Options\n"
           "\t7. Set Preview Image\n"
           "\t8. Set Spoof Function Control\n"
           "\t9. End program")

    ch = input(" >> ")
    if (ch == '1'):
        ok = StartCapture(IBSU_ImageType.ENUM_IBSU_FLAT_SINGLE_FINGER.value)
        if (ok == False):
            return -1

        return 0
    elif (ch == '2'):
        ok = StartCapture(IBSU_ImageType.ENUM_IBSU_FLAT_TWO_FINGERS.value)
        if (ok == False):
            return -1
    elif (ch == '3'):
        ok = StartCapture(IBSU_ImageType.ENUM_IBSU_ROLL_SINGLE_FINGER.value)
        if (ok == False):
            return False
    elif (ch == '4'):
        ok = StartCapture(IBSU_ImageType.ENUM_IBSU_FLAT_FOUR_FINGERS.value)
        if (ok == False):
            return -1
    elif (ch == '5'):
        nRc = IBSU_CancelCaptureImage(m_deviceHandle)
        if (nRc < IBSU_STATUS_OK):
            print("Problem Aborting capture: %d" % nRc)
            return -1

        print("\nCapture stopped.")
    elif (ch == '6'):
        print("\nDo you want to save images (Bitmap, WSQ, PNG and JPEG-2000)? 0=No, 1=Yes: [%d] " % m_options[0])
        sys.stdout.flush()
        ch = input(" >> ")
        if (ch == '1'):
            m_options[0] = 1
        elif (ch == '0'):
            m_options[0] = 0

        print("\nDo you want to calculate NFIQ score? 0=No, 1=Yes: [%d] " % m_options[1])
        sys.stdout.flush()
        ch = input(" >> ")
        if (ch == '1'):
            m_options[1] = 1
        elif (ch == '0'):
            m_options[1] = 0
    elif (ch == '7'):
        print("\nSet preview image)? 0=No, 1=Yes: [%d] " % m_options[2])
        sys.stdout.flush()
        ch = input(" >> ")

        if (ch == '1'):
            propertyValue = "TRUE"
            IBSU_SetProperty(m_deviceHandle, IBSU_PropertyId.ENUM_IBSU_PROPERTY_NO_PREVIEW_IMAGE.value, create_string_buffer(propertyValue.encode("utf-8")))
        elif (ch == '0'):
            propertyValue = "FALSE"
            IBSU_SetProperty(m_deviceHandle, IBSU_PropertyId.ENUM_IBSU_PROPERTY_NO_PREVIEW_IMAGE.value, create_string_buffer(propertyValue.encode("utf-8")))
    elif (ch == '8'): # Spoof function Enable/Disable
        print("\nDo you want to turn on Spoof function? 0=Off, 1=On / Default : Off: [%d]" % m_options[3])
        sys.stdout.flush()
        ch = input(" >> ")

        if (ch == '1'):
            m_options[3] = 1
            # Input / Set Spoof level
            print("\nPlease select spoof level (1~5) / Default Level is 3 : [%d]" % m_options[4])
            sys.stdout.flush()
            ch = input(" >> ")
            m_options[4] = int(ch)
        else :
            m_options[3] = 0
    elif (ch == '9'):
        if (m_deviceHandle.value >= 0):
            IBSU_CloseDevice(m_deviceHandle)
            m_deviceHandle.value = -1
        return -1

    return 1

'''
/*******************************************************************************
 * RunCaptureTest()
 *
 * DESCRIPTION:
 *     Run a capture test.
 ******************************************************************************/
'''
def RunCaptureTest():
    while True:
        nRc = DisplayManu()
        if (nRc == -1):
            break

        time.sleep(0.1)


'''
/*******************************************************************************
 * main()
 * 
 * DESCRIPTION:
 *     Application entry point
 ******************************************************************************/
'''
def main():
    global m_devDesc
    version = IBSU_SdkVersion()

    # /* Get the SDK version. */
    nRc = IBSU_GetSDKVersion(byref(version))
    if (nRc < IBSU_STATUS_OK):
        print("Error %d Retrieving version info" % (nRc))
        sys.exit(1)
    print("IBScanUltimate Product version: %s, File version: %s" \
        % (bytes(version.Product).decode('ascii'), bytes(version.File).decode('ascii')))

    #nRc = IBSU_EnableTraceLog(True)

    # /* Get the number of attached scanners. */
    deviceCount = GetConfiguration()
    if (deviceCount == 0):
        print("No IB Scan devices attached... exiting")
        sys.exit(1)

    # /* Register callbacks for notifications. */
    IBSU_RegisterCallbacks(0, IBSU_Events.ENUM_IBSU_ESSENTIAL_EVENT_DEVICE_COUNT.value,
                           _c_callbackDeviceCount, _c_callbackDeviceCount)

    if (nRc < IBSU_STATUS_OK ):
        print("Problem registering device count change callback: %d" % (nRc))
        sys.exit(1)

    IBSU_RegisterCallbacks(0, IBSU_Events.ENUM_IBSU_ESSENTIAL_EVENT_INIT_PROGRESS.value,
                           _c_callbackInitProgress, _c_callbackInitProgress)
    if (nRc < IBSU_STATUS_OK):
        print("Problem registering init progress change callback: %d" % nRc)
        sys.exit(1)

    # /*
    # * For each scanner, run test.
    # */
    for i in range(deviceCount.value):
#        devDesc = IBSU_DeviceDesc()

        # /* Get device description. */
        nRc = IBSU_GetDeviceDescription(i, byref(m_devDesc))
        if (nRc < IBSU_STATUS_OK):
            print("Error %d Retrieving device description, index # %d" % (nRc, i))
            continue

        # /* Format description of scanner. */
        if (m_devDesc.productName[0] == 0):
            strDevice = "unknown device"
        else:
            strDevice  = bytes(m_devDesc.productName).decode('ascii')
        strDevice += "_"
        strDevice += bytes(m_devDesc.fwVersion).decode('ascii')
        strDevice += " S/N("
        strDevice += bytes(m_devDesc.serialNumber).decode('ascii')
        strDevice += ") on "
        strDevice += bytes(m_devDesc.interfaceType).decode('ascii')

        print (strDevice)


    # /* Launch main menu */
    RunCaptureTest()

    # /* Close the device handle, if still open. */
    nRc = IBSU_CloseDevice(m_deviceHandle)

    print("\nFinished.")


if __name__ == '__main__':
    main()
