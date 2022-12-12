from threading import Thread
import hivemq_subscribe as mqtt
import firebase

mqtt_client: mqtt.hive_mq_client = None
firebase_session: firebase.firebase_session = None


def main():
    # Display the default message
    intro_message()

    # Setup code
    setup()

    # Run until user quits the program
    main_loop()
    
    # Shutdown all the components gracefully
    shutdown()



def intro_message():
    print("----------------------------------------------------")
    print("This is the hand gesture detection server program.")
    print("This program was designed by __names__here__...")
    print("----------------------------------------------------\n\n")


def setup():
    # Connect to firebase
    global firebase_session
    firebase_session = firebase.firebase_session()

    # Read the realtime database
    firebase_session.update_gestures_from_db()
    
    # Schedule a task to update the gestures every minute in a different thread
    Thread(target=firebase_session.schedule_updating_gestures).start()

    # Setup the mqtt subscribe stuff
    global mqtt_client
    mqtt_client = mqtt.hive_mq_client(firebase_session)
    mqtt_client.subscribe()


def main_loop():
    # End the program when the user enters something
    input("Enter anything to have the program exit...\n")
    shutdown()


def shutdown():
    print("Shutting down.... goodbye")

    global firebase_session
    firebase_session.stop_updating_gestures()
    global mqtt_client
    mqtt_client.stop()


if __name__ == '__main__':
    main()
