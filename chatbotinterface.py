#  Develop a chatbot interface for AI representative 
# to communicate with US citizens and understand their needs and concerns related to overall wellbeing, 
# and generate a survey based on the conversation.

import os
import openai
from flask import Flask, request, jsonify, render_template
import config
# Replace with your OpenAI API key
openai.api_key = config.OPENAI_API_KEY

app = Flask(__name__)

@app.route('/')
def index():
    return "Chatbot API is up and running!"


@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form.get('user_input')
    response = generate_ai_response(user_input)
    return jsonify({'response': response})

def generate_ai_response(prompt):
    model_engine = "text-davinci-002"
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()

if __name__ == '__main__':
    app.run(debug=True)

