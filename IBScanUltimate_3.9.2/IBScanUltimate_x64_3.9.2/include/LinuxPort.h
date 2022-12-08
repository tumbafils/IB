/*
****************************************************************************************************
* LinuxPort.h
*
* DESCRIPTION:
*     Types and constants for IBScanUltimate Linux port.
*     http://www.integratedbiometrics.com
*
* NOTES:
*     Copyright (c) Integrated Biometrics, 2009-2013
*
* HISTORY:
*     2012/04/06  1.0.0  Created.
*     2013/08/03  1.6.9  Reformatted.
*     2014/07/23  1.8.0  Removed typedef (struct _GUID)
*     2015/03/04  1.8.3  Added typedef keyword to support UNICODE for WinCE
****************************************************************************************************
*/

#ifndef __LINUX_PORT_H__
#define __LINUX_PORT_H__

#include <limits.h>
#include <inttypes.h>
#include <pthread.h>

#define Sleep(x) usleep(x*1000)
#define AFX_MANAGE_STATE(x)
#define CALLBACK
#define WINAPI
#define DECLSPEC_SELECTANY

typedef unsigned char   UCHAR;
typedef unsigned char   BYTE;
typedef unsigned short  USHORT;
typedef unsigned int    UINT;
typedef int             LONG;
typedef unsigned int    ULONG;
typedef UCHAR          *PUCHAR;
typedef unsigned int    DWORD;
typedef unsigned short  WORD;
typedef UCHAR           TCHAR;
typedef DWORD           HANDLE;
typedef int             BOOL;

typedef char           *LPSTR;
typedef char           *LPCSTR;
typedef wchar_t        *LPWSTR;
typedef wchar_t        *LPCWSTR;
typedef wchar_t         WCHAR;

#define VOID void

typedef struct _GUID {
    DWORD  Data1;
    USHORT Data2;
    USHORT Data3;
    BYTE   Data4[ 8 ];
} GUID;

#define EXTERN_C extern "C"
typedef GUID                 *LPGUID;
typedef DWORD                *LPDWORD;
typedef void                 *LPVOID;
typedef void                 *PVOID;
typedef void                 *LPCVOID;

typedef uint64_t              ULONG_PTR;
typedef PVOID                 HDEVINFO;

// Fixup type later
#define OVERLAPPED HANDLE
typedef DWORD        (WINAPI *PTHREAD_START_ROUTINE)(LPVOID lpThreadParameter);
typedef PTHREAD_START_ROUTINE LPTHREAD_START_ROUTINE;
typedef int                   WPARAM;
typedef int                   LPARAM;
typedef HANDLE                HWND;
typedef int                   LRESULT;

//
// Device interface information structure (references a device
// interface that is associated with the device information
// element that owns it).
//
typedef struct _SP_DEVICE_INTERFACE_DATA {
    DWORD cbSize;
    GUID  InterfaceClassGuid;
    DWORD Flags;
    ULONG_PTR Reserved;
} SP_DEVICE_INTERFACE_DATA, *PSP_DEVICE_INTERFACE_DATA;

typedef PSP_DEVICE_INTERFACE_DATA PSP_INTERFACE_DEVICE_DATA;

#define MAX_PATH PATH_MAX

#define DEFINE_GUID(name, l, w1, w2, b1, b2, b3, b4, b5, b6, b7, b8) \
        EXTERN_C const GUID DECLSPEC_SELECTANY name \
                = { l, w1, w2, { b1, b2,  b3,  b4,  b5,  b6,  b7,  b8 } }

#define INVALID_HANDLE_VALUE 0xFFFFFFFF
#define TRUE  1
#define FALSE 0
#ifndef NULL
#define NULL  0
#endif


#endif  // __LINUX_PORT_H__
