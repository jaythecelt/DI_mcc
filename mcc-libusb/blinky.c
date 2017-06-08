/*
 *
 *  Copyright (c) 2015 Warren J. Jasper <wjasper@tx.ncsu.edu>
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2.1 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
 * Lesser General Public License for more details.
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
*/

#include <stdlib.h>
#include <time.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <ctype.h>
#include <math.h>


#include <Python.h>
#include "pmd.h"
#include "usb-2408.h"

#define MAX_COUNT     (0xffff)
#define FALSE 0
#define TRUE 1


int Cfib(int n)
{
	if (n<2)
		return n;
	else
		return Cfib(n-1) + Cfib(n-2);
}

static PyObject* fib(PyObject* self, PyObject* args)
{
	int n;
	if (!PyArg_ParseTuple(args, "i", &n))
		return NULL;
		
	blinkIt(25);
		
	return Py_BuildValue("i", Cfib(n));
}


static PyObject* version(PyObject* self)
{
	return Py_BuildValue("s", "Blinky Version 1.0");
}


// Method Definition
static PyMethodDef myMethods[] = {
	{"fib", fib, METH_VARARGS, "Calculates Fibonacci numbers"},
	{"version", (PyCFunction)version, METH_NOARGS, "Returns the version"},
	{NULL, NULL, 0, NULL}
};


// Module Definition
static struct PyModuleDef myModule = {
	PyModuleDef_HEAD_INIT,
	"myModule",
	"Fibonacci Module",
	-1, 
	myMethods
};

//Initializer Function
PyMODINIT_FUNC PyInit_myModule(void)
{
	return PyModule_Create(&myModule);
};





int blinkIt(int num)
{
  libusb_device_handle *udev = NULL;

  udev = NULL;
  
  int ret = libusb_init(NULL);
  if (ret < 0) {
    perror("usb_device_find_USB_MCC: Failed to initialize libusb");
    exit(1);
  }

  if ((udev = usb_device_find_USB_MCC(USB2408_PID, NULL))) {
    printf("Success, found a USB 2408!\n");
  } else if ((udev = usb_device_find_USB_MCC(USB2408_2AO_PID, NULL))) {
    printf("Success, found a USB 2408_2AO!\n");
//    usb2408_2AO = TRUE;
  } else {
    printf("Failure, did not find a USB 2408 or 2408_2AO!\n");
    return 0;
  }
  
  usbBlink_USB2408(udev, num);
  cleanup_USB2408(udev);
  return (0);
}



int main (int argc, char **argv)
{
  printf("==== Welcome to Blinky! ========\n");
  printf("Blinking that LED 25 times....\n");
  blinkIt(25);
  printf("Thanks for watching!\n");
  
  return 0;
}






