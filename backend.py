import firebase_admin
from firebase_admin import db
import os

cred_object = firebase_admin.credentials.Certificate(os.path.join("keys","foodforall-45f30-firebase-adminsdk-9xuwc-34706f48e2.json"))

firebase_admin.initialize_app(cred_object, {
         'databaseURL': 'https://foodforall-45f30-default-rtdb.firebaseio.com'
})

class Backend:
    def __init__(self):
        self.ref = db.reference('DB')

    # restaurant is the child node

    def add_restaurant(self, rest_name, rest_id, foods):
        self.restaurants_ref = self.ref.child('restaurants')
        self.restaurants_ref.child(rest_name).child(rest_id).set(foods)

    def add_org(self, cust_name, cust_id, foods):
        self.customers_ref = self.ref.child('customers')
        self.customers_ref.child(cust_name).child(cust_id).set(foods)

    def add_food(self, food_name, food_id, quantity):
        self.foods_ref = self.ref.child('foods')
        self.foods_ref.child(food_name).child(food_id).set(quantity)

    def get_restaurant(self, rest_name):
        self.restaurants_ref = self.ref.child('restaurants')
        return self.restaurants_ref.child(rest_name).get()

    def get_org(self, cust_name):
        self.customers_ref = self.ref.child('customers')
        return self.customers_ref.child(cust_name).get()

    def get_food(self, food_name):
        self.foods_ref = self.ref.child('foods')
        return self.foods_ref.child(food_name).get()



# foods = {
#     food1: quantity1,
#     food2: quantity2
# }

# backend = Backend()
# backend.add_restaurant(rest_name, rest_id, foods)

