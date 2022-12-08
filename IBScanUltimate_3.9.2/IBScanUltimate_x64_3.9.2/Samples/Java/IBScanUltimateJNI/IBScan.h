/* *************************************************************************************************
 * IBScan.h
 *
 * DESCRIPTION:
 *     JNI wrapper for IBScanUltimate library
 *     http://www.integratedbiometrics.com
 *
 * NOTES:
 *     Copyright (c) Integrated Biometrics, 2013
 *
 * HISTORY:
 *     2013/03/01  First version.
 *     2013/04/06  Add function to enable/disable trace log.
 *     2017/11/08  Add function isWritableDirectory() to check whether a directrly is writable
 *     2018/11/19  Add function getRequiredSDKVersion()
 *     2020/09/21  Add function setCustomerKey(), getErrorString()
 ************************************************************************************************ */

#include <jni.h>

#ifndef IBSCAN_H_
#define IBSCAN_H_

#ifdef __cplusplus
extern "C" { 
#endif 

/***************************************************************************************************
 * GLOBAL MACROS
 **************************************************************************************************/

#define IBSCAN_BUILD_JNI_FNCT(name) Java_com_integratedbiometrics_ibscanultimate_IBScan_##name

/***************************************************************************************************
 * GLOBAL FUNCTION PROTOTYPES
 **************************************************************************************************/

/*
 * Handle load of library.
 */
jboolean IBScan_OnLoad(
    JavaVM *vm,
    void   *reserved);

/*
 * Handle load of library.
 */
JNIEXPORT jint JNICALL JNI_OnLoad(
    JavaVM *vm,
    void   *reserved);

/***************************************************************************************************
 * JNI FUNCTION PROTOTYPES
 **************************************************************************************************/

/*
 * private native void init();
 */
JNIEXPORT void JNICALL IBSCAN_BUILD_JNI_FNCT(initNative)(
    JNIEnv  *pEnv,
    jobject  tthis);
    
/*
 * private native void enableTraceLog(boolean on, IBScan.NativeError error);
 */
JNIEXPORT void JNICALL IBSCAN_BUILD_JNI_FNCT(enableTraceLogNative)(
    JNIEnv  *pEnv,
    jobject  tthis,
    jboolean on,
    jobject  error);

/*
 * private native IBScan.SdkVersion getSdkVersionNative(IBScan.NativeError error);
 */
JNIEXPORT jobject JNICALL IBSCAN_BUILD_JNI_FNCT(getSdkVersionNative)(
    JNIEnv  *pEnv,
	jobject  tthis,
	jobject  error);

/*
 * private native int getDeviceCountNative(IBScan.NativeError error);
 */
JNIEXPORT jint JNICALL IBSCAN_BUILD_JNI_FNCT(getDeviceCountNative)(
    JNIEnv  *pEnv,
	jobject  tthis,
	jobject  error);

/*
 * private native IBScan.DeviceDesc getDeviceDescNative(int deviceIndex, IBScan.NativeError error);
 */
JNIEXPORT jobject JNICALL IBSCAN_BUILD_JNI_FNCT(getDeviceDescNative)(
    JNIEnv  *pEnv,
    jobject  tthis,
	jint     deviceIndex,
	jobject  error);

/*
 * private native IBScanDevice openDeviceNative(int deviceIndex, IBScan.NativeError error);
 */
JNIEXPORT jobject JNICALL IBSCAN_BUILD_JNI_FNCT(openDeviceNative)(
    JNIEnv  *pEnv,
	jobject  tthis,
	jint     deviceIndex,
	jobject  error);

/*
 * private native IBScanDevice openDeviceExNativeEx(int deviceIndex, String uniformityMaskPath,
 *     IBScan.NativeError error);
 */
JNIEXPORT jobject JNICALL IBSCAN_BUILD_JNI_FNCT(openDeviceExNative)(
    JNIEnv  *pEnv,
	jobject  tthis,
	jint     deviceIndex,
	jstring  uniformityMaskPath,
	jobject  error);

/*
 * private native void openDeviceAsyncNative(int deviceIndex, IBScan.NativeError error);
 */
JNIEXPORT void JNICALL IBSCAN_BUILD_JNI_FNCT(openDeviceAsyncNative)(
    JNIEnv  *pEnv,
	jobject  tthis,
	jint     deviceIndex,
	jobject  error);

/*
 * private native void openDeviceAsyncExNative(int deviceIndex, String uniformityMaskPath,
 *     IBScan.NativeError error);
 */
JNIEXPORT void JNICALL IBSCAN_BUILD_JNI_FNCT(openDeviceAsyncExNative)(
    JNIEnv  *pEnv,
	jobject  tthis,
	jint     deviceIndex,
	jstring  uniformityMaskPath,
	jobject  error);

/*
 * private native int getInitProgressNative(int deviceIndex, NativeError error);
 */
JNIEXPORT jint JNICALL IBSCAN_BUILD_JNI_FNCT(getInitProgressNative)(
    JNIEnv  *pEnv,
	jobject  tthis,
	jint     deviceIndex,
	jobject  error);

/*
 * private native int unloadLibraryNative(NativeError error);
 */
JNIEXPORT void JNICALL IBSCAN_BUILD_JNI_FNCT(unloadLibraryNative)(
    JNIEnv  *pEnv,
	jobject  tthis,
	jobject  error);

/*
 * private native void isWritableDirectory(String dirpath, boolean needCreateSubFolder, NativeError error);
 */
JNIEXPORT void JNICALL IBSCAN_BUILD_JNI_FNCT(isWritableDirectoryNative)(
    JNIEnv  *pEnv,
	jobject  tthis,
	jstring  dirpath,
	jboolean needCreateSubFolder,
	jobject  error);

/*
 * private native String getRequiredSDKVersionNative(int deviceIndex, NativeError error);
 */
JNIEXPORT jstring JNICALL IBSCAN_BUILD_JNI_FNCT(getRequiredSDKVersionNative)(
	JNIEnv  *pEnv,
	jobject  tthis,
	jint     deviceIndex,
	jobject  error);

/*
 * private native void setCustomerKeyNative(int deviceIndex, int hashType, String customerKey, IBScan.NativeError error);
 */
JNIEXPORT void JNICALL IBSCAN_BUILD_JNI_FNCT(setCustomerKeyNative)(
    JNIEnv  *pEnv,
    jobject  tthis,
	jint     deviceIndex,
	jint     hashType,
	jstring  customerKey,
	jobject  error);

/*
 * private native void getErrorStringNative(int errorCode, IBScan.NativeError error);
 */
JNIEXPORT jstring JNICALL IBSCAN_BUILD_JNI_FNCT(getErrorStringNative)
    (JNIEnv  *pEnv,
	 jobject  tthis,
	 jint     errorCode,
	 jobject  error);

#ifdef __cplusplus
} //extern "C" {
#endif 

#endif /* IBSCAN_H_ */
