#!/usr/bin/python3
from LinphoneInterface import LinphoneInterface
from HomeAssistant import HomeAssistant
from Doorbell import Doorbell
from time import sleep

from Config import DOOR_OPEN_CODE, RING_SIP_NUMBER

# TODO make doorbell work even when HomeAssistant is not available.
homeassistant = HomeAssistant()
doorbell = Doorbell()

def open_door():
    print("#### DOOR OPEN ####")
    doorbell.open()
    homeassistant.open_door(True)

def state_change_callback(state: str):
    print("SIP state: %s" % state)
    if state == "call_connected":
        homeassistant.voice_connection(state)
    else:
        homeassistant.voice_connection(state)

def code_callback(code: str):
    print("Code received: %s" % code)
    if code == DOOR_OPEN_CODE:
        open_door()

def error_callback(error: str):
    if "liblinphone-error-LinphoneCore has video disabled for both capture and display, but video policy is to start the call with video." in error:
        return
    if "iblinphone-error-Unable to determine IP version from signaling operation, no via header found" in error:
        return
    if "discarding too old packet" in error:
        return
    if"ortp-error-Jitter buffer stays unconverged for one second, reset it." in error:
        return

    homeassistant.error(error)
    print("ERROR: %s" % error)

def perform_voice_call():
    homeassistant.ring()
    phone = LinphoneInterface(state_change_callback, code_callback, error_callback)
    phone.call(RING_SIP_NUMBER)

    # wait for the call to finish
    while phone.should_run:
        sleep(0.1)

print("Active")
while True:
    doorbell.wait_for_ring()
    print("RINGGGG")
    perform_voice_call()
    print("Waiting for another ring...")

print("Terminated")
