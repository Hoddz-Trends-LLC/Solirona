# server.py

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from simulation import SolironaSimulation
import threading

app = Flask(__name__, static_folder="../web_client", static_url_path="/")
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

sim = SolironaSimulation(num_nodes=40, connect_prob=0.3, waveform_length=128)

@app.route('/')
def index():
    return send_from_directory('../web_client', 'index.html')

@app.route('/api/state')
def get_state():
    return jsonify(sim.get_state())

@socketio.on('connect')
def on_connect():
    emit('state', sim.get_state())

def background_sim():
    sim.run(interval=0.2)

if __name__ == '__main__':
    thread = threading.Thread(target=background_sim)
    thread.daemon = True
    thread.start()
    socketio.run(app, port=5000)
