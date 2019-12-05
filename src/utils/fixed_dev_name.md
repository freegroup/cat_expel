If you have multiple USB devices connected, sometimes after a reboot the device order is changed (ttyUSB0 is ttyUSB1, or the other way around)

The good news is, that there is a solution for this. This page explains how to 'lock' the serial ports into place.

## Introduction 

When you plug in multiple USB devices that emulate a terminal (for instance the P1 cable and RFXcom transceiver) the Raspberry randomly allocates ttyyUSBx device names. This means that if Domoticz is configured to use ttyUSB0 for the P1 cable, the device may show up at ttyUSB1 after the next reboot. This means the P1 connection no longer works. You can assign a fixed device name for a given USB device. 

## Procedure

From a terminal window:


2. list all attributes of the devices (in this case video0 and video2):


 ...
 pi@raspberrypi:~ $ udevadm info -a -p  $(udevadm info -q path -n /dev/video2)
 ...
  looking at parent device '/devices/platform/soc/3f980000.usb/usb1/1-1/1-1.2':
    KERNELS=="1-1.2"
    SUBSYSTEMS=="usb"
    DRIVERS=="usb"
    ATTRS{bDeviceSubClass}=="00"
    ATTRS{bDeviceProtocol}=="00"
    ATTRS{devpath}=="1.2"
    ATTRS{idVendor}=="0403"
    ATTRS{speed}=="12"
    ATTRS{bNumInterfaces}==" 1"
    ATTRS{bConfigurationValue}=="1"
    ATTRS{bMaxPacketSize0}=="8"
    ATTRS{busnum}=="1"
    ATTRS{devnum}=="4"
    ATTRS{configuration}==""
    ATTRS{bMaxPower}=="90mA"
    ATTRS{authorized}=="1"
    ATTRS{bmAttributes}=="a0"
    ATTRS{bNumConfigurations}=="1"
    ATTRS{maxchild}=="0"
    ATTRS{bcdDevice}=="0600"
    ATTRS{avoid_reset_quirk}=="0"
    ATTRS{quirks}=="0x0"
    ATTRS{serial}=="A1LPXWF"
    ATTRS{version}==" 2.00"
    ATTRS{urbnum}=="179474001"
    ATTRS{ltm_capable}=="no"
    ATTRS{manufacturer}=="RFXCOM"
    ATTRS{removable}=="removable"
    ATTRS{idProduct}=="6001"
    ATTRS{bDeviceClass}=="00"
    ATTRS{product}=="RFXtrx433"
 ...

Look at the tree leaf matching the node name from the prior step. In this case '''..../usb1/1-1/1-1.3''' and '''..../usb1/1-1/1-1.2'''
You have to look at a unique differentiator between the devices. In most cases you can use the idVendor field (0403 in this case) or the idProduct  field (6001 in this case) as the differentiator between the two devices. In case the vendor ID is the same, you can use the serial number of the two devices. 

3. We are now going to create a new USB device linked to the unique information we have. Create a file /etc/udev/rules.d/10-usb-video.rules with rules for all USB devices in it:
```
sudo vi /etc/udev/rules.d/10-usb-video.rules
```

Note: the serial numbers, idVendor and idProduct shown as these need to be replaced by your ids
In case you have devices that have different vendor ids you can leave out the Serial attribute part:<br>

```
SUBSYSTEM=="video4linux", ATTRS{idVendor}=="046d", ATTRS{idProduct}=="081b", ATTRS{serial}=="539A4A60",  SYMLINK+="video_left"
SUBSYSTEM=="video4linux", ATTRS{idVendor}=="046d", ATTRS{idProduct}=="081b", ATTRS{serial}=="57618940",  SYMLINK+="video_right"
```

4. Load the new rule:
```
sudo udevadm trigger
```

5. Verify this works:

```
 ls -l /dev/video*
 crw-rw---- 1 root dialout 188, 0 Nov 11 10:29 /dev/video0
 crw-rw---- 1 root dialout 188, 1 Nov 11 10:00 /dev/video2
 lrwxrwxrwx 1 root root         7 Nov 11 10:00 /dev/video_left -> video0
 lrwxrwxrwx 1 root root         7 Nov 11 10:00 /dev/video_right -> video2
```

As you see we still have the existing video0 and video1 devices, but we also have 2 symbolic links to devices that are match the correct hardware. These symbolic links will be created at each reboot or when the Video device is plugged into an USB port.


An article with more background is available on Stackexchange: 
[http://unix.stackexchange.com/questions/66901/how-to-bind-usb-device-under-a-static-name]
