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
    const absvals = wf.map(c => Math.abs(c));
    const maxA = Math.max(...absvals) || 1;
    const scaled = absvals.map(a => a / maxA);

    const row = Math.floor(idx / perRow);
    const yOffset = row * rowHeight;

    ctx.strokeStyle = `hsl(${(idx * 360 / count)}, 80%, 60%)`;
    ctx.beginPath();
    wf.forEach((c, i) => {
      const x = i * (canvas.width / wf.length);
      const y = yOffset + (1 - scaled[i]) * (rowHeight - 10) + 5;
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    });
    ctx.stroke();
  });
}
