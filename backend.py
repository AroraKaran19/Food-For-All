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
        if self.check_user(id, org_type):
            print("User already exists")
            return False
        self.users_ref = self.ref.child(org_type)
        self.users_ref.child(id).set({
            'name': name,
            'password': password
        })
        print("User added successfully")
        return True

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

    
    def list_all_foods(self, rest_id=None):
        rest_list = self.ref.child('restaurants').get()
        food_data = {}
        # format {id : {restaurant_name: {food1: quantity1, food2: quantity2}}}
        if rest_id != None:
            # return food data of a particular restaurant
            try:
                foods = self.list_foods(rest_id, 'restaurants')
                name = self.ref.child('restaurants').child(rest_id).get()['name']
                food_data[rest_id] = {name: foods}
            except:
                pass
        else:
            for rest in rest_list:
                try:
                    foods = self.list_foods(rest, 'restaurants')
                    name = self.ref.child('restaurants').child(rest).get()['name']
                except:
                    pass
                food_data[rest] = {name: foods}
                # print(food_data)
        return food_data
        
    def list_foods(self, id, org_type):
        self.foods_ref = self.ref.child(org_type).child(id).child('foods')
        # output looks like {'food1': quantity1, 'food2': quantity2}
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

    # def add_to_cart(self, ngo_id, restaurant_id, food_name, quantity):
    #     # make cart node if it doesn't exist
    #     # food_name and quantity goes to cart node
        
    #     food_data = self.list_all_foods(restaurant_id)
    #     # food data is in the format {id : {restaurant_name: {food1: quantity1, food2: quantity2}}}

    #     self.ngo_ref = self.ref.child('ngo').child(ngo_id)

    #     # if cart node doesn't exist, create it
    #     if self.ngo_ref.child('cart').get() == None:
    #         self.ngo_ref.child('cart').set({})

    #     # if node with restaurant_id doesn't exist in cart node, create it
    #     if self.ngo_ref.child('cart').child(restaurant_id).get() == None:
    #         self.ngo_ref.child('cart').child(restaurant_id).set({})

        
    #     food_avail = food_data[restaurant_id].values().__iter__().__next__()[food_name]
    #     if food_avail < quantity:
    #         return food_avail
        
    #     # add food to cart
    #     # increment quantity if food already exists in cart

    #     # get cart data
    #     cart_data = self.ngo_ref.child('cart').get()
    #     if food_name in cart_data:
    #         cart_data[food_name] += quantity
    #     else:
    #         cart_data[food_name] = quantity

    #     # update cart data under restaurant_id
    #     self.ngo_ref.child('cart').child(restaurant_id).update(cart_data)


    #     return -1

    def add_to_cart(self, ngo_id, restaurant_id, food_name, quantity):
    # make cart node if it doesn't exist
    # food_name and quantity goes to cart node
    
        food_data = self.list_all_foods(restaurant_id)
        # food data is in the format {id : {restaurant_name: {food1: quantity1, food2: quantity2}}}

        self.ngo_ref = self.ref.child('ngo').child(ngo_id)

        # if cart node doesn't exist, create it
        if self.ngo_ref.child('cart').get() is None:
            print("cart node doesn't exist.. creating it")
            # set cart with a restaurant_id node
            self.ngo_ref.child('cart').set({restaurant_id: {food_name: quantity}})

        # if node with restaurant_id doesn't exist in cart node, create it and add food
        elif self.ngo_ref.child('cart').child(restaurant_id).get() is None:
            self.ngo_ref.child('cart').child(restaurant_id).set({food_name: quantity})

        else: 
            food_avail = food_data[restaurant_id].values().__iter__().__next__()[food_name]
            if int(food_avail) < quantity:
                return [food_avail]

            # add food to cart
            # increment quantity if food already exists in cart

            # get cart data
            cart_data = self.ngo_ref.child('cart').child(restaurant_id).get()

            if food_name in cart_data:
                cart_data[food_name] += quantity
            else:
                cart_data[food_name] = quantity

            # update cart data under restaurant_id
            self.ngo_ref.child('cart').child(restaurant_id).update({food_name: cart_data[food_name]})

        return [-1, food_avail-quantity]

    def return_cart (self, ngo_id):
        # return in format {rest_id: {food_name: food_quantity}
        # node structure is {ngo_id: {cart: {rest_id: {food_name: food_quantity}}}}
        cart_data = self.ref.child('ngo').child(ngo_id).child('cart').get()
        return cart_data
        
        

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

    #search_food('roti')
    # backend.list_foods("0431", 'restaurants')
    # print(backend.list_all_foods("0431"))
    add_to_cart_status = backend.add_to_cart("0001", "0431", "potato", 100)
    print(add_to_cart_status)

    print(backend.return_cart('0001'))


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


