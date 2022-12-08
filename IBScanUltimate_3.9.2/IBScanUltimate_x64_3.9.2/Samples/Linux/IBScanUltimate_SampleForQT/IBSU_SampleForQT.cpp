#include "IBSU_SampleForQT.h"
#include "ui_IBSU_SampleForQT.h"


// Capture sequence definitions
const QString CAPTURE_SEQ_FLAT_SINGLE_FINGER		= "Single flat finger";
const QString CAPTURE_SEQ_ROLL_SINGLE_FINGER		= "Single rolled finger";
const QString CAPTURE_SEQ_2_FLAT_FINGERS			= "2 flat fingers";
const QString CAPTURE_SEQ_10_SINGLE_FLAT_FINGERS	= "10 single flat fingers";
const QString CAPTURE_SEQ_10_SINGLE_ROLLED_FINGERS	= "10 single rolled fingers";
const QString CAPTURE_SEQ_4_FLAT_FINGERS			= "4 flat fingers";
const QString CAPTURE_SEQ_10_FLAT_WITH_4_FINGER_SCANNER	= "10 flat fingers with 4-finger scanner";

const QColor IBSU_SampleForQT::s_brushRed(255,0,0);
const QColor IBSU_SampleForQT::s_brushOrange(255,128,0);
const QColor IBSU_SampleForQT::s_brushGreen(0,128,0);
const QColor IBSU_SampleForQT::s_brushPlaten(114,114,114);

const int TIMER_STATUS_DELAY = 500;

// LED color definitions
const int __LED_COLOR_NONE__    = 0;
const int __LED_COLOR_GREEN__	= 1;
const int __LED_COLOR_RED__		= 2;
const int __LED_COLOR_YELLOW__	= 3;

// Key button definitions
const int __LEFT_KEY_BUTTON__	= 1;
const int __RIGHT_KEY_BUTTON__	= 2;

IBSU_ImageData	m_drawImage;
unsigned char   *m_pBuffer;
unsigned char   *m_pScaledBuffer;
QMutex			m_mutex;


IBSU_SampleForQT::IBSU_SampleForQT(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::IBSU_SampleForQT)
{
	ui->setupUi(this);

	m_nSelectedDevIndex = -1;
	m_drawImage.Buffer = NULL;

	for(int i=0; i<4; i++)
		m_FingerQuality[i] = ENUM_IBSU_FINGER_NOT_PRESENT;

	m_nDevHandle = -1;
	m_nCurrentCaptureStep = -1;
	m_bInitializing = false;
	m_strImageMessage = "";
	m_bNeedClearPlaten = false;
    m_bPaintEvent = false;
    m_bDevLocked = false;

	ui->m_sliderContrast->setRange(0, 34);
	ui->m_sliderContrast->setValue(0);
	ui->m_txtContrast->setText(QString("0"));

#ifdef Q_WS_WIN
	ui->m_chkInvalidArea->setEnabled(true);
#endif

	IBSU_GetSDKVersion(&m_verInfo);
	QString strDrawString;
	strDrawString.sprintf("<html><head/><body><p><span style=' font-size:19pt; color:#ffffff;'>SDK v%s</span></p></body></html>", m_verInfo.Product);
	ui->m_txtDllVersion->setText(strDrawString);

	ui->m_cboSmearLevel->clear();
    ui->m_cboSmearLevel->addItem("LOW");
    ui->m_cboSmearLevel->addItem("MEDIUM");
    ui->m_cboSmearLevel->addItem("HIGH");
	ui->m_cboSmearLevel->setCurrentIndex(1);

	// Spoof control level
	ui->m_cboSpoofLevel->clear();
	ui->m_cboSpoofLevel->addItem("1");
	ui->m_cboSpoofLevel->addItem("2");
	ui->m_cboSpoofLevel->addItem("3");
	ui->m_cboSpoofLevel->addItem("4");
	ui->m_cboSpoofLevel->addItem("5");
    ui->m_cboSpoofLevel->setCurrentIndex(2);

	connect(ui->m_sliderContrast, SIGNAL(valueChanged(int)), this,SLOT(OnChangeContrast()));
	connect(ui->m_btnCaptureStart, SIGNAL(clicked()), this, SLOT(OnBnClickedBtnCaptureStart()));
	connect(ui->m_btnCaptureStop, SIGNAL(clicked()), this, SLOT(OnBnClickedBtnCaptureStop()));
	connect(ui->m_cboUsbDevices, SIGNAL(currentIndexChanged(int)), this, SLOT(OnCbnSelchangeComboDevices()));
	connect(ui->m_cboCaptureSeq, SIGNAL(currentIndexChanged(int)), this, SLOT(OnCbnSelchangeComboCaptureSeq()));
	connect(ui->m_btnImageFolder, SIGNAL(clicked()), this, SLOT(OnBnClickedBtnImageFolder()));

	m_timerQuality = NULL;
	m_timerQuality = new QTimer(this);
	connect(m_timerQuality, SIGNAL(timeout()), this, SLOT(OnTimerQuality()));
	m_timerQuality->start(TIMER_STATUS_DELAY);

	IBSU_RegisterCallbacks( 0, ENUM_IBSU_ESSENTIAL_EVENT_DEVICE_COUNT, reinterpret_cast<void*>(OnEvent_DeviceCount), this );
	IBSU_RegisterCallbacks( 0, ENUM_IBSU_ESSENTIAL_EVENT_INIT_PROGRESS, reinterpret_cast<void*>(OnEvent_InitProgress), this );
	IBSU_RegisterCallbacks( 0, ENUM_IBSU_ESSENTIAL_EVENT_ASYNC_OPEN_DEVICE, reinterpret_cast<void*>(OnEvent_AsyncOpenDevice), this );

	OnMsg_UpdateDeviceList();
}

IBSU_SampleForQT::~IBSU_SampleForQT()
{
	int nRc;
	for (int i=0; i<10; i++)
	{
		nRc = _ReleaseDevice();
		if (nRc != IBSU_ERR_RESOURCE_LOCKED)
			break;
		Sleeper::msleep( 100 );
	}

	if (m_pBuffer)
	{
		delete [] m_pBuffer;
	}
	
	if (m_pScaledBuffer)
	{
		delete [] m_pScaledBuffer;
	}

	if (m_timerQuality)
	{
		m_timerQuality->stop();
		delete m_timerQuality;
	}

	delete ui;
}

////////////////////////////////////////////////////////////////////////////////////////////
// User defined functions

void IBSU_SampleForQT::_Make32bitImage_FromRaw(uchar *data, int width, int height, QImage *rawImage)
{
    uchar* row;
    for(int i=0;i<height;i++)
    {
        row = rawImage->scanLine(i);

        for(int j=0;j<width;j++)
        {
            row[j*4] = data[(height-1-i)*width+j];
            row[j*4+1] = data[(height-1-i)*width+j];
            row[j*4+2] = data[(height-1-i)*width+j];
            row[j*4+3] = 0xFF;//data[i*width+j];
        }
    }
}

void IBSU_SampleForQT::_SetStatusBarMessage( char* Format, ... )
{
	char cMessage[IBSU_MAX_STR_LEN+1];
	va_list arg_ptr;

	va_start( arg_ptr, Format );
	qvsnprintf( cMessage, IBSU_MAX_STR_LEN, Format, arg_ptr );
	va_end( arg_ptr );  

	QString strMessage;
	strMessage.sprintf("%s", cMessage);
	ui->m_txtStatusMessage->setText(strMessage);
}

void IBSU_SampleForQT::_SetImageMessage( char* Format, ... )
{
	char cMessage[IBSU_MAX_STR_LEN+1];
	va_list arg_ptr;

	va_start( arg_ptr, Format );
	qvsnprintf( cMessage, IBSU_MAX_STR_LEN, Format, arg_ptr );
	va_end( arg_ptr );  

	m_strImageMessage.clear();
	m_strImageMessage.sprintf("%s", cMessage);
}

void IBSU_SampleForQT::_UpdateCaptureSequences()
{
	// store currently selected sequence
    QString strSelectedText;
    int selectedSeq = (ui->m_cboCaptureSeq->currentIndex());
    if (selectedSeq > -1)
        strSelectedText = ui->m_cboCaptureSeq->currentText();

    ui->m_cboCaptureSeq->clear();
    ui->m_cboCaptureSeq->addItem("- Please select -");

    const int devIndex = ui->m_cboUsbDevices->currentIndex() - 1;
    IBSU_DeviceDesc devDesc;
    devDesc.productName[0] = 0;
    if(devIndex > -1)
        IBSU_GetDeviceDescription(devIndex, &devDesc);

    if( (strcmp(devDesc.productName, "WATSON")		== 0) ||
        (strcmp(devDesc.productName, "WATSON MINI")   == 0) ||
        (strcmp(devDesc.productName, "SHERLOCK_ROIC") == 0) ||
        (strcmp(devDesc.productName, "SHERLOCK")      == 0) )
    {
        ui->m_cboCaptureSeq->addItem( CAPTURE_SEQ_FLAT_SINGLE_FINGER );
        ui->m_cboCaptureSeq->addItem( CAPTURE_SEQ_ROLL_SINGLE_FINGER );
        ui->m_cboCaptureSeq->addItem( CAPTURE_SEQ_2_FLAT_FINGERS );
        ui->m_cboCaptureSeq->addItem( CAPTURE_SEQ_10_SINGLE_FLAT_FINGERS );
        ui->m_cboCaptureSeq->addItem( CAPTURE_SEQ_10_SINGLE_ROLLED_FINGERS );
    }
	else if( (strcmp(devDesc.productName, "COLUMBO")	== 0) ||
			 (strcmp(devDesc.productName, "COLUMBO MINI")	== 0) ||
			 (strcmp(devDesc.productName, "CURVE")				== 0) ||
			 (strcmp(devDesc.productName, "DANNO")				== 0) ||
			 (strcmp(devDesc.productName, "COLUMBO 2.0")	== 0) )
    {
        ui->m_cboCaptureSeq->addItem( CAPTURE_SEQ_FLAT_SINGLE_FINGER );
        ui->m_cboCaptureSeq->addItem( CAPTURE_SEQ_10_SINGLE_FLAT_FINGERS );
    }
	else if( (strcmp(devDesc.productName, "HOLMES")			== 0) ||
	         (strcmp(devDesc.productName, "KOJAK") 			== 0) ||
			 (strcmp(devDesc.productName, "FIVE-0")			== 0) ||
			 (strcmp(devDesc.productName, "TF10")			== 0) ||
			 (strcmp(devDesc.productName, "MF10")			== 0))
    {
        ui->m_cboCaptureSeq->addItem( CAPTURE_SEQ_FLAT_SINGLE_FINGER );
        ui->m_cboCaptureSeq->addItem( CAPTURE_SEQ_ROLL_SINGLE_FINGER );
        ui->m_cboCaptureSeq->addItem( CAPTURE_SEQ_2_FLAT_FINGERS );
        ui->m_cboCaptureSeq->addItem( CAPTURE_SEQ_4_FLAT_FINGERS );
        ui->m_cboCaptureSeq->addItem( CAPTURE_SEQ_10_SINGLE_FLAT_FINGERS );
        ui->m_cboCaptureSeq->addItem( CAPTURE_SEQ_10_SINGLE_ROLLED_FINGERS );
        ui->m_cboCaptureSeq->addItem( CAPTURE_SEQ_10_FLAT_WITH_4_FINGER_SCANNER );
    }

    m_bDevLocked = devDesc.IsDeviceLocked;
    if( devIndex > -1 && m_bDevLocked )
    {
        ui->m_picLock->show();
        ui->m_txtDevLockState->show();
    }
    else
    {
        ui->m_picLock->hide();
        ui->m_txtDevLockState->hide();
    }

	// select previously selected sequence
    if(selectedSeq > -1)
        selectedSeq = ui->m_cboCaptureSeq->findText(strSelectedText);

    ui->m_cboCaptureSeq->setCurrentIndex(selectedSeq == -1 ? 0 : selectedSeq);

    OnMsg_UpdateDisplayResources();
}

int IBSU_SampleForQT::_ReleaseDevice()
{
    int nRc = IBSU_STATUS_OK;

    if (m_nDevHandle != -1)
        nRc = IBSU_CloseDevice(m_nDevHandle);

    if(nRc >= IBSU_STATUS_OK)
    {
        m_nDevHandle = -1;
        m_nCurrentCaptureStep = -1;
        m_bInitializing = false;
		m_drawImage.Buffer = NULL;
    }

    return nRc;
}

void IBSU_SampleForQT::_BeepFail()
{
	IBSU_BeeperType beeperType;
    if (IBSU_GetOperableBeeper(m_nDevHandle, &beeperType) != IBSU_STATUS_OK)
    {
#ifdef Q_WS_WIN
		Beep( 3500, 300 );
		Sleeper::msleep( 150 );
		Beep( 3500, 150 );
		Sleeper::msleep( 150 );
		Beep( 3500, 150 );
		Sleeper::msleep( 150 );
		Beep( 3500, 150 );
#endif
	}
	else
    {
   	    IBSU_SetBeeper(m_nDevHandle, ENUM_IBSU_BEEP_PATTERN_GENERIC, 2/*Sol*/, 12/*300ms = 12*25ms*/, 0, 0);
	    Sleeper::msleep(150);
   	    IBSU_SetBeeper(m_nDevHandle, ENUM_IBSU_BEEP_PATTERN_GENERIC, 2/*Sol*/, 6/*150ms = 6*25ms*/, 0, 0);
	    Sleeper::msleep(150);
   	    IBSU_SetBeeper(m_nDevHandle, ENUM_IBSU_BEEP_PATTERN_GENERIC, 2/*Sol*/, 6/*150ms = 6*25ms*/, 0, 0);
	    Sleeper::msleep(150);
   	    IBSU_SetBeeper(m_nDevHandle, ENUM_IBSU_BEEP_PATTERN_GENERIC, 2/*Sol*/, 6/*150ms = 6*25ms*/, 0, 0);
    }
}

void IBSU_SampleForQT::_BeepSuccess()
{
	IBSU_BeeperType beeperType;
    if (IBSU_GetOperableBeeper(m_nDevHandle, &beeperType) != IBSU_STATUS_OK)
    {
#ifdef Q_WS_WIN
		Beep( 3500, 100 );
		Sleeper::msleep( 50 );
		Beep( 3500, 100 );
#endif
	}
	else
    {
   	    IBSU_SetBeeper(m_nDevHandle, ENUM_IBSU_BEEP_PATTERN_GENERIC, 2/*Sol*/, 4/*100ms = 4*25ms*/, 0, 0);
	    Sleeper::msleep(150);
   	    IBSU_SetBeeper(m_nDevHandle, ENUM_IBSU_BEEP_PATTERN_GENERIC, 2/*Sol*/, 4/*100ms = 4*25ms*/, 0, 0);
    }
}

void IBSU_SampleForQT::_BeepOk()
{
	IBSU_BeeperType beeperType;
    if (IBSU_GetOperableBeeper(m_nDevHandle, &beeperType) != IBSU_STATUS_OK)
	{
#ifdef Q_WS_WIN
		Beep( 3500, 100 );
#endif
	}
	else
    {
   	    IBSU_SetBeeper(m_nDevHandle, ENUM_IBSU_BEEP_PATTERN_GENERIC, 2/*Sol*/, 4/*100ms = 4*25ms*/, 0, 0);
    }
}

void IBSU_SampleForQT::_BeepDeviceCommunicationBreak()
{
#ifdef Q_WS_WIN
	for (int i=0; i<8; i++)
	{
		Beep( 3500, 100 );
		Sleeper::msleep( 100 );
	}
#endif
}

void IBSU_SampleForQT::_SaveBitmapImage(const IBSU_ImageData &image, const QString &fingerName)
{
	if( ( m_ImgSaveFolder.length() == 0 ) || ( m_ImgSubFolder.length() == 0 ) )
	{
		return;
	}
  
	QString strFolder;
#ifdef Q_WS_WIN
	strFolder = m_ImgSaveFolder + "\\" + m_ImgSubFolder;
#else
	strFolder = m_ImgSaveFolder + "/" + m_ImgSubFolder;
#endif
	if (!QDir(strFolder).exists())
		QDir().mkdir(strFolder);

	QString strFileName;
	QString temp;
#ifdef Q_WS_WIN
	temp.sprintf("\\Image_%02d_", m_nCurrentCaptureStep);
#else
	temp.sprintf("/Image_%02d_", m_nCurrentCaptureStep);
#endif
	strFileName = strFolder;
	strFileName += temp;
	strFileName += fingerName;
	strFileName += ".bmp";
	QByteArray byteName = strFileName.toLocal8Bit();
	char *cfileName = byteName.data();

	IBSU_SaveBitmapImage( cfileName, (BYTE*)image.Buffer, 
						  image.Width, image.Height, image.Pitch, 
						  image.ResolutionX, image.ResolutionY );
}

void IBSU_SampleForQT::_SaveWsqImage(const IBSU_ImageData &image, const QString &fingerName)
{
	if( ( m_ImgSaveFolder.length() == 0 ) || ( m_ImgSubFolder.length() == 0 ) )
	{
		return;
	}
  
	QString strFolder;
#ifdef Q_WS_WIN
	strFolder = m_ImgSaveFolder + "\\" + m_ImgSubFolder;
#else
	strFolder = m_ImgSaveFolder + "/" + m_ImgSubFolder;
#endif
	if (!QDir(strFolder).exists())
		QDir().mkdir(strFolder);

	QString strFileName;
	QString temp;
#ifdef Q_WS_WIN
	temp.sprintf("\\Image_%02d_", m_nCurrentCaptureStep);
#else
	temp.sprintf("/Image_%02d_", m_nCurrentCaptureStep);
#endif
	strFileName = strFolder;
	strFileName += temp;
	strFileName += fingerName;
	strFileName += ".wsq";
	QByteArray byteName = strFileName.toLocal8Bit();
	char *cfileName = byteName.data();

	IBSU_WSQEncodeToFile( cfileName, (BYTE*)image.Buffer, 
						  image.Width, image.Height, image.Pitch, image.BitsPerPixel, 
						  image.ResolutionX, (double)0.75, "" );
}

void IBSU_SampleForQT::_SavePngImage(const IBSU_ImageData &image, const QString &fingerName)
{
	if( ( m_ImgSaveFolder.length() == 0 ) || ( m_ImgSubFolder.length() == 0 ) )
	{
		return;
	}
  
	QString strFolder;
#ifdef Q_WS_WIN
	strFolder = m_ImgSaveFolder + "\\" + m_ImgSubFolder;
#else
	strFolder = m_ImgSaveFolder + "/" + m_ImgSubFolder;
#endif
	if (!QDir(strFolder).exists())
		QDir().mkdir(strFolder);

	QString strFileName;
	QString temp;
#ifdef Q_WS_WIN
	temp.sprintf("\\Image_%02d_", m_nCurrentCaptureStep);
#else
	temp.sprintf("/Image_%02d_", m_nCurrentCaptureStep);
#endif
	strFileName = strFolder;
	strFileName += temp;
	strFileName += fingerName;
	strFileName += ".png";
	QByteArray byteName = strFileName.toLocal8Bit();
	char *cfileName = byteName.data();

	IBSU_SavePngImage( cfileName, (BYTE*)image.Buffer, 
						  image.Width, image.Height, image.Pitch, 
						  image.ResolutionX, image.ResolutionY );
}

void IBSU_SampleForQT::_SaveJP2Image(const IBSU_ImageData &image, const QString &fingerName)
{
	if( ( m_ImgSaveFolder.length() == 0 ) || ( m_ImgSubFolder.length() == 0 ) )
	{
		return;
	}
  
	QString strFolder;
#ifdef Q_WS_WIN
	strFolder = m_ImgSaveFolder + "\\" + m_ImgSubFolder;
#else
	strFolder = m_ImgSaveFolder + "/" + m_ImgSubFolder;
#endif
	if (!QDir(strFolder).exists())
		QDir().mkdir(strFolder);

	QString strFileName;
	QString temp;
#ifdef Q_WS_WIN
	temp.sprintf("\\Image_%02d_", m_nCurrentCaptureStep);
#else
	temp.sprintf("/Image_%02d_", m_nCurrentCaptureStep);
#endif
	strFileName = strFolder;
	strFileName += temp;
	strFileName += fingerName;
	strFileName += ".jp2";
	QByteArray byteName = strFileName.toLocal8Bit();
	char *cfileName = byteName.data();

	IBSU_SaveJP2Image( cfileName, (BYTE*)image.Buffer, 
						  image.Width, image.Height, image.Pitch, 
						  image.ResolutionX, image.ResolutionY, 80 );
}

void IBSU_SampleForQT::_SaveISOImage(const IBSU_ImageData &image, const QString &fingerName)
{
	if( ( m_ImgSaveFolder.length() == 0 ) || ( m_ImgSubFolder.length() == 0 ) )
	{
		return;
	}
  
	QString strFolder;
#ifdef Q_WS_WIN
	strFolder = m_ImgSaveFolder + "\\" + m_ImgSubFolder;
#else
	strFolder = m_ImgSaveFolder + "/" + m_ImgSubFolder;
#endif
	if (!QDir(strFolder).exists())
		QDir().mkdir(strFolder);

    IBSM_StandardFormatData StdFormatData;
    FILE                    *fp;
	QString                 strFileName[6];
    IBSM_StandardFormat     STDformat[6];
	QString 				temp1, temp2;
#ifdef Q_WS_WIN
	temp1.sprintf("\\Image_%02d_", m_nCurrentCaptureStep);
#else
	temp1.sprintf("/Image_%02d_", m_nCurrentCaptureStep);
#endif
	temp2 = strFolder;
	temp2 += temp1;
	temp2 += fingerName;
	
    strFileName[0] = temp2 + "_ISO_IEC_19794-2_2005.bin";
    strFileName[1] = temp2 + "_ISO_IEC_19794-4_2005.bin";
    strFileName[2] = temp2 + "_ISO_IEC_19794-2_2011.bin";
    strFileName[3] = temp2 + "_ISO_IEC_19794-4_2011.bin";
    strFileName[4] = temp2 + "_ANSI_INCITS_378_2004.bin";
    strFileName[5] = temp2 + "_ANSI_INCITS_381_2004.bin";

    STDformat[0] = ENUM_IBSM_STANDARD_FORMAT_ISO_19794_2_2005;
    STDformat[1] = ENUM_IBSM_STANDARD_FORMAT_ISO_19794_4_2005;
    STDformat[2] = ENUM_IBSM_STANDARD_FORMAT_ISO_19794_2_2011;
    STDformat[3] = ENUM_IBSM_STANDARD_FORMAT_ISO_19794_4_2011;
    STDformat[4] = ENUM_IBSM_STANDARD_FORMAT_ANSI_INCITS_378_2004;
    STDformat[5] = ENUM_IBSM_STANDARD_FORMAT_ANSI_INCITS_381_2004;

    for(int i = 0; i < 6 ; i++)
    {
        int nRc;
        nRc = IBSU_ConvertImageToISOANSI(   m_nDevHandle,
                                            m_CapturedImgSplit,
                                            m_CapturedImgSplitCnt,
                                            IBSM_IMG_FORMAT_WSQ,
                                            STDformat[i],
                                            &StdFormatData);
        if(nRc == IBSU_STATUS_OK)
        {
            QByteArray byteName = strFileName[i].toLocal8Bit();
	        char *cfileName = byteName.data();

            fp = fopen(cfileName, "wb");
            if(fp == NULL)
            {
	            QString msg;
				msg.sprintf("ISO File write failed");
		        QMessageBox::information(this, "IntegrationSample For QT", msg);
	            return;
            }

            fwrite(StdFormatData.Data, 1, StdFormatData.DataLength, fp);
            fclose(fp);
        }
    }
}

int IBSU_SampleForQT::_WaitingForFinishInitDevice(const int devIndex)
{
    int     nRc;
    BOOL    IsComplete;
    int     devHandle;
    int     progressValue, saved_progressValue = -1;
	QString strMessage;
	char minSDKVersion[IBSU_MAX_STR_LEN];
    char errorString[IBSU_MAX_STR_LEN];

    while(true)
    {
        nRc = IBSU_BGetInitProgress(devIndex, &IsComplete, &devHandle, &progressValue);
        if( nRc != IBSU_STATUS_OK || IsComplete)
            break;

		if (saved_progressValue != progressValue)
		{
			strMessage.sprintf("Initializing device... %d%%", progressValue);
			ui->m_txtStatusMessage->setText(strMessage);
			ui->m_txtStatusMessage->repaint();
			saved_progressValue = progressValue;
		}

		Sleeper::msleep(100);
    }

    if(nRc >= IBSU_STATUS_OK)
    {
        m_nDevHandle = devHandle;

		if (m_pBuffer)
			delete m_pBuffer;
			
		if (m_pScaledBuffer)
			delete m_pScaledBuffer;

		char propertyValue[IBSU_MAX_STR_LEN];
		IBSU_GetProperty(devHandle, ENUM_IBSU_PROPERTY_IMAGE_WIDTH, propertyValue);
		int width = atoi(propertyValue);
		IBSU_GetProperty(devHandle, ENUM_IBSU_PROPERTY_IMAGE_HEIGHT, propertyValue);
		int height = atoi(propertyValue);

		m_pBuffer = new unsigned char [width * height];
        m_pScaledBuffer = new unsigned char [ui->m_FrameImage->width() * ui->m_FrameImage->height() * 4];

		// register callback functions
		IBSU_RegisterCallbacks( devHandle, ENUM_IBSU_ESSENTIAL_EVENT_COMMUNICATION_BREAK, reinterpret_cast<void*>(OnEvent_DeviceCommunicationBreak), this );    
		IBSU_RegisterCallbacks( devHandle, ENUM_IBSU_ESSENTIAL_EVENT_PREVIEW_IMAGE, reinterpret_cast<void*>(OnEvent_PreviewImage), this );
		IBSU_RegisterCallbacks( devHandle, ENUM_IBSU_ESSENTIAL_EVENT_TAKING_ACQUISITION, reinterpret_cast<void*>(OnEvent_TakingAcquisition), this );  
		IBSU_RegisterCallbacks( devHandle, ENUM_IBSU_ESSENTIAL_EVENT_COMPLETE_ACQUISITION, reinterpret_cast<void*>(OnEvent_CompleteAcquisition), this );  
        IBSU_RegisterCallbacks( devHandle, ENUM_IBSU_ESSENTIAL_EVENT_RESULT_IMAGE_EX, reinterpret_cast<void*>(OnEvent_ResultImageEx), this );  
		IBSU_RegisterCallbacks( devHandle, ENUM_IBSU_OPTIONAL_EVENT_FINGER_COUNT, reinterpret_cast<void*>(OnEvent_FingerCount), this );  
		IBSU_RegisterCallbacks( devHandle, ENUM_IBSU_OPTIONAL_EVENT_FINGER_QUALITY, reinterpret_cast<void*>(OnEvent_FingerQuality), this );  
		if( ui->m_chkUseClearPlaten->isChecked() )
			IBSU_RegisterCallbacks( devHandle, ENUM_IBSU_OPTIONAL_EVENT_CLEAR_PLATEN_AT_CAPTURE, reinterpret_cast<void*>(OnEvent_ClearPlatenAtCapture), this );  
		IBSU_RegisterCallbacks( devHandle, ENUM_IBSU_OPTIONAL_EVENT_NOTIFY_MESSAGE, reinterpret_cast<void*>(OnEvent_NotifyMessage), this );  
		IBSU_RegisterCallbacks( devHandle, ENUM_IBSU_ESSENTIAL_EVENT_KEYBUTTON, reinterpret_cast<void*>(OnEvent_PressedKeyButtons), this );
    }

    if(nRc == IBSU_STATUS_OK)
    {
        OnMsg_CaptureSeqStart();
        return 0;
    }

    if(nRc > IBSU_STATUS_OK)
        OnMsg_InitWarning();
    else
    {
        switch(nRc)
        {
        case IBSU_ERR_DEVICE_ACTIVE:
			strMessage.sprintf("[Error code = %d] Device initialization failed because in use by another thread/process.", nRc);
            break;
        case IBSU_ERR_USB20_REQUIRED:
			strMessage.sprintf("[Error code = %d] Device initialization failed because SDK only works with USB 2.0.", nRc);
            break;
        case IBSU_ERR_DEVICE_HIGHER_SDK_REQUIRED:
			IBSU_GetRequiredSDKVersion(devIndex, minSDKVersion);
			strMessage.sprintf("[Error code = %d] Devcie initialization failed because SDK Version %s is required at least.", nRc, minSDKVersion );
			break;
        default:
            IBSU_GetErrorString(nRc, errorString);
            _SetStatusBarMessage("[Error code = %d] Device initialization failed. %s", nRc, errorString);
            break;
        }
    }

	ui->m_txtStatusMessage->setText(strMessage);
    OnMsg_UpdateDisplayResources();
    return 0;
}

int IBSU_SampleForQT::_ExecuteInitializeDevice(int nRc, int devHandle)
{
	QString strMessage;
	int		ledCount;
	DWORD	operableLEDs;
	char minSDKVersion[IBSU_MAX_STR_LEN];
    char errorString[IBSU_MAX_STR_LEN];
    int devIndex = ui->m_cboUsbDevices->currentIndex() -1;

	if(nRc >= IBSU_STATUS_OK)
    {
        m_nDevHandle = devHandle;
        
        IBSU_GetOperableLEDs(devHandle, &m_LedType, &ledCount, &operableLEDs);

		if (m_pBuffer)
			delete m_pBuffer;
			
		if (m_pScaledBuffer)
			delete m_pScaledBuffer;

		char propertyValue[IBSU_MAX_STR_LEN];
		IBSU_GetProperty(devHandle, ENUM_IBSU_PROPERTY_IMAGE_WIDTH, propertyValue);
		int width = atoi(propertyValue);
		IBSU_GetProperty(devHandle, ENUM_IBSU_PROPERTY_IMAGE_HEIGHT, propertyValue);
		int height = atoi(propertyValue);

		m_pBuffer = new unsigned char [width * height];
        m_pScaledBuffer = new unsigned char [ui->m_FrameImage->width() * ui->m_FrameImage->height() * 4];

		// register callback functions
		IBSU_RegisterCallbacks( devHandle, ENUM_IBSU_ESSENTIAL_EVENT_COMMUNICATION_BREAK, reinterpret_cast<void*>(OnEvent_DeviceCommunicationBreak), this );    
		IBSU_RegisterCallbacks( devHandle, ENUM_IBSU_ESSENTIAL_EVENT_PREVIEW_IMAGE, reinterpret_cast<void*>(OnEvent_PreviewImage), this );
		IBSU_RegisterCallbacks( devHandle, ENUM_IBSU_ESSENTIAL_EVENT_TAKING_ACQUISITION, reinterpret_cast<void*>(OnEvent_TakingAcquisition), this );  
		IBSU_RegisterCallbacks( devHandle, ENUM_IBSU_ESSENTIAL_EVENT_COMPLETE_ACQUISITION, reinterpret_cast<void*>(OnEvent_CompleteAcquisition), this );  
        IBSU_RegisterCallbacks( devHandle, ENUM_IBSU_ESSENTIAL_EVENT_RESULT_IMAGE_EX, reinterpret_cast<void*>(OnEvent_ResultImageEx), this );  
		IBSU_RegisterCallbacks( devHandle, ENUM_IBSU_OPTIONAL_EVENT_FINGER_COUNT, reinterpret_cast<void*>(OnEvent_FingerCount), this );  
		IBSU_RegisterCallbacks( devHandle, ENUM_IBSU_OPTIONAL_EVENT_FINGER_QUALITY, reinterpret_cast<void*>(OnEvent_FingerQuality), this );  
		if( ui->m_chkUseClearPlaten->isChecked() )
			IBSU_RegisterCallbacks( devHandle, ENUM_IBSU_OPTIONAL_EVENT_CLEAR_PLATEN_AT_CAPTURE, reinterpret_cast<void*>(OnEvent_ClearPlatenAtCapture), this );  
		IBSU_RegisterCallbacks( devHandle, ENUM_IBSU_OPTIONAL_EVENT_NOTIFY_MESSAGE, reinterpret_cast<void*>(OnEvent_NotifyMessage), this );  
		IBSU_RegisterCallbacks( devHandle, ENUM_IBSU_ESSENTIAL_EVENT_KEYBUTTON, reinterpret_cast<void*>(OnEvent_PressedKeyButtons), this );
    }

    if(nRc == IBSU_STATUS_OK)
    {
        OnMsg_CaptureSeqStart();
        return 0;
    }

    if(nRc > IBSU_STATUS_OK)
        OnMsg_InitWarning();
    else
    {
        switch(nRc)
        {
        case IBSU_ERR_DEVICE_ACTIVE:
			strMessage.sprintf("[Error code = %d] Device initialization failed because in use by another thread/process.", nRc);
            break;
        case IBSU_ERR_USB20_REQUIRED:
			strMessage.sprintf("[Error code = %d] Device initialization failed because SDK only works with USB 2.0.", nRc);
            break;
        case IBSU_ERR_DEVICE_HIGHER_SDK_REQUIRED:
			IBSU_GetRequiredSDKVersion(devIndex, minSDKVersion);
			strMessage.sprintf("[Error code = %d] Devcie initialization failed because SDK Version %s is required at least.", nRc, minSDKVersion );
			break;
        default:
            IBSU_GetErrorString(nRc, errorString);
            _SetStatusBarMessage("[Error code = %d] Device initialization failed. %s", nRc, errorString);
            break;
        }
    }

	ui->m_txtStatusMessage->setText(strMessage);
    OnMsg_UpdateDisplayResources();
    return 0;
}

void IBSU_SampleForQT::_DrawOverlay_ImageText(QPainter *painter)
{
	if (!m_strImageMessage.isEmpty())
	{
		QPen pen;
		if (m_bNeedClearPlaten)
			pen.setColor(Qt::red);
		else
			pen.setColor(Qt::blue);

		pen.setWidth(1);

		QFont font(QString("Arial"), 10);
		painter->setPen(pen);
		painter->setFont(font);
		painter->drawText(10, 20, m_strImageMessage);
	}
}

void IBSU_SampleForQT::_DrawOverlay_WarningOfClearPlaten(QPainter *painter, int left, int top, int width, int height)
{
	if (m_nDevHandle == -1)
		return;

    bool idle = !m_bInitializing && ( m_nCurrentCaptureStep == -1 );

    if (!idle && m_bNeedClearPlaten && m_bBlank)
    {
		QPen paintpen(Qt::red);
		paintpen.setWidth(20);

		painter->setPen(paintpen);
		painter->drawRect(left, top, width, height);
	}
}

void IBSU_SampleForQT::_DrawOverlay_DispInvaliedArea(QPainter *painter, int width, int height)
{
	bool bDrawInvalidArea = false;

	for (int i=0; i<IBSU_MAX_SEGMENT_COUNT; i++)
	{
		if (m_FingerQuality[i] == ENUM_IBSU_QUALITY_INVALID_AREA_TOP ||
			m_FingerQuality[i] == ENUM_IBSU_QUALITY_INVALID_AREA_LEFT ||
			m_FingerQuality[i] == ENUM_IBSU_QUALITY_INVALID_AREA_RIGHT)
		{
			bDrawInvalidArea = true;
		}
	}

	if (bDrawInvalidArea)
	{
		QPen	pen;
		const int arrow_width = 20;
		const int arrow_thickness = 10;
		const int arrow_pos = 30;
		const int arrow_gab = 5;

		pen.setColor(Qt::red);
		painter->setPen(pen);

		for( int i=0; i<IBSU_MAX_SEGMENT_COUNT; i++ )
		{
			if (m_FingerQuality[i] == ENUM_IBSU_QUALITY_INVALID_AREA_TOP)
			{
				QPoint aptPoly[4];

				painter->setBrush(QBrush(Qt::red, Qt::SolidPattern));

				aptPoly[0].setX(width/2);
				aptPoly[0].setY(arrow_pos);
				aptPoly[1].setX(aptPoly[0].rx() + arrow_width);
				aptPoly[1].setY(aptPoly[0].ry() - arrow_width);
				aptPoly[2].setX(aptPoly[0].rx());
				aptPoly[2].setY(aptPoly[0].ry() - arrow_thickness);
				aptPoly[3].setX(aptPoly[0].rx() - arrow_width);
				aptPoly[3].setY(aptPoly[0].ry() - arrow_width);
				painter->drawPolygon(aptPoly, 4);
				
				aptPoly[0].setX(width/2);
				aptPoly[0].setY(arrow_pos+arrow_thickness+arrow_gab);
				aptPoly[1].setX(aptPoly[0].rx() + arrow_width);
				aptPoly[1].setY(aptPoly[0].ry() - arrow_width);
				aptPoly[2].setX(aptPoly[0].rx());
				aptPoly[2].setY(aptPoly[0].ry() - arrow_thickness);
				aptPoly[3].setX(aptPoly[0].rx() - arrow_width);
				aptPoly[3].setY(aptPoly[0].ry() - arrow_width);
				painter->drawPolygon(aptPoly, 4);
			}

			if (m_FingerQuality[i] == ENUM_IBSU_QUALITY_INVALID_AREA_BOTTOM)
			{
				QPoint aptPoly[4];

				painter->setBrush(QBrush(Qt::red, Qt::SolidPattern));

				aptPoly[0].setX(width/2);
				aptPoly[0].setY(height - arrow_pos);
				aptPoly[1].setX(aptPoly[0].rx() - arrow_width);
				aptPoly[1].setY(aptPoly[0].ry() + arrow_width);
				aptPoly[2].setX(aptPoly[0].rx());
				aptPoly[2].setY(aptPoly[0].ry() + arrow_thickness);
				aptPoly[3].setX(aptPoly[0].rx() + arrow_width);
				aptPoly[3].setY(aptPoly[0].ry() + arrow_width);
				painter->drawPolygon(aptPoly, 4);

				aptPoly[0].setX(width/2);
				aptPoly[0].setY(height - arrow_thickness - arrow_gab - arrow_pos);
				aptPoly[1].setX(aptPoly[0].rx() - arrow_width);
				aptPoly[1].setY(aptPoly[0].ry() + arrow_width);
				aptPoly[2].setX(aptPoly[0].rx());
				aptPoly[2].setY(aptPoly[0].ry() + arrow_thickness);
				aptPoly[3].setX(aptPoly[0].rx() + arrow_width);
				aptPoly[3].setY(aptPoly[0].ry() + arrow_width);
				painter->drawPolygon(aptPoly, 4);
			}

			if( m_FingerQuality[i] == ENUM_IBSU_QUALITY_INVALID_AREA_LEFT )
			{
				QPoint aptPoly[4];

				painter->setBrush(QBrush(Qt::red, Qt::SolidPattern));

				aptPoly[0].setX(arrow_pos);
				aptPoly[0].setY(height/2);
				aptPoly[1].setX(aptPoly[0].rx() - arrow_width);
				aptPoly[1].setY(aptPoly[0].ry() + arrow_width);
				aptPoly[2].setX(aptPoly[0].rx() - arrow_thickness);
				aptPoly[2].setY(aptPoly[0].ry());
				aptPoly[3].setX(aptPoly[0].rx() - arrow_width);
				aptPoly[3].setY(aptPoly[0].ry() - arrow_width);
				painter->drawPolygon(aptPoly, 4);
				
				aptPoly[0].setX(arrow_pos+arrow_thickness+arrow_gab);
				aptPoly[0].setY(height/2);
				aptPoly[1].setX(aptPoly[0].rx() - arrow_width);
				aptPoly[1].setY(aptPoly[0].ry() + arrow_width);
				aptPoly[2].setX(aptPoly[0].rx() - arrow_thickness);
				aptPoly[2].setY(aptPoly[0].ry());
				aptPoly[3].setX(aptPoly[0].rx() - arrow_width);
				aptPoly[3].setY(aptPoly[0].ry() - arrow_width);
				painter->drawPolygon(aptPoly, 4);
			}

			if( m_FingerQuality[i] == ENUM_IBSU_QUALITY_INVALID_AREA_RIGHT )
			{
				QPoint aptPoly[4];

				painter->setBrush(QBrush(Qt::red, Qt::SolidPattern));

				aptPoly[0].setX(width - arrow_pos);
				aptPoly[0].setY(height/2);
				aptPoly[1].setX(aptPoly[0].rx() + arrow_width);
				aptPoly[1].setY(aptPoly[0].ry() + arrow_width);
				aptPoly[2].setX(aptPoly[0].rx() + arrow_thickness);
				aptPoly[2].setY(aptPoly[0].ry());
				aptPoly[3].setX(aptPoly[0].rx() + arrow_width);
				aptPoly[3].setY(aptPoly[0].ry() - arrow_width);
				painter->drawPolygon(aptPoly, 4);
				
				aptPoly[0].setX(width - arrow_pos-arrow_thickness-arrow_gab);
				aptPoly[0].setY(height/2);
				aptPoly[1].setX(aptPoly[0].rx() + arrow_width);
				aptPoly[1].setY(aptPoly[0].ry() + arrow_width);
				aptPoly[2].setX(aptPoly[0].rx() + arrow_thickness);
				aptPoly[2].setY(aptPoly[0].ry());
				aptPoly[3].setX(aptPoly[0].rx() + arrow_width);
				aptPoly[3].setY(aptPoly[0].ry() - arrow_width);
				painter->drawPolygon(aptPoly, 4);
			}
		}
	}
}

void IBSU_SampleForQT::_DrawOverlay_ResultSegmentImage(QPainter *painter)
{
	if (m_drawImage.IsFinal)
	{
		if (ui->m_chkDrawSegmentImage->isChecked())
		{
			// Draw quadrangle for the segment image
			double scaleFactor;
			int leftMargin = 0;
			int topMargin = 0;
			int left = 0, top = 0;
			int outWidth = ui->m_FrameImage->width();
			int outHeight = ui->m_FrameImage->height();
			int tmp_width = outWidth;
			int tmp_height = outHeight;
			int imgWidth = m_drawImage.Width;
			int imgHeight = m_drawImage.Height;
			int dispWidth, dispHeight, dispImgX, dispImgY;

			if (outWidth > imgWidth)
			{
				tmp_width = imgWidth;
				left = (outWidth-imgWidth)/2;
			}
			if (outHeight > imgHeight)
			{
				tmp_height = imgHeight;
				top = (outHeight-imgHeight)/2;
			}

			float ratio_width = (float)tmp_width / (float)imgWidth;
			float ratio_height = (float)tmp_height / (float)imgHeight;

			dispWidth = ui->m_FrameImage->width();
			dispHeight = ui->m_FrameImage->height();

			if (ratio_width >= ratio_height)
			{
				dispWidth = tmp_height * imgWidth / imgHeight;
				dispWidth -= (dispWidth % 4);
				dispHeight = tmp_height;
				dispImgX = (tmp_width - dispWidth) / 2 + left;
				dispImgY = top;
			}
			else
			{
				dispWidth = tmp_width;
				dispWidth -= (dispWidth % 4);
				dispHeight = tmp_width * imgHeight / imgWidth;
				dispImgX = left;
				dispImgY = (tmp_height - dispHeight) / 2 + top;
			}

			if (dispImgX < 0)
			{
				dispImgX = 0;
			}
			if (dispImgY < 0)
			{
				dispImgY = 0;
			}

			///////////////////////////////////////////////////////////////////////////////////
			scaleFactor = (double)dispWidth / m_drawImage.Width;
			leftMargin = dispImgX;
			topMargin = dispImgY;
			///////////////////////////////////////////////////////////////////////////////////

			for (int i=0; i<m_nSegmentImageArrayCount; i++)
			{
				QPen pen(QColor(0, 128, 0));
				int x1, x2, x3, x4, y1, y2, y3, y4;
				x1 = leftMargin + (int)(m_SegmentPositionArray[i].x1*scaleFactor);
				x2 = leftMargin + (int)(m_SegmentPositionArray[i].x2*scaleFactor);
				x3 = leftMargin + (int)(m_SegmentPositionArray[i].x3*scaleFactor);
				x4 = leftMargin + (int)(m_SegmentPositionArray[i].x4*scaleFactor);
				y1 = topMargin +  (int)(m_SegmentPositionArray[i].y1*scaleFactor);
				y2 = topMargin +  (int)(m_SegmentPositionArray[i].y2*scaleFactor);
				y3 = topMargin +  (int)(m_SegmentPositionArray[i].y3*scaleFactor);
				y4 = topMargin +  (int)(m_SegmentPositionArray[i].y4*scaleFactor);

				painter->setPen(pen);
				painter->drawLine(x1, y1, x2, y2);
				painter->drawLine(x2, y2, x3, y3);
				painter->drawLine(x3, y3, x4, y4);
				painter->drawLine(x4, y4, x1, y1);
			}
		}
	}
}

void IBSU_SampleForQT::_DrawOverlay_RollGuideLine(QPainter *painter, int width, int height)
{
	if (m_nDevHandle == -1 || m_nCurrentCaptureStep == -1)
		return;

	if (m_ImageType == ENUM_IBSU_ROLL_SINGLE_FINGER)
	{
		int nRc = IBSU_BGetRollingInfo(m_nDevHandle, &m_rollingState, &m_rollingLineX);


#ifdef __G_DEBUG__
		qDebug("m_rollingState=%d, m_rollingLineX=%d\n", m_rollingState, m_rollingLineX);
#endif
		if ( ( nRc == IBSU_STATUS_OK ) && m_rollingLineX > 0 &&
			 ( m_rollingState == ENUM_IBSU_ROLLING_TAKE_ACQUISITION ||
			   m_rollingState == ENUM_IBSU_ROLLING_COMPLETE_ACQUISITION ) )
		{
			QPen pen;
			/*double scaleFactor = (double)width / m_drawImage.Width;
			int LineX = m_rollingLineX*scaleFactor;*/
			IBSU_DeviceDesc devDesc;
   		 	devDesc.productName[0] = 0;
			double scaleFactor;
			
            const int devIndex = ui->m_cboUsbDevices->currentIndex() - 1;
			IBSU_GetDeviceDescription(devIndex, &devDesc);

			scaleFactor = (double)width / m_drawImage.Width;

		int LineX = m_rollingLineX*scaleFactor;	
#ifdef __G_DEBUG__
		qDebug("scaleFactor=%f, LineX=%d\n", scaleFactor, LineX);
#endif

			// Guide line for rolling
			if (m_rollingState == ENUM_IBSU_ROLLING_TAKE_ACQUISITION)
				pen.setColor(Qt::red);
			else if (m_rollingState == 2)
				pen.setColor(Qt::green);

			if (m_rollingLineX > -1)
			{
				pen.setWidth(2);
				painter->setPen(pen);
				painter->drawLine(LineX, 0, LineX, height);
			}
		}
	}
}

void IBSU_SampleForQT::_SetLEDs(int deviceHandle, CaptureInfo info, int ledColor, bool bBlink)
{
	quint32 setLEDs = 0;

    if (m_LedType == ENUM_IBSU_LED_TYPE_FSCAN)
    {
		if( bBlink )
		{
			if( ledColor == __LED_COLOR_GREEN__ )
			{
				setLEDs |= IBSU_LED_F_BLINK_GREEN;
			}
			else if( ledColor == __LED_COLOR_RED__ )
			{
				setLEDs |= IBSU_LED_F_BLINK_RED;
			}
			else if( ledColor == __LED_COLOR_YELLOW__ )
			{
				setLEDs |= IBSU_LED_F_BLINK_GREEN;
				setLEDs |= IBSU_LED_F_BLINK_RED;
			}
		}
	
	    if( info.ImageType == ENUM_IBSU_ROLL_SINGLE_FINGER )
	    {
	        setLEDs |= IBSU_LED_F_PROGRESS_ROLL;
	    }
	
		if( (info.fingerName == "SFF_Right_Thumb") ||
			(info.fingerName == "SRF_Right_Thumb") )
		{
			setLEDs |= IBSU_LED_F_PROGRESS_TWO_THUMB;
			if( ledColor == __LED_COLOR_GREEN__ )
			{
				setLEDs |= IBSU_LED_F_RIGHT_THUMB_GREEN;
			}
			else if( ledColor == __LED_COLOR_RED__ )
			{
				setLEDs |= IBSU_LED_F_RIGHT_THUMB_RED;
			}
			else if( ledColor == __LED_COLOR_YELLOW__ )
			{
				setLEDs |= IBSU_LED_F_RIGHT_THUMB_GREEN;
				setLEDs |= IBSU_LED_F_RIGHT_THUMB_RED;
			}
		}
		else if( (info.fingerName == "SFF_Left_Thumb") ||
			(info.fingerName == "SRF_Left_Thumb") )
		{
			setLEDs |= IBSU_LED_F_PROGRESS_TWO_THUMB;
			if( ledColor == __LED_COLOR_GREEN__ )
			{
				setLEDs |= IBSU_LED_F_LEFT_THUMB_GREEN;
			}
			else if( ledColor == __LED_COLOR_RED__ )
			{
				setLEDs |= IBSU_LED_F_LEFT_THUMB_RED;
			}
			else if( ledColor == __LED_COLOR_YELLOW__ )
			{
				setLEDs |= IBSU_LED_F_LEFT_THUMB_GREEN;
				setLEDs |= IBSU_LED_F_LEFT_THUMB_RED;
			}
		}
		else if( (info.fingerName == "TFF_2_Thumbs") )
		{
			setLEDs |= IBSU_LED_F_PROGRESS_TWO_THUMB;
			if( ledColor == __LED_COLOR_GREEN__ )
			{
				setLEDs |= IBSU_LED_F_LEFT_THUMB_GREEN;
				setLEDs |= IBSU_LED_F_RIGHT_THUMB_GREEN;
			}
			else if( ledColor == __LED_COLOR_RED__ )
			{
				setLEDs |= IBSU_LED_F_LEFT_THUMB_RED;
				setLEDs |= IBSU_LED_F_RIGHT_THUMB_RED;
			}
			else if( ledColor == __LED_COLOR_YELLOW__ )
			{
				setLEDs |= IBSU_LED_F_LEFT_THUMB_GREEN;
				setLEDs |= IBSU_LED_F_LEFT_THUMB_RED;
				setLEDs |= IBSU_LED_F_RIGHT_THUMB_GREEN;
				setLEDs |= IBSU_LED_F_RIGHT_THUMB_RED;
			}
		}
		///////////////////LEFT HAND////////////////////
		else if( (info.fingerName == "SFF_Left_Index") ||
			(info.fingerName == "SRF_Left_Index") )
		{
			setLEDs |= IBSU_LED_F_PROGRESS_LEFT_HAND;
			if( ledColor == __LED_COLOR_GREEN__ )
			{
				setLEDs |= IBSU_LED_F_LEFT_INDEX_GREEN;
			}
			else if( ledColor == __LED_COLOR_RED__ )
			{
				setLEDs |= IBSU_LED_F_LEFT_INDEX_RED;
			}
			else if( ledColor == __LED_COLOR_YELLOW__ )
			{
				setLEDs |= IBSU_LED_F_LEFT_INDEX_GREEN;
				setLEDs |= IBSU_LED_F_LEFT_INDEX_RED;
			}
		}
		else if( (info.fingerName == "SFF_Left_Middle") ||
			(info.fingerName == "SRF_Left_Middle") )
		{
			setLEDs |= IBSU_LED_F_PROGRESS_LEFT_HAND;
			if( ledColor == __LED_COLOR_GREEN__ )
			{
				setLEDs |= IBSU_LED_F_LEFT_MIDDLE_GREEN;
			}
			else if( ledColor == __LED_COLOR_RED__ )
			{
				setLEDs |= IBSU_LED_F_LEFT_MIDDLE_RED;
			}
			else if( ledColor == __LED_COLOR_YELLOW__ )
			{
				setLEDs |= IBSU_LED_F_LEFT_MIDDLE_GREEN;
				setLEDs |= IBSU_LED_F_LEFT_MIDDLE_RED;
			}
		}
		else if( (info.fingerName == "SFF_Left_Ring") ||
			(info.fingerName == "SRF_Left_Ring") )
		{
			setLEDs |= IBSU_LED_F_PROGRESS_LEFT_HAND;
			if( ledColor == __LED_COLOR_GREEN__ )
			{
				setLEDs |= IBSU_LED_F_LEFT_RING_GREEN;
			}
			else if( ledColor == __LED_COLOR_RED__ )
			{
				setLEDs |= IBSU_LED_F_LEFT_RING_RED;
			}
			else if( ledColor == __LED_COLOR_YELLOW__ )
			{
				setLEDs |= IBSU_LED_F_LEFT_RING_GREEN;
				setLEDs |= IBSU_LED_F_LEFT_RING_RED;
			}
		}
		else if( (info.fingerName == "SFF_Left_Little") ||
			(info.fingerName == "SRF_Left_Little") )
		{
			setLEDs |= IBSU_LED_F_PROGRESS_LEFT_HAND;
			if( ledColor == __LED_COLOR_GREEN__ )
			{
				setLEDs |= IBSU_LED_F_LEFT_LITTLE_GREEN;
			}
			else if( ledColor == __LED_COLOR_RED__ )
			{
				setLEDs |= IBSU_LED_F_LEFT_LITTLE_RED;
			}
			else if( ledColor == __LED_COLOR_YELLOW__ )
			{
				setLEDs |= IBSU_LED_F_LEFT_LITTLE_GREEN;
				setLEDs |= IBSU_LED_F_LEFT_LITTLE_RED;
			}
		}
		else if( (info.fingerName == "4FF_Left_4_Fingers") )
		{
			setLEDs |= IBSU_LED_F_PROGRESS_LEFT_HAND;
			if( ledColor == __LED_COLOR_GREEN__ )
			{
				setLEDs |= IBSU_LED_F_LEFT_INDEX_GREEN;
				setLEDs |= IBSU_LED_F_LEFT_MIDDLE_GREEN;
				setLEDs |= IBSU_LED_F_LEFT_RING_GREEN;
				setLEDs |= IBSU_LED_F_LEFT_LITTLE_GREEN;
			}
			else if( ledColor == __LED_COLOR_RED__ )
			{
				setLEDs |= IBSU_LED_F_LEFT_INDEX_RED;
				setLEDs |= IBSU_LED_F_LEFT_MIDDLE_RED;
				setLEDs |= IBSU_LED_F_LEFT_RING_RED;
				setLEDs |= IBSU_LED_F_LEFT_LITTLE_RED;
			}
			else if( ledColor == __LED_COLOR_YELLOW__ )
			{
				setLEDs |= IBSU_LED_F_LEFT_INDEX_GREEN;
				setLEDs |= IBSU_LED_F_LEFT_MIDDLE_GREEN;
				setLEDs |= IBSU_LED_F_LEFT_RING_GREEN;
				setLEDs |= IBSU_LED_F_LEFT_LITTLE_GREEN;
				setLEDs |= IBSU_LED_F_LEFT_INDEX_RED;
				setLEDs |= IBSU_LED_F_LEFT_MIDDLE_RED;
				setLEDs |= IBSU_LED_F_LEFT_RING_RED;
				setLEDs |= IBSU_LED_F_LEFT_LITTLE_RED;
			}
		}
		///////////RIGHT HAND /////////////////////////
		else if( (info.fingerName == "SFF_Right_Index") ||
			(info.fingerName == "SRF_Right_Index") )
		{
			setLEDs |= IBSU_LED_F_PROGRESS_RIGHT_HAND;
			if( ledColor == __LED_COLOR_GREEN__ )
			{
				setLEDs |= IBSU_LED_F_RIGHT_INDEX_GREEN;
			}
			else if( ledColor == __LED_COLOR_RED__ )
			{
				setLEDs |= IBSU_LED_F_RIGHT_INDEX_RED;
			}
			else if( ledColor == __LED_COLOR_YELLOW__ )
			{
				setLEDs |= IBSU_LED_F_RIGHT_INDEX_GREEN;
				setLEDs |= IBSU_LED_F_RIGHT_INDEX_RED;
			}
		}
		else if( (info.fingerName == "SFF_Right_Middle") ||
			(info.fingerName == "SRF_Right_Middle") )
		{
			setLEDs |= IBSU_LED_F_PROGRESS_RIGHT_HAND;
			if( ledColor == __LED_COLOR_GREEN__ )
			{
				setLEDs |= IBSU_LED_F_RIGHT_MIDDLE_GREEN;
			}
			else if( ledColor == __LED_COLOR_RED__ )
			{
				setLEDs |= IBSU_LED_F_RIGHT_MIDDLE_RED;
			}
			else if( ledColor == __LED_COLOR_YELLOW__ )
			{
				setLEDs |= IBSU_LED_F_RIGHT_MIDDLE_GREEN;
				setLEDs |= IBSU_LED_F_RIGHT_MIDDLE_RED;
			}
		}
		else if( (info.fingerName == "SFF_Right_Ring") ||
			(info.fingerName == "SRF_Right_Ring") )
		{
			setLEDs |= IBSU_LED_F_PROGRESS_RIGHT_HAND;
			if( ledColor == __LED_COLOR_GREEN__ )
			{
				setLEDs |= IBSU_LED_F_RIGHT_RING_GREEN;
			}
			else if( ledColor == __LED_COLOR_RED__ )
			{
				setLEDs |= IBSU_LED_F_RIGHT_RING_RED;
			}
			else if( ledColor == __LED_COLOR_YELLOW__ )
			{
				setLEDs |= IBSU_LED_F_RIGHT_RING_GREEN;
				setLEDs |= IBSU_LED_F_RIGHT_RING_RED;
			}
		}
		else if( (info.fingerName == "SFF_Right_Little") ||
			(info.fingerName == "SRF_Right_Little") )
		{
			setLEDs |= IBSU_LED_F_PROGRESS_RIGHT_HAND;
			if( ledColor == __LED_COLOR_GREEN__ )
			{
				setLEDs |= IBSU_LED_F_RIGHT_LITTLE_GREEN;
			}
			else if( ledColor == __LED_COLOR_RED__ )
			{
				setLEDs |= IBSU_LED_F_RIGHT_LITTLE_RED;
			}
			else if( ledColor == __LED_COLOR_YELLOW__ )
			{
				setLEDs |= IBSU_LED_F_RIGHT_LITTLE_GREEN;
				setLEDs |= IBSU_LED_F_RIGHT_LITTLE_RED;
			}
		}
		else if( (info.fingerName == "4FF_Right_4_Fingers") )
		{
			setLEDs |= IBSU_LED_F_PROGRESS_RIGHT_HAND;
			if( ledColor == __LED_COLOR_GREEN__ )
			{
				setLEDs |= IBSU_LED_F_RIGHT_INDEX_GREEN;
				setLEDs |= IBSU_LED_F_RIGHT_MIDDLE_GREEN;
				setLEDs |= IBSU_LED_F_RIGHT_RING_GREEN;
				setLEDs |= IBSU_LED_F_RIGHT_LITTLE_GREEN;
			}
			else if( ledColor == __LED_COLOR_RED__ )
			{
				setLEDs |= IBSU_LED_F_RIGHT_INDEX_RED;
				setLEDs |= IBSU_LED_F_RIGHT_MIDDLE_RED;
				setLEDs |= IBSU_LED_F_RIGHT_RING_RED;
				setLEDs |= IBSU_LED_F_RIGHT_LITTLE_RED;
			}
			else if( ledColor == __LED_COLOR_YELLOW__ )
			{
				setLEDs |= IBSU_LED_F_RIGHT_INDEX_GREEN;
				setLEDs |= IBSU_LED_F_RIGHT_MIDDLE_GREEN;
				setLEDs |= IBSU_LED_F_RIGHT_RING_GREEN;
				setLEDs |= IBSU_LED_F_RIGHT_LITTLE_GREEN;
				setLEDs |= IBSU_LED_F_RIGHT_INDEX_RED;
				setLEDs |= IBSU_LED_F_RIGHT_MIDDLE_RED;
				setLEDs |= IBSU_LED_F_RIGHT_RING_RED;
				setLEDs |= IBSU_LED_F_RIGHT_LITTLE_RED;
			}
		}
		
		if (ledColor == __LED_COLOR_NONE__)
		{
			setLEDs = 0;
		}
		
		IBSU_SetLEDs(deviceHandle, setLEDs);
	}
}




/////////////////////////////////////////////////////////////////////////////
void IBSU_SampleForQT::OnEvent_DeviceCommunicationBreak(
						 const int deviceHandle,
						 void*     pContext
					   )
{
    if( pContext == NULL )
        return;

    IBSU_SampleForQT *pDlg = reinterpret_cast<IBSU_SampleForQT*>(pContext);
	QMutexLocker locker(&m_mutex);

	pDlg->OnMsg_DeviceCommunicationBreak();
}

void IBSU_SampleForQT::OnEvent_PreviewImage(
						 const int deviceHandle,
						 void*     pContext,
						 const	   IBSU_ImageData image
					   )
{
    if( pContext == NULL )
        return;

    IBSU_SampleForQT *pDlg = reinterpret_cast<IBSU_SampleForQT*>(pContext);
	QMutexLocker locker(&m_mutex);

    m_drawImage = image;
	memcpy(m_pBuffer, image.Buffer, image.Width * image.Height);
	m_drawImage.Buffer = m_pBuffer;
    pDlg->m_bPaintEvent = true;
	QMetaObject::invokeMethod(pDlg, "repaint", Qt::QueuedConnection);
}

void IBSU_SampleForQT::OnEvent_FingerCount(
						   const int                   deviceHandle,
						   void*                       pContext,
						   const IBSU_FingerCountState fingerCountState
						 )
{
    if( pContext == NULL )
        return;

    IBSU_SampleForQT *pDlg = reinterpret_cast<IBSU_SampleForQT*>(pContext);
	QMutexLocker locker(&m_mutex);
	
	CaptureInfo info = pDlg->m_vecCaptureSeq[pDlg->m_nCurrentCaptureStep];

	if(fingerCountState == ENUM_IBSU_NON_FINGER)
	{
		pDlg->_SetLEDs(deviceHandle, info, __LED_COLOR_RED__, true);
	}
	else
	{
		pDlg->_SetLEDs(deviceHandle, info, __LED_COLOR_YELLOW__, true);
	}
}

void IBSU_SampleForQT::OnEvent_FingerQuality(
                          const int                     deviceHandle,   
                          void                          *pContext,       
                          const IBSU_FingerQualityState *pQualityArray, 
                          const int                     qualityArrayCount    
						 )
{
    if( pContext == NULL )
        return;

    IBSU_SampleForQT *pDlg = reinterpret_cast<IBSU_SampleForQT*>(pContext);
	QMutexLocker locker(&m_mutex);

	memcpy(pDlg->m_FingerQuality, pQualityArray, sizeof(IBSU_FingerQualityState)*qualityArrayCount);
	pDlg->OnMsg_DrawFingerQuality();
}

void IBSU_SampleForQT::OnEvent_DeviceCount(
						 const int detectedDevices,
						 void      *pContext
					   )
{
    if( pContext == NULL )
        return;

    IBSU_SampleForQT *pDlg = reinterpret_cast<IBSU_SampleForQT*>(pContext);
	QMutexLocker locker(&m_mutex);

	pDlg->OnMsg_UpdateDeviceList();
}

void IBSU_SampleForQT::OnEvent_InitProgress(
						 const int deviceIndex,
						 void      *pContext,
						 const int progressValue
					   )
{
    if( pContext == NULL )
        return;

    IBSU_SampleForQT *pDlg = reinterpret_cast<IBSU_SampleForQT*>(pContext);
	QMutexLocker locker(&m_mutex);

	pDlg->_SetStatusBarMessage("Initializing device... %d%%", progressValue);
}

void IBSU_SampleForQT::OnEvent_TakingAcquisition(
						 const int				deviceHandle,
						 void					*pContext,
						 const IBSU_ImageType	imageType
					   )
{
    if( pContext == NULL )
        return;

    IBSU_SampleForQT *pDlg = reinterpret_cast<IBSU_SampleForQT*>(pContext);
	QMutexLocker locker(&m_mutex);

	if (imageType == ENUM_IBSU_ROLL_SINGLE_FINGER)
	{
		pDlg->_BeepOk();
		pDlg->_SetImageMessage("When done remove finger from sensor");
		pDlg->_SetStatusBarMessage("When done remove finger from sensor");
	}
}

void IBSU_SampleForQT::OnEvent_CompleteAcquisition(
						 const int				deviceHandle,
						 void					*pContext,
						 const IBSU_ImageType	imageType
					   )
{
    if( pContext == NULL )
        return;

    IBSU_SampleForQT *pDlg = reinterpret_cast<IBSU_SampleForQT*>(pContext);
	QMutexLocker locker(&m_mutex);

	if (imageType == ENUM_IBSU_ROLL_SINGLE_FINGER)
	{
		pDlg->_BeepOk();
	}
	else
	{
		pDlg->_BeepSuccess();
		pDlg->_SetImageMessage("Remove fingers from sensor");
		pDlg->_SetStatusBarMessage("Acquisition completed, postprocessing..");
		IBSU_RedrawClientWindow(deviceHandle); 
	}
}

void IBSU_SampleForQT::OnEvent_ResultImageEx(
                          const int                   deviceHandle,
                          void                        *pContext,
                          const int                   imageStatus,
                          const IBSU_ImageData        image,
						  const IBSU_ImageType        imageType,
						  const int                   detectedFingerCount,
                          const int                   segmentImageArrayCount,
                          const IBSU_ImageData        *pSegmentImageArray,
						  const IBSU_SegmentPosition  *pSegmentPositionArray
                        )
{
    if( pContext == NULL )
        return;

    IBSU_SampleForQT *pDlg = reinterpret_cast<IBSU_SampleForQT*>(pContext);
	QMutexLocker locker(&m_mutex);

	if (deviceHandle != pDlg->m_nDevHandle )
		return;

    if (imageStatus >= IBSU_STATUS_OK)
    {
		if (imageType == ENUM_IBSU_ROLL_SINGLE_FINGER)
		{
			pDlg->_BeepSuccess();
		}
	}

	if (pDlg->m_bNeedClearPlaten)
	{
		pDlg->m_bNeedClearPlaten = FALSE;
	}

    IBSU_GetIBSM_ResultImageInfo(deviceHandle, pDlg->m_vecCaptureSeq[pDlg->m_nCurrentCaptureStep].fingerPosition, 
								&pDlg->m_CapturedImg, pDlg->m_CapturedImgSplit, &pDlg->m_CapturedImgSplitCnt);

    char imgTypeName[IBSU_MAX_STR_LEN]={0};
    switch( imageType )
    {
    case ENUM_IBSU_ROLL_SINGLE_FINGER:
	    qstrcpy(imgTypeName, "-- Rolling single finger --"); break;
    case ENUM_IBSU_FLAT_SINGLE_FINGER:
	    qstrcpy(imgTypeName, "-- Flat single finger --"); break;
    case ENUM_IBSU_FLAT_TWO_FINGERS:
	    qstrcpy(imgTypeName, "-- Flat two fingers --"); break;
    case ENUM_IBSU_FLAT_FOUR_FINGERS:
	    qstrcpy(imgTypeName, "-- Flat 4 fingers --"); break;
    default:
	    qstrcpy(imgTypeName, "-- Unknown --"); break;
    }

    if (imageStatus >= IBSU_STATUS_OK)
    {
	    // Image acquisition successful
	    CaptureInfo info = pDlg->m_vecCaptureSeq[pDlg->m_nCurrentCaptureStep];
		pDlg->_SetLEDs(deviceHandle, info, __LED_COLOR_GREEN__, false);

		if (pDlg->ui->m_chkSaveImges->isChecked())
	    {
		    pDlg->_SetStatusBarMessage("Saving image...");
		    CaptureInfo info = pDlg->m_vecCaptureSeq[pDlg->m_nCurrentCaptureStep];
		    pDlg->_SaveBitmapImage(image, info.fingerName);
		    pDlg->_SaveWsqImage(image, info.fingerName);
		    pDlg->_SavePngImage(image, info.fingerName);
		    pDlg->_SaveJP2Image(image, info.fingerName);
		    if (segmentImageArrayCount > 0)
		    {
			    QString			segmentName;
				QByteArray		byteValue;
				char			*cValue;

			    for (int i=0; i<segmentImageArrayCount; i++)
			    {
					byteValue = info.fingerName.toLocal8Bit();
					cValue = byteValue.data();
					segmentName.sprintf("%s_Segment_%02d", cValue, i);
				    pDlg->_SaveBitmapImage(*(pSegmentImageArray+i), segmentName);
				    pDlg->_SaveWsqImage(*(pSegmentImageArray+i), segmentName);
				    pDlg->_SavePngImage(*(pSegmentImageArray+i), segmentName);
				    pDlg->_SaveJP2Image(*(pSegmentImageArray+i), segmentName);
			    }
		    }

            // Save ISO image & template 
            pDlg->_SaveISOImage(image, info.fingerName);
	    }

		if (pDlg->ui->m_chkDrawSegmentImage->isChecked())
		{
			pDlg->m_nSegmentImageArrayCount = segmentImageArrayCount;
			memcpy(&pDlg->m_SegmentPositionArray[0], pSegmentPositionArray, sizeof(IBSU_SegmentPosition)*segmentImageArrayCount);
		}
		/////
	    if (pDlg->ui->m_chkNFIQScore->isChecked())
	    {
			int nfiq_score[IBSU_MAX_SEGMENT_COUNT];
			int	score=0, nRc, segment_pos=0;
			memset(&nfiq_score, 0, sizeof(nfiq_score));
			QString strValue = "Err";
			pDlg->_SetStatusBarMessage("Get NFIQ score...");
			for (int i=0; i<IBSU_MAX_SEGMENT_COUNT; i++)
			{
				if (pDlg->m_FingerQuality[i] == ENUM_IBSU_FINGER_NOT_PRESENT)
					continue;

				nRc = IBSU_GetNFIQScore(deviceHandle, (const BYTE*)(pSegmentImageArray+segment_pos)->Buffer,
					(pSegmentImageArray+segment_pos)->Width, (pSegmentImageArray+segment_pos)->Height,
					(pSegmentImageArray+segment_pos)->BitsPerPixel, &score);
				if (nRc == IBSU_STATUS_OK)
					nfiq_score[i] = score;
				else
					nfiq_score[i] = -1;

				segment_pos++;
			}
			strValue.sprintf("%d-%d-%d-%d", nfiq_score[0], nfiq_score[1], nfiq_score[2], nfiq_score[3]);
			QMetaObject::invokeMethod(pDlg->ui->m_txtNFIQScore, "setText", Qt::QueuedConnection, Q_ARG(QString, strValue));
	    }
		
		//Spoof result
		if (pDlg->ui->m_chkEnableSpoof->isChecked())
	    {
			//int nfiq_score[IBSU_MAX_SEGMENT_COUNT];
			QString isSpoofStr[4];
			BOOL isSpoof;
			int	nRc, segment_pos=0;
			QString strValue;
			pDlg->_SetStatusBarMessage("Get Spoof Result...");
			for (int i=0; i<segmentImageArrayCount; i++)
			{
				nRc = IBSU_IsSpoofFingerDetected(deviceHandle,pSegmentImageArray[i],&isSpoof);
				if(nRc != IBSU_STATUS_OK)
				{
					strValue = "Error";
					QMetaObject::invokeMethod(pDlg->ui->m_txtSpoofResult, "setText", Qt::QueuedConnection, Q_ARG(QString, strValue));
					
					char errorString[IBSU_MAX_STR_LEN];
					IBSU_GetErrorString(nRc, errorString);
					
					sprintf(errorString, "%s (Error code = %d)", errorString, nRc);
					pDlg->_SetImageMessage(errorString);
					pDlg->_SetStatusBarMessage(errorString);

					// Stop all of acquisition
					pDlg->m_nCurrentCaptureStep = (int)pDlg->m_vecCaptureSeq.size();
					
					pDlg->OnMsg_CaptureSeqNext();
					return;
				}
				
				if (isSpoof == TRUE)
					isSpoofStr[i] = "FAKE";
				else
					isSpoofStr[i] = "LIVE";
			}	
			//strValue.sprintf("%s-%s-%s-%s", nfiq_score[0], nfiq_score[1], nfiq_score[2], nfiq_score[3]);
			if (segmentImageArrayCount == 1)
			{
				strValue = QString("%1").arg(isSpoofStr[0]);
			}
			if (segmentImageArrayCount == 2)
			{
				strValue = QString("%1-%2").arg(isSpoofStr[0]).arg(isSpoofStr[1]);
			}				
			if (segmentImageArrayCount == 4)
			{
				strValue = QString("%1-%2-%3-%4").arg(isSpoofStr[0]).arg(isSpoofStr[1]).arg(isSpoofStr[2]).arg(isSpoofStr[3]);
			}
			QMetaObject::invokeMethod(pDlg->ui->m_txtSpoofResult, "setText", Qt::QueuedConnection, Q_ARG(QString, strValue));
	    }

		if( imageStatus == IBSU_STATUS_OK )
        {
	        pDlg->_SetImageMessage("%s acquisition completed successfully", imgTypeName);
	        pDlg->_SetStatusBarMessage("%s acquisition completed successfully", imgTypeName);
        }
        else
        {
            // > IBSU_STATUS_OK
	        pDlg->_SetImageMessage("%s acquisition Warning (Warning code = %d)", imgTypeName, imageStatus);
	        pDlg->_SetStatusBarMessage("%s acquisition Warning (Warning code = %d)", imgTypeName, imageStatus);

			m_drawImage = image;
			memcpy(m_pBuffer, image.Buffer, image.Width * image.Height);
			m_drawImage.Buffer = m_pBuffer;
            
			pDlg->OnMsg_AskRecapture(imageStatus);
			return;
        }
    }
    else
    {
        // < IBSU_STATUS_OK
	    pDlg->_SetImageMessage("%s acquisition failed (Error code = %d)", imgTypeName, imageStatus);
	    pDlg->_SetStatusBarMessage("%s acquisition failed (Error code = %d)", imgTypeName, imageStatus);

        // Stop all of acquisition
        pDlg->m_nCurrentCaptureStep = (int)pDlg->m_vecCaptureSeq.size();
    }

    m_drawImage = image;
	memcpy(m_pBuffer, image.Buffer, image.Width * image.Height);
	m_drawImage.Buffer = m_pBuffer;
    pDlg->m_bPaintEvent = true;
	QMetaObject::invokeMethod(pDlg, "repaint", Qt::QueuedConnection);

    pDlg->OnMsg_CaptureSeqNext();
}

void IBSU_SampleForQT::OnEvent_ClearPlatenAtCapture(
                          const int                   deviceHandle,
                          void                        *pContext,
                          const IBSU_PlatenState      platenState
                        )
{
    if( pContext == NULL )
        return;

    IBSU_SampleForQT *pDlg = reinterpret_cast<IBSU_SampleForQT*>(pContext);
	QMutexLocker locker(&m_mutex);

	if (platenState == ENUM_IBSU_PLATEN_HAS_FINGERS)
		pDlg->m_bNeedClearPlaten = true;
	else
		pDlg->m_bNeedClearPlaten = false;

	if (pDlg->m_bNeedClearPlaten)
	{
		pDlg->_SetImageMessage("Please remove your fingers on the platen first!");
		pDlg->_SetStatusBarMessage("Please remove your fingers on the platen first!");
	}
	else
	{
		CaptureInfo info = pDlg->m_vecCaptureSeq[pDlg->m_nCurrentCaptureStep];

		// Display message for image acuisition again
		QString strMessage;
		QByteArray byteMessage;
		char *cMessage;
		strMessage = info.PreCaptureMessage;
		byteMessage = strMessage.toLocal8Bit();
		cMessage = byteMessage.data();

		pDlg->_SetStatusBarMessage("%s", cMessage);
		if (!pDlg->ui->m_chkAutoCapture->checkState())
			strMessage += QString("\r\nPress button 'Take Result Image' when image is good!");

		byteMessage = strMessage.toLocal8Bit();
		cMessage = byteMessage.data();
		pDlg->_SetImageMessage("%s", cMessage);
	}
}

void IBSU_SampleForQT::OnEvent_AsyncOpenDevice(
                          const int                   deviceIndex,
                          void                        *pContext,
                          const int                   deviceHandle,
                          const int                   errorCode
                        )
{
    if( pContext == NULL )
        return;

    IBSU_SampleForQT *pDlg = reinterpret_cast<IBSU_SampleForQT*>(pContext);
	QMutexLocker locker(&m_mutex);

	pDlg->_ExecuteInitializeDevice(errorCode, deviceHandle);
}

void IBSU_SampleForQT::OnEvent_NotifyMessage(
                          const int                deviceHandle,
                          void                     *pContext,
                          const int                message
                        )
{
    if( pContext == NULL )
        return;

//    IBSU_SampleForQT *pDlg = reinterpret_cast<IBSU_SampleForQT*>(pContext);
	QMutexLocker locker(&m_mutex);

#ifdef __G_DEBUG__
	qDebug("OnEvent_NotifyMessage = %d\n", message);
#endif
}

void IBSU_SampleForQT::OnEvent_PressedKeyButtons(
                          const int                deviceHandle,
                          void                     *pContext,
                          const int                pressedKeyButtons
						  )
{
	if( pContext == NULL )
		return;

    IBSU_SampleForQT *pDlg = reinterpret_cast<IBSU_SampleForQT*>(pContext);
	QMutexLocker locker(&m_mutex);

#ifdef __G_DEBUG__
	qDebug("OnEvent_PressedKeyButtons = %d\n", pressedKeyButtons);
#endif

	pDlg->OnMsg_GetSelectDevice();
    BOOL idle = !pDlg->m_bInitializing && ( pDlg->m_nCurrentCaptureStep == -1 );
	BOOL active = !pDlg->m_bInitializing && (pDlg->m_nCurrentCaptureStep != -1 );
    if( pressedKeyButtons == __LEFT_KEY_BUTTON__ )
    {
        if (pDlg->m_bSelectDev && idle)
        {
        	IBSU_SetBeeper(deviceHandle, ENUM_IBSU_BEEP_PATTERN_GENERIC, 2/*Sol*/, 4/*100ms = 4*25ms*/, 0, 0);
			pDlg->OnBnClickedBtnCaptureStart();
        }
    }
    else if( pressedKeyButtons == __RIGHT_KEY_BUTTON__ )
    {
        if ( (active) )
        {
        	IBSU_SetBeeper(deviceHandle, ENUM_IBSU_BEEP_PATTERN_GENERIC, 2/*Sol*/, 4/*100ms = 4*25ms*/, 0, 0);
			pDlg->OnBnClickedBtnCaptureStop();
        }
    }
}

////////////////////////////////////////////////////////////////////////////////////////////


void IBSU_SampleForQT::OnMsg_GetSelectDevice()
{
	if (QThread::currentThread() != this->thread())
	{
		// not sure how efficient it is
		QMetaObject::invokeMethod(this, "OnMsg_GetSelectDevice",
			Qt::QueuedConnection);
		return;
	}

    m_bSelectDev = ui->m_cboUsbDevices->currentIndex() > 0;
	return;
}




void IBSU_SampleForQT::OnMsg_CaptureSeqStart()
{
	if (QThread::currentThread() != this->thread())
	{
		// not sure how efficient it is
		QMetaObject::invokeMethod(this, "OnMsg_CaptureSeqStart",
			Qt::QueuedConnection);
		return;
	}

    if(m_nDevHandle == -1)
    {
        OnMsg_UpdateDisplayResources();
        return;
    }

    QString strCaptureSeq;
    int nSelectedSeq;
    nSelectedSeq = ui->m_cboCaptureSeq->currentIndex();
    if(nSelectedSeq > -1)
        strCaptureSeq = ui->m_cboCaptureSeq->currentText();

    m_vecCaptureSeq.clear();
    CaptureInfo info;

    if(strCaptureSeq == CAPTURE_SEQ_FLAT_SINGLE_FINGER)
    {
        info.PreCaptureMessage = "Please put a single finger on the sensor!";
        info.PostCaptuerMessage = "Keep finger on the sensor!";
        info.ImageType = ENUM_IBSU_FLAT_SINGLE_FINGER;
        info.NumberOfFinger = 1;
        info.fingerName = "SFF_Unknown";
		info.fingerPosition = IBSM_FINGER_POSITION_UNKNOWN;
        m_vecCaptureSeq.push_back(info);
    }

    if( strCaptureSeq == CAPTURE_SEQ_ROLL_SINGLE_FINGER )
    {
        info.PreCaptureMessage = "Please put a single finger on the sensor!";
        info.PostCaptuerMessage = "Roll finger!";
        info.ImageType = ENUM_IBSU_ROLL_SINGLE_FINGER;
        info.NumberOfFinger = 1;
        info.fingerName = "SRF_Unknown";
		info.fingerPosition = IBSM_FINGER_POSITION_UNKNOWN;
        m_vecCaptureSeq.push_back(info);
    }

    if( strCaptureSeq == CAPTURE_SEQ_2_FLAT_FINGERS )
    {
        info.PreCaptureMessage = "Please put two fingers on the sensor!";
        info.PostCaptuerMessage = "Keep fingers on the sensor!";
        info.ImageType = ENUM_IBSU_FLAT_TWO_FINGERS;
        info.NumberOfFinger = 2;
        info.fingerName = "TFF_Unknown";
		info.fingerPosition = IBSM_FINGER_POSITION_UNKNOWN;
        m_vecCaptureSeq.push_back(info);
    }

    if( strCaptureSeq == CAPTURE_SEQ_10_SINGLE_FLAT_FINGERS )
    {
        info.PreCaptureMessage = "Please put right thumb on the sensor!";
        info.fingerName = "SFF_Right_Thumb";
        info.PostCaptuerMessage = "Keep fingers on the sensor!";
        info.ImageType = ENUM_IBSU_FLAT_SINGLE_FINGER;
        info.NumberOfFinger = 1;
 		info.fingerPosition = IBSM_FINGER_POSITION_RIGHT_THUMB;
        m_vecCaptureSeq.push_back(info);

        info.PreCaptureMessage = "Please put right index on the sensor!";
        info.fingerName = "SFF_Right_Index";
		info.fingerPosition = IBSM_FINGER_POSITION_RIGHT_INDEX_FINGER;
        m_vecCaptureSeq.push_back(info);

        info.PreCaptureMessage = "Please put right middle on the sensor!";
        info.fingerName = "SFF_Right_Middle";
		info.fingerPosition = IBSM_FINGER_POSITION_RIGHT_MIDDLE_FINGER;
        m_vecCaptureSeq.push_back(info);

        info.PreCaptureMessage = "Please put right ring on the sensor!";
        info.fingerName = "SFF_Right_Ring";
		info.fingerPosition = IBSM_FINGER_POSITION_RIGHT_RING_FINGER;
		m_vecCaptureSeq.push_back(info);

        info.PreCaptureMessage = "Please put right little on the sensor!";
        info.fingerName = "SFF_Right_Little";
		info.fingerPosition = IBSM_FINGER_POSITION_RIGHT_LITTLE_FINGER;
		m_vecCaptureSeq.push_back(info);

        info.PreCaptureMessage = "Please put left thumb on the sensor!";
        info.fingerName = "SFF_Left_Thumb";
		info.fingerPosition = IBSM_FINGER_POSITION_LEFT_THUMB;
		m_vecCaptureSeq.push_back(info);

        info.PreCaptureMessage = "Please put left index on the sensor!";
        info.fingerName = "SFF_Left_Index";
		info.fingerPosition = IBSM_FINGER_POSITION_LEFT_INDEX_FINGER;
		m_vecCaptureSeq.push_back(info);

        info.PreCaptureMessage = "Please put left middle on the sensor!";
        info.fingerName = "SFF_Left_Middle";
		info.fingerPosition = IBSM_FINGER_POSITION_LEFT_MIDDLE_FINGER;
		m_vecCaptureSeq.push_back(info);

        info.PreCaptureMessage = "Please put left ring on the sensor!";
        info.fingerName = "SFF_Left_Ring";
		info.fingerPosition = IBSM_FINGER_POSITION_LEFT_RING_FINGER;
		m_vecCaptureSeq.push_back(info);

        info.PreCaptureMessage = "Please put left little on the sensor!";
        info.fingerName = "SFF_Left_Little";
		info.fingerPosition = IBSM_FINGER_POSITION_LEFT_LITTLE_FINGER;
		m_vecCaptureSeq.push_back(info);
    }

    if( strCaptureSeq == CAPTURE_SEQ_10_SINGLE_ROLLED_FINGERS )
    {
        info.PreCaptureMessage = "Please put right thumb on the sensor!";
        info.PostCaptuerMessage = "Roll finger!";
        info.ImageType = ENUM_IBSU_ROLL_SINGLE_FINGER;
        info.NumberOfFinger = 1;
        info.fingerName = "SRF_Right_Thumb";
		info.fingerPosition = IBSM_FINGER_POSITION_RIGHT_THUMB;
		m_vecCaptureSeq.push_back(info);

        info.PreCaptureMessage = "Please put right index on the sensor!";
        info.fingerName = "SRF_Right_Index";
		info.fingerPosition = IBSM_FINGER_POSITION_RIGHT_INDEX_FINGER;
		m_vecCaptureSeq.push_back(info);

        info.PreCaptureMessage = "Please put right middle on the sensor!";
        info.fingerName = "SRF_Right_Middle";
		info.fingerPosition = IBSM_FINGER_POSITION_RIGHT_MIDDLE_FINGER;
		m_vecCaptureSeq.push_back(info);

        info.PreCaptureMessage = "Please put right ring on the sensor!";
        info.fingerName = "SRF_Right_Ring";
		info.fingerPosition = IBSM_FINGER_POSITION_RIGHT_RING_FINGER;
		m_vecCaptureSeq.push_back(info);

        info.PreCaptureMessage = "Please put right little on the sensor!";
        info.fingerName = "SRF_Right_Little";
		info.fingerPosition = IBSM_FINGER_POSITION_RIGHT_LITTLE_FINGER;
		m_vecCaptureSeq.push_back(info);

        info.PreCaptureMessage = "Please put left thumb on the sensor!";
        info.fingerName = "SRF_Left_Thumb";
		info.fingerPosition = IBSM_FINGER_POSITION_LEFT_THUMB;
		m_vecCaptureSeq.push_back(info);

        info.PreCaptureMessage = "Please put left index on the sensor!";
        info.fingerName = "SRF_Left_Index";
		info.fingerPosition = IBSM_FINGER_POSITION_LEFT_INDEX_FINGER;
		m_vecCaptureSeq.push_back(info);

        info.PreCaptureMessage = "Please put left middle on the sensor!";
        info.fingerName = "SRF_Left_Middle";
		info.fingerPosition = IBSM_FINGER_POSITION_LEFT_MIDDLE_FINGER;
		m_vecCaptureSeq.push_back(info);

        info.PreCaptureMessage = "Please put left ring on the sensor!";
        info.fingerName = "SRF_Left_Ring";
		info.fingerPosition = IBSM_FINGER_POSITION_LEFT_RING_FINGER;
		m_vecCaptureSeq.push_back(info);

        info.PreCaptureMessage = "Please put left little on the sensor!";
        info.fingerName = "SRF_Left_Little";
		info.fingerPosition = IBSM_FINGER_POSITION_LEFT_LITTLE_FINGER;
		m_vecCaptureSeq.push_back(info);
    }

	if( strCaptureSeq == CAPTURE_SEQ_4_FLAT_FINGERS )
	{
		info.PreCaptureMessage = "Please put 4 fingers on the sensor!";
		info.PostCaptuerMessage = "Keep fingers on the sensor!";
		info.ImageType = ENUM_IBSU_FLAT_FOUR_FINGERS;
		info.NumberOfFinger = 4;
		info.fingerName = "4FF_Unknown";
		info.fingerPosition = IBSM_FINGER_POSITION_UNKNOWN;
		m_vecCaptureSeq.push_back(info);
	}

	if( strCaptureSeq == CAPTURE_SEQ_10_FLAT_WITH_4_FINGER_SCANNER )
	{
		info.PreCaptureMessage = "Please put right 4-fingers on the sensor!";
		info.fingerName = "4FF_Right_4_Fingers";
		info.PostCaptuerMessage = "Keep fingers on the sensor!";
		info.ImageType = ENUM_IBSU_FLAT_FOUR_FINGERS;
		info.NumberOfFinger = 4;
		info.fingerPosition = IBSM_FINGER_POSITION_PLAIN_RIGHT_FOUR_FINGERS;
		m_vecCaptureSeq.push_back(info);

		info.PreCaptureMessage = "Please put left 4-fingers on the sensor!";
		info.fingerName = "4FF_Left_4_Fingers";
		info.fingerPosition = IBSM_FINGER_POSITION_PLAIN_LEFT_FOUR_FINGERS;
		m_vecCaptureSeq.push_back(info);

		info.PreCaptureMessage = "Please put 2-thumbs on the sensor!";
		info.fingerName = "TFF_2_Thumbs";
		info.fingerPosition = IBSM_FINGER_POSITION_PLAIN_THUMBS;
		info.ImageType = ENUM_IBSU_FLAT_TWO_FINGERS;
		info.NumberOfFinger = 2;
		m_vecCaptureSeq.push_back(info);
	}

	// Make subfolder name
	QDateTime localTime = QDateTime::currentDateTime();
	m_ImgSubFolder = localTime.toString("yyyy-MM-dd hhmmss");

	OnMsg_CaptureSeqNext();
}

void IBSU_SampleForQT::OnMsg_CaptureSeqNext()
{
	if (QThread::currentThread() != this->thread())
	{
		// not sure how efficient it is
		QMetaObject::invokeMethod(this, "OnMsg_CaptureSeqNext",
			Qt::QueuedConnection);
		return;
	}

    int nRc;

    if (m_nDevHandle == -1)
        return;

    m_bBlank = false;
    memset(&m_FingerQuality[0], ENUM_IBSU_FINGER_NOT_PRESENT, sizeof(m_FingerQuality));

    m_nCurrentCaptureStep++;
    if(m_nCurrentCaptureStep >= (int)m_vecCaptureSeq.size())
    {
		// All of capture sequence completely
    	CaptureInfo tmpInfo;
		_SetLEDs(m_nDevHandle, tmpInfo, __LED_COLOR_NONE__, false);
        m_nCurrentCaptureStep = -1;
		m_ImgSubFolder = "";

        OnMsg_UpdateDisplayResources();
		ui->m_btnCaptureStart->setFocus();
        return;
    }

#ifdef Q_WS_WIN
	if (ui->m_chkInvalidArea->checkState())
	{
		IBSU_SetClientDisplayProperty(m_nDevHandle, ENUM_IBSU_WINDOW_PROPERTY_DISP_INVALID_AREA, "TRUE");
	}
	else
	{
		IBSU_SetClientDisplayProperty(m_nDevHandle, ENUM_IBSU_WINDOW_PROPERTY_DISP_INVALID_AREA, "FALSE");
	}
#endif

	if (ui->m_chkDetectSmear->checkState())
	{
		IBSU_SetProperty(m_nDevHandle, ENUM_IBSU_PROPERTY_ROLL_MODE, "1");
	    QString		strValue;
		QByteArray	byteValue;
		char		*cValue;

		strValue.sprintf("%d", ui->m_cboSmearLevel->currentIndex());
		byteValue = strValue.toLocal8Bit();
		cValue = byteValue.data();
		IBSU_SetProperty(m_nDevHandle, ENUM_IBSU_PROPERTY_ROLL_LEVEL, cValue);
	}
	else
	{
		IBSU_SetProperty(m_nDevHandle, ENUM_IBSU_PROPERTY_ROLL_MODE, "0");
	}

	// For Spoof control
	{
		QString		strValue;
		QMetaObject::invokeMethod(ui->m_txtSpoofResult, "setText", Qt::QueuedConnection, Q_ARG(QString, strValue));
	}
	
	if (ui->m_chkEnableSpoof->checkState()) // Turn of spoof enable
	{
		nRc = IBSU_SetProperty(m_nDevHandle, ENUM_IBSU_PROPERTY_ENABLE_SPOOF, "TRUE");
		// Disable segment rotation for the better PAD perfomance
		nRc = IBSU_SetProperty(m_nDevHandle, ENUM_IBSU_PROPERTY_DISABLE_SEGMENT_ROTATION, "TRUE");
		if(nRc == IBSU_STATUS_OK)
		{
			QString		strValue;
			QByteArray	byteValue;
			char		*cValue;

			strValue.sprintf("%d", ui->m_cboSpoofLevel->currentIndex()+1);
			byteValue = strValue.toLocal8Bit();
			cValue = byteValue.data();
			IBSU_SetProperty(m_nDevHandle, ENUM_IBSU_PROPERTY_SPOOF_LEVEL, cValue);	
		}
	}
	else
	{
		nRc = IBSU_SetProperty(m_nDevHandle, ENUM_IBSU_PROPERTY_ENABLE_SPOOF, "FALSE");
	}

//	for( int i=0; i<IBSU_MAX_SEGMENT_COUNT; i++ )
//		IBSU_ModifyOverlayQuadrangle(m_nDevHandle, m_nOvSegmentHandle[i], 0, 0, 0, 0, 0, 0, 0, 0, 0, (DWORD)0);

	// Make capture delay for display result image on multi capture mode (500 ms)
	if (m_nCurrentCaptureStep > 0)
    {
		Sleeper::msleep(500);
		m_strImageMessage = "";
    }

    CaptureInfo info = m_vecCaptureSeq[m_nCurrentCaptureStep];

    IBSU_ImageResolution imgRes = ENUM_IBSU_IMAGE_RESOLUTION_500;
    BOOL bAvailable = false;
    nRc = IBSU_IsCaptureAvailable(m_nDevHandle, info.ImageType, imgRes, &bAvailable );
    if (nRc != IBSU_STATUS_OK || !bAvailable)
    {
		_SetStatusBarMessage("The capture mode (%d) is not available", info.ImageType);
        m_nCurrentCaptureStep = -1;
        OnMsg_UpdateDisplayResources();
        return;
    }

	// Start capture
    unsigned long captureOptions = 0;
    if (ui->m_chkAutoContrast->checkState())
        captureOptions |= IBSU_OPTION_AUTO_CONTRAST;
    if (ui->m_chkAutoCapture->checkState())
        captureOptions |= IBSU_OPTION_AUTO_CAPTURE;
    if (ui->m_chkIgnoreFingerCount->checkState())
        captureOptions |= IBSU_OPTION_IGNORE_FINGER_COUNT;

    nRc = IBSU_BeginCaptureImage(m_nDevHandle, info.ImageType, imgRes, captureOptions);
    if(nRc>= IBSU_STATUS_OK)
    {
		// Display message for image acuisition
		QString strMessage;
		QByteArray byteMessage;
		char *cMessage;
		strMessage = info.PreCaptureMessage;
		byteMessage = strMessage.toLocal8Bit();
		cMessage = byteMessage.data();

		_SetStatusBarMessage("%s", cMessage);
		if( !ui->m_chkAutoCapture->checkState() )
			strMessage += "\r\nPress button 'Take Result Image' when image is good!";

		byteMessage = strMessage.toLocal8Bit();
		cMessage = byteMessage.data();
		_SetImageMessage("%s", cMessage);
		m_ImageType = info.ImageType;

        _SetLEDs(m_nDevHandle, info, __LED_COLOR_RED__, TRUE);
    }
    else
    {
		_SetStatusBarMessage("Failed to execute IBSU_BeginCaptureImage()");
		m_nCurrentCaptureStep = -1;
    }

    OnMsg_UpdateDisplayResources();

	return;
}

void IBSU_SampleForQT::OnMsg_DeviceCommunicationBreak()
{
	if (QThread::currentThread() != this->thread())
	{
		// not sure how efficient it is
		QMetaObject::invokeMethod(this, "OnMsg_DeviceCommunicationBreak",
			Qt::QueuedConnection);
		return;
	}

	int nRc;

	if( m_nDevHandle == -1 )
		return;

	_SetStatusBarMessage("Device communication was broken");

	nRc = _ReleaseDevice();
	if( nRc == IBSU_ERR_RESOURCE_LOCKED )
	{
		// retry to release device
		OnMsg_DeviceCommunicationBreak();
	}
	else
	{
		_BeepDeviceCommunicationBreak();
		OnMsg_UpdateDeviceList();
	}

	return;
}

void IBSU_SampleForQT::OnMsg_UpdateDeviceList()
{
	if (QThread::currentThread() != this->thread())
	{
		// not sure how efficient it is
		QMetaObject::invokeMethod(this, "OnMsg_UpdateDeviceList",
			Qt::QueuedConnection);
		return;
	}

    const bool idle = !m_bInitializing && (m_nCurrentCaptureStep == -1);

    if (idle)
    {
		ui->m_btnCaptureStop->setEnabled(false);
		ui->m_btnCaptureStart->setEnabled(false);
    }

	// store currently selected device
    QString strSelectedText;
    int selectedDev = (ui->m_cboUsbDevices->currentIndex());
    if (selectedDev > -1)
        strSelectedText = ui->m_cboUsbDevices->currentText();

    ui->m_cboUsbDevices->clear();
    ui->m_cboUsbDevices->addItem("-Please select-");

	// populate combo box
    int devices = 0;
    IBSU_GetDeviceCount(&devices);

    selectedDev = 0;
    for (int i=0; i<devices; i++)
    {
        IBSU_DeviceDesc devDesc;
        if (IBSU_GetDeviceDescription(i, &devDesc) < IBSU_STATUS_OK)
            continue;

        QString strDevice;
        if (devDesc.productName[0] == 0)
            strDevice = "unkonwn device";
        else
            strDevice.sprintf("%s_v%s (%s)", devDesc.productName, devDesc.fwVersion, devDesc.serialNumber);

        ui->m_cboUsbDevices->addItem(strDevice);
        if (strDevice == strSelectedText)
            selectedDev = i + 1;
    }

    if ((selectedDev == 0) && (ui->m_cboUsbDevices->count() == 2))
        selectedDev = 1;

    ui->m_cboUsbDevices->setCurrentIndex(selectedDev);

    if (idle)
    {
        OnCbnSelchangeComboDevices();
        _UpdateCaptureSequences();
    }

    return;
}

void IBSU_SampleForQT::OnMsg_InitWarning()
{
	if (QThread::currentThread() != this->thread())
	{
		// not sure how efficient it is
		QMetaObject::invokeMethod(this, "OnMsg_InitWarning",
			Qt::QueuedConnection);
		return;
	}

    return;
}

void IBSU_SampleForQT::OnMsg_UpdateDisplayResources()
{
	if (QThread::currentThread() != this->thread())
	{
		// not sure how efficient it is
		QMetaObject::invokeMethod(this, "OnMsg_UpdateDisplayResources",
			Qt::QueuedConnection);
		return;
	}

    bool selectedDev = ui->m_cboUsbDevices->currentIndex() > 0;
    bool captureSeq = ui->m_cboCaptureSeq->currentIndex() > 0;
    bool idle = !m_bInitializing && (m_nCurrentCaptureStep == -1);
    bool active = !m_bInitializing && (m_nCurrentCaptureStep != -1);
    bool uninitializeDev = selectedDev && (m_nDevHandle == -1);

    ui->m_cboUsbDevices->setEnabled(idle);
    ui->m_cboCaptureSeq->setEnabled(selectedDev && idle);

    ui->m_btnCaptureStart->setEnabled(captureSeq);
    ui->m_btnCaptureStop->setEnabled(active);

    ui->m_chkAutoContrast->setEnabled( selectedDev && idle);
    ui->m_chkAutoCapture->setEnabled(selectedDev && idle);
	ui->m_chkIgnoreFingerCount->setEnabled(selectedDev && idle);
    ui->m_chkSaveImges->setEnabled(selectedDev && idle);
	ui->m_btnImageFolder->setEnabled(selectedDev && idle);

	ui->m_chkUseClearPlaten->setEnabled(uninitializeDev);

	QString strCaption = "";
	if (active)
		strCaption = "Take Result Image";  
	else if (!active && !m_bInitializing)
		strCaption = "Start";  

	ui->m_btnCaptureStart->setText(strCaption);
	return;
}

void IBSU_SampleForQT::OnMsg_DrawFingerQuality()
{
	if (QThread::currentThread() != this->thread())
	{
		// not sure how efficient it is
		QMetaObject::invokeMethod(this, "OnMsg_DrawFingerQuality",
			Qt::QueuedConnection);
		return;
	}

	QPalette palette;
	for (int i=0; i<4; i++)
	{
		if (m_bNeedClearPlaten)
		{
			if (m_bBlank)
				palette.setColor(QPalette::Window, s_brushRed);
			else
				palette.setColor(QPalette::Window, s_brushPlaten);
		}
		else
		{
			switch( m_FingerQuality[i] )
			{
			case ENUM_IBSU_QUALITY_GOOD:
				palette.setColor(QPalette::Window, s_brushGreen);
				break;          
			case ENUM_IBSU_QUALITY_FAIR :
				palette.setColor(QPalette::Window, s_brushOrange);
				break;          
			case ENUM_IBSU_QUALITY_POOR :
				palette.setColor(QPalette::Window, s_brushRed);
				break;          
			case ENUM_IBSU_FINGER_NOT_PRESENT:
				palette.setColor(QPalette::Window, s_brushPlaten);
				break;
			case ENUM_IBSU_QUALITY_INVALID_AREA_TOP:
			case ENUM_IBSU_QUALITY_INVALID_AREA_BOTTOM:
			case ENUM_IBSU_QUALITY_INVALID_AREA_LEFT:
			case ENUM_IBSU_QUALITY_INVALID_AREA_RIGHT:
				palette.setColor(QPalette::Window, s_brushRed);
				break;
			default:
				palette.setColor(QPalette::Window, s_brushPlaten);
			}
		}

		switch (i)
		{
		case 0:
			ui->lblQuality_1->setAutoFillBackground(true);
			ui->lblQuality_1->setPalette(palette);
		case 1:
			ui->lblQuality_2->setAutoFillBackground(true);
			ui->lblQuality_2->setPalette(palette);
		case 2:
			ui->lblQuality_3->setAutoFillBackground(true);
			ui->lblQuality_3->setPalette(palette);
		case 3:
			ui->lblQuality_4->setAutoFillBackground(true);
			ui->lblQuality_4->setPalette(palette);
		}
	}

	return;
}

void IBSU_SampleForQT::OnMsg_AskRecapture(int imageStatus)
{
	if (QThread::currentThread() != this->thread())
	{
		// not sure how efficient it is
		QMetaObject::invokeMethod(this, "OnMsg_AskRecapture",
			Qt::QueuedConnection, Q_ARG(int, imageStatus));
		return;
	}

    QString askMsg;
	askMsg.sprintf("[Warning = %d] Do you want a recapture?", imageStatus);
	QMessageBox::StandardButton reply;
	reply = QMessageBox::question(this, "IntegrationSample For QT",
		askMsg, QMessageBox::Yes|QMessageBox::No);
	if (reply == QMessageBox::Yes)
    {
        // To recapture current finger position
        m_nCurrentCaptureStep--;
    }
    else
    {
        _BeepSuccess();
    }

	QMetaObject::invokeMethod(this, "repaint", Qt::QueuedConnection);

    OnMsg_CaptureSeqNext();
}







void IBSU_SampleForQT::paintEvent(QPaintEvent *)
{
    if(m_drawImage.Buffer == NULL || !m_bPaintEvent)
        return;

    m_bPaintEvent = false;

    if (m_drawImage.IsFinal)
    {
        IBSU_GenerateDisplayImage((const BYTE*)m_drawImage.Buffer, m_drawImage.Width, m_drawImage.Height,
                                    m_pScaledBuffer, ui->m_FrameImage->width(), ui->m_FrameImage->height(),
                                    0xFF, IBSU_IMG_FORMAT_GRAY, 2 /*HIGH QUALITY*/, TRUE);
    }
    else
    {
        IBSU_GenerateDisplayImage((const BYTE*)m_drawImage.Buffer, m_drawImage.Width, m_drawImage.Height,
                                    m_pScaledBuffer, ui->m_FrameImage->width(), ui->m_FrameImage->height(),
                                    0xFF, IBSU_IMG_FORMAT_GRAY, 0 /*LOW QUALITY*/, TRUE);
    }
    QImage Image(m_pScaledBuffer, ui->m_FrameImage->width(), ui->m_FrameImage->height(),
                 ui->m_FrameImage->width(), QImage::Format_Indexed8);
//    QImage ImgMirrored = Image.mirrored(false, true);
    QPixmap pixMap = QPixmap::fromImage(Image);
	QPainter painter(&pixMap);
#ifdef Q_WS_WIN
	_DrawOverlay_DispInvaliedArea(&painter, ui->m_FrameImage->width(), ui->m_FrameImage->height());
#endif
	_DrawOverlay_ImageText(&painter);
	_DrawOverlay_WarningOfClearPlaten(&painter, 0, 0, ui->m_FrameImage->width(), ui->m_FrameImage->height());
	_DrawOverlay_ResultSegmentImage(&painter);
	_DrawOverlay_RollGuideLine(&painter, ui->m_FrameImage->width(), ui->m_FrameImage->height());

    ui->m_FrameImage->setPixmap(pixMap);
}

void IBSU_SampleForQT::OnBnClickedBtnCaptureStart()
{
    int nRc;
	char minSDKVersion[IBSU_MAX_STR_LEN];
    char errorString[IBSU_MAX_STR_LEN];

    if(m_bInitializing)
        return;

    int devIndex = ui->m_cboUsbDevices->currentIndex() -1;
    if(devIndex < 0)
        return;

    if(m_nCurrentCaptureStep != -1)
    {
        BOOL IsActive;

		nRc = IBSU_IsCaptureActive(m_nDevHandle, &IsActive);

        if(nRc == IBSU_STATUS_OK && IsActive)
        {
            IBSU_TakeResultImageManually(m_nDevHandle);
        }

        return;
    }

    if(m_nDevHandle == -1)
    {
        m_bInitializing = true;

        if(m_bDevLocked)
        {
            bool ok;
            QString strKey = QInputDialog::getText(this, tr("Input Customer Key"), tr("Please enter Customer Key"), QLineEdit::Normal, tr(""), &ok);
            if(ok && !strKey.isEmpty())
            {
        	    QByteArray byteName = strKey.toLocal8Bit();
	            char *cCustomerKey = byteName.data();
                if (nRc = IBSU_SetCustomerKey(devIndex, ENUM_IBSU_HASH_TYPE_SHA256, cCustomerKey) != IBSU_STATUS_OK)
                {
                    IBSU_GetErrorString(nRc, errorString);
                    _SetStatusBarMessage("[Error code = %d] %s", nRc, errorString);
                    return;
                }
            }
        }

        int nRc = IBSU_AsyncOpenDevice( devIndex );
        m_bInitializing = false;

        if(nRc >= IBSU_STATUS_OK)
        {
			OnMsg_UpdateDisplayResources();
			return;
        }
        else
        {
			switch(nRc)
			{
			case IBSU_ERR_DEVICE_ACTIVE:
				_SetStatusBarMessage("[Error code = %d] Device initialization failed because in use by another thread/process.", nRc);
				break;
			case IBSU_ERR_USB20_REQUIRED:
				_SetStatusBarMessage("[Error code = %d] Device initialization failed because SDK only works with USB 2.0.", nRc);
				break;
	        case IBSU_ERR_DEVICE_HIGHER_SDK_REQUIRED:
				IBSU_GetRequiredSDKVersion(devIndex, minSDKVersion);
				_SetStatusBarMessage("[Error code = %d] Devcie initialization failed because SDK Version %s is required at least.", nRc, minSDKVersion );
				break;
			default:
                IBSU_GetErrorString(nRc, errorString);
                _SetStatusBarMessage("[Error code = %d] Device initialization failed. %s", nRc, errorString);
				break;
			}
        }
    }
    else
    {
        OnMsg_CaptureSeqStart();
    }

    OnMsg_UpdateDisplayResources();
}

void IBSU_SampleForQT::OnBnClickedBtnCaptureStop()
{
    if (m_nDevHandle == -1)
        return;

    IBSU_CancelCaptureImage(m_nDevHandle);
	CaptureInfo tmpInfo;
	_SetLEDs(m_nDevHandle, tmpInfo, __LED_COLOR_NONE__, false);
    m_nCurrentCaptureStep = -1;
	m_bNeedClearPlaten = FALSE;
	m_bBlank = FALSE;

	_SetStatusBarMessage("Capture Sequence aborted");
	_SetImageMessage("");
    OnMsg_UpdateDisplayResources();
}

void IBSU_SampleForQT::OnCbnSelchangeComboDevices()
{
    if (ui->m_cboUsbDevices->currentIndex() == m_nSelectedDevIndex)
        return;

	QApplication::setOverrideCursor(Qt::WaitCursor);
    m_nSelectedDevIndex = ui->m_cboUsbDevices->currentIndex();
    if(m_nDevHandle != -1)
    {
        OnBnClickedBtnCaptureStop();
		_ReleaseDevice();
    }

    _UpdateCaptureSequences();
	QApplication::restoreOverrideCursor();
}

void IBSU_SampleForQT::OnCbnSelchangeComboCaptureSeq()
{
    OnMsg_UpdateDisplayResources();
}

void IBSU_SampleForQT::OnChangeContrast()
{
	if (m_nDevHandle == -1 || ui->m_chkAutoContrast->checkState())
        return;

    int pos = ui->m_sliderContrast->value();
    QString strValue;
    strValue.sprintf("%d", pos);

	ui->m_txtContrast->setText(strValue);
    IBSU_SetContrast(m_nDevHandle, pos);
}

void IBSU_SampleForQT::OnBnClickedBtnImageFolder()
{
	QFileDialog *fd = new QFileDialog;
	QTreeView *tree = fd->findChild <QTreeView*>();
	tree->setRootIsDecorated(true);
	tree->setItemsExpandable(true);
	fd->setFileMode(QFileDialog::Directory);
	fd->setOption(QFileDialog::ShowDirsOnly);
	fd->setViewMode(QFileDialog::Detail);
	
	int result = fd->exec();
	if (result)
	{
		m_ImgSaveFolder = fd->selectedFiles()[0];
	}
	
    QByteArray ba = m_ImgSaveFolder.toLatin1();
    LPCSTR c_str2 = ba.data(); 

	if(IBSU_IsWritableDirectory(c_str2, true) != IBSU_STATUS_OK)
	{
	    QString msg;
		msg.sprintf("You don't have writing permission on this folder\r\nPlease select another folder (e.g. desktop folder)");
        QMessageBox::information(this, "IntegrationSample For QT", msg);
	}
}

void IBSU_SampleForQT::OnTimerQuality()
{
	OnMsg_DrawFingerQuality();

    if( m_bNeedClearPlaten )
	    m_bBlank = !m_bBlank;
}

