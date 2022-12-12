import requests
import time
import sched
from getpass import getpass
from firebase_admin import db
import json

API_KEY = "AIzaSyAx-h8OoQMpsBRplnKzmM0gwCpZpmcl2pk"

class firebase_session:
    
    # The time between each firebase realtime db update
    UPDATE_TIME = 30

    def __init__(self):
        # Loop enter the user enters a valid account
        while True:
            # Get input from user
            email = input("Enter the email: ")
            password = getpass()

            # Create the session
            try:
                self.signin(email, password)
                print("Logged into firebase account.")

                break
            except BaseException as e:
                print("Log in failed, try again: \"" + e.args[0] + "\"")


    def make_request(self, url, method="GET", body={}):
        if self.is_token_expired():
            self.refresh_token()

        response = requests.request(
            method=method,
            url=url,
            data=body
        )

        return response

    def update_gestures_from_db(self):
        url = "https://smarthome-4feea-default-rtdb.firebaseio.com/user:" + self.email.replace(".", "") + "/actuators.json"
        print(url)

        response = self.make_request(url)
        self.gestures = response.json()
        
        print(self.gestures)
        
        # Only schedule another update if the scheduler is defined
        if hasattr(self, "sched"):
            self.next_event = self.sched.enter(self.UPDATE_TIME, 1, self.update_gestures_from_db)
            self.sched.run()
        
    def get_gestures(self):
        if not hasattr(self, "gestures"):
            self.gestures = []
        return self.gestures
    
    def schedule_updating_gestures(self):
        self.sched = sched.scheduler(time.time, time.sleep)
        self.next_event = self.sched.enter(self.UPDATE_TIME, 1, self.update_gestures_from_db)
        self.sched.run()
        
    def stop_updating_gestures(self):
        if hasattr(self, "next_event"):
            self.sched.cancel(self.next_event)
            self.sched = None

    def logEvent(self, firebase_session, actuator, ip, timeStamp):
        index = self.numberEvents();
        url = "https://smarthome-4feea-default-rtdb.firebaseio.com/user:" + firebase_session.email.replace(".", "") + "/events/" + str(index) + ".json"
        body = json.dumps({'actuatorName' : actuator,'ip':ip,'timestamp': timeStamp})
        method = "PUT"

        if firebase_session.is_token_expired():
            firebase_session.refresh_token()

        response = requests.request(
            method=method,
            url=url,
            data=body
        )

    def numberEvents(self):
        events = self.fetchEvents()
        if (events == None):
            return 0
        else:
            return len(events)


    def fetchEvents(self):
        url = "https://smarthome-4feea-default-rtdb.firebaseio.com/user:" + self.email.replace(".", "") + "/events.json"
        print(url)

        response = self.make_request(url)
        self.events = response.json()

        return self.events

    def signin(self, email: str, password: str):
        url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=" + API_KEY

        body = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }

        response = requests.post(
            url=url,
            data=body
        )

        if (response.status_code != 200):
            error_msg = "Error code " + str(response.status_code)

            # Check if the response is json to add a more detailed message
            if response.headers.get('content-type').__contains__('application/json'):
                error_msg += ", message: " + response.json()['error']['message']
            else:
                error_msg += ", message: " + response.text

            # Some error occured
            raise ValueError(error_msg)

        jsonResponse = response.json()
        
        self.email = email
        self.id_token = jsonResponse['idToken']
        self.refreshtoken =jsonResponse['refreshToken']
        self.expires_in = int(jsonResponse['expiresIn'])
        self.expiration_time = time.time() + self.expires_in


    def refresh_token(self):
        url = "https://securetoken.googleapis.com/v1/token?key=" + API_KEY

        body = {
            "grant_type": "refresh_token",
            "refresh_token": self.refreshtoken
        }

        response = requests.post(url=url, data=body)
        jsonResponse = response.json()

        self.id_token = jsonResponse['id_token']

    def is_token_expired(self) -> bool:
        return time.time() > self.expiration_time

