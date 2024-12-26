import json

try:
    with open("Login.json", 'r') as file:
        data = json.load(file)
except FileNotFoundError:
    data = {"users": []}
except json.JSONDecodeError:
    data = {"users": []}

def register():
    """Fonction pour enregistrer un nouvel utilisateur."""
    print("\nWelcome to the QCM System!")
    username = input("Enter your username: ").strip()
    
    for user in data["users"] :
        if username == user["name"] :
            print("Username already exists. Please choose another username.")
            return
    while True :
        password = input("Enter your password: ").strip()
        confirm_password = input("Confirm your password: ").strip()
        
        if password == confirm_password:
            break
        print("Passwords do not match. Please try again.")

    
    new_user = {
        "name":username,
        "password":password,
        "history":{
            "Physics": [],
            "Mathematics": [],
            "computer_science": [],           
            "electronics": [],
            "Geo": [],
            "history": []
    }
    }
    data["users"].append(new_user)
    with open("Login.json","w") as file :
        json.dump(data, file, indent=4)
    
    print(f"Account successfully created for {username}!")
    return

def login():
 """Fonction pour connecter un utilisateur existant."""
 s=0
 while s == 0 :
    username = input("Enter your username: ").strip()
    
    for user in data["users"] :
        if username == user["name"] :
             while True:
                password = input("Enter your password: ").strip()
                if user["password"] == password:
                    print(f"Welcome back, {username}!")
                    return
                else:
                    print("Invalid password. Please try again.")

    print("The username is invalid !") 


def main():
    """Menu principal."""
    print("\nWelcome to the QCM System!")
    while True:
        print("\n1. Login")
        print("2. Register")
        print("3. Exit")
        
        choice = input("Enter your choice: ").strip()
        
        if choice == '1':
            login()
        elif choice == '2':
            register()
        elif choice == '3':
            print("Exiting the application. Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
