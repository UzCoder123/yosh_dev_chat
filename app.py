from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, leave_room, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Xabarlar saqlanadigan ro'yxat
messages = {}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join_room')
def handle_join_room(data):
    username = data['username']
    room = data['room']
    join_room(room)
    # Yangi foydalanuvchiga xonadagi avvalgi xabarlarni qaytarish
    if room in messages:
        emit('previous_messages', messages[room], room=request.sid)
    emit('user_joined', {'username': username, 'room': room}, room=room)

@socketio.on('chat_message')
def handle_chat_message(data):
    room = data['room']
    message = {'username': data['username'], 'message': data['message']}
    # Xabarlarni saqlash
    if room not in messages:
        messages[room] = []
    messages[room].append(message)
    emit('chat_message', message, room=room)

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', allow_unsafe_werkzeug=True)
