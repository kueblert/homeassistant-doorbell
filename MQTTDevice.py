import paho.mqtt.client as mqtt
import json

class MQTTSensor:
    def __init__(self, mqtt, uid, name, topic, unit, icon):
        self.mqtt = mqtt
        self.uid = uid
        self.name = name
        if topic[-1] != "/":
            topic += "/"
        self.topic = topic
        self.unit = unit
        self.icon = icon
        self.__config()
    
    def __config(self):
        config_topic = self.topic+"config"
        payload = {"unique_id": self.uid,
               "name": self.name,
               "state_topic": self.topic + "state",
               "unit_of_measurement": self.unit,
               "value_template": "{{ value_json.measurement }}" }
        if self.icon is not None:
               payload["icon"] = self.icon
        self.mqtt.publish(config_topic, json.dumps(payload))
    
    def send(self, measurement):
        topic = self.topic + "state"
        data = { 'measurement':    measurement }
        self.mqtt.publish(topic, json.dumps(data))
