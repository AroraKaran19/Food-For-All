from tkinter import *
from tkinter import messagebox
import os

database_name = "logininfo.db"
table_name = "login"

def on_close(gui):
    if messagebox.askokcancel("Quit", "Are you sure you want to quit?"):
        gui.destroy()

def login():
    print("Login")

def menu(event, opt, frame, canvas, button, elements=[]):
    if opt == "open":
        frame.config(width=200)
        canvas.config(width=200)
        button.config(text="X")
        menu_title = Label(canvas, text="Menu", bg="white", fg="black", font=("Monolisa", 20, "bold underline"))
        canvas.create_window(100, 60, window=menu_title)
        elements.append(menu_title)
        button.config(command=lambda: menu(None, "close", frame, canvas, button, elements))

    else:
        frame.config(width=50)
        canvas.config(width=50)
        button.config(text="☰")
        button.config(command=lambda: menu(None, "open", frame, canvas, button))
        for ele in elements:
            ele.destroy()

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

    login_button = Button(canvas, text="Login", bg="black", fg="white", font=("Monolisa", 25, "bold"), activebackground="black", activeforeground="white", command=login, pady=25, padx=25)
    canvas.create_window(400, 500, window=login_button)

    exit_button = Button(canvas, text="Exit", bg="black", fg="white", font=("Monolisa", 25, "bold"), activebackground="black", activeforeground="white", command=lambda: on_close(root), pady=25, padx=25)
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