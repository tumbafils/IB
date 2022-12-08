/* *************************************************************************************************
 * IBScanDevice.h
 * 
 * DESCRIPTION:
 *     JNI wrapper for IBScanUltimate library
 *     http://www.integratedbiometrics.com
 *
 * NOTES:
 *     Copyright (c) Integrated Biometrics, 2013-2017
 *
 * HISTORY:
 *     2013/03/01  First version.
 *     2013/03/22  Added function to calculate NFIQ score.
 *     2013/03/26  Added function to get extended result image.
 *     2013/10/18  Added captureImageExtended() native method.
 *                 Added enableEvent() native method.
 *     2013/11/24  Added generateZoomOutImageExNative() native method.
 *     2015/04/07  Added getEnhancedImageReservedNative() native method.
 *                 Added setPropertyReservedNative() native method.
 *                 Added wsqEncodeToFileNative() native method.
 *     2015/12/11  Added function for detecting the key button of device was pressed.
 *                 Added getOperableBeeperNative() native method.
 *                 Added setBeeperNative() native method.
 *     2017/04/27  Added getCombineImageExNative() native method.
 *     2017/12/11  Added generateDisplayImageNative() native method.
 *     2018/04/27  Added removeFingerImageNative() native method.
 *                 Added addFingerImageNative() native method. 
 *                 Added isFingerDuplicatedNative() native method. 
 *                 Added isValidFingerGeometryNative() native method.
 *                 Added SaveBitmapImageNative() native method.
 *     2019/06/21  Added SetEncryptionKeyNative() native method.
 *     2022/04/13  Added IBSU_ConvertImageToISOANSI() native method.
 ************************************************************************************************ */

#include <jni.h>

#ifndef IBSCANDEVICE_H_
#define IBSCANDEVICE_H_

#ifdef __cplusplus
extern "C" {
#endif

/***************************************************************************************************
 * GLOBAL MACROS
 **************************************************************************************************/

#define IBSCANDEVICE_BUILD_JNI_FNCT(name) Java_com_integratedbiometrics_ibscanultimate_IBScanDevice_##name

/***************************************************************************************************
 * GLOBAL FUNCTION PROTOTYPES
 **************************************************************************************************/

/*
 * Handle load of library.
 */
jboolean IBScanDevice_OnLoad(
    JavaVM *vm,
    void   *reserved);

/*
 * Perform additional steps to open device.
 */
void IBScanDevice_Open(
    JNIEnv  *pEnv,
    long     devHandle,
    jobject  devHandleJ);

/***************************************************************************************************
 * JNI FUNCTION PROTOTYPES
 **************************************************************************************************/

/*
 * private native void closeNative(NativeError error);
 */
JNIEXPORT void JNICALL IBSCANDEVICE_BUILD_JNI_FNCT(closeNative)(
    JNIEnv  *pEnv,
	jobject  tthis,
	jobject  error);

/*
 * private native void enableEvent(int eventTypeCode, boolean enable, NativeError error);
 */
JNIEXPORT void JNICALL IBSCANDEVICE_BUILD_JNI_FNCT(enableEventNative)(
    JNIEnv  *pEnv,
	jobject  tthis,
	jint     eventCode,
	jboolean enable,
	jobject  error);

/*
 * private native void setPropertyNative(int propertyIdCode, String propertyValue,
 *     NativeError error);
 */
JNIEXPORT void JNICALL IBSCANDEVICE_BUILD_JNI_FNCT(setPropertyNative)(
    JNIEnv  *pEnv,
	jobject  tthis,
	jint     propertyIDCode,
	jstring  propertyValue,
	jobject  error);

/*
 * private native void setPropertyReservedNative(String reservedKey, int propertyIdCode, String propertyValue,
 *     NativeError error);
 */
JNIEXPORT void JNICALL IBSCANDEVICE_BUILD_JNI_FNCT(setPropertyReservedNative)(
    JNIEnv  *pEnv,
	jobject  tthis,
	jstring  reservedKey,
	jint     propertyIDCode,
	jstring  propertyValue,
	jobject  error);

/*
 * private native String getPropertyNative(int propertyIdCode, NativeError error);
 */
JNIEXPORT jstring JNICALL IBSCANDEVICE_BUILD_JNI_FNCT(getPropertyNative)(
    JNIEnv  *pEnv,
	jobject  tthis,
	jint     propertyIDCode,
	jobject  error);

/*
 * private native boolean isCaptureAvailableNative(int imageTypeCode, int imageResolutionCode,
 *     NativeError error);
 */
JNIEXPORT jboolean JNICALL IBSCANDEVICE_BUILD_JNI_FNCT(isCaptureAvailableNative)(
    JNIEnv  *pEnv,
    jobject  tthis,
    jint     imageType,
    jint     imageResolution,
    jobject  error);

/*
 * private native void beginCaptureImageNative(int imageTypeCode, int imageResolutionCode,
 *     int captureOptions, NativeError error);
 */
JNIEXPORT void JNICALL IBSCANDEVICE_BUILD_JNI_FNCT(beginCaptureImageNative)(
    JNIEnv  *pEnv,
	jobject  tthis,
	jint     imageType,
	jint     imageResolution,
	jint     captureOptions,
	jobject  error);

/*
 * private native void cancelCaptureImageNative(NativeError error);
 */
JNIEXPORT void JNICALL IBSCANDEVICE_BUILD_JNI_FNCT(cancelCaptureImageNative)(
    JNIEnv  *pEnv, 
    jobject  tthis,
    jobject  error);

/*
 * private native boolean isCaptureActiveNative(NativeError error);
 */
JNIEXPORT jboolean JNICALL IBSCANDEVICE_BUILD_JNI_FNCT(isCaptureActiveNative)(
    JNIEnv  *pEnv,
	jobject  tthis,
	jobject  error);

/*
 * private native void captureImageManuallyNative(NativeError error);
 */
JNIEXPORT void JNICALL IBSCANDEVICE_BUILD_JNI_FNCT(captureImageManuallyNative)(
    JNIEnv  *pEnv,
	jobject  tthis,
    jobject  error);

/*
 * private native int getContrastNative(NativeError error);
 */
JNIEXPORT jint JNICALL IBSCANDEVICE_BUILD_JNI_FNCT(getContrastNative)(
    JNIEnv  *pEnv,
	jobject  tthis,
	jobject  error);

/*
 * private native void setContrastNative(int contrastValue, NativeError error);
 */
JNIEXPORT void JNICALL IBSCANDEVICE_BUILD_JNI_FNCT(setContrastNative)(
    JNIEnv  *pEnv,
	jobject  tthis,
	jint     contrastValue,
	jobject  error);

/*
 * private native void setLEOperationModeNative(int leOperationModeCode,
 *     NativeError error);
 */
JNIEXPORT void JNICALL IBSCANDEVICE_BUILD_JNI_FNCT(setLEOperationModeNative)(
    JNIEnv  *pEnv,
	jobject  tthis,
    jint     leOperationModeCode,
    jobject  error);

/*
 * private native int getLEOperationModeNative(NativeError error);
 */
JNIEXPORT jint JNICALL IBSCANDEVICE_BUILD_JNI_FNCT(getLEOperationModeNative)(
    JNIEnv  *pEnv,
	jobject  tthis,
    jobject  error);

/*
 * private native boolean isFingerTouchingNative(NativeError error);
 */
JNIEXPORT jboolean JNICALL IBSCANDEVICE_BUILD_JNI_FNCT(isFingerTouchingNative)(
    JNIEnv *pEnv,
	jobject  tthis,
	jobject  error);

/*
 * private native LedState getOperableLEDsNative(NativeError error);
 */
JNIEXPORT jobject JNICALL IBSCANDEVICE_BUILD_JNI_FNCT(getOperableLEDsNative)(
    JNIEnv  *pEnv,
	jobject  tthis,
	jobject  error);

/*
 * private native long getLEDsNative(NativeError error);
 */
JNIEXPORT jlong JNICALL IBSCANDEVICE_BUILD_JNI_FNCT(getLEDsNative)(
    JNIEnv  *pEnv,
	jobject  tthis,
    jobject  error);

/*
 * private native void setLEDsNative(long activeLEDs, NativeError error);
 */
JNIEXPORT void JNICALL IBSCANDEVICE_BUILD_JNI_FNCT(setLEDsNative)(
    JNIEnv  *pEnv,
	jobject  tthis,
	jlong    activeLEDs,
	jobject  error);

/*
 * private native Object[] captureImageNative(NativeError error);
 */
JNIEXPORT jobjectArray JNICALL IBSCANDEVICE_BUILD_JNI_FNCT(captureImageNative)(
    JNIEnv  *pEnv,
	jobject  tthis,
	jobject  error);

/*
 * private native Object[] captureImageExtendedNative(NativeError error);
 */
JNIEXPORT jobjectArray JNICALL IBSCANDEVICE_BUILD_JNI_FNCT(captureImageExtendedNative)(
    JNIEnv  *pEnv,
	jobject  tthis,
	jobject  error);

/*
 * private native PlatenState getPlatenStateAtCaptureNative(NativeError error);
 */
JNIEXPORT jint JNICALL IBSCANDEVICE_BUILD_JNI_FNCT(getPlatenStateAtCaptureNative)(
    JNIEnv  *pEnv,
	jobject  tthis,
	jobject  error);

/*
 * private native RollingData getRollingInfoNative(NativeError error);
 */
JNIEXPORT jobject JNICALL IBSCANDEVICE_BUILD_JNI_FNCT(getRollingInfoNative)(
    JNIEnv  *pEnv,
	jobject  tthis,
	jobject  error);

/*
 * private native int calculateNfiqScoreNative(ImageData image, NativeError error);
 */
JNIEXPORT jint JNICALL IBSCANDEVICE_BUILD_JNI_FNCT(calculateNfiqScoreNative)(
    JNIEnv  *pEnv,
	jobject  tthis,
	jobject  image,
	jobject  error);

/*
 * private native Object[] getResultImageExtNative(int fingerPositionCode, NativeError error);
 */
JNIEXPORT jobjectArray JNICALL IBSCANDEVICE_BUILD_JNI_FNCT(getResultImageExtNative)(
	JNIEnv  *pEnv,
	jobject  tthis,
	jint     fingerPositionCode,
	jobject  error);

/*
 * private native int wsqEncodeToFileNative(..., NativeError error);
 */
JNIEXPORT jint JNICALL IBSCANDEVICE_BUILD_JNI_FNCT(wsqEncodeToFileNative)(
    JNIEnv    *pEnv,
    jobject    tthis,
    jstring    filePath,
	jbyteArray image,
	jint       width,
	jint       height,
	jint       pitch,
	jint       bitPerPixel,
	jint       pixelPerInch,
	jdouble    bitRate,
	jstring    commentText,
    jobject    error);

/*
 * private native int SavePngImageNative(..., NativeError error);
 */
JNIEXPORT jint JNICALL IBSCANDEVICE_BUILD_JNI_FNCT(SavePngImageNative)(
    JNIEnv  *pEnv,
	jobject  tthis,
	jstring	filapath,
	jbyteArray	image,
	jint	width,
	jint	height,
	jint	pitch,
	jdouble resX,
	jdouble resY,
	jobject  error);

/*
 * private native int SaveJP2ImageNative(..., NativeError error);
 */
JNIEXPORT jint JNICALL IBSCANDEVICE_BUILD_JNI_FNCT(SaveJP2ImageNative)(
    JNIEnv  *pEnv,
	jobject  tthis,
	jstring	filapath,
	jbyteArray	image,
	jint	width,
	jint	height,
	jint	pitch,
	jdouble resX,
	jdouble resY,
	jint	fQuality,
	jobject  error);

/*
 * private native int SaveBitmapImageNative(..., NativeError error);
 */
JNIEXPORT jint JNICALL IBSCANDEVICE_BUILD_JNI_FNCT(SaveBitmapImageNative)(
    JNIEnv  *pEnv,
	jobject  tthis,
	jstring	filapath,
	jbyteArray	image,
	jint	width,
	jint	height,
	jint	pitch,
	jdouble resX,
	jdouble resY,
	jobject  error);

/*
 * private native int generateZoomOutImageExNative(..., NativeError error);
 */
JNIEXPORT jint JNICALL IBSCANDEVICE_BUILD_JNI_FNCT(generateZoomOutImageExNative)(
	JNIEnv *pEnv,
	jobject tthis,
	jbyteArray inImage,
	jint inWidth,
	jint inHeight,
	jbyteArray outImage,
	jint outWidth,
	jint outHeight,
	jbyte bkColor,
	jobject  error);

/*
 * private native int getEnhancedImageNative();
 */
JNIEXPORT jobjectArray JNICALL IBSCANDEVICE_BUILD_JNI_FNCT(getEnhancedImageReservedNative)(
    JNIEnv  *pEnv,
	jobject  tthis,
    jstring  reservedKey,
	jobject  image,
	jobject  error);

/*
 * private native int getCombineImageNative();
 */
JNIEXPORT jobject JNICALL IBSCANDEVICE_BUILD_JNI_FNCT(getCombineImageNative)(
    JNIEnv  *pEnv,
	jobject  tthis,
    jobject  image1,
	jobject  image2,
	jint  whichHand,
	jobject  error);

/*
 * private native int getOperableBeeperNative(NativeError error);
 */
JNIEXPORT jint JNICALL IBSCANDEVICE_BUILD_JNI_FNCT(getOperableBeeperNative)(
	JNIEnv  *pEnv,
	jobject  tthis,
	jobject  error);

/*
 * private native void setBeeper(IBSU_BeepPattern beepPattern, long soundTone, long duration, long reserved_1, long reserved_2, NativeError error);
 */
JNIEXPORT void JNICALL IBSCANDEVICE_BUILD_JNI_FNCT(setBeeperNative)(
	JNIEnv  *pEnv,
	jobject  tthis,
	jint     beepPattern,
	jint     soundTone,
	jint     duration,
	jint     reserved_1,
	jint     reserved_2,
	jobject  error);

/*
 * private native int getCombineImageExNative();
 */
JNIEXPORT jobjectArray JNICALL IBSCANDEVICE_BUILD_JNI_FNCT(getCombineImageExNative)(
    JNIEnv  *pEnv,
	jobject  tthis,
    jobject  image1,
	jobject  image2,
	jint  whichHand,
	jobject  error);

/*
 * private native int generateDisplayImageNative(..., NativeError error);
 */
JNIEXPORT jint JNICALL IBSCANDEVICE_BUILD_JNI_FNCT(generateDisplayImageNative)(
	JNIEnv *pEnv,
	jobject tthis,
	jbyteArray inImage,
	jint inWidth,
	jint inHeight,
	jbyteArray outImage,
	jint outWidth,
	jint outHeight,
	jbyte bkColor,
	jint outFormat,
	jint outQualityLevel,
	jboolean outVerticalFlip,
	jobject  error);

/*
 * private native int removeFingerImage(..., NativeError	error);
 */
JNIEXPORT jint JNICALL IBSCANDEVICE_BUILD_JNI_FNCT(removeFingerImageNative)(
    JNIEnv  *pEnv,
	jobject  tthis,
    jlong 	 fIndex,
	jobject  error);

/*
 * private native int addFingerImage(..., NativeError	error);
 */
JNIEXPORT jint JNICALL IBSCANDEVICE_BUILD_JNI_FNCT(addFingerImageNative)(
    JNIEnv  *pEnv,
	jobject  tthis,
	jobject  image,
    jlong 	 fIndex,
    jint 	 imageType,
    jboolean flagForce,
	jobject  error);

/*
 * private native int isFingerDuplicated(..., NativeError	error);
 */
JNIEXPORT jlong JNICALL IBSCANDEVICE_BUILD_JNI_FNCT(isFingerDuplicatedNative)(
    JNIEnv  *pEnv,
	jobject  tthis,
	jobject  image,
    jlong 	 fIndex,
    jint 	 imageType,
    jint 	 securityLevel,
	jobject  error);

/*
 * private native int isValidFingerGeometry(..., NativeError	error);
 */
JNIEXPORT jboolean JNICALL IBSCANDEVICE_BUILD_JNI_FNCT(isValidFingerGeometryNative)(
    JNIEnv  *pEnv,
	jobject  tthis,
	jobject  image,
    jlong 	 fIndex,
    jint 	 imageType,
	jobject  error);

/*
 * private native int GetSpoofScoreNative(String reservedKey, ImageData image, NativeError error);
 */
JNIEXPORT jint JNICALL IBSCANDEVICE_BUILD_JNI_FNCT(GetSpoofScoreNative)(
    JNIEnv  *pEnv,
	jobject  tthis,
	jstring  reservedKey,
	jobject  image,
	jobject  error);


/*
 * private native int SetEncryptionKeyNative(String encryptionKey, EncyptionMode encMode, NativeError error);
 */
JNIEXPORT jint JNICALL IBSCANDEVICE_BUILD_JNI_FNCT(SetEncryptionKeyNative)(
    JNIEnv  *pEnv,
	jobject  tthis,
	jbyteArray  encryptionKey,
	jint     encmode,
	jobject  error);

/*
 * private native int isFingerDuplicatedNative(..., NativeError	error);
 */
JNIEXPORT jlong JNICALL IBSCANDEVICE_BUILD_JNI_FNCT(isFingerDuplicatedNative)(
    JNIEnv  *pEnv,
	jobject  tthis,
	jobject  image,
    jlong 	 fIndex,
    jint 	 imageType,
    jint 	 securityLevel,
	jobject  error);
	
/*
 * private native Object ConvertImageToISOANSINative(ImageDataExt[] image, int imageCount, int imageFormat, int STDformat);
 */
JNIEXPORT jobject JNICALL IBSCANDEVICE_BUILD_JNI_FNCT(ConvertImageToISOANSINative)(
    JNIEnv  *pEnv,
	jobject  tthis,
	jobjectArray segmentImageArray,
	jint     imageCount,
	jint	 imageFormat,
	jint	 STDformat,
	jobject  error);	
	
/*
 * private native int SaveStandardFileNative(StandardFormatData STDFormatData, String filename, NativeError error);
 */
JNIEXPORT jint JNICALL IBSCANDEVICE_BUILD_JNI_FNCT(SaveStandardFileNative)(
    JNIEnv  *pEnv,
	jobject  tthis,
	jobject  StandardFileFormatData,
	jstring  filePath,
	jobject  error);	
	
#ifdef __cplusplus
} //extern "C" {
#endif 

#endif /* IBSCANDEVICE_H_ */
