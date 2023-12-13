import pyrebase
import json

# rewriting backend.py using pyrebase instead of firebase_admin

class Backend:
    def __init__(self):
        with open('firebase_config.json') as f:
            config = json.load(f)
        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()
        self.auth = firebase.auth()

    def sign_in(self, email, password):
        try:
            user = self.auth.sign_in_with_email_and_password(email, password)
        except:
            return None
        return user

    def sign_up(self, email, password):
        user = self.auth.create_user_with_email_and_password(email, password)
        if user:
            uid = user['localId']
            # create user node with UID under NGO
            self.db.child("NGO").child(uid).set({
                'email': email
            })
            return user
        return None



if __name__ == "__main__":
    backend = Backend()
        