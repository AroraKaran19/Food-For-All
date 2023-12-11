from tkinter import *
from tkinter.messagebox import *
import os
import backend

food_list = {}
elements = []
check = backend.Backend()

def update_food_quantity(food_entry, quantity):
    food_entry.delete(0, END)
    food_entry.insert(0, quantity)

def show_foods_gui(rest_name, food_data, ngo_id=None, restaurant_id=None):
    # GUI to show Restaurant Name and Food Items as a label and Food Quantity in Entry
    root = Tk()
    root.title("FFA: Show Foods")
    root.geometry("800x800")
    root.resizable(False, False)

    canvas = Canvas(root, width=800, height=800, bg="#263D42")
    canvas.pack()

    title = Label(root, text=rest_name, bg="#263D42", fg="white", font=("Monolisa", 30, "bold"))
    canvas.create_window(400, 60, window=title)

    frame = LabelFrame(root, bg="white", height=500, width=700)
    canvas.create_window(400, 350, window=frame)

    frame_canvas = Canvas(frame, bg="white", width=700, height=500)
    frame_canvas.pack(side=LEFT)

    scroll_bar = Scrollbar(frame, orient="vertical", command=frame_canvas.yview)

    height = 100
    for food in food_data:
        food_label = Label(frame_canvas, text=f"{food.title()}: ", bg="white", fg="black", font=("Monolisa", 20, "bold"))
        frame_canvas.create_window(150, height, window=food_label)

        food_entry = Entry(frame_canvas, width=8, bg="white", fg="black", font=("Monolisa", 20, "bold"))
        food_entry.insert(0, food_data[food])
        frame_canvas.create_window(400, height, window=food_entry)
        
        def cart(food_name=food, food_quantity=food_entry):
            if food_quantity.get() not in ["", " "]:
                quantity = check.add_to_cart(ngo_id, restaurant_id, food_name, int(food_quantity.get())) # Adds the food items to the cart in DB
                if quantity[0] == -1:
                    update_food_quantity(food_quantity, quantity[1])
                else:
                    showinfo("(!) Invalid Quantity (!)", f"Sorry, but there are only {quantity[0]} {food_name} left!")
            else:
                showerror("(!) Invalid Quantity (!)", "Please enter a valid quantity!")
        
        add_order_button = Button(frame_canvas, text="Add to Order", bg="black", fg="white", font=("Monolisa", 10, "bold"), activebackground="black", activeforeground="white", command=cart)
        frame_canvas.create_window(550, height, window=add_order_button)
        height += 50

    frame_canvas.configure(yscrollcommand=scroll_bar.set)
    frame_canvas.bind("<Configure>", lambda e: frame_canvas.configure(scrollregion=frame_canvas.bbox("all")))
    scroll_bar.pack(side="right", fill="y")
    
    order_button = Button(root, text="Order", bg="black", fg="white", font=("Monolisa", 20, "bold"), activebackground="black", activeforeground="white")
    canvas.create_window(400, 700, window=order_button)

    root.eval('tk::PlaceWindow . center')
    root.mainloop()

def ngo_gui(id=None):
    root = Tk()
    root.title("FFA: NGO")
    root.geometry("800x800")
    root.resizable(False, False)

    canvas = Canvas(root, width=800, height=800, bg="#263D42")
    canvas.pack()

    title = Label(root, text="FoodForAll", bg="#263D42", fg="white", font=("Monolisa", 30, "bold"))
    canvas.create_window(400, 60, window=title)
    subtitle = Label(root, text="NGO", bg="#263D42", fg="white", font=("Monolisa", 15, "bold italic underline"))
    canvas.create_window(400, 100, window=subtitle)
    
    sub_heading = Label(root, text="Restaurant with Food", bg="#263D42", fg="white", font=("Monolisa", 22, "bold"))
    canvas.create_window(400, 200, window=sub_heading)

    # Food List
    frame = LabelFrame(root, bg="white", height=500, width=700)
    canvas.create_window(425, 500, window=frame)

    frame_canvas = Canvas(frame, bg="#263D42", width=700, height=500)
    frame_canvas.pack(side=LEFT)
    
    scroll_bar = Scrollbar(frame, orient="vertical", command=frame_canvas.yview)
    
    data = check.list_all_foods()
    food_data = {}
    for temp in data:
        food_data.update(data[temp])
    rest_data = {}
    restaurant_names, restaurant_ids = list(food_data.keys()), list(data.keys())
    for i in range(len(restaurant_ids)):
        rest_data[restaurant_ids[i]] = restaurant_names[i]
    height = 50
    for rest_id, restaurant_name in rest_data.items():
        def details(restaurant_n=restaurant_name, food_list=food_data[restaurant_name], restaurant_id=rest_id, ngo_id=id):
            show_foods_gui(restaurant_n, food_list, restaurant_id=restaurant_id, ngo_id=ngo_id)
        if food_data[restaurant_name] != None:
            restaurant = Button(frame_canvas, text=restaurant_name, fg="black", font=("Monolisa", 20, "bold"), bg="lime", activebackground="#263D42", activeforeground="white", command=details)
            frame_canvas.create_window(350, height, window=restaurant)
            height += 100
    
    frame_canvas.configure(yscrollcommand=scroll_bar.set)
    frame_canvas.bind("<Configure>", lambda e: frame_canvas.configure(scrollregion=frame_canvas.bbox("all")))
    scroll_bar.pack(side=RIGHT, fill="y")

    menu_frame = Frame(root, bg="white", width=50, height=800)
    canvas.create_window(0, 0, anchor=NW, window=menu_frame)

    menu_canvas = Canvas(menu_frame, width=50, height=800, bg="white")
    menu_canvas.pack()
    menu_canvas.bind("<Leave>", lambda event: menu(event, "close", menu_frame, menu_canvas, menu_button, logout=True, gui=root))

    menu_button = Button(menu_canvas, text="☰", bg="black", fg="white", font=("Monolisa", 20, "bold"), activebackground="black", activeforeground="white", command=lambda: menu(None, "open", menu_frame, menu_canvas, menu_button, logout=True, gui=root))
    if os.name == "nt":
        menu_canvas.create_window(26, 30, window=menu_button)
    else:
        menu_canvas.create_window(25, 20, window=menu_button)
    menu_button.bind("<Enter>", lambda event: menu(event, "open", menu_frame, menu_canvas, menu_button, logout=True, gui=root))

    setting_button = Button(menu_canvas, text="⚙", bg="black", fg="white", font=("Monolisa", 20, "bold"), activebackground="black", activeforeground="white")
    if os.name == "nt":
        menu_canvas.create_window(26, 80, window=setting_button)
    else:
        menu_canvas.create_window(25, 60, window=setting_button)
    
    root.protocol("WM_DELETE_WINDOW", lambda: on_close(root))
    root.eval('tk::PlaceWindow . center')
    root.mainloop()

def retrieve_credentials():
    if os.path.exists("credentials.txt"):
        with open("credentials.txt", "r") as file:
            id = file.readline().strip().replace("\n", "")
            org_type = file.readline().strip().replace("\n", "")
        return id, org_type

def on_close(gui):
    if askokcancel("Quit", "Are you sure you want to quit?"):
        gui.destroy()

def save(food_name, food_no):
    global food_count, food_list
    test = backend.Backend()
    id, org_type = retrieve_credentials()
    if food_count == 0:
        food_list[str(food_name.get())] = str(food_no.get())
    elif food_count > 0 and food_name.get() != "" and food_no.get() != "":
        food_list[str(food_name.get())] = str(food_no.get())
    test.add_foods(id, food_list, org_type)
    food_name.set("")
    food_no.set("")
    food_count = 0
    food_label.config(text=f"Food Count: {food_count}")
    food_list = {}
    showinfo("Success", "Your food items have been saved!")


def add_count(label, food_name, food_no):
    global food_count, food_list
    food_count += 1
    label.config(text=f"Food Count: {food_count}")
    food_list[str(food_name.get())] = str(food_no.get())
    food_name.set("")
    food_no.set("")


def restaurant_gui():
    global food_count, food_list, food_label
    root = Tk()
    root.title("FFA: Restaurant")
    root.geometry("800x800")
    root.resizable(False, False)

    canvas = Canvas(root, width=800, height=800, bg="#263D42")
    canvas.pack()

    title = Label(root, text="FoodForAll", bg="#263D42", fg="white", font=("Monolisa", 30, "bold"))
    canvas.create_window(400, 60, window=title)
    subtitle = Label(root, text="Restaurant", bg="#263D42", fg="white", font=("Monolisa", 15, "bold italic underline"))
    canvas.create_window(400, 100, window=subtitle)

    food_count = 0
    food_label = Label(root, text=f"Food Count: {food_count}", bg="#263D42", fg="white", font=("Monolisa", 20, "bold"))
    canvas.create_window(400, 200, window=food_label)

    food_item_label = Label(root, text="Food Item", bg="#263D42", fg="white", font=("Monolisa", 20, "bold"))
    canvas.create_window(400, 300, window=food_item_label)
    food_name = StringVar()
    food_item_entry = Entry(root, textvariable=food_name, width=15, bg="white", fg="black", font=("Monolisa", 20, "bold"))
    canvas.create_window(400, 350, window=food_item_entry)

    food_item_label = Label(root, text="Quantity", bg="#263D42", fg="white", font=("Monolisa", 20, "bold"))
    canvas.create_window(400, 400, window=food_item_label)
    food_no = StringVar()
    food_item_entry = Entry(root, textvariable=food_no, width=15, bg="white", fg="black", font=("Monolisa", 20, "bold"))
    canvas.create_window(400, 450, window=food_item_entry)

    add_new_button = Button(root, text="Add New", bg="black", fg="white", font=("Monolisa", 20, "bold"), activebackground="black", activeforeground="white", command=lambda: add_count(food_label, food_name.title(), food_no))                
    canvas.create_window(300, 550, window=add_new_button)

    save_button = Button(root, text="Save", bg="black", fg="white", font=("Monolisa", 20, "bold"), activebackground="black", activeforeground="white", command=lambda: save(food_name.title(), food_no))
    canvas.create_window(500, 550, window=save_button)

    menu_frame = Frame(root, bg="white", width=50, height=800)
    canvas.create_window(0, 0, anchor=NW, window=menu_frame)

    menu_canvas = Canvas(menu_frame, width=50, height=800, bg="white")
    menu_canvas.pack()
    menu_canvas.bind("<Leave>", lambda event: menu(event, "close", menu_frame, menu_canvas, menu_button, logout=True, gui=root))

    menu_button = Button(menu_canvas, text="☰", bg="black", fg="white", font=("Monolisa", 20, "bold"), activebackground="black", activeforeground="white", command=lambda: menu(None, "open", menu_frame, menu_canvas, menu_button, logout=True, gui=root))
    if os.name == "nt":
        menu_canvas.create_window(26, 30, window=menu_button)
    else:
        menu_canvas.create_window(25, 20, window=menu_button)
    menu_button.bind("<Enter>", lambda event: menu(event, "open", menu_frame, menu_canvas, menu_button, logout=True, gui=root))

    setting_button = Button(menu_canvas, text="⚙", bg="black", fg="white", font=("Monolisa", 20, "bold"), activebackground="black", activeforeground="white")
    if os.name == "nt":
        menu_canvas.create_window(26, 80, window=setting_button)
    else:
        menu_canvas.create_window(25, 60, window=setting_button)

    root.eval('tk::PlaceWindow . center')
    root.protocol("WM_DELETE_WINDOW", lambda: on_close(root))
    root.mainloop()

def user_validation(id, password, org_type, gui=None):
    if gui != None:
        gui.destroy()
    if id.strip() != "" and password.strip() != "":
        if check.check_user(id, org_type):
            try:
                if check.validate_user(id, password, org_type):
                    if org_type == "restaurants":
                        with open("credentials.txt", "w") as file:
                            file.write(f"{id}\n{org_type}")
                        restaurant_gui()
                    elif org_type == "ngo":
                        ngo_gui(id)
                else:
                    showerror("Error", "Invalid Credentials!\nPlease try again!")
                    login("login", id)
            except Exception as e:
                showerror("Error", str(e))
        else:
            ask = askokcancel("User Not Found", "User not found!\nDo you want to register?")
            if ask:
                login("register", id)
            else:
                main_menu()
    else:
        if id == "" and password == "":
            showerror("Error", "Please enter all details!")
        elif id == "":
            showerror("Error", "Please enter your id!")
        elif password == "":
            showerror("Error", "Please enter your password!")
        if id != "":
            login("login", id)
        else:
            login("login")

def user_registration(name, id, password, org_type, gui):
    check = backend.Backend()
    registeration = check.add_user(id, name, password, org_type)
    if registeration:
        showinfo("Success", "User Registered Successfully!")
        gui.destroy()
        user_validation(id, password, org_type)
    else:
        showerror("Error", "User already exists!")
        login("register", id)

def show_selected(org_type):
    showinfo("Selected", f"Selected: {org_type.get().upper()}")
    
def menu(event, opt, frame, canvas, button, elements=[], logout=False, gui=None):
    if opt == "open":
        try:
            frame.config(width=200)
            canvas.config(width=200)
            button.config(text="X")
            if os.name == "nt":
                button.config(padx=10)
            menu_title = Label(canvas, text="Menu", bg="white", fg="black", font=("Monolisa", 20, "bold underline"))
            if os.name == "nt":
                canvas.create_window(120, 60, window=menu_title)
            else:
                canvas.create_window(100, 60, window=menu_title)
            if logout:
                if os.name == "nt":
                    logout_button = Button(canvas, text="Logout", bg="red", fg="white", font=("Monolisa", 15, "bold"), activebackground="black", activeforeground="white", command=lambda: (gui.destroy(), login(method="login")), pady=18, padx=20)
                    canvas.create_window(100, 200, window=logout_button)
                else:
                    logout_button = Button(canvas, text="Logout", bg="red", fg="white", font=("Monolisa", 20, "bold"), activebackground="black", activeforeground="white", command=lambda: (gui.destroy(), main_menu()))
                    canvas.create_window(100, 200, window=logout_button)
                elements.append(logout_button)       
            elements.append(menu_title)
            if logout:
                button.config(command=lambda: menu(None, "close", frame, canvas, button, elements, logout=True, gui=gui))
            else:
                button.config(command=lambda: menu(None, "close", frame, canvas, button, elements, logout=False, gui=gui))
        except:
            pass
    else:
        frame.config(width=50)
        canvas.config(width=50)
        button.config(text="☰")
        if logout:
            button.config(command=lambda: menu(None, "open", frame, canvas, button, logout=True, gui=gui))
        else:
            button.config(command=lambda: menu(None, "open", frame, canvas, button, logout=False, gui=gui))
        if len(elements) != 0:
            for ele in elements:
                try:
                    ele.destroy()
                except:
                    pass
            elements = []

def login(method, prev=None):
    login_gui = Tk()
    login_gui.title("FFA: Login")
    login_gui.geometry("800x800")
    login_gui.resizable(False, False)

    canvas = Canvas(login_gui, width=800, height=800, bg="#263D42")
    canvas.pack()

    title = Label(login_gui, text="FoodForAll", bg="#263D42", fg="white", font=("Monolisa", 30, "bold"))
    canvas.create_window(400, 60, window=title)

    back_button = Button(login_gui, text="←", bg="black", fg="white", font=("Monolisa", 20, "bold"), padx=10, activebackground="black", activeforeground="white", command=lambda: (login_gui.destroy(), main_menu()))
    canvas.create_window(50, 40, window=back_button)

    org_type_label = Label(login_gui, text="Organization Type", bg="#263D42", fg="white", font=("Monolisa", 20, "bold"))
    canvas.create_window(400, 200, window=org_type_label)
    
    org_type = StringVar()
    org_type_radio1 = Radiobutton(login_gui, text="Restaurants", variable=org_type, value="restaurants", bg="#263D42", fg="white", font=("Monolisa", 20, "bold"))
    org_type.set("restaurants")
    canvas.create_window(330, 250, window=org_type_radio1)
    org_type_radio2 = Radiobutton(login_gui, text="NGO", variable=org_type, value="ngo", bg="#263D42", fg="white", font=("Monolisa", 20, "bold"))
    canvas.create_window(530, 250, window=org_type_radio2)
    org_type.trace("w", lambda *args: show_selected(org_type))

    if method == "login":
        subtitle = Label(login_gui, text="Login", bg="#263D42", fg="white", font=("Monolisa", 15, "bold italic underline"))
        canvas.create_window(400, 100, window=subtitle)

        register_button = Button(login_gui, text="Register", bg="black", fg="white", font=("Monolisa", 20, "bold"), activebackground="black", activeforeground="white", command=lambda: (login_gui.destroy(), login("register")))
        canvas.create_window(700, 40, window=register_button)
    else:
        login_gui.title("FFA: Register")
        subtitle = Label(login_gui, text="Register", bg="#263D42", fg="white", font=("Monolisa", 15, "bold italic underline"))
        canvas.create_window(400, 100, window=subtitle)
        name = StringVar()
        name_label = Label(login_gui, text="Name", bg="#263D42", fg="white", font=("Monolisa", 20, "bold"))
        canvas.create_window(400, 300, window=name_label)
        name_entry = Entry(login_gui, textvariable=name, width=15, bg="white", fg="black", font=("Monolisa", 20, "bold"))
        canvas.create_window(400, 350, window=name_entry)

    id_label = Label(login_gui, text="ID", bg="#263D42", fg="white", font=("Monolisa", 20, "bold"))
    canvas.create_window(400, 400, window=id_label)
    id = StringVar()
    if prev != None:
        id.set(prev)
    id_entry = Entry(login_gui, textvariable=id, width=15, bg="white", fg="black", font=("Monolisa", 20, "bold"))
    canvas.create_window(400, 450, window=id_entry)

    password_label = Label(login_gui, text="Password", bg="#263D42", fg="white", font=("Monolisa", 20, "bold"))
    canvas.create_window(400, 500, window=password_label)
    password = StringVar()
    password_entry = Entry(login_gui, textvariable=password, width=15, bg="white", fg="black", font=("Monolisa", 20, "bold"), show="*")
    canvas.create_window(400, 550, window=password_entry)

    if method == "login":
        login_button = Button(login_gui, text="Login", bg="black", fg="white", font=("Monolisa", 20, "bold"), activebackground="black", activeforeground="white", command=lambda: user_validation(str(id.get()), str(password.get()), str(org_type.get()), login_gui))
        if os.name == "nt":
            canvas.create_window(400, 620, window=login_button)
        else:
            canvas.create_window(400, 620, window=login_button)
    else:
        register_button = Button(login_gui, text="Register", bg="black", fg="white", font=("Monolisa", 20, "bold"), activebackground="black", activeforeground="white", command= lambda: user_registration(str(name.get()), str(id.get()), str(password.get()), str(org_type.get()), login_gui))
        canvas.create_window(400, 620, window=register_button)

    login_gui.eval('tk::PlaceWindow . center')
    login_gui.mainloop()

def main_menu():
    root = Tk()
    root.title("FFA: Main Menu")
    root.geometry("800x800")
    root.resizable(False, False)

    canvas = Canvas(root, width=800, height=800, bg="#263D42")
    canvas.pack()

    title = Label(root, text="FoodForAll", bg="#263D42", fg="white", font=("Monolisa", 30, "bold"))
    canvas.create_window(400, 80, window=title)

    image_logo = PhotoImage(file="res/help_image.png")
    logo = Label(root, image=image_logo, bg="#263D42")
    canvas.create_window(400, 300, window=logo)

    if os.name == "nt":
        login_button = Button(canvas, text="Login", bg="black", fg="white", font=("Monolisa", 25, "bold"), activebackground="black", activeforeground="white", command=lambda: (root.destroy(), login("login")), pady=18, padx=20)
        canvas.create_window(400, 500, window=login_button)
        
        exit_button = Button(canvas, text="Exit", bg="black", fg="white", font=("Monolisa", 25, "bold"), activebackground="black", activeforeground="white", command=lambda: root.destroy(), pady=18, padx=30)
        canvas.create_window(400, 650, window=exit_button)
    
    else:
        login_button = Button(canvas, text="Login", bg="black", fg="white", font=("Monolisa", 25, "bold"), activebackground="black", activeforeground="white", command=lambda: (root.destroy(), login("login")), pady=25, padx=25)
        canvas.create_window(400, 500, window=login_button)

        exit_button = Button(canvas, text="Exit", bg="black", fg="white", font=("Monolisa", 25, "bold"), activebackground="black", activeforeground="white", command=lambda: root.destroy(), pady=25, padx=25)
        canvas.create_window(400, 650, window=exit_button)

    menu_frame = Frame(root, bg="white", width=50, height=800)
    canvas.create_window(0, 0, anchor=NW, window=menu_frame)

    menu_canvas = Canvas(menu_frame, width=50, height=800, bg="white")
    menu_canvas.pack()
    menu_canvas.bind("<Leave>", lambda event: menu(event, "close", menu_frame, menu_canvas, menu_button))

    menu_button = Button(menu_canvas, text="☰", bg="black", fg="white", font=("Monolisa", 20, "bold"), activebackground="black", activeforeground="white", command=lambda: menu(None, "open", menu_frame, menu_canvas, menu_button))
    if os.name == "nt":
        menu_canvas.create_window(26, 30, window=menu_button)
    else:
        menu_canvas.create_window(25, 20, window=menu_button)
    menu_button.bind("<Enter>", lambda event: menu(event, "open", menu_frame, menu_canvas, menu_button))

    setting_button = Button(menu_canvas, text="⚙", bg="black", fg="white", font=("Monolisa", 20, "bold"), activebackground="black", activeforeground="white")
    if os.name == "nt":
        menu_canvas.create_window(26, 80, window=setting_button)
    else:
        menu_canvas.create_window(25, 60, window=setting_button)

    root.eval('tk::PlaceWindow . center')
    root.protocol("WM_DELETE_WINDOW", lambda: on_close(root))
    root.mainloop()


main_menu()