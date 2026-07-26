// Retro Nokia-3310-style Snake — vanilla canvas game + PWA glue.
(() => {
  "use strict";

  // ---------- Config (mirrors the original pygame version's feel) ----------
  const COLS = 30;
  const ROWS = 20;
  const CELL = 10; // canvas is COLS*CELL x ROWS*CELL internal pixels

  const NOKIA_GREEN = "#9bbc0f";
  const NOKIA_BLACK = "#0f1a0a";
  const NOKIA_DARK_GREEN = "#306230";

  const State = { MENU: 0, PLAYING: 1, GAME_OVER: 2, PAUSED: 3 };

  const HIGH_SCORE_KEY = "snake_high_score";
  const SOUND_KEY = "snake_sound_on";

  // ---------- DOM ----------
  const canvas = document.getElementById("game");
  const ctx = canvas.getContext("2d");
  const soundBtn = document.getElementById("soundBtn");
  const installBtn = document.getElementById("installBtn");
  const dpad = document.getElementById("dpad");
  const softLeft = document.getElementById("softLeft");
  const softRight = document.getElementById("softRight");
  const screenEl = document.getElementById("screen");

  // ---------- Audio (WebAudio bleeps, no assets needed) ----------
  let audioCtx = null;
  let soundOn = localStorage.getItem(SOUND_KEY) !== "off";

  function updateSoundBtn() {
    soundBtn.textContent = "SND: " + (soundOn ? "ON" : "OFF");
  }
  updateSoundBtn();

  function ensureAudio() {
    if (!audioCtx) {
      const AC = window.AudioContext || window.webkitAudioContext;
      if (AC) audioCtx = new AC();
    }
    if (audioCtx && audioCtx.state === "suspended") audioCtx.resume();
  }

  function beep(freq, dur, type = "square", gainVal = 0.06, delay = 0) {
    if (!soundOn || !audioCtx) return;
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    osc.type = type;
    osc.frequency.value = freq;
    gain.gain.value = gainVal;
    osc.connect(gain).connect(audioCtx.destination);
    const t0 = audioCtx.currentTime + delay;
    osc.start(t0);
    gain.gain.setValueAtTime(gainVal, t0);
    gain.gain.exponentialRampToValueAtTime(0.0001, t0 + dur);
    osc.stop(t0 + dur + 0.02);
  }

  const sfx = {
    eat: () => { beep(660, 0.07, "square"); beep(880, 0.08, "square", 0.05, 0.06); },
    powerup: () => { beep(440, 0.05, "triangle"); beep(660, 0.05, "triangle", 0.05, 0.05); beep(880, 0.08, "triangle", 0.05, 0.1); },
    turn: () => beep(140, 0.02, "square", 0.02),
    gameover: () => { beep(200, 0.12, "sawtooth"); beep(140, 0.16, "sawtooth", 0.06, 0.12); beep(90, 0.22, "sawtooth", 0.06, 0.26); },
    select: () => beep(520, 0.04, "square", 0.04),
  };

  soundBtn.addEventListener("click", () => {
    soundOn = !soundOn;
    localStorage.setItem(SOUND_KEY, soundOn ? "on" : "off");
    updateSoundBtn();
    ensureAudio();
    if (soundOn) sfx.select();
  });

  // ---------- Game state ----------
  function loadHighScore() {
    return parseInt(localStorage.getItem(HIGH_SCORE_KEY) || "0", 10);
  }
  function saveHighScore(v) {
    localStorage.setItem(HIGH_SCORE_KEY, String(v));
  }

  let highScore = loadHighScore();
  let state = State.MENU;

  let snake, dir, nextDir, food, powerup, lastStepAt, speedOffset, score;

  function resetGame() {
    const cx = Math.floor(COLS / 2);
    const cy = Math.floor(ROWS / 2);
    snake = [{ x: cx, y: cy }];
    dir = { x: 0, y: 0 };
    nextDir = { x: 0, y: 0 };
    food = randomFoodPosition();
    powerup = null;
    lastStepAt = 0;
    score = 0;
    speedOffset = 0;
  }

  function currentSpeed() {
    return Math.min(40, Math.max(5, adjustSpeed(score) + speedOffset));
  }

  function randomFoodPosition() {
    let pos;
    do {
      pos = { x: (Math.random() * COLS) | 0, y: (Math.random() * ROWS) | 0 };
    } while (snake && snake.some((s) => s.x === pos.x && s.y === pos.y));
    return pos;
  }

  function adjustSpeed(currentScore) {
    return Math.min(10 + Math.floor(currentScore / 5), 25);
  }

  function maybeSpawnPowerup() {
    if (Math.random() * 100 <= 5) {
      const pos = randomFoodPosition();
      const types = ["speed", "slow", "score_boost"];
      const type = types[(Math.random() * types.length) | 0];
      return { pos, type, spawnedAt: performance.now(), duration: 10000 };
    }
    return null;
  }

  resetGame();

  // ---------- Input ----------
  const KEY_DIR = {
    ArrowUp: { x: 0, y: -1 }, w: { x: 0, y: -1 }, W: { x: 0, y: -1 },
    ArrowDown: { x: 0, y: 1 }, s: { x: 0, y: 1 }, S: { x: 0, y: 1 },
    ArrowLeft: { x: -1, y: 0 }, a: { x: -1, y: 0 }, A: { x: -1, y: 0 },
    ArrowRight: { x: 1, y: 0 }, d: { x: 1, y: 0 }, D: { x: 1, y: 0 },
  };

  function requestDir(d) {
    // Ignore reversals and no-ops; only queue perpendicular/forward turns.
    if (dir.x === 0 && dir.y === 0) {
      nextDir = d;
      return;
    }
    if (d.x === -dir.x && d.y === -dir.y) return;
    nextDir = d;
  }

  function startGame() {
    resetGame();
    state = State.PLAYING;
    ensureAudio();
    sfx.select();
  }

  function handleActivate() {
    ensureAudio();
    if (state === State.MENU) startGame();
    else if (state === State.GAME_OVER) startGame();
    else if (state === State.PAUSED) { state = State.PLAYING; sfx.select(); }
  }

  function togglePause() {
    if (state === State.PLAYING) { state = State.PAUSED; sfx.turn(); }
    else if (state === State.PAUSED) { state = State.PLAYING; sfx.select(); }
  }

  window.addEventListener("keydown", (e) => {
    ensureAudio();
    if (e.key === "p" || e.key === "P") { togglePause(); e.preventDefault(); return; }
    if (e.key === " " || e.key === "Enter") {
      if (state === State.MENU || state === State.GAME_OVER) startGame();
      else if (state === State.PAUSED) togglePause();
      e.preventDefault();
      return;
    }
    if (e.key === "c" || e.key === "C") {
      if (state === State.GAME_OVER) startGame();
      return;
    }
    const d = KEY_DIR[e.key];
    if (d && state === State.PLAYING) {
      requestDir(d);
      e.preventDefault();
    }
  });

  // On-screen D-pad
  dpad.addEventListener("click", (e) => {
    const btn = e.target.closest(".dp");
    if (!btn) return;
    ensureAudio();
    const dirName = btn.dataset.dir;
    if (dirName === "pause") {
      if (state === State.MENU || state === State.GAME_OVER) startGame();
      else togglePause();
      return;
    }
    if (state !== State.PLAYING) { handleActivate(); return; }
    const map = { up: { x: 0, y: -1 }, down: { x: 0, y: 1 }, left: { x: -1, y: 0 }, right: { x: 1, y: 0 } };
    requestDir(map[dirName]);
  });

  softLeft.addEventListener("click", () => { ensureAudio(); state = State.MENU; sfx.select(); });
  softRight.addEventListener("click", handleActivate);

  // Tap / swipe directly on the LCD screen
  let touchStart = null;
  screenEl.addEventListener("touchstart", (e) => {
    ensureAudio();
    const t = e.changedTouches[0];
    touchStart = { x: t.clientX, y: t.clientY };
  }, { passive: true });

  screenEl.addEventListener("touchend", (e) => {
    if (!touchStart) return;
    const t = e.changedTouches[0];
    const dx = t.clientX - touchStart.x;
    const dy = t.clientY - touchStart.y;
    const absX = Math.abs(dx), absY = Math.abs(dy);
    const SWIPE_THRESHOLD = 18;

    if (absX < SWIPE_THRESHOLD && absY < SWIPE_THRESHOLD) {
      handleActivate();
    } else if (state === State.PLAYING) {
      if (absX > absY) requestDir({ x: dx > 0 ? 1 : -1, y: 0 });
      else requestDir({ x: 0, y: dy > 0 ? 1 : -1 });
    }
    touchStart = null;
  });

  // ---------- Drawing helpers ----------
  function drawCell(x, y, fill, borderColor) {
    ctx.fillStyle = fill;
    ctx.fillRect(x * CELL, y * CELL, CELL, CELL);
    if (borderColor) {
      ctx.strokeStyle = borderColor;
      ctx.lineWidth = 1;
      ctx.strokeRect(x * CELL + 0.5, y * CELL + 0.5, CELL - 1, CELL - 1);
    }
  }

  function drawSnake() {
    for (const seg of snake) drawCell(seg.x, seg.y, NOKIA_BLACK, NOKIA_DARK_GREEN);
  }

  function drawHeart(cx, cy, size, color) {
    ctx.fillStyle = color;
    const r = size / 2;
    ctx.beginPath();
    ctx.arc(cx - r, cy - r * 0.6, r, 0, Math.PI * 2);
    ctx.arc(cx + r, cy - r * 0.6, r, 0, Math.PI * 2);
    ctx.fill();
    ctx.beginPath();
    ctx.moveTo(cx - size, cy - size * 0.15);
    ctx.lineTo(cx + size, cy - size * 0.15);
    ctx.lineTo(cx, cy + size);
    ctx.closePath();
    ctx.fill();
  }

  function drawFood() {
    const cx = food.x * CELL + CELL / 2;
    const cy = food.y * CELL + CELL / 2;
    drawHeart(cx, cy, CELL * 0.42, NOKIA_BLACK);
  }

  function drawPowerup() {
    if (!powerup) return;
    const { x, y } = powerup.pos;
    drawCell(x, y, NOKIA_BLACK, null);
    ctx.strokeStyle = NOKIA_GREEN;
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(x * CELL, y * CELL + CELL / 2);
    ctx.lineTo(x * CELL + CELL, y * CELL + CELL / 2);
    ctx.moveTo(x * CELL + CELL / 2, y * CELL);
    ctx.lineTo(x * CELL + CELL / 2, y * CELL + CELL);
    ctx.stroke();
  }

  function pixelFont(px, bold = true) {
    return `${bold ? "bold " : ""}${px}px "Courier New", monospace`;
  }

  function centerText(text, y, px, color = NOKIA_BLACK) {
    ctx.fillStyle = color;
    ctx.font = pixelFont(px);
    ctx.textAlign = "center";
    ctx.fillText(text, canvas.width / 2, y);
  }

  function clearScreen() {
    ctx.fillStyle = NOKIA_GREEN;
    ctx.fillRect(0, 0, canvas.width, canvas.height);
  }

  function showScore() {
    ctx.textAlign = "left";
    ctx.fillStyle = NOKIA_BLACK;
    ctx.font = pixelFont(10);
    ctx.fillText(`SCORE:${String(score).padStart(4, "0")}`, 4, 12);
    ctx.fillText(`HIGH:${String(highScore).padStart(4, "0")}`, 4, 24);
  }

  function drawMenu() {
    clearScreen();
    centerText("SNAKE", canvas.height * 0.36, 26);
    centerText("PRESS SPACE", canvas.height * 0.62, 10);
    centerText("OR TAP TO START", canvas.height * 0.62 + 13, 10);
    centerText(`HIGH SCORE ${String(highScore).padStart(4, "0")}`, canvas.height - 10, 8);
  }

  function drawPauseOverlay() {
    ctx.fillStyle = NOKIA_DARK_GREEN;
    const step = 5;
    for (let x = 0; x < canvas.width; x += step) {
      for (let y = 0; y < canvas.height; y += step) {
        if ((x + y) % (step * 2) === 0) ctx.fillRect(x, y, 2, 2);
      }
    }
    centerText("PAUSED", canvas.height / 2 - 8, 16);
    centerText("PRESS P TO RESUME", canvas.height / 2 + 10, 8);
  }

  function drawGameOver() {
    clearScreen();
    centerText("GAME OVER", canvas.height * 0.32, 18);
    showScore();
    centerText("PRESS C TO RETRY", canvas.height * 0.62, 9);
    centerText("OR TAP SCREEN", canvas.height * 0.62 + 12, 9);
  }

  // ---------- Game step ----------
  function step() {
    dir = nextDir;
    if (dir.x === 0 && dir.y === 0) return; // hasn't moved yet

    const head = { x: snake[0].x + dir.x, y: snake[0].y + dir.y };

    if (head.x < 0 || head.x >= COLS || head.y < 0 || head.y >= ROWS) {
      return endGame();
    }
    if (snake.some((s) => s.x === head.x && s.y === head.y)) {
      return endGame();
    }

    snake.unshift(head);

    let grew = false;
    if (head.x === food.x && head.y === food.y) {
      grew = true;
      food = randomFoodPosition();
      score += 1;
      sfx.eat();
    }

    if (powerup && head.x === powerup.pos.x && head.y === powerup.pos.y) {
      if (powerup.type === "speed") speedOffset += 5;
      else if (powerup.type === "slow") speedOffset -= 5;
      else if (powerup.type === "score_boost") { score += 5; for (let i = 0; i < 5; i++) snake.push({ ...snake[snake.length - 1] }); }
      powerup = null;
      sfx.powerup();
    }

    if (!grew) snake.pop();

    if (!powerup || performance.now() - powerup.spawnedAt > powerup.duration) {
      powerup = maybeSpawnPowerup();
    }

    if (score > highScore) {
      highScore = score;
      saveHighScore(highScore);
    }
  }

  function endGame() {
    state = State.GAME_OVER;
    sfx.gameover();
    if (navigator.vibrate) navigator.vibrate([60, 40, 120]);
  }

  // ---------- Main loop ----------
  function frame(ts) {
    requestAnimationFrame(frame);

    if (state === State.PLAYING) {
      const stepInterval = 1000 / currentSpeed();
      if (ts - lastStepAt >= stepInterval) {
        lastStepAt = ts;
        step();
      }
      clearScreen();
      drawSnake();
      drawFood();
      drawPowerup();
      showScore();
    } else if (state === State.MENU) {
      drawMenu();
    } else if (state === State.PAUSED) {
      clearScreen();
      drawSnake();
      drawFood();
      drawPowerup();
      showScore();
      drawPauseOverlay();
    } else if (state === State.GAME_OVER) {
      drawGameOver();
    }
  }

  requestAnimationFrame(frame);

  // ---------- PWA: service worker + install prompt ----------
  if ("serviceWorker" in navigator) {
    window.addEventListener("load", () => {
      navigator.serviceWorker.register("sw.js").catch(() => {});
    });
  }

  let deferredInstallPrompt = null;
  window.addEventListener("beforeinstallprompt", (e) => {
    e.preventDefault();
    deferredInstallPrompt = e;
    installBtn.hidden = false;
  });

  installBtn.addEventListener("click", async () => {
    if (!deferredInstallPrompt) return;
    installBtn.hidden = true;
    deferredInstallPrompt.prompt();
    await deferredInstallPrompt.userChoice;
    deferredInstallPrompt = null;
  });

  window.addEventListener("appinstalled", () => {
    installBtn.hidden = true;
  });
})();
