import configparser

config = configparser.ConfigParser()
config.read('klingel.ini')

DOOR_OPEN_CODE = config.get("sip", "door_open_code", fallback="2")
RING_SIP_NUMBER = config.get("sip", "ring_number", fallback="42")
SIP_USERNAME = config.get("sip", "username", fallback="sprechanlage")
SIP_PASSWORD = config.get("sip", "password", fallback="")

BUTTON_GPIO_PIN = config.getint("bell", "button_gpio_pin", fallback=10)
OPENER_GPIO_PIN = config.getint("bell", "opener_gpio_pin", fallback=11)

MQTT_BROKER = config.get("mqtt", "broker", fallback="homeassistant.local")
MQTT_TOPIC = config.get("mqtt", "topic", fallback="doorbell")
MQTT_USERNAME = config.get("mqtt", "username", fallback="mqtt")
MQTT_PASSWORD = config.get("mqtt", "password", fallback="")
MQTT_PORT = config.getint("mqtt", "port", fallback=1883)