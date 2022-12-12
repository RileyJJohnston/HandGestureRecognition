import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
import datetime

# Fetch the service account key JSON file contents
cred = credentials.Certificate("smarthome-4feea-firebase-adminsdk-200yx-9ea93a1af6.json")

# Initialize the app with a service account, granting admin privileges
app = firebase_admin.initialize_app(cred, {
    'storageBucket': 'smarthome-4feea.appspot.com',
}, name='storage')

bucket = storage.bucket(app=app)
blob = bucket.blob("profilePictures/profile_johnstonriley1@gmail.com") #TODO: don't hardcode the file name. Use this to fetch any arbitrary file from Firebase

url = blob.generate_signed_url(datetime.timedelta(seconds=300), method='GET')

print(url)

