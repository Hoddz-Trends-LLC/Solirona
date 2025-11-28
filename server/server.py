# server.py
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from simulation import SolironaSimulation
from solirona_engine import SolironaNode
import threading

app = Flask(__name__, static_folder="../web_client", static_url_path="/")
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Instantiate simulation
sim = SolironaSimulation(num_nodes=40, connect_prob=0.3, waveform_length=128)

@app.route('/')
def index():
    return send_from_directory('../web_client', 'index.html')

@app.route('/api/state')
def get_state():
    return jsonify(sim.get_state())

@socketio.on('connect')
def on_connect(auth=None):
    emit('state', sim.get_state())

def background_sim():
    sim.run(interval=0.2)

# Advanced control endpoints
@socketio.on('step')
def on_step(data=None):
    count = (data or {}).get('count', 1)
    with sim.lock:
        for _ in range(count):
            sim.step()
    emit('state', sim.get_state(), broadcast=True)

@socketio.on('set_params')
def on_set_params(data):
    cp = data.get('connect_prob')
    cc = data.get('collapse_chance')
    ig = data.get('interference_gain')
    with sim.lock:
        if cp is not None:
            sim.network.random_connect(float(cp))
        if cc is not None:
            sim.collapse_chance = float(cc)
        if ig is not None:
            sim.interference_gain = float(ig)
    emit('state', sim.get_state(), broadcast=True)

@socketio.on('rotate_phase_all')
def on_rotate_phase_all(data):
    angle = (data or {}).get('angle')
    with sim.lock:
        for node in sim.network.nodes.values():
            sim.rotate_phase(node, angle)
    emit('state', sim.get_state(), broadcast=True)

@socketio.on('add_node')
def on_add_node(data=None):
    with sim.lock:
        nid = f"n{len(sim.network.nodes)}"
        sim.network.add_node(SolironaNode(nid, sim.waveform_length))
    emit('state', sim.get_state(), broadcast=True)

@socketio.on('remove_node')
def on_remove_node(data=None):
    with sim.lock:
        if sim.network.nodes:
            last = sorted(sim.network.nodes.keys())[-1]
            sim.network.remove_node(last)
    emit('state', sim.get_state(), broadcast=True)

@socketio.on('reconnect')
def on_reconnect(data):
    prob = float(data.get('connect_prob', 0.3))
    with sim.lock:
        sim.network.random_connect(prob)
    emit('state', sim.get_state(), broadcast=True)

@socketio.on('set_node_count')
def on_set_node_count(data):
    target = int(data.get('count', len(sim.network.nodes)))
    with sim.lock:
        while len(sim.network.nodes) < target:
            nid = f"n{len(sim.network.nodes)}"
            sim.network.add_node(SolironaNode(nid, sim.waveform_length))
        while len(sim.network.nodes) > target:
            last = sorted(sim.network.nodes.keys())[-1]
            sim.network.remove_node(last)
    emit('state', sim.get_state(), broadcast=True)

if __name__ == '__main__':
    thread = threading.Thread(target=background_sim, daemon=True)
    thread.start()
    socketio.run(app, port=5000)
