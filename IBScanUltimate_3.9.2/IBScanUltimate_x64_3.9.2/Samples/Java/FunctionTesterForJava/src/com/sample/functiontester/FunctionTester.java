/* *************************************************************************************************
 * FunctionTester.java
 *
 * DESCRIPTION:
 *     Java FunctionTester sample application for IBScanUltimate
 *     http://www.integratedbiometrics.com
 *
 * NOTES:
 *     Copyright (c) Integrated Biometrics, 2013
 *
 * HISTORY:
 *    2013/03/01  First verion
 *    2013/03/22  Add NFIQ score button
 *    2014/11/24  Added generateZoomOutImageEx() function to increase speed to draw the image.
 ************************************************************************************************ */

package com.sample.functiontester;

import java.awt.Color;
import java.awt.Font;
import java.awt.Image;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.net.URL;
import java.util.Arrays;

import javax.imageio.ImageIO;
import javax.swing.BoxLayout;
import javax.swing.DefaultComboBoxModel;
import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JCheckBox;
import javax.swing.JComboBox;
import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JMenuItem;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JPopupMenu;
import javax.swing.JTextField;
import javax.swing.JTextPane;
import javax.swing.SwingUtilities;
import javax.swing.border.EtchedBorder;
import javax.swing.border.TitledBorder;
import javax.swing.filechooser.FileFilter;

import com.integratedbiometrics.ibscanultimate.IBScan;
import com.integratedbiometrics.ibscanultimate.IBScan.HashType;
import com.integratedbiometrics.ibscanultimate.IBScanDevice;
import com.integratedbiometrics.ibscanultimate.IBScanDeviceListener;
import com.integratedbiometrics.ibscanultimate.IBScanException;
import com.integratedbiometrics.ibscanultimate.IBScanListener;
import com.integratedbiometrics.ibscanultimate.IBScanDevice.FingerCountState;
import com.integratedbiometrics.ibscanultimate.IBScanDevice.FingerQualityState;
import com.integratedbiometrics.ibscanultimate.IBScanDevice.ImageData;
import com.integratedbiometrics.ibscanultimate.IBScanDevice.ImageType;
import com.integratedbiometrics.ibscanultimate.IBScanDevice.PlatenState;
import com.integratedbiometrics.ibscanultimate.IBScanDevice.SegmentPosition;

/**
 * Principal class for function tester demo UI.
 */
@SuppressWarnings("serial")
public class FunctionTester extends JFrame implements IBScanListener, IBScanDeviceListener
{
    /**
     * @param args
     */
    public static void main(String[] args)
    {
        FunctionTester frame = new FunctionTester();
        frame.setVisible(true);
    }

    /**
     * Create UI for function tester, initialize IBScan, and register callbacks.
     */
    public FunctionTester()
    {
        Font mainFont = new Font("Lucida Grande", Font.PLAIN, 11);
        Font titleFont = new Font("Lucida Grande", Font.PLAIN, 11);

        setTitle("IB Scan Ultimate Function Tester -- (" + System.getProperty("sun.arch.data.model") + ")bit");
        setResizable(false);
        getContentPane().setLayout(new BoxLayout(getContentPane(), BoxLayout.X_AXIS));
        setBounds(0, 0, 933, 765);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        JPanel pnl = new JPanel();
        getContentPane().add(pnl);
        pnl.setLayout(null);

        //
        // Top Functions
        //

        JButton btnGetSDKVersion = new JButton("getSDKVersion");
        btnGetSDKVersion.addActionListener(this.btnGetSDKVersionListener);
        btnGetSDKVersion.setFont(mainFont);
        btnGetSDKVersion.setBounds(10, 97, 140, 27);
        pnl.add(btnGetSDKVersion);

        JButton btnGetDeviceCount = new JButton("getDeviceCount");
        btnGetDeviceCount.addActionListener(this.btnGetDeviceCountListener);
        btnGetDeviceCount.setFont(mainFont);
        btnGetDeviceCount.setBounds(165, 97, 140, 27);
        pnl.add(btnGetDeviceCount);

        //
        // Main Interface Function
        //

        JPanel pnlMainInterfaceFunction = new JPanel();
        pnlMainInterfaceFunction.setBounds(10, 138, 295, 239);
        pnlMainInterfaceFunction.setBorder(new TitledBorder(new EtchedBorder(EtchedBorder.LOWERED,
            null, null), "Main Interface Function", TitledBorder.LEADING, TitledBorder.TOP,
            titleFont, new Color(0, 0, 0)));
        pnl.add(pnlMainInterfaceFunction);
        pnlMainInterfaceFunction.setLayout(null);

        JLabel DeviceIndex = new JLabel("Device index\n");
        DeviceIndex.setFont(mainFont);
        DeviceIndex.setBounds(6, 24, 76, 27);
        pnlMainInterfaceFunction.add(DeviceIndex);

        JButton btnGetDeviceDescription = new JButton("getDeviceDescription");
        btnGetDeviceDescription.addActionListener(this.btnGetDeviceDescriptionListener);
        btnGetDeviceDescription.setFont(mainFont);
        btnGetDeviceDescription.setBounds(149, 24, 140, 27);
        pnlMainInterfaceFunction.add(btnGetDeviceDescription);

        JButton btnOpenDevice = new JButton("openDevice");
        btnOpenDevice.addActionListener(this.btnOpenDeviceListener);
        btnOpenDevice.setFont(mainFont);
        btnOpenDevice.setBounds(149, 54, 140, 27);
        pnlMainInterfaceFunction.add(btnOpenDevice);

        JButton btnCloseDevice = new JButton("closeDevice");
        btnCloseDevice.addActionListener(this.btnCloseDeviceListener);
        btnCloseDevice.setFont(mainFont);
        btnCloseDevice.setBounds(149, 84, 140, 27);
        pnlMainInterfaceFunction.add(btnCloseDevice);

        JButton btnIsDeviceOpened = new JButton("isDeviceOpened");
        btnIsDeviceOpened.addActionListener(this.btnIsDeviceOpenedListener);
        btnIsDeviceOpened.setFont(mainFont);
        btnIsDeviceOpened.setBounds(149, 114, 140, 27);
        pnlMainInterfaceFunction.add(btnIsDeviceOpened);

        this.txtfldDeviceIndex = new JTextField();
        this.txtfldDeviceIndex.setFont(mainFont);
        this.txtfldDeviceIndex.setBounds(86, 24, 43, 27);
        this.txtfldDeviceIndex.setText("0");
        pnlMainInterfaceFunction.add(this.txtfldDeviceIndex);
        this.txtfldDeviceIndex.setColumns(10);

        this.cmbbxPropertyID = new JComboBox();
        this.cmbbxPropertyID.setFont(mainFont);
        this.cmbbxPropertyID.setModel(new DefaultComboBoxModel(IBScanDevice.PropertyId.values()));
        this.cmbbxPropertyID.setBounds(6, 144, 283, 27);
        pnlMainInterfaceFunction.add(this.cmbbxPropertyID);

        JButton btnGetProperty = new JButton("getProperty");
        btnGetProperty.addActionListener(this.btnGetPropertyListener);
        btnGetProperty.setFont(mainFont);
        btnGetProperty.setBounds(6, 174, 140, 27);
        pnlMainInterfaceFunction.add(btnGetProperty);

        JButton btnSetProperty = new JButton("setProperty");
        btnSetProperty.addActionListener(this.btnSetPropertyListener);
        btnSetProperty.setFont(mainFont);
        btnSetProperty.setBounds(6, 204, 140, 27);
        pnlMainInterfaceFunction.add(btnSetProperty);

        this.txtfldPropertyValue = new JTextField();
        this.txtfldPropertyValue.setFont(mainFont);
        this.txtfldPropertyValue.setColumns(10);
        this.txtfldPropertyValue.setBounds(149, 203, 140, 27);
        pnlMainInterfaceFunction.add(this.txtfldPropertyValue);

        //
        // Set and Get LE Operation
        //

        JPanel pnlLEOperationMode = new JPanel();
        pnlLEOperationMode.setLayout(null);
        pnlLEOperationMode.setBorder(new TitledBorder(new EtchedBorder(EtchedBorder.LOWERED, null,
            null), "Set and Get LE Operation", TitledBorder.LEADING, TitledBorder.TOP, titleFont,
            new Color(0, 0, 0)));
        pnlLEOperationMode.setBounds(10, 392, 295, 83);
        pnl.add(pnlLEOperationMode);

        JButton btnGetLEOperationMode = new JButton("getLEOperationMode");
        btnGetLEOperationMode.addActionListener(this.btnGetLEOperationModeListener);
        btnGetLEOperationMode.setFont(mainFont);
        btnGetLEOperationMode.setBounds(6, 20, 140, 27);
        pnlLEOperationMode.add(btnGetLEOperationMode);

        JButton btnSetLEOperationMode = new JButton("setLEOperationMode");
        btnSetLEOperationMode.addActionListener(this.btnSetLEOperationModeListener);
        btnSetLEOperationMode.setFont(mainFont);
        btnSetLEOperationMode.setBounds(6, 50, 140, 27);
        pnlLEOperationMode.add(btnSetLEOperationMode);

        this.cmbbxLEOperationMode = new JComboBox();
        this.cmbbxLEOperationMode.setFont(mainFont);
        this.cmbbxLEOperationMode.setBounds(149, 50, 140, 27);
        this.cmbbxLEOperationMode.setModel(new DefaultComboBoxModel(IBScanDevice.LEOperationMode
            .values()));
        pnlLEOperationMode.add(this.cmbbxLEOperationMode);

        //
        // Set and Get LED Operation
        //

        JPanel pnlLEDOperation = new JPanel();
        pnlLEDOperation.setLayout(null);
        pnlLEDOperation.setBorder(new TitledBorder(new EtchedBorder(EtchedBorder.LOWERED, null,
            null), "Set and Get LED Operation", TitledBorder.LEADING, TitledBorder.TOP, titleFont,
            new Color(0, 0, 0)));
        pnlLEDOperation.setBounds(10, 487, 295, 83);
        pnl.add(pnlLEDOperation);

        JButton btnGetOperableLEDs = new JButton("getOperableLEDs");
        btnGetOperableLEDs.addActionListener(this.btnGetOperableLEDsListener);
        btnGetOperableLEDs.setFont(mainFont);
        btnGetOperableLEDs.setBounds(6, 20, 140, 27);
        pnlLEDOperation.add(btnGetOperableLEDs);

        JButton btnSetLEDs = new JButton("setLEDs");
        btnSetLEDs.addActionListener(this.btnSetLEDsListener);
        btnSetLEDs.setFont(mainFont);
        btnSetLEDs.setBounds(6, 50, 140, 27);
        pnlLEDOperation.add(btnSetLEDs);

        JButton btnGetLEDs = new JButton("getLEDs");
        btnGetLEDs.addActionListener(this.btnGetLEDsListener);
        btnGetLEDs.setFont(mainFont);
        btnGetLEDs.setBounds(149, 19, 140, 27);
        pnlLEDOperation.add(btnGetLEDs);

        this.txtfldLEDs = new JTextField();
        this.txtfldLEDs.setFont(mainFont);
        this.txtfldLEDs.setColumns(10);
        this.txtfldLEDs.setBounds(149, 50, 96, 27);
        pnlLEDOperation.add(this.txtfldLEDs);

        JLabel lblLEDsHex = new JLabel("(hex)");
        lblLEDsHex.setBounds(246, 50, 43, 27);
        pnlLEDOperation.add(lblLEDsHex);
        lblLEDsHex.setFont(mainFont);

        //
        // Image Acquisition
        //

        JPanel pnlImageAcquisition = new JPanel();
        pnlImageAcquisition.setLayout(null);
        pnlImageAcquisition.setBorder(new TitledBorder(new EtchedBorder(EtchedBorder.LOWERED, null,
            null), "Image Acquisition", TitledBorder.LEADING, TitledBorder.TOP, titleFont,
            new Color(0, 0, 0)));
        pnlImageAcquisition.setBounds(317, 97, 295, 184);
        pnl.add(pnlImageAcquisition);

        JLabel labelImageType = new JLabel("Image Type");
        labelImageType.setFont(mainFont);
        labelImageType.setBounds(6, 24, 76, 27);
        pnlImageAcquisition.add(labelImageType);

        JButton btnCaptureImageManually = new JButton("captureImageManually");
        btnCaptureImageManually.addActionListener(this.btnCaptureImageManuallyListener);
        btnCaptureImageManually.setFont(mainFont);
        btnCaptureImageManually.setBounds(6, 150, 283, 27);
        pnlImageAcquisition.add(btnCaptureImageManually);

        JButton btnBeginCaptureImage = new JButton("beginCaptureImage");
        btnBeginCaptureImage.addActionListener(this.btnBeginCaptureImageListener);
        btnBeginCaptureImage.setFont(mainFont);
        btnBeginCaptureImage.setBounds(6, 120, 140, 27);
        pnlImageAcquisition.add(btnBeginCaptureImage);

        JButton btnCancelCaptureImage = new JButton("cancelCaptureImage");
        btnCancelCaptureImage.addActionListener(this.btnCancelCaptureImageListener);
        btnCancelCaptureImage.setFont(mainFont);
        btnCancelCaptureImage.setBounds(149, 120, 140, 27);
        pnlImageAcquisition.add(btnCancelCaptureImage);

        this.cmbbxImageType = new JComboBox();
        this.cmbbxImageType.setFont(mainFont);
        this.cmbbxImageType.setBounds(94, 26, 195, 27);
        this.cmbbxImageType.setModel(new DefaultComboBoxModel(IBScanDevice.ImageType.values()));
        pnlImageAcquisition.add(this.cmbbxImageType);

        this.chckbxAutoContrastOptimization = new JCheckBox("Automatic contrast optimization");
        this.chckbxAutoContrastOptimization.setFont(mainFont);
        this.chckbxAutoContrastOptimization.setBounds(6, 55, 283, 23);
        pnlImageAcquisition.add(this.chckbxAutoContrastOptimization);

        this.chckbxAutoCaptureFingerprints = new JCheckBox("Automatic capture for fingerprints");
        this.chckbxAutoCaptureFingerprints.setFont(mainFont);
        this.chckbxAutoCaptureFingerprints.setBounds(6, 75, 283, 23);
        pnlImageAcquisition.add(this.chckbxAutoCaptureFingerprints);

        this.chckbxTriggerInvalidFingerCount =
            new JCheckBox("Trigger invalid finger count on auto-capture");
        this.chckbxTriggerInvalidFingerCount.setFont(mainFont);
        this.chckbxTriggerInvalidFingerCount.setBounds(6, 95, 283, 23);
        pnlImageAcquisition.add(this.chckbxTriggerInvalidFingerCount);

        //
        // Capture Status
        //

        JPanel pnlCaptureStatus = new JPanel();
        pnlCaptureStatus.setLayout(null);
        pnlCaptureStatus.setBorder(new TitledBorder(new EtchedBorder(EtchedBorder.LOWERED, null,
            null), "Capture Status", TitledBorder.LEADING, TitledBorder.TOP, titleFont, new Color(
            0, 0, 0)));
        pnlCaptureStatus.setBounds(315, 287, 295, 83);
        pnl.add(pnlCaptureStatus);

        JButton btnIsCaptureAvailable = new JButton("isCaptureAvailable");
        btnIsCaptureAvailable.addActionListener(this.btnIsCaptureAvailableListener);
        btnIsCaptureAvailable.setFont(mainFont);
        btnIsCaptureAvailable.setBounds(6, 20, 140, 27);
        pnlCaptureStatus.add(btnIsCaptureAvailable);

        JButton btnIsFingerTouching = new JButton("isFingerTouching");
        btnIsFingerTouching.addActionListener(this.btnIsFingerTouchingListener);
        btnIsFingerTouching.setFont(mainFont);
        btnIsFingerTouching.setBounds(75, 48, 140, 27);
        pnlCaptureStatus.add(btnIsFingerTouching);

        JButton btnIsCaptureActive = new JButton("isCaptureActive");
        btnIsCaptureActive.addActionListener(this.btnIsCaptureActiveListener);
        btnIsCaptureActive.setFont(mainFont);
        btnIsCaptureActive.setBounds(149, 20, 140, 27);
        pnlCaptureStatus.add(btnIsCaptureActive);

        //
        // Get and Set Contrast Value
        //

        JPanel pnlContrastValue = new JPanel();
        pnlContrastValue.setLayout(null);
        pnlContrastValue.setBorder(new TitledBorder(new EtchedBorder(EtchedBorder.LOWERED, null,
            null), "Set and Get Contrast Value", TitledBorder.LEADING, TitledBorder.TOP, titleFont,
            new Color(0, 0, 0)));
        pnlContrastValue.setBounds(315, 382, 295, 83);
        pnl.add(pnlContrastValue);

        JButton btnSetContrast = new JButton("setContrast");
        btnSetContrast.addActionListener(this.btnSetContrastListener);
        btnSetContrast.setFont(mainFont);
        btnSetContrast.setBounds(6, 50, 140, 27);
        pnlContrastValue.add(btnSetContrast);

        JButton btnGetContrast = new JButton("getContrast");
        btnGetContrast.addActionListener(this.btnGetContrastListener);
        btnGetContrast.setFont(mainFont);
        btnGetContrast.setBounds(6, 21, 140, 27);
        pnlContrastValue.add(btnGetContrast);

        this.txtfldContrastValue = new JTextField();
        this.txtfldContrastValue.setFont(mainFont);
        this.txtfldContrastValue.setColumns(10);
        this.txtfldContrastValue.setBounds(149, 50, 96, 27);
        pnlContrastValue.add(this.txtfldContrastValue);

        JLabel lblContrastLimits = new JLabel("(0 - 34)");
        lblContrastLimits.setFont(mainFont);
        lblContrastLimits.setBounds(249, 50, 43, 27);
        pnlContrastValue.add(lblContrastLimits);

        //
        // Callbacks Fired
        //

        JPanel pnlCallbacksFired = new JPanel();
        pnlCallbacksFired.setLayout(null);
        pnlCallbacksFired.setBorder(new TitledBorder(new EtchedBorder(EtchedBorder.LOWERED, null,
            null), "Callbacks Fired", TitledBorder.LEADING, TitledBorder.TOP, titleFont, new Color(
            0, 0, 0)));
        pnlCallbacksFired.setBounds(624, 97, 295, 304);
        pnl.add(pnlCallbacksFired);

        JLabel lblScanDeviceInitProgress = new JLabel("deviceInitProgress");
        lblScanDeviceInitProgress.setFont(mainFont);
        lblScanDeviceInitProgress.setBounds(43, 20, 107, 23);
        pnlCallbacksFired.add(lblScanDeviceInitProgress);

        this.txtfldScanDeviceInitValue = new JTextField();
        this.txtfldScanDeviceInitValue.setEditable(false);
        this.txtfldScanDeviceInitValue.setFont(mainFont);
        this.txtfldScanDeviceInitValue.setColumns(10);
        this.txtfldScanDeviceInitValue.setBounds(157, 20, 132, 28);
        pnlCallbacksFired.add(this.txtfldScanDeviceInitValue);

        JLabel lblScanDeviceCountChanged = new JLabel("deviceCountChanged");
        lblScanDeviceCountChanged.setFont(mainFont);
        lblScanDeviceCountChanged.setBounds(43, 48, 114, 23);
        pnlCallbacksFired.add(lblScanDeviceCountChanged);

        this.txtfldScanDeviceCountValue = new JTextField();
        this.txtfldScanDeviceCountValue.setEditable(false);
        this.txtfldScanDeviceCountValue.setFont(mainFont);
        this.txtfldScanDeviceCountValue.setColumns(10);
        this.txtfldScanDeviceCountValue.setBounds(157, 48, 132, 28);
        pnlCallbacksFired.add(this.txtfldScanDeviceCountValue);

        JLabel lblScanDeviceCommunicationBroken = new JLabel("deviceCommunicationBroken");
        lblScanDeviceCommunicationBroken.setFont(mainFont);
        lblScanDeviceCommunicationBroken.setBounds(43, 76, 153, 23);
        pnlCallbacksFired.add(lblScanDeviceCommunicationBroken);

        JLabel lblDeviceImagePreviewAvailable = new JLabel("imagePreviewAvailable");
        lblDeviceImagePreviewAvailable.setFont(mainFont);
        lblDeviceImagePreviewAvailable.setBounds(43, 104, 153, 23);
        pnlCallbacksFired.add(lblDeviceImagePreviewAvailable);

        JLabel lblDeviceFingerCountChanged = new JLabel("fingerCountChanged");
        lblDeviceFingerCountChanged.setFont(mainFont);
        lblDeviceFingerCountChanged.setBounds(43, 132, 107, 23);
        pnlCallbacksFired.add(lblDeviceFingerCountChanged);

        this.txtfldDeviceFingerCountValue = new JTextField();
        this.txtfldDeviceFingerCountValue.setEditable(false);
        this.txtfldDeviceFingerCountValue.setFont(mainFont);
        this.txtfldDeviceFingerCountValue.setColumns(10);
        this.txtfldDeviceFingerCountValue.setBounds(157, 132, 132, 28);
        pnlCallbacksFired.add(this.txtfldDeviceFingerCountValue);

        JLabel lblDeviceFingerQualityChanged = new JLabel("fingerQualityChanged");
        lblDeviceFingerQualityChanged.setFont(mainFont);
        lblDeviceFingerQualityChanged.setBounds(43, 160, 114, 23);
        pnlCallbacksFired.add(lblDeviceFingerQualityChanged);

        this.txtfldDeviceFingerQualityValue = new JTextField();
        this.txtfldDeviceFingerQualityValue.setFont(mainFont);
        this.txtfldDeviceFingerQualityValue.setEditable(false);
        this.txtfldDeviceFingerQualityValue.setColumns(10);
        this.txtfldDeviceFingerQualityValue.setBounds(157, 160, 132, 28);
        pnlCallbacksFired.add(this.txtfldDeviceFingerQualityValue);

        JLabel lblDeviceAcquisitionBegun = new JLabel("acquisitionBegun");
        lblDeviceAcquisitionBegun.setFont(mainFont);
        lblDeviceAcquisitionBegun.setBounds(43, 187, 132, 23);
        pnlCallbacksFired.add(lblDeviceAcquisitionBegun);

        JLabel lblDeviceImageResultAvailable = new JLabel("imageResultAvailable");
        lblDeviceImageResultAvailable.setFont(mainFont);
        lblDeviceImageResultAvailable.setBounds(43, 215, 132, 23);
        pnlCallbacksFired.add(lblDeviceImageResultAvailable);

        JLabel lblDeviceImageResultExtendedAvailable = new JLabel("imageResultExtendedAvailable");
        lblDeviceImageResultExtendedAvailable.setFont(new Font("Dialog", Font.PLAIN, 11));
        lblDeviceImageResultExtendedAvailable.setBounds(43, 242, 153, 23);
        pnlCallbacksFired.add(lblDeviceImageResultExtendedAvailable);

        JLabel lblDevicePlatenStateChanged = new JLabel("platenStateChanged");
        lblDevicePlatenStateChanged.setFont(mainFont);
        lblDevicePlatenStateChanged.setBounds(43, 270, 102, 23);
        pnlCallbacksFired.add(lblDevicePlatenStateChanged);

        this.txtfldDevicePlatenStateValue = new JTextField();
        this.txtfldDevicePlatenStateValue.setFont(mainFont);
        this.txtfldDevicePlatenStateValue.setEditable(false);
        this.txtfldDevicePlatenStateValue.setColumns(10);
        this.txtfldDevicePlatenStateValue.setBounds(157, 268, 132, 28);
        pnlCallbacksFired.add(this.txtfldDevicePlatenStateValue);

        this.btnScanDeviceInitProgress = new JButton("");
        this.btnScanDeviceInitProgress.setFont(mainFont);
        this.btnScanDeviceInitProgress.setBounds(10, 20, 21, 23);
        pnlCallbacksFired.add(this.btnScanDeviceInitProgress);

        this.btnScanDeviceCountChanged = new JButton("");
        this.btnScanDeviceCountChanged.setFont(mainFont);
        this.btnScanDeviceCountChanged.setBounds(10, 48, 21, 23);
        pnlCallbacksFired.add(this.btnScanDeviceCountChanged);

        this.btnScanDeviceCommunicationBroken = new JButton("");
        this.btnScanDeviceCommunicationBroken.setFont(mainFont);
        this.btnScanDeviceCommunicationBroken.setBounds(10, 76, 21, 23);
        pnlCallbacksFired.add(this.btnScanDeviceCommunicationBroken);

        this.btnDeviceImagePreviewAvailable = new JButton("");
        this.btnDeviceImagePreviewAvailable.setFont(mainFont);
        this.btnDeviceImagePreviewAvailable.setBounds(10, 104, 21, 23);
        pnlCallbacksFired.add(this.btnDeviceImagePreviewAvailable);

        this.btnDeviceFingerCountChanged = new JButton("");
        this.btnDeviceFingerCountChanged.setFont(mainFont);
        this.btnDeviceFingerCountChanged.setBounds(10, 132, 21, 23);
        pnlCallbacksFired.add(this.btnDeviceFingerCountChanged);

        this.btnDeviceFingerQualityChanged = new JButton("");
        this.btnDeviceFingerQualityChanged.setFont(mainFont);
        this.btnDeviceFingerQualityChanged.setBounds(10, 160, 21, 23);
        pnlCallbacksFired.add(this.btnDeviceFingerQualityChanged);

        this.btnDeviceAcquisitionBegun = new JButton("");
        this.btnDeviceAcquisitionBegun.setFont(mainFont);
        this.btnDeviceAcquisitionBegun.setBounds(10, 187, 21, 23);
        pnlCallbacksFired.add(this.btnDeviceAcquisitionBegun);

        this.btnDeviceImageResultAvailable = new JButton("");
        this.btnDeviceImageResultAvailable.setFont(mainFont);
        this.btnDeviceImageResultAvailable.setBounds(10, 215, 21, 23);
        pnlCallbacksFired.add(this.btnDeviceImageResultAvailable);

        this.btnDevicePlatenStateChanged = new JButton("");
        this.btnDevicePlatenStateChanged.setFont(mainFont);
        this.btnDevicePlatenStateChanged.setBounds(10, 270, 21, 23);
        pnlCallbacksFired.add(this.btnDevicePlatenStateChanged);
        
        this.btnDeviceImageResultExtendedAvailable = new JButton("");
        this.btnDeviceImageResultExtendedAvailable.setFont(new Font("Dialog", Font.PLAIN, 11));
        this.btnDeviceImageResultExtendedAvailable.setBounds(10, 242, 21, 23);
        pnlCallbacksFired.add(this.btnDeviceImageResultExtendedAvailable);
        
        //
        // Function Result
        //

        JPanel pnlFunctionResult = new JPanel();
        pnlFunctionResult.setLayout(null);
        pnlFunctionResult.setBorder(new TitledBorder(new EtchedBorder(EtchedBorder.LOWERED, null,
            null), "Function Result", TitledBorder.LEADING, TitledBorder.TOP, titleFont, new Color(
            0, 0, 0)));
        pnlFunctionResult.setBounds(620, 412, 295, 79);
        pnl.add(pnlFunctionResult);

        this.txtpnFunctionResult = new JTextPane();
        this.txtpnFunctionResult.setEditable(false);
        this.txtpnFunctionResult.setBounds(6, 22, 283, 51);
        this.txtpnFunctionResult.setFont(mainFont);
        pnlFunctionResult.add(this.txtpnFunctionResult);

        //
        // Additional Information
        //

        JPanel pnlAdditionalInformation = new JPanel();
        pnlAdditionalInformation.setLayout(null);
        pnlAdditionalInformation.setBorder(new TitledBorder(new EtchedBorder(EtchedBorder.LOWERED,
            null, null), "Additional Information", TitledBorder.LEADING, TitledBorder.TOP,
            titleFont, new Color(0, 0, 0)));
        pnlAdditionalInformation.setBounds(620, 502, 295, 149);
        pnl.add(pnlAdditionalInformation);

        this.txtpnAdditionalInformation = new JTextPane();
        this.txtpnAdditionalInformation.setEditable(false);
        this.txtpnAdditionalInformation.setBounds(6, 22, 283, 121);
        this.txtpnAdditionalInformation.setFont(mainFont);
        pnlAdditionalInformation.add(this.txtpnAdditionalInformation);

        //
        // Image Preview
        //

        JPanel pnlImagePreview = new JPanel();
        pnlImagePreview.setBorder(new TitledBorder(null, "Image Preview", TitledBorder.LEADING,
            TitledBorder.TOP, titleFont, new Color(0, 0, 0)));
        pnlImagePreview.setBounds(315, 472, 295, 217);
        pnl.add(pnlImagePreview);

        this.lblImagePreview = new JLabel(new ImageIcon());
        this.lblImagePreview.setBounds(321, 402, IMAGE_WIDTH, IMAGE_HEIGHT);
        this.lblImagePreview.addMouseListener(this.lblImagePreviewListener);
        pnlImagePreview.add(this.lblImagePreview);
        
        JButton btnCalculateNfiqScore = new JButton("calculateNfiqScore");
        btnCalculateNfiqScore.setFont(new Font("Dialog", Font.PLAIN, 11));
        btnCalculateNfiqScore.setBounds(389, 700, 140, 27);
        btnCalculateNfiqScore.addActionListener(this.btnCalculateNfiqScoreListener);
        pnl.add(btnCalculateNfiqScore);

        //
        // Logo
        //
        
        URL logoUrl = FunctionTester.class.getResource("/resources/Logo.png");
        JLabel lblLogo;
        if (logoUrl == null)
        {
    		lblLogo = new JLabel(new ImageIcon());
        }
        else
        {
        	lblLogo = new JLabel(new ImageIcon(logoUrl));
        }
        lblLogo.setBounds(10, 11, 905, 75);
        pnl.add(lblLogo);
        
        //
        // Initialize IBScan
        //

        this.ibScan = IBScan.getInstance();
        this.ibScan.setScanListener(this);
    }

    // //////////////////////////////////////////////////////////////////////////////////////////////
    // UI ELEMENTS
    // //////////////////////////////////////////////////////////////////////////////////////////////

    // Main Interface Function
    protected JTextField txtfldDeviceIndex;
    protected JTextField txtfldPropertyValue;
    protected JComboBox cmbbxPropertyID;

    // Set and Get LE Operation
    protected JComboBox cmbbxLEOperationMode;

    // Set and Get LED Operation
    protected JTextField txtfldLEDs;

    // Set and Get Contrast Value
    protected JTextField txtfldContrastValue;

    // Image Acquisition
    protected JComboBox cmbbxImageType;
    protected JCheckBox chckbxAutoContrastOptimization;
    protected JCheckBox chckbxAutoCaptureFingerprints;
    protected JCheckBox chckbxTriggerInvalidFingerCount;

    // Function Result
    protected JTextField txtfldScanDeviceInitValue;
    protected JTextField txtfldScanDeviceCountValue;
    protected JTextField txtfldDeviceFingerCountValue;
    protected JTextField txtfldDeviceFingerQualityValue;
    protected JTextField txtfldDevicePlatenStateValue;
    protected JButton btnScanDeviceInitProgress;
    protected JButton btnScanDeviceCountChanged;
    protected JButton btnScanDeviceCommunicationBroken;
    protected JButton btnDeviceImagePreviewAvailable;
    protected JButton btnDeviceFingerCountChanged;
    protected JButton btnDeviceFingerQualityChanged;
    protected JButton btnDeviceAcquisitionBegun;
    protected JButton btnDeviceImageResultAvailable;
    protected JButton btnDeviceImageResultExtendedAvailable;
    protected JButton btnDevicePlatenStateChanged;
    protected JTextPane txtpnFunctionResult;

    // Additional Information
    protected JTextPane txtpnAdditionalInformation;

    // Image Preview
    protected JLabel lblImagePreview;

    // //////////////////////////////////////////////////////////////////////////////////////////////
    // EVENT HANDLERS - Top Functions
    // //////////////////////////////////////////////////////////////////////////////////////////////

    // Handle clicks on "GetSDKVersion" button.
    private ActionListener btnGetSDKVersionListener = new ActionListener()
    {
        @Override
        public void actionPerformed(ActionEvent ae)
        {
            logPrintln("GetSDKVersion button pressed.");

            try
            {
                // Get SDK version and set "Additional Information" field.
                IBScan.SdkVersion sdkVersion = getIBScan().getSdkVersion();
                setFunctionResult("IBScan.getSDKVersion() successful");
                setAdditionalInformation(sdkVersion.toString());
            }
            catch (IBScanException ibse)
            {
                setFunctionResult("IBScan.getSDKVersion() returned exception "
                    + ibse.getType().toString() + ".");
                setAdditionalInformation("");
            }
        }
    };

    // Handle clicks on "GetDeviceCount" button.
    private ActionListener btnGetDeviceCountListener = new ActionListener()
    {
        @Override
        public void actionPerformed(ActionEvent ae)
        {
            logPrintln("GetDeviceCount button pressed.");

            try
            {
                // Get device count and set "Additional Information" field.
                int deviceCount = getIBScan().getDeviceCount();
                setFunctionResult("IBScan.getDeviceCount() successful");
                setAdditionalInformation("Number of Device(s): " + deviceCount);
            }
            catch (IBScanException ibse)
            {
                setFunctionResult("IBScan.getDeviceCount() returned exception "
                    + ibse.getType().toString() + ".");
                setAdditionalInformation("");
            }
        }
    };

    // //////////////////////////////////////////////////////////////////////////////////////////////
    // EVENT HANDLERS - Main Interface Function
    // //////////////////////////////////////////////////////////////////////////////////////////////

    // Handle clicks on "GetDeviceDescription" button.
    private ActionListener btnGetDeviceDescriptionListener = new ActionListener()
    {
        @Override
        public void actionPerformed(ActionEvent ae)
        {
            logPrintln("GetDeviceDescription button pressed; deviceIndex = " + getDeviceIndex()
                + ".");

            int deviceIndex = getDeviceIndex();

            if (deviceIndex == DEVICE_INDEX_INVALID)
            {
                // Alert user that device index is invalid.
                alertUser("Invalid device index.");
                setFunctionResult("");
                setAdditionalInformation("");
            }
            else
            {
                try
                {
                    // Get device description for the device index specified in
                    // "Device Index" field.
                    IBScan.DeviceDesc deviceDesc = getIBScan().getDeviceDescription(deviceIndex);
                    setFunctionResult("IBScan.getDeviceDescription() successful");
                    setAdditionalInformation(deviceDesc.toString());
                }
                catch (IBScanException ibse)
                {
                    setFunctionResult("IBScan.getDeviceDescription() returned exception "
                        + ibse.getType().toString() + ".");
                    setAdditionalInformation("");
                }
            }
        }
    };

    // Handle clicks on "OpenDevice" button.
    private ActionListener btnOpenDeviceListener = new ActionListener()
    {
        @Override
        public void actionPerformed(ActionEvent ae)
        {
            logPrintln("OpenDevice button pressed; deviceIndex = " + getDeviceIndex() + ".");

            int deviceIndex = getDeviceIndex();

            if (deviceIndex == DEVICE_INDEX_INVALID)
            {
                // Alert user that device index is invalid.
                alertUser("Invalid device index.");
                setFunctionResult("");
                setAdditionalInformation("");
            }
            else
            {
                if (getIBScanDevice() != null)
                {
                    // Close old device.
                    try
                    {
                        if (getIBScanDevice().isOpened())
                        {
                            getIBScanDevice().close();
                        }
                    }
                    catch (IBScanException ibse)
                    {
                        alertUser("Exception closing old device: " + ibse.getType().toString()
                            + ".");
                    }
                    setIBScanDevice(null);
                }

                // Local runnable class to perform action on background thread.
                class OpenDeviceThread extends Thread
                {
                    private int deviceIndexTemp;

                    OpenDeviceThread(int deviceIndexTemp)
                    {
                        this.deviceIndexTemp = deviceIndexTemp;
                    }

                    @Override
                    public void run()
                    {
                        try
                        {
                        	
                        	IBScan.DeviceDesc devDesc = null; 
                        	devDesc = getIBScan().getDeviceDescription(deviceIndexTemp);
                        	
                        	if (devDesc.isLocked == true)
                        	{
                        		String m_strCustomerKey = JOptionPane.showInputDialog("Customer Key");
                            	if (m_strCustomerKey == null) // Value is null
            					{
                            		// Input cancelled with Locked device
            						return;
            					}
                            	else 
                            	{
                            		getIBScan().setCustomerKey(this.deviceIndexTemp, HashType.SHA256, m_strCustomerKey);
                            	}
                        		
                        	}
                        	
                        	// Open device for the device index specified in
                            // "Device Index" field and save
                            // device.
                            IBScanDevice ibScanDeviceNew =
                                FunctionTester.this.getIBScan().openDevice(this.deviceIndexTemp);
                            FunctionTester.this.setIBScanDevice(ibScanDeviceNew);
                            SwingUtilities.invokeLater(new ReportResultsRunnable(
                                "IBScan.openDevice() successful", ""));
                        }
                        catch (IBScanException ibse)
                        {
                            SwingUtilities.invokeLater(new ReportResultsRunnable(
                                "IBScan.openDevice() returned exception "
                                    + ibse.getType().toString() + ".", ""));
                        }
                    }
                }

                // Create thread to open device.
                OpenDeviceThread openDeviceThread = new OpenDeviceThread(deviceIndex);
                openDeviceThread.start();
            }
        }
    };

    // Handle clicks on "CloseDevice" button.
    private ActionListener btnCloseDeviceListener = new ActionListener()
    {
        @Override
        public void actionPerformed(ActionEvent ae)
        {
            logPrintln("CloseDevice button pressed.");

            if (getIBScanDevice() == null)
            {
                // Alert user no device has been opened.
                alertUser("No device has been opened.");
                setFunctionResult("");
                setAdditionalInformation("");
            }
            else
            {
                try
                {
                    // Close open device.
                    getIBScanDevice().close();
                    setFunctionResult("IBScan.closeDevice() successful");
                    setAdditionalInformation("");
                }
                catch (IBScanException ibse)
                {
                    setFunctionResult("IBScan.closeDevice() returned exception "
                        + ibse.getType().toString() + ".");
                    setAdditionalInformation("");
                }
            }
        }
    };

    // Handle clicks on "IsDeviceOpened" button.
    private ActionListener btnIsDeviceOpenedListener = new ActionListener()
    {
        @Override
        public void actionPerformed(ActionEvent ae)
        {
            logPrintln("IsDeviceOpened button pressed.");

            if (getIBScanDevice() == null)
            {
                // Alert user no device has been opened.
                alertUser("No device has been opened.");
                setFunctionResult("");
                setAdditionalInformation("");
            }
            else
            {
                // Test whether device is open.
                boolean open = getIBScanDevice().isOpened();
                setFunctionResult("");
                if (open)
                    setAdditionalInformation("Device is open.");
                else
                    setAdditionalInformation("Device is not open.");
            }
        }
    };

    // Handle clicks on "GetProperty" button.
    private ActionListener btnGetPropertyListener = new ActionListener()
    {
        @Override
        public void actionPerformed(ActionEvent ae)
        {
            logPrintln("GetProperty button pressed; propertyID = " + getPropertyId().toString()
                + ".");

            if (getIBScanDevice() == null)
            {
                // Alert user no device has been opened.
                alertUser("No device has been opened.");
                setFunctionResult("");
                setAdditionalInformation("");
            }
            else
            {
                try
                {
                    // Get the property highlighted in the "PropertyID" combo
                    // box for opened device and put
                    // the value in the "Additional Information" field.
                    IBScanDevice.PropertyId propertyId = getPropertyId();
                    String propertyValue = getIBScanDevice().getProperty(propertyId);
                    setFunctionResult("IBScanDevice.getProperty() successful");
                    setAdditionalInformation("Property value: " + propertyValue);
                }
                catch (IBScanException ibse)
                {
                    setFunctionResult("IBScanDevice.getProperty() returned exception "
                        + ibse.getType().toString() + ".");
                    setAdditionalInformation("");
                }
            }
        }
    };

    // Handle clicks on "SetProperty" button.
    private ActionListener btnSetPropertyListener = new ActionListener()
    {
        @Override
        public void actionPerformed(ActionEvent ae)
        {
            logPrintln("SetProperty button pressed; propertyID = " + getPropertyId().toString()
                + "; propertyValue = " + getPropertyValue() + ".");

            if (getIBScanDevice() == null)
            {
                // Alert user no device has been opened.
                alertUser("No device has been opened.");
                setFunctionResult("");
                setAdditionalInformation("");
            }
            else
            {
                try
                {
                    // Set the property highlighted in the "ProductID" combo box
                    // to the value in the
                    // "Property Value" field for active device.
                    IBScanDevice.PropertyId propertyId = getPropertyId();
                    String propertyValue = getPropertyValue();
                    getIBScanDevice().setProperty(propertyId, propertyValue);
                    setFunctionResult("IBScanDevice.setProperty() successful");
                    setAdditionalInformation("");
                }
                catch (IBScanException ibse)
                {
                    setFunctionResult("IBScanDevice.setProperty() returned exception "
                        + ibse.getType().toString() + ".");
                    setAdditionalInformation("");
                }
            }
        }
    };

    // //////////////////////////////////////////////////////////////////////////////////////////////
    // EVENT HANDLERS - Set and Get LE Operation
    // //////////////////////////////////////////////////////////////////////////////////////////////

    // Handle clicks on "GetLEOperationMode" button.
    private ActionListener btnGetLEOperationModeListener = new ActionListener()
    {
        @Override
        public void actionPerformed(ActionEvent ae)
        {
            logPrintln("GetLEOperationMode button pressed.");

            if (getIBScanDevice() == null)
            {
                // Alert user no device has been opened.
                alertUser("No device has been opened.");
                setFunctionResult("");
                setAdditionalInformation("");
            }
            else
            {
                try
                {
                    // Get LE operation mode for active device and set
                    // "Additional Information" field.
                    IBScanDevice.LEOperationMode leOperationMode =
                        getIBScanDevice().getLEOperationMode();
                    setFunctionResult("IBScanDevice.getLEOperationMode() successful");
                    setAdditionalInformation("LE Operation Mode: " + leOperationMode.toString());
                }
                catch (IBScanException ibse)
                {
                    setFunctionResult("IBScanDevice.getLEOperationMode() returned exception "
                        + ibse.getType().toString() + ".");
                    setAdditionalInformation("");
                }
            }
        }
    };

    // Handle clicks on "SetLEOperationMode" button.
    private ActionListener btnSetLEOperationModeListener = new ActionListener()
    {
        @Override
        public void actionPerformed(ActionEvent ae)
        {
            logPrintln("SetLEOperationMode button pressed; leOperationMode = "
                + getLEOperationMode().toString() + ".");

            if (getIBScanDevice() == null)
            {
                // Alert user no device has been opened.
                alertUser("No device has been opened.");
                setFunctionResult("");
                setAdditionalInformation("");
            }
            else
            {
                try
                {
                    // Set LE operation mode for active device to value in
                    // "LE Operation Mode" combo box.
                    IBScanDevice.LEOperationMode leOperationMode = getLEOperationMode();
                    getIBScanDevice().setLEOperationMode(leOperationMode);
                    setFunctionResult("IBScanDevice.setLEOperationMode() successful");
                    setAdditionalInformation("");
                }
                catch (IBScanException ibse)
                {
                    setFunctionResult("IBScanDevice.setLEOperationMode() returned exception "
                        + ibse.getType().toString() + ".");
                    setAdditionalInformation("");
                }
            }
        }
    };

    // //////////////////////////////////////////////////////////////////////////////////////////////
    // EVENT HANDLERS - Set and Get LED Operation
    // //////////////////////////////////////////////////////////////////////////////////////////////

    // Handle clicks on "GetOperableLEDs" button.
    private ActionListener btnGetOperableLEDsListener = new ActionListener()
    {
        @Override
        public void actionPerformed(ActionEvent ae)
        {
            logPrintln("GetOperableLEDs button pressed; deviceIndex = " + getDeviceIndex() + ".");

            // Get information about operable LEDs for active device and set
            // "Additional
            // Information" field.
            if (getIBScanDevice() == null)
            {
                // Alert user no device has been opened.
                alertUser("No device has been opened.");
                setFunctionResult("");
                setAdditionalInformation("");
            }
            else
            {
                try
                {
                    // Get LE operation mode for active device and set
                    // "Additional Information" field.
                    IBScanDevice.LedState ledState = getIBScanDevice().getOperableLEDs();
                    setFunctionResult("IBScanDevice.getOperableLEDs() successful");
                    setAdditionalInformation(ledState.toString());
                }
                catch (IBScanException ibse)
                {
                    setFunctionResult("IBScanDevice.getOperableLEDs() returned exception "
                        + ibse.getType().toString() + ".");
                    setAdditionalInformation("");
                }
            }
        }
    };

    // Handle clicks on "GetLEDs" button.
    private ActionListener btnGetLEDsListener = new ActionListener()
    {
        @Override
        public void actionPerformed(ActionEvent ae)
        {
            logPrintln("GetLEDs button pressed.");

            if (getIBScanDevice() == null)
            {
                // Alert user no device has been opened.
                alertUser("No device has been opened.");
                setFunctionResult("");
                setAdditionalInformation("");
            }
            else
            {
                try
                {
                    // Get active LEDs for active device and set
                    // "Additional Information" field.
                    long activeLEDs = getIBScanDevice().getLEDs();
                    setFunctionResult("IBScanDevice.getLEDs() successful");
                    setAdditionalInformation("LED status: " + String.format("%1$08X", activeLEDs));
                }
                catch (IBScanException ibse)
                {
                    setFunctionResult("IBScanDevice.getLEDs() returned exception "
                        + ibse.getType().toString() + ".");
                    setAdditionalInformation("");
                }
            }
        }
    };

    // Handle clicks on "SetLEDs" button.
    private ActionListener btnSetLEDsListener = new ActionListener()
    {
        @Override
        public void actionPerformed(ActionEvent ae)
        {
            logPrintln("SetLEDs button pressed; LEDs = 0x" + String.format("%1$08X", getLEDs())
                + ".");

            if (getIBScanDevice() == null)
            {
                // Alert user no device has been opened.
                alertUser("No device has been opened.");
                setFunctionResult("");
                setAdditionalInformation("");
            }
            else
            {
                long activeLEDs;

                activeLEDs = getLEDs();
                if (activeLEDs == LEDS_INVALID)
                {
                    // Alert user that LED specifier is invalid.
                    alertUser("Invalid LED specifier.");
                    setFunctionResult("");
                    setAdditionalInformation("");
                }
                else
                {
                    try
                    {
                        // Set active LEDs for active device to value in "LEDs"
                        // field.
                        getIBScanDevice().setLEDs(activeLEDs);
                        setFunctionResult("IBScanDevice.setLEDs() successful");
                        setAdditionalInformation("");
                    }
                    catch (IBScanException ibse)
                    {
                        setFunctionResult("IBScanDevice.setLEDs() returned exception "
                            + ibse.getType().toString() + ".");
                        setAdditionalInformation("");
                    }
                }
            }
        }
    };

    // //////////////////////////////////////////////////////////////////////////////////////////////
    // EVENT HANDLERS - Image Acquisition
    // //////////////////////////////////////////////////////////////////////////////////////////////

    // Handle clicks on "BeginCaptureImage" button.
    private ActionListener btnBeginCaptureImageListener = new ActionListener()
    {
        @Override
        public void actionPerformed(ActionEvent ae)
        {
            logPrintln("BeginCaptureImage button pressed; imageType = " + getImageType()
                + "; imageResolution = " + getImageResolution() + "; captureOptions = "
                + getCaptureOptions() + ".");

            if (getIBScanDevice() == null)
            {
                // Alert user no device has been opened.
                alertUser("No device has been opened.");
                setFunctionResult("");
                setAdditionalInformation("");
            }
            else
            {
                // Begin capturing image for active device.
                int captureOptions = getCaptureOptions();
                IBScanDevice.ImageType imageType = getImageType();
                IBScanDevice.ImageResolution imageResolution = getImageResolution();

                try
                {
                    // Begin capturing image for active device.
                    FunctionTester.this.getIBScanDevice().beginCaptureImage(imageType, 
                        imageResolution,captureOptions);
                    SwingUtilities.invokeLater(new ReportResultsRunnable(
                        "IBScanDevice.beginCaptureImage() successful", ""));
                }
                catch (IBScanException ibse)
                {
                    SwingUtilities.invokeLater(new ReportResultsRunnable(
                        "IBScanDevice.beginCaptureImage() returned exception "
                            + ibse.getType().toString() + ".", ""));
                }
            }
        }
    };

    // Utility class to report results back to display thread.
    private class ReportResultsRunnable implements Runnable
    {
        private String functionResult;
        private String additionalInformation;

        ReportResultsRunnable(String functionResult, String additionalInformation)
        {
            this.functionResult = functionResult;
            this.additionalInformation = additionalInformation;
        }

        @Override
        public void run()
        {
            FunctionTester.this.setFunctionResult(this.functionResult);
            FunctionTester.this.setAdditionalInformation(this.additionalInformation);
        }
    }

    // Handle clicks on "CancelCaptureImage" button.
    private ActionListener btnCancelCaptureImageListener = new ActionListener()
    {
        @Override
        public void actionPerformed(ActionEvent ae)
        {
            // Cancel capturing image for active device.
            logPrintln("CancelCaptureImage button pressed.");

            if (getIBScanDevice() == null)
            {
                // Alert user no device has been opened.
                alertUser("No device has been opened.");
                setFunctionResult("");
                setAdditionalInformation("");
            }
            else
            {
                try
                {
                    // Cancel capturing image for active device.
                    getIBScanDevice().cancelCaptureImage();
                    setFunctionResult("IBScanDevice.cancelCaptureImage() successful");
                    setAdditionalInformation("");
                }
                catch (IBScanException ibse)
                {
                    setFunctionResult("IBScanDevice.cancelCaptureImage() returned exception "
                        + ibse.getType().toString() + ".");
                    setAdditionalInformation("");
                }
            }
        }
    };

    // Handle clicks on "TakeResultImageManually" button.
    private ActionListener btnCaptureImageManuallyListener = new ActionListener()
    {
        @Override
        public void actionPerformed(ActionEvent ae)
        {
            logPrintln("TakeResultImageManually button pressed.");

            if (getIBScanDevice() == null)
            {
                // Alert user no device has been opened.
                alertUser("No device has been opened.");
                setFunctionResult("");
                setAdditionalInformation("");
            }
            else
            {
                try
                {
                    // Capture image manually for active device
                    getIBScanDevice().captureImageManually();
                    setFunctionResult("IBScanDevice.takeResultImageManually() successful");
                    setAdditionalInformation("");
                }
                catch (IBScanException ibse)
                {
                    setFunctionResult("IBScanDevice.takeResultImageManually() returned exception "
                        + ibse.getType().toString() + ".");
                    setAdditionalInformation("");
                }
            }
        }
    };

    // //////////////////////////////////////////////////////////////////////////////////////////////
    // EVENT HANDLERS - Capture Status
    // //////////////////////////////////////////////////////////////////////////////////////////////

    // Handle clicks on "IsCaptureAvailable" button.
    private ActionListener btnIsCaptureAvailableListener = new ActionListener()
    {
        @Override
        public void actionPerformed(ActionEvent ae)
        {
            logPrintln("IsCaptureAvailable button pressed; imageType = " + getImageType()
                + "; imageResolution = " + getImageResolution() + ".");

            if (getIBScanDevice() == null)
            {
                // Alert user no device has been opened.
                alertUser("No device has been opened.");
                setFunctionResult("");
                setAdditionalInformation("");
            }
            else
            {
                try
                {
                    // Determine whether capture is available for active device
                    // and populate
                    // "Additional Information" field.
                    IBScanDevice.ImageType imageType = getImageType();
                    IBScanDevice.ImageResolution imageResolution = getImageResolution();
                    boolean available =
                        getIBScanDevice().isCaptureAvailable(imageType, imageResolution);
                    setFunctionResult("IBScanDevice.isCaptureAvailable() successful");
                    if (available)
                        setAdditionalInformation(imageType.toString() + " mode is available");
                    else
                        setAdditionalInformation(imageType.toString() + " mode is not available");
                }
                catch (IBScanException ibse)
                {
                    setFunctionResult("IBScanDevice.isCaptureAvailable() returned exception "
                        + ibse.getType().toString() + ".");
                    setAdditionalInformation("");
                }
            }
        }
    };

    // Handle clicks on "IsCaptureActive" button.
    private ActionListener btnIsCaptureActiveListener = new ActionListener()
    {
        @Override
        public void actionPerformed(ActionEvent ae)
        {
            logPrintln("IsCaptureActive button pressed.");

            if (getIBScanDevice() == null)
            {
                // Alert user no device has been opened.
                alertUser("No device has been opened.");
                setFunctionResult("");
                setAdditionalInformation("");
            }
            else
            {
                try
                {
                    // Determine whether capture is active for active device and
                    // populate
                    // "Additional Information" field.
                    boolean active = getIBScanDevice().isCaptureActive();
                    setFunctionResult("IBScanDevice.isCaptureActive() successful");
                    if (active)
                        setAdditionalInformation("Capturing...");
                    else
                        setAdditionalInformation("Not capturing...");
                }
                catch (IBScanException ibse)
                {
                    setFunctionResult("IBScanDevice.isCaptureActive() returned exception "
                        + ibse.getType().toString() + ".");
                    setAdditionalInformation("");
                }
            }
        }
    };

    // Handle clicks on "IsFingerTouching" button.
    private ActionListener btnIsFingerTouchingListener = new ActionListener()
    {
        @Override
        public void actionPerformed(ActionEvent ae)
        {
            logPrintln("isFingerTouching button pressed; deviceIndex = " + getDeviceIndex() + ".");

            if (getIBScanDevice() == null)
            {
                // Alert user no device has been opened.
                alertUser("No device has been opened.");
                setFunctionResult("");
                setAdditionalInformation("");
            }
            else
            {
                try
                {
                    // Determine whether finger is touched on active device and
                    // populate "Additional
                    // Information" field.
                    boolean touched = getIBScanDevice().isFingerTouching();
                    setFunctionResult("IBScanDevice.isFingerTouching() successful");
                    if (touched)
                        setAdditionalInformation("Detected finger");
                    else
                        setAdditionalInformation("No finger detected");
                }
                catch (IBScanException ibse)
                {
                    setFunctionResult("IBScanDevice.isFingerTouching() returned exception "
                        + ibse.getType().toString() + ".");
                    setAdditionalInformation("");
                }
            }
        }
    };

    // //////////////////////////////////////////////////////////////////////////////////////////////
    // EVENT HANDLERS - Set and Get Contrast Value
    // //////////////////////////////////////////////////////////////////////////////////////////////

    // Handle clicks on "GetContrast" button.
    private ActionListener btnGetContrastListener = new ActionListener()
    {
        @Override
        public void actionPerformed(ActionEvent ae)
        {
            logPrintln("GetContrast button pressed.");

            if (getIBScanDevice() == null)
            {
                // Alert user no device has been opened.
                alertUser("No device has been opened.");
                setFunctionResult("");
                setAdditionalInformation("");
            }
            else
            {
                try
                {
                    // Get the contrast for the active device and populate the
                    // "Additional
                    // Information" field.
                    int contrastValue = getIBScanDevice().getContrast();
                    setFunctionResult("IBScanDevice.getContrast() successful");
                    setAdditionalInformation("Contrast: " + contrastValue);
                }
                catch (IBScanException ibse)
                {
                    setFunctionResult("IBScanDevice.getContrast() returned exception "
                        + ibse.getType().toString() + ".");
                    setAdditionalInformation("");
                }
            }
        }
    };

    // Handle clicks on "SetContrast" button.
    private ActionListener btnSetContrastListener = new ActionListener()
    {
        @Override
        public void actionPerformed(ActionEvent ae)
        {
            logPrintln("SetContrast button pressed; contrastValue = " + getContrastValue() + ".");

            if (getIBScanDevice() == null)
            {
                // Alert user no device has been opened.
                alertUser("No device has been opened.");
                setFunctionResult("");
                setAdditionalInformation("");
            }
            else
            {
                int contrastValue;

                contrastValue = getContrastValue();
                if (contrastValue == CONTRAST_INVALID)
                {
                    // Alert user that contrast value is invalid.
                    alertUser("Invalid contrast value.");
                    setFunctionResult("");
                    setAdditionalInformation("");
                }
                else
                {
                    try
                    {
                        // Set the contrast for the active device to the value
                        // in the "Contrast Value" field.
                        getIBScanDevice().setContrast(contrastValue);
                        setFunctionResult("IBScanDevice.contrast() successful");
                        setAdditionalInformation("");
                    }
                    catch (IBScanException ibse)
                    {
                        setFunctionResult("IBScanDevice.contrast() returned exception "
                            + ibse.getType().toString() + ".");
                        setAdditionalInformation("");
                    }
                }
            }
        }
    };

    // //////////////////////////////////////////////////////////////////////////////////////////////
    // EVENT HANDLERS - Image Preview
    // //////////////////////////////////////////////////////////////////////////////////////////////

    // Handle right-clicks on the image preview to save image.
    private MouseAdapter lblImagePreviewListener = new MouseAdapter()
    {
        // Handle clicks on right-click menu on image preview.
        private ActionListener imageSaveListener = new ActionListener()
        {
            // Get extension of file name.
            protected String getExtension(String fileName)
            {
                String extension = "";
                int index = fileName.lastIndexOf('.');
                if ((index >= 0) && (index != fileName.length() - 1))
                {
                    extension = fileName.substring(index + 1).toLowerCase();
                }

                return (extension);
            }

            @Override
            public void actionPerformed(ActionEvent ae)
            {
                // Custom file filter to choose only image files.
                FileFilter imageFilter = new FileFilter()
                {
                    @Override
                    public boolean accept(File f)
                    {
                        String extension = getExtension(f.getName());
                        String[] formats = ImageIO.getWriterFormatNames();

                        // Filter by image formats
                        for (String format : formats)
                        {
                            if (extension.equals(format.toLowerCase()))
                            {
                                return (true);
                            }
                        }
                        return (false);
                    }

                    @Override
                    public String getDescription()
                    {
                        String s;
                        String[] suffixes = ImageIO.getWriterFileSuffixes();

                        // Return description with list of acceptable suffixes
                        s = "Image files (";
                        for (int i = 0; i < suffixes.length; i++)
                        {
                            s += suffixes[i];
                            if (i != suffixes.length - 1)
                            {
                                s += ", ";
                            }
                        }
                        s += ")";
                        return (s);
                    }
                };

                // Show chooser for output image.
                JFileChooser chooser = new JFileChooser();
                chooser.setFileFilter(imageFilter);
                int returnVal = chooser.showSaveDialog(FunctionTester.this);
                if (returnVal == JFileChooser.APPROVE_OPTION)
                {
                    if (FunctionTester.this.lastScanImage != null)
                    {
                        // Determine image type by extension. If invalid
                        // extension, default to BMP.
                        String extension = getExtension(chooser.getSelectedFile().getName());
                        boolean ok = imageFilter.accept(chooser.getSelectedFile());
                        if (!ok)
                        {
                            extension = "BMP";
                        }
                        try
                        {
                            boolean okWrite = ImageIO.write(FunctionTester.this.lastScanImage, 
                                extension, chooser.getSelectedFile());
                            if (!okWrite)
                            {
                                logPrintln("Failure saving image to file "
                                    + chooser.getSelectedFile().getAbsolutePath());
                            }
                        }
                        catch (IOException e)
                        {
                            logPrintln("Failure saving image to file "
                                + chooser.getSelectedFile().getAbsolutePath());
                        }
                    }
                }
            }
        };

        @Override
        public void mousePressed(MouseEvent e)
        {
            if (e.isPopupTrigger())
            {
                if (FunctionTester.this.lastScanImage != null)
                {
                    JPopupMenu menu = new JPopupMenu();
                    JMenuItem menuItem = new JMenuItem("Save image...");
                    menuItem.addActionListener(this.imageSaveListener);
                    menu.add(menuItem);
                    menu.show(e.getComponent(), e.getX(), e.getY());
                }
            }
        }

        @Override
        public void mouseReleased(MouseEvent e)
        {
            mousePressed(e);
        }
    };

    // Handle clicks on "CalculateNfiqScore" button.
    private ActionListener btnCalculateNfiqScoreListener = new ActionListener()
    {
        @Override
        public void actionPerformed(ActionEvent ae)
        {
            logPrintln("CalculateNfiqScore button pressed.");

            class CalculateNfiqScoreThread extends Thread
            {
                @Override
                public void run()
                {
                	IBScanDevice ibScanDevice = getIBScanDevice();
                	ImageData    imageData    = FunctionTester.this.lastScanImageData;
                	
                	if ((ibScanDevice == null) || (imageData == null))
                	{
                		alertUser("No device open or no image captured.");
                	}
                	else
                	{
                		try
                		{
                			int nfiqScore = ibScanDevice.calculateNfiqScore(imageData);
                			SwingUtilities.invokeLater(new ReportResultsRunnable("IBScanDevice.calculateNfiqScore() successful.", 
                					"NFIQ score = " + nfiqScore));
                		}
                		catch (IBScanException ibse)
                		{
                			SwingUtilities.invokeLater(new ReportResultsRunnable("IBScanDevice.calculateNfiqScore() returned exception " 
                					+ ibse.getType().toString() + ".", ""));
                		}
                	}
                }
            }

            // Calculate on a background thread.
            CalculateNfiqScoreThread cnst = new CalculateNfiqScoreThread();
            cnst.start();
        }
    };

    // //////////////////////////////////////////////////////////////////////////////////////////////
    // PROTECTED INTERFACE
    // //////////////////////////////////////////////////////////////////////////////////////////////

    protected static final int DEVICE_INDEX_INVALID = -12345678;
    protected static final long LEDS_INVALID = -12345678;
    protected static final int CONTRAST_INVALID = -12345678;

    // The IB scan through which the bus is accessed.
    protected IBScan        ibScan            = null;
    protected IBScanDevice  ibScanDevice      = null;
    protected BufferedImage lastScanImage     = null;
    protected ImageData     lastScanImageData = null;
    
    // Get IBScan.
    protected IBScan getIBScan()
    {
        return (this.ibScan);
    }

    // Get opened or null IBScanDevice.
    protected IBScanDevice getIBScanDevice()
    {
        return (this.ibScanDevice);
    }

    // Set IBScanDevice.
    protected void setIBScanDevice(IBScanDevice ibScanDevice)
    {
        this.ibScanDevice = ibScanDevice;
        if (ibScanDevice != null)
        {
            ibScanDevice.setScanDeviceListener(this);
        }
    }

    // Get device index.
    protected int getDeviceIndex()
    {
        String deviceIndexString = this.txtfldDeviceIndex.getText();
        int deviceIndex;

        try
        {
            deviceIndex = Integer.parseInt(deviceIndexString);
        }
        catch (NumberFormatException nfe)
        {
            deviceIndex = DEVICE_INDEX_INVALID;
        }

        return (deviceIndex);
    }

    // Get property ID.
    protected IBScanDevice.PropertyId getPropertyId()
    {
        IBScanDevice.PropertyId propertyID =
            (IBScanDevice.PropertyId) this.cmbbxPropertyID.getSelectedItem();

        return (propertyID);
    }

    // Get property value.
    protected String getPropertyValue()
    {
        String propertyValue = this.txtfldPropertyValue.getText();

        return (propertyValue);
    }

    // Get LE operation mode.
    protected IBScanDevice.LEOperationMode getLEOperationMode()
    {
        IBScanDevice.LEOperationMode leOperationMode =
            (IBScanDevice.LEOperationMode) this.cmbbxLEOperationMode.getSelectedItem();

        return (leOperationMode);
    }

    // Get LEDs.
    protected long getLEDs()
    {
        String ledsString = this.txtfldLEDs.getText();
        long leds;

        try
        {
            leds = Long.parseLong(ledsString, 16);
        }
        catch (NumberFormatException nfe)
        {
            leds = LEDS_INVALID;
        }

        return (leds);
    }

    // Get image type.
    protected IBScanDevice.ImageType getImageType()
    {
        IBScanDevice.ImageType imageType =
            (IBScanDevice.ImageType) this.cmbbxImageType.getSelectedItem();

        return (imageType);
    }

    // Get image type.
    protected IBScanDevice.ImageResolution getImageResolution()
    {
        // Currently only 500ppi is supported.
        IBScanDevice.ImageResolution imageResolution = IBScanDevice.ImageResolution.RESOLUTION_500;

        return (imageResolution);
    }

    // Get contrast value.
    protected int getContrastValue()
    {
        String contrastValueString = this.txtfldContrastValue.getText();
        int contrastValue;

        try
        {
            contrastValue = Integer.parseInt(contrastValueString, 16);
        }
        catch (NumberFormatException nfe)
        {
            contrastValue = CONTRAST_INVALID;
        }

        return (contrastValue);
    }

    // Get capture options.
    protected int getCaptureOptions()
    {
        int options = 0;

        if (this.chckbxAutoContrastOptimization.isSelected())
        {
            options |= IBScanDevice.OPTION_AUTO_CONTRAST;
        }
        if (this.chckbxAutoCaptureFingerprints.isSelected())
        {
            options |= IBScanDevice.OPTION_AUTO_CAPTURE;
        }
        if (this.chckbxTriggerInvalidFingerCount.isSelected())
        {
            options |= IBScanDevice.OPTION_IGNORE_FINGER_COUNT;
        }

        return (options);
    }

    // Set function result.
    protected void setFunctionResult(String s)
    {
        this.txtpnFunctionResult.setText(s);
    }

    // Set additional information.
    protected void setAdditionalInformation(String s)
    {
        this.txtpnAdditionalInformation.setText(s);
    }

    // Alert user to error.
    protected void alertUser(String s)
    {
        JOptionPane.showMessageDialog(this, s, "ERROR", JOptionPane.ERROR_MESSAGE);
    }

    // Light a "callback" button when a IBScan or IBScanDevice callback is
    // triggered.
    protected void lightCallbackButton(JButton btn, int nTime_ms)
    {
        btn.doClick(nTime_ms);
    }

    // Log statement to System.out.
    protected static void logPrintln(String ln)
    {
        // System.out.println(ln);
    }

    // //////////////////////////////////////////////////////////////////////////////////////////////
    // PRIVATE INTERFACE
    // //////////////////////////////////////////////////////////////////////////////////////////////

    private static final int CLICK_TIME_MS = 5;//50;
    private static final int IMAGE_WIDTH = 280;//279;
    private static final int IMAGE_HEIGHT = 200;//201;

    // //////////////////////////////////////////////////////////////////////////////////////////////
    // PUBLIC INTERFACE: IBScanListener METHODS
    // //////////////////////////////////////////////////////////////////////////////////////////////

    @Override
    public void scanDeviceCountChanged(int deviceCount)
    {
        logPrintln("Callback \"deviceCountChanged\" received");

        class DisplayDeviceCountRunnable implements Runnable
        {
            private final int deviceCountTemp;

            DisplayDeviceCountRunnable(int deviceCountTemp)
            {
                this.deviceCountTemp = deviceCountTemp;
            }

            @Override
            public void run()
            {
                // Update value in deviceCountValue field and flash button.
                FunctionTester.this.txtfldScanDeviceCountValue.setText("" + this.deviceCountTemp);
                lightCallbackButton(FunctionTester.this.btnScanDeviceCountChanged, 50);
            }
        }

        // UI updates must occur on UI thread.
        SwingUtilities.invokeLater(new DisplayDeviceCountRunnable(deviceCount));
    }

    @Override
    public void scanDeviceInitProgress(int deviceIndex, int progressValue)
    {
        logPrintln("Callback \"deviceInitProgress\" received");

        class DisplayDeviceInitProgressRunnable implements Runnable
        {
            private final int progressValueTemp;

            DisplayDeviceInitProgressRunnable(int progressValueTemp)
            {
                this.progressValueTemp = progressValueTemp;
            }

            @Override
            public void run()
            {
                // Update value in deviceInitValue field and flash button.
                FunctionTester.this.txtfldScanDeviceInitValue.setText("" + this.progressValueTemp);
                lightCallbackButton(FunctionTester.this.btnScanDeviceInitProgress, 50);
            }
        }

        // UI updates must occur on UI thread.
        SwingUtilities.invokeLater(new DisplayDeviceInitProgressRunnable(progressValue));
    }

    @Override
    public void scanDeviceOpenComplete(int deviceIndex, IBScanDevice device, IBScanException exception)
    {
        logPrintln("Callback \"deviceOpenComplete\" received");
    }

    // //////////////////////////////////////////////////////////////////////////////////////////////
    // PUBLIC INTERFACE: IBScanDeviceListener METHODS
    // //////////////////////////////////////////////////////////////////////////////////////////////

    @Override
    public void deviceCommunicationBroken(IBScanDevice device)
    {
        logPrintln("Callback \"scanCommunicationBroken\" received");

        // UI updates must occur on UI thread.
        SwingUtilities.invokeLater(new Runnable() 
        {
            @Override
            public void run()
            {
                // Flash button.
                lightCallbackButton(FunctionTester.this.btnScanDeviceCommunicationBroken, 50);
            }            
        });
    }

    @Override
    public void deviceImagePreviewAvailable(IBScanDevice device, ImageData image)
    {
        logPrintln("Callback \"scanPreviewImageAvailable\" received with (image = "
            + image.width + "x" + image.height + " " + image.bitsPerPixel + "-bpp "
            + image.format.toString() + " pitch=" + image.pitch + " res=" + image.resolutionX
            + "x" + image.resolutionY + ")");

        class DisplayImagePreviewRunnable implements Runnable
        {
            ImageIcon imageIconTemp;

            DisplayImagePreviewRunnable(ImageIcon imageIconTemp)
            {
                this.imageIconTemp = imageIconTemp;
            }

            @Override
            public void run()
            {
                // Set image in image preview and flash button.
                FunctionTester.this.lblImagePreview.setIcon(this.imageIconTemp);
                lightCallbackButton(FunctionTester.this.btnDeviceImagePreviewAvailable, 5);
            }
        }

        // UI updates must occur on UI thread.
        int destWidth = IMAGE_WIDTH;
		int destHeight = IMAGE_HEIGHT;
		int outImageSize = destWidth * destHeight;

		byte[] outImage = new byte[outImageSize];
		Arrays.fill(outImage, (byte) 255);

		try {
			int nRc = ibScanDevice.generateZoomOutImageEx(image.buffer,
					image.width, image.height, outImage, destWidth, destHeight,
					(byte) 255);
		} catch (IBScanException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

		// /////////////////////////////////////////////////////////////////////////////////////////////////////////////////
		Image imageJ = image.toImage(outImage, IMAGE_WIDTH, IMAGE_HEIGHT);
        ImageIcon imageIcon = new ImageIcon(imageJ);
        SwingUtilities.invokeLater(new DisplayImagePreviewRunnable(imageIcon));
    }

    @Override
    public void deviceFingerCountChanged(IBScanDevice device, FingerCountState fingerState)
    {
        logPrintln("Callback \"fingerCountChanged\" received (fingerState = "
            + fingerState.toString() + ")");

        class DisplayFingerCountRunnable implements Runnable
        {
            private final FingerCountState fingerStateTemp;

            DisplayFingerCountRunnable(FingerCountState fingerStateTemp)
            {
                this.fingerStateTemp = fingerStateTemp;
            }

            @Override
            public void run()
            {
                // Update value in fingerCountValue field and flash button.
                FunctionTester.this.txtfldDeviceFingerCountValue.setText(this.fingerStateTemp.toString());
                lightCallbackButton(FunctionTester.this.btnDeviceFingerCountChanged, 50);
            }
        }

        // UI updates must occur on UI thread.
        SwingUtilities.invokeLater(new DisplayFingerCountRunnable(fingerState));
    }

    @Override
    public void deviceFingerQualityChanged(IBScanDevice device, FingerQualityState[] fingerQualities)
    {
        logPrintln("Callback \"fingerQualityChanged\" received (length = " + fingerQualities.length
            + "; fingerQualities = " + fingerQualities[0].toString() + ")");

        class DisplayFingerQualityRunnable implements Runnable
        {
            private final FingerQualityState[] fingerQualitiesTemp;

            DisplayFingerQualityRunnable(FingerQualityState[] fingerQualitiesTemp)
            {
                this.fingerQualitiesTemp = fingerQualitiesTemp;
            }

            @Override
            public void run()
            {
                // Update value in fingerQuality field and flash button.
                FunctionTester.this.txtfldDeviceFingerQualityValue.setText(this.fingerQualitiesTemp[0]
                    .toString());
                lightCallbackButton(FunctionTester.this.btnDeviceFingerQualityChanged, 50);
            }
        }

        // UI updates must occur on UI thread.
        SwingUtilities.invokeLater(new DisplayFingerQualityRunnable(fingerQualities));
    }

    @Override
    public void deviceAcquisitionBegun(IBScanDevice device, ImageType imageType)
    {
        logPrintln("Callback \"acquisitionTaking\" received (imageType=" + imageType.toString()
            + ")");

        // UI updates must occur on UI thread.
        SwingUtilities.invokeLater(new Runnable() 
        {
            @Override
            public void run()
            {
                // Flash button.
                lightCallbackButton(FunctionTester.this.btnDeviceAcquisitionBegun, 50);
            }           
        });
    }

    @Override
    public void deviceAcquisitionCompleted(IBScanDevice device, ImageType imageType)
    {
        logPrintln("Callback \"acquisitionCompleted\" received (imageType=" + imageType.toString()
            + ")");
    }

    @Override
    public void deviceImageResultAvailable(IBScanDevice device, ImageData image, ImageType imageType,
        ImageData[] splitImageArray)
    {
        logPrintln("Callback \"imageResultAvailable\" received (image = " + image.width + "x"
                + image.height + " " + image.bitsPerPixel + "-bpp " + image.format.toString()
                + " pitch=" + image.pitch + " res=" + image.resolutionX + "x" + image.resolutionY
                + ")");

        class DisplayImageResultRunnable implements Runnable
        {
            DisplayImageResultRunnable()
            {
            }

            @Override
            public void run()
            {
                // Set image in image preview, preserve image for saving, and
                // flash button.
                lightCallbackButton(FunctionTester.this.btnDeviceImageResultAvailable, 50);
            }
        }

        // UI updates must occur on UI thread.
        SwingUtilities.invokeLater(new DisplayImageResultRunnable());
    }

    @Override
    public void deviceImageResultExtendedAvailable(IBScanDevice device, IBScanException imageStatus,
    		ImageData image, ImageType imageType, int detectedFingerCount, ImageData[] segmentImageArray,
    		SegmentPosition[] segmentPositionArray)
    {
        logPrintln("Callback \"imageResultExtendedAvailable\" received (image = " + image.width + "x"
            + image.height + " " + image.bitsPerPixel + "-bpp " + image.format.toString()
            + " pitch=" + image.pitch + " res=" + image.resolutionX + "x" + image.resolutionY
            + ")");

        class DisplayImageResultExtendedRunnable implements Runnable
        {
            BufferedImage imageTemp;
            ImageData     imageDataTemp;

            DisplayImageResultExtendedRunnable(BufferedImage imageTemp, ImageData imageDataTemp)
            {
                this.imageTemp     = imageTemp;
                this.imageDataTemp = imageDataTemp;
            }

            @Override
            public void run()
            {
                // Set image in image preview, preserve image for saving, and
                // flash button.
                lightCallbackButton(FunctionTester.this.btnDeviceImageResultExtendedAvailable, 50);
                int destWidth = IMAGE_WIDTH;
				int destHeight = IMAGE_HEIGHT;
				int outImageSize = destWidth * destHeight;

				byte[] outImage = new byte[outImageSize];
				Arrays.fill(outImage, (byte) 255);

				try {
					int nRc = ibScanDevice.generateZoomOutImageEx(
							imageDataTemp.buffer,
							imageDataTemp.width,
							imageDataTemp.height, outImage, destWidth,
							destHeight, (byte) 255);
				} catch (IBScanException e1) {
					// TODO Auto-generated catch block
					e1.printStackTrace();
				}

				// /////////////////////////////////////////////////////////////////////////////////////////////////////////////////
				Image imageJ = imageDataTemp.toImage(outImage,
						IMAGE_WIDTH, IMAGE_HEIGHT);
				ImageIcon imageIcon = new ImageIcon(imageJ);
                FunctionTester.this.lblImagePreview.setIcon(imageIcon);
                FunctionTester.this.lastScanImage = this.imageTemp;
                FunctionTester.this.lastScanImageData = this.imageDataTemp;
            }
        }

        // UI updates must occur on UI thread.
        BufferedImage imageJ = image.toImage();
        SwingUtilities.invokeLater(new DisplayImageResultExtendedRunnable(imageJ, image));
    }

    @Override
    public void devicePlatenStateChanged(IBScanDevice device, PlatenState platenState)
    {
        logPrintln("Callback \"platenStateChanged\" received (platenState="
            + platenState.toString() + ")");

        class DisplayPlatenStateRunnable implements Runnable
        {
            private final PlatenState platenStateTemp;

            DisplayPlatenStateRunnable(PlatenState platenStateTemp)
            {
                this.platenStateTemp = platenStateTemp;
            }

            @Override
            public void run()
            {
                // Update value in platenStateValue field and flash button.
                FunctionTester.this.txtfldDevicePlatenStateValue.setText(this.platenStateTemp.toString());
                lightCallbackButton(FunctionTester.this.btnDevicePlatenStateChanged, 50);
            }
        }

        // UI updates must occur on UI thread.
        SwingUtilities.invokeLater(new DisplayPlatenStateRunnable(platenState));
    }

    @Override
    public void deviceWarningReceived(IBScanDevice device, IBScanException warning)
    {
        logPrintln("Callback \"warningReceived\" received");
    }

	@Override
	public void devicePressedKeyButtons(IBScanDevice device, int pressedKeyButtons)
    {
        logPrintln("Callback \"device key button\" pressed");
	}
}
