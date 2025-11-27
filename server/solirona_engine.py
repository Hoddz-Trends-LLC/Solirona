# solirona_engine.py

import numpy as np
import random
import threading
import time

class SolironaNode:
    def __init__(self, id, waveform_length=128):
        self.id = id
        self.waveform = np.ones(waveform_length, dtype=np.complex128)
        self.connections = []
        self.collapsed = False
        self.value = None

    def normalize(self):
        norm = np.linalg.norm(self.waveform)
        if norm > 0:
            self.waveform /= norm

class SolironaNetwork:
    def __init__(self):
        self.nodes = {}

    def add_node(self, node: SolironaNode):
        self.nodes[node.id] = node

    def connect(self, id1, id2):
        n1, n2 = self.nodes[id1], self.nodes[id2]
        if n2 not in n1.connections:
            n1.connections.append(n2)
        if n1 not in n2.connections:
            n2.connections.append(n1)

    def random_connect(self, prob=0.2):
        ids = list(self.nodes.keys())
        for i in range(len(ids)):
            for j in range(i+1, len(ids)):
                if random.random() < prob:
                    self.connect(ids[i], ids[j])
