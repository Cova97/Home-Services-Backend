import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("services\serviceshomebackend-firebase-admins.json")
firebase_admin.initialize_app(cred)