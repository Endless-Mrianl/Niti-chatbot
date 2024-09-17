from flask import Flask, render_template, request, session
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import subprocess
import os

# Load the dataset and vectorizer
df = pd.read_csv('D:/chatbotdoj/data/chatbot_dataset.csv')
vectorizer = TfidfVectorizer()
questions = df['question'].values
vectorized_questions = vectorizer.fit_transform(questions)

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session handling

@app.route('/')
def home():
    session.clear()  # Clear session when the page is loaded
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.form['user_input'].strip().lower()  # Get user input

    # Define greeting keywords
    if user_input == 'greeting':
        return handle_greeting()

    # Check if the bot is expecting a case type after clicking "Pending Cases"
    elif session.get('expecting_case_type', False):
        return handle_case_type(user_input)

    # Check if the input is "pending cases"
    elif user_input == 'pending_cases':
        session['expecting_case_type'] = True  # Set session to expect case type next
        return handle_pending_cases()
    
    elif session.get('expecting_year_range', False):
        return handle_year_range(user_input)

    # If no match, respond with a default message
    else:
        return render_template('index.html', response="I didn't understand that. Please try again.")

def handle_greeting():
    response = "Hello! How can I assist you today?"
    return render_template('index.html', response=response)

def handle_pending_cases():
    # Ask for case type input
    return render_template('index.html', response="Please enter the case type (e.g., civil case, criminal case)")

def handle_case_type(case_type):
    # Reset the session flag after receiving the case type
    session['expecting_case_type'] = False
    session['expecting_year_range'] = True
    
    # Call the Selenium script to get case details based on type
    result = subprocess.run(["python", "selenium_scraper.py", case_type], capture_output=True, text=True)
    
    # Check if the file exists before reading
    file_path = 'case_details.txt'
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            case_details = file.read()
    else:
        case_details = "No case details available at the moment."
    response = f"Total pending cases for {case_type}: {case_details}\n" \
               "Please enter the year range (e.g., 0 to 1 years, 1 to 2 years)."

    return render_template('index.html', response=case_details)
def handle_year_range(year_range):
    # Call the Selenium script again or handle year range logic
    # Here, assuming you'll pass the year range to the Selenium script if needed
    result = subprocess.run(["python", "selenium_scraper.py", year_range], capture_output=True, text=True)
    
    # Check if the file exists before reading
    file_path = 'case_details.txt'
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            year_details = file.read()
    else:
        year_details = "No case details available for the specified year range."

    return render_template('index.html', response=year_details)

if __name__ == '__main__':
    app.run(debug=True)
