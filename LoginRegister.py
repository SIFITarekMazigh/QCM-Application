import json

# Load or initialize the user data
try:
    with open("Login.json", 'r') as file:
        data = json.load(file)
except FileNotFoundError:
    data = {"users": []}
except json.JSONDecodeError:
    data = {"users": []}

def register():
    """Function to register a new user."""
    print("\nWelcome to the QCM System!")
    username = input("Enter your username: ").strip()
    
    for user in data["users"]:
        if username == user["name"]:
            print("Username already exists. Please choose another username.")
            return
    while True:
        password = input("Enter your password: ").strip()
        confirm_password = input("Confirm your password: ").strip()
        
        if password == confirm_password:
            break
        print("Passwords do not match. Please try again.")

    new_user = {
        "name": username,
        "password": password,
        "history": {
            "Physics": [],
            "Mathematics": [],
            "Computer Science": [],
            "Electronics": [],
            "Geography": [],
            "History": []
        }
    }
    data["users"].append(new_user)
    with open("Login.json", "w") as file:
        json.dump(data, file, indent=4)
    
    print(f"Account successfully created for {username}!")
    return

def login():
    """Function to log in an existing user."""
    while True:
        username = input("Enter your username: ").strip()
        for user in data["users"]:
            if username == user["name"]:
                while True:
                    password = input("Enter your password: ").strip()
                    if user["password"] == password:
                        print(f"Welcome back, {username}!")
                        return user  # Return the logged-in user's data
                    else:
                        print("Invalid password. Please try again.")
        print("The username is invalid!")

def select_topic(user):
    """Function to display and select topics."""
    print("\nSelect a topic:")
    topics = ["Physics", "Mathematics", "Computer Science"]
    for i, topic in enumerate(topics, start=1):
        print(f"{i}. {topic}")
    
    choice = input("Enter the number of the topic you want to select: ").strip()
    try:
        choice = int(choice)
        if 1 <= choice <= len(topics):
            selected_topic = topics[choice - 1]
            print(f"You selected: {selected_topic}")
            # Add additional functionality for selected topics if needed
            return
        else:
            print("Invalid selection. Please try again.")
    except ValueError:
        print("Invalid input. Please enter a number.")


