# Door bell for FritzBox with Raspberry Pi and HomeAssistant
Connect a Raspberry Pi as a doorbell to an AVM Fritz!Box and to HomeAssistant.

Transmit voice between door and telephone (requires a speaker and microphone).
Trigger a door opener via Fritz!Fon.
Send events and state to HomeAssistant.

Uses Liblinphone for SIP communication, MQTT for communication with HomeAssistant.

IMPORTANT! This is made to work with my setup and so far untested as I am not actively operating this doorbell. You might need to adjust code to make it work with your setup. It might also possibly drop into unreliable states.

## Doorbell
Uses GPIO library to detect a button press and (planned development) can use another pin to trigger the door opener.

## Fritz.box
You need to install the device as a door opener in LAN connection mode.
Set login data and provide the information to the config file as well as ~/.linphonerc
Configure number of the door bell as 42 (only one bell is currently supported, but changing it should be trivial).
The door opener responds to dialing the digit 2.

## HomeAssistant
The device should be able to configure automatically using MQTT device detection. Make sure to have the MQTT Addon installed and the config file adjusted to your installation.

## Not implemented
No video feed. Purposefully.
