import network
import time
from umqtt.simple import MQTTClient

SSID = "Phone43"
WIFI_PASSWORD = "hellomann"

CLIENT_ID = b'MorseCode'
HIVE_URL = 'f6916d7ba7d14b32a68d2d99b9074a6d.s1.eu.hivemq.cloud'
USERNAME = b'cameron'
PASSWORD = b'Dundee123'

SUB_TOPIC = b'button'   # no leading slash
PUB_TOPIC = b'status'

latest_message = None

def wifi_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, WIFI_PASSWORD)
    while not wlan.isconnected():
        time.sleep(0.5)

def mqtt_callback(topic, msg):
    global latest_message
    latest_message = msg.decode('utf-8')

wifi_connect()
mqtt = MQTTClient(
    client_id=CLIENT_ID,
    server=HIVE_URL,
    port=8883,
    user=USERNAME,
    password=PASSWORD,
    keepalive=60,
    ssl=True,
    ssl_params={'server_hostname': HIVE_URL}
)
mqtt.set_callback(mqtt_callback)
mqtt.connect()
mqtt.subscribe(SUB_TOPIC)

def publish_message(text):
    mqtt.publish(PUB_TOPIC, text.encode('utf-8'))

usrinput = input("message(0) or receive(1): ")
if usrinput == "1":
    while True:
        mqtt.wait_msg()   # blocks until a message arrives
        if latest_message:
            print("Received:", latest_message)
            latest_message = None
else:
    input2 = input("enter message: ")
    publish_message(input2)