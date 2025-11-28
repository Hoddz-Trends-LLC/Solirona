# simulation.py
from solirona_engine import SolironaNetwork, SolironaNode
import random
import numpy as np
import threading
import time

class SolironaSimulation:
    def __init__(self, num_nodes=30, connect_prob=0.25, waveform_length=128):
        self.network = SolironaNetwork()
        self.waveform_length = waveform_length
        for i in range(num_nodes):
            self.network.add_node(SolironaNode(f"n{i}", waveform_length))
        self.network.random_connect(connect_prob)

        self.running = False
        self.lock = threading.Lock()

        # Adjustable parameters
        self.interference_gain = 0.5
        self.collapse_chance = 0.05

    def rotate_phase(self, node, angle=None):
        if angle is None:
            angle = random.uniform(0, np.pi)
        node.waveform *= np.exp(1j * angle)

    def interfere(self, node):
        for nb in node.connections:
            node.waveform += self.interference_gain * nb.waveform
        node.normalize()

    def collapse(self, node):
        if node.collapsed:
            return
        probabilities = np.abs(node.waveform) ** 2
        total = probabilities.sum()
        if total <= 0:
            return
        probabilities /= total
        choice = np.random.choice(len(node.waveform), p=probabilities)
        node.collapsed = True
        node.value = int(choice)
        node.waveform = np.zeros_like(node.waveform)
        node.waveform[choice] = 1.0

    def propagate_resonance(self, node, iterations=1):
        for _ in range(iterations):
            self.interfere(node)
            self.rotate_phase(node)

    def step(self, collapse_chance=None):
        cc = self.collapse_chance if collapse_chance is None else collapse_chance
        for node in self.network.nodes.values():
            self.propagate_resonance(node)
        for node in self.network.nodes.values():
            if not node.collapsed and random.random() < cc:
                self.collapse(node)

    def run(self, interval=0.2):
        self.running = True
        while self.running:
            with self.lock:
                self.step()
            time.sleep(interval)

    def stop(self):
        self.running = False

    def get_state(self):
        # JSON‑serializable representation with complex decomposition
        state = {}
        for nid, node in self.network.nodes.items():
            wf = []
            for val in node.waveform:
                wf.append({
                    "real": float(val.real),
                    "imag": float(val.imag),
                    "magnitude": float(abs(val)),
                    "phase": float(np.angle(val))
                })
            state[nid] = {
                "waveform": wf,
                "collapsed": bool(node.collapsed),
                "value": node.value,
                "connections": [nb.id for nb in node.connections]
            }
        return state
