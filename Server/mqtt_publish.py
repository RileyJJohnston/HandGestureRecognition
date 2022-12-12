import mqtt_constants
import paho.mqtt.client as mqtt


def main():
    # Get the gesture from the user. This is what will be sent over mqtt.
    payload = input("What gesture to transmit (1-5)?: ")

    # Set up the client
    client = mqtt.Client(client_id=mqtt_constants.mqtt_clientId)
    client.username_pw_set(
        username=mqtt_constants.mqtt_username,
        password=mqtt_constants.mqtt_password
    )
    client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
    client.connect(mqtt_constants.mqtt_host, 8883, 60)

    # Set up the callbacks
    client.on_publish = on_publish

    # Publish the message
    message_info = client.publish(
        topic=mqtt_constants.mqtt_topic_publish,
        payload=payload,
        qos=2
    )

    # Wait until the message is published
    while not message_info.is_published():
        client.loop(1)

    print("Is the message published?: " + str(message_info.is_published()))

# with this callback you can see if your publish was successful


def on_publish(client: mqtt.Client, userdata, mid, properties=None):
    print("mid: " + str(mid))


if __name__ == "__main__":
    main()
