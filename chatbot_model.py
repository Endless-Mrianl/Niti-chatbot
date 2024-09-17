import pandas as pd
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle

# Download NLTK stopwords
nltk.download('punkt')
nltk.download('stopwords')

# Load the dataset
data = pd.read_csv('D:\chatbotdoj\data\chatbot_dataset.csv')

# Extract questions and answers
questions = data['question']
answers = data['answer']

# Vectorize the text data using TF-IDF
vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
X = vectorizer.fit_transform(questions)

# Train a simple model using Logistic Regression
model = LogisticRegression()
model.fit(X, answers)

# Save the model and vectorizer
with open('models/chatbot_model.pkl', 'wb') as f:
    pickle.dump(model, f)

with open('models/vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)

print("Model training complete and saved!")
