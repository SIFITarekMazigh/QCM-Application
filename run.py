import json
import random
import datetime

# Load or initialize the user data
try:
    with open("Login.json", 'r') as file:
        data = json.load(file)
except FileNotFoundError:
    data = {"users": []}
except json.JSONDecodeError:
    data = {"users": []}

# Load questions from questions.json
try:
    with open("questions.json", 'r', encoding='utf-8') as file:
        questions = json.load(file)
except FileNotFoundError:
    questions = {}
except json.JSONDecodeError:
    questions = {}

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

def play_quiz(topic, user):
    """Function to play the quiz."""
    topic_key = topic.capitalize()  # Ensure topic key is capitalized

    # Ensure the topic and difficulty exist in the questions data structure
    if topic.lower() not in questions:
        print(f"No questions available for the topic: {topic}.")
        return
    
    # Ensure that the selected difficulty is available
    difficulty_levels = ["easy", "medium", "hard"]
    difficulty = input(f"Select a difficulty level ({', '.join(difficulty_levels)}): ").strip().lower()
    if difficulty not in difficulty_levels:
        print("Invalid difficulty level. Please choose from easy, medium, or hard.")
        return
    
    # Fetch questions for the selected difficulty
    if difficulty not in questions[topic.lower()]:
        print(f"No questions available for {topic} at {difficulty} level.")
        return

    # Get the questions for the selected topic and difficulty
    topic_questions = questions[topic.lower()][difficulty]

    # Select n questions (number of questions to show)
    n = int(input(f"How many questions do you want to attempt? (Max {len(topic_questions)}): "))
    n = min(n, len(topic_questions))  # Make sure n doesn't exceed available questions

    # Ensure the topic exists in user's history, if not initialize it
    if topic_key not in user["history"]:
        user["history"][topic_key] = []

    score = 0
    for i in range(n):
        q = topic_questions[i]
        print(f"Question {i + 1}: {q['question']}")
        for option, text in q['choices'].items():
            print(f"   {option}. {text}")
        
        # Get the user's answer
        answer = input("Your answer (a, b, c, or d): ").strip().lower()
        
        # Validate the user's answer
        if answer not in ['a', 'b', 'c', 'd']:
            print("Invalid answer! Please select a valid option (a, b, c, or d).")
            continue
        
        # Check if the answer is correct
        if answer == q['correct_answer']:
            score += 1

    # Record the quiz history after the quiz ends
    from datetime import datetime
    quiz_date = datetime.now().strftime("%Y/%m/%d")
    quiz_time = datetime.now().strftime("%H:%M:%S")
    mark = f"{score}/{n}"
    
    history_entry = {
        "date": quiz_date,
        "time": quiz_time,
        "mark": mark,
        "difficulty": difficulty  # Add difficulty to history
    }

    # Add the quiz result to the user's history for the selected topic
    user["history"][topic_key].append(history_entry)

    # Save the updated data back to the file
    with open("Login.json", "w") as file:
        json.dump(data, file, indent=4)
    
    # Display the results
    print(f"\nQuiz completed! You scored {score}/{n}.")
    print(f"Date: {quiz_date}, Time: {quiz_time}")


def printHistory(user , topic):
    print()
    print("Your History : ")
    print()
    for u in user["history"][topic] :   
        print(u)
    print()

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
            print(f"\nYou selected: {selected_topic}")
            while True:
                print("\n1. View Scores")
                print("2. Play")
                print("3. Back")
                sub_choice = input("Enter your choice: ").strip()
                
                if sub_choice == '1':
                    printHistory(user , selected_topic)
                elif sub_choice == '2':
                    play_quiz(selected_topic, user)  # Pass the current_user here
                elif sub_choice == '3':
                    return
                else:
                    print("Invalid choice, please try again.")
        else:
            print("Invalid selection. Please try again.")
    except ValueError:
        print("Invalid input. Please enter a number.")


def main():
    """Main menu."""
    print("\nWelcome to the QCM System!")
    current_user = None
    while True:
        if not current_user:
            print("\n1. Login")
            print("2. Register")
            print("3. Exit")
        else:
            print("\n1. Select Topic")
            print("2. Logout")
            print("3. Exit")
        
        choice = input("Enter your choice: ").strip()
        
        if choice == '1':
            if current_user:
                select_topic(current_user)
            else:
                current_user = login()
        elif choice == '2':
            if current_user:
                current_user = None
                print("Logged out successfully.")
            else:
                register()
        elif choice == '3':
            print("Exiting the application. Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
