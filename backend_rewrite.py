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

    def sign_up(self, email, name, password, org_type='NGO'):
        user = self.auth.create_user_with_email_and_password(email, password)
        if user:
            uid = user['localId']
            # create user node with UID under NGO
            # self.db.child(f"{org_type}").child(uid).set({
            #     'email': email
            # })
            self.db.child(f"{org_type}").child(uid).set({
                'email': email,
                'name': name
            })
            return user
        return None

    def sign_in(self, email, password, org_type='NGO'):
        try:
            user = self.auth.sign_in_with_email_and_password(email, password)
            return user
        except:
            return None

    def add_foods(self, uid, foods, org_type = 'RESTAURANT', action='add'):
        # if food already exists in node, action = update
        if self.list_foods(uid, org_type) != None:
            action = 'update'
        if action == 'add':
            self.foods_ref = self.db.child(org_type).child(uid).child('foods')
            self.foods_ref.update(foods)
        elif action == 'remove':
            self.foods_ref = self.db.child(org_type).child(uid).child('foods')
            self.foods_ref.delete()
        elif action == 'update':
            # use list_foods to get the existing foods
            existing_foods = self.list_foods(uid, org_type)
            for food in foods:
                if food in existing_foods:
                    existing_foods[food] += foods[food]
                else:
                    existing_foods[food] = foods[food]
            self.foods_ref = self.db.child(org_type).child(uid).child('foods')
            self.foods_ref.update(existing_foods)

    def list_foods(self, uid, org_type = 'RESTAURANT'):
        try:
            foods = self.db.child(f"{org_type}").child(uid).child('foods').get().val()
            return dict(foods)
        except Exception as e:
            return None

    def list_all_foods(self, uid = None, org_type = 'RESTAURANT'):
        # format {id : {restaurant_name: {food1: quantity1, food2: quantity2}}}
        if uid == None:
            rest_list = self.db.child('RESTAURANT').get().val()
        else:
            print(uid)
            rest_list = {uid: self.db.child('RESTAURANT').child(uid).get().val()}
            print(rest_list)
            print(type(rest_list))
        food_data = {}
        for rest_id in rest_list:
            rest_name = rest_list[rest_id]['name']
            food_data[rest_id] = {rest_name: self.list_foods(rest_id)}
        return food_data

    def add_to_cart(self, ngo_uid, restaurant_uid, food_name, quantity):
        # check if food is available in restaurant
        # if yes, add to cart
        # if no, return -1
        # make cart node if it doesn't exist
        # food_name and quantity goes to cart node
        food_avail = int(self.list_foods(restaurant_uid)[food_name])
        if food_avail < int(quantity):
            return [food_avail]

    
        cart_data = self.db.child('NGO').child(ngo_uid).child('cart').child(restaurant_uid).get().val()

        if cart_data:
            if food_name in cart_data:
                cart_data[food_name] += quantity
            else:
                cart_data[food_name] = quantity

            # update cart data under restaurant_id
            self.db.child('NGO').child(ngo_uid).child('cart').child(restaurant_uid).update({food_name: cart_data[food_name]})
        else:
            self.db.child('NGO').child(ngo_uid).child('cart').child(restaurant_uid).update({food_name: quantity})

        return [-1, food_avail-quantity]

    def return_cart(self, ngo_uid):
        cart_data = self.db.child('NGO').child(ngo_uid).child('cart').get().val()
        return dict(cart_data)

    def update_cart(self, ngo_uid, restaurant_uid, food_name, quantity):
        cart_data = self.db.child('NGO').child(ngo_uid).child('cart').child(restaurant_uid).get().val()

        if quantity == 0:
            del cart_data[food_name]
        else:
            cart_data[food_name] = quantity

        self.db.child('NGO').child(ngo_uid).child('cart').child(restaurant_uid).update(cart_data)

    def place_order(self, ngo_uid):
        cart_data = self.db.child('NGO').child(ngo_uid).child('cart').get().val()
        for restaurant in cart_data:
            for food in cart_data[restaurant]:
                # create a node under restaurant>orders>ngo_uid
                self.db.child('RESTAURANT').child(restaurant).child('orders').child(ngo_uid).set(cart_data[restaurant])
        self.db.child('NGO').child(ngo_uid).child('cart').set(None)
        return True

    def approve_order(self, ngo_uid, restaurant_uid, food_name=None, quantity=None):
        # if food_name and quantity are None, approve all orders 
        if food_name == None and quantity == None:
            # TODO: checking if food is available in restaurant before approving
            # delete the node under restaurant>orders>ngo_uid
            # add to NGO>approved_orders>restaurant_uid
            self.db.child('RESTAURANT').child(restaurant_uid).child('orders').child(ngo_uid).set(None)
            self.db.child('NGO').child(ngo_uid).child('approved_orders').child(restaurant_uid).set(True)
        # check if food is still available in restaurant
        # if yes, approve order and decrement food quantity
        else:
            food_avail = self.list_foods(restaurant_uid)[food_name]
            if food_avail < quantity:
                return [food_avail]
            else:
                # decrement food quantity
                self.add_foods(restaurant_uid, {food_name: -quantity})
                # delete the node under restaurant>orders>ngo_uid
                # add to NGO>approved_orders>restaurant_uid
                self.db.child('RESTAURANT').child(restaurant_uid).child('orders').child(ngo_uid).set(None)
                self.db.child('NGO').child(ngo_uid).child('approved_orders').child(restaurant_uid).set(True)
        return -1
    
    def decline_order(self, ngo_uid, restaurant_uid):
        # delete the node under restaurant>orders>ngo_uid
        self.db.child('RESTAURANT').child(restaurant_uid).child('orders').child(ngo_uid).set(None)
        return True
    
    def get_name(self, uid, org_type='RESTAURANT'):
        return self.db.child(f"{org_type}").child(uid).child('name').get().val()
    
    def list_orders(self, uid, org_type='RESTAURANT'):
        return dict(self.db.child(f"{org_type}").child(uid).child('orders').get().val())