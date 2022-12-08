/* *************************************************************************************************
 * IBScanUltimate_SampleForJAVA.java
 *
 * DESCRIPTION:
 *     Java FunctionTester sample application for IBScanUltimate
 *     http://www.integratedbiometrics.com
 *
 * NOTES:
 *     Copyright (c) Integrated Biometrics, 2013-2017
 *
 * HISTORY:
 *    2014/04/16  First verion
 *    2014/11/24  Added generateZoomOutImageEx() function to increase speed to draw the image.
 *    2015/12/11  Updated for IBScanUltimate v1.9.0.
 *    2017/10/17  Re-formatted code for logic improvement
 ************************************************************************************************ */

package com.sample.IBScanUltimate_SampleforJava;

import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Font;
import java.awt.Graphics2D;
import java.awt.Rectangle;
import java.awt.SystemColor;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.net.URL;
import java.sql.Date;
import java.text.SimpleDateFormat;
import java.util.Vector;

import javax.imageio.ImageIO;
import javax.sound.sampled.LineUnavailableException;
import javax.swing.BoxLayout;
import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JCheckBox;
import javax.swing.JComboBox;
import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JSlider;
import javax.swing.JTextField;
import javax.swing.JTextPane;
import javax.swing.SwingConstants;
import javax.swing.border.EtchedBorder;
import javax.swing.border.TitledBorder;
import javax.swing.event.ChangeEvent;
import javax.swing.event.ChangeListener;
import javax.swing.filechooser.FileFilter;
import java.awt.image.DataBufferByte;

import com.integratedbiometrics.ibscanultimate.IBScan;
import com.integratedbiometrics.ibscanultimate.IBScan.HashType;
import com.integratedbiometrics.ibscanultimate.IBScanDevice;
import com.integratedbiometrics.ibscanultimate.IBScanDevice.FingerCountState;
import com.integratedbiometrics.ibscanultimate.IBScanDevice.FingerQualityState;
import com.integratedbiometrics.ibscanultimate.IBScanDevice.ImageData;
import com.integratedbiometrics.ibscanultimate.IBScanDevice.ImageType;
import com.integratedbiometrics.ibscanultimate.IBScanDevice.LedState;
import com.integratedbiometrics.ibscanultimate.IBScanDevice.PlatenState;
import com.integratedbiometrics.ibscanultimate.IBScanDevice.RollingData;
import com.integratedbiometrics.ibscanultimate.IBScanDevice.SegmentPosition;
import com.integratedbiometrics.ibscanultimate.IBScanDeviceListener;
import com.integratedbiometrics.ibscanultimate.IBScanException;
import com.integratedbiometrics.ibscanultimate.IBScanListener;

import com.integratedbiometrics.ibscancommon.IBCommon.*;

/**
 * Principal class for function tester demo UI.
 */
@SuppressWarnings("serial")
public class IBScanUltimate_Sample extends JFrame implements IBScanListener, IBScanDeviceListener
{
	/**
	 * @param args
	 * @throws IBScanException 
	 */
	public static void main(String[] args) throws IBScanException
	{
		IBScanUltimate_Sample frame = new IBScanUltimate_Sample();
		frame.init();
		frame.setVisible(true);
	}

	/**
	 * Create UI for function tester, initialize IBScan, and register callbacks.
	 */
	public IBScanUltimate_Sample()
	{
		Font mainFont = new Font("Lucida Grande", Font.PLAIN, 11);
		Font titleFont = new Font("Lucida Grande", Font.PLAIN, 11);

		setTitle("IntergrationSample for JAVA -- (" + System.getProperty("sun.arch.data.model") + ")bit");
		setResizable(false);
		getContentPane().setLayout(
				new BoxLayout(getContentPane(), BoxLayout.X_AXIS));
		setBounds(0, 0, 787, 617);
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

		JPanel pnl = new JPanel();
		getContentPane().add(pnl);
		pnl.setLayout(null);
		pnl.setBackground(new Color(255,255,255));

		JPanel pnlMainInterfaceFunction = new JPanel();
		pnlMainInterfaceFunction.setBounds(10, 85, 295, 50);
		pnl.add(pnlMainInterfaceFunction);
		pnlMainInterfaceFunction.setLayout(null);

		// Device -ComboBox
		this.m_cboUsbDevices = new JComboBox();
		this.m_cboUsbDevices.setFont(mainFont);
		this.m_cboUsbDevices.setBounds(14, 20, 265, 21);
		this.m_cboUsbDevices.addItem("--PLEASE SELECT--");
		this.m_cboUsbDevices.addActionListener(this.m_cboUsbDevice_Changed);
		pnlMainInterfaceFunction.add(this.m_cboUsbDevices);
		
	
		// Image Label - DEVICES
		try {
			m_buflblDevices = ImageIO.read(m_urllblDevices);
		} catch (IOException e) {
			e.printStackTrace();
		}
		this.m_lblDevices = new JLabel(new ImageIcon(m_buflblDevices));
		this.m_lblDevices.setBounds(14, 5, 265, 15);
		pnlMainInterfaceFunction.add(this.m_lblDevices);

		//
		// Image Acquisition
		//

		JPanel pnlImageAcquisition = new JPanel();
		pnlImageAcquisition.setLayout(null);
		/*
		 * pnlImageAcquisition.setBorder(new TitledBorder(new EtchedBorder(
		 * EtchedBorder.LOWERED, null, null), "Fingerprint Capture",
		 * TitledBorder.LEADING, TitledBorder.TOP, titleFont, new Color(0, 0, 0)));
		 */
		pnlImageAcquisition.setBounds(10, 140, 295, 215);
		pnl.add(pnlImageAcquisition);

		// Image Type Combobox
		this.m_cboCaptureSeq = new JComboBox();
		this.m_cboCaptureSeq.setFont(mainFont);
		this.m_cboCaptureSeq.setBounds(14, 20, 265, 25);
		this.m_cboCaptureSeq.addActionListener(m_cboCaptureSeq_Changed);
		pnlImageAcquisition.add(this.m_cboCaptureSeq);

		// CheckBox Selected
		this.m_chkAutoContrast = new JCheckBox(
				"Automatic contrast optimization");
		this.m_chkAutoContrast.setFont(mainFont);
		this.m_chkAutoContrast.setBounds(10, 50, 273, 20);
		this.m_chkAutoContrast.setSelected(true);
		pnlImageAcquisition.add(this.m_chkAutoContrast);

		this.m_chkAutoCapture = new JCheckBox(
				"Automatic capture for fingerprints");
		this.m_chkAutoCapture.setFont(mainFont);
		this.m_chkAutoCapture.setBounds(10, 68, 273, 20);
		this.m_chkAutoCapture.setSelected(true);
		pnlImageAcquisition.add(this.m_chkAutoCapture);

		this.m_chkIgnoreFingerCount = new JCheckBox(
				"Trigger invalid finger count on auto-capture");
		this.m_chkIgnoreFingerCount.setFont(mainFont);
		this.m_chkIgnoreFingerCount.setBounds(10, 86, 273, 20);
		pnlImageAcquisition.add(this.m_chkIgnoreFingerCount);

		this.m_chkSaveImages = new JCheckBox("save images");
		this.m_chkSaveImages.setFont(mainFont);
		this.m_chkSaveImages.setBounds(10, 108, 92, 20);
		pnlImageAcquisition.add(this.m_chkSaveImages);

		// START Button
		this.m_btnCaptureStart = new JButton("Start");
		this.m_btnCaptureStart.addActionListener(this.m_btnCaptureStart_Click);
		this.m_btnCaptureStart.setFont(mainFont);
		this.m_btnCaptureStart.setBounds(155, 135, 125, 25);
		this.m_btnCaptureStart.setEnabled(false);
		pnlImageAcquisition.add(this.m_btnCaptureStart);

		// STOP Button
		this.m_btnCaptureStop = new JButton("Stop");
		this.m_btnCaptureStop.addActionListener(this.m_btnCaptureStop_Click);
		this.m_btnCaptureStop.setFont(mainFont);
		this.m_btnCaptureStop.setBounds(14, 135, 125, 25);
		this.m_btnCaptureStop.setEnabled(false);
		pnlImageAcquisition.add(this.m_btnCaptureStop);
		
		this.lblContrast = new JLabel("Contrast");
		this.lblContrast.setFont(new Font("Dialog", Font.PLAIN, 11));
		this.lblContrast.setBounds(14, 174, 46, 14);
		pnlImageAcquisition.add(this.lblContrast);
		
		this.m_sliderContrast = new JSlider();
		this.m_sliderContrast.setFont(new Font("Dialog", Font.PLAIN, 11));
		this.m_sliderContrast.setPaintLabels(true);
		this.m_sliderContrast.setPaintTicks(true);
		this.m_sliderContrast.setMaximum(34);
		this.m_sliderContrast.setMinimum(0);
		this.m_sliderContrast.setValue(21);
		this.m_sliderContrast.setMajorTickSpacing(5);
		this.m_sliderContrast.setMinorTickSpacing(1);
		this.m_sliderContrast.setBounds(60, 168, 175, 35);
		this.m_sliderContrast.addChangeListener(new m_sliderContrast_Change());
		pnlImageAcquisition.add(this.m_sliderContrast);
		
		this.m_txtContrast = new JTextField();
		m_txtContrast.setFont(new Font("Dialog", Font.PLAIN, 11));
		this.m_txtContrast.setText("21");
		this.m_txtContrast.setHorizontalAlignment(SwingConstants.CENTER);
		this.m_txtContrast.setEditable(false);
		this.m_txtContrast.setColumns(10);
		this.m_txtContrast.setBounds(240, 171, 39, 20);
		pnlImageAcquisition.add(this.m_txtContrast);
		
		this.m_btnImageFolder = new JButton("...");
		this.m_btnImageFolder.addActionListener(this.m_btnImageFolder_Click);
		this.m_btnImageFolder.setFont(new Font("Dialog", Font.PLAIN, 11));
		this.m_btnImageFolder.setEnabled(false);
		this.m_btnImageFolder.setBounds(107, 107, 39, 20);
		pnlImageAcquisition.add(this.m_btnImageFolder);
		
		
		// Image Label - FingerPrint Capture
		try {
			m_bufFingerPrintStatus = ImageIO.read(m_urllblFingerPrintStatus);
		} catch (IOException e) {
			e.printStackTrace();
		}
		this.m_lblFingerprintcapture = new JLabel(new ImageIcon(m_bufFingerPrintStatus));
		this.m_lblFingerprintcapture.setBounds(14, 5, 265, 15);
		pnlImageAcquisition.add(this.m_lblFingerprintcapture);

		//
		// Function Result
		//
		JPanel pnlFunctionResult = new JPanel();
		pnlFunctionResult.setLayout(null);
		pnlFunctionResult.setBorder(new EtchedBorder(EtchedBorder.LOWERED, null, null));
		pnlFunctionResult.setBounds(323, 548, 440, 30);
		pnl.add(pnlFunctionResult);

		this.m_txtStatusMessage = new JTextPane();
		this.m_txtStatusMessage.setBackground(SystemColor.menu);
		this.m_txtStatusMessage.setEditable(false);
		this.m_txtStatusMessage.setBounds(2, 2, 457, 26);
		this.m_txtStatusMessage.setFont(mainFont);
		this.m_txtStatusMessage.setText("Ready");
		pnlFunctionResult.add(this.m_txtStatusMessage);

		//
		// Image Preview
		//
		this.pnlImagePreview = new JPanel();
		this.pnlImagePreview.setBorder(new TitledBorder(new EtchedBorder(EtchedBorder.LOWERED, null, null), "", TitledBorder.LEADING, TitledBorder.TOP, null, new Color(0, 0, 0)));
		this.pnlImagePreview.setBounds(323, 85, 440, 420);
		this.m_lblImagePreview = new JLabel(new ImageIcon());
		this.m_lblImagePreview.setBounds(this.pnlImagePreview.getX()+5, this.pnlImagePreview.getY()+5, this.pnlImagePreview.getWidth()-20, this.pnlImagePreview.getHeight()-20);
		this.pnlImagePreview.add(this.m_lblImagePreview);
		pnl.add(this.pnlImagePreview);

		//
		// Device Quality
		//

		JPanel pnlDevicequality = new JPanel();
		pnlDevicequality.setBounds(10, 360, 295, 215);
	
		try {
			img = ImageIO.read(m_urlScannerImg);
		} catch (IOException e) {
			e.printStackTrace();
		}
		this.m_lblScanner = new JLabel(new ImageIcon(img));
		this.m_lblScanner.setBounds(14, 383, 130, 135);
		pnl.add(this.m_lblScanner);
		
		try {
			m_bufLockImg = ImageIO.read(m_urlLockImg);
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		pnl.add(pnlDevicequality);
		pnlDevicequality.setLayout(null);

		//
		// Logo
		//

/*		URL m_urlLogoImg = IBScanUltimate_Sample.class
				.getResource("/resources/Logo.png");
		JLabel lblLogo;
		if (m_urlLogoImg == null) {
			lblLogo = new JLabel(new ImageIcon());
		} else {
			lblLogo = new JLabel(new ImageIcon(m_urlLogoImg));
		}
		lblLogo.setBounds(0, 0, 905, 75);
		pnl.add(lblLogo);
*/
		try {
			m_bufImgLog = ImageIO.read(m_urlLogoImg);
		} catch (IOException e) {
			e.printStackTrace();
		}
		this.lblLogo = new JLabel(new ImageIcon(m_bufImgLog));
		lblLogo.setHorizontalAlignment(SwingConstants.LEFT);
		this.lblLogo.setBounds(0, 0, 905, 75);
		pnl.add(this.lblLogo);

		//
		// checkBox
		//

		this.m_chkUseClearPlaten = new JCheckBox("Detect clear Platen");
		this.m_chkUseClearPlaten.setFont(mainFont);
		this.m_chkUseClearPlaten.setBounds(132, 20, 145, 20);
		this.m_chkUseClearPlaten.setSelected(true);
		pnlDevicequality.add(this.m_chkUseClearPlaten);

		this.m_chkDrawSegmentImage = new JCheckBox(
				"Draw quadrangle for segment image ");
		this.m_chkDrawSegmentImage.setFont(mainFont);
		this.m_chkDrawSegmentImage.setBounds(132, 43, 157, 20);
		this.m_chkDrawSegmentImage.setSelected(true);
		pnlDevicequality.add(this.m_chkDrawSegmentImage);

		this.m_chkNFIQScore = new JCheckBox("NFIQ");
		this.m_chkNFIQScore.setFont(mainFont);
		this.m_chkNFIQScore.setBounds(132, 66, 55, 20);
		this.m_chkNFIQScore.setSelected(true);
		pnlDevicequality.add(this.m_chkNFIQScore);
		
		this.m_txtNFIQScore = new JTextField();
		this.m_txtNFIQScore.setFont(new Font("Dialog", Font.PLAIN, 11));
		this.m_txtNFIQScore.setHorizontalAlignment(SwingConstants.CENTER);
		this.m_txtNFIQScore.setEditable(false);
		this.m_txtNFIQScore.setBounds(191, 66, 86, 20);
		pnlDevicequality.add(this.m_txtNFIQScore);
		this.m_txtNFIQScore.setColumns(10);
		
		this.m_chkInvalidArea = new JCheckBox("Invalied area");
		this.m_chkInvalidArea.setFont(new Font("Dialog", Font.PLAIN, 11));
		this.m_chkInvalidArea.setBounds(132, 89, 145, 20);
		pnlDevicequality.add(this.m_chkInvalidArea);
		
		this.m_chkDetectSmear = new JCheckBox("Detect smear");
		this.m_chkDetectSmear.setSelected(true);
		this.m_chkDetectSmear.setFont(new Font("Dialog", Font.PLAIN, 11));
		this.m_chkDetectSmear.setBounds(132, 112, 90, 20);
		pnlDevicequality.add(this.m_chkDetectSmear);
		
		this.m_cboSmearLevel = new JComboBox();
		this.m_cboSmearLevel.setFont(new Font("Dialog", Font.PLAIN, 11));
		this.m_cboSmearLevel.setBounds(225, 112, 52, 20);
		pnlDevicequality.add(this.m_cboSmearLevel);
		
		this.m_chkEnableSpoof = new JCheckBox("Enable Spoof");
		this.m_chkEnableSpoof.setSelected(false);
		this.m_chkEnableSpoof.setFont(new Font("Dialog", Font.PLAIN, 11));
		this.m_chkEnableSpoof.setBounds(132, 134, 90, 20);
		pnlDevicequality.add(this.m_chkEnableSpoof);
		
		this.m_txtSpoofResult = new JTextField();
		this.m_txtSpoofResult.setFont(new Font("Dialog", Font.PLAIN, 11));
		this.m_txtSpoofResult.setHorizontalAlignment(SwingConstants.CENTER);
		this.m_txtSpoofResult.setEditable(false);
		this.m_txtSpoofResult.setBounds(153, 160, 124, 20);
		pnlDevicequality.add(this.m_txtSpoofResult);
		
		this.m_cboSpoofLevel = new JComboBox();
		this.m_cboSpoofLevel.setBounds(225, 134, 52, 20);
		this.m_cboSpoofLevel.setFont(new Font("Dialog", Font.PLAIN, 11));
		pnlDevicequality.add(this.m_cboSpoofLevel);
		

		
		// Image Label - Device Status
		try {
			m_buflblDeviceStatus = ImageIO.read(m_urllblDeviceStatus);
		} catch (IOException e) {
			e.printStackTrace();
		}
		this.m_lblDeviceStatus = new JLabel(new ImageIcon(m_buflblDeviceStatus));
		this.m_lblDeviceStatus.setBounds(12, 5, 265, 15);
		pnlDevicequality.add(this.m_lblDeviceStatus);
		
		this.m_lblLocked = new JLabel("LOCKED");
		this.m_lblLocked.setFont(new Font("Microsoft Sans Serif", Font.BOLD, 14));
		this.m_lblLocked.setForeground(new Color(0,166,81));
		this.m_lblLocked.setBounds(68, 175, 73, 15);
		pnlDevicequality.add(this.m_lblLocked);
		
		this.m_lblLockedImg = new JLabel(new ImageIcon(m_bufLockImg));
		this.m_lblLockedImg.setBounds(28, 168, 28, 28);
		pnlDevicequality.add(this.m_lblLockedImg);

		//
		// Initialize IBScan
		//

		this.ibScan = IBScan.getInstance();
		this.ibScan.setScanListener(this);
		
	}

	// //////////////////////////////////////////////////////////////////////////////////////////////
	// UI ELEMENTS
	// //////////////////////////////////////////////////////////////////////////////////////////////

	protected JTextField m_txtNFIQScore;
	protected JLabel lblContrast;
	protected JTextField m_txtContrast;

	// Button
	protected JButton btnCaptureImage;
	protected JButton m_btnCaptureStart;
	protected JButton m_btnCaptureStop;
	protected JButton m_btnImageFolder;

	// Main Interface Function
	protected JComboBox m_cboUsbDevices;

	// Image Acquisition
	protected JPanel pnlImagePreview;
	protected JComboBox m_cboCaptureSeq;
	protected JCheckBox m_chkAutoContrast;
	protected JCheckBox m_chkAutoCapture;
	protected JCheckBox m_chkIgnoreFingerCount;
	protected JCheckBox m_chkSaveImages;
	protected JCheckBox m_chkDetectSmear;
	protected JComboBox m_cboSmearLevel;
	
	// Spoof Control
	protected JCheckBox m_chkEnableSpoof;
	protected JComboBox m_cboSpoofLevel;
	protected JTextField m_txtSpoofResult;

	// Device Quality
	protected JCheckBox m_chkUseClearPlaten;
	protected JCheckBox m_chkDrawSegmentImage;
	protected JCheckBox m_chkNFIQScore;
	protected JCheckBox m_chkInvalidArea;

	// Function Result
	protected JTextPane m_txtStatusMessage;

	// Labels for renewal UI
	protected JLabel m_lblDevices; // "DEVICES" Label
	protected JLabel m_lblFingerprintcapture; // "FINGERPRINT CAPTURE" Label
	protected JLabel m_lblDeviceStatus; // "DEVICE STATUS" Label
	protected JLabel m_lblLocked; // "LOCKED" Label 
	
	// Image Preview
	protected JLabel m_lblImagePreview;

	// Device Image
	protected JLabel m_lblScanner;
	// Locked image
	protected JLabel m_lblLockedImg; 

	// Logo
	protected JLabel lblLogo;
	
	// Contrast slider
	protected JSlider m_sliderContrast;

	//
	protected String SelDeviceName = null;
	
	protected final int __TIMER_STATUS_DELAY__				= 500;

	// Capture sequence definitions
	protected final String CAPTURE_SEQ_FLAT_SINGLE_FINGER 				= "Single flat finger";
	protected final String CAPTURE_SEQ_ROLL_SINGLE_FINGER 				= "Single rolled finger";
	protected final String CAPTURE_SEQ_2_FLAT_FINGERS 					= "2 flat fingers";
	protected final String CAPTURE_SEQ_10_SINGLE_FLAT_FINGERS 			= "10 single flat fingers";
	protected final String CAPTURE_SEQ_10_SINGLE_ROLLED_FINGERS 		= "10 single rolled fingers";
	protected final String CAPTURE_SEQ_4_FLAT_FINGERS 					= "4 flat fingers";
	protected final String CAPTURE_SEQ_10_FLAT_WITH_4_FINGER_SCANNER 	= "10 flat fingers with 4-finger scanner";
	
	// Beep definitions
	protected final int __BEEP_FAIL__						= 0;
	protected final int __BEEP_SUCCESS__					= 1;
	protected final int __BEEP_OK__							= 2;
	protected final int __BEEP_DEVICE_COMMUNICATION_BREAK__	= 3;

	// LED color definitions
	protected final int __LED_COLOR_NONE__		= 0;
	protected final int __LED_COLOR_GREEN__		= 1;
	protected final int __LED_COLOR_RED__		= 2;
	protected final int __LED_COLOR_YELLOW__	= 3;

	// Key button definitions
	protected final int __LEFT_KEY_BUTTON__		= 1;
	protected final int __RIGHT_KEY_BUTTON__	= 2;
	
	// Device Lock definitions
	protected final int DEVICE_NORMAL		= 0;
	protected final int DEVICE_LOCKED		= 1;
	protected final int DEVICE_UNLOCKED		= 2;
	protected final int DEVICE_KEY_MATCHED	= 3;
	protected final int DEVICE_KEY_INVALID	= 4;
	

	/* *********************************************************************************************
	 * PRIVATE CLASSES
	 ******************************************************************************************** */

	protected class CaptureInfo
	{
		String		PreCaptureMessage;		// to display on fingerprint window
		String		PostCaptuerMessage;		// to display on fingerprint window
		ImageType	ImageType;				// capture mode
		int			NumberOfFinger;			// number of finger count
		String		fingerName;				// finger name (e.g left thumbs, left index ... )
		FingerPosition fingerPosition;      // Finger position for IBSM(Matcher) structure
	};

				

	// Device Image
	protected BufferedImage img = null;
	protected BufferedImage m_bufImgLog = null;
	protected BufferedImage m_bufLockImg = null;
	// Image Label Buffer
	protected BufferedImage m_buflblDevices = null;
	protected BufferedImage m_buflblDeviceStatus = null;
	protected BufferedImage m_bufFingerPrintStatus = null;
	
	protected URL m_urlScannerImg = IBScanUltimate_Sample.class.getResource("/resources/Scanner.png");
	protected URL m_urlLogoImg = IBScanUltimate_Sample.class.getResource("/resources/Logo.png");
	protected URL m_urlLockImg = IBScanUltimate_Sample.class.getResource("/resources/Lock.png");
	
	// Image Label URL
	protected URL m_urllblDevices = IBScanUltimate_Sample.class.getResource("/resources/Devices.png");
	protected URL m_urllblDeviceStatus = IBScanUltimate_Sample.class.getResource("/resources/Device_Status.png");
	protected URL m_urllblFingerPrintStatus = IBScanUltimate_Sample.class.getResource("/resources/Fingerprint_Status.png");
	
	protected ImageIcon imageicon = null;

	protected int		m_nSelectedDevIndex = -1;				///< Index of selected device
	protected boolean	m_bInitializing = false;				///< Device initialization is in progress
	String				m_ImgSaveFolder = "";					///< Base folder for image saving
	String				m_ImgSubFolder = "";					///< Sub Folder for image sequence
	protected String 	m_strImageMessage = "";
	protected boolean 	m_bNeedClearPlaten = false;
	protected boolean 	m_bBlank = false;
	protected boolean	m_bSaveWarningOfClearPlaten;

	protected Vector<CaptureInfo> m_vecCaptureSeq = new Vector<CaptureInfo>();		///< Sequence of capture steps
	protected int m_nCurrentCaptureStep = -1;					///< Current capture step

	protected IBScanDevice.LedState m_LedState;
//	protected FingerQualityState[] m_FingerQuality =  {FINGER_NOT_PRESENT, FINGER_NOT_PRESENT, FINGER_NOT_PRESENT, FINGER_NOT_PRESENT};
	protected FingerQualityState[] m_FingerQuality = {FingerQualityState.FINGER_NOT_PRESENT, FingerQualityState.FINGER_NOT_PRESENT, FingerQualityState.FINGER_NOT_PRESENT, FingerQualityState.FINGER_NOT_PRESENT};
	protected ImageType	m_ImageType;
	protected int m_nSegmentImageArrayCount=0;
	protected SegmentPosition[] m_SegmentPositionArray;

	protected BufferedImage m_grayscaleImageJ = null;
	protected BufferedImage m_drawImageJ = null;
	protected byte[] m_drawBuffer;
	protected byte[] m_grayscaleImageData;

	protected String 	m_minSDKVersion = ""; 
	protected int m_nDeviceLockState = DEVICE_UNLOCKED;
	
	// For ISO Save
	protected Object[] m_imageDataExtResult ; // ImageDataExt structure for ISO/Matcher result get
	

	public void init() throws IBScanException
	{
		// Draw SDK Version into Logo image
		IBScan.SdkVersion sdkVersion = getIBScan().getSdkVersion();
		try
		{
			m_bufImgLog = ImageIO.read(m_urlLogoImg);
		}
		catch (IOException e)
		{
			e.printStackTrace();
	}
		Graphics2D g = (Graphics2D) m_bufImgLog.getGraphics();
		Font oldFont = g.getFont();
		Color oldForeColor = g.getColor();
		g.setColor(Color.WHITE);
		g.drawString("Copyright (c) Integrated Biometrics", 485, 65);
		//Font drawFont = new Font("Dialog", Font.PLAIN, 19);
		Font drawFont = new Font("SansSerif", Font.PLAIN, 30);
		g.setFont(drawFont);
		g.drawString("SDK V " + sdkVersion.product, 485, 45);
		g.setFont(oldFont);
		g.setColor(oldForeColor);
		lblLogo.setIcon(new ImageIcon(m_bufImgLog));
		
		m_ImgSaveFolder = System.getProperty("user.dir");
		
		m_cboSmearLevel.addItem("LOW");
		m_cboSmearLevel.addItem("MEDIUM");
		m_cboSmearLevel.addItem("HIGH");
		m_cboSmearLevel.setSelectedIndex(1);
		
		m_cboSpoofLevel.addItem("1");
		m_cboSpoofLevel.addItem("2");
		m_cboSpoofLevel.addItem("3");
		m_cboSpoofLevel.addItem("4");
		m_cboSpoofLevel.addItem("5"); 
		m_cboSpoofLevel.setSelectedIndex(2);

		
		//////////////////////////////////////////////////////////////////////////////////////
		int destWidth = pnlImagePreview.getWidth()-20;
		int destHeight = pnlImagePreview.getHeight()-20;
		int outImageSize = destWidth * destHeight;

		m_drawBuffer = new byte[outImageSize];
		m_grayscaleImageJ = new BufferedImage(destWidth, destHeight, BufferedImage.TYPE_BYTE_GRAY);
		m_grayscaleImageData = ((DataBufferByte)m_grayscaleImageJ.getRaster().getDataBuffer()).getData();
		m_drawImageJ = new BufferedImage(destWidth, destHeight, BufferedImage.TYPE_4BYTE_ABGR);

		OnMsg_UpdateDeviceList();

		_TimerTaskThreadCallback thread = new _TimerTaskThreadCallback(__TIMER_STATUS_DELAY__);
		thread.start();
	}

	////////////////////////////////////////////////////////////////////////////////////////////
	//User defined functions

	/*
	 * Timer task with using Thread
	 */
	class _TimerTaskThreadCallback extends Thread
	{
		private int timeInterval;

		_TimerTaskThreadCallback(int timeInterval)
		{
			this.timeInterval = timeInterval;
				}

		@Override
		public void run()
		{
			while (!Thread.currentThread().isInterrupted()) {
					if (getIBScanDevice() != null) {
					OnMsg_DrawFingerQuality();

					if (m_bNeedClearPlaten)
						m_bBlank = !m_bBlank;
					}

				_Sleep(timeInterval);

				try {
					Thread.sleep(timeInterval);
				} catch (InterruptedException e) {
					e.printStackTrace();
				}
				}
			}

		}

	/*
	 * Initialize Device with using Thread
	 */
	class _InitializeDeviceThreadCallback extends Thread
	{
		private int devIndex;

		_InitializeDeviceThreadCallback(int devIndex)
		{
			this.devIndex = devIndex;
			}

		@Override
		public void run()
		{
			try
			{
				m_bInitializing = true;
				
				if (m_nDeviceLockState == DEVICE_LOCKED || m_nDeviceLockState == DEVICE_KEY_INVALID)
				{
					String m_strCustomerKey = JOptionPane.showInputDialog("Customer Key");
					if (m_strCustomerKey == null) // Value is null
					{
						m_bInitializing = false;
						OnMsg_UpdateDisplayResources();
						return;
					}
					else // m_strCustomerKey has not null, Try to unlock
					{
						getIBScan().setCustomerKey(this.devIndex, HashType.SHA256, m_strCustomerKey);
					}
				}
				
				
				IBScanDevice ibScanDeviceNew = getIBScan().openDevice(this.devIndex);
				setIBScanDevice(ibScanDeviceNew);
				m_bInitializing = false;

				m_LedState = getIBScanDevice().getOperableLEDs();

				OnMsg_CaptureSeqStart();
			 }
			catch (IBScanException ibse)
			{
				m_bInitializing = false;

				if (ibse.getType().equals(IBScanException.Type.DEVICE_ACTIVE))
				{
					_SetStatusBarMessage("[Error Code =-203] Device initialization failed because in use by another thread/process.");
				}
				else if (ibse.getType().equals(IBScanException.Type.USB20_REQUIRED))
				{
					_SetStatusBarMessage("[Error Code =-209] Device initialization failed because SDK only works with USB 2.0.");
				}
				else if (ibse.getType().equals(IBScanException.Type.DEVICE_HIGHER_SDK_REQUIRED))
				{
					try
					{
						m_minSDKVersion = getIBScan().getRequiredSDKVersion(this.devIndex);
						_SetStatusBarMessage("[Error Code =-214] Devcie initialization failed because SDK Version " + m_minSDKVersion + " is required at least.");
					}
					catch (IBScanException e)
					{
					}
				}
				else
				{
					try {
						_SetStatusBarMessage("[Error code = "+ ibse.getType().toCode()+"] Device initialization failed. "+getIBScan().getErrorString(ibse.getType().toCode()));
					} catch (IBScanException e) {
						e.printStackTrace();
					}
					
				}

				OnMsg_UpdateDisplayResources();
			}
		}
	}
	
	/*
	protected void _DrawOverlay_DispInvailedArea(Graphics2D g, int width, int height)
	{
		boolean bDrawInvalidArea = false;

		for (int i=0; i<4; i++)
		{
			if (m_FingerQuality[i] == IBScanDevice.FingerQualityState.INVALID_AREA_TOP ||
				m_FingerQuality[i] == IBScanDevice.FingerQualityState.INVALID_AREA_LEFT ||
				m_FingerQuality[i] == IBScanDevice.FingerQualityState.INVALID_AREA_RIGHT ||
				m_FingerQuality[i] == IBScanDevice.FingerQualityState.INVALID_AREA_BOTTOM)
			{
				bDrawInvalidArea = true;
			}
		}

		if (bDrawInvalidArea)
		{
			final int arrow_width = 20;
			final int arrow_thickness = 10;
			final int arrow_pos = 30;
			final int arrow_gab = 5;

			Color oldColor = g.getColor();
			g.setColor(Color.RED);
			g.setStroke(new BasicStroke(1));

			for( int i=0; i<4; i++ )
			{
				if (m_FingerQuality[i] == IBScanDevice.FingerQualityState.INVALID_AREA_TOP)
				{
					int[] aptPoly_x = new int[4];
					int[] aptPoly_y = new int[4];
					
					aptPoly_x[0] = width/2;
					aptPoly_y[0] = arrow_pos;
					aptPoly_x[1] = (aptPoly_x[0] + arrow_width);
					aptPoly_y[1] = (aptPoly_y[0] - arrow_width);
					aptPoly_x[2] = (aptPoly_x[0]);
					aptPoly_y[2] = (aptPoly_y[0] - arrow_thickness);
					aptPoly_x[3] = (aptPoly_x[0] - arrow_width);
					aptPoly_y[3] = (aptPoly_y[0] - arrow_width);
					g.fillPolygon(aptPoly_x, aptPoly_y, 4);
					
					aptPoly_x[0] = width/2;
					aptPoly_y[0] = (arrow_pos+arrow_thickness+arrow_gab);
					aptPoly_x[1] = (aptPoly_x[0] + arrow_width);
					aptPoly_y[1] = (aptPoly_y[0] - arrow_width);
					aptPoly_x[2] = (aptPoly_x[0]);
					aptPoly_y[2] = (aptPoly_y[0] - arrow_thickness);
					aptPoly_x[3] = (aptPoly_x[0] - arrow_width);
					aptPoly_y[3] = (aptPoly_y[0] - arrow_width);
					g.fillPolygon(aptPoly_x, aptPoly_y, 4);
				}

				if (m_FingerQuality[i] == IBScanDevice.FingerQualityState.INVALID_AREA_BOTTOM)
				{
					int[] aptPoly_x = new int[4];
					int[] aptPoly_y = new int[4];

					aptPoly_x[0] = width/2;
					aptPoly_y[0] = (height - arrow_pos);
					aptPoly_x[1] = (aptPoly_x[0] - arrow_width);
					aptPoly_y[1] = (aptPoly_y[0] + arrow_width);
					aptPoly_x[2] = (aptPoly_x[0]);
					aptPoly_y[2] = (aptPoly_y[0] + arrow_thickness);
					aptPoly_x[3] = (aptPoly_x[0] + arrow_width);
					aptPoly_y[3] = (aptPoly_y[0] + arrow_width);
					g.fillPolygon(aptPoly_x, aptPoly_y, 4);

					aptPoly_x[0] = width/2;
					aptPoly_y[0] = (height - arrow_thickness - arrow_gab - arrow_pos);
					aptPoly_x[1] = (aptPoly_x[0] - arrow_width);
					aptPoly_y[1] = (aptPoly_y[0] + arrow_width);
					aptPoly_x[2] = (aptPoly_x[0]);
					aptPoly_y[2] = (aptPoly_y[0] + arrow_thickness);
					aptPoly_x[3] = (aptPoly_x[0] + arrow_width);
					aptPoly_y[3] = (aptPoly_y[0] + arrow_width);
					g.fillPolygon(aptPoly_x, aptPoly_y, 4);
				}

				if( m_FingerQuality[i] == IBScanDevice.FingerQualityState.INVALID_AREA_LEFT )
				{
					int[] aptPoly_x = new int[4];
					int[] aptPoly_y = new int[4];

					aptPoly_x[0] = arrow_pos;
					aptPoly_y[0] = (height/2);
					aptPoly_x[1] = (aptPoly_x[0] - arrow_width);
					aptPoly_y[1] = (aptPoly_y[0] + arrow_width);
					aptPoly_x[2] = (aptPoly_x[0] - arrow_thickness);
					aptPoly_y[2] = (aptPoly_y[0]);
					aptPoly_x[3] = (aptPoly_x[0] - arrow_width);
					aptPoly_y[3] = (aptPoly_y[0] - arrow_width);
					g.fillPolygon(aptPoly_x, aptPoly_y, 4);

					aptPoly_x[0] = (arrow_pos+arrow_thickness+arrow_gab);
					aptPoly_y[0] = (height/2);
					aptPoly_x[1] = (aptPoly_x[0] - arrow_width);
					aptPoly_y[1] = (aptPoly_y[0] + arrow_width);
					aptPoly_x[2] = (aptPoly_x[0] - arrow_thickness);
					aptPoly_y[2] = (aptPoly_y[0]);
					aptPoly_x[3] = (aptPoly_x[0] - arrow_width);
					aptPoly_y[3] = (aptPoly_y[0] - arrow_width);
					g.fillPolygon(aptPoly_x, aptPoly_y, 4);
				}

				if( m_FingerQuality[i] == IBScanDevice.FingerQualityState.INVALID_AREA_RIGHT )
				{
					int[] aptPoly_x = new int[4];
					int[] aptPoly_y = new int[4];

					aptPoly_x[0] = (width - arrow_pos);
					aptPoly_y[0] = (height/2);
					aptPoly_x[1] = (aptPoly_x[0] + arrow_width);
					aptPoly_y[1] = (aptPoly_y[0] + arrow_width);
					aptPoly_x[2] = (aptPoly_x[0] + arrow_thickness);
					aptPoly_y[2] = (aptPoly_y[0]);
					aptPoly_x[3] = (aptPoly_x[0] + arrow_width);
					aptPoly_y[3] = (aptPoly_y[0] - arrow_width);
					g.fillPolygon(aptPoly_x, aptPoly_y, 4);

					aptPoly_x[0] = (width - arrow_pos-arrow_thickness-arrow_gab);
					aptPoly_y[0] = (height/2);
					aptPoly_x[1] = (aptPoly_x[0] + arrow_width);
					aptPoly_y[1] = (aptPoly_y[0] + arrow_width);
					aptPoly_x[2] = (aptPoly_x[0] + arrow_thickness);
					aptPoly_y[2] = (aptPoly_y[0]);
					aptPoly_x[3] = (aptPoly_x[0] + arrow_width);
					aptPoly_y[3] = (aptPoly_y[0] - arrow_width);
					g.fillPolygon(aptPoly_x, aptPoly_y, 4);
				}
						
				g.setColor(oldColor);
			}
		}
					}
*/

	protected void _DrawOverlay_ImageText(Graphics2D g)
	{
		Font oldFont = g.getFont();
		Color oldForeColor = g.getColor();
		if (m_bNeedClearPlaten)
			g.setColor(Color.RED);
		else
			g.setColor(Color.BLUE);
		Font drawFont = new Font("Dialog", Font.BOLD, 12);
		g.setFont(drawFont);
		g.drawString(m_strImageMessage, 10, 20);
		g.setFont(oldFont);
		g.setColor(oldForeColor);
	}

	protected void _DrawOverlay_WarningOfClearPlaten(Graphics2D g, int left, int top, int width, int height)
	{
		if (getIBScanDevice() == null)
			return;

	    boolean idle = !m_bInitializing && ( m_nCurrentCaptureStep == -1 );

	    if (!idle && m_bNeedClearPlaten && m_bBlank)
	    {
			Color oldColor = g.getColor();
			g.setColor(Color.RED);
			g.setStroke(new BasicStroke(10));
			g.drawRect(left, top, width-1, height-1);
			g.setColor(oldColor);
					}
				}
				
	protected void _DrawOverlay_ResultSegmentImage(Graphics2D g, ImageData image, int outWidth, int outHeight)
				{
		if (image.isFinal)
		{
			if (m_chkDrawSegmentImage.isSelected())
			{
				// Draw quadrangle for the segment image
				double scaleFactor;
				int leftMargin = 0;
				int topMargin = 0;
				int left = 0, top = 0;
				int tmp_width = outWidth;
				int tmp_height = outHeight;
				int imgWidth = image.width;
				int imgHeight = image.height;
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

				dispWidth = outWidth;
				dispHeight = outHeight;

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
				scaleFactor = (double)dispWidth / image.width;
				leftMargin = dispImgX;
				topMargin = dispImgY;
				///////////////////////////////////////////////////////////////////////////////////

				Color oldColor = g.getColor();
				g.setColor(new Color(0, 128 ,0));
				g.setStroke(new BasicStroke(1));
				for (int i=0; i<m_nSegmentImageArrayCount; i++)
				{
					int x1, x2, x3, x4, y1, y2, y3, y4;
					x1 = leftMargin + (int)(m_SegmentPositionArray[i].x1*scaleFactor);
					x2 = leftMargin + (int)(m_SegmentPositionArray[i].x2*scaleFactor);
					x3 = leftMargin + (int)(m_SegmentPositionArray[i].x3*scaleFactor);
					x4 = leftMargin + (int)(m_SegmentPositionArray[i].x4*scaleFactor);
					y1 = topMargin +  (int)(m_SegmentPositionArray[i].y1*scaleFactor);
					y2 = topMargin +  (int)(m_SegmentPositionArray[i].y2*scaleFactor);
					y3 = topMargin +  (int)(m_SegmentPositionArray[i].y3*scaleFactor);
					y4 = topMargin +  (int)(m_SegmentPositionArray[i].y4*scaleFactor);

					g.drawLine(x1, y1, x2, y2);
					g.drawLine(x2, y2, x3, y3);
					g.drawLine(x3, y3, x4, y4);
					g.drawLine(x4, y4, x1, y1);
			}
				g.setColor(oldColor);
				}
			}

		}

	protected void _DrawOverlay_RollGuideLine(Graphics2D g, ImageData image, int width, int height)
	{
		if (getIBScanDevice() == null || m_nCurrentCaptureStep == -1)
			return;

		if (m_ImageType == IBScanDevice.ImageType.ROLL_SINGLE_FINGER)
		{
			RollingData rollingdata;
			try
			{
				rollingdata = getIBScanDevice().getRollingInfo();

			}
			catch (IBScanException e)
			{
				rollingdata = null;
		}

			if ( (rollingdata != null) && rollingdata.rollingLineX > 0 &&
				 (rollingdata.rollingState.equals(IBScanDevice.RollingState.TAKE_ACQUISITION) ||
				  rollingdata.rollingState.equals(IBScanDevice.RollingState.COMPLETE_ACQUISITION)) )
			{
				double scaleFactor = (double)width / image.width;
				int LineX = (int)(rollingdata.rollingLineX*scaleFactor);	

				// Guide line for rolling
				if (rollingdata.rollingState.equals(IBScanDevice.RollingState.TAKE_ACQUISITION))
					g.setColor(Color.RED);
				else if (rollingdata.rollingState.equals(IBScanDevice.RollingState.COMPLETE_ACQUISITION))
					g.setColor(Color.GREEN);

				if (rollingdata.rollingLineX > -1)
				{
					g.setStroke(new BasicStroke(2));
					g.drawLine(LineX, 0, LineX, height);
	}
	}
		}
	}


	protected void _BeepFail()
		{
	    try
		{
	    	IBScanDevice.BeeperType beeperType = getIBScanDevice().getOperableBeeper();
	    	if (beeperType != IBScanDevice.BeeperType.BEEPER_TYPE_NONE)
	    	{
				getIBScanDevice().setBeeper(IBScanDevice.BeepPattern.BEEP_PATTERN_GENERIC, 2/*Sol*/, 12/*300ms = 12*25ms*/, 0, 0);
			    _Sleep(150);
			    getIBScanDevice().setBeeper(IBScanDevice.BeepPattern.BEEP_PATTERN_GENERIC, 2/*Sol*/, 6/*150ms = 6*25ms*/, 0, 0);
			    _Sleep(150);
			    getIBScanDevice().setBeeper(IBScanDevice.BeepPattern.BEEP_PATTERN_GENERIC, 2/*Sol*/, 6/*150ms = 6*25ms*/, 0, 0);
			    _Sleep(150);
			    getIBScanDevice().setBeeper(IBScanDevice.BeepPattern.BEEP_PATTERN_GENERIC, 2/*Sol*/, 6/*150ms = 6*25ms*/, 0, 0);
	}
	}
		catch (IBScanException ibse)
		{
			try
			{
				// devices for without beep chip 
	    		PlaySound.tone(3500, 300);
	    		_Sleep(150);
	    		PlaySound.tone(3500, 150);
	    		_Sleep(150);
	    		PlaySound.tone(3500, 150);
	    		_Sleep(150);
	    		PlaySound.tone(3500, 150);
	}
			catch (LineUnavailableException e)
			{
				e.printStackTrace();
		}
		}
		}

	protected void _BeepSuccess()
	{
	    try
	    {
	    	IBScanDevice.BeeperType beeperType = getIBScanDevice().getOperableBeeper();
	    	if (beeperType != IBScanDevice.BeeperType.BEEPER_TYPE_NONE)
	    	{
				getIBScanDevice().setBeeper(IBScanDevice.BeepPattern.BEEP_PATTERN_GENERIC, 2/*Sol*/, 4/*100ms = 4*25ms*/, 0, 0);
			    _Sleep(50);
			    getIBScanDevice().setBeeper(IBScanDevice.BeepPattern.BEEP_PATTERN_GENERIC, 2/*Sol*/, 4/*100ms = 4*25ms*/, 0, 0);
	}
	}
		catch (IBScanException ibse)
		{
			try
			{
				// devices for without beep chip 
	    		PlaySound.tone(3500, 100);
	    		_Sleep(50);
	    		PlaySound.tone(3500, 100);
	}
			catch (LineUnavailableException e)
			{
				e.printStackTrace();
	}
		}
	}

	protected void _BeepOk()
	{
	    try
	    {
	    	IBScanDevice.BeeperType beeperType = getIBScanDevice().getOperableBeeper();
	    	if (beeperType != IBScanDevice.BeeperType.BEEPER_TYPE_NONE)
	    	{
				getIBScanDevice().setBeeper(IBScanDevice.BeepPattern.BEEP_PATTERN_GENERIC, 2/*Sol*/, 4/*100ms = 4*25ms*/, 0, 0);
	    	}
	    }
		catch (IBScanException ibse)
		{
			try
			{
				// devices for without beep chip 
	    		PlaySound.tone(3500, 100);
			}
			catch (LineUnavailableException e)
			{
				e.printStackTrace();
			}	
		}
	}

	protected void _BeepDeviceCommunicationBreak()
	{
		try
		{
			for (int i=0; i<8; i++)
			{
	    		PlaySound.tone(3500, 100);
	    		_Sleep(100);
			}
		}
		catch (LineUnavailableException e)
		{
			e.printStackTrace();
		}	
	}
	
	protected void _Sleep(int time)
	{
		try
		{
			Thread.sleep(time);
		}
		catch (InterruptedException e)
		{
		}
		}

	protected void _SetTxtNFIQScore(final String s)
	{
		this.m_txtNFIQScore.setText(s);
	}
	
	protected void _SetTxtSpoofResult(final String s)
	{
		this.m_txtSpoofResult.setText(s);
	}
	
	
	
	protected void _SetTxtContrast(String s)
	{
		this.m_txtContrast.setText(s);
	}
	
	protected void _SetStatusBarMessage(String s)
	{
		this.m_txtStatusMessage.setText(s);
	}

	protected void _SetImageMessage(String s)
	{
		m_strImageMessage = s;
	}
	

	protected void _AddCaptureSeqVector(String PreCaptureMessage, String PostCaptuerMessage,
			IBScanDevice.ImageType imageType, int NumberOfFinger, String fingerName , FingerPosition fingerPosition)
	{
		CaptureInfo info = new CaptureInfo();
		info.PreCaptureMessage = PreCaptureMessage;
		info.PostCaptuerMessage = PostCaptuerMessage;
		info.ImageType = imageType;
		info.NumberOfFinger = NumberOfFinger;
		info.fingerName = fingerName;
		info.fingerPosition = fingerPosition;
		m_vecCaptureSeq.addElement(info);
	}
	
	protected void _UpdateCaptureSequences()
	{
		try
		{
			//store currently selected device
			String strSelectedText = "";
			int selectedSeq = m_cboCaptureSeq.getSelectedIndex();
			if (selectedSeq > -1)
				strSelectedText = m_cboCaptureSeq.getSelectedItem().toString();
					
			// populate combo box
			m_cboCaptureSeq.removeActionListener(m_cboCaptureSeq_Changed);
			m_cboCaptureSeq.removeAllItems();
			m_cboCaptureSeq.addActionListener(m_cboCaptureSeq_Changed);
			m_cboCaptureSeq.addItem("- Please select -");
	
			final int devIndex = this.m_cboUsbDevices.getSelectedIndex() - 1;
			IBScan.DeviceDesc devDesc = null; 
			if (devIndex > -1)
			{
				devDesc = getIBScan().getDeviceDescription(devIndex);
				//logPrintln(devDesc.toString());
				if ( (devDesc.productName.equals("WATSON")) ||
					 (devDesc.productName.equals("WATSON MINI")) ||
					 (devDesc.productName.equals("SHERLOCK_ROIC")) ||
					 (devDesc.productName.equals("SHERLOCK")) )
				{
					m_cboCaptureSeq.addItem(CAPTURE_SEQ_FLAT_SINGLE_FINGER);
					m_cboCaptureSeq.addItem(CAPTURE_SEQ_ROLL_SINGLE_FINGER);
					m_cboCaptureSeq.addItem(CAPTURE_SEQ_2_FLAT_FINGERS);
					m_cboCaptureSeq.addItem(CAPTURE_SEQ_10_SINGLE_FLAT_FINGERS);
					m_cboCaptureSeq.addItem(CAPTURE_SEQ_10_SINGLE_ROLLED_FINGERS);
				}
				else if ( (devDesc.productName.equals("COLUMBO")) ||
						  (devDesc.productName.equals("CURVE")) ||
						  (devDesc.productName.equals("COLUMBO MINI")) ||
						  (devDesc.productName.equals("DANNO")) ||
						  (devDesc.productName.equals("COLUMBO 2.0")))
				{
					m_cboCaptureSeq.addItem(CAPTURE_SEQ_FLAT_SINGLE_FINGER);
					m_cboCaptureSeq.addItem(CAPTURE_SEQ_10_SINGLE_FLAT_FINGERS);
				}
				else if ( (devDesc.productName.equals("HOLMES")) ||
						  (devDesc.productName.equals("KOJAK")) ||
						  (devDesc.productName.equals("FIVE-0")) ||
						  (devDesc.productName.equals("TF10")) ||
						  (devDesc.productName.equals("MF10")))
				{
					m_cboCaptureSeq.addItem(CAPTURE_SEQ_FLAT_SINGLE_FINGER);
					m_cboCaptureSeq.addItem(CAPTURE_SEQ_ROLL_SINGLE_FINGER);
					m_cboCaptureSeq.addItem(CAPTURE_SEQ_2_FLAT_FINGERS);
					m_cboCaptureSeq.addItem(CAPTURE_SEQ_4_FLAT_FINGERS);
					m_cboCaptureSeq.addItem(CAPTURE_SEQ_10_SINGLE_FLAT_FINGERS);
					m_cboCaptureSeq.addItem(CAPTURE_SEQ_10_SINGLE_ROLLED_FINGERS);
					m_cboCaptureSeq.addItem(CAPTURE_SEQ_10_FLAT_WITH_4_FINGER_SCANNER);
				}
			}
			
			if (devIndex >=0 )
			{
				if (devDesc.isLocked == true)
				{
					m_nDeviceLockState = DEVICE_LOCKED;
					m_lblLockedImg.setVisible(true);
					m_lblLocked.setVisible(true);
				}
				else // Unlocked
				{
					m_nDeviceLockState = DEVICE_UNLOCKED;
					m_lblLockedImg.setVisible(false);
					m_lblLocked.setVisible(false);
				}
			}
			else
			{
				m_nDeviceLockState = DEVICE_UNLOCKED;
				m_lblLockedImg.setVisible(false);
				m_lblLocked.setVisible(false);
			}
			
			if (selectedSeq > -1)
				this.m_cboCaptureSeq.setSelectedItem(strSelectedText);
			
			OnMsg_UpdateDisplayResources();
		}
		catch (IBScanException e)
		{
			e.printStackTrace();
		}
	}

	protected void _ReleaseDevice() throws IBScanException
	{
		if (getIBScanDevice() != null)
		{
			if (getIBScanDevice().isOpened() == true) {
				getIBScanDevice().close();
				setIBScanDevice(null);
			}
		}
		
		m_nCurrentCaptureStep = -1;
		m_bInitializing = false;
	}

	protected void _SaveBitmapImage(ImageData image, String fingerName)
	{
		if (m_ImgSaveFolder == "" || m_ImgSubFolder == "")
		{
			return;
		}
		
		String strFolder = m_ImgSaveFolder + File.separator + m_ImgSubFolder;
		File dirs = new File(strFolder);
		if (!dirs.exists())
		{
			if (!dirs.mkdirs())
			{
				return;
			}
		}
			
		String strFileName = strFolder + File.separator + "Image_" + m_nCurrentCaptureStep + "_" + fingerName +".bmp";

		try
		{
			getIBScanDevice().SaveBitmapImage(strFileName, image.buffer, image.width, image.height, image.pitch, image.resolutionX, image.resolutionY);
		}
		catch(IBScanException e)
		{
			e.printStackTrace();
		}
	}
	
	protected void _SaveWsqImage(ImageData image, String fingerName)
	{
		if (m_ImgSaveFolder == "" || m_ImgSubFolder == "")
		{
			return;
		}
		
		String strFolder = m_ImgSaveFolder + File.separator + m_ImgSubFolder;
		File dirs = new File(strFolder);
		if (!dirs.exists())
		{
			if (!dirs.mkdirs())
			{
				return;
			}
		}
			
		String strFileName = strFolder + File.separator + "Image_" + m_nCurrentCaptureStep + "_" + fingerName +".wsq";

		try
		{
			getIBScanDevice().wsqEncodeToFile(strFileName, image.buffer, image.width, image.height, image.pitch, image.bitsPerPixel, 500, 0.75, "");
		}
		catch (IBScanException e)
		{
			e.printStackTrace();
		}
	}
	
	protected void _SavePngImage(ImageData image, String fingerName)
	{
		if (m_ImgSaveFolder == "" || m_ImgSubFolder == "")
		{
			return;
		}
		
		String strFolder = m_ImgSaveFolder + File.separator + m_ImgSubFolder;
		File dirs = new File(strFolder);
		if (!dirs.exists())
		{
			if (!dirs.mkdirs())
			{
				return;
			}
		}
			
		String strFileName = strFolder + File.separator + "Image_" + m_nCurrentCaptureStep + "_" + fingerName +".png";

		try
		{
			getIBScanDevice().SavePngImage(strFileName, image.buffer, image.width, image.height, image.pitch, image.resolutionX, image.resolutionY);
		}
		catch (IBScanException e)
		{
			e.printStackTrace();
		}
	}
				
	protected void _SaveJP2Image(ImageData image, String fingerName)
	{
		if (m_ImgSaveFolder == "" || m_ImgSubFolder == "")
		{
			return;
		}
		
		String strFolder = m_ImgSaveFolder + File.separator + m_ImgSubFolder;
		File dirs = new File(strFolder);
		if (!dirs.exists())
		{
			if (!dirs.mkdirs())
			{
				return;
			}
		}
			
		String strFileName = strFolder + File.separator + "Image_" + m_nCurrentCaptureStep + "_" + fingerName +".jp2";

		try
		{
			getIBScanDevice().SaveJP2Image(strFileName, image.buffer, image.width, image.height, image.pitch, image.resolutionX, image.resolutionY , 80);
		}
		catch (IBScanException e)
		{
			e.printStackTrace();
		}
		catch( StackOverflowError e)
		{
			System.out.println("Exception :"+ e);
			e.printStackTrace();
		}
	}
	
	protected void _SaveISOImage(String fingerName)
	{
		if (m_ImgSaveFolder == "" || m_ImgSubFolder == "")
		{
			return;
		}
		
		String strFolder = m_ImgSaveFolder + File.separator + m_ImgSubFolder;
		File dirs = new File(strFolder);
		if (!dirs.exists())
		{
			if (!dirs.mkdirs())
			{
				return;
			}
		}
			
		//String strFileName = strFolder + File.separator + "Image_" + m_nCurrentCaptureStep + "_" + fingerName +".jp2";
		String[] strFileName = new String[6];
		strFileName[0] = strFolder + File.separator + "Image_" + m_nCurrentCaptureStep + "_" + fingerName +"_ISO_IEC_19794-2_2005.bin";
		strFileName[1] = strFolder + File.separator + "Image_" + m_nCurrentCaptureStep + "_" + fingerName +"_ISO_IEC_19794-4_2005.bin";
		strFileName[2] = strFolder + File.separator + "Image_" + m_nCurrentCaptureStep + "_" + fingerName +"_ISO_IEC_19794-2_2011.bin";
		strFileName[3] = strFolder + File.separator + "Image_" + m_nCurrentCaptureStep + "_" + fingerName +"_ISO_IEC_19794-4_2011.bin";
		strFileName[4] = strFolder + File.separator + "Image_" + m_nCurrentCaptureStep + "_" + fingerName +"_ANSI_INCITS_378_2004.bin";
		strFileName[5] = strFolder + File.separator + "Image_" + m_nCurrentCaptureStep + "_" + fingerName +"_ANSI_INCITS_381_2004.bin";
		
		StandardFormat[] standardFormat = new StandardFormat[6];
		standardFormat[0] = StandardFormat.STANDARD_FORMAT_ISO_19794_2_2005;
		standardFormat[1] = StandardFormat.STANDARD_FORMAT_ISO_19794_4_2005;
		standardFormat[2] = StandardFormat.STANDARD_FORMAT_ISO_19794_2_2011;
		standardFormat[3] = StandardFormat.STANDARD_FORMAT_ISO_19794_4_2011;
		standardFormat[4] = StandardFormat.STANDARD_FORMAT_ANSI_INCITS_378_2004;
		standardFormat[5] = StandardFormat.STANDARD_FORMAT_ANSI_INCITS_381_2004;
		
		StandardFormatData STDdata;
		ImageDataExt[] imageDataExt_Segments = (ImageDataExt[]) m_imageDataExtResult[1];
			
		try
		{
			for (int i=0; i<6; i++)
			{
				STDdata = (StandardFormatData) getIBScanDevice().ConvertImageToISOANSI(imageDataExt_Segments, (Integer) m_imageDataExtResult[2],
						ImageFormat.WSQ, standardFormat[i]); 
				getIBScanDevice().SaveStandardFile(STDdata, strFileName[i]);
			}
			
		}
		catch (IBScanException e)
		{
			e.printStackTrace();
		}
		catch( StackOverflowError e)
		{
			System.out.println("Exception :"+ e);
			e.printStackTrace();
		}
	}
	
	public void _SetLEDs(CaptureInfo info, int ledColor, boolean bBlink) 
	{
        try
        {
			LedState ledState = getIBScanDevice().getOperableLEDs();
			if (ledState.ledCount == 0)
			{
				return;
			}
        }
		catch (IBScanException ibse)
		{
			ibse.printStackTrace();
		}
		
		int setLEDs = 0;

        if (ledColor == __LED_COLOR_NONE__)
        {
            try
	        {
	        	getIBScanDevice().setLEDs(setLEDs);
	        }
			catch (IBScanException ibse)
			{
				ibse.printStackTrace();
			}

            return;
        }
	        
		if (m_LedState.ledType == IBScanDevice.LedType.FSCAN)
		{
			if (bBlink)
			{
				if (ledColor == __LED_COLOR_GREEN__)
				{
					setLEDs |= IBScanDevice.IBSU_LED_F_BLINK_GREEN;
				}
				else if(ledColor == __LED_COLOR_RED__)
				{
					setLEDs |= IBScanDevice.IBSU_LED_F_BLINK_RED;
				}
				else if(ledColor == __LED_COLOR_YELLOW__)
				{
					setLEDs |= IBScanDevice.IBSU_LED_F_BLINK_GREEN;
					setLEDs |= IBScanDevice.IBSU_LED_F_BLINK_RED;
				}
			}
			
			if (info.ImageType == IBScanDevice.ImageType.ROLL_SINGLE_FINGER)
			{
				setLEDs |= IBScanDevice.IBSU_LED_F_PROGRESS_ROLL;
			}
			
		    if( (info.fingerName.equals("SFF_Right_Thumb")) ||
			    (info.fingerName.equals("SRF_Right_Thumb")) )
			{
			    setLEDs |= IBScanDevice.IBSU_LED_F_PROGRESS_TWO_THUMB;
			    if( ledColor == __LED_COLOR_GREEN__ )
			    {
				    setLEDs |= IBScanDevice.IBSU_LED_F_RIGHT_THUMB_GREEN;
			    }
			    else if( ledColor == __LED_COLOR_RED__ )
			    {
				    setLEDs |= IBScanDevice.IBSU_LED_F_RIGHT_THUMB_RED;
			    }
			    else if( ledColor == __LED_COLOR_YELLOW__ )
			    {
				    setLEDs |= IBScanDevice.IBSU_LED_F_RIGHT_THUMB_GREEN;
				    setLEDs |= IBScanDevice.IBSU_LED_F_RIGHT_THUMB_RED;
			    }
		    }
		    else if( (info.fingerName.equals("SFF_Left_Thumb")) ||
			    (info.fingerName.equals("SRF_Left_Thumb")) )
		    {
			    setLEDs |= IBScanDevice.IBSU_LED_F_PROGRESS_TWO_THUMB;
			    if( ledColor == __LED_COLOR_GREEN__ )
			    {
				    setLEDs |= IBScanDevice.IBSU_LED_F_LEFT_THUMB_GREEN;
			    }
			    else if( ledColor == __LED_COLOR_RED__ )
			    {
				    setLEDs |= IBScanDevice.IBSU_LED_F_LEFT_THUMB_RED;
			    }
			    else if( ledColor == __LED_COLOR_YELLOW__ )
			    {
				    setLEDs |= IBScanDevice.IBSU_LED_F_LEFT_THUMB_GREEN;
				    setLEDs |= IBScanDevice.IBSU_LED_F_LEFT_THUMB_RED;
			    }
		    }
		    else if( (info.fingerName.equals("TFF_2_Thumbs")) )
		    {
			    setLEDs |= IBScanDevice.IBSU_LED_F_PROGRESS_TWO_THUMB;
			    if( ledColor == __LED_COLOR_GREEN__ )
			    {
				    setLEDs |= IBScanDevice.IBSU_LED_F_LEFT_THUMB_GREEN;
				    setLEDs |= IBScanDevice.IBSU_LED_F_RIGHT_THUMB_GREEN;
			    }
			    else if( ledColor == __LED_COLOR_RED__ )
			    {
				    setLEDs |= IBScanDevice.IBSU_LED_F_LEFT_THUMB_RED;
				    setLEDs |= IBScanDevice.IBSU_LED_F_RIGHT_THUMB_RED;
			    }
			    else if( ledColor == __LED_COLOR_YELLOW__ )
			    {
				    setLEDs |= IBScanDevice.IBSU_LED_F_LEFT_THUMB_GREEN;
				    setLEDs |= IBScanDevice.IBSU_LED_F_LEFT_THUMB_RED;
				    setLEDs |= IBScanDevice.IBSU_LED_F_RIGHT_THUMB_GREEN;
				    setLEDs |= IBScanDevice.IBSU_LED_F_RIGHT_THUMB_RED;
			    }
		    }
		    ///////////////////LEFT HAND////////////////////
		    else if( (info.fingerName.equals("SFF_Left_Index")) ||
			    (info.fingerName.equals("SRF_Left_Index")) )
		    {
			    setLEDs |= IBScanDevice.IBSU_LED_F_PROGRESS_LEFT_HAND;
			    if( ledColor == __LED_COLOR_GREEN__ )
			    {
				    setLEDs |= IBScanDevice.IBSU_LED_F_LEFT_INDEX_GREEN;
			    }
			    else if( ledColor == __LED_COLOR_RED__ )
			    {
				    setLEDs |= IBScanDevice.IBSU_LED_F_LEFT_INDEX_RED;
			    }
			    else if( ledColor == __LED_COLOR_YELLOW__ )
			    {
				    setLEDs |= IBScanDevice.IBSU_LED_F_LEFT_INDEX_GREEN;
				    setLEDs |= IBScanDevice.IBSU_LED_F_LEFT_INDEX_RED;
			    }
		    }
		    else if( (info.fingerName.equals("SFF_Left_Middle")) ||
			    (info.fingerName.equals("SRF_Left_Middle")) )
		    {
			    setLEDs |= IBScanDevice.IBSU_LED_F_PROGRESS_LEFT_HAND;
			    if( ledColor == __LED_COLOR_GREEN__ )
			    {
				    setLEDs |= IBScanDevice.IBSU_LED_F_LEFT_MIDDLE_GREEN;
			    }
			    else if( ledColor == __LED_COLOR_RED__ )
			    {
				    setLEDs |= IBScanDevice.IBSU_LED_F_LEFT_MIDDLE_RED;
			    }
			    else if( ledColor == __LED_COLOR_YELLOW__ )
			    {
				    setLEDs |= IBScanDevice.IBSU_LED_F_LEFT_MIDDLE_GREEN;
				    setLEDs |= IBScanDevice.IBSU_LED_F_LEFT_MIDDLE_RED;
			    }
		    }
		    else if( (info.fingerName.equals("SFF_Left_Ring")) ||
			    (info.fingerName.equals("SRF_Left_Ring")) )
		    {
			    setLEDs |= IBScanDevice.IBSU_LED_F_PROGRESS_LEFT_HAND;
			    if( ledColor == __LED_COLOR_GREEN__ )
			    {
				    setLEDs |= IBScanDevice.IBSU_LED_F_LEFT_RING_GREEN;
			    }
			    else if( ledColor == __LED_COLOR_RED__ )
			    {
				    setLEDs |= IBScanDevice.IBSU_LED_F_LEFT_RING_RED;
			    }
			    else if( ledColor == __LED_COLOR_YELLOW__ )
			    {
				    setLEDs |= IBScanDevice.IBSU_LED_F_LEFT_RING_GREEN;
				    setLEDs |= IBScanDevice.IBSU_LED_F_LEFT_RING_RED;
			    }
		    }
		    else if( (info.fingerName.equals("SFF_Left_Little")) ||
			    (info.fingerName.equals("SRF_Left_Little")) )
		    {
			    setLEDs |= IBScanDevice.IBSU_LED_F_PROGRESS_LEFT_HAND;
			    if( ledColor == __LED_COLOR_GREEN__ )
			    {
				    setLEDs |= IBScanDevice.IBSU_LED_F_LEFT_LITTLE_GREEN;
			    }
			    else if( ledColor == __LED_COLOR_RED__ )
			    {
				    setLEDs |= IBScanDevice.IBSU_LED_F_LEFT_LITTLE_RED;
			    }
			    else if( ledColor == __LED_COLOR_YELLOW__ )
			    {
				    setLEDs |= IBScanDevice.IBSU_LED_F_LEFT_LITTLE_GREEN;
				    setLEDs |= IBScanDevice.IBSU_LED_F_LEFT_LITTLE_RED;
			    }
		    }
		    else if( (info.fingerName.equals("4FF_Left_4_Fingers")) )
		    {
			    setLEDs |= IBScanDevice.IBSU_LED_F_PROGRESS_LEFT_HAND;
			    if( ledColor == __LED_COLOR_GREEN__ )
			    {
				    setLEDs |= IBScanDevice.IBSU_LED_F_LEFT_INDEX_GREEN;
				    setLEDs |= IBScanDevice.IBSU_LED_F_LEFT_MIDDLE_GREEN;
				    setLEDs |= IBScanDevice.IBSU_LED_F_LEFT_RING_GREEN;
				    setLEDs |= IBScanDevice.IBSU_LED_F_LEFT_LITTLE_GREEN;
			    }
			    else if( ledColor == __LED_COLOR_RED__ )
			    {
				    setLEDs |= IBScanDevice.IBSU_LED_F_LEFT_INDEX_RED;
				    setLEDs |= IBScanDevice.IBSU_LED_F_LEFT_MIDDLE_RED;
				    setLEDs |= IBScanDevice.IBSU_LED_F_LEFT_RING_RED;
				    setLEDs |= IBScanDevice.IBSU_LED_F_LEFT_LITTLE_RED;
			    }
			    else if( ledColor == __LED_COLOR_YELLOW__ )
			    {
				    setLEDs |= IBScanDevice.IBSU_LED_F_LEFT_INDEX_GREEN;
				    setLEDs |= IBScanDevice.IBSU_LED_F_LEFT_MIDDLE_GREEN;
				    setLEDs |= IBScanDevice.IBSU_LED_F_LEFT_RING_GREEN;
				    setLEDs |= IBScanDevice.IBSU_LED_F_LEFT_LITTLE_GREEN;
				    setLEDs |= IBScanDevice.IBSU_LED_F_LEFT_INDEX_RED;
				    setLEDs |= IBScanDevice.IBSU_LED_F_LEFT_MIDDLE_RED;
				    setLEDs |= IBScanDevice.IBSU_LED_F_LEFT_RING_RED;
				    setLEDs |= IBScanDevice.IBSU_LED_F_LEFT_LITTLE_RED;
			    }
		    }
		    ///////////RIGHT HAND /////////////////////////
		    else if( (info.fingerName.equals("SFF_Right_Index")) ||
			    (info.fingerName.equals("SRF_Right_Index")) )
		    {
			    setLEDs |= IBScanDevice.IBSU_LED_F_PROGRESS_RIGHT_HAND;
			    if( ledColor == __LED_COLOR_GREEN__ )
			    {
				    setLEDs |= IBScanDevice.IBSU_LED_F_RIGHT_INDEX_GREEN;
			    }
			    else if( ledColor == __LED_COLOR_RED__ )
			    {
				    setLEDs |= IBScanDevice.IBSU_LED_F_RIGHT_INDEX_RED;
			    }
			    else if( ledColor == __LED_COLOR_YELLOW__ )
			    {
				    setLEDs |= IBScanDevice.IBSU_LED_F_RIGHT_INDEX_GREEN;
				    setLEDs |= IBScanDevice.IBSU_LED_F_RIGHT_INDEX_RED;
			    }
		    }
		    else if( (info.fingerName.equals("SFF_Right_Middle")) ||
			    (info.fingerName.equals("SRF_Right_Middle")) )
		    {
			    setLEDs |= IBScanDevice.IBSU_LED_F_PROGRESS_RIGHT_HAND;
			    if( ledColor == __LED_COLOR_GREEN__ )
			    {
				    setLEDs |= IBScanDevice.IBSU_LED_F_RIGHT_MIDDLE_GREEN;
			    }
			    else if( ledColor == __LED_COLOR_RED__ )
			    {
				    setLEDs |= IBScanDevice.IBSU_LED_F_RIGHT_MIDDLE_RED;
			    }
			    else if( ledColor == __LED_COLOR_YELLOW__ )
			    {
				    setLEDs |= IBScanDevice.IBSU_LED_F_RIGHT_MIDDLE_GREEN;
				    setLEDs |= IBScanDevice.IBSU_LED_F_RIGHT_MIDDLE_RED;
			    }
		    }
		    else if( (info.fingerName.equals("SFF_Right_Ring")) ||
			    (info.fingerName.equals("SRF_Right_Ring")) )
		    {
			    setLEDs |= IBScanDevice.IBSU_LED_F_PROGRESS_RIGHT_HAND;
			    if( ledColor == __LED_COLOR_GREEN__ )
			    {
				    setLEDs |= IBScanDevice.IBSU_LED_F_RIGHT_RING_GREEN;
			    }
			    else if( ledColor == __LED_COLOR_RED__ )
			    {
				    setLEDs |= IBScanDevice.IBSU_LED_F_RIGHT_RING_RED;
			    }
			    else if( ledColor == __LED_COLOR_YELLOW__ )
			    {
				    setLEDs |= IBScanDevice.IBSU_LED_F_RIGHT_RING_GREEN;
				    setLEDs |= IBScanDevice.IBSU_LED_F_RIGHT_RING_RED;
			    }
		    }
		    else if( (info.fingerName.equals("SFF_Right_Little")) ||
			    (info.fingerName.equals("SRF_Right_Little")) )
		    {
			    setLEDs |= IBScanDevice.IBSU_LED_F_PROGRESS_RIGHT_HAND;
			    if( ledColor == __LED_COLOR_GREEN__ )
			    {
				    setLEDs |= IBScanDevice.IBSU_LED_F_RIGHT_LITTLE_GREEN;
			    }
			    else if( ledColor == __LED_COLOR_RED__ )
			    {
				    setLEDs |= IBScanDevice.IBSU_LED_F_RIGHT_LITTLE_RED;
			    }
			    else if( ledColor == __LED_COLOR_YELLOW__ )
			    {
				    setLEDs |= IBScanDevice.IBSU_LED_F_RIGHT_LITTLE_GREEN;
				    setLEDs |= IBScanDevice.IBSU_LED_F_RIGHT_LITTLE_RED;
			    }
		    }
		    else if( (info.fingerName.equals("4FF_Right_4_Fingers")) )
		    {
			    setLEDs |= IBScanDevice.IBSU_LED_F_PROGRESS_RIGHT_HAND;
			    if( ledColor == __LED_COLOR_GREEN__ )
			    {
				    setLEDs |= IBScanDevice.IBSU_LED_F_RIGHT_INDEX_GREEN;
				    setLEDs |= IBScanDevice.IBSU_LED_F_RIGHT_MIDDLE_GREEN;
				    setLEDs |= IBScanDevice.IBSU_LED_F_RIGHT_RING_GREEN;
				    setLEDs |= IBScanDevice.IBSU_LED_F_RIGHT_LITTLE_GREEN;
			    }
			    else if( ledColor == __LED_COLOR_RED__ )
			    {
				    setLEDs |= IBScanDevice.IBSU_LED_F_RIGHT_INDEX_RED;
				    setLEDs |= IBScanDevice.IBSU_LED_F_RIGHT_MIDDLE_RED;
				    setLEDs |= IBScanDevice.IBSU_LED_F_RIGHT_RING_RED;
				    setLEDs |= IBScanDevice.IBSU_LED_F_RIGHT_LITTLE_RED;
			    }
			    else if( ledColor == __LED_COLOR_YELLOW__ )
			    {
				    setLEDs |= IBScanDevice.IBSU_LED_F_RIGHT_INDEX_GREEN;
				    setLEDs |= IBScanDevice.IBSU_LED_F_RIGHT_MIDDLE_GREEN;
				    setLEDs |= IBScanDevice.IBSU_LED_F_RIGHT_RING_GREEN;
				    setLEDs |= IBScanDevice.IBSU_LED_F_RIGHT_LITTLE_GREEN;
				    setLEDs |= IBScanDevice.IBSU_LED_F_RIGHT_INDEX_RED;
				    setLEDs |= IBScanDevice.IBSU_LED_F_RIGHT_MIDDLE_RED;
				    setLEDs |= IBScanDevice.IBSU_LED_F_RIGHT_RING_RED;
				    setLEDs |= IBScanDevice.IBSU_LED_F_RIGHT_LITTLE_RED;
			    }
			}
		    
	        if (ledColor == __LED_COLOR_NONE__)
	        {
	            setLEDs = 0;
	        }

	        try
	        {
	        	getIBScanDevice().setLEDs(setLEDs);
	        }
			catch (IBScanException ibse)
			{
				ibse.printStackTrace();
			}
		}
	}

	////////////////////////////////////////////////////////////////////////////////////////////
	// Event-dispatch threads
	private void OnMsg_SetStatusBarMessage(final String s)
	{
		javax.swing.SwingUtilities.invokeLater(new Runnable()
		{

		@Override
			public void run()
			{
				_SetStatusBarMessage(s);
			}
		});
	}


	private void OnMsg_SetTxtNFIQScore(final String s)
	{
		javax.swing.SwingUtilities.invokeLater(new Runnable()
		{

			@Override
			public void run()
			{
				_SetTxtNFIQScore(s);
			}
		});
			}
	
	private void OnMsg_SetTxtSpoofResult(final String s)
	{
		javax.swing.SwingUtilities.invokeLater(new Runnable()
		{

			@Override
			public void run()
			{
				_SetTxtSpoofResult(s);
			}
		});
	}


	private void OnMsg_Beep(final int beepType)
	{
		javax.swing.SwingUtilities.invokeLater(new Runnable()
		{

			@Override
			public void run()
			{
				if( beepType == __BEEP_FAIL__ )
					_BeepFail();
				else if( beepType == __BEEP_SUCCESS__ )
					_BeepSuccess();
				else if( beepType == __BEEP_OK__ )
					_BeepOk();
				else if( beepType == __BEEP_DEVICE_COMMUNICATION_BREAK__ )
					_BeepDeviceCommunicationBreak();
			}
		});
		}

	private void OnMsg_CaptureSeqStart()
	{
		javax.swing.SwingUtilities.invokeLater(new Runnable()
		{

		@Override
			public void run()
			{
				if (getIBScanDevice() == null)
				{
					OnMsg_UpdateDisplayResources();
					return;
				}

				String strCaptureSeq = "";
				int nSelectedSeq = m_cboCaptureSeq.getSelectedIndex();
				if (nSelectedSeq > -1)
					strCaptureSeq = m_cboCaptureSeq.getSelectedItem().toString();
				
				m_vecCaptureSeq.clear();
				
/** Please refer to definition below
protected final String CAPTURE_SEQ_FLAT_SINGLE_FINGER 				= "Single flat finger";
protected final String CAPTURE_SEQ_ROLL_SINGLE_FINGER 				= "Single rolled finger";
protected final String CAPTURE_SEQ_2_FLAT_FINGERS 					= "2 flat fingers";
protected final String CAPTURE_SEQ_10_SINGLE_FLAT_FINGERS 			= "10 single flat fingers";
protected final String CAPTURE_SEQ_10_SINGLE_ROLLED_FINGERS 		= "10 single rolled fingers";
protected final String CAPTURE_SEQ_4_FLAT_FINGERS 					= "4 flat fingers";
protected final String CAPTURE_SEQ_10_FLAT_WITH_4_FINGER_SCANNER 	= "10 flat fingers with 4-finger scanner";
*/
				if (strCaptureSeq.equals(CAPTURE_SEQ_FLAT_SINGLE_FINGER))
				{
					_AddCaptureSeqVector("Please put a single finger on the sensor!",
							"Keep finger on the sensor!",
							IBScanDevice.ImageType.FLAT_SINGLE_FINGER,
							1,
							"SFF_Unknown", FingerPosition.UNKNOWN);
				}


				if (strCaptureSeq.equals(CAPTURE_SEQ_ROLL_SINGLE_FINGER))
				{
					_AddCaptureSeqVector("Please put a single finger on the sensor!",
							"Roll finger!",
							IBScanDevice.ImageType.ROLL_SINGLE_FINGER,
							1,
							"SRF_Unknown", FingerPosition.UNKNOWN);
				}

				if( strCaptureSeq == CAPTURE_SEQ_2_FLAT_FINGERS )
				{
					_AddCaptureSeqVector("Please put two fingers on the sensor!",
							"Keep fingers on the sensor!",
							IBScanDevice.ImageType.FLAT_TWO_FINGERS,
							2,
							"TFF_Unknown", FingerPosition.UNKNOWN);
				}

				if( strCaptureSeq == CAPTURE_SEQ_10_SINGLE_FLAT_FINGERS )
				{
					_AddCaptureSeqVector("Please put right thumb on the sensor!",
							"Keep fingers on the sensor!",
							IBScanDevice.ImageType.FLAT_SINGLE_FINGER,
							1,
							"SFF_Right_Thumb", FingerPosition.RIGHT_THUMB);

					_AddCaptureSeqVector("Please put right index on the sensor!",
							"Keep fingers on the sensor!",
							IBScanDevice.ImageType.FLAT_SINGLE_FINGER,
							1,
							"SFF_Right_Index", FingerPosition.RIGHT_INDEX_FINGER);

					_AddCaptureSeqVector("Please put right middle on the sensor!",
							"Keep fingers on the sensor!",
							IBScanDevice.ImageType.FLAT_SINGLE_FINGER,
							1,
							"SFF_Right_Middle", FingerPosition.RIGHT_MIDDLE_FINGER);

					_AddCaptureSeqVector("Please put right ring on the sensor!",
							"Keep fingers on the sensor!",
							IBScanDevice.ImageType.FLAT_SINGLE_FINGER,
							1,
							"SFF_Right_Ring", FingerPosition.RIGHT_RING_FINGER);

					_AddCaptureSeqVector("Please put right little on the sensor!",
							"Keep fingers on the sensor!",
							IBScanDevice.ImageType.FLAT_SINGLE_FINGER,
							1,
							"SFF_Right_Little", FingerPosition.RIGHT_LITTLE_FINGER);

					_AddCaptureSeqVector("Please put left thumb on the sensor!",
							"Keep fingers on the sensor!",
							IBScanDevice.ImageType.FLAT_SINGLE_FINGER,
							1,
							"SFF_Left_Thumb", FingerPosition.LEFT_THUMB);

					_AddCaptureSeqVector("Please put left index on the sensor!",
							"Keep fingers on the sensor!",
							IBScanDevice.ImageType.FLAT_SINGLE_FINGER,
							1,
							"SFF_Left_Index", FingerPosition.LEFT_INDEX_FINGER);

					_AddCaptureSeqVector("Please put left middle on the sensor!",
							"Keep fingers on the sensor!",
							IBScanDevice.ImageType.FLAT_SINGLE_FINGER,
							1,
							"SFF_Left_Middle", FingerPosition.LEFT_MIDDLE_FINGER);

					_AddCaptureSeqVector("Please put left ring on the sensor!",
							"Keep fingers on the sensor!",
							IBScanDevice.ImageType.FLAT_SINGLE_FINGER,
							1,
							"SFF_Left_Ring", FingerPosition.LEFT_RING_FINGER);

					_AddCaptureSeqVector("Please put left little on the sensor!",
							"Keep fingers on the sensor!",
							IBScanDevice.ImageType.FLAT_SINGLE_FINGER,
							1,
							"SFF_Left_Little", FingerPosition.LEFT_LITTLE_FINGER);
				}

				if( strCaptureSeq == CAPTURE_SEQ_10_SINGLE_ROLLED_FINGERS )
				{
					_AddCaptureSeqVector("Please put right thumb on the sensor!",
							"Roll finger!",
							IBScanDevice.ImageType.ROLL_SINGLE_FINGER,
							1,
							"SFF_Right_Thumb", FingerPosition.RIGHT_THUMB);

					_AddCaptureSeqVector("Please put right index on the sensor!",
							"Roll finger!",
							IBScanDevice.ImageType.ROLL_SINGLE_FINGER,
							1,
							"SFF_Right_Index", FingerPosition.RIGHT_INDEX_FINGER);

					_AddCaptureSeqVector("Please put right middle on the sensor!",
							"Roll finger!",
							IBScanDevice.ImageType.ROLL_SINGLE_FINGER,
							1,
							"SFF_Right_Middle", FingerPosition.RIGHT_MIDDLE_FINGER);

					_AddCaptureSeqVector("Please put right ring on the sensor!",
							"Roll finger!",
							IBScanDevice.ImageType.ROLL_SINGLE_FINGER,
							1,
							"SFF_Right_Ring", FingerPosition.RIGHT_RING_FINGER);

					_AddCaptureSeqVector("Please put right little on the sensor!",
							"Roll finger!",
							IBScanDevice.ImageType.ROLL_SINGLE_FINGER,
							1,
							"SFF_Right_Little", FingerPosition.RIGHT_LITTLE_FINGER);

					_AddCaptureSeqVector("Please put left thumb on the sensor!",
							"Roll finger!",
							IBScanDevice.ImageType.ROLL_SINGLE_FINGER,
							1,
							"SFF_Left_Thumb", FingerPosition.LEFT_THUMB);

					_AddCaptureSeqVector("Please put left index on the sensor!",
							"Roll finger!",
							IBScanDevice.ImageType.ROLL_SINGLE_FINGER,
							1,
							"SFF_Left_Index", FingerPosition.LEFT_INDEX_FINGER);

					_AddCaptureSeqVector("Please put left middle on the sensor!",
							"Roll finger!",
							IBScanDevice.ImageType.ROLL_SINGLE_FINGER,
							1,
							"SFF_Left_Middle", FingerPosition.LEFT_MIDDLE_FINGER);

					_AddCaptureSeqVector("Please put left ring on the sensor!",
							"Roll finger!",
							IBScanDevice.ImageType.ROLL_SINGLE_FINGER,
							1,
							"SFF_Left_Ring", FingerPosition.LEFT_RING_FINGER);

					_AddCaptureSeqVector("Please put left little on the sensor!",
							"Roll finger!",
							IBScanDevice.ImageType.ROLL_SINGLE_FINGER,
							1,
							"SFF_Left_Little", FingerPosition.LEFT_LITTLE_FINGER);
				}

				if( strCaptureSeq == CAPTURE_SEQ_4_FLAT_FINGERS )
				{
					_AddCaptureSeqVector("Please put 4 fingers on the sensor!",
							"Keep fingers on the sensor!",
							IBScanDevice.ImageType.FLAT_FOUR_FINGERS,
							4,
							"4FF_Unknown", FingerPosition.UNKNOWN);
				}

				if( strCaptureSeq == CAPTURE_SEQ_10_FLAT_WITH_4_FINGER_SCANNER )
				{
					_AddCaptureSeqVector("Please put right 4-fingers on the sensor!",
							"Keep fingers on the sensor!",
							IBScanDevice.ImageType.FLAT_FOUR_FINGERS,
							4,
							"4FF_Right_4_Fingers", FingerPosition.PLAIN_RIGHT_FOUR_FINGERS);

					_AddCaptureSeqVector("Please put left 4-fingers on the sensor!",
							"Keep fingers on the sensor!",
							IBScanDevice.ImageType.FLAT_FOUR_FINGERS,
							4,
							"4FF_Left_4_Fingers", FingerPosition.PLAIN_LEFT_FOUR_FINGERS);

					_AddCaptureSeqVector("Please put 2-thumbs on the sensor!",
							"Keep fingers on the sensor!",
							IBScanDevice.ImageType.FLAT_TWO_FINGERS,
							2,
							"TFF_2_Thumbs", FingerPosition.PLAIN_THUMBS);
				}
				
				long time = System.currentTimeMillis();
				SimpleDateFormat dayTime = new SimpleDateFormat("yyyy-MM-dd hhmmss");
				m_ImgSubFolder = dayTime.format(new Date(time));
				
				OnMsg_CaptureSeqNext();
				}
		});
			}

	private void OnMsg_CaptureSeqNext()
	{
		javax.swing.SwingUtilities.invokeLater(new Runnable()
		{

			@Override
			public void run()
			{
				if (getIBScanDevice() == null)
					return;
				
				m_bBlank = false;
				for (int i=0; i<4; i++)
					m_FingerQuality[i] = FingerQualityState.FINGER_NOT_PRESENT;
				
				m_nCurrentCaptureStep++;
				if (m_nCurrentCaptureStep >= m_vecCaptureSeq.size())
				{
					// All of capture sequence completely
			        CaptureInfo tmpInfo = new CaptureInfo();
		        	_SetLEDs(tmpInfo, __LED_COLOR_NONE__, false);

					m_nCurrentCaptureStep = -1;

					OnMsg_UpdateDisplayResources();
					return;
				}
				
				try
				{
					if (m_chkDetectSmear.isSelected())
					{
						try
						{
							getIBScanDevice().setProperty(IBScanDevice.PropertyId.ROLL_MODE, "1");
							String strValue = String.valueOf(m_cboSmearLevel.getSelectedIndex());
							getIBScanDevice().setProperty(IBScanDevice.PropertyId.ROLL_LEVEL, strValue);
						}
						catch (IBScanException e)
						{
						}
					}
					else
					{
						try
						{
							getIBScanDevice().setProperty(IBScanDevice.PropertyId.ROLL_MODE, "0");
						}
						catch (IBScanException e)
						{
						}
					}
					
					// Spoof Control
					OnMsg_SetTxtSpoofResult("");
					if (m_chkEnableSpoof.isSelected())
					{
						try 
						{
							getIBScanDevice().setProperty(IBScanDevice.PropertyId.ENABLE_SPOOF, "TRUE");
							// Disable segment rotation for the better PAD perfomance
							getIBScanDevice().setProperty(IBScanDevice.PropertyId.DISABLE_SEGMENT_ROTATION, "TRUE");

							String strValue = String.valueOf(m_cboSpoofLevel.getSelectedIndex()+1);
							getIBScanDevice().setProperty(IBScanDevice.PropertyId.SPOOF_LEVEL, strValue);
						}
						catch (IBScanException ibse)
						{
							//ibse.printStackTrace();
						}
					}
					else
					{
						try
						{
							getIBScanDevice().setProperty(IBScanDevice.PropertyId.ENABLE_SPOOF, "FALSE");
						}
						catch (IBScanException ibse)
						{
							//ibse.printStackTrace();
						}
					}
					
					
					// Make capture delay for display result image on multi capture mode (500 ms)
					if (m_nCurrentCaptureStep > 0)
					{
						_Sleep(500);
						m_strImageMessage = "";
					}
	
					CaptureInfo info = m_vecCaptureSeq.elementAt(m_nCurrentCaptureStep);
	
					IBScanDevice.ImageResolution imgRes = IBScanDevice.ImageResolution.RESOLUTION_500;
					boolean bAvailable = getIBScanDevice().isCaptureAvailable(info.ImageType, imgRes);
					if (!bAvailable)
					{
						_SetStatusBarMessage("The capture mode (" + info.ImageType + ") is not available");
						m_nCurrentCaptureStep = -1;
						OnMsg_UpdateDisplayResources();
						return;
					}
					
					// Start capture
					int captureOptions = 0;
					if (m_chkAutoContrast.isSelected())
						captureOptions |= IBScanDevice.OPTION_AUTO_CONTRAST;
					if (m_chkAutoCapture.isSelected())
						captureOptions |= IBScanDevice.OPTION_AUTO_CAPTURE;
					if (m_chkIgnoreFingerCount.isSelected())
						captureOptions |= IBScanDevice.OPTION_IGNORE_FINGER_COUNT;

					getIBScanDevice().beginCaptureImage(info.ImageType, imgRes, captureOptions);
					
					String strMessage = info.PreCaptureMessage;
					_SetStatusBarMessage(strMessage);
					if (!m_chkAutoCapture.isSelected())
						strMessage += "\r\nPress button 'Take Result Image' when image is good!";

					_SetImageMessage(strMessage);
					m_strImageMessage = strMessage;
					
					m_ImageType = info.ImageType;

				    _SetLEDs(info, __LED_COLOR_RED__, true);

					OnMsg_UpdateDisplayResources();
				}
				catch (IBScanException ibse)
				{
					ibse.printStackTrace();
					_SetStatusBarMessage("Failed to execute beginCaptureImage()");
					m_nCurrentCaptureStep = -1;
				}
			}
		});
	}

	private void OnMsg_cboUsbDevice_Changed()
	{
		javax.swing.SwingUtilities.invokeLater(new Runnable()
		{

			@Override
			public void run()
			{
				if (m_nSelectedDevIndex == m_cboUsbDevices.getSelectedIndex())
					return;
			
				m_nSelectedDevIndex = m_cboUsbDevices.getSelectedIndex();
				if (getIBScanDevice() != null)
				{
					try
					{
						_ReleaseDevice();
					}
					catch (IBScanException ibse)
					{
						ibse.printStackTrace();
					}
				}
				
				_UpdateCaptureSequences();
			}
		});
			}

	private void OnMsg_UpdateDeviceList()
	{
		javax.swing.SwingUtilities.invokeLater(new Runnable()
		{

	@Override
			public void run()
			{
				try
				{
					boolean idle = !m_bInitializing && (m_nCurrentCaptureStep == -1);

					if (idle)
					{
						m_btnCaptureStop.setEnabled(false);
						m_btnCaptureStart.setEnabled(false);
	}

					//store currently selected device
					String strSelectedText = "";
					int selectedDev = m_cboUsbDevices.getSelectedIndex();
					if (selectedDev > -1)
						strSelectedText = m_cboUsbDevices.getSelectedItem().toString();

					m_cboUsbDevices.removeActionListener(m_cboUsbDevice_Changed);
					m_cboUsbDevices.removeAllItems();
					m_cboUsbDevices.addActionListener(m_cboUsbDevice_Changed);
					m_cboUsbDevices.addItem("--PLEASE SELECT--");

					// populate combo box
					int devices = getIBScan().getDeviceCount();
					m_cboUsbDevices.setMaximumRowCount(devices + 1);

					selectedDev = 0;
					for (int i = 0; i < devices; i++)
					{
						IBScan.DeviceDesc devDesc = getIBScan().getDeviceDescription(i);
						String strDevice;
						strDevice = devDesc.productName + "_v"+ devDesc.fwVersion + "(" + devDesc.serialNumber + ")";

						m_cboUsbDevices.addItem(strDevice);
						if (strDevice == strSelectedText)
							selectedDev = i + 1;
		}

					if ( (selectedDev == 0 && (m_cboUsbDevices.getItemCount() == 2)))
						selectedDev = 1;

					m_cboUsbDevices.setSelectedIndex(selectedDev);

					if (idle)
					{
						OnMsg_cboUsbDevice_Changed();
						_UpdateCaptureSequences();
					}
				}
				catch (IBScanException e)
				{
					e.printStackTrace();
				}
			}
		});
	}

	private void OnMsg_UpdateDisplayResources()
	{
		javax.swing.SwingUtilities.invokeLater(new Runnable()
		{

	@Override
			public void run()
			{
				boolean selectedDev = m_cboUsbDevices.getSelectedIndex() > 0;
				boolean captureSeq = m_cboCaptureSeq.getSelectedIndex() > 0;
				boolean idle = !m_bInitializing && (m_nCurrentCaptureStep == -1);
				boolean active = !m_bInitializing && (m_nCurrentCaptureStep != -1);
				boolean uninitializedDev = selectedDev && (getIBScanDevice() == null);

				m_cboUsbDevices.setEnabled(idle);
				m_cboCaptureSeq.setEnabled(selectedDev && idle);
					
				m_btnCaptureStart.setEnabled(captureSeq);
				m_btnCaptureStop.setEnabled(active);

				m_chkAutoContrast.setEnabled(selectedDev && idle );
				m_chkAutoCapture.setEnabled(selectedDev && idle );
				m_chkIgnoreFingerCount.setEnabled(selectedDev && idle );
				m_chkSaveImages.setEnabled(selectedDev && idle );
				m_btnImageFolder.setEnabled(selectedDev && idle );

				m_chkUseClearPlaten.setEnabled(uninitializedDev);

				if (active)
				{
					m_btnCaptureStart.setText("Take Result Image");
				}
				else
				{
					m_btnCaptureStart.setText("Start");
				}
			}
		});
	}

	private void OnMsg_AskRecapture(final IBScanException imageStatus)
	{
		javax.swing.SwingUtilities.invokeLater(new Runnable()
		{

	@Override
			public void run()
			{
				String askMsg;

				askMsg = "[Warning = " + imageStatus.getType().toString() + "] Do you want a recapture?";

				if (JOptionPane.showConfirmDialog(null, askMsg, "IBSanUltimate_SampleForJAVA", JOptionPane.YES_NO_OPTION) == JOptionPane.YES_OPTION)
			    {
			        // To recapture current finger position
			        m_nCurrentCaptureStep--;
			    }

			    OnMsg_CaptureSeqNext();
			}
		});
			}


	private void OnMsg_DeviceCommunicationBreak()
	{
		javax.swing.SwingUtilities.invokeLater(new Runnable()
		{
			
			@Override
			public void run()
			{
				if (getIBScanDevice() == null)
					return;
				
				_SetStatusBarMessage("Device communication was broken");

				try
				{
					_ReleaseDevice();

					OnMsg_Beep(__BEEP_DEVICE_COMMUNICATION_BREAK__);
					OnMsg_UpdateDeviceList();
			}
				catch (IBScanException ibse)
				{
					if (ibse.getType().equals(IBScanException.Type.RESOURCE_LOCKED))
					{
						OnMsg_DeviceCommunicationBreak();
					}
				}
			}
		});
		}

	private void OnMsg_DrawImage(final IBScanDevice device, final ImageData image)
	{
		javax.swing.SwingUtilities.invokeLater(new Runnable()
		{
			@Override
			public void run()
			{
				int destWidth = pnlImagePreview.getWidth()-20;
				int destHeight = pnlImagePreview.getHeight()-20;
//				int outImageSize = destWidth * destHeight;

//				byte[] outImage = new byte[outImageSize];
//				Arrays.fill(outImage, (byte) 255);

				try
				{
					if (image.isFinal)
					{
						ibScanDevice.generateDisplayImage(image.buffer, image.width, image.height,
								m_drawBuffer, destWidth, destHeight, (byte) 255, 0 /*IBSU_IMG_FORMAT_GRAY*/, 2 /*HIGH QUALITY*/, true);
					}
					else
					{
						ibScanDevice.generateDisplayImage(image.buffer, image.width, image.height,
								m_drawBuffer, destWidth, destHeight, (byte) 255, 0 /*IBSU_IMG_FORMAT_GRAY*/, 0 /*LOW QUALITY*/, true);
						}
				}
				catch (IBScanException e)
				{
			e.printStackTrace();
		}

		// /////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/*				BufferedImage m_drawImageJ = new BufferedImage(destWidth, destHeight, BufferedImage.TYPE_4BYTE_ABGR);
				byte[] drawImageData = ((DataBufferByte)m_drawImageJ.getRaster().getDataBuffer()).getData();
				System.arraycopy(m_drawBuffer, 0, drawImageData, 0, m_drawBuffer.length);
*/
				System.arraycopy(m_drawBuffer, 0, m_grayscaleImageData, 0, m_drawBuffer.length);
				m_drawImageJ.createGraphics().drawImage(m_grayscaleImageJ, 0, 0, null);

				Graphics2D g = (Graphics2D) m_drawImageJ.getGraphics();

				_DrawOverlay_ImageText(g);
				_DrawOverlay_WarningOfClearPlaten(g, 0, 0, destWidth, destHeight);
				_DrawOverlay_ResultSegmentImage(g, image, destWidth, destHeight);
				_DrawOverlay_RollGuideLine(g, image, destWidth, destHeight);

				ImageIcon imageIcon = new ImageIcon(m_drawImageJ);
				m_lblImagePreview.setIcon(imageIcon);
				}
		});
				}
	
	private void OnMsg_DrawFingerQuality()
	{
		javax.swing.SwingUtilities.invokeLater(new Runnable()
		{

			@Override
			public void run()
			{
				try
				{
					img = ImageIO.read(m_urlScannerImg);
				}
				catch (IOException e)
				{
					e.printStackTrace();
				}

				// Update value in fingerQuality field and flash button.
				Graphics2D g = (Graphics2D)IBScanUltimate_Sample.this.img.getGraphics();
				for (int i = 0; i < 4; i++)
				{
					Color color;
					if (m_FingerQuality[i] == IBScanDevice.FingerQualityState.GOOD)
						color = new Color(0, 128, 0);
					else if (m_FingerQuality[i] == IBScanDevice.FingerQualityState.FAIR)
						color = new Color(255, 128, 0);
					else if (m_FingerQuality[i] == IBScanDevice.FingerQualityState.POOR ||
							 m_FingerQuality[i] == IBScanDevice.FingerQualityState.INVALID_AREA_TOP ||
							 m_FingerQuality[i] == IBScanDevice.FingerQualityState.INVALID_AREA_BOTTOM ||
							 m_FingerQuality[i] == IBScanDevice.FingerQualityState.INVALID_AREA_LEFT ||
							 m_FingerQuality[i] == IBScanDevice.FingerQualityState.INVALID_AREA_RIGHT
							)
						color = new Color(255, 0, 0);
					else
					{
						color = new Color(114, 114, 114);
					}

					g.setColor(color);
					g.fill(new Rectangle(20 + 20 * i, 43, 15, 70));
			}

				m_lblScanner.setIcon(new ImageIcon(IBScanUltimate_Sample.this.img));
			}
		});
		}

		

	// //////////////////////////////////////////////////////////////////////////////////////////////
	// EVENT HANDLERS - Image Acquisition
	// //////////////////////////////////////////////////////////////////////////////////////////////

	// Device ComboBox Listener
	private ActionListener m_cboUsbDevice_Changed = new ActionListener()
	{
		@Override
		public void actionPerformed(ActionEvent ae)
		{
			OnMsg_cboUsbDevice_Changed();
		}
	};

	// //Image ComboBox Listener
	private ActionListener m_cboCaptureSeq_Changed = new ActionListener() {

		@Override
		public void actionPerformed(ActionEvent e) {
			int SelImageCombo;
			SelImageCombo = IBScanUltimate_Sample.this.m_cboCaptureSeq.getSelectedIndex();
			if (SelImageCombo == 0) {
				IBScanUltimate_Sample.this.m_btnCaptureStart.setEnabled(false);
			} else {
				IBScanUltimate_Sample.this.m_btnCaptureStart.setEnabled(true);
	}
		}
	};

	/* *********************************************************************************************
	 * EVENT HANDLERS
	 ******************************************************************************************** */
	
	/* 
	 * Handle click on "Start capture" button.
	 */
	private ActionListener m_btnCaptureStart_Click = new ActionListener()
	{
	@Override
		public void actionPerformed(ActionEvent ae)
		{
			if (m_bInitializing)
				return;

			int devIndex = m_cboUsbDevices.getSelectedIndex() - 1;
			if (devIndex < 0)
				return;

			if (m_nCurrentCaptureStep != -1)
			{
				try
				{
					boolean IsActive = getIBScanDevice().isCaptureActive();
					if (IsActive)
					{
						// Capture image manually for active device
						getIBScanDevice().captureImageManually();
						return;
					}
				}
				catch (IBScanException ibse)
				{
					_SetStatusBarMessage("IBScanDevice.takeResultImageManually() returned exception "
							+ ibse.getType().toString() + ".");
				}
			}

			if (getIBScanDevice() == null)
			{
				m_bInitializing = true;
				_InitializeDeviceThreadCallback thread = new _InitializeDeviceThreadCallback(m_nSelectedDevIndex - 1);
				thread.start();
			}
			else
			{
				OnMsg_CaptureSeqStart();
			}

			OnMsg_UpdateDisplayResources();
			}
	};

	/*
	 * Handle click on "Stop capture" button. 
	 */	
	private ActionListener m_btnCaptureStop_Click = new ActionListener()
	{
			@Override
		public void actionPerformed(ActionEvent ae)
				{					
			if (getIBScanDevice() == null)
				return;
			
			// Cancel capturing image for active device.
			try
					{
				// Cancel capturing image for active device.
				getIBScanDevice().cancelCaptureImage();
				CaptureInfo tmpInfo = new CaptureInfo();
				_SetLEDs(tmpInfo, __LED_COLOR_NONE__, false);
				m_nCurrentCaptureStep = -1;
				m_bNeedClearPlaten = false;
				m_bBlank = false;

				_SetStatusBarMessage("Capture Sequence aborted");
				m_strImageMessage = "";
				_SetImageMessage("");
				OnMsg_UpdateDisplayResources();
			}
			catch (IBScanException ibse)
					{
				_SetStatusBarMessage("cancel returned exception " + ibse.getType().toString() + ".");
						}
					}
	};

	/*
	 * Handle click on "Save folder" button. 
	 */	
	private ActionListener m_btnImageFolder_Click = new ActionListener()
				{					
		@Override
		public void actionPerformed(ActionEvent ae)
					{
			if (getIBScan() == null)
				return;
			
			// Select folder to save image.
			JFileChooser fc = new JFileChooser();
			fc.setCurrentDirectory(new java.io.File("."));
			fc.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY);
			int returnVal = fc.showSaveDialog(IBScanUltimate_Sample.this);
			
			if (returnVal == JFileChooser.APPROVE_OPTION)
					{
			    m_ImgSaveFolder = fc.getCurrentDirectory().toString() + File.separator + fc.getSelectedFile().getName();
						}
			
			try
			{
				getIBScan().isWritableDirectory(m_ImgSaveFolder, true);
			}
			catch (IBScanException ibse)
			{
				JOptionPane.showMessageDialog(null, "You don't have writing permission on this folder\r\nPlease select another folder (e.g. desktop folder)");
				_SetStatusBarMessage("Returned exception " + ibse.getType().toString() + ".");
					}
				}
	};

	/*
	 * Handle scroll on m_sliderContrast.
	 */
	class m_sliderContrast_Change implements ChangeListener {
		public void stateChanged(ChangeEvent e) {

			logPrintln("Contrast slider changed.");
			_SetTxtContrast(String.valueOf(m_sliderContrast.getValue()));

			if (getIBScanDevice() == null) {
				// Alert user no device has been opened.
				_SetStatusBarMessage("No device has been opened.");
			} else {
				try {
					// Cancel capturing image for active device.
					getIBScanDevice().setContrast(m_sliderContrast.getValue());
				} catch (IBScanException ibse) {
					_SetStatusBarMessage("setContrast() returned exception "
							+ ibse.getType().toString() + ".");
			}
		}

		}
	}

	// //////////////////////////////////////////////////////////////////////////////////////////////
	// PROTECTED INTERFACE
	// //////////////////////////////////////////////////////////////////////////////////////////////

	protected static final int DEVICE_INDEX_INVALID = -12345678;
	protected static final long LEDS_INVALID = -12345678;
	protected static final int CONTRAST_INVALID = -12345678;

	// The IB scan through which the bus is accessed.
	protected IBScan ibScan = null;
	protected IBScanDevice ibScanDevice = null;
	protected BufferedImage lastScanImage = null;
	protected ImageData lastScanImageData = null;
	protected RollingData startRollingData = null;
	protected SegmentPosition arraySegmentPosion = null;

	// Get IBScan.
	protected IBScan getIBScan() {
		return (this.ibScan);
			}

	// Get opened or null IBScanDevice.
	protected IBScanDevice getIBScanDevice() {
		return (this.ibScanDevice);
	}

	// Set IBScanDevice.
	protected void setIBScanDevice(IBScanDevice ibScanDevice) {
		this.ibScanDevice = ibScanDevice;
		if (ibScanDevice != null) {
			ibScanDevice.setScanDeviceListener(this);
		}
	}

//	// Alert user to error.
	protected void alertUser(String s) {
		JOptionPane.showMessageDialog(this, s, "ERROR",
				JOptionPane.ERROR_MESSAGE);
				}

	// Log statement to System.out.
	protected static void logPrintln(String ln) {
		 //System.out.println(ln);
					}

	
	// Get extension of file name.
	protected String getExtension(String fileName) {
		String extension = "";
		int index = fileName.lastIndexOf('.');
		if ((index >= 0) && (index != fileName.length() - 1)) {
			extension = fileName.substring(index + 1).toLowerCase();
				}

			return (extension);
		}
		// Custom file filter to choose only image files.
	FileFilter imageFilter = new FileFilter() {
		@Override
		public boolean accept(File f) {
			String extension = getExtension(f.getName());
			String[] formats = ImageIO.getWriterFormatNames();

				// Filter by image formats
			for (String format : formats) {
			if (extension.equals(format.toLowerCase())) {
				return (true);
			}
		}
			return (false);
	}

	@Override
		public String getDescription() {
		String s;
		String[] suffixes ={"bmp","wsq","png","jp2"};//ImageIO.getWriterFileSuffixes();

		// Return description with list of acceptable
		// suffixes
		s = "Save all images (";
		for (int i = 0; i < suffixes.length; i++) {
			s += suffixes[i];
			if (i != suffixes.length - 1) {
				s += ", ";
			}
	}
				s += ")";
				return (s);
			}
		};
	

	// //////////////////////////////////////////////////////////////////////////////////////////////
	// PUBLIC INTERFACE: IBScanListener METHODS
	// //////////////////////////////////////////////////////////////////////////////////////////////
				
	@Override
	public void scanDeviceCountChanged(final int deviceCount)
			{
		OnMsg_UpdateDeviceList();
				}	

	@Override
	public void scanDeviceInitProgress(final int deviceIndex, final int progressValue) 
			{
		OnMsg_SetStatusBarMessage("Initializing device..."+ progressValue + "%");
				}	

	@Override
	public void scanDeviceOpenComplete(final int deviceIndex, final IBScanDevice device, 
			final IBScanException exception) 
	{
			}
		
	// //////////////////////////////////////////////////////////////////////////////////////////////
	// PUBLIC INTERFACE: IBScanDeviceListener METHODS
	// //////////////////////////////////////////////////////////////////////////////////////////////

	@Override
	public void deviceCommunicationBroken(final IBScanDevice device) 
	{
		OnMsg_DeviceCommunicationBreak();
	}

	@Override
	public void deviceImagePreviewAvailable(final IBScanDevice device, final ImageData image) throws IBScanException
	{
		OnMsg_DrawImage(device, image);
			}

			@Override
	public void deviceFingerCountChanged(final IBScanDevice device, final FingerCountState fingerState) 
	{
		if (m_nCurrentCaptureStep >= 0)
		{
			CaptureInfo info = m_vecCaptureSeq.elementAt(m_nCurrentCaptureStep);
			if (fingerState == IBScanDevice.FingerCountState.NON_FINGER)
			{
				_SetLEDs(info, __LED_COLOR_RED__, true);
			}
			else
			{
				_SetLEDs(info, __LED_COLOR_YELLOW__, true);
			}
		}

	}

	@Override
	public void deviceFingerQualityChanged(final IBScanDevice device, final FingerQualityState[] fingerQualities)
	{
		for (int i=0; i<fingerQualities.length; i++)
		{
			m_FingerQuality[i] = fingerQualities[i];
					}

		OnMsg_DrawFingerQuality();
				}

	@Override
	public void deviceAcquisitionBegun(final IBScanDevice device, final ImageType imageType) 
	{
		if (imageType.equals(IBScanDevice.ImageType.ROLL_SINGLE_FINGER))
		{
			OnMsg_Beep(__BEEP_OK__);
			m_strImageMessage = "When done remove finger from sensor";
			_SetImageMessage(m_strImageMessage);
			_SetStatusBarMessage(m_strImageMessage);
			}
		}

	@Override
	public void deviceAcquisitionCompleted(final IBScanDevice device, final ImageType imageType) 
	{
		if (imageType.equals(IBScanDevice.ImageType.ROLL_SINGLE_FINGER))
		{
			OnMsg_Beep(__BEEP_OK__);
				}
		else
		{
			OnMsg_Beep(__BEEP_SUCCESS__);
			_SetImageMessage("Remove fingers from sensor");
			_SetStatusBarMessage("Acquisition completed, postprocessing..");
			}
		}

	@Override
	public void deviceImageResultAvailable(final IBScanDevice device, final ImageData image, 
			final ImageType imageType, final ImageData[] splitImageArray) 
	{
		/* TODO: ALTERNATIVELY, USE RESULTS IN THIS FUNCTION */
			}

			@Override
    public void deviceImageResultExtendedAvailable(IBScanDevice device, IBScanException imageStatus,
    		final ImageData image, final ImageType imageType, final int detectedFingerCount, 
    		final ImageData[] segmentImageArray, final SegmentPosition[] segmentPositionArray)
    {

		// imageStatus value is greater than "STATUS_OK", Image acquisition successful.
		if (imageStatus == null /*STATUS_OK*/ || 
			imageStatus.getType().compareTo(IBScanException.Type.INVALID_PARAM_VALUE) > 0)
		{
				if (imageType.equals(IBScanDevice.ImageType.ROLL_SINGLE_FINGER))
				{
					OnMsg_Beep(__BEEP_SUCCESS__);
				}	
		}
				
		if (m_bNeedClearPlaten)
		{
			m_bNeedClearPlaten = false;
			OnMsg_DrawFingerQuality();
		}
							
		// imageStatus value is greater than "STATUS_OK", Image acquisition successful.
		if (imageStatus == null /*STATUS_OK*/ || 
			imageStatus.getType().compareTo(IBScanException.Type.INVALID_PARAM_VALUE) > 0)
		{
		    // Image acquisition successful
			CaptureInfo info = m_vecCaptureSeq.elementAt(m_nCurrentCaptureStep);
			_SetLEDs(info, __LED_COLOR_GREEN__, false);

			// SAVE IMAGE
			if (m_chkSaveImages.isSelected())
			{
				_SetStatusBarMessage("Saving image...");
			    _SaveBitmapImage(image, info.fingerName);
				_SaveWsqImage(image, info.fingerName);
			    _SavePngImage(image, info.fingerName);
			    _SaveJP2Image(image, info.fingerName);
								
				//save segmented fingers
				for (int i = 0; i < detectedFingerCount; i++)
				{
					 String segmentName = info.fingerName + "_Segment_" + String.valueOf(i);
				    _SaveBitmapImage(segmentImageArray[i], segmentName);
					_SaveWsqImage(segmentImageArray[i], segmentName);
				    _SavePngImage(segmentImageArray[i], segmentName);
				    _SaveJP2Image(segmentImageArray[i], segmentName);
				}
				
			    //// Save ISO image & template
				try {
					m_imageDataExtResult = getIBScanDevice().getResultImageExt(info.fingerPosition);
				} catch (IBScanException e) {
					e.printStackTrace();
				}
			    _SaveISOImage(info.fingerName);

			}

			if (m_chkDrawSegmentImage.isSelected())
			{
				m_nSegmentImageArrayCount = detectedFingerCount;
				m_SegmentPositionArray = segmentPositionArray;
				}

				// NFIQ
			if (m_chkNFIQScore.isSelected())
			{
				byte[] nfiq_score = { 0, 0, 0, 0 };
				try
				{
					for (int i=0, segment_pos=0; i<4; i++)
					{
						if (m_FingerQuality[i].ordinal() != IBScanDevice.FingerQualityState.FINGER_NOT_PRESENT.ordinal())
						{
							nfiq_score[i] = (byte)getIBScanDevice().calculateNfiqScore(segmentImageArray[segment_pos++]);
						}
					}
				}
				catch (IBScanException ibse)
				{
					ibse.printStackTrace();
				}
				
				OnMsg_SetTxtNFIQScore("" + nfiq_score[0] + "-" + nfiq_score[1] + "-" + nfiq_score[2] + "-" + nfiq_score[3]);
			}
			
			// Spoof
			if (m_chkEnableSpoof.isSelected())
			{
				boolean isSpoof;
				String[] isSpoofStr = new String[4];
				
				int temp = segmentImageArray.length;
				
				try
				{
					for (int i=0; i<segmentImageArray.length; i++)
					{
						isSpoof = getIBScanDevice().IsSpoofFingerDetected(segmentImageArray[i]);
						
						if (isSpoof == true)
							isSpoofStr[i] = "FAKE";
						else
							isSpoofStr[i] = "LIVE";
					}
					
				} catch (IBScanException ibse)
				{
					OnMsg_SetTxtSpoofResult("Error");
					
					try {
						m_strImageMessage = getIBScan().getErrorString(ibse.getType().toCode()) + "(Error code = "+ ibse.getType().toCode()+")";
					} catch (IBScanException e) {
						e.printStackTrace();
					}
					//_SetStatusBarMessage("[Error Code = "+ ibse.getType().toCode() + "]");
					
					_Sleep(1000);
					
					_SetImageMessage(m_strImageMessage);
		      _SetStatusBarMessage(m_strImageMessage);
					
					// Stop all of acquisition
					m_nCurrentCaptureStep = (int)m_vecCaptureSeq.size();
			
					OnMsg_DrawImage(device, image);
					OnMsg_CaptureSeqNext();
					return;
				}

				if (segmentImageArray.length == 1)
				{
					OnMsg_SetTxtSpoofResult(isSpoofStr[0]);
				}
				if (segmentImageArray.length == 2)
				{
					OnMsg_SetTxtSpoofResult(isSpoofStr[0]+"-"+isSpoofStr[1]);
				}
				if (segmentImageArray.length == 4)
				{
					OnMsg_SetTxtSpoofResult(isSpoofStr[0]+"-"+isSpoofStr[1]+"-"+isSpoofStr[2]+"-"+isSpoofStr[3]);
				}
				
			}
			
			if (imageStatus == null /*STATUS_OK*/)
			{
		        m_strImageMessage = "Acquisition completed successfully";
		        _SetImageMessage(m_strImageMessage);
		        _SetStatusBarMessage(m_strImageMessage);
			}
	        else
					{
	            // > IBSU_STATUS_OK
		        m_strImageMessage = "Acquisition Warning (Warning code = " + imageStatus.getType().toString() + ")";
		        _SetImageMessage(m_strImageMessage);
		        _SetStatusBarMessage(m_strImageMessage);
					
		        OnMsg_DrawImage(device, image);
		        OnMsg_AskRecapture(imageStatus);
				return;
			}
		}
		else
		{
	        // < IBSU_STATUS_OK
		    m_strImageMessage = "Acquisition failed (Error code = " + imageStatus.getType().toString() + ")";
		    _SetImageMessage(m_strImageMessage);
		    _SetStatusBarMessage(m_strImageMessage);
			
	        // Stop all of acquisition
	        m_nCurrentCaptureStep = (int)m_vecCaptureSeq.size();
		}

		OnMsg_DrawImage(device, image);

		OnMsg_CaptureSeqNext();
	}

	@Override
	public void devicePlatenStateChanged(final IBScanDevice device, final PlatenState platenState) 
	{
		if (platenState.equals(IBScanDevice.PlatenState.HAS_FINGERS))
			m_bNeedClearPlaten = true;
		else
			m_bNeedClearPlaten = false;

		if (platenState.equals(IBScanDevice.PlatenState.HAS_FINGERS))
		{
			m_strImageMessage = "Please remove your fingers on the platen first!";
			_SetImageMessage(m_strImageMessage);
			_SetStatusBarMessage(m_strImageMessage);
			}
		else
		{
	        if (m_nCurrentCaptureStep >= 0)
	        {
			    CaptureInfo info = m_vecCaptureSeq.elementAt(m_nCurrentCaptureStep);

			    // Display message for image acuisition again
			    String strMessage = info.PreCaptureMessage;

			    _SetStatusBarMessage(strMessage);
			    if (!m_chkAutoCapture.isSelected())
				    strMessage += "\r\nPress button 'Take Result Image' when image is good!";

			    _SetImageMessage(strMessage);
			    m_strImageMessage = strMessage;
			}
		}

		OnMsg_DrawFingerQuality();
	}

	@Override
	public void deviceWarningReceived(final IBScanDevice device, final IBScanException warning) 
	{
		_SetStatusBarMessage("Warning received " + warning.getType().toString());
	}

	@Override
	public void devicePressedKeyButtons(IBScanDevice device, int pressedKeyButtons)
    {
		_SetStatusBarMessage("PressedKeyButtons " + pressedKeyButtons);
		
	    boolean selectedDev = m_cboUsbDevices.getSelectedIndex() > 0;
	    boolean idle = m_bInitializing && (m_nCurrentCaptureStep == -1);
		boolean active = m_bInitializing && (m_nCurrentCaptureStep != -1);
		try
		{
			if (pressedKeyButtons == __LEFT_KEY_BUTTON__)
			{
		        if (selectedDev && idle)
		        {
					System.out.println("Capture Start");
					device.setBeeper(IBScanDevice.BeepPattern.BEEP_PATTERN_GENERIC, 2/*Sol*/, 4/*100ms = 4*25ms*/, 0, 0);
					this.m_btnCaptureStart.doClick();
		        }
			}
			else if (pressedKeyButtons == __RIGHT_KEY_BUTTON__)
			{
		        if ( (active) )
		        {
					System.out.println("Capture Stop");
					device.setBeeper(IBScanDevice.BeepPattern.BEEP_PATTERN_GENERIC, 2/*Sol*/, 4/*100ms = 4*25ms*/, 0, 0);
					this.m_btnCaptureStop.doClick();
		        }
			}
		}
		catch (IBScanException e)
		{
			e.printStackTrace();
		}
	}
}
