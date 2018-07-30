import time
import usb
from enum import Enum
import json
import re
import RPi.GPIO as GPIO # Pi GPIO library


#-----------------------------------#

'''
System operation finite-state machine enumeration class
'''
class State(Enum):
    WAITING_FOR_LICENSE = 1
    WAITING_FOR_PHONE = 2
    OPERATION_WITHOUT_PHONE = 3
    OPERATION_WITH_PHONE = 4
    WRONG_DEVICE = 5
    CLOSE_BOX = 6

Output = {
    'LED1': 38,
    'LED2': 40,
    'INTERLOCK': 12,
    'REED': 37
}

def addToLogFile(message):
    with open('logs.txt', 'a') as f:

        f.write(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()) + message + "\n\n")

def logAccess(phone, card):
    addToLogFile("Licence: " + card + "   \t Phone Serial Number: " + phone)

def logOtherUser(card):
    addToLogFile("**OTHER USER** Licence: " + card)

def logError(message):
    addToLogFile("**ERROR** " + message)

def initialize_gpio():
    global Output
    GPIO.setmode(GPIO.BOARD) # Uses GPIO numbering as it appears on board header
    GPIO.setwarnings(False) # Disable GPIO warnings messages

    #------- GPIO Initialization -------#
    #LED UI
    GPIO.setup(Output['LED1'], GPIO.OUT) # Configured as analog output *
    GPIO.setup(Output['LED2'], GPIO.OUT) # *

    #Ignition Interlock
    GPIO.setup(Output['INTERLOCK'], GPIO.OUT) # *

    #Reed Switch
    GPIO.setup(Output['REED'], GPIO.IN, pull_up_down=GPIO.PUD_UP) # Configured as input w/ pull-up resistor 

    # Forcen GPIO states for initialization												  
    GPIO.output(Output['LED1'],GPIO.LOW)
    GPIO.output(Output['LED2'],GPIO.LOW)
    GPIO.output(Output['INTERLOCK'],GPIO.LOW)
    
def is_culprit_license(card_info):
    with open('info.json') as f:
        data = json.load(f)

    # Check if scanned license is in list of culprit licenses
    return card_info in data.values()


def is_drivers_license(card_info):
    regex = '^%[A-Z]+\^[A-Z\-]+,\$[A-Z ]+\^[0-9A-Z\- ]+\$[A-Z]+ [A-Z]+  [0-9A-Z ]typ+\^*\?;[0-9]{13}=[0-9]{12}=\?\+[0-9A-Z]{8} {21}[A-Z0-9]+ [A-Z0-9]+ +\S+\?$'
    return re.match(regex, card_info)

def enable_vehicle():
    print('vehicle enabled')

def setup_config(card_info):
    dict = {}
    dict['driver_info'] = card_info
    #add more json entries if u want
    json_string = json.dumps(dict)
    with open('info.json', 'w') as outfile:
        json.dump(dict, outfile)




'''
Checks all the connected USB devices and returns the serial number
of the connected device.
IDEALLY, we would only check one specific address (the USB port
that the phone will connect to should now change, but it seems that
the address changes each time the device is unplugged.
'''
def poll_device():
    for dev in usb.core.find(find_all=True):

        if True:
            try:
                if dev.serial_number is not None:
                    return dev.serial_number
            except:
                pass
    return None;


'''
System operation tracks the current state of the system,
as well as the serial number of the connected device.
'''
def main():

    state = State.WAITING_FOR_LICENSE
    device_serial_number = None
    card_info = None
    
    initialize_gpio()

    with open("info.json") as config:
        data = json.load(config)
    
    while True:
       # card_info = ""

        if state == State.WAITING_FOR_LICENSE:
            print ("WAITING FOR LICENSE")

            initialize_gpio() # turn gpios all off again

            card_info = input("CC: \n")
            if is_culprit_license(card_info):
                state = State.WAITING_FOR_PHONE
                
            elif is_drivers_license(card_info):
                state = State.OPERATION_WITHOUT_PHONE
                logOtherUser(card_info)

            else:
                print ("wrong drivers license dummy")
                logError("Invalid Drivers Licence")


        if state == State.WAITING_FOR_PHONE:
            print ("WAITING FOR PHONE")

            # gpio for led to signal driver's license read
            GPIO.output(Output['LED1'],GPIO.HIGH)
            
            device_serial_number = poll_device()

            if device_serial_number is not None:
                try:
                    print (card_info, " card_ info")
                    print (device_serial_number, " dev serial number")
                    print (data[device_serial_number], " data")
                    if card_info == data[device_serial_number]:
                        state = State.CLOSE_BOX
                        logAccess(card_info, device_serial_number)
                    
                    else:
                        #device_serial_number is not None:
                        state = State.WRONG_DEVICE
                except:
                    pass

        if state == State.CLOSE_BOX:
            print ("WAITING FOR BOX CLOSE")

            GPIO.output(Output['LED2'],GPIO.HIGH)
            GPIO.wait_for_edge(Output['REED'], GPIO.FALLING, 400)
            print ('box closed')
            state = State.OPERATION_WITH_PHONE
            

        if state == State.OPERATION_WITHOUT_PHONE:
            print ("ENABLE VEHICLE OPERATION, NOT CULPRIT")

            # do gpio stuff to allow vehicle vroom (me mumz caar) ignition interlock
            GPIO.output(Output['INTERLOCK'],GPIO.HIGH)


        if state == State.OPERATION_WITH_PHONE:
            print ("ENABLE VEHICLE OPERATION, PHONE REQUIRED")

            # gpio stuff to enable vehicle vroom ignition interlock and LED2
            GPIO.output(Output['INTERLOCK'],GPIO.HIGH)
            print ('interlock disengaged')
            
            device_serial_number = poll_device()
            if device_serial_number is None:
                state = State.WAITING_FOR_LICENSE


        if state == State.WRONG_DEVICE:
            print ("INCORRECT DEVICE CONNECTED")
            logError("Wrong device")
            device_serial_number = poll_device()
            
            if card_info == data[device_serial_number]:
                state = State.OPERATION
            elif device_serial_number is None:
                state = State.WAITING_FOR_LICENSE
            
        time.sleep(1)

while (True):
    try:
        main()

    except KeyboardInterrupt:
        GPIO.cleanup()
        pass







