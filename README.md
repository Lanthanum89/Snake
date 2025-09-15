# 🐍 Retro Snake Game

A classic Snake game with a nostalgic Nokia 3310 aesthetic, built with Python and Pygame.

![Snake Game](https://img.shields.io/badge/Python-3.x-blue.svg)
![Pygame](https://img.shields.io/badge/Pygame-Required-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🎮 Features

- **Retro Nokia 3310 Design**: Authentic light green background with black pixel graphics
- **Love Heart Food**: Collect adorable heart-shaped food items
- **Power-ups**: Special items that modify gameplay
  - Speed Boost: Increases snake movement speed
  - Slow Down: Decreases snake movement speed  
  - Score Boost: Instantly adds 5 points to your length
- **High Score System**: Tracks your best performance locally
- **Pause Functionality**: Press 'P' to pause/resume the game
- **Progressive Difficulty**: Game speed increases as your score grows
- **Multiple Control Schemes**: Use arrow keys or WASD

## 🕹️ Controls

| Action | Keys |
|--------|------|
| Move Up | ↑ or W |
| Move Down | ↓ or S |
| Move Left | ← or A |
| Move Right | → or D |
| Pause/Resume | P |
| Start Game | Space |
| Quit | Q |
| Play Again | C (after game over) |

## 🚀 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Lanthanum89/Snake.git
   cd Snake
   ```

2. **Install Python 3.x** if you haven't already:
   - Download from [python.org](https://www.python.org/downloads/)

3. **Install Pygame:**
   ```bash
   pip install pygame
   ```

## 🎯 How to Play

1. **Run the game:**
   ```bash
   python snake.py
   ```

2. **Game Rules:**
   - Control the snake to collect heart-shaped food
   - Each heart increases your score and snake length
   - Avoid hitting the walls or your own tail
   - Collect power-ups for special effects
   - Try to beat your high score!

## 📁 File Structure

```
Snake/
│
├── snake.py           # Main game file
├── high_score.json    # High score storage (generated automatically)
└── README.md         # This file
```

## 🎨 Game Elements

- **Snake**: Black rectangular segments with dark green borders
- **Food**: Black heart shapes with decorative borders
- **Power-ups**: Black squares with cross patterns
- **UI**: Retro monospace font displaying score and high score

## ⚙️ Configuration

You can modify game settings in the `Config` class:

```python
class Config:
    WIDTH = 1200          # Window width
    HEIGHT = 800          # Window height
    BLOCK_SIZE = 40       # Size of each game block
    INITIAL_SPEED = 15    # Starting game speed
```

## 🐛 Troubleshooting

**Game won't start:**
- Ensure Python 3.x is installed
- Install Pygame: `pip install pygame`

**Performance issues:**
- Reduce window size in Config class
- Lower the INITIAL_SPEED value

**High score not saving:**
- Ensure the game has write permissions in its directory

## 🤝 Contributing

Feel free to fork this project and submit pull requests for improvements:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🎮 About

This Snake game was created as a tribute to the classic Nokia 3310 Snake game that introduced many people to mobile gaming. The retro aesthetic and simple gameplay capture the essence of early mobile games.

**Score System:**
- Each heart collected = +1 point
- Power-up score boost = +5 points
- Game speed increases every 5 points

**Power-up Details:**
- 5% chance to spawn each game cycle
- Last for 10 seconds if not collected
- Visual cross pattern distinguishes them from food

---

*Enjoy playing this retro Snake game! 🐍💚*