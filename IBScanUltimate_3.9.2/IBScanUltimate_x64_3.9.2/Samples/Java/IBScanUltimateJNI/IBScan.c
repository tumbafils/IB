/* *************************************************************************************************
 * IBScan.c
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
 *     2013/03/08  Changed name of LOG macro.
 *     2013/04/06  Add function to enable/disable trace log.
 *     2017/11/08  Add function isWritableDirectory() to check whether a directrly is writable
 *     2018/11/19  Add function getRequiredSDKVersion()
 *     2020/09/21  Add function setCustomerKey(), getErrorString()
 ************************************************************************************************ */

#include <jni.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include "IBScan.h"

#ifndef _WINDOWS
#include "LinuxPort.h"
#else
#include <Windows.h>
#endif

#include "IBScanUltimateApi.h"

#ifdef __android__
#include <android/log.h>
#endif

/***************************************************************************************************
 * LOCAL MACROS
 **************************************************************************************************/

#define DEBUG       0
#define MODULE_NAME "ibscan"

#if DEBUG
	#ifdef __android__
		#define ANDROID_LOG(...) __android_log_print(ANDROID_LOG_INFO, MODULE_NAME, __VA_ARGS__)
		#define LOG(s) { ANDROID_LOG s; }
	#else
		#define LOG(s) { printf(MODULE_NAME ": %s"); printf s; fflush(stdout); }
	#endif
#else
	#define LOG(s)
#endif

#define USE_PARAM(p) (void)p

#define IBSCAN_JAVA_CLASS_PATH       "com/integratedbiometrics/ibscanultimate/IBScan"
#define IBSCANDEVICE_JAVA_CLASS_PATH "com/integratedbiometrics/ibscanultimate/IBScanDevice"
#define STRING_CLASS_PATH            "java/lang/String"

/***************************************************************************************************
 * LOCAL VARIABLES
 **************************************************************************************************/

static JavaVM   *SavedJavaVM                                    = NULL;

static jclass    Class_IBScan                                   = NULL;
static jmethodID MethodID_IBScan_callbackScanDeviceCountChanged = NULL;
static jmethodID MethodID_IBScan_callbackScanDeviceInitProgress = NULL;
static jmethodID MethodID_IBScan_callbackScanDeviceOpenComplete = NULL;
static jclass    Class_IBScan_DeviceDesc                        = NULL;
static jmethodID MethodID_IBScan_DeviceDesc_DeviceDesc          = NULL;
static jclass    Class_IBScan_SdkVersion                        = NULL;
static jmethodID MethodID_IBScan_SdkVersion_SdkVersion          = NULL;
static jclass    Class_IBScan_NativeError                       = NULL;
static jfieldID  FieldID_IBScan_NativeError_code                = NULL;
static jclass    Class_IBScanDevice                             = NULL;
static jmethodID MethodID_IBScanDevice_IBScanDevice             = NULL;

/***************************************************************************************************
 * LOCAL FUNCTION PROTOTYPES
 **************************************************************************************************/

static jclass    findClass        (JNIEnv *pEnv, const char *name, BOOL *pOk);
static jfieldID  getFieldID       (JNIEnv *pEnv, jclass cclass, const char *name, const char *sig, BOOL *pOk);
static jmethodID getMethodID      (JNIEnv *pEnv, jclass cclass, const char *name, const char *sig, BOOL *pOk);
static jmethodID getStaticMethodID(JNIEnv *pEnv, jclass cclass, const char *name, const char *sig, BOOL *pOk);
static void      setNativeError   (JNIEnv *pEnv, jobject obj, int code);
static jint      attachToVM      (void **env, BOOL *pAttached);
static void      detachFromVM    (BOOL attached);

static void CALLBACK callbackScanDeviceCountChanged(const int detectedDevices, void *pContext);
static void CALLBACK callbackScanDeviceInitProgress(const int deviceIndex, void *pContext, const int progressValue);
static void CALLBACK callbackScanDeviceOpenComplete(const int deviceIndex, void *pContext, const int deviceHandle,
    const int errorCode);

/***************************************************************************************************
 * EXTERNAL FUNCTION PROTOTYPES
 **************************************************************************************************/

extern jboolean IBScanDevice_OnLoad(JavaVM *vm, void *reserved);
extern void     IBScanDevice_Open  (JNIEnv *pEnv, long devHandle, jobject devHandleJ);

/***************************************************************************************************
 * GLOBAL FUNCTIONS
 **************************************************************************************************/

/*
 * Handle load of library.
 */
jboolean IBScan_OnLoad(
    JavaVM *vm,
    void   *reserved)
{
    JNIEnv *pEnv;
    jint    res;
    BOOL    ok = TRUE;

    USE_PARAM(reserved);

    LOG(("%s\n", __FUNCTION__));

    res = (*vm)->GetEnv(vm, (void **)&pEnv, JNI_VERSION_1_2);
    if (res < 0)
    {
    	LOG(("unable to get JNIEnv reference\n"));
        ok = FALSE;
    }
    else
    {
        /* Cache classes, field IDs, and method IDs. */
        Class_IBScan = findClass(pEnv, IBSCAN_JAVA_CLASS_PATH, &ok);
        if (Class_IBScan != NULL)
        {
            MethodID_IBScan_callbackScanDeviceCountChanged = getStaticMethodID(pEnv, Class_IBScan, "callbackScanDeviceCountChanged", "(I)V",   &ok);
            MethodID_IBScan_callbackScanDeviceInitProgress = getStaticMethodID(pEnv, Class_IBScan, "callbackScanDeviceInitProgress", "(II)V", &ok);
            MethodID_IBScan_callbackScanDeviceOpenComplete = getStaticMethodID(pEnv, Class_IBScan, "callbackScanDeviceOpenComplete", "(IL" IBSCANDEVICE_JAVA_CLASS_PATH ";I)V",  &ok);
        }
        Class_IBScan_DeviceDesc = findClass(pEnv, IBSCAN_JAVA_CLASS_PATH "$DeviceDesc", &ok);
        if (Class_IBScan_DeviceDesc != NULL)
        {
			MethodID_IBScan_DeviceDesc_DeviceDesc = getMethodID(pEnv, Class_IBScan_DeviceDesc, "<init>", "(L" STRING_CLASS_PATH ";L" STRING_CLASS_PATH ";L" STRING_CLASS_PATH ";L" STRING_CLASS_PATH ";L" STRING_CLASS_PATH ";ZZL" STRING_CLASS_PATH ";)V", &ok);

        }
        Class_IBScan_SdkVersion = findClass(pEnv, IBSCAN_JAVA_CLASS_PATH "$SdkVersion", &ok);
        if (Class_IBScan_SdkVersion != NULL)
        {
            MethodID_IBScan_SdkVersion_SdkVersion = getMethodID(pEnv, Class_IBScan_SdkVersion, "<init>", "(L" STRING_CLASS_PATH ";L" STRING_CLASS_PATH ";)V", &ok);
        }
        Class_IBScan_NativeError = findClass(pEnv, IBSCAN_JAVA_CLASS_PATH "$NativeError", &ok);
        if (Class_IBScan_NativeError != NULL)
        {
            FieldID_IBScan_NativeError_code = getFieldID(pEnv, Class_IBScan_NativeError, "code", "I", &ok);
        }
        Class_IBScanDevice = findClass(pEnv, IBSCANDEVICE_JAVA_CLASS_PATH, &ok);
        if (Class_IBScanDevice != NULL)
        {
            MethodID_IBScanDevice_IBScanDevice = getMethodID(pEnv, Class_IBScanDevice, "<init>", "(J)V", &ok);
        }
    }

    /* Save pointer to VM for use in callbacks. */
    SavedJavaVM = vm;

    /* Indicate whether initialization was successful. */
    return (ok);
}

/*
 * Handle load of library.
 */
JNIEXPORT jint JNICALL JNI_OnLoad(
    JavaVM *vm,
    void   *reserved)
{
	LOG(("%s\n", __FUNCTION__));

	IBScan_OnLoad(vm, reserved);
    IBScanDevice_OnLoad(vm, reserved);

    return (JNI_VERSION_1_2);
}

/***************************************************************************************************
 * JNI FUNCTIONS
 **************************************************************************************************/

/*
 * private native void initNative();
 */
JNIEXPORT void JNICALL IBSCAN_BUILD_JNI_FNCT(initNative)(
    JNIEnv  *pEnv,
    jobject  tthis)
{
    int nRc;

    USE_PARAM(pEnv);
    USE_PARAM(tthis);

    LOG(("%s\n", __FUNCTION__));

	/* 
      * Register callbacks.  None of these need a context; the function is provided as a dummy fourth
      * argument to circumvent the return error in the libary.
      */
    nRc = IBSU_RegisterCallbacks(0, ENUM_IBSU_ESSENTIAL_EVENT_DEVICE_COUNT,      (void *)callbackScanDeviceCountChanged, (void *)callbackScanDeviceCountChanged);
    if (nRc < IBSU_STATUS_OK)
    {
    	LOG(("unable to register DEVICE_COUNT callback with error code %d\n", nRc));
    }
    nRc = IBSU_RegisterCallbacks(0, ENUM_IBSU_ESSENTIAL_EVENT_INIT_PROGRESS,     (void *)callbackScanDeviceInitProgress, (void *)callbackScanDeviceInitProgress);
    if (nRc < IBSU_STATUS_OK)
    {
    	LOG(("unable to register INIT_PROGRESS callback with error code %d\n", nRc));
    }
    nRc = IBSU_RegisterCallbacks(0, ENUM_IBSU_ESSENTIAL_EVENT_ASYNC_OPEN_DEVICE, (void *)callbackScanDeviceOpenComplete, (void *)callbackScanDeviceOpenComplete);
    if (nRc < IBSU_STATUS_OK)
    {
    	LOG(("unable to register ASYNC_OPEN_DEVICE callback with error code %d\n", nRc));
    }
}

/*
 * private native void enableTraceLog(IBScan.NativeError error);
 */
JNIEXPORT void JNICALL IBSCAN_BUILD_JNI_FNCT(enableTraceLogNative)(
    JNIEnv  *pEnv,
    jobject  tthis,
    jboolean on,
    jobject  error)
{
    int nRc;
    
    LOG(("%s\n", __FUNCTION__));
    
    nRc = IBSU_EnableTraceLog(on);
    setNativeError(pEnv, error, nRc);
}

/*
 * private native int getDeviceCountNative(IBScan.NativeError error);
 */
JNIEXPORT jint JNICALL IBSCAN_BUILD_JNI_FNCT(getDeviceCountNative)(
    JNIEnv  *pEnv,
	jobject  tthis,
	jobject  error)
{
    int devices = 0;
    int nRc;

    USE_PARAM(tthis);

    LOG(("%s\n", __FUNCTION__));

    nRc = IBSU_GetDeviceCount(&devices);
    setNativeError(pEnv, error, nRc);

    return (devices);
}

/*
 * private native IBScan.SdkVersion getSdkVersionNative(IBScan.NativeError error);
 */
JNIEXPORT jobject JNICALL IBSCAN_BUILD_JNI_FNCT(getSdkVersionNative)(
    JNIEnv  *pEnv,
	jobject  tthis,
	jobject  error)
{
    IBSU_SdkVersion verInfo;
    int             nRc;
    jobject         verInfoJ = NULL;

    USE_PARAM(tthis);

    LOG(("%s\n", __FUNCTION__));

    memset(&verInfo, 0, sizeof(verInfo));
    nRc = IBSU_GetSDKVersion(&verInfo);
    setNativeError(pEnv, error, nRc);

    if (nRc >= IBSU_STATUS_OK)
    {
        jstring product;

        product = (*pEnv)->NewStringUTF(pEnv, verInfo.Product);
        if (product == NULL)
        {
            setNativeError(pEnv, error, IBSU_ERR_MEM_ALLOC);
            LOG(("%s: unable to allocate string\n", __FUNCTION__));
        }
        else
        {
            jstring file;

            file = (*pEnv)->NewStringUTF(pEnv, verInfo.File);
            if (file == NULL)
            {
                setNativeError(pEnv, error, IBSU_ERR_MEM_ALLOC);
                LOG(("%s: unable to allocate string\n", __FUNCTION__));
            }
            else
            {
                verInfoJ = (*pEnv)->NewObject(pEnv, Class_IBScan_SdkVersion, MethodID_IBScan_SdkVersion_SdkVersion, product, file);
                if (verInfoJ == NULL)
                {
                    setNativeError(pEnv, error, IBSU_ERR_MEM_ALLOC);
                    LOG(("%s: unable to allocate SdkVersion object\n", __FUNCTION__));
                }
            }
        }
    }

	return (verInfoJ);
}

/*
 * private native IBScan.DeviceDesc getDeviceDescNative(int deviceIndex, IBScan.NativeError error);
 */
JNIEXPORT jobject JNICALL IBSCAN_BUILD_JNI_FNCT(getDeviceDescNative)(
    JNIEnv  *pEnv,
	jobject  tthis,
	jint     deviceIndex,
	jobject  error)
{
    jobject         devDescJ = NULL;
    IBSU_DeviceDesc devDesc;
    int             nRc;

    USE_PARAM(tthis);

    LOG(("%s\n", __FUNCTION__));

    memset(&devDesc, 0, sizeof(devDesc));
    nRc = IBSU_GetDeviceDescription(deviceIndex, &devDesc);
    setNativeError(pEnv, error, nRc);

    if (nRc >= IBSU_STATUS_OK)
    {
        jstring serialNumber;

        serialNumber = (*pEnv)->NewStringUTF(pEnv, devDesc.serialNumber);
        if (serialNumber == NULL)
        {
            setNativeError(pEnv, error, IBSU_ERR_MEM_ALLOC);
            LOG(("%s: unable to allocate string\n", __FUNCTION__));
        }
        else
        {
            jstring productName;

            productName = (*pEnv)->NewStringUTF(pEnv, devDesc.productName);
            if (productName == NULL)
            {
                setNativeError(pEnv, error, IBSU_ERR_MEM_ALLOC);
                LOG(("%s: unable to allocate string\n", __FUNCTION__));
            }
            else
            {
                jstring interfaceType;

                interfaceType = (*pEnv)->NewStringUTF(pEnv, devDesc.interfaceType);
                if (interfaceType == NULL)
                {
                    setNativeError(pEnv, error, IBSU_ERR_MEM_ALLOC);
                    LOG(("%s: unable to allocate string\n", __FUNCTION__));
                }
                else
                {
                    jstring fwVersion;

                    fwVersion = (*pEnv)->NewStringUTF(pEnv, devDesc.fwVersion);
                    if (fwVersion == NULL)
                    {
                        setNativeError(pEnv, error, IBSU_ERR_MEM_ALLOC);
                        LOG(("%s: unable to allocate string\n", __FUNCTION__));
                    }
                    else
                    {
						jstring devRevision;

                        devRevision = (*pEnv)->NewStringUTF(pEnv, devDesc.devRevision);
                        if (devRevision == NULL)
                        {
                            setNativeError(pEnv, error, IBSU_ERR_MEM_ALLOC);
                            LOG(("%s: unable to allocate string\n", __FUNCTION__));
                        }
						else 
						{
							jstring customerStr;

							customerStr = (*pEnv)->NewStringUTF(pEnv, devDesc.customerString);
							if (customerStr == NULL)
							{
								setNativeError(pEnv, error, IBSU_ERR_MEM_ALLOC);
								LOG(("%s: unable to allocate string\n", __FUNCTION__));
							}
							else
							{
								BOOL isHandleOpened;
								BOOL IsDeviceLocked;

								isHandleOpened = devDesc.IsHandleOpened;
								IsDeviceLocked = devDesc.IsDeviceLocked;

								devDescJ = (*pEnv)->NewObject(pEnv, Class_IBScan_DeviceDesc, MethodID_IBScan_DeviceDesc_DeviceDesc,
												serialNumber, productName, interfaceType, fwVersion, devRevision, isHandleOpened, IsDeviceLocked, customerStr);
								if (devDescJ == NULL)
								{
									setNativeError(pEnv, error, IBSU_ERR_MEM_ALLOC);
									LOG(("%s: unable to allocate DeviceDesc object\n", __FUNCTION__));
								}
							}
						}
                    }
                }
            }
        }
    }

    return (devDescJ);
}

/*
 * private native IBScanDevice openDeviceNative(int deviceIndex, IBScan.NativeError error);
 */
JNIEXPORT jobject JNICALL IBSCAN_BUILD_JNI_FNCT(openDeviceNative)(
    JNIEnv  *pEnv,
	jobject  tthis,
	jint     deviceIndex,
	jobject  error)
{
    jobject devHandleJ = NULL;
    int     devHandle = -1;
    int     nRc;

    USE_PARAM(tthis);

    LOG(("%s\n", __FUNCTION__));

    nRc = IBSU_OpenDevice(deviceIndex, &devHandle);
    setNativeError(pEnv, error, nRc);

    if (nRc >= IBSU_STATUS_OK)
    {
        devHandleJ = (*pEnv)->NewObject(pEnv, Class_IBScanDevice, MethodID_IBScanDevice_IBScanDevice, (jlong)devHandle);
        if (devHandleJ == NULL)
        {
            setNativeError(pEnv, error, IBSU_ERR_MEM_ALLOC);
            LOG(("%s: unable to allocate IBScanDevice object\n", __FUNCTION__));
        }
        else
        {
            /* Perform additional steps to open device. */
            IBScanDevice_Open(pEnv, devHandle, devHandleJ);
        }
    }

	return (devHandleJ);
}

/*
 * private native IBScanDevice openDeviceExNative(int deviceIndex, String uniformityMaskPath,
 *     IBScan.NativeError error);
 */
JNIEXPORT jobject JNICALL IBSCAN_BUILD_JNI_FNCT(openDeviceExNative)(
    JNIEnv  *pEnv,
	jobject  tthis,
	jint     deviceIndex,
	jstring  uniformityMaskPath,
	jobject  error)
{
    jobject     devHandleJ = NULL;
    int         devHandle = -1;
    const char *uniformityMaskPathC;
    int         nRc;

    USE_PARAM(tthis);

    LOG(("%s\n", __FUNCTION__));

    uniformityMaskPathC = (*pEnv)->GetStringUTFChars(pEnv, uniformityMaskPath, NULL);
    if (uniformityMaskPathC == NULL)
    {
        setNativeError(pEnv, error, IBSU_ERR_MEM_ALLOC);
        LOG(("%s: unable to get characters from string\n", __FUNCTION__));
    }
    else
    {
        nRc = IBSU_OpenDeviceEx(deviceIndex, (char *)uniformityMaskPathC, FALSE, &devHandle);
        setNativeError(pEnv, error, nRc);

        if (nRc >= IBSU_STATUS_OK)
        {
            devHandleJ = (*pEnv)->NewObject(pEnv, Class_IBScanDevice, MethodID_IBScanDevice_IBScanDevice, (jlong)devHandle);
            if (devHandleJ == NULL)
            {
                setNativeError(pEnv, error, IBSU_ERR_MEM_ALLOC);
                LOG(("%s: unable to allocate IBScanDevice object\n", __FUNCTION__));
            }
            else
            {
                /* Perform additional steps to open device. */
                IBScanDevice_Open(pEnv, devHandle, devHandleJ);
            }
        }

        (*pEnv)->ReleaseStringUTFChars(pEnv, uniformityMaskPath, uniformityMaskPathC);
    }

	return (devHandleJ);
}

/*
 * private native void openDeviceAsyncNative(int deviceIndex, IBScan.NativeError error);
 */
JNIEXPORT void JNICALL IBSCAN_BUILD_JNI_FNCT(openDeviceAsyncNative)(
    JNIEnv  *pEnv,
	jobject  tthis,
	jint     deviceIndex,
	jobject  error)
{
    int nRc;

    USE_PARAM(tthis);

    LOG(("%s\n", __FUNCTION__));

    nRc = IBSU_AsyncOpenDevice(deviceIndex);
    setNativeError(pEnv, error, nRc);
}

/*
 * private native void openDeviceAsyncExNative(int deviceIndex, String uniformityMaskPath,
 *     IBScan.NativeError error);
 */
JNIEXPORT void JNICALL IBSCAN_BUILD_JNI_FNCT(openDeviceAsyncExNative)(
    JNIEnv  *pEnv,
	jobject  tthis,
	jint     deviceIndex,
	jstring  uniformityMaskPath,
	jobject  error)
{
    int         devHandle = -1;
    const char *uniformityMaskPathC;
    int         nRc;

    USE_PARAM(tthis);

    LOG(("%s\n", __FUNCTION__));

    uniformityMaskPathC = (*pEnv)->GetStringUTFChars(pEnv, uniformityMaskPath, NULL);
    if (uniformityMaskPathC == NULL)
    {
        setNativeError(pEnv, error, IBSU_ERR_MEM_ALLOC);
        LOG(("%s: unable to get characters from string\n", __FUNCTION__));
    }
    else
    {
        nRc = IBSU_OpenDeviceEx(deviceIndex, (char *)uniformityMaskPathC, TRUE, &devHandle);
        setNativeError(pEnv, error, nRc);

        (*pEnv)->ReleaseStringUTFChars(pEnv, uniformityMaskPath, uniformityMaskPathC);
    }
}

/*
 * private native int getInitProgressNative(int deviceIndex, NativeError error);
 */
JNIEXPORT jint JNICALL IBSCAN_BUILD_JNI_FNCT(getInitProgressNative)(
    JNIEnv  *pEnv,
	jobject  tthis,
	jint     deviceIndex,
	jobject  error)
{
    int  nRc;
    BOOL isComplete = FALSE;
    int  deviceHandle = -1;
    int  progressValue = 0;

    USE_PARAM(tthis);

    LOG(("%s\n", __FUNCTION__));

    nRc = IBSU_BGetInitProgress(deviceIndex, &isComplete, &deviceHandle, &progressValue);
    setNativeError(pEnv, error, nRc);

	return (progressValue);
}

/*
 * private native int unloadLibraryNative(NativeError error);
 */
JNIEXPORT void JNICALL IBSCAN_BUILD_JNI_FNCT(unloadLibraryNative)(
    JNIEnv  *pEnv,
	jobject  tthis,
	jobject  error)
{
    int  nRc;

    USE_PARAM(tthis);

    LOG(("%s\n", __FUNCTION__));

    nRc = IBSU_UnloadLibrary();
    setNativeError(pEnv, error, nRc);
}

/*
 * private native void isWritableDirectory(String dirpath, boolean needCreateSubFolder, NativeError error);
 */
JNIEXPORT void JNICALL IBSCAN_BUILD_JNI_FNCT(isWritableDirectoryNative)(
    JNIEnv  *pEnv,
	jobject  tthis,
	jstring  dirpath,
	jboolean needCreateSubFolder,
	jobject  error)
{
    const char *dirpathC;
    int  nRc;

    USE_PARAM(tthis);

    LOG(("%s\n", __FUNCTION__));

    dirpathC = (*pEnv)->GetStringUTFChars(pEnv, dirpath, NULL);
    if (dirpathC == NULL)
    {
        setNativeError(pEnv, error, IBSU_ERR_MEM_ALLOC);
        LOG(("%s: unable to get characters from string\n", __FUNCTION__));
    }
    else
    {
	    nRc = IBSU_IsWritableDirectory((char *)dirpathC, needCreateSubFolder);
	    setNativeError(pEnv, error, nRc);

        (*pEnv)->ReleaseStringUTFChars(pEnv, dirpath, dirpathC);
    }
}

/*
 * private native String getRequiredSDKVersionNative(int deviceIndex, NativeError error);
 */
JNIEXPORT jstring JNICALL IBSCAN_BUILD_JNI_FNCT(getRequiredSDKVersionNative)
	(JNIEnv  *pEnv,
	 jobject  tthis,
	 jint     deviceIndex,
	 jobject  error)
{
    jstring minSDKVersionJ = NULL;
    char    minSDKVersion[IBSU_MAX_STR_LEN];
    int     nRc;

    LOG(("%s\n", __FUNCTION__));

    memset(&minSDKVersion[0], 0, sizeof(minSDKVersion));
    nRc       = IBSU_GetRequiredSDKVersion(deviceIndex, minSDKVersion);
    setNativeError(pEnv, error, nRc);
    if (nRc >= IBSU_STATUS_OK)
    {
        minSDKVersionJ = (*pEnv)->NewStringUTF(pEnv, minSDKVersion);
        if (minSDKVersionJ == NULL)
        {
            setNativeError(pEnv, error, IBSU_ERR_MEM_ALLOC);
            LOG(("%s: unable to allocate string\n", __FUNCTION__));
        }
    }

	return (minSDKVersionJ);
}

/*
 * private native void setCustomerKeyNative(int deviceIndex, int hashType, String customerKey, IBScan.NativeError error);
 */
JNIEXPORT void JNICALL IBSCAN_BUILD_JNI_FNCT(setCustomerKeyNative)
    (JNIEnv  *pEnv,
	 jobject  tthis,
	 jint     deviceIndex,
	 jint     hashType,
	 jstring  customerKey,
	 jobject  error)
{
    const char *customerKeyC;
    int  nRc;

    USE_PARAM(tthis);

    LOG(("%s\n", __FUNCTION__));

    customerKeyC = (*pEnv)->GetStringUTFChars(pEnv, customerKey, NULL);
    if (customerKeyC == NULL)
    {
        setNativeError(pEnv, error, IBSU_ERR_MEM_ALLOC);
        LOG(("%s: unable to get characters from string\n", __FUNCTION__));
    }
    else
    {
	    nRc = IBSU_SetCustomerKey(deviceIndex, hashType, (char *)customerKeyC);
	    setNativeError(pEnv, error, nRc);

        (*pEnv)->ReleaseStringUTFChars(pEnv, customerKey, customerKeyC);
    }
}

/*
 * private native void getErrorStringNative(int errorCode, IBScan.NativeError error);
 */
JNIEXPORT jstring JNICALL IBSCAN_BUILD_JNI_FNCT(getErrorStringNative)
    (JNIEnv  *pEnv,
	 jobject  tthis,
	 jint     errorCode,
	 jobject  error)
{
    int  nRc;
	jstring propertyValueJ = NULL;
    char    propertyValue[IBSU_MAX_STR_LEN];

    USE_PARAM(tthis);

    LOG(("%s\n", __FUNCTION__));

    nRc       = IBSU_GetErrorString(errorCode, propertyValue);
    setNativeError(pEnv, error, nRc);
    if (nRc >= IBSU_STATUS_OK)
    {
        propertyValueJ = (*pEnv)->NewStringUTF(pEnv, propertyValue);
        if (propertyValueJ == NULL)
        {
            setNativeError(pEnv, error, IBSU_ERR_MEM_ALLOC);
            LOG(("%s: unable to allocate string\n", __FUNCTION__));
        }
    }

	return (propertyValueJ);
}


/***************************************************************************************************
 * LOCAL FUNCTIONS (CALLBACKS)
 **************************************************************************************************/

/*
 * Device count change notification.
 */
static void CALLBACK callbackScanDeviceCountChanged(
    const int  detectedDevices,
    void      *pContext)
{
    JNIEnv *pEnv = NULL;
    jint    rc;
	BOOL    attached = FALSE;

	USE_PARAM(pContext);

    LOG(("%s (detectedDevices=%d)\n", __FUNCTION__, detectedDevices));

    /* Attach thread to VM, if necessary. */
    rc = attachToVM((void **)&pEnv, &attached);
    if (rc == 0)
    {
        (*pEnv)->CallStaticVoidMethod(pEnv, Class_IBScan, MethodID_IBScan_callbackScanDeviceCountChanged, detectedDevices);
		detachFromVM(attached);
    }
}

/*
 * Device initialization progress notification.
 */
static void CALLBACK callbackScanDeviceInitProgress(
    const int  deviceIndex,
    void      *pContext,
    const int  progressValue)
{
    JNIEnv *pEnv = NULL;
    jint    rc;
    BOOL    attached = FALSE;

    USE_PARAM(pContext);

    LOG(("%s (deviceIndex=%d,progressValue=%d)\n", __FUNCTION__, deviceIndex, progressValue));

    /* Attach thread to VM, if necessary. */
    rc = attachToVM((void **)&pEnv, &attached);
    if (rc == 0)
    {
        (*pEnv)->CallStaticVoidMethod(pEnv, Class_IBScan, MethodID_IBScan_callbackScanDeviceInitProgress, deviceIndex, progressValue);
		detachFromVM(attached);
    }
}

/*
 * Asynchonous initialize device notification.
 */
static void CALLBACK callbackScanDeviceOpenComplete(
    const int  deviceIndex,
    void      *pContext,
    const int  deviceHandle,
    const int  errorCode)
{
    JNIEnv *pEnv = NULL;
    jint    rc;
	BOOL    attached = FALSE;

	USE_PARAM(pContext);

    LOG(("%s\n", __FUNCTION__));

    /* Attach thread to VM, if necessary. */
    rc = attachToVM((void **)&pEnv, &attached);
    if (rc == 0)
    {
        jobject devHandleJ     = NULL;
        int     errorCodeLocal = errorCode;

        if (errorCode >= IBSU_STATUS_OK)
        {
            devHandleJ = (*pEnv)->NewObject(pEnv, Class_IBScanDevice, MethodID_IBScanDevice_IBScanDevice, (jlong)deviceHandle);
            if (devHandleJ == NULL)
            {
                errorCodeLocal = IBSU_ERR_MEM_ALLOC;
                LOG(("%s: unable to allocate IBScanDevice object\n", __FUNCTION__));
            }
            else
            {
                /* Perform additional steps to open device. */
                IBScanDevice_Open(pEnv, deviceHandle, devHandleJ);
            }
        }

        (*pEnv)->CallStaticVoidMethod(pEnv, Class_IBScan, MethodID_IBScan_callbackScanDeviceOpenComplete, deviceIndex, devHandleJ, errorCodeLocal);
		detachFromVM(attached);
    }
}

/***************************************************************************************************
 * LOCAL FUNCTIONS
 **************************************************************************************************/

/*
 * Find a class and log result.
 */
static jclass findClass(
    JNIEnv     *pEnv,
    const char *name,
    BOOL       *pOk)
{
    jclass cclass = NULL;

    if (*pOk == TRUE)
    {
		cclass = (*pEnv)->FindClass(pEnv, name);
		if (cclass == NULL)
		{
			LOG(("unable to get reference to \"%s\" class\n", name));
			*pOk = FALSE;
		}
		else
		{
			LOG(("got reference to \"%s\" class\n", name));
			cclass = (*pEnv)->NewGlobalRef(pEnv, cclass);
		}
    }
    return (cclass);
}

/*
 * Get a field ID and log result.
 */
static jfieldID getFieldID(
    JNIEnv     *pEnv,
    jclass      cclass,
    const char *name,
    const char *sig,
    BOOL       *pOk)
{
    jfieldID fieldID = NULL;

    if (*pOk == TRUE)
    {
		fieldID = (*pEnv)->GetFieldID(pEnv, cclass, name, sig);
		if (fieldID == NULL)
		{
			LOG(("unable to get reference to \"%s\" field with signature \"%s\"\n", name, sig));
			*pOk = FALSE;
		}
		else
		{
			LOG(("got reference to \"%s\" field with signature \"%s\"\n", name, sig));
		}
    }
    return (fieldID);
}

/*
 * Get a method ID and log result.
 */
static jmethodID getMethodID(
    JNIEnv     *pEnv,
    jclass      cclass,
    const char *name,
    const char *sig,
    BOOL       *pOk)
{
    jmethodID methodID = NULL;

    if (*pOk == TRUE)
    {
		methodID = (*pEnv)->GetMethodID(pEnv, cclass, name, sig);
		if (methodID == NULL)
		{
			LOG(("unable to get reference to \"%s\" method with signature \"%s\"\n", name, sig));
			*pOk = FALSE;
		}
		else
		{
			LOG(("got reference to \"%s\" method with signature \"%s\"\n", name, sig));
		}
    }
    return (methodID);
}

/*
 * Get a static method ID and log result.
 */
static jmethodID getStaticMethodID(
    JNIEnv     *pEnv,
    jclass      cclass,
    const char *name,
    const char *sig,
    BOOL       *pOk)
{
    jmethodID methodID = NULL;

    if (*pOk == TRUE)
    {
		methodID = (*pEnv)->GetStaticMethodID(pEnv, cclass, name, sig);
		if (methodID == NULL)
		{
			LOG(("unable to get reference to static \"%s\" method with signature \"%s\"\n", name, sig));
			*pOk = FALSE;
		}
		else
		{
			LOG(("got reference to static \"%s\" method with signature \"%s\"\n", name, sig));
		}
    }
    return (methodID);
}

/*
 * Set native error.
 */
static void setNativeError(
    JNIEnv  *pEnv,
    jobject  obj,
    int      code)
{
    (*pEnv)->SetIntField(pEnv, obj, FieldID_IBScan_NativeError_code, code);
}

/*
 * Attach thread from VM.
 */
static jint attachToVM(void **env, BOOL *pAttached)
{
	jint rc;

    /* Attach thread to VM, if necessary. */
	rc = (*SavedJavaVM)->GetEnv(SavedJavaVM, env, JNI_VERSION_1_2);
	if (rc == 0)
	{
		*pAttached = TRUE;
	}
	else
	{
	    rc = (*SavedJavaVM)->AttachCurrentThread(SavedJavaVM, env, NULL);
		*pAttached = FALSE;

		if (rc < 0)
		{
			LOG(("failed to attach thread to VM\n"));
		}
	}

	return (rc);
}

/*
 * Detach thread from VM.
 */
static void detachFromVM(BOOL attached)
{
	if (attached)
	{
		(*SavedJavaVM)->DetachCurrentThread(SavedJavaVM);
	}
}
