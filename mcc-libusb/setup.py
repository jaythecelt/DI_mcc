from distutils.core import setup, Extension

#lmccusb  -lm -L/usr/local/lib -lhidapi-libusb -lusb-1.0 

module = Extension("mcc2408Module", 
					libraries = [ "mccusb", "m", "hidapi-libusb", "usb-1.0"  ],
					library_dirs = ["/home/pi/DI_mcc/mcc-libusb" ],
					sources = ["blinky.c" ])

setup(name="PackageName",
    version = "1.0",
    description="This is a package description",
    ext_modules = [module])

	
print("Done with setup.py")
