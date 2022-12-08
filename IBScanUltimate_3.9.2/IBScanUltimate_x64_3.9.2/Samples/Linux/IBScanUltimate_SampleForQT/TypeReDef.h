#ifndef TYPEREDEF_H
#define TYPEREDEF_H

#if defined(__linux__)
#undef __linux__
#endif

#define CALLBACK
#define WINAPI

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

#define VOID void

typedef DWORD                *LPDWORD;
typedef void                 *LPVOID;
typedef void                 *PVOID;
typedef void                 *LPCVOID;

#ifndef NULL
#define NULL  0
#endif


#endif // TYPEREDEF_H
