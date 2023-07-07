#  Develop a chatbot interface for AI representative 
# to communicate with US citizens and understand their needs and concerns related to overall wellbeing, 
# and generate a survey based on the conversation.
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import openai
import config

# Replace with your OpenAI API key
openai.api_key = config.OPENAI_API_KEY

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_input = db.Column(db.String(500))
    ai_response = db.Column(db.String(500))

@app.route('/')
def index():
    return "Chatbot API is up and running!"

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form.get('user_input')
    response = generate_ai_response(user_input)

    chat = Chat(user_input=user_input, ai_response=response)
    db.session.add(chat)
    db.session.commit()

    return jsonify({'response': response})

def generate_ai_response(prompt):
    model_engine = "text-davinci-003"
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
    db.create_all()
    app.run(debug=True)
