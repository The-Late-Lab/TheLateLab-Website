const launch = document.querySelector('#launch-demo');
const slot = document.querySelector('#demo-slot');
const fullscreen = document.querySelector('#fullscreen-demo');
launch.addEventListener('click', () => {
  const frame = document.createElement('iframe');
  frame.id = 'game-demo';
  frame.className = 'demo-frame';
  frame.title = 'Play Stealthmate browser demo';
  frame.src = '/play/stealthmate/';
  frame.allow = 'fullscreen; clipboard-write; web-share';
  frame.allowFullscreen = true;
  slot.replaceChildren(frame);
  launch.hidden = true;
  fullscreen.hidden = false;
  frame.addEventListener('load', () => frame.focus(), { once: true });
});
fullscreen.addEventListener('click', async () => {
  const frame = document.querySelector('#game-demo');
  if (frame?.requestFullscreen) {
    try { await frame.requestFullscreen(); return; } catch { /* Use the standalone page. */ }
  }
  window.location.assign('/play/stealthmate/');
});
