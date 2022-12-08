/* *************************************************************************************************
 * IBScanListener.java
 *
 * DESCRIPTION:
 *     Java wrapper for IBScanUltimate library
 *     http://www.integratedbiometrics.com
 *
 * NOTES:
 *     Copyright (c) Integrated Biometrics, 2013
 *     
 * HISTORY:
 *     2013/03/01  First version.
 ************************************************************************************************ */

package com.integratedbiometrics.ibscanultimate;

/**
 * Listener for device management events on an <code>IBScan</code>. This listener should be registered by  
 * an application with the <code>setScanListener()</code> method.
 */
public interface IBScanListener
{
    /**
     * Device count change notification.
     * 
     * @param deviceCount  new count of devices
     */
    public void scanDeviceCountChanged(int deviceCount);

    /**
     * Device initialization progress notification.  This notification occurs while the <code>openDevice()</code>
     * is executing; or after <code>openDeviceAsync()</code> has been called before initialization
     * completes or an error occurs.
     * 
     * @param deviceIndex   zero-based index of device
     * @param progressValue initialization progress between 0 and 100. A value of 100 indicates that
     *                      that initialization is complete.
     */
    public void scanDeviceInitProgress(int deviceIndex, int progressValue);

    /**
     * Device open complete notification.  This notification occurs after <code>openDeviceAsync()</code>
     * has been called when initialization completes or an error occurs.
     * 
     * @param deviceIndex  zero-based index of device
     * @param device       opened device, if successful; otherwise, <code>null</code>
     * @param exception    exception, if any, encountered while opening device; otherwise, 
     *                     <code>null</code>
     */
    public void scanDeviceOpenComplete(int deviceIndex, IBScanDevice device, IBScanException exception);
}
