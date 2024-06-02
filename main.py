import tkinter as tk
import random

# Board configuration
snakes = {14: 7, 38: 1, 84: 28, 95: 73, 99: 78}
ladders = {3: 22, 11: 26, 27: 56, 39: 60, 50: 91, 63: 81, 72: 92}

class SnakeAndLadder:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake and Ladder Game")
        self.board_size = 10
        self.cell_size = 50
        self.position = 0

        self.create_board()
        self.create_ui()
        
    def create_board(self):
        self.board = tk.Canvas(self.root, width=self.board_size*self.cell_size, height=self.board_size*self.cell_size)
        self.board.grid(row=0, column=0, columnspan=3)
        
        self.cells = {}
        colors = ["#D2B48C", "#8FBC8F"]
        for i in range(100):
            row = i // self.board_size
            col = i % self.board_size
            if row % 2 == 0:
                col = self.board_size - 1 - col
            cell_number = 100 - i
            x1 = col * self.cell_size
            y1 = row * self.cell_size
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size
            color = colors[(row + col) % 2]
            self.cells[cell_number] = self.board.create_rectangle(x1, y1, x2, y2, fill=color)
            self.board.create_text(x1 + self.cell_size//2, y1 + self.cell_size//2, text=str(cell_number))

        for start, end in snakes.items():
            self.draw_line(start, end, "red")
        for start, end in ladders.items():
            self.draw_line(start, end, "green")
        
        self.player = self.board.create_oval(0, 0, self.cell_size, self.cell_size, fill="yellow")
        self.update_board()
        
    def draw_line(self, start, end, color):
        start_row, start_col = divmod(100 - start, self.board_size)
        end_row, end_col = divmod(100 - end, self.board_size)
        if start_row % 2 == 0:
            start_col = self.board_size - 1 - start_col
        if end_row % 2 == 0:
            end_col = self.board_size - 1 - end_col

        x1 = start_col * self.cell_size + self.cell_size // 2
        y1 = start_row * self.cell_size + self.cell_size // 2
        x2 = end_col * self.cell_size + self.cell_size // 2
        y2 = end_row * self.cell_size + self.cell_size // 2
        self.board.create_line(x1, y1, x2, y2, fill=color, width=2)
    
    def create_ui(self):
        self.message = tk.Label(self.root, text="Press the button to roll the dice.")
        self.message.grid(row=1, column=0, columnspan=3)
        
        self.roll_button = tk.Button(self.root, text="Roll Dice", command=self.play_game)
        self.roll_button.grid(row=2, column=1)
        
    def roll_dice(self):
        return random.randint(1, 6)
    
    def move_player(self):
        roll = self.roll_dice()
        self.message['text'] = f"Rolled a {roll}"
        self.position += roll
        
        if self.position in snakes:
            self.message['text'] += f"\nOops! Landed on a snake at {self.position}. Sliding down to {snakes[self.position]}."
            self.position = snakes[self.position]
        elif self.position in ladders:
            self.message['text'] += f"\nYay! Landed on a ladder at {self.position}. Climbing up to {ladders[self.position]}."
            self.position = ladders[self.position]
        
        self.message['text'] += f"\nNew position: {self.position}"
        self.update_board()
        
        if self.position >= 100:
            self.message['text'] += "\nCongratulations! You've won the game."
            self.roll_button.config(state=tk.DISABLED)
    
    def update_board(self):
        row = (100 - self.position) // self.board_size
        col = (100 - self.position) % self.board_size
        if row % 2 == 0:
            col = self.board_size - 1 - col
        x1 = col * self.cell_size
        y1 = row * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        self.board.coords(self.player, x1, y1, x2, y2)
    
    def play_game(self):
        self.move_player()

root = tk.Tk()
game = SnakeAndLadder(root)
root.mainloop()