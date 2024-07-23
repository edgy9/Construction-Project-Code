from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('websocketTest.html')

@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)
    emit('response', {'data': 'Message received!'})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)