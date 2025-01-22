import json
import random
import datetime
import time
import csv
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.panel import Panel
from rich.text import Text


console = Console()

try:
    with open("Login.json", 'r') as file:
        data = json.load(file)
except FileNotFoundError:
    data = {"users": []}
except json.JSONDecodeError:
    data = {"users": []}

try:
    with open("Questions.json", 'r', encoding='utf-8') as file:
        questions = json.load(file)
except FileNotFoundError:
    questions = {}
except json.JSONDecodeError:
    questions = {}

def show_user_history(user):
    """Display the user's quiz history for all topics."""
    console.print(Panel.fit("Your Quiz History", style="bold blue"))
    if not any(user["history"].values()):  
        console.print("No history available.", style="italic red")
        return

    for topic, history in user["history"].items():
        table = Table(title=f"Topic: {topic.capitalize()}", style="cyan")
        table.add_column("Date", style="dim")
        table.add_column("Time", style="dim")
        table.add_column("Score", justify="right", style="green")
        table.add_column("Difficulty", style="magenta")

        if not history:
            table.add_row("No history available.")
        else:
            for entry in history:
                table.add_row(entry['date'], entry['time'], entry['mark'], entry['difficulty'])

        console.print(table)

def register():
    """Function to register a new user."""
    console.print(Panel.fit("Welcome to the QCM System!", style="bold blue"))
    username = Prompt.ask("Enter your username", default="user")
    
    for user in data["users"]:
        if username == user["name"]:
            console.print("Username already exists. Please choose another username.", style="bold red")
            return
    while True:
        password = Prompt.ask("Enter your password", password=True)
        confirm_password = Prompt.ask("Confirm your password", password=True)
        
        if password == confirm_password:
            break
        console.print("Passwords do not match. Please try again.", style="bold red")

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
    
    console.print(f"Account successfully created for {username}!", style="bold green")

def login():
    """Function to log in an existing user."""
    while True:
        username = Prompt.ask("Enter your username", default="user")
        for user in data["users"]:
            if username == user["name"]:
                while True:
                    password = Prompt.ask("Enter your password", password=True)
                    if user["password"] == password:
                        console.print(f"Welcome back, {username}!", style="bold green")
                        show_user_history(user)  
                        return user  
                    else:
                        console.print("Invalid password. Please try again.", style="bold red")
        console.print("The username is invalid!", style="bold red")

def play_quiz(topic, user):
    """Function to play the quiz."""
    topic_key = topic  

    if topic.lower() not in questions:
        console.print(f"No questions available for the topic: {topic}.", style="bold red")
        return
    
    difficulty_levels = ["easy", "medium", "hard"]
    
    console.print("\nSelect a difficulty level:", style="bold blue")
    for i, level in enumerate(difficulty_levels):
        console.print(f"{i+1}. {level.capitalize()}")

    try:
        difficulty_choice = int(Prompt.ask("Enter the number of your chosen difficulty", choices=["1", "2", "3"]))
        difficulty = difficulty_levels[difficulty_choice - 1]
    except ValueError:
        console.print("Invalid input. Please enter a valid number.", style="bold red")
        return
        
    if difficulty not in questions[topic.lower()]:
        console.print(f"No questions available for {topic} at {difficulty} level.", style="bold red")
        return

    time_par_qst = 20 if difficulty == "easy" else 40 if difficulty == "medium" else 60
    
    topic_questions = questions[topic.lower()][difficulty]

    n = int(Prompt.ask(f"How many questions do you want to attempt? (Max {len(topic_questions)})", default=str(len(topic_questions))))
    n = min(n, len(topic_questions)) 

    if topic_key not in user["history"]:
        user["history"][topic_key] = []

    total_time = n * time_par_qst  
    start_time = time.time()
    end_time = start_time + total_time

    hours, remainder = divmod(total_time, 3600)
    minutes, seconds = divmod(remainder, 60)
    console.print(f"\nYou have {hours:02d}:{minutes:02d}:{seconds:02d} to complete the quiz.", style="bold cyan")

    score = 0
    for i in range(n):
        remaining_time = int(end_time - time.time())
        if remaining_time <= 0:
            console.print("\nTime's up! The quiz has ended.", style="bold red")
            break

        hours, remainder = divmod(remaining_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        console.print(f"\nTime left: {hours:02d}:{minutes:02d}:{seconds:02d}", style="bold cyan")

        q = topic_questions[i]
        console.print(f"Question {i + 1}: {q['question']}", style="bold")
        for option, text in q['choices'].items():
            console.print(f"   {option}. {text}")
        
        answer = Prompt.ask("Your answer (a, b, c, or d)", choices=['a', 'b', 'c', 'd'])
        
        if time.time() > end_time:
            console.print("\nTime's up! The quiz has ended.", style="bold red")
            break

        if answer == q['correct_answer']:
            score += 1
            console.print("Correct Answer", style="bold green")
        else:
            console.print("Incorrect Answer !", style="bold red")
            console.print(f"The correct answer is {q['correct_answer']}", style="bold green")

    quiz_date = datetime.datetime.now().strftime("%Y/%m/%d")
    quiz_time = datetime.datetime.now().strftime("%H:%M:%S")
    mark = f"{score}/{n}"
    
    history_entry = {
        "date": quiz_date,
        "time": quiz_time,
        "mark": mark,
        "difficulty": difficulty  
    }

    user["history"][topic_key].append(history_entry)

    with open("Login.json", "w") as file:
        json.dump(data, file, indent=4)
    
    console.print(f"\nQuiz completed! You scored {score}/{n}.", style="bold green")
    console.print(f"Date: {quiz_date}, Time: {quiz_time}", style="bold cyan")

def export_results(user, topic):
    if not user["history"].get(topic):
        console.print(f"No history available for the topic: {topic}", style="bold red")
        return

    console.print("\nChoose export format:", style="bold blue")
    console.print("1. Text file (.txt)")
    console.print("2. CSV file (.csv)")
    format_choice = Prompt.ask("Enter your choice", choices=["1", "2"])

    filename = f"{user['name']}_{topic}_history"
    
    if format_choice == '1':
        filename += ".txt"
        try:
            with open(filename, 'w') as file:
                file.write(f"Quiz Results for {user['name']} in {topic}:\n")
                file.write("=" * 40 + "\n")
                for u in user["history"][topic]:
                    file.write(f"Date: {u['date']}, Time: {u['time']}, Score: {u['mark']}, Difficulty: {u['difficulty']}\n")
            console.print(f"Results successfully exported to {filename}", style="bold green")
        except IOError:
            console.print("Error occurred while exporting results to text file.", style="bold red")
    
    elif format_choice == '2':
        filename += ".csv"
        try:
            with open(filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Date", "Time", "Score", "Difficulty"])
                for u in user["history"][topic]:
                    writer.writerow([u["date"], u["time"], u["mark"], u["difficulty"]])
            console.print(f"Results successfully exported to {filename}", style="bold green")
        except IOError:
            console.print("Error occurred while exporting results to CSV file.", style="bold red")

def printHistory(user, topic):
    console.print()
    console.print(Panel.fit(f"Your History in {topic}", style="bold blue"))
    if not user["history"][topic]:
        console.print("No history available.", style="italic red")
        return

    table = Table(style="cyan")
    table.add_column("Date", style="dim")
    table.add_column("Time", style="dim")
    table.add_column("Score", justify="right", style="green")
    table.add_column("Difficulty", style="magenta")

    for u in user["history"][topic]:
        table.add_row(u["date"], u["time"], u["mark"], u["difficulty"])

    console.print(table)

    console.print("\nWould you like to export this history?", style="bold blue")
    console.print("1. Yes")
    console.print("2. No")
    choice = Prompt.ask("Enter your choice", choices=["1", "2"])
    if choice == '1':
        export_results(user, topic)
    elif choice == '2':
        console.print("Export cancelled.", style="bold red")
    else:
        console.print("Invalid choice.", style="bold red")

def select_topic(user):
    """Function to display and select topics."""
    console.print("\nSelect a topic:", style="bold blue")
    topics = ["physics", "mathematics", "computerscience" , "electronics" , "geography" , "history"]
    for i, topic in enumerate(topics, start=1):
        console.print(f"{i}. {topic}")
    
    choice = Prompt.ask("Enter the number of the topic you want to select", choices=[str(i) for i in range(1, len(topics) + 1)])
    selected_topic = topics[int(choice) - 1]
    console.print(f"\nYou selected: {selected_topic}", style="bold green")
    while True:
        console.print("\n1. View Scores", style="bold blue")
        console.print("2. Play", style="bold blue")
        console.print("3. Back", style="bold blue")
        sub_choice = Prompt.ask("Enter your choice", choices=["1", "2", "3"])
        
        if sub_choice == '1':
            printHistory(user , selected_topic)
        elif sub_choice == '2':
            play_quiz(selected_topic, user)  
        elif sub_choice == '3':
            return
        else:
            console.print("Invalid choice, please try again.", style="bold red")

def main():
    """Main menu."""
    console.print(Panel.fit("Welcome to the QCM System!", style="bold blue"))
    current_user = None
    while True:
        if not current_user:
            console.print("\n1. Login", style="bold blue")
            console.print("2. Register", style="bold blue")
            console.print("3. Exit", style="bold blue")
        else:
            console.print("\n1. Select Topic", style="bold blue")
            console.print("2. Logout", style="bold blue")
            console.print("3. Exit", style="bold blue")
        
        choice = Prompt.ask("Enter your choice", choices=["1", "2", "3"])
        
        if choice == '1':
            if current_user:
                select_topic(current_user)
            else:
                current_user = login()
        elif choice == '2':
            if current_user:
                current_user = None
                console.print("Logged out successfully.", style="bold green")
            else:
                register()
        elif choice == '3':
            console.print("Exiting the application. Goodbye!", style="bold blue")
            break
        else:
            console.print("Invalid choice, please try again.", style="bold red")

if __name__ == "__main__":
    main()