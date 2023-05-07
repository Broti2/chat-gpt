from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
socketio = SocketIO(app)

# ChatGPT API endpoint
API_ENDPOINT = "https://api.openai.com/v1/engines/davinci-codex/completions"

# Your ChatGPT API key
API_KEY = "sk - qJvgRQj3CaRLWAtJQKxGT3BlbkFJFPV8rCtpIeCPRujudSWT"

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(message):
    user_message = message['data']
    emit('response', {'message': user_message}, broadcast=True)

    bot_response = generate_chat_response(user_message)
    emit('response', {'message': bot_response}, broadcast=True, include_self=False)

def generate_chat_response(message):
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

    data = {
        'prompt': message,
        'max_tokens': 50  # Adjust this value to control the response length
    }

    response = requests.post(API_ENDPOINT, headers=headers, json=data)
    result = response.json()
    completion = result['choices'][0]['text']

    return completion

if __name__ == '__main__':
    socketio.run(app)
