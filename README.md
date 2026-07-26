# 🐍 Retro Snake — PWA

A classic Snake game with a nostalgic monochrome LCD handset aesthetic, rendered on HTML5 canvas and installable as an offline-capable Progressive Web App. A Python/Pygame version of the original game is also included.

![PWA](https://img.shields.io/badge/PWA-Installable-5A0FC8.svg)
![Offline](https://img.shields.io/badge/Offline-Supported-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🎮 Play it

Open `index.html` through any static web server (opening the file directly with `file://` will work for the game itself, but service worker registration requires `http://`/`https://`):

```bash
python3 -m http.server 8000
# then visit http://localhost:8000/ in a browser
```

Or deploy the folder as-is to any static host (GitHub Pages, Netlify, Vercel, etc.) — there's no build step.

### Install as an app

Once served over `http(s)://`, browsers that support PWAs (Chrome, Edge, Android, and "Add to Home Screen" on iOS Safari) will let you install Retro Snake like a native app. It then runs full-screen, with its own icon, and works fully offline after the first load.

## 🕹️ Controls

| Action | Input |
|--------|-------|
| Move | Arrow keys, WASD, on-screen D-pad, or swipe the screen |
| Pause / Resume | `P`, the D-pad's center button, or tap the screen |
| Start | `Space` / `Enter`, or tap the screen |
| Play again (after game over) | `C`, or tap the screen |
| Mute / unmute | `SND` button |

The on-screen D-pad and phone shell are shown automatically on touch devices; keyboard controls work everywhere.

## 🎨 Features

- **Retro LCD handset look**: pixel-art phone shell, green monochrome screen, scanlines, vignette, and a subtle CRT flicker
- **Chunky pixel-art rendering**: crisp, non-antialiased canvas scaling for an authentic low-res feel
- **Love Heart Food**: collect heart-shaped food to grow and score
- **Power-ups**: speed boost, slow-down, and instant +5 score, each with a distinct visual and sound cue
- **8-bit WebAudio bleeps**: no audio files — all sound effects are synthesized in-browser, with a mute toggle
- **High Score System**: saved locally (`localStorage`), persists across sessions
- **Pause overlay** with the classic dithered-screen effect
- **Progressive Difficulty**: speed increases as your score grows
- **Installable PWA**: manifest + service worker cache the app shell for offline play
- **Touch-friendly**: on-screen D-pad and swipe gestures for mobile

## 📁 File Structure

```
Snake/
│
├── index.html              # App shell / phone-shaped screen markup
├── style.css                # Retro handset styling, CRT effects, responsive layout
├── app.js                   # Game logic, rendering, audio, PWA registration
├── manifest.webmanifest     # PWA manifest (name, icons, colors, display mode)
├── sw.js                    # Service worker (offline caching)
├── icons/                   # Generated app icons (regular + maskable + favicons)
│
├── snake.py                 # Original Python/Pygame desktop version
├── high_score.json          # High score storage for the Python version
└── README.md
```

## ⚙️ Configuration

Grid size, colors, and speed curve live at the top of `app.js`:

```js
const COLS = 30;
const ROWS = 20;
const CELL = 10;

const NOKIA_GREEN = "#9bbc0f";
const NOKIA_BLACK = "#0f1a0a";
```

## 🐍 Legacy: Python/Pygame version

The original desktop version (`snake.py`) still works and is kept for reference.

```bash
pip install pygame
python snake.py
```

Same rules apply: arrow keys/WASD to move, `P` to pause, `Q` to quit, `Space` to start, `C` to restart after game over.

## 🤝 Contributing

Feel free to fork this project and submit pull requests for improvements:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

---

*Enjoy playing this retro Snake game! 🐍💚*
