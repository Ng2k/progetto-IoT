import os

import firebase_admin
from firebase_admin import credentials, firestore

from .firestore.event import EventDataClass

cred = credentials.Certificate(os.getenv("FIREBASE_CONFIG_PATH"))
firebase_admin.initialize_app(cred)

db = firestore.client()
event = EventDataClass(
	stand_list=["stand1", "stand2"],
	start_date="2021-10-10",
	end_date="2021-10-12"
)
db.collection("users").document("user1").set(event)

print("Data written to Firestore")