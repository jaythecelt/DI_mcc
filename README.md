# DI_mcc
A data injector that works with an MCC USB2408 or USB2408-2AO.

## Installation
DI_mcc runs on Python 3.4+
```sh
$ cd /home/pi
```
Clone the MCC Data Injector drivers:
```sh
$ git clone git://github.com/jaythecelt/DI_mcc.git
```
Install libusb:  
```sh
$ sudo apt-get install libusb-1.0-0 libusb-1.0-0-dev 
```
Copy the mcc USB rules file to the /etc/udev/rules.d directory, renaming it to 99-mcc.rules (preventing an issue with the standard naming on the Raspberry Pi):
```sh
$ cd DI_mcc
$ sudo cp 61-mcc.rules /etc/udev/rules.d/99-mcc.rules
```
HIDAPI is required to interface with Human Interface Devices (HID).
Clone the hidapi GIT repository to the home/pi directory: 
```sh
$ cd /home/pi
$ git clone git://github.com/signal11/hidapi.git
```
From the instructions in the hidapi README.txt to install the hidapi library:
The autotools package is required for building the hidapi library.  Install autotools, a suite of programming tools designed to assist in making source code packages portable to Unix-like systems. 
```sh
$ sudo apt-get install libudev-dev libfox-1.6-dev autotools-dev autoconf automake libtool 
```
Compile the hidapi library: 
```sh
$ cd ~pi/hidapi
$ ./bootstrap
$./configure
$ make
$ sudo make install
```
Reboot!

## Build the MCC data injector
Install the Linux drivers and compile the test app 
```sh
$ cd ~pi/DI_mcc/mcc_libusb
$ sudo make
$ sudo make install
$ sudo ldconfig  
$ sudo python3 setup.py build
```

## Test App to verify comms withe the MMC USB2408 device
If an MCC 2408-2AO is available:
Connect MCC USB2408-2A0 to a USB port on the RPi
```sh
$ cd ~pi/DI_mcc/mcc_libusb
$ ./test-usb2408
```
If successful, there should be a menu of commands that appear that allow the user to read and set the various I/O on the MCC
