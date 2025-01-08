import json
import random
import datetime
import time
import csv

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
    
    print("\nSelect a difficulty level:")
    for i, level in enumerate(difficulty_levels):
        print(f"{i+1}. {level.capitalize()}")

    try:
        difficulty_choice = int(input("Enter the number of your chosen difficulty: ").strip())
        
        if not 1 <= difficulty_choice <= len(difficulty_levels):
            print("Invalid choice. Please select a valid number.")
            return
        
        difficulty = difficulty_levels[difficulty_choice - 1]
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return
        
    #if difficulty not in difficulty_levels:
        #print("Invalid difficulty level. Please choose from easy, medium, or hard.")
        #return
    
    # Fetch questions for the selected difficulty
    if difficulty not in questions[topic.lower()]:
        print(f"No questions available for {topic} at {difficulty} level.")
        return

    if difficulty == "easy" :
        time_par_qst = 20
    elif difficulty == "medium" :
        time_par_qst = 40
    else :
        time_par_qst = 60
    # Get the questions for the selected topic and difficulty
    topic_questions = questions[topic.lower()][difficulty]

    # Select n questions (number of questions to show)
    n = int(input(f"How many questions do you want to attempt? (Max {len(topic_questions)}): "))
    n = min(n, len(topic_questions))  # Make sure n doesn't exceed available questions

    # Ensure the topic exists in user's history, if not initialize it
    if topic_key not in user["history"]:
        user["history"][topic_key] = []



    # Temps total pour le quiz (en secondes)
    total_time = n * time_par_qst  # Par exemple, 20 questions * 40s par question = 800s
    start_time = time.time()
    end_time = start_time + total_time

    # Calculer et afficher le temps total sous format HH:MM:SS
    hours, remainder = divmod(total_time, 3600)
    minutes, seconds = divmod(remainder, 60)
    print(f"\nYou have {hours:02d}:{minutes:02d}:{seconds:02d} to complete the quiz.")


    score = 0
    for i in range(n):

        # calculer le temps restant
        remaining_time = int(end_time - time.time())
        if remaining_time <= 0:
            print("\nTime's up! The quiz has ended.")
            break

        # afficher le temps restant 
        hours, remainder = divmod(remaining_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        print(f"\nTime left: {hours:02d}:{minutes:02d}:{seconds:02d}")

        # choisir la question
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
        
        if time.time() > end_time:
            print("\nTime's up! The quiz has ended.")
            break

        # Check if the answer is correct
        if answer == q['correct_answer']:
            score += 1
            print("Correct Answer")
        else :
            print("Incorrect Answer !")


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




def export_results(user, topic):
    if not user["history"].get(topic):
        print(f"No history available for the topic: {topic}")
        return

    print("\nChoose export format:")
    print("1. Text file (.txt)")
    print("2. CSV file (.csv)")
    format_choice = input("Enter your choice: ").strip()

    filename = f"{user['name']}_{topic}_history"
    
    if format_choice == '1':
        filename += ".txt"
        try:
            with open(filename, 'w') as file:
                file.write(f"Quiz Results for {user['name']} in {topic}:\n")
                file.write("=" * 40 + "\n")
                for u in user["history"][topic]:
                    file.write(f"Date: {u['date']}, Time: {u['time']}, Score: {u['mark']}, Difficulty: {u['difficulty']}\n")
            print(f"Results successfully exported to {filename}")
        except IOError:
            print("Error occurred while exporting results to text file.")
    
    elif format_choice == '2':
        filename += ".csv"
        try:
            with open(filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Date", "Time", "Score", "Difficulty"])
                for u in user["history"][topic]:
                    writer.writerow([u["date"], u["time"], u["mark"], u["difficulty"]])
            print(f"Results successfully exported to {filename}")
        except IOError:
            print("Error occurred while exporting results to CSV file.")
    
    else:
        print("Invalid choice. Export cancelled.")

def printHistory(user, topic):
    print()
    print(f"Your History in {topic}:")
    print("=" * 40)
    if not user["history"][topic]:
        print("No history available.")
        return

    for u in user["history"][topic]:
        print(u)

    print("\nWould you like to export this history?")
    print("1. Yes")
    print("2. No")
    choice = input("Enter your choice: ").strip()
    if choice == '1':
        export_results(user, topic)
    elif choice == '2':
        print("Export cancelled.")
    else:
        print("Invalid choice.")

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
