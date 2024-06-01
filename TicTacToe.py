from tkinter import *
from tkinter import Tk, Label, font, Canvas, messagebox

# Constants
WIN_CONDITIONS = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]

# Global Variables
positions = ['-', '-', '-', '-', '-', '-', '-', '-', '-']
turn = 1  # 1 for player, 0 for AI
turns = 0
gameOver = False
playerCharacter = 'X'
aiCharacter = 'O'
winLabel = None

# Tkinter Setup
root = Tk()
root.title("Tic-Tac-Toe")
# root.iconbitmap(r"C:\Users\ernes\Downloads\images.ico")
root.configure(bg="darkgrey")

# Fonts
aphos_font = font.Font(family="Aphos", size=25, weight="bold")
largeFont = font.Font(family="Helvetica", size=30, weight="bold")

# Functions
def create_rounded_button(parent, text, command, font, fg, bg, corner=10, **kwargs):
    button = Canvas(parent, highlightthickness=0, bg=bg)
    button.round_rect = button.create_rounded_rectangle(0, 0, 100, 100, corner, fill=bg, outline="")
    button.text = button.create_text(50, 50, text=text, font=font, fill=fg, anchor="center")
    button.config(width=100, height=100)
    button.bind("<Button-1>", lambda event: command())
    button.bind("<Enter>", lambda event: button.config(bg="lightgrey"))
    button.bind("<Leave>", lambda event: button.config(bg=bg))
    button.grid(**kwargs)
    return button

def create_rounded_rectangle(self, x1, y1, x2, y2, radius, **kwargs):
    points = [x1 + radius, y1,
              x1 + radius, y1,
              x2 - radius, y1,
              x2 - radius, y1,
              x2, y1,
              x2, y1 + radius,
              x2, y1 + radius,
              x2, y2 - radius,
              x2, y2 - radius,
              x2, y2,
              x2 - radius, y2,
              x2 - radius, y2,
              x1 + radius, y2,
              x1 + radius, y2,
              x1, y2,
              x1, y2 - radius,
              x1, y2 - radius,
              x1, y1 + radius,
              x1, y1 + radius,
              x1, y1]
    return self.create_polygon(points, **kwargs, smooth=True)

Canvas.create_rounded_rectangle = create_rounded_rectangle

def checkGameOver(pos):
    global gameOver
    for (a, b, c) in WIN_CONDITIONS:
        if pos[a] == pos[b] == pos[c] and pos[a] != '-':
            gameOver = True
            show_popup(f'{pos[a]} Wins!')
            return gameOver
    if '-' not in pos:
        gameOver = True
        show_popup('Draw!')
        return gameOver
    gameOver = False
    return gameOver

def show_popup(message):
    play_again = messagebox.askyesno("Game Over", f"{message}\nDo you want to play again?")
    if play_again:
        reset_game()
    else:
        root.quit()

def aiTurn():
    global turns, turn, positions, gameOver
    if turn == 0 and not gameOver:
        bestScore = float('-inf')
        bestMove = None
        for i in range(9):
            if positions[i] == '-':
                positions[i] = aiCharacter
                score = minimax(positions, 0, False)
                positions[i] = '-'
                if score > bestScore:
                    bestScore = score
                    bestMove = i
        if bestMove is not None:
            positions[bestMove] = aiCharacter
            update_board()
            gameOver = checkGameOver(positions)
            turn = 1
            turns += 1

def minimax(board, depth, isMaximizing):
    scores = {aiCharacter: 10, playerCharacter: -10, 'tie': 0}
    result = checkWinner()
    if result:
        return scores[result]

    if isMaximizing:
        bestScore = float('-inf')
        for i in range(9):
            if board[i] == '-':
                board[i] = aiCharacter
                score = minimax(board, depth + 1, False)
                board[i] = '-'
                bestScore = max(score, bestScore)
        return bestScore - depth  # Subtract depth to prioritize quicker wins
    else:
        bestScore = float('inf')
        for i in range(9):
            if board[i] == '-':
                board[i] = playerCharacter
                score = minimax(board, depth + 1, True)
                board[i] = '-'
                bestScore = min(score, bestScore)
        return bestScore + depth  # Add depth to prioritize delayed losses

def checkWinner():
    for (a, b, c) in WIN_CONDITIONS:
        if positions[a] == positions[b] == positions[c] and positions[a] != '-':
            return positions[a]
    if '-' not in positions:
        return 'tie'
    return None

def xSelect():
    global playerCharacter, aiCharacter, turn
    playerCharacter = 'X'
    aiCharacter = 'O'
    turn = 1
    Label(root, text=f'You have selected {playerCharacter}', bg="darkgrey", font=aphos_font).grid(row=3, column=0, sticky='nesw', columnspan=3)
    Button(root, text='Start', command=draw_board, bg="lightgrey", font=aphos_font).grid(row=4, column=0, columnspan=3)
    xButton.config(state="disabled")
    oButton.config(state="disabled")

def oSelect():
    global playerCharacter, aiCharacter, turn
    playerCharacter = 'O'
    aiCharacter = 'X'
    turn = 0  # Set turn to 0 so AI makes the first move after starting
    Label(root, text=f'You have selected {playerCharacter}', bg="darkgrey", font=aphos_font).grid(row=3, column=0, sticky='nesw', columnspan=3)
    Button(root, text='Start', command=draw_board, bg="lightgrey", font=aphos_font).grid(row=4, column=0, columnspan=3)
    xButton.config(state="disabled")
    oButton.config(state="disabled")

def playerPos(pos):
    global turn, turns, positions, gameOver
    if turn == 1 and turns < 9 and not gameOver:
        if positions[pos] == '-':
            positions[pos] = playerCharacter
            update_board()
            gameOver = checkGameOver(positions)
            turn = 0
            turns += 1
            if not gameOver:
                aiTurn()

def update_board():
    for i in range(9):
        if 0 <= i <= 2:
            r = 5
        elif 3 <= i <= 5:
            r = 6
        else:
            r = 7
        c = i % 3
        color = "red" if positions[i] == "X" else "blue" if positions[i] == "O" else "black"
        create_rounded_button(root, text=positions[i], command=lambda i=i: playerPos(i), font=largeFont, fg=color, bg="lightgrey", corner=20).grid(row=r, column=c, sticky='nesw', padx=5, pady=5)

def draw_board():
    global positions, turn, turns, gameOver, winLabel
    turn = 1 if playerCharacter == 'X' else 0  # Player goes first if 'X', otherwise AI goes first
    turns = 0
    gameOver = False
    positions = ['-', '-', '-', '-', '-', '-', '-', '-', '-']
    update_board()
    if winLabel:
        winLabel.destroy()
    winLabel = Label(root, text='         ', font=largeFont, bg="darkgrey")
    winLabel.grid(row=8, column=0, columnspan=3)
    if turn == 0:
        aiTurn()

def reset_game():
    global playerCharacter, aiCharacter
    playerCharacter = 'X'
    aiCharacter = 'O'
    xButton.config(state="normal")
    oButton.config(state="normal")
    for widget in root.winfo_children():
        if isinstance(widget, Button) and widget.cget('text') == 'Start':
            widget.destroy()
    draw_board()

# Widgets
mainLabel = Label(root, text='Welcome to Tic-Tac-Toe!', bg="darkgrey", font=aphos_font)
playerSelectLabel = Label(root, text='Select a character to play as', bg="darkgrey", font=aphos_font)
xButton = Button(root, text='X', command=xSelect, font=aphos_font, bg="lightgrey", fg="red")
oButton = Button(root, text='O', command=oSelect, font=aphos_font, bg="lightgrey", fg="blue")

# Grid Layout
mainLabel.grid(row=0, column=0, columnspan=3)
playerSelectLabel.grid(row=1, column=0, columnspan=3)
xButton.grid(row=2, column=0, sticky='ew')
oButton.grid(row=2, column=2, sticky='ew')

# Configure grid to make widgets resize with window
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_rowconfigure(4, weight=1)
root.grid_rowconfigure(5, weight=1)
root.grid_rowconfigure(6, weight=1)
root.grid_rowconfigure(7, weight=1)
root.grid_rowconfigure(8, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

# Main Loop
root.mainloop()
