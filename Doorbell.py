from time import sleep
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library

from Config import BUTTON_GPIO_PIN, OPENER_GPIO_PIN

class Doorbell:
    def __init__(self):
        #GPIO.setwarnings(False) # Ignore warning for now
        GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
        GPIO.setup(BUTTON_GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
    def __del__(self):
        GPIO.cleanup()
    
    def wait_for_ring():
        while True:
            if GPIO.input(BUTTON_GPIO_PIN) == GPIO.HIGH:
                return
            else:
                sleep(0.01)
    
    def open():
        #TODO use OPENER_GPIO_PIN
        print("DOOR OPENER NOT IMPLEMENTED!")
