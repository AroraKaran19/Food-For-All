from tkinter import *
from tkinter.messagebox import *
import os
import backend

food_count = 0
food_list = {}

def ngo_gui():
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

    frame = LabelFrame(root, bg="white", height=500, width=700)
    canvas.create_window(425, 500, window=frame)

    frame_canvas = Canvas(frame, bg="white", width=700, height=500)
    frame_canvas.pack()

    scroll_bar = Scrollbar(frame, orient="vertical", command=frame_canvas.yview)
    scroll_bar.pack(side=RIGHT, fill="y")
    frame_canvas.configure(yscrollcommand=scroll_bar.set)
    frame_canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=frame_canvas.bbox("all")))

    menu_frame = Frame(root, bg="white", width=50, height=800)
    canvas.create_window(0, 0, anchor=NW, window=menu_frame)

    menu_canvas = Canvas(menu_frame, width=50, height=800, bg="white")
    menu_canvas.pack()
    menu_canvas.bind("<Leave>", lambda event: menu(event, "close", menu_frame, menu_canvas, menu_button, logout=True, gui=root))

    menu_button = Button(menu_canvas, text="☰", bg="black", fg="white", font=("Monolisa", 20, "bold"), activebackground="black", activeforeground="white", command=lambda: menu(None, "open", menu_frame, menu_canvas, menu_button, logout=True, gui=root))
    menu_canvas.create_window(25, 20, window=menu_button)
    menu_button.bind("<Enter>", lambda event: menu(event, "open", menu_frame, menu_canvas, menu_button, logout=True, gui=root))

    setting_button = Button(menu_canvas, text="⚙", bg="black", fg="white", font=("Monolisa", 20, "bold"), activebackground="black", activeforeground="white")
    menu_canvas.create_window(25, 60, window=setting_button)

    root.protocol("WM_DELETE_WINDOW", lambda: on_close(root))
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
    showinfo("Success", "Your food items have been saved!")


def add_count(label, food_name, food_no):
    global food_count, food_list
    food_count += 1
    label.config(text=f"Food Count: {food_count}")
    food_list[str(food_name.get())] = str(food_no.get())
    food_name.set("")
    food_no.set("")


def restaurant_gui():
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

    add_new_button = Button(root, text="Add New", bg="black", fg="white", font=("Monolisa", 20, "bold"), activebackground="black", activeforeground="white", command=lambda: add_count(food_label, food_name, food_no))                
    canvas.create_window(300, 550, window=add_new_button)

    save_button = Button(root, text="Save", bg="black", fg="white", font=("Monolisa", 20, "bold"), activebackground="black", activeforeground="white", command=lambda: save(food_name, food_no))
    canvas.create_window(500, 550, window=save_button)

    menu_frame = Frame(root, bg="white", width=50, height=800)
    canvas.create_window(0, 0, anchor=NW, window=menu_frame)

    menu_canvas = Canvas(menu_frame, width=50, height=800, bg="white")
    menu_canvas.pack()
    menu_canvas.bind("<Leave>", lambda event: menu(event, "close", menu_frame, menu_canvas, menu_button, logout=True, gui=root))

    menu_button = Button(menu_canvas, text="☰", bg="black", fg="white", font=("Monolisa", 20, "bold"), activebackground="black", activeforeground="white", command=lambda: menu(None, "open", menu_frame, menu_canvas, menu_button, logout=True, gui=root))
    menu_canvas.create_window(25, 20, window=menu_button)
    menu_button.bind("<Enter>", lambda event: menu(event, "open", menu_frame, menu_canvas, menu_button, logout=True, gui=root))

    setting_button = Button(menu_canvas, text="⚙", bg="black", fg="white", font=("Monolisa", 20, "bold"), activebackground="black", activeforeground="white")
    menu_canvas.create_window(25, 60, window=setting_button)

    root.eval('tk::PlaceWindow . center')
    root.protocol("WM_DELETE_WINDOW", lambda: on_close(root))
    root.mainloop()

def user_validation(id, password, org_type, gui=None):
    if gui != None:
        gui.destroy()
    if id != "" or password != "":
        check = backend.Backend()
        if check.check_user(id, org_type):
            if check.validate_user(id, password, org_type):
                if org_type == "restaurants":
                    with open("credentials.txt", "w") as file:
                        file.write(f"{id}\n{org_type}")
                    restaurant_gui()
                elif org_type == "ngo":
                    ngo_gui()
            else:
                showerror("Error", "Invalid Credentials!\nPlease try again!")
        else:
            ask = askokcancel("User Not Found", "User not found!\nDo you want to register?")
            if ask:
                login("register", id)
            else:
                main_menu()
    else:
        showerror("Error", "Please enter all the details!")

def user_registration(name, id, password, org_type, gui):
    check = backend.Backend()
    check.add_user(id, name, password, org_type)
    showinfo("Success", "User Registered Successfully!")
    gui.destroy()
    user_validation(id, password, org_type)

def show_selected(org_type):
    showinfo("Selected", f"Selected: {org_type.get()}")

def login(method, prev=None):
    login_gui = Tk()
    login_gui.title("FFA: Login")
    login_gui.geometry("800x800")
    login_gui.resizable(False, False)

    canvas = Canvas(login_gui, width=800, height=800, bg="#263D42")
    canvas.pack()

    title = Label(login_gui, text="FoodForAll", bg="#263D42", fg="white", font=("Monolisa", 30, "bold"))
    canvas.create_window(400, 60, window=title)

    back_button = Button(login_gui, text="←", bg="black", fg="white", font=("Monolisa", 20, "bold"), activebackground="black", activeforeground="white", command=lambda: (login_gui.destroy(), main_menu()))
    canvas.create_window(25, 25, window=back_button)

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
        canvas.create_window(700, 25, window=register_button)
    else:
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
        canvas.create_window(400, 600, window=login_button)
    else:
        register_button = Button(login_gui, text="Register", bg="black", fg="white", font=("Monolisa", 20, "bold"), activebackground="black", activeforeground="white", command= lambda: user_registration(str(name.get()), str(id.get()), str(password.get()), str(org_type.get()), login_gui))
        canvas.create_window(400, 600, window=register_button)

    login_gui.eval('tk::PlaceWindow . center')
    login_gui.mainloop()

def menu(event, opt, frame, canvas, button, elements=[], logout=False, gui=None):
    if opt == "open":
        try:
            frame.config(width=200)
            canvas.config(width=200)
            button.config(text="X")
            menu_title = Label(canvas, text="Menu", bg="white", fg="black", font=("Monolisa", 20, "bold underline"))
            canvas.create_window(100, 60, window=menu_title)
            elements.append(menu_title)
            if logout:
                logout_button = Button(canvas, text="Logout", bg="red", fg="white", font=("Monolisa", 20, "bold"), activebackground="black", activeforeground="white", command=lambda: (gui.destroy(), main_menu()))
                canvas.create_window(100, 100, window=logout_button)
                elements.append(logout_button)
            button.config(command=lambda: menu(None, "close", frame, canvas, button, elements, logout))
        except:
            pass
    else:
        frame.config(width=50)
        canvas.config(width=50)
        button.config(text="☰")
        if elements != []:
            for ele in elements:
                ele.destroy()
        button.config(command=lambda: menu(None, "open", frame, canvas, button, logout=logout))

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
    menu_canvas.create_window(25, 20, window=menu_button)
    menu_button.bind("<Enter>", lambda event: menu(event, "open", menu_frame, menu_canvas, menu_button))

    setting_button = Button(menu_canvas, text="⚙", bg="black", fg="white", font=("Monolisa", 20, "bold"), activebackground="black", activeforeground="white")
    menu_canvas.create_window(25, 60, window=setting_button)

    root.eval('tk::PlaceWindow . center')
    root.protocol("WM_DELETE_WINDOW", lambda: on_close(root))
    root.mainloop()

if __name__ == "__main__":
    main_menu()   
