import paho.mqtt.client as mqtt

# MQTT global
client: mqtt.Client
payload = "1"
mqtt_clientId = ""
mqtt_username = "testing"
mqtt_password = "Abc12345"
mqtt_host = "f51bc650a9c24db18f2b2d13134a6da1.s1.eu.hivemq.cloud"
mqtt_port = 8883
mqtt_topic_publish = "gestures/dannywall"

def init_mqtt():
    global client
    # Set up the client
    client = mqtt.Client(client_id=mqtt_clientId)
    client.username_pw_set(
        username=mqtt_username,
        password=mqtt_password
    )
    client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
    client.connect(mqtt_host, 8883, 60)

    # Set up the callbacks
    client.on_publish = on_publish
    client.loop_start()

def publish(payload):
    global client

    client.publish(
        topic=mqtt_topic_publish,
        payload=payload,
        qos=2
    )

def on_publish(client: mqtt.Client, userdata, mid, properties=None):
    print("mid: " + str(mid))