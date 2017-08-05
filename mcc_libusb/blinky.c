/*
 *
 
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
#define DEGREES_C      'C'
#define DEGREES_F      'F'
#define MAX_THERMOCOUPLES 8
#define MAX_DIO 8
#define MAX_AI 8
#define MAX_AO 2
#define MAX_CNTR 2


/** MCC Channel configurations **/
typedef struct Thermocouple_Config_t
{
	uint8_t mccChannel;
	uint8_t tcType;
	char units;
} Thermocouple_Config;

Thermocouple_Config TCConfig[MAX_THERMOCOUPLES];

typedef struct DigitalIn_Config_t
{
	uint8_t mccChannel;
	uint8_t invert;
} DigitalIn_Config;

DigitalIn_Config DIConfig[MAX_DIO];

typedef struct DigitalOut_Config_t
{
	uint8_t mccChannel;
	char invert;
} DigitalOut_Config;

DigitalOut_Config DOConfig[MAX_DIO];

typedef struct AnalogIn_Config_t
{
	uint8_t mccChannel;
	uint8_t gainRange;
	uint8_t rate;
	uint8_t mode;
} AnalogIn_Config;

AnalogIn_Config AIConfig[MAX_AI];

typedef struct AnalogOut_Config_t
{
	uint8_t mccChannel;
	uint8_t invert;
} AnalogOut_Config;

AnalogOut_Config AOConfig[MAX_AO];

typedef struct Cntr_Config_t
{
	uint8_t mccChannel;
} Cntr_Config;

Cntr_Config CntrConfig[MAX_CNTR];



/** Functions **/
int    blinkIt(int num);
void   initDriver(void);
void   shutDownMCC(void);
double readTC(uint8_t channel);
uint8_t readDI(uint8_t channel);

/** Vars **/
//MCC device
libusb_device_handle *udev = NULL;

//Thermocouple tables//
double table_AIN[NGAINS_2408][2];
double table_AO[NCHAN_AO_2408][2];
float  table_CJCGrad[nCJCGrad_2408];

//LED on the MCC
int numberOfBlinks = 2;

//Python C Extension
static struct PyModuleDef mcc2408Module;
static PyMethodDef methods[];



/**********************/
/** Python functions **/
/**********************/

// Module Definition
static struct PyModuleDef mcc2408Module = {
	PyModuleDef_HEAD_INIT,
	"mcc2408Module",
	"Blinky Module",
	-1, 
	methods
};

//Initializer Function
PyMODINIT_FUNC PyInit_mcc2408Module(void)
{
	return PyModule_Create(&mcc2408Module);
};



/*** The Python Methods   ***/

/**
 *	Configures a thermocouple channel
 *
 */
static PyObject* setTCConfig(PyObject* self, PyObject* args)
{
	int channel;
	int mccChannel;
	char tcType;
	char units;
	
	if (!PyArg_ParseTuple(args, "i|i|b|b", &channel, &mccChannel, &tcType, &units)) {
		return NULL;
	}

	TCConfig[channel].mccChannel = mccChannel;
	TCConfig[channel].tcType = tcType;
	TCConfig[channel].units = units;
	
	return Py_BuildValue("i", mccChannel);
}


/**
 *	Configures a digital input channel
 *
 */
static PyObject* setDIConfig(PyObject* self, PyObject* args)
{
	int channel;
	int mccChannel;
	char invert;
	
	if (!PyArg_ParseTuple(args, "i|i|b", &channel, &mccChannel, &invert)) {
		return NULL;
	}

	DIConfig[channel].mccChannel = mccChannel;
	DIConfig[channel].invert = invert;
	
	return Py_BuildValue("i", mccChannel);
}

/**
 *	Configures a digital output channel
 *
 */
static PyObject* setDOConfig(PyObject* self, PyObject* args)
{
	int channel;
	int mccChannel;
	char invert;
	
	if (!PyArg_ParseTuple(args, "i|i|b", &channel, &mccChannel, &invert)) {
		return NULL;
	}

	DOConfig[channel].mccChannel = mccChannel;
	DOConfig[channel].invert = invert;
	
	return Py_BuildValue("i", mccChannel);
}

/**
 *	Configures an analog input channel
 *
 */
static PyObject* setAIConfig(PyObject* self, PyObject* args)
{
	int channel;
	int mccChannel;
	int gainRange;
	int rate;
	int mode;
	
	if (!PyArg_ParseTuple(args, "i|i|i|i|i", &channel, &mccChannel, &gainRange, &rate, &mode)) {
		return NULL;
	}

	AIConfig[channel].mccChannel = mccChannel;
	AIConfig[channel].gainRange = gainRange;
	AIConfig[channel].rate = rate;	
	AIConfig[channel].mode = mode;	
	
	return Py_BuildValue("i", mccChannel);
}


/**
 *	Configures an analog output channel
 *
 */
static PyObject* setAOConfig(PyObject* self, PyObject* args)
{
	int channel;
	int mccChannel;
	if (!PyArg_ParseTuple(args, "i|i", &channel, &mccChannel)) {
		return NULL;
	}
	AOConfig[channel].mccChannel = mccChannel;
	return Py_BuildValue("i", mccChannel);
}

/**
 *	Configures a counter channel
 *
 */
static PyObject* setCntrConfig(PyObject* self, PyObject* args)
{
	int channel;
	int mccChannel;
	if (!PyArg_ParseTuple(args, "i|i", &channel, &mccChannel)) {
		return NULL;
	}
	CntrConfig[channel].mccChannel = mccChannel;
	return Py_BuildValue("i", mccChannel);
}


/**
 *  Starts the counter specified by the channel in the parameter
 *
 */
  
static PyObject* startCntrChannel(PyObject* self, PyObject* args)
{
    int channel;
    int mccChannel;
    
	if (!PyArg_ParseTuple(args, "i", &channel)) {
		return NULL;
	}
    mccChannel = CntrConfig[channel].mccChannel;

    usbCounterInit_USB2408(udev, mccChannel);
    return Py_BuildValue("i", mccChannel);
}

/**
 *  Reads the 32 bit counter specified by the channel in the parameter
 *
 */

static PyObject* readCntrChannel(PyObject* self, PyObject* args)
{
	int channel;
	int mccChannel;
    int val;
    
	if (!PyArg_ParseTuple(args, "i", &channel)) {
		return NULL;
	}
    mccChannel = CntrConfig[channel].mccChannel;
    val = usbCounter_USB2408(udev, mccChannel);
    
    return Py_BuildValue("i", val);
}


/**
 *  Returns the thermocouple reading on the channel specified by the parameter.
 *
 */
static PyObject* readTCChannel(PyObject* self, PyObject* args)
{
	int channel;
	
	if (!PyArg_ParseTuple(args, "i", &channel)) {
		return NULL;
	}

    double temp = readTC(channel);

	return Py_BuildValue("d", temp);
}


/**
 *  Returns the digital input reading on the channel specified by the parameter.
 *
 */
static PyObject* readDIChannel(PyObject* self, PyObject* args)
{
	uint8_t channel;
	if (!PyArg_ParseTuple(args, "b", &channel)) {
		return NULL;
	}
	uint8_t data = usbDIn_USB2408(udev, 0);

	uint8_t shift = DIConfig[channel].mccChannel;
	if (DIConfig[channel].invert) {
		data = ~data;
	}
	data = data >> shift;
	data = data & 0x01;

	return Py_BuildValue("i", data);
}


/**
 *  Writes the digital output on the channel specified by the parameter.
 *
 */
static PyObject* writeDOChannel(PyObject* self, PyObject* args)
{
	uint8_t channel;
	uint8_t data;
	
	if (!PyArg_ParseTuple(args, "b|b", &channel, &data)) {
		printf("Parameter error!");
		return NULL;
	}

	uint8_t bitno = DOConfig[channel].mccChannel;
	uint8_t portData = usbDOutR_USB2408(udev, 0); //Read the digital output latch

	if (DOConfig[channel].invert) 
		data = ~data;
	data = data & 0x01;      //Mask any extra bits, using only bit 0
	portData &= ~(1<<bitno); //Clear the bit from portData
	portData |= data<<bitno; //Set the bit to the data value
	usbDOut_USB2408(udev, portData, 0); //Writes the entire port to the latch.

	return Py_BuildValue("i", data); //Return what was written
}

/**
 *  Returns the value in the digital output latch.
 *
 */
static PyObject* readDOLatch(PyObject* self, PyObject* args)
{
	uint8_t portData = usbDOutR_USB2408(udev, 0); //Read the digital output latch
	return Py_BuildValue("i", portData);
}

static PyObject* readAIChannel(PyObject* self, PyObject* args)
{
	int channel;
	int data;
	uint8_t flags;
	double volts;
	int gain;
	
	if (!PyArg_ParseTuple(args, "i", &channel)) {
		return NULL;
	}
	
	//Get the raw data from the MCC
	data = usbAIn_USB2408(	udev, 
							AIConfig[channel].mccChannel, 
							AIConfig[channel].mode, 
							AIConfig[channel].gainRange, 
							AIConfig[channel].rate, 
							&flags);

	gain = AIConfig[channel].gainRange;
	//Calculate voltage
	data = data*table_AIN[gain][0] + table_AIN[gain][1];
	volts = volts_USB2408(gain, data);
	
	return Py_BuildValue("d", volts);
}

static PyObject* writeAOChannel(PyObject* self, PyObject* args)
{
	int channel;
	double volts;

	if (!PyArg_ParseTuple(args, "i|d", &channel, &volts)) {
		return NULL;
	}
    usbAOut_USB2408_2AO(udev, AOConfig[channel].mccChannel, volts, table_AO);
	return Py_BuildValue("d", volts);
}




/**
 * Sets the number of times to blink the LED on the MCC.  
 * (see doBlinks)
 */
static PyObject* setBlinks(PyObject* self, PyObject* args)
{
	int n;
	if (!PyArg_ParseTuple(args, "i", &n))
		return NULL;

	numberOfBlinks = n;
	return Py_BuildValue("i", n);
}

/**
 *	Blinks the LED on the MCC numberOfBlinks times.
 *
 */
static PyObject* doBlinks(PyObject* self)
{
	blinkIt(numberOfBlinks);
	return Py_BuildValue("s", "Blinking!");
}

/**
 *	Initializes the driver.  Call this first!
 *
 */
static PyObject* init(PyObject* self)
{
	initDriver();
	return Py_BuildValue("s", "Success.");
}

/**
 *	Shuts down the MCC and the driver.  Call this last!
 *
 */
static PyObject* shutdown(PyObject* self)
{
	shutDownMCC();
	return Py_BuildValue("s", "Success.");
}


/**
 *  Returns the name and version of this module.
 *
 */
static PyObject* version(PyObject* self)
{
	return Py_BuildValue("s", "Blinky Version 2.0");
}



/*** Python Module and Method Definitions ***/

// Method Definition
static PyMethodDef methods[] = {
	{"setTCConfig",    setTCConfig,              METH_VARARGS, "Configures a TC channel"},
	{"setDIConfig",    setDIConfig,              METH_VARARGS, "Configures a DI channel"},
	{"setDOConfig",    setDOConfig,              METH_VARARGS, "Configures a DO channel"},
	{"setAIConfig",    setAIConfig,              METH_VARARGS, "Configures a AI channel"},
	{"setAOConfig",    setAOConfig,              METH_VARARGS, "Configures a AO channel"},
    {"setCntrConfig",  setCntrConfig,            METH_VARARGS, "Configures a Counter channel"},
	{"readTCChannel",  readTCChannel,            METH_VARARGS, "Reads the thermocouple" },
	{"readDIChannel",  readDIChannel,            METH_VARARGS, "Reads the digital input" },	
	{"writeDOChannel", writeDOChannel,           METH_VARARGS, "Writes a digital output" },	
	{"readAIChannel",  readAIChannel,            METH_VARARGS, "Reads an AI channel"},
	{"writeAOChannel", writeAOChannel,           METH_VARARGS, "Writes an analog output" },	
	{"readDOLatch",    (PyCFunction)readDOLatch, METH_NOARGS,  "Reads the digital output latch"},
    {"startCntrChannel", startCntrChannel,       METH_VARARGS, "Start a Counter channel"},
    {"readCntrChannel", readCntrChannel,         METH_VARARGS, "Reads a Counter channel"},
	{"setBlinks",      setBlinks,                METH_VARARGS, "Test function Sets the number of blinks" },
	{"doBlinks",       (PyCFunction)doBlinks,    METH_NOARGS, "Blink the LED per setBlinks value" },
	{"init",           (PyCFunction)init,        METH_NOARGS, "Initialize the driver" },
	{"shutdown",       (PyCFunction)shutdown,    METH_NOARGS, "Shutdown the driver" },
	{"version",        (PyCFunction)version,     METH_NOARGS, "Returns the version of this module"},
	{NULL, NULL, 0, NULL}
};




/********************************************************************************************************/



/************************/
/*** Implementations  ***/
/************************/


/**
 *	Initialize the MCC and the driver.
 *
 */
void initDriver()
{
    int ret = libusb_init(NULL);
    if (ret < 0) {
        perror("usb_device_find_USB_MCC: Failed to initialize libusb");
        exit(1);
    }

  if ((udev = usb_device_find_USB_MCC(USB2408_PID, NULL))) {
    printf("Found a USB 2408.  Note: analog outputs are not available with this model.\n");
  } else if ((udev = usb_device_find_USB_MCC(USB2408_2AO_PID, NULL))) {
    printf("Found a USB 2408_2AO.\n");
  } else {
    printf("Failure, did not find a USB 2408 or 2408_2AO!\n");
    exit(2);
  }
    //Build analog in and thermocouple tables//
    usbBuildGainTable_USB2408(udev, table_AIN);
    usbBuildCJCGradientTable_USB2408(udev, table_CJCGrad);
    //Build analog out table
    usbBuildGainTable_USB2408_2AO(udev, table_AO);
  
}


double readTC(uint8_t channel)
{
    double temperature = tc_temperature_USB2408(udev, TCConfig[channel].tcType, TCConfig[channel].mccChannel);
    
	if (TCConfig[channel].units == DEGREES_F) {
		//Return degrees F
		return (temperature * 9./5. + 32.);
	}
	//Else return degrees C
    return temperature;
}






/** 
 *	Blinks the LED on the MCC the number of times as provided in the parameter.
 *
 */
int blinkIt(int num)
{
  usbBlink_USB2408(udev, num);
  return (num);
}


/** 
 *	Provides a clean shutdown of the MCC and the driver.
 *
 */
void shutDownMCC()
{
  cleanup_USB2408(udev);	
}







