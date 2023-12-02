import firebase_admin
from firebase_admin import db
import os

# we no longer need the path variable since we have instructed to rename the key file to key.json in README.md
# path = next((filename for filename in os.listdir("keys") if filename.startswith("foodforall-45f30")), None)
cred_object = firebase_admin.credentials.Certificate(os.path.join("keys", "key.json"))

firebase_admin.initialize_app(cred_object, {
          # databaseURL should be placed in keys/firebase_url.txt
          'databaseURL': open(os.path.join("keys", "firebase_url.txt"), 'r').read()
})

class Backend:
    def __init__(self):
        self.ref = db.reference('DB')

    # restaurant is the child node

    # def add_restaurant(self, rest_id, rest_name, foods, org_type):
    #     self.org_type_ref = self.ref.child(org_type)
    #     # create foods node
    #     self.foods_ref = self.org_type_ref.child(rest_id).child('foods')
    #     self.foods_ref.set(foods)

    def validate_user(self, id, password, org_type):
        self.users_ref = self.ref.child(org_type)
        return self.users_ref.child(id).get()['password'] == password

    def check_user(self, id, org_type):
        self.users_ref = self.ref.child(org_type)
        return self.users_ref.child(id).get() != None

    
    def add_user(self, id, name, password, org_type):
        self.users_ref = self.ref.child(org_type)
        self.users_ref.child(id).set({
            'name': name,
            'password': password
        })

    # add multiple foods with their quantities
    def add_foods(self, id, foods, org_type, action='add'):
        # if food already exists in node, action = update
        if self.list_foods(id, org_type) != None:
            action = 'update'
        if action == 'add':
            self.foods_ref = self.ref.child(org_type).child(id).child('foods')
            self.foods_ref.update(foods)
        elif action == 'remove':
            self.foods_ref = self.ref.child(org_type).child(id).child('foods')
            self.foods_ref.delete()
        elif action == 'update':
            # use list_foods to get the existing foods
            existing_foods = self.list_foods(id, org_type)
            for food in foods:
                if food in existing_foods:
                    existing_foods[food] += foods[food]
                else:
                    existing_foods[food] = foods[food]
            self.foods_ref = self.ref.child(org_type).child(id).child('foods')
            self.foods_ref.update(existing_foods)

    
    def list_all_foods(self):
        rest_list = self.ref.child('restaurants').get()
        food_data = {}
        for rest in rest_list:
            data = {}
            try:
                foods = self.list_foods(rest, 'restaurants')
                name = self.ref.child('restaurants').child(rest).get()['name']
            except:
                pass
            food_data[name] = foods
        return food_data
        
        

    def list_foods(self, id, org_type):
        self.foods_ref = self.ref.child(org_type).child(id).child('foods')
        return self.foods_ref.get()

    def search_food(self, food_name):
        rest_list = self.ref.child('restaurants').get()
        for rest in rest_list:
            try:
                foods = self.list_foods(rest, 'restaurants')
                if food_name in foods:
                    print(rest, foods[food_name])
            except:
                pass


# def search_food(food_name):
#     rest_list = backend.ref.child('restaurants').get()
#     for rest in rest_list:
#         try:
#             foods = backend.list_foods(rest, 'restaurants')
#             if food_name in foods:
#                 print(rest, foods[food_name])
#         except:
#             pass


if __name__ == "__main__":
    #id=login('restaurants')
    backend = Backend()

    search_food('roti')
# food_n=int(input("Enter the number of food items you want to add: "))
# foods={}
# for i in range(food_n):
#     food=input("Enter the food item: ")
#     quantity=int(input("Enter the quantity: "))
#     foods[food]=quantity


# backend.add_foods(id, foods, 'restaurants')





























# foods = {
#     food1: quantity1,
#     food2: quantity2
# }

# backend = Backend()
# backend.add_restaurant(rest_name, rest_id, foods)


