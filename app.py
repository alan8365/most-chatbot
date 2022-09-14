from flask import Flask, render_template, request

from rasa.core.agent import Agent
from rasa.core.interpreter import RasaNLUInterpreter

import os
import asyncio
import requests


app = Flask(__name__)
app.config['SECRET_KEY'] = 'most-chatbot-gogogo'
models_folder = 'models'

projects = ['allen', 'shou']
agents = {}

loop = asyncio.get_event_loop()

for project in projects:
    interpreter = RasaNLUInterpreter(os.path.join(
        models_folder, project, "model", "nlu"))
    agents[project] = Agent.load(os.path.join(
        models_folder, project, "model"), interpreter=interpreter)


@app.route('/')
def index_page():
    return render_template('index.html')


@app.route('/chat')
def chat_room():
    return render_template('chat.html')


@app.route('/rasa')
def rasa():
    body = {
        "sender": "Lucy",
        "message": "老人照護"
    }
    a = requests.post(rasa_url, body)
    print(a.content)

    return a.content


@app.route('/callback/<string:project>', methods=["POST"])
def callback(project):
    content = request.form.get("message")
    return inference(project, content)


def inference(project, content):
    if project in agents:
        if content is None:
            return "arg lack", 400
        return loop.run_until_complete(agents[project].handle_text(content))[0]["text"]
    return "", 404



def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
