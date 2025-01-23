import json, subprocess
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, messagebox

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:.\assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Load existing user data
data = {"users": []}
try:
    with open("Login.json", "r") as file:
        data = json.load(file)
except FileNotFoundError:
    pass

# Register function
def register():
    username = entry_3.get().strip()
    password = entry_1.get().strip()
    confirm_password = entry_2.get().strip()

    # Validate inputs
    if not username or not password or not confirm_password:
        messagebox.showerror("Error", "All fields are required!")
        return

    # Check if username already exists
    for user in data["users"]:
        if username == user["name"]:
            messagebox.showerror("Error", "Username already exists. Please choose another username.")
            return

    # Check if passwords match
    if password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match!")
        return

    # Add new user
    new_user = {
        "name": username,
        "password": password,
        "history": {
            "physics": [],
            "mathematics": [],
            "computerscience": [],
            "electronics": [],
            "geography": [],
            "history": []
        }
    }
    data["users"].append(new_user)
    with open("Login.json", "w") as file:
        json.dump(data, file, indent=4)

    messagebox.showinfo("Success", f"Account successfully created for {username}!")
    subprocess.Popen(["python3", "C:.\gui\gui.py"])

    window.destroy()  # Close registration form
    # Optionally, you can call your login window here if needed.

# Tkinter GUI setup
window = Tk()
window.geometry("1200x920")
window.configure(bg="#050A24")

canvas = Canvas(
    window,
    bg="#050A24",
    height=920,
    width=1200,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
canvas.create_image(
    600.0,
    463.0,
    image=image_image_1
)

canvas.create_text(
    266.0,
    124.0,
    anchor="nw",
    text="Qcm Desktop Application",
    fill="#FFFFFF",
    font=("MontserratAlternates Bold", 48 * -1)
)

canvas.create_rectangle(
    278.0,
    269.0,
    922.0,
    780.0,
    fill="#FFFFFF",
    outline=""
)

canvas.create_text(
    473.0,
    287.0,
    anchor="nw",
    text="Welcome Among Us",
    fill="#000000",
    font=("MontserratAlternates Regular", 24 * -1)
)

canvas.create_text(
    401.0,
    401.0,
    anchor="nw",
    text="Username",
    fill="#000000",
    font=("MontserratAlternates Regular", 24 * -1)
)

canvas.create_text(
    401.0,
    496.0,
    anchor="nw",
    text="Password",
    fill="#000000",
    font=("MontserratAlternates Regular", 24 * -1)
)

canvas.create_text(
    401.0,
    594.0,
    anchor="nw",
    text="Confirm Password",
    fill="#000000",
    font=("MontserratAlternates Regular", 24 * -1)
)

canvas.create_text(
    495.0,
    332.0,
    anchor="nw",
    text="Register",
    fill="#000000",
    font=("MontserratAlternates Bold", 48 * -1)
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
canvas.create_image(
    603.0,
    551.0,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0,
    show="*"
)
entry_1.place(
    x=410.0,
    y=528.0,
    width=386.0,
    height=44.0
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
canvas.create_image(
    603.0,
    647.0,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0,
    show="*"
)
entry_2.place(
    x=410.0,
    y=624.0,
    width=386.0,
    height=44.0
)

entry_image_3 = PhotoImage(
    file=relative_to_assets("entry_3.png"))
canvas.create_image(
    603.0,
    455.0,
    image=entry_image_3
)
entry_3 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_3.place(
    x=410.0,
    y=432.0,
    width=386.0,
    height=44.0
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=register,
    relief="flat"
)
button_1.place(
    x=493.0,
    y=687.0,
    width=213.0,
    height=75.0
)
image_image_3 = PhotoImage(
    file=relative_to_assets("image_2copy.png"))
image_2 = canvas.create_image(
    151.0,
    158.0,
    image=image_image_3
)
window.resizable(False, False)
window.mainloop()
