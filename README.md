# Solirona Lab

**Solirona Lab** is a browser-based, quantum-inspired simulation engine that visualizes how energy flows, resonates, and collapses across a network of virtual nodes. It blends scientific modeling with interactive controls, allowing users to explore complex signal dynamics in real time — no coding required.

---

## 🌌 What Is Solirona?

Solirona simulates a network of virtual nodes, each carrying a complex waveform (a signal). These nodes interact through resonance and interference, and occasionally collapse into discrete states based on probabilistic rules — mimicking behaviors found in quantum systems.

You can think of it as a digital physics lab where each colored wave represents a node’s evolving signal. The simulation runs live in your browser, and you can control every aspect of it.

---

## 🧠 Key Concepts

- **Node**: A virtual signal point with a waveform that evolves over time.
- **Waveform**: A list of complex numbers representing the node’s signal.
- **Resonance**: Nodes influence each other’s signals through blending.
- **Interference**: Signals mix and shift based on network connections.
- **Collapse**: A node locks into a final state, shown as a red dot.
- **Network**: A graph of nodes connected by probabilistic links.

---

## 🖥️ Interface Overview

### 🔹 Canvas Display
- Colored waveforms represent each node’s signal.
- Red dots indicate collapsed nodes.
- Rows group nodes for visual clarity.
- Waveforms evolve in real time as the simulation runs.

### 🔹 Status Box
Updates every 5 seconds with:
- Simulation running status
- Number of collapsed nodes
- Average signal magnitude
- Time and separation metrics

---

## 🎛️ Control Panel

### 🧪 Simulation Controls
| Button           | Description                                      |
|------------------|--------------------------------------------------|
| **Pause / Resume** | Start or stop the simulation loop               |
| **Reset**        | Reload the simulation from scratch               |
| **Step ×1**      | Advance simulation by one step                   |
| **Step ×10**     | Advance simulation by ten steps                  |

---

### 🔗 Network Controls
| Control              | Description                                      |
|----------------------|--------------------------------------------------|
| **Nodes (input)**    | Set total number of nodes                        |
| **Apply**            | Apply new node count                             |
| **Connect prob**     | Set connection probability between nodes         |
| **Reconnect**        | Rebuild network connections                      |
| **Add node**         | Add one node to the network                      |
| **Remove node**      | Remove the last node                             |

---

### ⚛️ Quantum-Inspired Operations
| Control                  | Description                                      |
|--------------------------|--------------------------------------------------|
| **Phase angle (rad)**    | Set rotation angle for signal phase             |
| **Rotate phase (all)**   | Apply phase rotation to all nodes               |
| **Interference gain**    | Set how strongly nodes influence each other     |
| **Set interference gain**| Apply new interference strength                 |
| **Collapse chance**      | Set probability of node collapse per step       |
| **Set collapse chance**  | Apply new collapse probability                  |

---

## 🚀 Getting Started

### 1. Clone the repository

git clone https://github.com/hoddz-trends-llc/solirona.git
cd solirona

## 2. Setup Python environment

python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
pip install -r requirements.txt

## 3. Run the server

cd server
python server.py

## 4. Open the lab

Visit http://localhost:5000 in your browser.

## 🧩 Folder Structure

SolironaLab/
├─ server/
│  ├─ server.py
│  ├─ simulation.py
│  └─ solirona_engine.py
├─ web_client/
│  ├─ index.html
│  ├─ style.css
│  ├─ app.js
│  └─ assets/
│     └─ logo.png
├─ requirements.txt
└─ README.md

## 🌍 Use Cases

Education: Teach quantum-inspired concepts visually.
Research: Prototype signal networks and collapse models.
Creative: Explore emergent patterns and resonance art.
Engineering: Simulate probabilistic systems and waveform blending.

## 🛠️ Technologies Used

Python 3.12
Flask + Flask-SocketIO
NumPy
Eventlet
HTML/CSS/JavaScript

## 📦 Requirements

flask
flask-cors
flask-socketio
eventlet
numpy
scipy

## 🧑‍💻 Credits
Created by Hoddz Trends LLC 
Interface and simulation logic inspired by quantum systems and signal dynamics.
