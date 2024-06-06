import openai
from flask import Flask, render_template, request
from PyPDF2 import PdfReader
import os

app = Flask(__name__)

# Set your OpenAI API key
openai.api_key = 'sk-proj-qxet7XwxHam67TVhhKFZT3BlbkFJq9AYOzbmqY1pLAi8bmcA'

# Hardcode the PDF file path from your local system
script_dir = os.path.dirname(os.path.abspath(__file__))
PDF_FILE_PATH = os.path.join(script_dir, 'data', 'sofa.pdf')

# Store conversation history in a list
conversation_history = []

def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as file:
        pdf_reader = PdfReader(file)
        text = ''
        for page_num in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page_num].extract_text()
    return text

def answer_user_question(pdf_content, user_prompt):
    prompt = f"{pdf_content}\nUser's Prompt: {user_prompt}\n"

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    answer = response.choices[0].message.content
    return answer

@app.route('/', methods=['GET', 'POST'])
def index():
    global conversation_history

    if request.method == 'POST':
        # Extract text from the hardcoded PDF file
        pdf_content = extract_text_from_pdf(PDF_FILE_PATH)

        # User's prompt entered through the form
        user_prompt = request.form.get('user_prompt', '')

        # Handle the case where the user doesn't enter a prompt
        if not user_prompt:
            return "Please enter a question."

        # Add user prompt to conversation history
        conversation_history.append({"role": "user", "content": user_prompt})

        # Get the answer based on the PDF content and user's prompt
        answer = answer_user_question(pdf_content, user_prompt)
        # Add AI answer to conversation history
        conversation_history.append({"role": "assistant", "content": answer})

        return render_template('index.html', pdf_content=pdf_content, conversation=conversation_history)

    # Clear conversation history on GET request
    conversation_history = []
    return render_template('index.html', pdf_content='', conversation=[])

if __name__ == '__main__':
    app.run(debug=True)
