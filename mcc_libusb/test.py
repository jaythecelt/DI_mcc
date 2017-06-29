import mcc2408Module


### Constants ###
#Thermocouples
TYPE_J = 0
TYPE_K = 1
TYPE_T = 2
TYPE_E = 3
TYPE_R = 4
TYPE_S = 5
TYPE_B = 6
TYPE_N = 7
DEGREES_F = 'F'
DEGREES_C = 'C'

#Analog Input Mode
DIFFERENTIAL = 0 #Voltage - differential
SE_HIGH      = 1 #Voltage - single-ended high channel
SE_LOW       = 2 #Voltage - single-ended low channel

#Analog Gain Ranges
BP_10V    = 1  # +/- 10V
BP_5V     = 2  # +/- 5V
BP_2_5V   = 3  # +/- 2.5V
BP_1_25V  = 4  # +/- 1.25V
BP_625V   = 5  # +/- 0.625V
BP_312V   = 6  # +/- 0.3125V
BP_156V   = 7  # +/- 0.15625V
BP_078V   = 8  # +/- 0.078125V Voltage (all), Thermocouple

#Analog Sample Rate
HZ30000          = 0       # 30,000 S/s
HZ15000          = 1       # 15,000 S/s
HZ7500           = 2       #  7,500 S/s
HZ3750           = 3       #  3,750 S/s
HZ2000           = 4       #  2,000 S/s
HZ1000           = 5       #  1,000 S/s
HZ500            = 6       #    500 S/s
HZ100            = 7       #    100 S/s
HZ60             = 8       #     60 S/s
HZ50             = 9       #     50 S/s
HZ30             = 10      #     30 S/s
HZ25             = 11      #     25 S/s
HZ15             = 12      #     15 S/s
HZ10             = 13      #     10 S/s
HZ5              = 14      #      5 S/s
HZ2_5            = 15      #    2.5 S/s

############ Sensor Configuration Data ################################################

### Thermocouple configuration (Python dictionary of tuples) ###
#                    Channel MCCChannel   Type       Units  
tcConfig = {'TC0': [ 0,      0,           TYPE_K,    DEGREES_F],
            'TC1': [ 1,      0,           TYPE_K,    DEGREES_C],
            'TC2': [ 2,      0,           TYPE_S,    DEGREES_F]
}

### Analog Inputs
#                           Channel   MCCChannel  Gain Range  Rate     Mode
analogInConfig  = { 'AI0': [ 0,       3,          BP_5V,      HZ1000,  DIFFERENTIAL ],
					'AI1': [ 1,       7,          BP_5V,      HZ1000,  DIFFERENTIAL ]
}

### Analog Outputs
#                           Channel   MCCChannel
analogOutConfig = { 'AO0': [ 0,        0         ],
					'AO0': [ 1,        1         ],
}

### Digital Inputs
#                       Channel   MCCChannel   Invert
digInConfig = {
			   'DI0': [ 0,        4,           False ],
               'DI1': [ 1,        5,           False ],
			   'DI2': [ 2,        6,           False ],
			   'DI3': [ 3,        7,           False ]			   
}			

### Digital Outputs
#	 (!)NOTE: The DIO are open-drain, which when used as an output is capable of sinking up
#             to 150 mA. Writing a "1" to a bit will cause its voltage to go LOW (0V), and
#             writing a "0" to the bit will cause the voltage to go HIGH (5V) by the 47k Ohm
#             pullup resister.
#             Setting Invert to TRUE means the output will be the same as the logical value
#             ... i.e. writing 1 sets the output to high.
#
#                        Channel   MCCChannel   Invert
digOutConfig = {'DO0': [ 0,        0,           True ],
                'DO1': [ 1,        1,           True ],
				'DO2': [ 2,        2,           True ],
				'DO3': [ 3,        3,           True ]
}			

####################################################################################



### Functions ######################################################################

def digitalIOTests():
	"Digital I/O Tests"

	# Read the digital inputs and print them
	di0 = mcc2408Module.readDIChannel(0)
	di1 = mcc2408Module.readDIChannel(1)
	di2 = mcc2408Module.readDIChannel(2)
	di3 = mcc2408Module.readDIChannel(3)

	print("\nDigital inputs are " +  str(di3) +  str(di2) +  str(di1) +  str(di0))


	print("\n*******************\n\n")
	print("Start testing...")
	print("Digital I/O")

	print("\nDI1 is connected to ground")
	di1 = mcc2408Module.readDIChannel(1)
	print("DI1 is: " + str(di1) + "  \tExpected = 0")


	print("\nDI0 is connected to DO3")
	print("Set DO3 to False")
	mcc2408Module.writeDOChannel(3, False);
	di0 = mcc2408Module.readDIChannel(0)
	print("DI0 is: " + str(di0) + "  \tExpected = 0")

	print("Set DO3 to True")
	mcc2408Module.writeDOChannel(3, True);
	di0 = mcc2408Module.readDIChannel(0)
	print("DI0 is: " + str(di0) + "  \tExpected = 1")


	print("\nDO1 is connected to the scope")
	print("Set DO1 to False")
	mcc2408Module.writeDOChannel(1, False);
	print("Expect the scope to show LOW on DO1")
	input('<')
	print("Set DO1 to True")
	mcc2408Module.writeDOChannel(1, True);
	print("Expect the scope to show HIGH on DO1")
	
	return;


def thermocoupleTests():
	"Tests the thermocouples"

	# Read and print the thermocouple values.
	tc0_temp = mcc2408Module.readTCChannel(0)
	tc1_temp = mcc2408Module.readTCChannel(1)
	tc2_temp = mcc2408Module.readTCChannel(2)

	print("\n")
	print("The temperature is: " +  str(tc0_temp) + " " + str(DEGREES_F) )
#	print("The temperature on channel 1 is: " +  str(tc1_temp) + " " + str(DEGREES_C) )
#	print("The temperature on channel 2 is: " +  str(tc2_temp) + " " + str(DEGREES_F) )

	return;


def analogInTests():
	"Test the analog inputs"
	
	# Read and print AI0, in volts.
	print("\n")
	print("MCC Channel AI3 is connected to MCC channel DIO0\n")
	volts = mcc2408Module.readAIChannel(0)
	print("AI0 volts = " + str(volts))
	print("\n")
	
	return;
	

def analogOutTests():
	"Test the analog outputs"
	
	# Set AO0
	print("\n")
	print("AO0 is connected to input AI7\n")
	mcc2408Module.writeAOChannel(0, 1)
	volts = mcc2408Module.readAIChannel(1)
	print("AI1 volts = " + str(volts))

	return;

#######################################################################################	
	
	
	
### ********* Main ****************	

### Init the MCC
print(mcc2408Module.version())
mcc2408Module.init()

### Init the MCC's channels per config data ###
# Thermocouples
for k, v in tcConfig.items():
    mcc2408Module.setTCConfig(v[0], v[1], v[2], ord(v[3]))

### Digital Inputs
for k, v in digInConfig.items():
    mcc2408Module.setDIConfig(v[0], v[1], v[2])
	
### Digital Outputs
for k, v in digOutConfig.items():
    mcc2408Module.setDOConfig(v[0], v[1], v[2])

### Analog Inputs
for k, v in analogInConfig.items():
    mcc2408Module.setAIConfig(v[0], v[1], v[2], v[3], v[4])

### Analog Outputs
for k, v in analogOutConfig.items():
    mcc2408Module.setAOConfig(v[0], v[1])

	
	
	
	
#print("\nThermocouple Tests\n")

while True:
    thermocoupleTests()
    input('>')
#print("\n")
#input('<')
#print("\nAnalog Input Tests\n")
#analogInTests()
#input('<')
#print("\nAnalog Output Tests\n")
#analogOutTests()




# Shutting down the MCC
mcc2408Module.shutdown

