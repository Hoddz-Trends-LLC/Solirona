# simulation.py

from solirona_engine import SolironaNetwork, SolironaNode
import random
import numpy as np
import threading
import time   # ✅ Added import

class SolironaSimulation:
    def __init__(self, num_nodes=30, connect_prob=0.25, waveform_length=128):
        self.network = SolironaNetwork()
        for i in range(num_nodes):
            self.network.add_node(SolironaNode(f"n{i}", waveform_length))
        self.network.random_connect(connect_prob)
        self.running = False
        self.lock = threading.Lock()

    def rotate_phase(self, node, angle=None):
        if angle is None:
            angle = random.uniform(0, np.pi)
        node.waveform *= np.exp(1j * angle)

    def interfere(self, node):
        for nb in node.connections:
            node.waveform += 0.5 * nb.waveform
        node.normalize()

    def collapse(self, node):
        if node.collapsed:
            return
        probabilities = np.abs(node.waveform) ** 2
        probabilities /= probabilities.sum()
        choice = np.random.choice(len(node.waveform), p=probabilities)
        node.collapsed = True
        node.value = int(choice)
        node.waveform = np.zeros_like(node.waveform)
        node.waveform[choice] = 1.0

    def propagate_resonance(self, node, iterations=1):
        for _ in range(iterations):
            self.interfere(node)
            self.rotate_phase(node)

    def step(self, collapse_chance=0.05):
        for node in self.network.nodes.values():
            self.propagate_resonance(node)
        for node in self.network.nodes.values():
            if not node.collapsed and random.random() < collapse_chance:
                self.collapse(node)

    def run(self, interval=0.1):
        self.running = True
        while self.running:
            with self.lock:
                self.step()
            time.sleep(interval)

    def stop(self):
        self.running = False

    def get_state(self):
        # ✅ Convert complex numbers into serializable dicts
        state = {}
        for nid, node in self.network.nodes.items():
            state[nid] = {
                "waveform": [
                    {
                        "real": float(val.real),
                        "imag": float(val.imag),
                        "magnitude": float(abs(val)),
                        "phase": float(np.angle(val))
                    }
                    for val in node.waveform
                ],
                "collapsed": node.collapsed,
                "value": node.value,
                "connections": [nb.id for nb in node.connections]
            }
        return state
