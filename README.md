# Chess Variant AI Project - Advanced Chess with Fantasy Elements  

## 📌 Introduction  
This is an advanced chess game with fantasy elements. It features teleport squares, pawn replication, and an AI opponent using the Minimax algorithm with alpha-beta pruning. The game is built using Python, with `pygame` for graphics and `chess` for board logic.

## 🚀 Features  
- Player vs Player (PvP) Mode  
- Player vs AI Mode (Minimax AI with alpha-beta pruning)  
- Magic Squares:  
  - Teleport Squares (Blue): Instantly move between two linked squares.  
  - Replicate Squares (Purple): Duplicate a pawn forward.  
- Interactive Graphical Interface using Pygame  
- Sound Toggle: On/off music control  
- Error Handling: Manages missing images or sound without crashing  

## ⚙️ Technologies Used  
- Language: Python  
- Libraries:  
  - pygame: For graphical interface and user interaction  
  - chess: For handling chess rules, board state, and moves  


## 🚦 How to Run  
python main.py  
 

## 📝 Gameplay Instructions  
- **Main Menu:**  
  - Press **1** for Player vs Player (PvP)  
  - Press **2** for Player vs AI  

- **Magic Square Rules:**  
  - **Teleport Squares (Blue):** Step on one to appear at the other.  
  - **Replicate Squares (Purple):** Step on one with a pawn to duplicate it forward.  

- **Sound Control:** Click the sound icon to toggle music.  

---

## 💡 AI Mechanics  
- **Algorithm:** Minimax with alpha-beta pruning  
- **Difficulty:** Set to depth 2 (adjustable in code)  
- **Evaluation Function:** Based on standard chess piece values:  
  - 🟢 Pawn: 1  
  - 🟣 Knight: 3  
  - 🔵 Bishop: 3  
  - 🔴 Rook: 5  
  - 🟡 Queen: 9  

---

## ⚠️ Troubleshooting  
- **Sound Not Playing:** Ensure `win.mp3` is in the same directory.  
- **Image Errors:** Make sure piece images are named correctly (e.g., `white_pawn.png`).  
- **Slow Performance:** Increase Minimax depth carefully (higher values slow down AI).  

---

## ✨ Future Enhancements  
- Add more difficulty levels for AI  
- Add multiplayer mode (online)  
- Improve piece animations  
- Add customizable game settings  

---

## 📌 Contributors  
- **Muhammad Umar Farooq (22k-4218)**  
- **Syed Muhammad Abubakar (22k-4184)**  
- **Timotheous Ayub (22k-4547)**  
