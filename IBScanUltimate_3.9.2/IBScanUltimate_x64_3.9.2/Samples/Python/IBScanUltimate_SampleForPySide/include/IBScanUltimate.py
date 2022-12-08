from ctypes import *
from enum import Enum

'''
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
'''


'''
****************************************************************************************************
* GLOBAL TYPES
****************************************************************************************************
'''

'''
****************************************************************************************************
* IBSU_ImageFormat
*
* DESCRIPTION:
*     Enumeration of image formats.
****************************************************************************************************
'''
class IBSU_ImageFormat(Enum):
    IBSU_IMG_FORMAT_GRAY=0    #/* Gray-scale image. */
    IBSU_IMG_FORMAT_RGB24=1   #/* 24-bit color image. */
    IBSU_IMG_FORMAT_RGB32=2   #/* True-color RGB image. */
    IBSU_IMG_FORMAT_UNKNOWN=3  #/* Unknown format. */


'''
****************************************************************************************************
* IBSU_ImageData
*
* DESCRIPTION:
*     Container for image data and metadata.
****************************************************************************************************
'''
class IBSU_ImageData(Structure):
    _fields_ = [
        # /* Pointer to image buffer.  If this structure is supplied by a callback function, this pointer
        #  * must not be retained; the data should be copied to an application buffer for any processing
        #  * after the callback returns. */
        ("Buffer", c_void_p),
        #/* Image horizontal size (in pixels). */
		("Width", c_uint),
         #/* Image vertical size (in pixels). */
		("Height", c_uint),
         #/* Horizontal image resolution (in pixels/inch). */
		("ResolutionX", c_double),
         #/* Vertical image resolution (in pixels/inch). */
		("ResolutionY", c_double),
         #/* Image acquisition time, excluding processing time (in seconds). */
		("FrameTime", c_double),
         #/* Image line pitch (in bytes).  A positive value indicates top-down line order; a negative 
         # * value indicates bottom-up line order. */
		("Pitch", c_int),
         #/* Number of bits per pixel. */
		("BitsPerPixel", c_ubyte),
         #/* Image color format. */
		("Format", c_int),
         #/* Marks image as the final processed result from the capture.  If this is FALSE, the image is
         # * a preview image or a preliminary result. */
		("IsFinal", c_bool),
         #/* Threshold of image processing. */
		("ProcessThres", c_uint)
    ]
               

