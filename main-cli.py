import backend

backend = backend.Backend()

def login(org_type):
    id = input("Enter your id: ")
    if backend.check_user(id, org_type):
        password = input("Enter your password: ")
        if backend.validate_user(id, password, org_type):
            print("Login successful")
        else:
            print("Invalid password")
    else:  
        print("User not found. Please signup!")
        name = input("Enter your name: ")
        password = input("Enter your password: ")
        backend.add_user(id, name, password, org_type)
        print("User added successfully")
    return id

org_type = "restaurants"
# id = login(org_type)
backend.search_food('roti')
# backend.add_foods(id, {'roti': 10, 'sabzi': 5}, org_type)