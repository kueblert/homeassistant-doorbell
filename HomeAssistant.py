import paho.mqtt.client as mqtt
from Config import MQTT_BROKER, MQTT_PORT, MQTT_TOPIC, MQTT_USERNAME, MQTT_PASSWORD
from MQTTDevice import MQTTSensor

class HomeAssistant:
    doorbell_state: MQTTSensor
    voip_call_state: MQTTSensor
    dooropener_state: MQTTSensor
    ring_state: MQTTSensor

    def __init__(self):
        # Send a single message to set the mood
        # register for regular messages
        self.client = mqtt.Client("doorbell-client")
        self.client.username_pw_set(username=MQTT_USERNAME, password=MQTT_PASSWORD)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(MQTT_BROKER, MQTT_PORT, 60)
        self.client.loop_start()
        self.__init_sensors()
    
    def __init_sensors(self):
        self.doorbell_state = MQTTSensor(self.client, "doorbell_state", "Doorbell state", f"homeassistant/sensor/{MQTT_TOPIC}/doorbell_state/", "", "mdi:door-closed-lock")
        self.voip_call_state = MQTTSensor(self.client, "voip_call_state", "VOIP call state", f"homeassistant/sensor/{MQTT_TOPIC}/voip_call_state/", "", "mdi:phone")
        self.dooropener_state = MQTTSensor(self.client, "dooropener_state", "Door opener state", f"homeassistant/sensor/{MQTT_TOPIC}/dooropener_state/", "", "mdi:door")
        self.ring_state = MQTTSensor(self.client, "ring_state", "Ringing", f"homeassistant/sensor/{MQTT_TOPIC}/ringing/", "", "mdi:doorbell")
        
        self.doorbell_state.send("ONLINE")
        self.voip_call_state.send("DISCONNECTED")
        self.dooropener_state.send("0")
        self.ring_state.send("0")
    
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("MQTT connected.")
        else:
            print("MQTT error: ", rc)

    def on_message(self, client, userdata, msg):
        print("MQTT received: %s from %s" % (msg.payload.decode("utf-8"), msg.topic))
    
    def __del__(self):
        self.voip_call_state.send("OFFLINE")
        self.dooropener_state.send("0")
        self.ring_state.send("0")
        self.doorbell_state.send("OFFLINE")

    def open_door(self, should_open: bool):
        self.dooropener_state.send("1" if should_open else "0")
    
    def ring(self, should_ring: bool = True):
        self.ring_state.send("1" if should_ring else "0")
    
    def voice_connection(self, state: str):
        state2msg = {"init": "INITIALIZED", "estabilishing_call":"ESTABLISHING", "call_in_progess": "CALLING", "call_connected": "CONNECTED", "call_ended": "INITIALIZED", "error": "ERROR"}
        if state in state2msg:
            self.voip_call_state.send(state2msg[state])
        else:
            print("ERROR: Unknown SIP state!")
            self.voip_call_state.send("ERROR")
    
    def error(self, error: str):
        self.voip_call_state.send("ERROR")
        self.doorbell_state.send("ERROR")
