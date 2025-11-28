// app.js — connect to backend, receive state, draw waveforms
const socket = io();

let simState = null;
let paused = false;

socket.on('state', state => {
  simState = state;
  if (!paused) render();
});

document.getElementById('pauseBtn').onclick = () => {
  paused = !paused;
};

document.getElementById('resetBtn').onclick = () => {
  location.reload();
};

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

    // Extract magnitudes and phases
    const absvals = wf.map(c => Math.abs(c.magnitude ?? c)); // handle dict or raw number
    const phases = wf.map(c => (c.phase !== undefined ? c.phase : 0));
    const maxA = Math.max(...absvals) || 1;
    const scaled = absvals.map(a => a / maxA);

    const row = Math.floor(idx / perRow);
    const yOffset = row * rowHeight;

    // Color hue by node index, brightness by average phase
    const avgPhase = phases.reduce((a, b) => a + b, 0) / phases.length;
    const hue = (idx * 360 / count);
    const lightness = 50 + 30 * Math.sin(avgPhase); // vary brightness with phase
    ctx.strokeStyle = `hsl(${hue}, 80%, ${lightness}%)`;

    ctx.beginPath();
    scaled.forEach((val, i) => {
      const x = i * (canvas.width / scaled.length);
      const y = yOffset + (1 - val) * (rowHeight - 10) + 5;
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    });
    ctx.stroke();

    // Highlight collapsed nodes
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
