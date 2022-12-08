import sys
import time
import os.path
import pickle
from ctypes import *
from os import path
from PySide.QtCore import *
from PySide.QtGui import *
from IBSU_SampleForPySideWidget import *
from include.IBScanUltimateApi import *


class CaptureInfo():
    def __init__(self, PreCaptureMessage=None, PostCaptuerMessage=None, ImageType=None, NumberOfFinger=None, fingerName=None, fingerPosition=None):
        self.PreCaptureMessage = PreCaptureMessage
        self.PostCaptuerMessage = PostCaptuerMessage
        self.ImageType = ImageType
        self.NumberOfFinger = NumberOfFinger
        self.fingerName = fingerName
        self.fingerPosition = fingerPosition


# ///<  Red background brush for scanner
s_brushRed = QColor.fromRgb(255,0,0)
# ///<  Orange background brush for scanner
s_brushOrange = QColor.fromRgb(255,128,0)
# ///<  Green background brush for scanner
s_brushGreen = QColor.fromRgb(0,128,0)
# ///<  Platen brush for scanner
s_brushPlaten = QColor.fromRgb(114,114,114)

CAPTURE_SEQ_FLAT_SINGLE_FINGER = "Single flat finger"
CAPTURE_SEQ_ROLL_SINGLE_FINGER = "Single rolled finger"
CAPTURE_SEQ_2_FLAT_FINGERS = "2 flat fingers"
CAPTURE_SEQ_10_SINGLE_FLAT_FINGERS = "10 single flat fingers"
CAPTURE_SEQ_10_SINGLE_ROLLED_FINGERS = "10 single rolled fingers"
CAPTURE_SEQ_4_FLAT_FINGERS = "4 flat fingers"
CAPTURE_SEQ_10_FLAT_WITH_4_FINGER_SCANNER = "10 flat fingers with 4-finger scanner"

TIMER_STATUS_DELAY = 500

#// LED color definitions
__LED_COLOR_NONE__ = 0
__LED_COLOR_GREEN__	= 1
__LED_COLOR_RED__ = 2
__LED_COLOR_YELLOW__ = 3

#// Key button definitions
__LEFT_KEY_BUTTON__	= 1
__RIGHT_KEY_BUTTON__ = 2

m_callbackDeviceCount = None
m_callbackInitProgress = None
m_callbackAsyncOpenDevice = None
m_callbackCommunicationBreak = None
m_callbackPreviewImage = None
m_callbackTakingAcquisition = None
m_callbackCompleteAcquisition = None
m_callbackResultImageEx = None
m_callbackFingerCount = None
m_callbackFingerQuality = None
m_callbackClearPlaten = None
m_callbackNotifyMessage = None
m_callbackPressedKeyButtons = None

# Spoof Error code string // For Pyside (Python GUI) limitation 
m_strImageStatusCode = 0


class IBSU_SampleDialog(QMainWindow, Ui_IBSU_SampleForPySide):

    def __init__(self, parent=None):
        super(IBSU_SampleDialog, self).__init__(parent)
        self.setupUi(self)

        self.m_nDevHandle = -1                          # ///< Device handle
        self.m_bInitializing = False
        self.m_nSelectedDevIndex = -1                   # ///< Index of selected device
        self.m_nCurrentCaptureStep = -1                 # ///< Current capture step
        self.m_bNeedClearPlaten = False

        self.m_drawImage = IBSU_ImageData()
        self.m_drawImage.Buffer = None

        self.m_strImageMessage = ""
        self.m_bNeedClearPlaten = False
        self.m_bSelectDev = False
        # ///< Sequence of capture steps
        self.m_vecCaptureSeq = []
        # ///< Current capture step

        # ///< Base folder for image saving
        self.m_ImgSaveFolder = ""
        # ///< Sub Folder for image sequence
        self.m_ImgSubFolder = ""
        self.m_strImageMessage = ""
        self.m_nSegmentImageArrayCount = 0
        self.m_SegmentPositionArray = []

        self.m_capturedImg = IBSM_ImageData()
        self.m_capturedImgSplit = IBSM_ImageData()
        self.m_capturedImgSplitCnt = c_int()


        self.m_FingerQuality = [IBSU_FingerQualityState.ENUM_IBSU_FINGER_NOT_PRESENT.value,
                                IBSU_FingerQualityState.ENUM_IBSU_FINGER_NOT_PRESENT.value,
                                IBSU_FingerQualityState.ENUM_IBSU_FINGER_NOT_PRESENT.value,
                                IBSU_FingerQualityState.ENUM_IBSU_FINGER_NOT_PRESENT.value]
        self.m_LedType = c_int(0)
        self.m_ImageType = c_int(0)
        self.m_rollingState = c_int(0)
        self.m_rollingLineX = c_int(0)

        self.m_pBuffer = []
        self.m_pScaledBuffer = []
        self.m_mutex = QMutex()
        self.m_bCapturing = False
        self.m_bDevLocked = False

        for i in range(0, 4):
            segPosition = IBSU_SegmentPosition()
            self.m_SegmentPositionArray.append(segPosition)

        self.m_sliderContrast.setRange(0, 34)
        self.m_sliderContrast.setValue(0)
        self.m_txtContrast.setText("0")

        version = IBSU_SdkVersion()
        # /* Get the SDK version. */
        IBSU_GetSDKVersion(byref(version))
        strDrawString = ("<html><head/><body><p><span style=' font-size:24pt; color:#ffffff;'>SDK v%s</span></p></body></html>" % bytes(version.Product).decode('ascii'));
        self.m_txtDllVersion.setText(strDrawString)

        IBSU_EnableTraceLog(True)

        self.m_cboSmearLevel.clear()
        self.m_cboSmearLevel.addItem("LOW")
        self.m_cboSmearLevel.addItem("MEDIUM")
        self.m_cboSmearLevel.addItem("HIGH")
        self.m_cboSmearLevel.setCurrentIndex(1)

        self.m_cboSpoofLevel.clear()
        self.m_cboSpoofLevel.addItem("1")
        self.m_cboSpoofLevel.addItem("2")
        self.m_cboSpoofLevel.addItem("3")
        self.m_cboSpoofLevel.addItem("4")
        self.m_cboSpoofLevel.addItem("5")
        self.m_cboSpoofLevel.setCurrentIndex(2)

        self.connect(self.m_sliderContrast, SIGNAL("valueChanged(int)"), self.OnChangeContrast)
        self.connect(self.m_btnCaptureStart, SIGNAL("clicked()"), self.OnBnClickedBtnCaptureStart)
        self.connect(self.m_btnCaptureStop, SIGNAL("clicked()"), self.OnBnClickedBtnCaptureStop)
        self.connect(self.m_cboUsbDevices, SIGNAL("currentIndexChanged(int)"), self.OnCbnSelchangeComboDevices)
        self.connect(self.m_cboCaptureSeq, SIGNAL("currentIndexChanged(int)"), self.OnCbnSelchangeComboCaptureSeq)
        self.connect(self.m_btnImageFolder, SIGNAL("clicked()"), self.OnBnClickedBtnImageFolder)

        self.m_timerQuality = QTimer(self)
        self.connect(self.m_timerQuality, SIGNAL("timeout()"), self.OnTimerQuality)
        self.m_timerQuality.start(TIMER_STATUS_DELAY)

        global m_callbackDeviceCount
        global m_callbackInitProgress
        global m_callbackAsyncOpenDevice
        m_callbackDeviceCount = self.OnEvent_DeviceCount()
        m_callbackInitProgress = self.OnEvent_InitProgress()
        m_callbackAsyncOpenDevice = self.OnEvent_AsyncOpenDevice()
        IBSU_RegisterCallbacks(0, IBSU_Events.ENUM_IBSU_ESSENTIAL_EVENT_DEVICE_COUNT.value,
                               m_callbackDeviceCount, byref(py_object(self)))
        IBSU_RegisterCallbacks(0, IBSU_Events.ENUM_IBSU_ESSENTIAL_EVENT_INIT_PROGRESS.value,
                               m_callbackInitProgress, byref(py_object(self)))
        IBSU_RegisterCallbacks(0, IBSU_Events.ENUM_IBSU_ESSENTIAL_EVENT_ASYNC_OPEN_DEVICE.value,
                               m_callbackAsyncOpenDevice, byref(py_object(self)))

        self.OnMsg_UpdateDeviceList()


    def closeEvent(self, event):
        for i in range(0, 10):
            nRc = self._ReleaseDevice()
            if (nRc != IBSU_ERR_RESOURCE_LOCKED):
                break

        time.sleep(0.1)

        self.m_timerQuality.stop()


    def _AddCaptureSeqVector(self, PreCaptureMessage, PostCaptuerMessage, imageType, NumberOfFinger, fingerName, fingerPosition):
        info = CaptureInfo()
        info.PreCaptureMessage = PreCaptureMessage
        info.PostCaptuerMessage = PostCaptuerMessage
        info.ImageType = imageType
        info.NumberOfFinger = NumberOfFinger
        info.fingerName = fingerName
        info.fingerPosition = fingerPosition
        self.m_vecCaptureSeq.append(info)


    def _Make32bitImage_FromRaw(self, data, width, height, rawImage):
        for i in range(0, height):
            row = rawImage.scanLine(i)

            for j in range(0, width):
                row[j*4] = int.from_bytes(data[(height-1-i)*width+j], byteorder='little')
                row[j*4+1] = int.from_bytes(data[(height-1-i)*width+j], byteorder='little')
                row[j*4+2] = int.from_bytes(data[(height-1-i)*width+j], byteorder='little')
                row[j*4+3] = 255


    def _SetStatusBarMessage(self, strMessage):
        self.m_txtStatusMessage.setText(strMessage)


    def _SetImageMessage(self, strMessage):
        self.m_strImageMessage = strMessage


    def _UpdateCaptureSequences(self):
        # // store currently selected sequence
        selectedSeq = self.m_cboCaptureSeq.currentIndex()
        if (selectedSeq > -1):
            strSelectedText = self.m_cboCaptureSeq.currentText()

        self.m_cboCaptureSeq.clear()
        self.m_cboCaptureSeq.addItem("- Please select -")

        devIndex = self.m_cboUsbDevices.currentIndex() - 1
        devDesc = IBSU_DeviceDesc()
        # devDesc.productName[0] = 0
        if (devIndex > -1):
            IBSU_GetDeviceDescription(devIndex, byref(devDesc))

        if ((devDesc.productName == b"WATSON") or
            (devDesc.productName == b"WATSON MINI") or
            (devDesc.productName == b"SHERLOCK_ROIC") or
            (devDesc.productName == b"SHERLOCK")):
            self.m_cboCaptureSeq.addItem(CAPTURE_SEQ_FLAT_SINGLE_FINGER)
            self.m_cboCaptureSeq.addItem(CAPTURE_SEQ_ROLL_SINGLE_FINGER)
            self.m_cboCaptureSeq.addItem(CAPTURE_SEQ_2_FLAT_FINGERS)
            self.m_cboCaptureSeq.addItem(CAPTURE_SEQ_10_SINGLE_FLAT_FINGERS)
            self.m_cboCaptureSeq.addItem(CAPTURE_SEQ_10_SINGLE_ROLLED_FINGERS)
        elif ((devDesc.productName == b"COLUMBO") or
            (devDesc.productName == b"DANNO") or
			(devDesc.productName == b"COLUMBO MINI") or
            (devDesc.productName == b"CURVE") or
            (devDesc.productName == b"COLUMBO 2.0")):
            self.m_cboCaptureSeq.addItem(CAPTURE_SEQ_FLAT_SINGLE_FINGER)
            self.m_cboCaptureSeq.addItem(CAPTURE_SEQ_10_SINGLE_FLAT_FINGERS)
        elif ((devDesc.productName == b"HOLMES") or
            (devDesc.productName == b"KOJAK") or
			(devDesc.productName == b"FIVE-0") or
            (devDesc.productName == b"TF10") or
            (devDesc.productName == b"MF10")):
            self.m_cboCaptureSeq.addItem(CAPTURE_SEQ_FLAT_SINGLE_FINGER)
            self.m_cboCaptureSeq.addItem(CAPTURE_SEQ_ROLL_SINGLE_FINGER)
            self.m_cboCaptureSeq.addItem(CAPTURE_SEQ_2_FLAT_FINGERS)
            self.m_cboCaptureSeq.addItem(CAPTURE_SEQ_4_FLAT_FINGERS)
            self.m_cboCaptureSeq.addItem(CAPTURE_SEQ_10_SINGLE_FLAT_FINGERS)
            self.m_cboCaptureSeq.addItem(CAPTURE_SEQ_10_SINGLE_ROLLED_FINGERS)
            self.m_cboCaptureSeq.addItem(CAPTURE_SEQ_10_FLAT_WITH_4_FINGER_SCANNER)

        self.m_bDevLocked = devDesc.IsDeviceLocked
        if ((devIndex > -1) and (self.m_bDevLocked)):
            self.m_picLock.show()
            self.m_txtDevLockState.show()
        else:
            self.m_picLock.hide()
            self.m_txtDevLockState.hide()

        # // select previously selected sequence
        if (selectedSeq > -1):
            selectedSeq = self.m_cboCaptureSeq.findText(strSelectedText)

        if (selectedSeq == -1):
            self.m_cboCaptureSeq.setCurrentIndex(0)
        else:
            self.m_cboCaptureSeq.setCurrentIndex(selectedSeq)

        self.OnMsg_UpdateDisplayResources()


    def _ReleaseDevice(self):
        if (self.m_nDevHandle != -1):
            nRc = IBSU_CloseDevice(self.m_nDevHandle)
            if (nRc >= IBSU_STATUS_OK):
                self.m_nDevHandle = -1
                self.m_nCurrentCaptureStep = -1
                self.m_bInitializing = False
                self.m_drawImage.Buffer = None

            return nRc

        return IBSU_STATUS_OK


    def _BeepFail(self):
        beeperType = c_int(0)

        if (IBSU_GetOperableBeeper(self.m_nDevHandle, byref(beeperType)) != IBSU_STATUS_OK):
            if (sys.platform.startswith("win")):
                import winsound
                winsound.Beep(3500, 300)
                time.sleep(0.15)
                winsound.Beep(3500, 150)
                time.sleep(0.15)
                winsound.Beep(3500, 150)
                time.sleep(0.15)
                winsound.Beep(3500, 150)
        else:
            # 2/*Sol*/, 12/*300ms = 12*25ms*/
            IBSU_SetBeeper(self.m_nDevHandle, IBSU_BeepPattern.ENUM_IBSU_BEEP_PATTERN_GENERIC.value, 2, 12, 0, 0)
            time.sleep(0.15)
            # 2/*Sol*/, 6/*150ms = 6*25ms*/
            IBSU_SetBeeper(self.m_nDevHandle, IBSU_BeepPattern.ENUM_IBSU_BEEP_PATTERN_GENERIC.value, 2, 6, 0, 0)
            time.sleep(0.15)
            # 2/*Sol*/, 6/*150ms = 6*25ms*/
            IBSU_SetBeeper(self.m_nDevHandle, IBSU_BeepPattern.ENUM_IBSU_BEEP_PATTERN_GENERIC.value, 2, 6, 0, 0)
            time.sleep(0.15)
            IBSU_SetBeeper(self.m_nDevHandle, IBSU_BeepPattern.ENUM_IBSU_BEEP_PATTERN_GENERIC.value, 2, 6, 0, 0)


    def _BeepSuccess(self):
        beeperType = c_int(0)

        if (IBSU_GetOperableBeeper(self.m_nDevHandle, byref(beeperType)) != IBSU_STATUS_OK):
            if (sys.platform.startswith("win")):
                import winsound
                winsound.Beep(3500, 100)
                time.sleep(0.05)
                winsound.Beep(3500, 100)
        else:
            # 2/*Sol*/, 4/*100ms = 12*25ms*/
            IBSU_SetBeeper(self.m_nDevHandle, IBSU_BeepPattern.ENUM_IBSU_BEEP_PATTERN_GENERIC.value, 2, 4, 0, 0)
            time.sleep(0.05)
            # 2/*Sol*/, 4/*100ms = 12*25ms*/
            IBSU_SetBeeper(self.m_nDevHandle, IBSU_BeepPattern.ENUM_IBSU_BEEP_PATTERN_GENERIC.value, 2, 4, 0, 0)


    def _BeepOk(self):
        beeperType = c_int(0)

        if (IBSU_GetOperableBeeper(self.m_nDevHandle, byref(beeperType)) != IBSU_STATUS_OK):
            if (sys.platform.startswith("win")):
                import winsound
                winsound.Beep(3500, 100)

        else:
            # 2/*Sol*/, 4/*100ms = 12*25ms*/
            IBSU_SetBeeper(self.m_nDevHandle, IBSU_BeepPattern.ENUM_IBSU_BEEP_PATTERN_GENERIC.value, 2, 4, 0, 0)


    def _BeepDeviceCommunicationBreak(self):
        if (sys.platform.startswith("win")):
            import winsound
            for i in range(0, 8):
                winsound.Beep(3500, 100)
                time.sleep(0.1)


    def _SaveBitmapImage(self, image, fingerName):
        if ((len(self.m_ImgSaveFolder) == 0) or (len(self.m_ImgSubFolder) == 0)):
            return

        if (sys.platform.startswith("win")):
            strFolder = self.m_ImgSaveFolder + "\\" + self.m_ImgSubFolder
        else:
            strFolder = self.m_ImgSaveFolder + "/" + self.m_ImgSubFolder

        if (QDir(strFolder).exists() == False):
            QDir().mkdir(strFolder)

        if (sys.platform.startswith("win")):
            temp = "\\Image_%02d_" % self.m_nCurrentCaptureStep
        else:
            temp = "/Image_%02d_" % self.m_nCurrentCaptureStep

        strFileName = strFolder
        strFileName += temp
        strFileName += fingerName
        strFileName += ".bmp"
        print (strFileName)

        IBSU_SaveBitmapImage(create_string_buffer(strFileName.encode("utf-8")), image.Buffer,
                             image.Width, image.Height, image.Pitch, image.ResolutionX, image.ResolutionY)


    def _SaveWsqImage(self, image, fingerName):
        if ((len(self.m_ImgSaveFolder) == 0) or (len(self.m_ImgSubFolder) == 0)):
            return

        if (sys.platform.startswith("win")):
            strFolder = self.m_ImgSaveFolder + "\\" + self.m_ImgSubFolder
        else:
            strFolder = self.m_ImgSaveFolder + "/" + self.m_ImgSubFolder

        if (QDir(strFolder).exists() == False):
            QDir().mkdir(strFolder)

        if (sys.platform.startswith("win")):
            temp = "\\Image_%02d_" % self.m_nCurrentCaptureStep
        else:
            temp = "/Image_%02d_" % self.m_nCurrentCaptureStep

        strFileName = strFolder
        strFileName += temp
        strFileName += fingerName
        strFileName += ".wsq"

        comment = ""
        IBSU_WSQEncodeToFile(create_string_buffer(strFileName.encode("utf-8")), image.Buffer,
                             image.Width, image.Height, image.Pitch, image.BitsPerPixel,
                             c_int(500), c_double(0.75), create_string_buffer(comment.encode("utf-8")))


    def _SavePngImage(self, image, fingerName):
        if ((len(self.m_ImgSaveFolder) == 0) or (len(self.m_ImgSubFolder) == 0)):
            return

        if (sys.platform.startswith("win")):
            strFolder = self.m_ImgSaveFolder + "\\" + self.m_ImgSubFolder
        else:
            strFolder = self.m_ImgSaveFolder + "/" + self.m_ImgSubFolder

        if (QDir(strFolder).exists() == False):
            QDir().mkdir(strFolder)

        if (sys.platform.startswith("win")):
            temp = "\\Image_%02d_" % self.m_nCurrentCaptureStep
        else:
            temp = "/Image_%02d_" % self.m_nCurrentCaptureStep

        strFileName = strFolder
        strFileName += temp
        strFileName += fingerName
        strFileName += ".png"

        IBSU_SavePngImage(create_string_buffer(strFileName.encode("utf-8")), image.Buffer,
                          image.Width, image.Height, image.Pitch, image.ResolutionX, image.ResolutionY)


    def _SaveJP2Image(self, image, fingerName):
        if ((len(self.m_ImgSaveFolder) == 0) or (len(self.m_ImgSubFolder) == 0)):
            return

        if (sys.platform.startswith("win")):
            strFolder = self.m_ImgSaveFolder + "\\" + self.m_ImgSubFolder
        else:
            strFolder = self.m_ImgSaveFolder + "/" + self.m_ImgSubFolder

        if (QDir(strFolder).exists() == False):
            QDir().mkdir(strFolder)

        if (sys.platform.startswith("win")):
            temp = "\\Image_%02d_" % self.m_nCurrentCaptureStep
        else:
            temp = "/Image_%02d_" % self.m_nCurrentCaptureStep

        strFileName = strFolder
        strFileName += temp
        strFileName += fingerName
        strFileName += ".jp2"

        IBSU_SaveJP2Image(create_string_buffer(strFileName.encode("utf-8")), image.Buffer,
                          image.Width, image.Height, image.Pitch, image.ResolutionX, image.ResolutionY, 80)


    def _SaveISOImage(self, image, fingerName):
        if ((len(self.m_ImgSaveFolder) == 0) or (len(self.m_ImgSubFolder) == 0)):
            return

        if (sys.platform.startswith("win")):
            strFolder = self.m_ImgSaveFolder + "\\" + self.m_ImgSubFolder
        else:
            strFolder = self.m_ImgSaveFolder + "/" + self.m_ImgSubFolder

        if (QDir(strFolder).exists() == False):
            QDir().mkdir(strFolder)

        if (sys.platform.startswith("win")):
            temp = "\\Image_%02d_" % self.m_nCurrentCaptureStep
        else:
            temp = "/Image_%02d_" % self.m_nCurrentCaptureStep

        strFileName = [0] * 6
        strFileName[0] = strFolder + temp + fingerName + "_ISO_IEC_19794-2_2005.bin"
        strFileName[1] = strFolder + temp + fingerName + "_ISO_IEC_19794-4_2005.bin"
        strFileName[2] = strFolder + temp + fingerName + "_ISO_IEC_19794-2_2011.bin"
        strFileName[3] = strFolder + temp + fingerName + "_ISO_IEC_19794-4_2011.bin"
        strFileName[4] = strFolder + temp + fingerName + "_ANSI_INCITS_378_2004.bin"
        strFileName[5] = strFolder + temp + fingerName + "_ANSI_INCITS_381_2004.bin"

        stdFormat = [IBSM_StandardFormat.ENUM_IBSM_STANDARD_FORMAT_ISO_19794_2_2005.value,
                     IBSM_StandardFormat.ENUM_IBSM_STANDARD_FORMAT_ISO_19794_4_2005.value,
                     IBSM_StandardFormat.ENUM_IBSM_STANDARD_FORMAT_ISO_19794_2_2011.value,
                     IBSM_StandardFormat.ENUM_IBSM_STANDARD_FORMAT_ISO_19794_4_2011.value,
                     IBSM_StandardFormat.ENUM_IBSM_STANDARD_FORMAT_ANSI_INCITS_378_2004.value,
                     IBSM_StandardFormat.ENUM_IBSM_STANDARD_FORMAT_ANSI_INCITS_381_2004.value]

        stdFormatData = IBSM_StandardFormatData()

        for i in range(0, 6):
            nRc = IBSU_ConvertImageToISOANSI(self.m_nDevHandle, pointer(self.m_capturedImgSplit), self.m_capturedImgSplitCnt,
                IBSM_ImageFormat.IBSM_IMG_FORMAT_WSQ.value, stdFormat[i], byref(stdFormatData))
            if (nRc == IBSU_STATUS_OK):
                buf = (c_byte * stdFormatData.DataLength)()
                memmove(buf, stdFormatData.Data, stdFormatData.DataLength)
                with open(strFileName[i], "wb") as fp:
                    fp.write(bytes(buf))
            else:
                print("fail to save %d" % nRc)


    def _WaitingForFinishInitDevice(self, devIndex):
        IsComplete = c_bool()
        devHandle = c_int()
        progressValue = c_int()
        saved_progressValue = -1

        while (True):
            nRc = IBSU_BGetInitProgress(devIndex, byref(IsComplete), byref(devHandle), byref(progressValue))
            if( nRc != IBSU_STATUS_OK or IsComplete == True):
                break

            if (saved_progressValue != progressValue.value):
                strMessage = "Initializing device... %d%%" % progressValue
                self.m_txtStatusMessage.setText(strMessage)
                self.m_txtStatusMessage.repaint()
                saved_progressValue = progressValue

            time.sleep(0.1)

        if (nRc >= IBSU_STATUS_OK):
            self.m_nDevHandle = devHandle

            propertyValue = create_string_buffer(IBSU_MAX_STR_LEN)
            IBSU_GetProperty(devHandle, IBSU_PropertyId.ENUM_IBSU_PROPERTY_IMAGE_WIDTH.value,
                             propertyValue)
            # width = self._atoi(self, propertyValue.value)
            width = int(propertyValue.value)
            IBSU_GetProperty(devHandle, IBSU_PropertyId.ENUM_IBSU_PROPERTY_IMAGE_HEIGHT.value,
                             propertyValue)
            # height = self._atoi(self, propertyValue.value)
            height = int(propertyValue.value)

            self.m_pBuffer = create_string_buffer(width * height)
            self.m_pScaledBuffer = create_string_buffer(self.m_FrameImage.width() * self.m_FrameImage.height())

            # // register callback functions
            global m_callbackCommunicationBreak
            global m_callbackPreviewImage
            global m_callbackTakingAcquisition
            global m_callbackCompleteAcquisition
            global m_callbackResultImageEx
            global m_callbackFingerCount
            global m_callbackFingerQuality
            global m_callbackClearPlaten
            global m_callbackNotifyMessage
            global m_callbackPressedKeyButtons
            m_callbackCommunicationBreak = self.OnEvent_DeviceCommunicationBreak()
            m_callbackPreviewImage = self.OnEvent_PreviewImage()
            m_callbackTakingAcquisition = self.OnEvent_TakingAcquisition()
            m_callbackCompleteAcquisition = self.OnEvent_CompleteAcquisition()
            m_callbackResultImageEx = self.OnEvent_ResultImageEx()
            m_callbackFingerCount = self.OnEvent_FingerCount()
            m_callbackFingerQuality = self.OnEvent_FingerQuality()
            m_callbackClearPlaten = self.OnEvent_ClearPlatenAtCapture()
            m_callbackNotifyMessage = self.OnEvent_NotifyMessage()
            m_callbackPressedKeyButtons = self.OnEvent_PressedKeyButtons()

            IBSU_RegisterCallbacks(devHandle, IBSU_Events.ENUM_IBSU_ESSENTIAL_EVENT_COMMUNICATION_BREAK.value,
                                   m_callbackCommunicationBreak, byref(py_object(self)))
            IBSU_RegisterCallbacks(devHandle, IBSU_Events.ENUM_IBSU_ESSENTIAL_EVENT_PREVIEW_IMAGE.value,
                                   m_callbackPreviewImage, byref(py_object(self)))
            IBSU_RegisterCallbacks(devHandle, IBSU_Events.ENUM_IBSU_ESSENTIAL_EVENT_TAKING_ACQUISITION.value,
                                   m_callbackTakingAcquisition, byref(py_object(self)))
            IBSU_RegisterCallbacks(devHandle, IBSU_Events.ENUM_IBSU_ESSENTIAL_EVENT_COMPLETE_ACQUISITION.value,
                                   m_callbackCompleteAcquisition, byref(py_object(self)))
            IBSU_RegisterCallbacks(devHandle, IBSU_Events.ENUM_IBSU_ESSENTIAL_EVENT_RESULT_IMAGE_EX.value,
                                   m_callbackResultImageEx, byref(py_object(self)))
            IBSU_RegisterCallbacks(devHandle, IBSU_Events.ENUM_IBSU_OPTIONAL_EVENT_FINGER_COUNT.value,
                                   m_callbackFingerCount, byref(py_object(self)))
            IBSU_RegisterCallbacks(devHandle, IBSU_Events.ENUM_IBSU_OPTIONAL_EVENT_FINGER_QUALITY.value,
                                   m_callbackFingerQuality, byref(py_object(self)))
            if (self.m_chkUseClearPlaten.isChecked()):
                IBSU_RegisterCallbacks(devHandle, IBSU_Events.ENUM_IBSU_OPTIONAL_EVENT_CLEAR_PLATEN_AT_CAPTURE.value,
                                       m_callbackClearPlaten, byref(py_object(self)))
            IBSU_RegisterCallbacks(devHandle, IBSU_Events.ENUM_IBSU_OPTIONAL_EVENT_NOTIFY_MESSAGE.value,
                                   m_callbackNotifyMessage, byref(py_object(self)))
            IBSU_RegisterCallbacks(devHandle, IBSU_Events.ENUM_IBSU_ESSENTIAL_EVENT_KEYBUTTON.value,
                                   m_callbackPressedKeyButtons, byref(py_object(self)))

        if (nRc == IBSU_STATUS_OK):
            self.OnMsg_CaptureSeqStart()
            return 0

        if (nRc > IBSU_STATUS_OK):
            self.OnMsg_InitWarning()
        else:
            if (nRc == IBSU_ERR_DEVICE_ACTIVE):
                strMessage = "[Error code = %d] Device initialization failed because in use by another thread/process." % nRc
            elif (nRc == IBSU_ERR_USB20_REQUIRED):
                strMessage = "[Error code = %d] Device initialization failed because SDK only works with USB 2.0." % nRc
            elif (nRc == IBSU_ERR_DEVICE_HIGHER_SDK_REQUIRED):
                minSDKVersion = create_string_buffer(IBSU_MAX_STR_LEN)
                IBSU_GetRequiredSDKVersion(devIndex, minSDKVersion)
                strMessage = "[Error code = %d] Devcie initialization failed because SDK Version %s is required at least." % (nRc, bytes(minSDKVersion.value).decode("ascii"))
            else:
                errorString = create_string_buffer(IBSU_MAX_STR_LEN)
                IBSU_GetErrorString(nRc, errorString)
                strMessage = "[Error code = %d] Device initialization failed. %s" % (nRc, bytes(errorString.value).decode("ascii"))

        self.m_txtStatusMessage.setText(strMessage)
        self.OnMsg_UpdateDisplayResources()
        return 0


    def _ExecuteInitializeDevice(self, nRc, devHandle):
        ledCount = c_int()
        operableLEDs = c_uint()
        devIndex = self.m_cboUsbDevices.currentIndex() -1;

        if (nRc >= IBSU_STATUS_OK):
            self.m_nDevHandle = devHandle

        IBSU_GetOperableLEDs(devHandle, byref(self.m_LedType), byref(ledCount), byref(operableLEDs))

        # if (self.m_pBuffer = None):
        #     delete self.m_pBuffer;
        #
        # if (self.m_pScaledBuffer)
        #     delete self.m_pScaledBuffer;

        propertyValue = create_string_buffer(IBSU_MAX_STR_LEN)
        IBSU_GetProperty(devHandle, IBSU_PropertyId.ENUM_IBSU_PROPERTY_IMAGE_WIDTH.value,
                         propertyValue)
        # width = self._atoi(propertyValue)
        width = int(propertyValue.value)
        IBSU_GetProperty(devHandle, IBSU_PropertyId.ENUM_IBSU_PROPERTY_IMAGE_HEIGHT.value,
                         propertyValue)
        # height = self._atoi(propertyValue)
        height = int(propertyValue.value)

        self.m_pBuffer = create_string_buffer(width * height)
        self.m_pScaledBuffer = create_string_buffer(self.m_FrameImage.width() * self.m_FrameImage.height())


        # // register callback functions
        global m_callbackCommunicationBreak
        global m_callbackPreviewImage
        global m_callbackTakingAcquisition
        global m_callbackCompleteAcquisition
        global m_callbackResultImageEx
        global m_callbackFingerCount
        global m_callbackFingerQuality
        global m_callbackClearPlaten
        global m_callbackNotifyMessage
        global m_callbackPressedKeyButtons
        m_callbackCommunicationBreak = self.OnEvent_DeviceCommunicationBreak()
        m_callbackPreviewImage = self.OnEvent_PreviewImage()
        m_callbackTakingAcquisition = self.OnEvent_TakingAcquisition()
        m_callbackCompleteAcquisition = self.OnEvent_CompleteAcquisition()
        m_callbackResultImageEx = self.OnEvent_ResultImageEx()
        m_callbackFingerCount = self.OnEvent_FingerCount()
        m_callbackFingerQuality = self.OnEvent_FingerQuality()
        m_callbackClearPlaten = self.OnEvent_ClearPlatenAtCapture()
        m_callbackNotifyMessage = self.OnEvent_NotifyMessage()
        m_callbackPressedKeyButtons = self.OnEvent_PressedKeyButtons()

        IBSU_RegisterCallbacks(devHandle, IBSU_Events.ENUM_IBSU_ESSENTIAL_EVENT_COMMUNICATION_BREAK.value,
                               m_callbackCommunicationBreak, byref(py_object(self)))
        IBSU_RegisterCallbacks(devHandle, IBSU_Events.ENUM_IBSU_ESSENTIAL_EVENT_PREVIEW_IMAGE.value,
                               m_callbackPreviewImage, byref(py_object(self)))
        IBSU_RegisterCallbacks(devHandle, IBSU_Events.ENUM_IBSU_ESSENTIAL_EVENT_TAKING_ACQUISITION.value,
                               m_callbackTakingAcquisition, byref(py_object(self)))
        IBSU_RegisterCallbacks(devHandle, IBSU_Events.ENUM_IBSU_ESSENTIAL_EVENT_COMPLETE_ACQUISITION.value,
                               m_callbackCompleteAcquisition, byref(py_object(self)))
        IBSU_RegisterCallbacks(devHandle, IBSU_Events.ENUM_IBSU_ESSENTIAL_EVENT_RESULT_IMAGE_EX.value,
                               m_callbackResultImageEx, byref(py_object(self)))
        IBSU_RegisterCallbacks(devHandle, IBSU_Events.ENUM_IBSU_OPTIONAL_EVENT_FINGER_COUNT.value,
                               m_callbackFingerCount, byref(py_object(self)))
        IBSU_RegisterCallbacks(devHandle, IBSU_Events.ENUM_IBSU_OPTIONAL_EVENT_FINGER_QUALITY.value,
                               m_callbackFingerQuality, byref(py_object(self)))
        if (self.m_chkUseClearPlaten.isChecked()):
            IBSU_RegisterCallbacks(devHandle, IBSU_Events.ENUM_IBSU_OPTIONAL_EVENT_CLEAR_PLATEN_AT_CAPTURE.value,
                                   m_callbackClearPlaten, byref(py_object(self)))
        IBSU_RegisterCallbacks(devHandle, IBSU_Events.ENUM_IBSU_OPTIONAL_EVENT_NOTIFY_MESSAGE.value,
                               m_callbackNotifyMessage, byref(py_object(self)))
        IBSU_RegisterCallbacks(devHandle, IBSU_Events.ENUM_IBSU_ESSENTIAL_EVENT_KEYBUTTON.value,
                               m_callbackPressedKeyButtons, byref(py_object(self)))

        if (nRc == IBSU_STATUS_OK):
            self.OnMsg_CaptureSeqStart()
            return 0

        if (nRc > IBSU_STATUS_OK):
            self.OnMsg_InitWarning()
        else:
            if (nRc == IBSU_ERR_DEVICE_ACTIVE):
                strMessage = "[Error code = %d] Device initialization failed because in use by another thread/process." % nRc
            elif (nRc == IBSU_ERR_USB20_REQUIRED):
                strMessage = "[Error code = %d] Device initialization failed because SDK only works with USB 2.0." % nRc
            elif (nRc == IBSU_ERR_DEVICE_HIGHER_SDK_REQUIRED):
                minSDKVersion = create_string_buffer(IBSU_MAX_STR_LEN)
                IBSU_GetRequiredSDKVersion(devIndex, minSDKVersion)
                strMessage = "[Error code = %d] Devcie initialization failed because SDK Version %s is required at least." % (nRc, bytes(minSDKVersion.value).decode("ascii"))
            else:
                errorString = create_string_buffer(IBSU_MAX_STR_LEN)
                IBSU_GetErrorString(nRc, errorString)
                strMessage = "[Error code = %d] Device initialization failed. %s" % (nRc, bytes(errorString.value).decode("ascii"))

        self.m_txtStatusMessage.setText(strMessage)
        self.OnMsg_UpdateDisplayResources()
        return 0


    def _DrawOverlay_ImageText(self, painter):
        if (len(self.m_strImageMessage) > 0):
            pen = QPen()
        if (self.m_bNeedClearPlaten):
            pen.setColor(Qt.red)
        else:
            pen.setColor(Qt.blue)

        pen.setWidth(1)

        font = QFont("Arial", 10)
        painter.setPen(pen)
        painter.setFont(font)
        painter.drawText(10, 20, self.m_strImageMessage)


    def _DrawOverlay_WarningOfClearPlaten(self, painter, left, top, width, height):
        if (self.m_nDevHandle == -1):
            return

        idle = (self.m_bInitializing == False) and (self.m_nCurrentCaptureStep == -1)

        if (idle == False and self.m_bNeedClearPlaten and self.m_bBlank):
            paintpen = QPen(Qt.red)
            paintpen.setWidth(20)

            painter.setPen(paintpen)
            painter.drawRect(left, top, width, height)


    def _DrawOverlay_DispInvaliedArea(self, painter, width, height):
        bDrawInvalidArea = False

        for i in range(0, IBSU_MAX_SEGMENT_COUNT):
            if ((self.m_FingerQuality[i] == IBSU_FingerQualityState.ENUM_IBSU_QUALITY_INVALID_AREA_TOP.value) or
                (self.m_FingerQuality[i] == IBSU_FingerQualityState.ENUM_IBSU_QUALITY_INVALID_AREA_LEFT.value) or
                (self.m_FingerQuality[i] == IBSU_FingerQualityState.ENUM_IBSU_QUALITY_INVALID_AREA_RIGHT.value)):
                bDrawInvalidArea = True


        if (bDrawInvalidArea):
            pen = QPen()
            arrow_width = 20
            arrow_thickness = 10
            arrow_pos = 30
            arrow_gab = 5

            pen.setColor(Qt.red)
            painter.setPen(pen)

            for i in range(0, IBSU_MAX_SEGMENT_COUNT):
                if (self.m_FingerQuality[i] == IBSU_FingerQualityState.ENUM_IBSU_QUALITY_INVALID_AREA_TOP.value):
                    aptPoly = QPoint()[0,0,0,0]

                    painter.setBrush(QBrush(Qt.red, Qt.SolidPattern))

                    aptPoly[0].setX(width/2)
                    aptPoly[0].setY(arrow_pos)
                    aptPoly[1].setX(aptPoly[0].rx() + arrow_width)
                    aptPoly[1].setY(aptPoly[0].ry() - arrow_width)
                    aptPoly[2].setX(aptPoly[0].rx())
                    aptPoly[2].setY(aptPoly[0].ry() - arrow_thickness)
                    aptPoly[3].setX(aptPoly[0].rx() - arrow_width)
                    aptPoly[3].setY(aptPoly[0].ry() - arrow_width)
                    painter.drawPolygon(aptPoly, 4)

                    aptPoly[0].setX(width/2)
                    aptPoly[0].setY(arrow_pos+arrow_thickness+arrow_gab)
                    aptPoly[1].setX(aptPoly[0].rx() + arrow_width)
                    aptPoly[1].setY(aptPoly[0].ry() - arrow_width)
                    aptPoly[2].setX(aptPoly[0].rx())
                    aptPoly[2].setY(aptPoly[0].ry() - arrow_thickness)
                    aptPoly[3].setX(aptPoly[0].rx() - arrow_width)
                    aptPoly[3].setY(aptPoly[0].ry() - arrow_width)
                    painter.drawPolygon(aptPoly, 4)

                if (self.m_FingerQuality[i] == IBSU_FingerQualityState.ENUM_IBSU_QUALITY_INVALID_AREA_BOTTOM.value):
                    aptPoly = QPoint()[0,0,0,0]

                    painter.setBrush(QBrush(Qt.red, Qt.SolidPattern))

                    aptPoly[0].setX(width/2)
                    aptPoly[0].setY(height - arrow_pos)
                    aptPoly[1].setX(aptPoly[0].rx() - arrow_width)
                    aptPoly[1].setY(aptPoly[0].ry() + arrow_width)
                    aptPoly[2].setX(aptPoly[0].rx())
                    aptPoly[2].setY(aptPoly[0].ry() + arrow_thickness)
                    aptPoly[3].setX(aptPoly[0].rx() + arrow_width)
                    aptPoly[3].setY(aptPoly[0].ry() + arrow_width)
                    painter.drawPolygon(aptPoly, 4)

                    aptPoly[0].setX(width/2)
                    aptPoly[0].setY(height - arrow_thickness - arrow_gab - arrow_pos)
                    aptPoly[1].setX(aptPoly[0].rx() - arrow_width)
                    aptPoly[1].setY(aptPoly[0].ry() + arrow_width)
                    aptPoly[2].setX(aptPoly[0].rx())
                    aptPoly[2].setY(aptPoly[0].ry() + arrow_thickness)
                    aptPoly[3].setX(aptPoly[0].rx() + arrow_width)
                    aptPoly[3].setY(aptPoly[0].ry() + arrow_width)
                    painter.drawPolygon(aptPoly, 4)

                if ( self.m_FingerQuality[i] == IBSU_FingerQualityState.ENUM_IBSU_QUALITY_INVALID_AREA_LEFT.value):
                    aptPoly = QPoint()[0, 0, 0, 0]

                    painter.setBrush(QBrush(Qt.red, Qt.SolidPattern))

                    aptPoly[0].setX(arrow_pos)
                    aptPoly[0].setY(height/2)
                    aptPoly[1].setX(aptPoly[0].rx() - arrow_width)
                    aptPoly[1].setY(aptPoly[0].ry() + arrow_width)
                    aptPoly[2].setX(aptPoly[0].rx() - arrow_thickness)
                    aptPoly[2].setY(aptPoly[0].ry())
                    aptPoly[3].setX(aptPoly[0].rx() - arrow_width)
                    aptPoly[3].setY(aptPoly[0].ry() - arrow_width)
                    painter.drawPolygon(aptPoly, 4)

                    aptPoly[0].setX(arrow_pos+arrow_thickness+arrow_gab)
                    aptPoly[0].setY(height/2)
                    aptPoly[1].setX(aptPoly[0].rx() - arrow_width)
                    aptPoly[1].setY(aptPoly[0].ry() + arrow_width)
                    aptPoly[2].setX(aptPoly[0].rx() - arrow_thickness)
                    aptPoly[2].setY(aptPoly[0].ry())
                    aptPoly[3].setX(aptPoly[0].rx() - arrow_width)
                    aptPoly[3].setY(aptPoly[0].ry() - arrow_width)
                    painter.drawPolygon(aptPoly, 4)

                if ( self.m_FingerQuality[i] == IBSU_FingerQualityState.ENUM_IBSU_QUALITY_INVALID_AREA_RIGHT.value):
                    aptPoly = QPoint()[0, 0, 0, 0]

                    painter.setBrush(QBrush(Qt.red, Qt.SolidPattern))

                    aptPoly[0].setX(width - arrow_pos)
                    aptPoly[0].setY(height/2)
                    aptPoly[1].setX(aptPoly[0].rx() + arrow_width)
                    aptPoly[1].setY(aptPoly[0].ry() + arrow_width)
                    aptPoly[2].setX(aptPoly[0].rx() + arrow_thickness)
                    aptPoly[2].setY(aptPoly[0].ry())
                    aptPoly[3].setX(aptPoly[0].rx() + arrow_width)
                    aptPoly[3].setY(aptPoly[0].ry() - arrow_width)
                    painter.drawPolygon(aptPoly, 4)

                    aptPoly[0].setX(width - arrow_pos-arrow_thickness-arrow_gab)
                    aptPoly[0].setY(height/2)
                    aptPoly[1].setX(aptPoly[0].rx() + arrow_width)
                    aptPoly[1].setY(aptPoly[0].ry() + arrow_width)
                    aptPoly[2].setX(aptPoly[0].rx() + arrow_thickness)
                    aptPoly[2].setY(aptPoly[0].ry())
                    aptPoly[3].setX(aptPoly[0].rx() + arrow_width)
                    aptPoly[3].setY(aptPoly[0].ry() - arrow_width)
                    painter.drawPolygon(aptPoly, 4)



    def _DrawOverlay_ResultSegmentImage(self, painter):
        if (self.m_drawImage.IsFinal):
            if (self.m_chkDrawSegmentImage.isChecked()):
                # // Draw quadrangle for the segment image
                scaleFactor = 0
                leftMargin = 0
                topMargin = 0
                left = 0
                top = 0
                outWidth = self.m_FrameImage.width()
                outHeight = self.m_FrameImage.height()
                tmp_width = outWidth
                tmp_height = outHeight
                imgWidth = self.m_drawImage.Width
                imgHeight = self.m_drawImage.Height
                dispWidth = 0
                dispHeight = 0
                dispImgX = 0
                dispImgY = 0

                if (outWidth > imgWidth):
                    tmp_width = imgWidth
                    left = (outWidth-imgWidth)/2
                if (outHeight > imgHeight):
                    tmp_height = imgHeight
                    top = (outHeight-imgHeight)/2

                ratio_width = tmp_width / imgWidth
                ratio_height = tmp_height / imgHeight

                dispWidth = self.m_FrameImage.width()
                dispHeight = self.m_FrameImage.height()

                if (ratio_width >= ratio_height):
                    dispWidth = tmp_height * imgWidth / imgHeight
                    dispWidth -= (dispWidth % 4)
                    dispHeight = tmp_height
                    dispImgX = (tmp_width - dispWidth) / 2 + left
                    dispImgY = top
                else:
                    dispWidth = tmp_width
                    dispWidth -= (dispWidth % 4)
                    dispHeight = tmp_width * imgHeight / imgWidth
                    dispImgX = left
                    dispImgY = (tmp_height - dispHeight) / 2 + top

                if (dispImgX < 0):
                    dispImgX = 0
                if (dispImgY < 0):
                    dispImgY = 0

                # ///////////////////////////////////////////////////////////////////////////////////
                scaleFactor = dispWidth / self.m_drawImage.Width
                leftMargin = int(dispImgX)
                topMargin = int(dispImgY)
                # ///////////////////////////////////////////////////////////////////////////////////

                for i in range(0, self.m_nSegmentImageArrayCount):
                    pen = QPen(QColor(0, 128, 0))
                    x1 = leftMargin + int(self.m_SegmentPositionArray[i].x1*scaleFactor)
                    x2 = leftMargin + int(self.m_SegmentPositionArray[i].x2*scaleFactor)
                    x3 = leftMargin + int(self.m_SegmentPositionArray[i].x3*scaleFactor)
                    x4 = leftMargin + int(self.m_SegmentPositionArray[i].x4*scaleFactor)
                    y1 = topMargin +  int(self.m_SegmentPositionArray[i].y1*scaleFactor)
                    y2 = topMargin +  int(self.m_SegmentPositionArray[i].y2*scaleFactor)
                    y3 = topMargin +  int(self.m_SegmentPositionArray[i].y3*scaleFactor)
                    y4 = topMargin +  int(self.m_SegmentPositionArray[i].y4*scaleFactor)

                    painter.setPen(pen)
                    painter.drawLine(x1, y1, x2, y2)
                    painter.drawLine(x2, y2, x3, y3)
                    painter.drawLine(x3, y3, x4, y4)
                    painter.drawLine(x4, y4, x1, y1)


    def _DrawOverlay_RollGuideLine(self, painter, width, height):
        if (self.m_nDevHandle == -1 or self.m_nCurrentCaptureStep == -1):
            return

        if (self.m_ImageType == IBSU_ImageType.ENUM_IBSU_ROLL_SINGLE_FINGER.value):
            nRc = IBSU_BGetRollingInfo(self.m_nDevHandle, byref(self.m_rollingState), byref(self.m_rollingLineX))

            if ((nRc == IBSU_STATUS_OK) and self.m_rollingLineX.value > 0 and
                (self.m_rollingState.value == IBSU_RollingState.ENUM_IBSU_ROLLING_TAKE_ACQUISITION.value or
                   self.m_rollingState.value == IBSU_RollingState.ENUM_IBSU_ROLLING_COMPLETE_ACQUISITION.value)):
                pen = QPen()
                # /*double scaleFactor = (double)width / self.m_drawImage.Width;
                # int LineX = self.m_rollingLineX*scaleFactor;*/
                devDesc = IBSU_DeviceDesc()
                # devDesc.productName[0] = 0

                devIndex = self.m_cboUsbDevices.currentIndex() - 1
                IBSU_GetDeviceDescription(devIndex, byref(devDesc))

                scaleFactor = width / self.m_drawImage.Width

                LineX = int(self.m_rollingLineX.value*scaleFactor)

                # // Guide line for rolling
                if (self.m_rollingState.value == IBSU_RollingState.ENUM_IBSU_ROLLING_TAKE_ACQUISITION.value):
                    pen.setColor(Qt.red)
                elif (self.m_rollingState.value == 2):
                    pen.setColor(Qt.green)

                if (self.m_rollingLineX.value > -1):
                    pen.setWidth(2)
                    painter.setPen(pen)
                    painter.drawLine(LineX, 0, LineX, height)


    def _SetLEDs(self, deviceHandle, info, ledColor, bBlink):
        setLEDs = c_int(0)
        ledType = c_int()
        ledCount = c_int()
        operableLEDs = c_uint()
        IBSU_GetOperableLEDs(deviceHandle, byref(ledType), byref(ledCount), byref(operableLEDs))
        if (ledCount == 0):
            return

        if (self.m_LedType == IBSU_LedType.ENUM_IBSU_LED_TYPE_FSCAN.value):
            if (bBlink):
                if (ledColor == __LED_COLOR_GREEN__):
                    setLEDs |= IBSU_LED_F_BLINK_GREEN
                elif (ledColor == __LED_COLOR_RED__):
                    setLEDs |= IBSU_LED_F_BLINK_RED
                elif (ledColor == __LED_COLOR_YELLOW__):
                    setLEDs |= IBSU_LED_F_BLINK_GREEN
                    setLEDs |= IBSU_LED_F_BLINK_RED
        
            if (info.ImageType == IBSU_ImageType.ENUM_IBSU_ROLL_SINGLE_FINGER.value):
                setLEDs |= IBSU_LED_F_PROGRESS_ROLL
        
            if ((info.fingerName == "SFF_Right_Thumb") or
                (info.fingerName == "SRF_Right_Thumb")):
                setLEDs |= IBSU_LED_F_PROGRESS_TWO_THUMB
                if (ledColor == __LED_COLOR_GREEN__):
                    setLEDs |= IBSU_LED_F_RIGHT_THUMB_GREEN
                elif( ledColor == __LED_COLOR_RED__ ):
                    setLEDs |= IBSU_LED_F_RIGHT_THUMB_RED
                elif( ledColor == __LED_COLOR_YELLOW__ ):
                    setLEDs |= IBSU_LED_F_RIGHT_THUMB_GREEN
                    setLEDs |= IBSU_LED_F_RIGHT_THUMB_RED
            elif((info.fingerName == "SFF_Left_Thumb") or
                (info.fingerName == "SRF_Left_Thumb")):
                setLEDs |= IBSU_LED_F_PROGRESS_TWO_THUMB
                if( ledColor == __LED_COLOR_GREEN__ ):
                    setLEDs |= IBSU_LED_F_LEFT_THUMB_GREEN
                elif( ledColor == __LED_COLOR_RED__ ):
                    setLEDs |= IBSU_LED_F_LEFT_THUMB_RED
                elif( ledColor == __LED_COLOR_YELLOW__ ):
                    setLEDs |= IBSU_LED_F_LEFT_THUMB_GREEN
                    setLEDs |= IBSU_LED_F_LEFT_THUMB_RED
            elif( (info.fingerName == "TFF_2_Thumbs") ):
                setLEDs |= IBSU_LED_F_PROGRESS_TWO_THUMB
                if( ledColor == __LED_COLOR_GREEN__ ):
                    setLEDs |= IBSU_LED_F_LEFT_THUMB_GREEN
                    setLEDs |= IBSU_LED_F_RIGHT_THUMB_GREEN
                elif( ledColor == __LED_COLOR_RED__ ):
                    setLEDs |= IBSU_LED_F_LEFT_THUMB_RED
                    setLEDs |= IBSU_LED_F_RIGHT_THUMB_RED
                elif( ledColor == __LED_COLOR_YELLOW__ ):
                    setLEDs |= IBSU_LED_F_LEFT_THUMB_GREEN
                    setLEDs |= IBSU_LED_F_LEFT_THUMB_RED
                    setLEDs |= IBSU_LED_F_RIGHT_THUMB_GREEN
                    setLEDs |= IBSU_LED_F_RIGHT_THUMB_RED
            # ///////////////////LEFT HAND////////////////////
            elif( (info.fingerName == "SFF_Left_Index") or
                (info.fingerName == "SRF_Left_Index") ):
                setLEDs |= IBSU_LED_F_PROGRESS_LEFT_HAND
                if( ledColor == __LED_COLOR_GREEN__ ):
                    setLEDs |= IBSU_LED_F_LEFT_INDEX_GREEN
                elif( ledColor == __LED_COLOR_RED__ ):
                    setLEDs |= IBSU_LED_F_LEFT_INDEX_RED
                elif( ledColor == __LED_COLOR_YELLOW__ ):
                    setLEDs |= IBSU_LED_F_LEFT_INDEX_GREEN
                    setLEDs |= IBSU_LED_F_LEFT_INDEX_RED
            elif( (info.fingerName == "SFF_Left_Middle") or
                (info.fingerName == "SRF_Left_Middle") ):
                setLEDs |= IBSU_LED_F_PROGRESS_LEFT_HAND
                if( ledColor == __LED_COLOR_GREEN__ ):
                    setLEDs |= IBSU_LED_F_LEFT_MIDDLE_GREEN
                elif( ledColor == __LED_COLOR_RED__ ):
                    setLEDs |= IBSU_LED_F_LEFT_MIDDLE_RED
                elif( ledColor == __LED_COLOR_YELLOW__ ):
                    setLEDs |= IBSU_LED_F_LEFT_MIDDLE_GREEN
                    setLEDs |= IBSU_LED_F_LEFT_MIDDLE_RED
            elif( (info.fingerName == "SFF_Left_Ring") or
                (info.fingerName == "SRF_Left_Ring") ):
                setLEDs |= IBSU_LED_F_PROGRESS_LEFT_HAND
                if( ledColor == __LED_COLOR_GREEN__ ):
                    setLEDs |= IBSU_LED_F_LEFT_RING_GREEN
                elif( ledColor == __LED_COLOR_RED__ ):
                    setLEDs |= IBSU_LED_F_LEFT_RING_RED
                elif( ledColor == __LED_COLOR_YELLOW__ ):
                    setLEDs |= IBSU_LED_F_LEFT_RING_GREEN
                    setLEDs |= IBSU_LED_F_LEFT_RING_RED
            elif( (info.fingerName == "SFF_Left_Little") or
                (info.fingerName == "SRF_Left_Little") ):
                setLEDs |= IBSU_LED_F_PROGRESS_LEFT_HAND
                if( ledColor == __LED_COLOR_GREEN__ ):
                    setLEDs |= IBSU_LED_F_LEFT_LITTLE_GREEN
                elif( ledColor == __LED_COLOR_RED__ ):
                    setLEDs |= IBSU_LED_F_LEFT_LITTLE_RED
                elif( ledColor == __LED_COLOR_YELLOW__ ):
                    setLEDs |= IBSU_LED_F_LEFT_LITTLE_GREEN
                    setLEDs |= IBSU_LED_F_LEFT_LITTLE_RED
            elif( (info.fingerName == "4FF_Left_4_Fingers") ):
                setLEDs |= IBSU_LED_F_PROGRESS_LEFT_HAND
                if( ledColor == __LED_COLOR_GREEN__ ):
                    setLEDs |= IBSU_LED_F_LEFT_INDEX_GREEN
                    setLEDs |= IBSU_LED_F_LEFT_MIDDLE_GREEN
                    setLEDs |= IBSU_LED_F_LEFT_RING_GREEN
                    setLEDs |= IBSU_LED_F_LEFT_LITTLE_GREEN
                elif( ledColor == __LED_COLOR_RED__ ):
                    setLEDs |= IBSU_LED_F_LEFT_INDEX_RED
                    setLEDs |= IBSU_LED_F_LEFT_MIDDLE_RED
                    setLEDs |= IBSU_LED_F_LEFT_RING_RED
                    setLEDs |= IBSU_LED_F_LEFT_LITTLE_RED
                elif( ledColor == __LED_COLOR_YELLOW__ ):
                    setLEDs |= IBSU_LED_F_LEFT_INDEX_GREEN
                    setLEDs |= IBSU_LED_F_LEFT_MIDDLE_GREEN
                    setLEDs |= IBSU_LED_F_LEFT_RING_GREEN
                    setLEDs |= IBSU_LED_F_LEFT_LITTLE_GREEN
                    setLEDs |= IBSU_LED_F_LEFT_INDEX_RED
                    setLEDs |= IBSU_LED_F_LEFT_MIDDLE_RED
                    setLEDs |= IBSU_LED_F_LEFT_RING_RED
                    setLEDs |= IBSU_LED_F_LEFT_LITTLE_RED
            # ///////////RIGHT HAND /////////////////////////
            elif( (info.fingerName == "SFF_Right_Index") or
                (info.fingerName == "SRF_Right_Index") ):
                setLEDs |= IBSU_LED_F_PROGRESS_RIGHT_HAND
                if( ledColor == __LED_COLOR_GREEN__ ):
                    setLEDs |= IBSU_LED_F_RIGHT_INDEX_GREEN
                elif( ledColor == __LED_COLOR_RED__ ):
                    setLEDs |= IBSU_LED_F_RIGHT_INDEX_RED
                elif( ledColor == __LED_COLOR_YELLOW__ ):
                    setLEDs |= IBSU_LED_F_RIGHT_INDEX_GREEN
                    setLEDs |= IBSU_LED_F_RIGHT_INDEX_RED
            elif( (info.fingerName == "SFF_Right_Middle") or
                (info.fingerName == "SRF_Right_Middle") ):
                setLEDs |= IBSU_LED_F_PROGRESS_RIGHT_HAND
                if( ledColor == __LED_COLOR_GREEN__ ):
                    setLEDs |= IBSU_LED_F_RIGHT_MIDDLE_GREEN
                elif( ledColor == __LED_COLOR_RED__ ):
                    setLEDs |= IBSU_LED_F_RIGHT_MIDDLE_RED
                elif( ledColor == __LED_COLOR_YELLOW__ ):
                    setLEDs |= IBSU_LED_F_RIGHT_MIDDLE_GREEN
                    setLEDs |= IBSU_LED_F_RIGHT_MIDDLE_RED
            elif( (info.fingerName == "SFF_Right_Ring") or
                (info.fingerName == "SRF_Right_Ring") ):
                setLEDs |= IBSU_LED_F_PROGRESS_RIGHT_HAND
                if( ledColor == __LED_COLOR_GREEN__ ):
                    setLEDs |= IBSU_LED_F_RIGHT_RING_GREEN
                elif( ledColor == __LED_COLOR_RED__ ):
                    setLEDs |= IBSU_LED_F_RIGHT_RING_RED
                elif( ledColor == __LED_COLOR_YELLOW__ ):
                    setLEDs |= IBSU_LED_F_RIGHT_RING_GREEN
                    setLEDs |= IBSU_LED_F_RIGHT_RING_RED
            elif( (info.fingerName == "SFF_Right_Little") or
                (info.fingerName == "SRF_Right_Little") ):
                setLEDs |= IBSU_LED_F_PROGRESS_RIGHT_HAND
                if( ledColor == __LED_COLOR_GREEN__ ):
                    setLEDs |= IBSU_LED_F_RIGHT_LITTLE_GREEN
                elif( ledColor == __LED_COLOR_RED__ ):
                    setLEDs |= IBSU_LED_F_RIGHT_LITTLE_RED
                elif( ledColor == __LED_COLOR_YELLOW__ ):
                    setLEDs |= IBSU_LED_F_RIGHT_LITTLE_GREEN
                    setLEDs |= IBSU_LED_F_RIGHT_LITTLE_RED
            elif( (info.fingerName == "4FF_Right_4_Fingers") ):
                setLEDs |= IBSU_LED_F_PROGRESS_RIGHT_HAND
                if( ledColor == __LED_COLOR_GREEN__ ):
                    setLEDs |= IBSU_LED_F_RIGHT_INDEX_GREEN
                    setLEDs |= IBSU_LED_F_RIGHT_MIDDLE_GREEN
                    setLEDs |= IBSU_LED_F_RIGHT_RING_GREEN
                    setLEDs |= IBSU_LED_F_RIGHT_LITTLE_GREEN
                elif( ledColor == __LED_COLOR_RED__ ):
                    setLEDs |= IBSU_LED_F_RIGHT_INDEX_RED
                    setLEDs |= IBSU_LED_F_RIGHT_MIDDLE_RED
                    setLEDs |= IBSU_LED_F_RIGHT_RING_RED
                    setLEDs |= IBSU_LED_F_RIGHT_LITTLE_RED
                elif( ledColor == __LED_COLOR_YELLOW__ ):
                    setLEDs |= IBSU_LED_F_RIGHT_INDEX_GREEN
                    setLEDs |= IBSU_LED_F_RIGHT_MIDDLE_GREEN
                    setLEDs |= IBSU_LED_F_RIGHT_RING_GREEN
                    setLEDs |= IBSU_LED_F_RIGHT_LITTLE_GREEN
                    setLEDs |= IBSU_LED_F_RIGHT_INDEX_RED
                    setLEDs |= IBSU_LED_F_RIGHT_MIDDLE_RED
                    setLEDs |= IBSU_LED_F_RIGHT_RING_RED
                    setLEDs |= IBSU_LED_F_RIGHT_LITTLE_RED
            
            if (ledColor == __LED_COLOR_NONE__):
                setLEDs = 0
            
            IBSU_SetLEDs(deviceHandle, setLEDs)






# /////////////////////////////////////////////////////////////////////////////////////////////////

    @QtCore.Slot()
    def OnMsg_GetSelectDevice(self):
        if (QThread.currentThread() != self.thread()):
            # // not sure how efficient it is
            QMetaObject.invokeMethod(self, "OnMsg_GetSelectDevice", Qt.QueuedConnection)
            return

        self.m_bSelectDev = self.m_cboUsbDevices.currentIndex() > 0
        return


    @QtCore.Slot()
    def OnMsg_CaptureSeqStart(self):
        if (QThread.currentThread() != self.thread()):
            # // not sure how efficient it is
            QMetaObject.invokeMethod(self, "OnMsg_CaptureSeqStart", Qt.QueuedConnection)
            return
    
        if (self.m_nDevHandle == -1):
            self.OnMsg_UpdateDisplayResources()
            return
    
        strCaptureSeq = ""
        nSelectedSeq = self.m_cboCaptureSeq.currentIndex()
        if (nSelectedSeq > -1):
            strCaptureSeq = self.m_cboCaptureSeq.currentText()
    
        self.m_vecCaptureSeq.clear()
   
        if (strCaptureSeq == CAPTURE_SEQ_FLAT_SINGLE_FINGER):
            self._AddCaptureSeqVector("Please put a single finger on the sensor!",
                                  "Keep finger on the sensor!",
                                  IBSU_ImageType.ENUM_IBSU_FLAT_SINGLE_FINGER.value,
                                  1,
                                  "SFF_Unknown",
                                  IBSM_FingerPosition.IBSM_FINGER_POSITION_UNKNOWN.value)
    
        if (strCaptureSeq == CAPTURE_SEQ_ROLL_SINGLE_FINGER):
            self._AddCaptureSeqVector("Please put a single finger on the sensor!",
                                 "Roll finger!",
                                 IBSU_ImageType.ENUM_IBSU_ROLL_SINGLE_FINGER.value,
                                 1,
                                 "SRF_Unknown",
                                      IBSM_FingerPosition.IBSM_FINGER_POSITION_UNKNOWN.value)

        if (strCaptureSeq == CAPTURE_SEQ_2_FLAT_FINGERS):
            self._AddCaptureSeqVector("Please put two fingers on the sensor!",
                                 "Keep fingers on the sensor!",
                                 IBSU_ImageType.ENUM_IBSU_FLAT_TWO_FINGERS.value,
                                 2,
                                 "TFF_Unknown",
                                      IBSM_FingerPosition.IBSM_FINGER_POSITION_UNKNOWN.value)
    
        if( strCaptureSeq == CAPTURE_SEQ_10_SINGLE_FLAT_FINGERS ):
            self._AddCaptureSeqVector("Please put right thumb on the sensor!",
                                 "Keep fingers on the sensor!",
                                 IBSU_ImageType.ENUM_IBSU_FLAT_SINGLE_FINGER.value,
                                 1,
                                 "SFF_Right_Thumb",
                                      IBSM_FingerPosition.IBSM_FINGER_POSITION_RIGHT_THUMB.value)

            self._AddCaptureSeqVector("Please put right index on the sensor!",
                                 "Keep fingers on the sensor!",
                                 IBSU_ImageType.ENUM_IBSU_FLAT_SINGLE_FINGER.value,
                                 1,
                                 "SFF_Right_Index",
                                      IBSM_FingerPosition.IBSM_FINGER_POSITION_RIGHT_INDEX_FINGER.value)

            self._AddCaptureSeqVector("Please put right middle on the sensor!",
                                 "Keep fingers on the sensor!",
                                 IBSU_ImageType.ENUM_IBSU_FLAT_SINGLE_FINGER.value,
                                 1,
                                 "SFF_Right_Middle",
                                      IBSM_FingerPosition.IBSM_FINGER_POSITION_RIGHT_MIDDLE_FINGER.value)

            self._AddCaptureSeqVector("Please put right ring on the sensor!",
                                 "Keep fingers on the sensor!",
                                 IBSU_ImageType.ENUM_IBSU_FLAT_SINGLE_FINGER.value,
                                 1,
                                 "SFF_Right_Ring",
                                      IBSM_FingerPosition.IBSM_FINGER_POSITION_RIGHT_RING_FINGER.value)

            self._AddCaptureSeqVector("Please put right little on the sensor!",
                                 "Keep fingers on the sensor!",
                                 IBSU_ImageType.ENUM_IBSU_FLAT_SINGLE_FINGER.value,
                                 1,
                                 "SFF_Right_Little",
                                      IBSM_FingerPosition.IBSM_FINGER_POSITION_RIGHT_LITTLE_FINGER.value)

            self._AddCaptureSeqVector("Please put left thumb on the sensor!",
                                 "Keep fingers on the sensor!",
                                 IBSU_ImageType.ENUM_IBSU_FLAT_SINGLE_FINGER.value,
                                 1,
                                 "SFF_Left_Thumb",
                                      IBSM_FingerPosition.IBSM_FINGER_POSITION_LEFT_THUMB.value)

            self._AddCaptureSeqVector("Please put left index on the sensor!",
                                 "Keep fingers on the sensor!",
                                 IBSU_ImageType.ENUM_IBSU_FLAT_SINGLE_FINGER.value,
                                 1,
                                 "SFF_Left_Index",
                                      IBSM_FingerPosition.IBSM_FINGER_POSITION_LEFT_INDEX_FINGER.value)

            self._AddCaptureSeqVector("Please put left middle on the sensor!",
                                 "Keep fingers on the sensor!",
                                 IBSU_ImageType.ENUM_IBSU_FLAT_SINGLE_FINGER.value,
                                 1,
                                 "SFF_Left_Middle",
                                      IBSM_FingerPosition.IBSM_FINGER_POSITION_LEFT_MIDDLE_FINGER.value)

            self._AddCaptureSeqVector("Please put left ring on the sensor!",
                                 "Keep fingers on the sensor!",
                                 IBSU_ImageType.ENUM_IBSU_FLAT_SINGLE_FINGER.value,
                                 1,
                                 "SFF_Left_Ring",
                                      IBSM_FingerPosition.IBSM_FINGER_POSITION_LEFT_RING_FINGER.value)

            self._AddCaptureSeqVector("Please put left little on the sensor!",
                                 "Keep fingers on the sensor!",
                                 IBSU_ImageType.ENUM_IBSU_FLAT_SINGLE_FINGER.value,
                                 1,
                                 "SFF_Left_Little",
                                      IBSM_FingerPosition.IBSM_FINGER_POSITION_LEFT_LITTLE_FINGER.value)

        if (strCaptureSeq == CAPTURE_SEQ_10_SINGLE_ROLLED_FINGERS):
            self._AddCaptureSeqVector("Please put right thumb on the sensor!",
                                 "Roll finger!",
                                 IBSU_ImageType.ENUM_IBSU_ROLL_SINGLE_FINGER.value,
                                 1,
                                 "SFF_Right_Thumb",
                                      IBSM_FingerPosition.IBSM_FINGER_POSITION_RIGHT_THUMB.value)
    
            self._AddCaptureSeqVector("Please put right index on the sensor!",
                                 "Roll finger!",
                                 IBSU_ImageType.ENUM_IBSU_ROLL_SINGLE_FINGER.value,
                                 1,
                                 "SFF_Right_Index",
                                      IBSM_FingerPosition.IBSM_FINGER_POSITION_RIGHT_INDEX_FINGER.value)
    
            self._AddCaptureSeqVector("Please put right middle on the sensor!",
                                 "Roll finger!",
                                 IBSU_ImageType.ENUM_IBSU_ROLL_SINGLE_FINGER.value,
                                 1,
                                 "SFF_Right_Middle",
                                      IBSM_FingerPosition.IBSM_FINGER_POSITION_RIGHT_MIDDLE_FINGER.value)
    
            self._AddCaptureSeqVector("Please put right ring on the sensor!",
                                 "Roll finger!",
                                 IBSU_ImageType.ENUM_IBSU_ROLL_SINGLE_FINGER.value,
                                 1,
                                 "SFF_Right_Ring",
                                      IBSM_FingerPosition.IBSM_FINGER_POSITION_RIGHT_RING_FINGER.value)
    
            self._AddCaptureSeqVector("Please put right little on the sensor!",
                                 "Roll finger!",
                                 IBSU_ImageType.ENUM_IBSU_ROLL_SINGLE_FINGER.value,
                                 1,
                                 "SFF_Right_Little",
                                      IBSM_FingerPosition.IBSM_FINGER_POSITION_LITTLE_INDEX_FINGER.value)
    
            self._AddCaptureSeqVector("Please put left thumb on the sensor!",
                                 "Roll finger!",
                                 IBSU_ImageType.ENUM_IBSU_ROLL_SINGLE_FINGER.value,
                                 1,
                                 "SFF_Left_Thumb",
                                      IBSM_FingerPosition.IBSM_FINGER_POSITION_LEFT_THUMB.value)
    
            self._AddCaptureSeqVector("Please put left index on the sensor!",
                                 "Roll finger!",
                                 IBSU_ImageType.ENUM_IBSU_ROLL_SINGLE_FINGER.value,
                                 1,
                                 "SFF_Left_Index",
                                      IBSM_FingerPosition.IBSM_FINGER_POSITION_LEFT_INDEX_FINGER.value)
    
            self._AddCaptureSeqVector("Please put left middle on the sensor!",
                                 "Roll finger!",
                                 IBSU_ImageType.ENUM_IBSU_ROLL_SINGLE_FINGER.value,
                                 1,
                                 "SFF_Left_Middle",
                                      IBSM_FingerPosition.IBSM_FINGER_POSITION_LEFT_MIDDLE_FINGER_FINGER.value)
    
            self._AddCaptureSeqVector("Please put left ring on the sensor!",
                                 "Roll finger!",
                                 IBSU_ImageType.ENUM_IBSU_ROLL_SINGLE_FINGER.value,
                                 1,
                                 "SFF_Left_Ring",
                                      IBSM_FingerPosition.IBSM_FINGER_POSITION_LEFT_RING_FINGER.value)
    
            self._AddCaptureSeqVector("Please put left little on the sensor!",
                                 "Roll finger!",
                                 IBSU_ImageType.ENUM_IBSU_ROLL_SINGLE_FINGER.value,
                                 1,
                                 "SFF_Left_Little",
                                      IBSM_FingerPosition.IBSM_FINGER_POSITION_LEFT_LITTLE_FINGER.value)


        if (strCaptureSeq == CAPTURE_SEQ_4_FLAT_FINGERS):
            self._AddCaptureSeqVector("Please put 4 fingers on the sensor!",
                                 "Keep fingers on the sensor!",
                                 IBSU_ImageType.ENUM_IBSU_FLAT_FOUR_FINGERS.value,
                                 4,
                                 "4FF_Unknown",
                                      IBSM_FingerPosition.IBSM_FINGER_POSITION_UNKNOWN.value)

        if (strCaptureSeq == CAPTURE_SEQ_10_FLAT_WITH_4_FINGER_SCANNER):
            self._AddCaptureSeqVector("Please put right 4-fingers on the sensor!",
                                 "Keep fingers on the sensor!",
                                 IBSU_ImageType.ENUM_IBSU_FLAT_FOUR_FINGERS.value,
                                 4,
                                 "4FF_Right_4_Fingers",
                                      IBSM_FingerPosition.IBSM_FINGER_POSITION_PLAIN_RIGHT_FOUR_FINGERS.value)
            
            self._AddCaptureSeqVector("Please put left 4-fingers on the sensor!",
                                 "Keep fingers on the sensor!",
                                 IBSU_ImageType.ENUM_IBSU_FLAT_FOUR_FINGERS.value,
                                 4,
                                 "4FF_Left_4_Fingers",
                                      IBSM_FingerPosition.IBSM_FINGER_POSITION_PLAIN_LEFT_FOUR_FINGERS.value)
            
            self._AddCaptureSeqVector("Please put 2-thumbs on the sensor!",
                                 "Keep fingers on the sensor!",
                                 IBSU_ImageType.ENUM_IBSU_FLAT_TWO_FINGERS.value,
                                 2,
                                 "TFF_2_Thumbs",
                                      IBSM_FingerPosition.IBSM_FINGER_POSITION_PLAIN_THUMBS.value)
            
        # // Make subfolder name
        local_time = QDateTime(QDateTime.currentDateTime())
        self.m_ImgSubFolder = local_time.toString("yyyy-MM-dd hhmmss")
    
        self.OnMsg_CaptureSeqNext()


    @QtCore.Slot()
    def OnMsg_CaptureSeqNext(self):
        if (QThread.currentThread() != self.thread()):
            # // not sure how efficient it is
            QMetaObject.invokeMethod(self, "OnMsg_CaptureSeqNext", Qt.QueuedConnection)
            return
    
        if (self.m_nDevHandle == -1):
            return
    
        self.m_bBlank = False
        for i in range(0, 4):
            self.m_FingerQuality[i] = IBSU_FingerQualityState.ENUM_IBSU_FINGER_NOT_PRESENT.value
            
        self.m_nCurrentCaptureStep += 1
        if(self.m_nCurrentCaptureStep >= len(self.m_vecCaptureSeq)):
            # // All of capture sequence completely
            tmpInfo = CaptureInfo()
            self._SetLEDs(self.m_nDevHandle, tmpInfo, __LED_COLOR_NONE__, False)
            self.m_nCurrentCaptureStep = -1
            self.m_ImgSubFolder = ""
    
            self.OnMsg_UpdateDisplayResources()
            self.m_btnCaptureStart.setFocus()
            return

        # if (sys.platform.startswith("win")):
            # if (self.m_chkInvalidArea.checkState()):
            #     IBSU_SetClientDisplayProperty(self.m_nDevHandle, IBSU_ClientWindowPropertyId.ENUM_IBSU_WINDOW_PROPERTY_DISP_INVALID_AREA.value, c_char_p("TRUE".encode("utf-8")))
            # else:
            #     IBSU_SetClientDisplayProperty(self.m_nDevHandle, IBSU_ClientWindowPropertyId.ENUM_IBSU_WINDOW_PROPERTY_DISP_INVALID_AREA.value, c_char_p("FALSE".encode("utf-8")))
    
        if (self.m_chkDetectSmear.checkState()):
            IBSU_SetProperty(self.m_nDevHandle, IBSU_PropertyId.ENUM_IBSU_PROPERTY_ROLL_MODE.value, c_char_p("1".encode("utf-8")))
            strValue = "%d" % self.m_cboSmearLevel.currentIndex()
            IBSU_SetProperty(self.m_nDevHandle, IBSU_PropertyId.ENUM_IBSU_PROPERTY_ROLL_LEVEL.value, c_char_p(strValue.encode("utf-8")))
        else:
            IBSU_SetProperty(self.m_nDevHandle, IBSU_PropertyId.ENUM_IBSU_PROPERTY_ROLL_MODE.value, c_char_p("0".encode("utf-8")))

        if (self.m_chkEnableSpoof.checkState()): # If spoof enable
            nPropRc = 0
            propertyValue = "TRUE"
            nPropRc = IBSU_SetProperty(self.m_nDevHandle, IBSU_PropertyId.ENUM_IBSU_PROPERTY_ENABLE_SPOOF.value, create_string_buffer(propertyValue.encode("utf-8")))
			# Disable segment rotation for the better PAD perfomance
			nPropRc = IBSU_SetProperty(self.m_nDevHandle, IBSU_PropertyId.ENUM_IBSU_PROPERTY_DISABLE_SEGMENT_ROTATION.value, create_string_buffer(propertyValue.encode("utf-8")))
            if (nPropRc == IBSU_STATUS_OK):
                propertyValue = "%d" % self.m_cboSpoofLevel.currentIndex()
                IBSU_SetProperty(self.m_nDevHandle, IBSU_PropertyId.ENUM_IBSU_PROPERTY_SPOOF_LEVEL.value, create_string_buffer(propertyValue.encode("utf-8")))
            else:
                get_propertyValue = create_string_buffer(IBSU_MAX_STR_LEN)
                IBSU_GetErrorString(nPropRc, get_propertyValue)
                get_propertyValueStr = bytes(get_propertyValue.value).decode('ascii')
                self._SetStatusBarMessage(get_propertyValueStr)

        else: # If spoof disable
            propertyValue = "FALSE"
            IBSU_SetProperty(self.m_nDevHandle, IBSU_PropertyId.ENUM_IBSU_PROPERTY_ENABLE_SPOOF.value, create_string_buffer(propertyValue.encode("utf-8")))
    
    # //	for( int i=0; i<IBSU_MAX_SEGMENT_COUNT; i++ )
    # //		IBSU_ModifyOverlayQuadrangle(self.m_nDevHandle, m_nOvSegmentHandle[i], 0, 0, 0, 0, 0, 0, 0, 0, 0, (DWORD)0);
    
        # // Make capture delay for display result image on multi capture mode (500 ms)
        if (self.m_nCurrentCaptureStep > 0):
            time.sleep(0.5)
            self.m_strImageMessage = ""
    
        info = self.m_vecCaptureSeq[self.m_nCurrentCaptureStep]
    
        imgRes = IBSU_ImageResolution.ENUM_IBSU_IMAGE_RESOLUTION_500.value
        bAvailable = c_bool(False)
        nRc = IBSU_IsCaptureAvailable(self.m_nDevHandle, info.ImageType, imgRes, byref(bAvailable))
        if (nRc != IBSU_STATUS_OK or bAvailable == False):
            self._SetStatusBarMessage("The capture mode (%d) is not available" % info.ImageType)
            self.m_nCurrentCaptureStep = -1
            self.OnMsg_UpdateDisplayResources()
            return
    
        # // Start capture
        captureOptions = 0
        if (self.m_chkAutoContrast.checkState()):
            captureOptions |= IBSU_OPTION_AUTO_CONTRAST
        if (self.m_chkAutoCapture.checkState()):
            captureOptions |= IBSU_OPTION_AUTO_CAPTURE
        if (self.m_chkIgnoreFingerCount.checkState()):
            captureOptions |= IBSU_OPTION_IGNORE_FINGER_COUNT
    
        nRc = IBSU_BeginCaptureImage(self.m_nDevHandle, info.ImageType, imgRes, captureOptions)
        if(nRc>= IBSU_STATUS_OK):
            # // Display message for image acuisition
            strMessage = info.PreCaptureMessage
            self._SetStatusBarMessage(strMessage)
            if (self.m_chkAutoCapture.checkState() == False):
                strMessage += "\r\nPress button 'Take Result Image' when image is good!"
    
            self._SetImageMessage(strMessage)
            self.m_ImageType = info.ImageType
    
            self._SetLEDs(self.m_nDevHandle, info, __LED_COLOR_RED__, True)
        else:
            self._SetStatusBarMessage("Failed to execute IBSU_BeginCaptureImage()")
            self.m_nCurrentCaptureStep = -1
    
        self.OnMsg_UpdateDisplayResources()
    
        return


    @QtCore.Slot()
    def OnMsg_DeviceCommunicationBreak(self):
        if (QThread.currentThread() != self.thread()):
            # // not sure how efficient it is
            QMetaObject.invokeMethod(self, "OnMsg_DeviceCommunicationBreak", Qt.QueuedConnection)
            return
    
        if (self.m_nDevHandle == -1):
            return
    
        self._SetStatusBarMessage("Device communication was broken")
    
        nRc = self._ReleaseDevice()
        if (nRc == IBSU_ERR_RESOURCE_LOCKED):
            # // retry to release device
            self.OnMsg_DeviceCommunicationBreak()
        else:
            self._BeepDeviceCommunicationBreak()
            self.OnMsg_UpdateDeviceList()
    
        return


    @QtCore.Slot()
    def OnMsg_UpdateDeviceList(self):
        if (QThread.currentThread() != self.thread()):
            # // not sure how efficient it is
            QMetaObject.invokeMethod(self, "OnMsg_UpdateDeviceList", Qt.QueuedConnection)
            return
    
        idle = self.m_bInitializing == False and (self.m_nCurrentCaptureStep == -1)
    
        if (idle):
            self.m_btnCaptureStop.setEnabled(False)
            self.m_btnCaptureStart.setEnabled(False)
    
        # // store currently selected device
        strSelectedText = ""
        selectedDev = (self.m_cboUsbDevices.currentIndex())
        if (selectedDev > -1):
            strSelectedText = self.m_cboUsbDevices.currentText()

        self.m_cboUsbDevices.clear()
        self.m_cboUsbDevices.addItem("-Please select-")
    
        # // populate combo box
        devices = c_int(0)
        IBSU_GetDeviceCount(byref(devices))
    
        selectedDev = 0
        for i in range(0, devices.value):
            devDesc = IBSU_DeviceDesc()
            if (IBSU_GetDeviceDescription(i, byref(devDesc)) < IBSU_STATUS_OK):
                continue
    
            if (devDesc.productName[0] == 0):
                strDevice = "unkonwn device"
            else:
                bytes(devDesc.productName).decode('ascii')
                strDevice = "%s_v%s (%s)" % (bytes(devDesc.productName).decode("ascii"),
                                             bytes(devDesc.fwVersion).decode("ascii"),
                                             bytes(devDesc.serialNumber).decode("ascii"))

            self.m_cboUsbDevices.addItem(strDevice)
            if (strDevice == strSelectedText):
                selectedDev = i + 1

        if ((selectedDev == 0) and (self.m_cboUsbDevices.count() == 2)):
            selectedDev = 1

        self.m_cboUsbDevices.setCurrentIndex(selectedDev)
    
        if (idle):
            self.OnCbnSelchangeComboDevices()
            self._UpdateCaptureSequences()

        return


    @QtCore.Slot()
    def OnMsg_InitWarning(self):
        if (QThread.currentThread() != self.thread()):
            # // not sure how efficient it is
            QMetaObject.invokeMethod(self, "OnMsg_InitWarning", Qt.QueuedConnection)
            return

        return


    @QtCore.Slot()
    def OnMsg_UpdateDisplayResources(self):
        if (QThread.currentThread() != self.thread()):
            # // not sure how efficient it is
            QMetaObject.invokeMethod(self, "OnMsg_UpdateDisplayResources", Qt.QueuedConnection)
            return

        selectedDev = self.m_cboUsbDevices.currentIndex() > 0
        captureSeq = self.m_cboCaptureSeq.currentIndex() > 0
        idle = (self.m_bInitializing == False) and (self.m_nCurrentCaptureStep == -1)
        active = (self.m_bInitializing == False) and (self.m_nCurrentCaptureStep != -1)
        uninitializeDev = selectedDev and (self.m_nDevHandle == -1)

        self.m_cboUsbDevices.setEnabled(idle)
        self.m_cboCaptureSeq.setEnabled(selectedDev and idle)

        self.m_btnCaptureStart.setEnabled(captureSeq)
        self.m_btnCaptureStop.setEnabled(active)

        self.m_chkAutoContrast.setEnabled( selectedDev and idle)
        self.m_chkAutoCapture.setEnabled(selectedDev and idle)
        self.m_chkIgnoreFingerCount.setEnabled(selectedDev and idle)
        self.m_chkSaveImges.setEnabled(selectedDev and idle)
        self.m_btnImageFolder.setEnabled(selectedDev and idle)

        self.m_chkUseClearPlaten.setEnabled(uninitializeDev)

        strCaption = ""
        if (active):
            strCaption = "Take Result Image"
        elif (active == False) and (self.m_bInitializing == False):
            strCaption = "Start"

        self.m_btnCaptureStart.setText(strCaption)
        return


    @QtCore.Slot()
    def OnMsg_DrawFingerQuality(self):
        if (QThread.currentThread() != self.thread()):
            # // not sure how efficient it is
            QMetaObject.invokeMethod(self, "OnMsg_DrawFingerQuality", Qt.QueuedConnection)
            return

        palette = QPalette()
        for i in range(0, 4):
            if (self.m_bNeedClearPlaten):
                if (self.m_bBlank):
                    palette.setColor(QPalette.Window, s_brushRed)
                else:
                    palette.setColor(QPalette.Window, s_brushPlaten)
            else:
                if (self.m_FingerQuality[i] == IBSU_FingerQualityState.ENUM_IBSU_QUALITY_GOOD.value):
                    palette.setColor(QPalette.Window, s_brushGreen)
                elif (self.m_FingerQuality[i] == IBSU_FingerQualityState.ENUM_IBSU_QUALITY_FAIR.value):
                    palette.setColor(QPalette.Window, s_brushOrange)
                elif (self.m_FingerQuality[i] == IBSU_FingerQualityState.ENUM_IBSU_QUALITY_POOR.value):
                    palette.setColor(QPalette.Window, s_brushRed)
                elif (self.m_FingerQuality[i] == IBSU_FingerQualityState.ENUM_IBSU_FINGER_NOT_PRESENT.value):
                    palette.setColor(QPalette.Window, s_brushPlaten)
                elif (self.m_FingerQuality[i] == IBSU_FingerQualityState.ENUM_IBSU_QUALITY_INVALID_AREA_TOP.value or
                      self.m_FingerQuality[i] == IBSU_FingerQualityState.ENUM_IBSU_QUALITY_INVALID_AREA_TOP.value or
                      self.m_FingerQuality[i] == IBSU_FingerQualityState.ENUM_IBSU_QUALITY_INVALID_AREA_TOP.value or
                      self.m_FingerQuality[i] == IBSU_FingerQualityState.ENUM_IBSU_QUALITY_INVALID_AREA_TOP.value):
                    palette.setColor(QPalette.Window, s_brushRed)
                else:
                    palette.setColor(QPalette.Window, s_brushPlaten)

            if (i == 0):
                self.lblQuality_1.setAutoFillBackground(True)
                self.lblQuality_1.setPalette(palette)
            elif (i == 1):
                self.lblQuality_2.setAutoFillBackground(True)
                self.lblQuality_2.setPalette(palette)
            elif (i == 2):
                self.lblQuality_3.setAutoFillBackground(True)
                self.lblQuality_3.setPalette(palette)
            elif (i == 3):
                self.lblQuality_4.setAutoFillBackground(True)
                self.lblQuality_4.setPalette(palette)

        return


    #@QtCore.Slot(int)
    @QtCore.Slot()
    def OnMsg_AskRecapture(self):
        if (QThread.currentThread() != self.thread()):
            # // not sure how efficient it is
            QMetaObject.invokeMethod(self, "OnMsg_AskRecapture", Qt.QueuedConnection)
            return

        askMsg = "[Warning = %d] Do you want a recapture?" % m_strImageStatusCode
        reply = QMessageBox.question(self, "IntegrationSample For PySide", askMsg, QMessageBox.Yes|QMessageBox.No)
        if (reply == QMessageBox.Yes):
            # // To recapture current finger position
            self.m_nCurrentCaptureStep -= 1
        else:
            self._BeepSuccess()

        QMetaObject.invokeMethod(self, "repaint", Qt.QueuedConnection)

        self.OnMsg_CaptureSeqNext()


    def paintEvent(self, event):
        if (self.m_drawImage.Buffer == None):
            return

        if (self.m_bCapturing == False):
            return

        self.m_bCapturing = False

        if (self.m_drawImage.IsFinal == True):
            # create scaled grayscale (8bit) image with high quality for the result image
            IBSU_GenerateDisplayImage(self.m_drawImage.Buffer, self.m_drawImage.Width, self.m_drawImage.Height,
                                        self.m_pScaledBuffer, self.m_FrameImage.width(), self.m_FrameImage.height(), 0xFF, 0, 2, True)
        else:
            # create scaled grayscale (8bit) image with low quality for the preview images
            IBSU_GenerateDisplayImage(self.m_drawImage.Buffer, self.m_drawImage.Width, self.m_drawImage.Height,
                                        self.m_pScaledBuffer, self.m_FrameImage.width(), self.m_FrameImage.height(), 0xFF, 0, 0, True)

        Image = QImage(self.m_pScaledBuffer, self.m_FrameImage.width(), self.m_FrameImage.height(), self.m_FrameImage.width(), QImage.Format_Indexed8)
        pixMap = QPixmap(QPixmap.fromImage(Image))

        painter = QPainter(pixMap)
        if (sys.platform.startswith("win")):
            self._DrawOverlay_DispInvaliedArea(painter, self.m_FrameImage.width(), self.m_FrameImage.height())

        self._DrawOverlay_ImageText(painter)
        self._DrawOverlay_WarningOfClearPlaten(painter, 0, 0, self.m_FrameImage.width(), self.m_FrameImage.height())
        self._DrawOverlay_ResultSegmentImage(painter)
        self._DrawOverlay_RollGuideLine(painter, self.m_FrameImage.width(), self.m_FrameImage.height())

        self.m_FrameImage.setPixmap(pixMap)

        painter.end()


    def OnBnClickedBtnCaptureStart(self):
        if (self.m_bInitializing == True):
            return

        devIndex = self.m_cboUsbDevices.currentIndex() -1;
        if (devIndex < 0):
            return

        if (self.m_nCurrentCaptureStep != -1):
            IsActive = c_bool()

            nRc = IBSU_IsCaptureActive(self.m_nDevHandle, byref(IsActive))

            if (nRc == IBSU_STATUS_OK and IsActive):
                IBSU_TakeResultImageManually(self.m_nDevHandle)

            return

        if (self.m_nDevHandle == -1):
            self.m_bInitializing = True

            if (self.m_bDevLocked):
                customerKey, ok = QInputDialog.getText(self, self.tr("Input Customer Key"), self.tr("Please enter Customer Key"), QLineEdit.Normal, self.tr(""))
                if (ok):
                    nRc = IBSU_SetCustomerKey(devIndex, IBSU_HashType.ENUM_IBSU_HASH_TYPE_SHA256.value, create_string_buffer(customerKey.encode("utf-8")))
                    if (nRc != IBSU_STATUS_OK):
                        errorString = create_string_buffer(IBSU_MAX_STR_LEN)
                        IBSU_GetErrorString(nRc, errorString)
                        self._SetStatusBarMessage("[Error code = %d] %s" % (nRc, bytes(errorString.value).decode("ascii")))

            nRc = IBSU_AsyncOpenDevice(devIndex)
            self.m_bInitializing = False

            if (nRc >= IBSU_STATUS_OK):
                self.OnMsg_UpdateDisplayResources()
                return
            else:
                if (nRc == IBSU_ERR_DEVICE_ACTIVE):
                    self._SetStatusBarMessage("[Error code = %d] Device initialization failed because in use by another thread/process." % nRc)
                elif (nRc == IBSU_ERR_USB20_REQUIRED):
                    self._SetStatusBarMessage("[Error code = %d] Device initialization failed because SDK only works with USB 2.0." % nRc)
                elif (nRc == IBSU_ERR_DEVICE_HIGHER_SDK_REQUIRED):
                    minSDKVersion = create_string_buffer(IBSU_MAX_STR_LEN)
                    IBSU_GetRequiredSDKVersion(devIndex, minSDKVersion)
                    self._SetStatusBarMessage("[Error code = %d] Devcie initialization failed because SDK Version %s is required at least." % (nRc, bytes(minSDKVersion.value).decode("ascii")))
                else:
                    self._SetStatusBarMessage("[Error code = %d] Device initialization failed" % nRc)
        else:
            self.OnMsg_CaptureSeqStart()

        self.OnMsg_UpdateDisplayResources()


    def OnBnClickedBtnCaptureStop(self):
        if (self.m_nDevHandle == -1):
            return

        IBSU_CancelCaptureImage(self.m_nDevHandle)
        tmpInfo = CaptureInfo()
        self._SetLEDs(self.m_nDevHandle, tmpInfo, __LED_COLOR_NONE__, False)
        self.m_nCurrentCaptureStep = -1
        self.m_bNeedClearPlaten = False
        self.m_bBlank = False

        self._SetStatusBarMessage("Capture Sequence aborted")
        self._SetImageMessage("")
        self.OnMsg_UpdateDisplayResources()


    def OnCbnSelchangeComboDevices(self):
        if (self.m_cboUsbDevices.currentIndex() == self.m_nSelectedDevIndex):
            return

        # QApplication.setOverrideCursor(Qt.WaitCursor)
        self.m_nSelectedDevIndex = self.m_cboUsbDevices.currentIndex()
        if (self.m_nDevHandle != -1):
            self.OnBnClickedBtnCaptureStop()
            self._ReleaseDevice()

        self._UpdateCaptureSequences()
        # QApplication.restoreOverrideCursor()


    def OnCbnSelchangeComboCaptureSeq(self):
        self.OnMsg_UpdateDisplayResources()


    def OnChangeContrast(self):
        if (self.m_nDevHandle == -1 or self.m_chkAutoContrast.checkState()):
            return

        pos = self.m_sliderContrast.value()
        strValue = "%d" % pos

        self.m_txtContrast.setText(strValue)
        IBSU_SetContrast(self.m_nDevHandle, pos)


    def OnBnClickedBtnImageFolder(self):
        fd = QFileDialog()
        fd.setFileMode(QFileDialog.Directory)
        fd.setOption(QFileDialog.ShowDirsOnly)
        fd.setViewMode(QFileDialog.Detail)

        result = fd.exec()
        if (result):
            self.m_ImgSaveFolder = fd.selectedFiles()[0]

        if (IBSU_IsWritableDirectory(self.m_ImgSaveFolder.encode("utf-8"), True) != IBSU_STATUS_OK):
            msg = "You don't have writing permission on this folder\r\nPlease select another folder (e.g. desktop folder)"
            QMessageBox.information(self, "IntegrationSample For PySide", msg)


    def OnTimerQuality(self):
        self.OnMsg_DrawFingerQuality()

        if (self.m_bNeedClearPlaten):
            if (self.m_bBlank):
                self.m_bBlank = False
            else:
                self.m_bBlank = True








#///////////////////////////////////////////////////////////////////////////////////////
    def OnEvent_DeviceCommunicationBreak(self):
        def OnDeviceCommunicationBreak(deviceHandle, pContext):
            if (pContext == None):
                return

            QMutexLocker(self.m_mutex)
            self.OnMsg_DeviceCommunicationBreak()

        return IBSU_Callback(OnDeviceCommunicationBreak)


    def OnEvent_PreviewImage(self):
        def OnPreviewImage(deviceHandle, pContext, image):
            if (pContext == None):
                return

            QMutexLocker(self.m_mutex)
            self.m_drawImage = image
            self.m_pBuffer = image.Buffer

            self.m_bCapturing = True
            QMetaObject.invokeMethod(self, "repaint", Qt.QueuedConnection)

        return IBSU_CallbackPreviewImage(OnPreviewImage)


    def OnEvent_FingerCount(self):
        def OnFingerCount(deviceHandle, pContext, fingerCountState):
            if (pContext == None):
                return

            QMutexLocker(self.m_mutex)
            info = CaptureInfo()
            info = self.m_vecCaptureSeq[self.m_nCurrentCaptureStep]

            if (fingerCountState == IBSU_FingerCountState.ENUM_IBSU_NON_FINGER.value):
                self._SetLEDs(deviceHandle, info, __LED_COLOR_RED__, True)
            else:
                self._SetLEDs(deviceHandle, info, __LED_COLOR_YELLOW__, True)

        return IBSU_CallbackFingerCount(OnFingerCount)


    def OnEvent_FingerQuality(self):
        def OnFingerQuality(deviceHandle, pContext, pQualityArray, qualityArrayCount):
            if (pContext == None):
                return

            QMutexLocker(self.m_mutex)
            info = CaptureInfo()
            info = self.m_vecCaptureSeq[self.m_nCurrentCaptureStep]

            for i in range(0, qualityArrayCount):
                self.m_FingerQuality[i] = pQualityArray[i]

            self.OnMsg_DrawFingerQuality()

        return IBSU_CallbackFingerQuality(OnFingerQuality)


    def OnEvent_DeviceCount(self):
        def OnDeviceCount(detectedDevices, pContext):
            if (pContext == None):
                return

            QMutexLocker(self.m_mutex)
            self.OnMsg_UpdateDeviceList()

        return IBSU_CallbackDeviceCount(OnDeviceCount)


    def OnEvent_InitProgress(self):
        def OnInitProgress(deviceIndex, pContext, progressValue):
            if (pContext == None):
                return

            QMutexLocker(self.m_mutex)
            self._SetStatusBarMessage("Initializing device... %d%%" % progressValue)

        return IBSU_CallbackInitProgress(OnInitProgress)


    def OnEvent_TakingAcquisition(self):
        def OnTakingAcquisition(deviceHandle, pContext, imageType):
            if (pContext == None):
                return

            QMutexLocker(self.m_mutex)
            if (imageType == IBSU_ImageType.ENUM_IBSU_ROLL_SINGLE_FINGER.value):
                self._BeepOk()
                self._SetImageMessage("When done remove finger from sensor")
                self._SetStatusBarMessage("When done remove finger from sensor")

        return IBSU_CallbackTakingAcquisition(OnTakingAcquisition)


    def OnEvent_CompleteAcquisition(self):
        def OnCompleteAcquisition(deviceHandle, pContext, imageType):
            if (pContext == None):
                return

            QMutexLocker(self.m_mutex)
            if (imageType == IBSU_ImageType.ENUM_IBSU_ROLL_SINGLE_FINGER.value):
                self._BeepOk()
            else:
                self._BeepSuccess()
                self._SetImageMessage("Remove fingers from sensor")
                self._SetStatusBarMessage("Acquisition completed, postprocessing..")

        return IBSU_CallbackCompleteAcquisition(OnCompleteAcquisition)


    def OnEvent_ResultImageEx(self):
        def OnResultImageEx(deviceHandle, pContext, imageStatus, image, imageType,
                            detectedFingerCount, segmentImageArrayCount, pSegmentImageArray, pSegmentPositionArray):
            if (pContext == None):
                return

            QMutexLocker(self.m_mutex)
            if (deviceHandle != self.m_nDevHandle):
                return

            if (imageStatus >= IBSU_STATUS_OK):
                if (imageType == IBSU_ImageType.ENUM_IBSU_ROLL_SINGLE_FINGER.value):
                    self._BeepSuccess()

            if (self.m_bNeedClearPlaten):
                self.m_bNeedClearPlaten = False

            IBSU_GetIBSM_ResultImageInfo(self.m_nDevHandle,
                                               self.m_vecCaptureSeq[self.m_nCurrentCaptureStep].fingerPosition,
                                               byref(self.m_capturedImg),
                                               byref(self.m_capturedImgSplit),
                                               byref(self.m_capturedImgSplitCnt))

            imgTypeName = "Unknown"
            if (imageStatus == IBSU_STATUS_OK):
                if (imageType == IBSU_ImageType.ENUM_IBSU_ROLL_SINGLE_FINGER.value):
                    imgTypeName = "Rolling single finger"
                elif (imageType == IBSU_ImageType.ENUM_IBSU_FLAT_SINGLE_FINGER.value):
                    imgTypeName = "Flat single finger"
                elif (imageType == IBSU_ImageType.ENUM_IBSU_FLAT_TWO_FINGERS.value):
                    imgTypeName = "Flat two fingers"
                elif (imageType == IBSU_ImageType.ENUM_IBSU_FLAT_FOUR_FINGERS.value):
                    imgTypeName = "Flat 4 fingers"
                elif (imageType == IBSU_ImageType.ENUM_IBSU_FLAT_THREE_FINGERS.value):
                    imgTypeName = "Flat 3 fingers"
                else:
                    imgTypeName = "Unknown"


            if (imageStatus >= IBSU_STATUS_OK):
                #// Image acquisition successful
                info = CaptureInfo()
                info = self.m_vecCaptureSeq[self.m_nCurrentCaptureStep]
                self._SetLEDs(deviceHandle, info, __LED_COLOR_GREEN__, False)

                if (self.m_chkSaveImges.isChecked()):
                    self._SetStatusBarMessage("Saving image...")
                    info = CaptureInfo()
                    info = self.m_vecCaptureSeq[self.m_nCurrentCaptureStep]
                    self._SaveBitmapImage(image, info.fingerName)
                    self._SaveWsqImage(image, info.fingerName)
                    self._SavePngImage(image, info.fingerName)
                    self._SaveJP2Image(image, info.fingerName)
                    self._SaveISOImage(image, info.fingerName)
                    if (segmentImageArrayCount > 0):
                       for i in range(0, segmentImageArrayCount):
                            segmentName = "%s_Segment_%02d" % (info.fingerName, i)
                            self._SaveBitmapImage(pSegmentImageArray[i], segmentName)
                            self._SaveWsqImage(pSegmentImageArray[i], segmentName)
                            self._SavePngImage(pSegmentImageArray[i], segmentName)
                            self._SaveJP2Image(pSegmentImageArray[i], segmentName)

                if (self.m_chkDrawSegmentImage.isChecked()):
                    self.m_nSegmentImageArrayCount = segmentImageArrayCount
                    self.m_SegmentPositionArray = pSegmentPositionArray

                if (self.m_chkNFIQScore.isChecked()):
                    nfiq_score = [0,0,0,0]
                    score = c_int()
                    strValue = "Err"
                    self._SetStatusBarMessage("Get NFIQ score...")
                    segment_pos = 0
                    for i in range(0, IBSU_MAX_SEGMENT_COUNT):
                        if (self.m_FingerQuality[i] == IBSU_FingerQualityState.ENUM_IBSU_FINGER_NOT_PRESENT.value):
                            continue

                        nRc = IBSU_GetNFIQScore(deviceHandle, pSegmentImageArray[segment_pos].Buffer,
                                                pSegmentImageArray[segment_pos].Width, pSegmentImageArray[segment_pos].Height,
                                                pSegmentImageArray[segment_pos].BitsPerPixel, byref(score))

                        if (nRc == IBSU_STATUS_OK):
                            nfiq_score[i] = score.value
                        else:
                            nfiq_score[i] = -1

                        segment_pos += 1

                    strValue = "%d-%d-%d-%d" % (nfiq_score[0], nfiq_score[1], nfiq_score[2], nfiq_score[3])
                    self.m_txtNFIQScore.setText(strValue)
                    
                if (self.m_chkEnableSpoof.isChecked()): # PAD check for multiple finger(Segment based)
                    isSpoofTotal = ["","","",""]
                    isSpoof = c_int()
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
                        strValue = "%s" % (isSpoofTotal[0])
                    elif (segmentImageArrayCount == 2):
                        strValue = "%s-%s" % (isSpoofTotal[0], isSpoofTotal[1])
                    elif (segmentImageArrayCount == 4):
                        strValue = "%s-%s-%s-%s" % (isSpoofTotal[0], isSpoofTotal[1], isSpoofTotal[2], isSpoofTotal[3])

                    self.m_txtSpoofResult.setText(strValue)

                if (imageStatus == IBSU_STATUS_OK):
                    self._SetImageMessage("%s acquisition completed successfully" % imgTypeName)
                    self._SetStatusBarMessage("%s acquisition completed successfully" % imgTypeName)
                else:
                    # // > IBSU_STATUS_OK
                    self._SetImageMessage("%s acquisition Warning (Warning code = %d)" % (imgTypeName, imageStatus))
                    self._SetStatusBarMessage("%s acquisition Warning (Warning code = %d)" % (imgTypeName, imageStatus))

                    self.m_drawImage = image
                    self.m_pBuffer = image.Buffer
                    self.m_drawImage.Buffer = self.m_pBuffer

                    #self.OnMsg_AskRecapture(imageStatus)
                    global m_strImageStatusCode 
                    m_strImageStatusCode = imageStatus
                    self.OnMsg_AskRecapture()
                    return
            else:
                # // < IBSU_STATUS_OK
                self._SetImageMessage("%s acquisition failed (Error code = %d)" % (imgTypeName, imageStatus))
                self._SetStatusBarMessage("%s acquisition failed (Error code = %d)" % (imgTypeName, imageStatus))

                # // Stop all of acquisition
                self.m_nCurrentCaptureStep = len(self.m_vecCaptureSeq)

            self.m_drawImage = image
            self.m_pBuffer = image.Buffer
            self.m_drawImage.Buffer = self.m_pBuffer
            self.m_bCapturing = True
            QMetaObject.invokeMethod(self, "repaint", Qt.QueuedConnection)

            self.OnMsg_CaptureSeqNext()

        return IBSU_CallbackResultImageEx(OnResultImageEx)


    def OnEvent_ClearPlatenAtCapture(self):
        def OnClearPlatenAtCapture(deviceHandle, pContext, platenState):
            if (pContext == None):
                return

            QMutexLocker(self.m_mutex)
            if (platenState == IBSU_PlatenState.ENUM_IBSU_PLATEN_HAS_FINGERS.value):
                self.m_bNeedClearPlaten = True
            else:
                self.m_bNeedClearPlaten = False

            if (self.m_bNeedClearPlaten):
                self._SetImageMessage("Please remove your fingers on the platen first!")
                self._SetStatusBarMessage("Please remove your fingers on the platen first!")
            else:
                info = CaptureInfo()
                info = self.m_vecCaptureSeq[self.m_nCurrentCaptureStep]

                # // Display message for image acuisition again
                strMessage = info.PreCaptureMessage
                self._SetStatusBarMessage(strMessage)
                if (self.m_chkAutoCapture.checkState() == False):
                    strMessage += "\r\nPress button 'Take Result Image' when image is good!"

                self._SetImageMessage(strMessage)

        return IBSU_CallbackClearPlatenAtCapture(OnClearPlatenAtCapture)


    def OnEvent_AsyncOpenDevice(self):
        def OnAsyncOpenDevice(deviceIndex, pContext, deviceHandle, errorCode):
            if (pContext == None):
                return

            QMutexLocker(self.m_mutex)
            self._ExecuteInitializeDevice(errorCode, deviceHandle)

        return IBSU_CallbackAsyncOpenDevice(OnAsyncOpenDevice)


    def OnEvent_NotifyMessage(self):
        def OnNotifyMessage(deviceHandle, pContext, message):
            if (pContext == None):
                return

            QMutexLocker(self.m_mutex)
            print("OnEvent_NotifyMessage = %d" % message)

        return IBSU_CallbackNotifyMessage(OnNotifyMessage)


    def OnEvent_PressedKeyButtons(self):
        def OnPressedKeyButtons(deviceHandle, pContext, pressedKeyButtons):
            if (pContext == None):
                return

            QMutexLocker(self.m_mutex)
            print("OnEvent_PressedKeyButtons = %d" % pressedKeyButtons)

            self.OnMsg_GetSelectDevice()

            idle = (self.m_bInitializing == False) and (self.m_nCurrentCaptureStep == -1)
            active = (self.m_bInitializing == False) and (self.m_nCurrentCaptureStep != -1 )
            if (pressedKeyButtons == __LEFT_KEY_BUTTON__):
                if (self.m_bSelectDev and idle):
                    IBSU_SetBeeper(deviceHandle, IBSU_BeepPattern.ENUM_IBSU_BEEP_PATTERN_GENERIC.value, 2, 4, 0, 0)
                    self.OnBnClickedBtnCaptureStart()
            elif (pressedKeyButtons == __RIGHT_KEY_BUTTON__):
                if (active):
                    IBSU_SetBeeper(deviceHandle, IBSU_BeepPattern.ENUM_IBSU_BEEP_PATTERN_GENERIC.value, 2, 4, 0, 0)
                    self.OnBnClickedBtnCaptureStop()

        return IBSU_CallbackKeyButtons(OnPressedKeyButtons)









if __name__ == "__main__":
    app = QApplication(sys.argv)
    dlg = IBSU_SampleDialog()
    dlg.show()
    sys.exit(app.exec_())