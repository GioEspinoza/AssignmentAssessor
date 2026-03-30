# CTk() = MAIN WINDOW
# CTkLabel() = LABEL (any text on screen)
# CTkentry() = Entry, user input.
# CTkButton() = Button, click to do something.
# pack() or grid() = how to put widgets on the screen.
# mainloop() = start the GUI event loop, keeps the window open.
import customtkinter as ctk

ctk.set_appearance_mode("dark")  # Set the appearance mode to dark
ctk.set_default_color_theme("blue")  # Set the default color theme to blue

app = ctk.CTk()  # Create the main application window
app.title("My First GUI")  # Set the window title
app.geometry("400x300")  # Set the window size

label = ctk.CTkLabel(app, text="Type your name below")  # Create a label widget
label.pack(pady=20)  # Add the label to the window with some padding

entry = ctk.CTkEntry(app)  # Create an entry widget for user input
entry.pack(pady=10)  # Add the entry widget to the window with some padding


def say_hello():
    name = entry.get()  # Get the text from the entry widget
    label.configure(text=f"Hello, {name}!")  # Update the label text to greet the user


button = ctk.CTkButton(
    app, text="Submit", command=say_hello
)  # Create a button that calls the say_hello function when clicked
button.pack(pady=10)  # Add the button to the window with some padding

app.mainloop()  # Start the GUI event loop
