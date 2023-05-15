from time import sleep
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library

from Config import BUTTON_GPIO_PIN, OPENER_GPIO_PIN

class Doorbell:
    def __init__(self):
        #GPIO.setwarnings(False) # Ignore warning for now
        GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
        GPIO.setup(BUTTON_GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(OPENER_GPIO_PIN, GPIO.OUT)
    
    def __del__(self):
        GPIO.cleanup()
    
    def wait_for_ring(self):
        while True:
            if GPIO.input(BUTTON_GPIO_PIN) == GPIO.HIGH:
                return
            else:
                sleep(0.01)
    
    def open(self):
        GPIO.output(OPENER_GPIO_PIN, 1)
        time.sleep(Config.OPENER_ACTIVE_DURATION)
        GPIO.output(OPENER_GPIO_PIN, 0)


class DummyDoorbell(Doorbell):
    # Rings the doorbell after a timeout is reached
    # Intended for debugging when no physical doorbell is connected
    counter:  int = 2
    
    def wait_for_ring(self):
        while True:
            if self.counter == 0:
                print("Ringing that bell for you.")
                return
            else:
                print("Sleeping for %i more seconds."%self.counter)
                sleep(1)
                self.counter-=1
    
    def open(self):
        GPIO.output(OPENER_GPIO_PIN, 1)
        time.sleep(Config.OPENER_ACTIVE_DURATION)
        GPIO.output(OPENER_GPIO_PIN, 0)
