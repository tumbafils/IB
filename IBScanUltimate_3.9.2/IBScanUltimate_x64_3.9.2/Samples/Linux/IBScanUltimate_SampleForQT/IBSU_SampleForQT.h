#ifndef IBSU_SampleForQT_H
#define IBSU_SampleForQT_H

#include <QMainWindow>
#include <QMessageBox>
#include <QThread>
#include <QPainter>
#include <QPixmap>
#include <QMutex>
#include <QWaitCondition>
#include <QTimer>
#include <QVector>
#include <QDir>
#include <QMetaObject>
#include <QFileDialog>
#include <QDateTime>
#include <QTreeView>
#include <QInputDialog>

#ifdef Q_WS_WIN
#include <qt_windows.h>
#else
#include "TypeReDef.h"
#endif
#include "IBScanUltimateApi.h"

typedef struct tagCaptureInfo
{
    QString			PreCaptureMessage;		// to display on fingerprint window
    QString			PostCaptuerMessage;		// to display on fingerprint window
    IBSU_ImageType	ImageType;				// capture mode
    int				NumberOfFinger;			// number of finger count
    QString			fingerName;				// finger name (e.g left thumbs, left index ... )
	IBSM_FingerPosition fingerPosition;		// Finger position. e.g Right Thumb, Right Index finger
}CaptureInfo;

namespace Ui {
class IBSU_SampleForQT;
}


class Sleeper : public QThread
{
public:
    static void usleep(unsigned long usecs){QThread::usleep(usecs);}
    static void msleep(unsigned long msecs){QThread::msleep(msecs);}
    static void sleep(unsigned long secs){QThread::sleep(secs);}
};

class IBSU_SampleForQT : public QMainWindow
{
    Q_OBJECT
    
public:
    explicit IBSU_SampleForQT(QWidget *parent = 0);
    ~IBSU_SampleForQT();



	/// Callback functions.
	/// Please refer to IBScanUltimateApi_defs.h in include folder.
	static void CALLBACK OnEvent_DeviceCommunicationBreak(
						 const int deviceHandle,
						 void*     pContext
					   );

	static void CALLBACK OnEvent_PreviewImage(
						 const int deviceHandle,
						 void*     pContext,
						 const	   IBSU_ImageData image
					   );

	static void CALLBACK OnEvent_FingerCount(
						   const int                   deviceHandle,
						   void*                       pContext,
						   const IBSU_FingerCountState fingerCountState
						 );

	static void CALLBACK OnEvent_FingerQuality(
                          const int                     deviceHandle,   
                          void                          *pContext,       
                          const IBSU_FingerQualityState *pQualityArray, 
                          const int                     qualityArrayCount    
						 );

	static void CALLBACK OnEvent_DeviceCount(
						 const int detectedDevices,
						 void      *pContext
					   );

	static void CALLBACK OnEvent_InitProgress(
						 const int deviceIndex,
						 void      *pContext,
						 const int progressValue
					   );

	static void CALLBACK OnEvent_TakingAcquisition(
						 const int				deviceHandle,
						 void					*pContext,
						 const IBSU_ImageType	imageType
					   );

	static void CALLBACK OnEvent_CompleteAcquisition(
						 const int				deviceHandle,
						 void					*pContext,
						 const IBSU_ImageType	imageType
					   );

/****
 ** This IBSU_CallbackResultImage callback was deprecated since 1.7.0
 ** Please use IBSU_CallbackResultImageEx instead
*/
    static void CALLBACK OnEvent_ResultImageEx(
                          const int                   deviceHandle,
                          void                        *pContext,
                          const int                   imageStatus,
                          const IBSU_ImageData        image,
						  const IBSU_ImageType        imageType,
						  const int                   detectedFingerCount,
                          const int                   segmentImageArrayCount,
                          const IBSU_ImageData        *pSegmentImageArray,
						  const IBSU_SegmentPosition  *pSegmentPositionArray
                        );

	static void CALLBACK OnEvent_ClearPlatenAtCapture(
                          const int                   deviceHandle,
                          void                        *pContext,
                          const IBSU_PlatenState      platenState
                        );

	static void CALLBACK OnEvent_AsyncOpenDevice(
                          const int                   deviceIndex,
                          void                        *pContext,
                          const int                   deviceHandle,
                          const int                   errorCode
                        );

	static void CALLBACK OnEvent_NotifyMessage(
                          const int                deviceHandle,
                          void                     *pContext,
                          const int                message
                        );

	static void CALLBACK OnEvent_PressedKeyButtons(
                          const int                deviceHandle,
                          void                     *pContext,
                          const int                pressedKeyButtons
                        );

	void		_Make32bitImage_FromRaw(uchar *data, int width, int height, QImage *rawImage);
	void		_SetStatusBarMessage(char* Format, ...);
	void		_SetImageMessage(char* Format, ...);
    void		_UpdateCaptureSequences();
    int			_ReleaseDevice();
	void		_BeepFail();
	void		_BeepSuccess();
	void		_BeepOk();
	void		_BeepDeviceCommunicationBreak();
    void		_SaveBitmapImage(const IBSU_ImageData &image, const QString &fingerName);
    void		_SaveWsqImage(const IBSU_ImageData &image, const QString &fingerName);
    void		_SavePngImage(const IBSU_ImageData &image, const QString &fingerName);
    void		_SaveJP2Image(const IBSU_ImageData &image, const QString &fingerName);
    void		_SaveISOImage(const IBSU_ImageData &image, const QString &fingerName );
    int			_WaitingForFinishInitDevice(const int devIndex);
	int			_ExecuteInitializeDevice(int nRc, int devHandle);
	void		_DrawOverlay_ImageText(QPainter *painter);
	void		_DrawOverlay_WarningOfClearPlaten(QPainter *painter, int left, int top, int width, int height);
	void		_DrawOverlay_DispInvaliedArea(QPainter *painter, int width, int height);
	void		_DrawOverlay_ResultSegmentImage(QPainter *painter);
	void		_DrawOverlay_RollGuideLine(QPainter *painter, int width, int height);
	void		_SetLEDs(int deviceHandle, CaptureInfo info, int ledColor, bool bBlink);





protected:
    void    paintEvent(QPaintEvent *);


public:
	static const QColor   s_brushRed;                   ///<  Red background brush for scanner
	static const QColor   s_brushOrange;                ///<  Orange background brush for scanner
	static const QColor   s_brushGreen;                 ///<  Green background brush for scanner
	static const QColor   s_brushPlaten;				///<  Platen brush for scanner

	QTimer			*m_timerQuality;

	int				m_nSelectedDevIndex;						///< Index of selected device
	int				m_nDevHandle;								///< Device handle
	bool			m_bSelectDev;
	bool			m_bInitializing;							///< Device initialization is in progress
	QString			m_ImgSaveFolder;							///< Base folder for image saving
	QString			m_ImgSubFolder;								///< Sub Folder for image sequence
	QString			m_strImageMessage;
	bool			m_bNeedClearPlaten;
	bool			m_bBlank;
	int				m_nSegmentImageArrayCount;
    bool            m_bPaintEvent;
    IBSU_SegmentPosition  m_SegmentPositionArray[IBSU_MAX_SEGMENT_COUNT];

	QVector< CaptureInfo >		m_vecCaptureSeq;				///< Sequence of capture steps
	int							m_nCurrentCaptureStep;			///< Current capture step

	IBSU_SdkVersion m_verInfo;
	IBSU_FingerQualityState	m_FingerQuality[IBSU_MAX_SEGMENT_COUNT];
	IBSU_LedType 	m_LedType;

    IBSM_ImageData  m_CapturedImg;
	IBSM_ImageData	m_CapturedImgSplit[IBSU_MAX_SEGMENT_COUNT];
	int				m_CapturedImgSplitCnt;
	
	/*#########################################*/
	IBSU_ImageType	m_ImageType;
    IBSU_RollingState       m_rollingState;
    int                     m_rollingLineX;
    int                     m_bDevLocked;





private:
    Ui::IBSU_SampleForQT *ui;

private slots:
    void		OnBnClickedBtnCaptureStart();
    void		OnBnClickedBtnCaptureStop();
    void		OnCbnSelchangeComboDevices();
    void		OnChangeContrast();
    void		OnCbnSelchangeComboCaptureSeq();
	void		OnBnClickedBtnImageFolder();
	void		OnTimerQuality();

public Q_SLOTS:
    void		OnMsg_CaptureSeqStart();
    void		OnMsg_CaptureSeqNext();
	void		OnMsg_DeviceCommunicationBreak();
    void		OnMsg_UpdateDeviceList();
    void		OnMsg_InitWarning();
    void        OnMsg_UpdateDisplayResources();
	void		OnMsg_DrawFingerQuality();
	void		OnMsg_AskRecapture(int imageStatus);
	void		OnMsg_GetSelectDevice();



};

#endif // IBSU_SampleForQT_H
