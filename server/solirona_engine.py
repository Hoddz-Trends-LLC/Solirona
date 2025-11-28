# solirona_engine.py
import numpy as np
import random

class SolironaNode:
    def __init__(self, node_id: str, waveform_length: int = 128):
        self.id = node_id
        self.waveform = self._init_waveform(waveform_length)
        self.connections = []
        self.collapsed = False
        self.value = None

    def _init_waveform(self, n):
        # Random complex waveform with normalization
        real = np.random.randn(n)
        imag = np.random.randn(n)
        wf = real + 1j * imag
        norm = np.linalg.norm(wf)
        return wf / (norm if norm != 0 else 1.0)

    def normalize(self):
        norm = np.linalg.norm(self.waveform)
        if norm > 0:
            self.waveform = self.waveform / norm

class SolironaNetwork:
    def __init__(self):
        self.nodes = {}

    def add_node(self, node: SolironaNode):
        self.nodes[node.id] = node

    def remove_node(self, node_id: str):
        if node_id in self.nodes:
            target = self.nodes[node_id]
            # Remove from others' connections
            for n in self.nodes.values():
                n.connections = [c for c in n.connections if c is not target]
            del self.nodes[node_id]

    def connect(self, id1: str, id2: str):
        if id1 in self.nodes and id2 in self.nodes and id1 != id2:
            n1, n2 = self.nodes[id1], self.nodes[id2]
            if n2 not in n1.connections:
                n1.connections.append(n2)
            if n1 not in n2.connections:
                n2.connections.append(n1)

    def random_connect(self, prob: float = 0.25):
        # Rebuild connections based on probability
        for n in self.nodes.values():
            n.connections = []
        ids = list(self.nodes.keys())
        for i in range(len(ids)):
            for j in range(i + 1, len(ids)):
                if random.random() < prob:
                    self.connect(ids[i], ids[j])
