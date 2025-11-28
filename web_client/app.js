// app.js — advanced controls and visualization
const socket = io();

let simState = null;
let paused = false;

// Receive state updates
socket.on('state', state => {
  simState = state;
  if (!paused) render();
});

// Simulation control
document.getElementById('pauseBtn').onclick = () => { paused = !paused; };
document.getElementById('resetBtn').onclick = () => { location.reload(); };
document.getElementById('stepBtn').onclick = () => { socket.emit('step', { count: 1 }); };
document.getElementById('step10Btn').onclick = () => { socket.emit('step', { count: 10 }); };

// Network controls
document.getElementById('applyNodeCount').onclick = () => {
  const count = parseInt(document.getElementById('nodeCount').value, 10);
  socket.emit('set_node_count', { count });
};
document.getElementById('reconnect').onclick = () => {
  const p = parseFloat(document.getElementById('connectProb').value);
  socket.emit('reconnect', { connect_prob: p });
};
document.getElementById('addNode').onclick = () => socket.emit('add_node');
document.getElementById('removeNode').onclick = () => socket.emit('remove_node');

// Quantum-inspired ops
document.getElementById('applyPhaseAll').onclick = () => {
  const angle = parseFloat(document.getElementById('phaseAngle').value);
  socket.emit('rotate_phase_all', { angle });
};
document.getElementById('applyInterfGain').onclick = () => {
  const g = parseFloat(document.getElementById('interfGain').value);
  socket.emit('set_params', { interference_gain: g });
};
document.getElementById('applyCollapseChance').onclick = () => {
  const c = parseFloat(document.getElementById('collapseChance').value);
  socket.emit('set_params', { collapse_chance: c });
};

// Status updates every 5s
function updateStatus() {
  if (!simState) return;
  const nodes = Object.values(simState);
  const collapsed = nodes.filter(n => n.collapsed).length;
  const total = nodes.length;
  const percent = total ? ((collapsed / total) * 100).toFixed(1) : '0.0';

  const avgMag = nodes.reduce((acc, n) => {
    if (!n.waveform || !n.waveform.length) return acc;
    const mags = n.waveform.map(c => c.magnitude ?? Math.abs(c));
    const mean = mags.reduce((a, b) => a + b, 0) / mags.length;
    return acc + mean;
  }, 0) / (total || 1);

  const msg = `Running: ${!paused}. Collapsed ${collapsed}/${total} (${percent}%). Avg magnitude ${avgMag.toFixed(3)}.`;
  document.getElementById('statusBox').textContent = msg;
}
setInterval(updateStatus, 5000);

// 🔹 Sidebar calculations every 5s
function updateCalculations() {
  if (!simState) return;
  const nodes = Object.values(simState);
  const collapsed = nodes.filter(n => n.collapsed).length;
  const total = nodes.length;

  const avgMag = nodes.reduce((acc, n) => {
    if (!n.waveform || !n.waveform.length) return acc;
    const mags = n.waveform.map(c => c.magnitude ?? Math.abs(c));
    return acc + (mags.reduce((a, b) => a + b, 0) / mags.length);
  }, 0) / (total || 1);

  const calcText = `
Nodes: ${total}
Collapsed: ${collapsed}
Avg Magnitude: ${avgMag.toFixed(3)}
Collapse Chance: ${(nodes[0]?.collapseChance ?? '0.05')}
Interference Gain: ${(nodes[0]?.interferenceGain ?? '0.5')}
Phase Angle: ${(nodes[0]?.phase ?? 'variable')}
  `;
  const calcBox = document.getElementById('calcContent');
  if (calcBox) calcBox.textContent = calcText;
}
setInterval(updateCalculations, 5000);

// Rendering
function render() {
  if (!simState) return;
  const canvas = document.getElementById('waveCanvas');
  const ctx = canvas.getContext('2d');
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  const nodeIds = Object.keys(simState);
  const count = nodeIds.length;
  const maxRows = 4;
  const perRow = Math.ceil(count / maxRows);
  const rowHeight = canvas.height / maxRows;

  nodeIds.forEach((nid, idx) => {
    const node = simState[nid];
    const wf = node.waveform;

    // Magnitude and phase (supports dict or number)
    const mags = wf.map(c => c.magnitude ?? Math.abs(c));
    const phases = wf.map(c => (c.phase !== undefined ? c.phase : 0));
    const maxA = Math.max(...mags, 1);
    const scaled = mags.map(a => a / maxA);

    const row = Math.floor(idx / perRow);
    const yOffset = row * rowHeight;

    // Color hue by node index, brightness by avg phase
    const avgPhase = phases.reduce((a, b) => a + b, 0) / (phases.length || 1);
    const hue = (idx * 360 / count);
    const lightness = 50 + 30 * Math.sin(avgPhase);
    ctx.strokeStyle = `hsl(${hue}, 80%, ${lightness}%)`;

    ctx.beginPath();
    scaled.forEach((val, i) => {
      const x = i * (canvas.width / scaled.length);
      const y = yOffset + (1 - val) * (rowHeight - 10) + 5;
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    });
    ctx.stroke();

    // Collapsed marker
    if (node.collapsed) {
      ctx.fillStyle = 'red';
      const collapseX = node.value * (canvas.width / wf.length);
      const collapseY = yOffset + rowHeight / 2;
      ctx.beginPath();
      ctx.arc(collapseX, collapseY, 5, 0, 2 * Math.PI);
      ctx.fill();
    }
  });
}
