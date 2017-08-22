'''
Constnats and Configuration data for the interface to the MCC 2408-2A0


'''
from RTEvent import RTEvent


################ Constants #########################
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

#Units
DEGREES_F = 'F'
DEGREES_C = 'C'
VOLTS = 'V'
AMPS = 'A'

THERMOCOUPLE_DATA_KEY   = 'TC'
ANALOG_INPUT_DATA_KEY   = 'AI'
ANALOG_OUTPUT_DATA_KEY  = 'AO'
DIGITAL_INPUT_DATA_KEY  = 'DI'
DIGITAL_OUTPUT_DATA_KEY = 'DO'
HUMIDITY_DATA_KEY       = 'HM'


############ Sensor Configuration Data ################################################

### Thermocouple configuration (Python dictionary of tuples) ###
#                    Channel MCCChannel   Type       Units  
tcConfig = {
	#'TC0': [ 0,      0,           TYPE_K,    DEGREES_F],

}

### Analog Inputs
#                           Channel   MCCChannel  Gain Range  Rate     Mode
analogInConfig  = { #'AI0': [ 0,       3,          BP_5V,      HZ1000,  DIFFERENTIAL ],
					#'AI1': [ 1,       7,          BP_5V,      HZ1000,  DIFFERENTIAL ]
}

### Analog Outputs
#                           Channel   MCCChannel
analogOutConfig = { #'AO0': [ 0,        0         ],
					#'AO0': [ 1,        1         ],
}

### Digital Inputs
#                       Channel   MCCChannel   Invert	RTEvent   RTEvent Type
digInConfig = {
			   'DI0': [ 0,        0,           False,    True,     RTEvent.DI_RISING_EDGE        ],
               'DI1': [ 1,        1,           False,    False,    None               ],
			   'DI2': [ 2,        2,           False,    False,    None               ],
			   'DI3': [ 3,        3,           False,    False,    None               ]			   
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
digOutConfig = {#'DO0': [ 0,        0,           True ],
                #'DO1': [ 1,        1,           True ],
				#'DO2': [ 2,        2,           True ],
				#'DO3': [ 3,        3,           True ]
}			

### Counters
#                          Channel   MCCChannel
counterConfig = {'H0': [ 0,        0],
                 #'CTR1': [ 1,        1]
}			




####################################################################################


