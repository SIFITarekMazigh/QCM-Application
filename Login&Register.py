
users_db = {}


modules = ["Computer Science", "Mathematics", "Physics", "History", "Englais"]

def register():
    """Fonction pour enregistrer un nouvel utilisateur."""
    print("\nWelcome to the QCM System!")
    username = input("Enter your username: ").strip()
    
    if username in users_db:
        print("Username already exists. Please choose another username.")
        return
    while True :
        password = input("Enter your password: ").strip()
        confirm_password = input("Confirm your password: ").strip()
        
        if password == confirm_password:
            break
        print("Passwords do not match. Please try again.")

    
    users_db[username] = password
    print(f"Account successfully created for {username}!")

def login():
    """Fonction pour connecter un utilisateur existant."""
    print("\nWelcome to the QCM System!")
    username = input("Enter your username: ").strip()
    
    if username not in users_db:
        print("Username not found. Please register first.")
        return
    while True:
        password = input("Enter your password: ").strip()
        if users_db[username] == password:
            print(f"Welcome back, {username}!")
            choose_module(username)
            break
        else:
            print("Invalid password. Please try again.")
            

def choose_module(username):
    """Permet à l'utilisateur de choisir un module après connexion."""
    print(f"\nHello {username}, please choose a module to start:")
    for i, module in enumerate(modules, start=1):
        print(f"{i}. {module}")
    
    choice = input("Enter the number of your choice: ").strip()
    
    if choice.isdigit() and 1 <= int(choice) <= len(modules):
        selected_module = modules[int(choice) - 1]
        print(f"\nYou have selected the {selected_module} module.")
        start_qcm(selected_module)
    else:
        print("Invalid choice. Please try again.")
        choose_module(username)

def start_qcm(module):
    """Démarre le QCM pour un module donné."""
    print(f"\nStarting the QCM for {module}...")
    print("QCM is under development. Stay tuned for updates!")

def main():
    """Menu principal."""
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
