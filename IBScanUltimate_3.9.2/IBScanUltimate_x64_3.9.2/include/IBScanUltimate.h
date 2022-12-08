/*
****************************************************************************************************
* IBScanUltimate.h
*
* DESCRIPTION:
*     Definition of image data structures for IBScanUltimate.
*     http://www.integratedbiometrics.com
*
* NOTES:
*     Copyright (c) Integrated Biometrics, 2009-2014
*
* HISTORY:
*     2012/04/12  Created.
*     2013/08/03  Reformatted.
*     2015/04/07  Added enumeration value to IBSU_ImageData.
*                     (ProcessThres)
****************************************************************************************************
*/

#pragma once

#ifdef __linux__
#include "LinuxPort.h"
#endif

#ifdef __cplusplus
extern "C" {
#endif 

/*
****************************************************************************************************
* GLOBAL TYPES
****************************************************************************************************
*/

/*
****************************************************************************************************
* IBSU_ImageFormat
*
* DESCRIPTION:
*     Enumeration of image formats.
****************************************************************************************************
*/
typedef enum tagIBScanUImageFormat
{
    IBSU_IMG_FORMAT_GRAY,    /* Gray-scale image. */
    IBSU_IMG_FORMAT_RGB24,   /* 24-bit color image. */
    IBSU_IMG_FORMAT_RGB32,   /* True-color RGB image. */
    IBSU_IMG_FORMAT_UNKNOWN  /* Unknown format. */
}
IBSU_ImageFormat;

/*
****************************************************************************************************
* IBSU_ImageData
*
* DESCRIPTION:
*     Container for image data and metadata.
****************************************************************************************************
*/
typedef struct tagIBSU_ImageData
{
    /* Pointer to image buffer.  If this structure is supplied by a callback function, this pointer 
     * must not be retained; the data should be copied to an application buffer for any processing
     * after the callback returns. */
    void             *Buffer;                           
    
    /* Image horizontal size (in pixels). */
    DWORD             Width;                            
    
    /* Image vertical size (in pixels). */
    DWORD             Height;                           
    
    /* Horizontal image resolution (in pixels/inch). */
    double            ResolutionX;                      
    
    /* Vertical image resolution (in pixels/inch). */
    double            ResolutionY;                      
    
    /* Image acquisition time, excluding processing time (in seconds). */
    double            FrameTime;                        
    
    /* Image line pitch (in bytes).  A positive value indicates top-down line order; a negative 
     * value indicates bottom-up line order. */
    int               Pitch;                            
    
    /* Number of bits per pixel. */
    BYTE              BitsPerPixel;
    
    /* Image color format. */
    IBSU_ImageFormat  Format;
    
    /* Marks image as the final processed result from the capture.  If this is FALSE, the image is
     * a preview image or a preliminary result. */
    BOOL              IsFinal;                    
    
    /* Threshold of image processing. */
    DWORD             ProcessThres;                    
}
IBSU_ImageData;

#ifdef __cplusplus
} // extern "C"
#endif 