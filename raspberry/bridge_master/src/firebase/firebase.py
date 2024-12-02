import os

import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate(os.getenv("FIREBASE_CONFIG_PATH"))
firebase_admin.initialize_app(cred)

db = firestore.client()
db.collection("users").document("user1").set({"name": "John Doe", "age": 30})

print("Data written to Firestore")