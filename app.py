from flask import Flask, render_template, request
# TODO load rasa model in code

from flask_socketio import SocketIO
from rasa.core.agent import Agent
from rasa.core.interpreter import RasaNLUInterpreter

import os
import asyncio
import requests


app = Flask(__name__)
app.config['SECRET_KEY'] = 'most-chatbot-gogogo'
socketio = SocketIO(app)
rasa_url = 'http://localhost:5005/webhooks/rest/webhook'
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
    # return render_template('rasa.html')


@app.route('/callback/<string:project>', methods=["POST"])
def callback(project):
    content = request.form.get("content")
    return inference(project, content)


def inference(project, content):
    if project in agents:
        if content is None:
            return "arg lack", 400
        return loop.run_until_complete(agents[project].handle_text(content))[0]["text"]
    return "", 404

# @app.route('/', methods=['POST'])
# def my_form_post():
#     print(request.form)
#     text = request.form['message']
#     processed_text = text.upper()
#     return processed_text


def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')


@socketio.on('init-connect')
def handle_connect_event(json, methods=['GET', 'POST']):
    print('received connect: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)


@socketio.on('rasa')
def handle_rasa_event(json, methods=['GET', 'POST']):
    print('receivee rasa: ' + str(json))

    response = inference(json['project'], json['message'])
    socketio.emit('rasa-response', response, callback=messageReceived)


if __name__ == '__main__':
    socketio.run(app, debug=True)
    # app.run(debug=True, host='0.0.0.0')
