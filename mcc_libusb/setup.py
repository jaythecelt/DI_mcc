from distutils.core import setup, Extension
import shutil

#lmccusb  -lm -L/usr/local/lib -lhidapi-libusb -lusb-1.0 

module = Extension("mcc2408Module", 
					libraries = [ "mccusb", "m", "hidapi-libusb", "usb-1.0"  ],
					library_dirs = ["/home/pi/DI_mcc/mcc_libusb" ],
					sources = ["blinky.c" ])

setup(name="PackageName",
    version = "1.0",
    description="This is a package description",
    ext_modules = [module])

	

source = "/home/pi/DI_mcc/mcc_libusb/build/lib.linux-armv7l-3.4/mcc2408Module.cpython-34m.so"
dest   = "/home/pi/DI_mcc/mcc_libusb/mcc2408Module.cpython-34m.so"

print("Moving .so file from build to mcc_libusb")
shutil.copyfile(source, dest)
print("Done with setup.py")
