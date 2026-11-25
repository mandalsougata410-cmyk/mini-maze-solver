# 🧀 Mini Maze Cheese Collector & Solver

An interactive, visual web-based solver for the **Mini Maze Cheese Collection** problem. The mouse starts at `(0, 0)`, must collect all pieces of cheese `🧀` scattered throughout the maze, and finally reach the destination goal `🏁` at `(R - 1, C - 1)` in the minimum number of steps without hitting walls.

---

## 🚀 Live Demo & Web App
- Open `index.html` directly in any web browser!

---

## 🧠 Algorithms Used

1. **Multi-Source Breadth-First Search (BFS)**:
   - Computes all-pairs shortest paths between the Start, each Cheese location, and the Goal.
   - Reconstructs exact move sequences (`U`, `D`, `L`, `R`).
2. **Traveling Salesperson Problem (TSP) with Bitmask Dynamic Programming**:
   - Optimal bitmask DP ($O(N^2 \cdot 2^N)$ where $N$ is the count of cheeses) to find the exact minimum-cost permutation of cheese collection before heading to the goal.

---

## 📁 Repository Contents

- `index.html`: Fully self-contained web app with interactive grid editor, animation controls, speed slider, and statistics.
- `mini_maze_solver.py`: Original Python implementation with 10 built-in test suites.

---

## 🏃 Running the Python Code
```bash
python mini_maze_solver.py
```
