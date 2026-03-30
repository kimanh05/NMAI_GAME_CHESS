# ♟️ Mini Chess AI – AlphaBeta vs MCTS

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Pygame](https://img.shields.io/badge/Pygame-2.6-green)

---

## 📌 Introduction

This project implements a simplified version of chess (**Mini Chess**) with a graphical user interface and AI opponents.

The system supports:
- Human vs Human
- Human vs AI (Alpha-Beta / MCTS)
- AI vs AI simulation

The project is designed for learning **Artificial Intelligence + Game Development**.

---

## 🎯 Objectives

- Build a playable chess-like game using Python
- Implement game logic (legal moves, check, checkmate, draw)
- Develop AI players:
  - Alpha-Beta Pruning
  - Monte Carlo Tree Search (MCTS)
- Design interactive GUI using **Pygame**
- Structure code for teamwork and scalability

---

## 🧠 Features

### 🎮 Gameplay
- 8x8 board (simplified setup)
- Legal move validation
- Check & Checkmate detection
- Draw conditions:
  - Only kings left
  - Stalemate

### 🤖 AI Modes
- Human vs Human
- Human vs Alpha-Beta AI
- Human vs MCTS AI
- AI vs AI

### 🖥️ GUI
- Click-based control (no keyboard required)
- Highlight valid moves
- Highlight king when in check
- Game over popup (center screen)
- Timer display (auto freeze when game ends)
- Buttons:
  - Restart
  - Menu
  - Quit

---

## 🗂️ Project Structure

```bash
mini_chess/
│
├── main.py              # Entry point
├── config.py            # Game configuration
│
├── core/                # Game logic
│   ├── board.py
│   ├── move.py
│   ├── pieces.py
│   ├── rules.py
│   ├── game_state.py
│   └── game_manager.py
│
├── gui/                 # UI rendering
│   ├── renderer.py
│   ├── input_handler.py
│   └── assets/          # Chess images
│
├── ai/                  # AI algorithms
│   ├── ai_interface.py
│   ├── alphabeta.py
│   └── mcts.py
│
└── tests/