import tkinter as tk
import random
from tkinter.simpledialog import askinteger, askstring, askyesno

# Board configuration
snakes = {14: 7, 31: 26, 38: 1, 84: 28, 95: 73, 99: 78}
ladders = {3: 22, 5: 8, 11: 26, 20: 29, 27: 56, 39: 60, 50: 91, 63: 81, 72: 92}

class SnakeAndLadder:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake and Ladder Game")
        self.board_size = 10
        self.cell_size = 50
        self.players = []
        self.num_players = 1
        self.current_player = 0

        self.setup_game()
        self.create_board()
        self.create_ui()

    def setup_game(self):
        # Ask if the user wants to play with multiple players
        if askyesno("Multiplayer", "Do you want to play with multiple players?"):
            self.num_players = askinteger("Number of Players", "Enter the number of players:", minvalue=2, maxvalue=4)
        for i in range(self.num_players):
            self.players.append({
                "name": askstring("Player Name", f"Enter the name for Player {i + 1}:") or f"Player {i + 1}",
                "position": 0,
                "color": self.random_color()
            })

    def random_color(self):
        return "#{:06x}".format(random.randint(0, 0xFFFFFF))

    def create_board(self):
        self.board = tk.Canvas(self.root, width=self.board_size * self.cell_size, height=self.board_size * self.cell_size)
        self.board.grid(row=0, column=0, columnspan=3)

        self.cells = {}
        colors = ["#D2B48C", "#8FBC8F"]
        for i in range(100):
            row, col = divmod(i, self.board_size)
            col = col if row % 2 == 1 else self.board_size - 1 - col
            cell_number = 100 - i
            x1, y1 = col * self.cell_size, row * self.cell_size
            x2, y2 = x1 + self.cell_size, y1 + self.cell_size
            color = colors[(row + col) % 2]
            self.cells[cell_number] = self.board.create_rectangle(x1, y1, x2, y2, fill=color)
            self.board.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=str(cell_number), font=("Arial", 12, "bold"))

        self.draw_lines(snakes, "red")
        self.draw_lines(ladders, "green")

        self.player_ovals = []
        for player in self.players:
            player_oval = self.board.create_oval(0, 0, self.cell_size, self.cell_size, fill=player["color"])
            self.player_ovals.append(player_oval)
        self.update_board()

    def draw_lines(self, mapping, color):
        for start, end in mapping.items():
            self.draw_line(start, end, color)

    def draw_line(self, start, end, color):
        start_x, start_y = self.get_cell_center(start)
        end_x, end_y = self.get_cell_center(end)
        self.board.create_line(start_x, start_y, end_x, end_y, fill=color, width=2)

    def get_cell_center(self, position):
        row, col = divmod(100 - position, self.board_size)
        col = col if row % 2 == 1 else self.board_size - 1 - col
        x = col * self.cell_size + self.cell_size // 2
        y = row * self.cell_size + self.cell_size // 2
        return x, y

    def create_ui(self):
        self.message = tk.Label(self.root, text="Press the button to roll the dice.", font=("Arial", 14))
        self.message.grid(row=1, column=0, columnspan=3, pady=10)

        self.roll_button = tk.Button(self.root, text="Roll Dice", command=self.play_game, font=("Arial", 14))
        self.roll_button.grid(row=2, column=1)

    def roll_dice(self):
        return random.randint(1, 6)

    def move_player(self):
        current = self.players[self.current_player]
        roll = self.roll_dice()
        self.message['text'] = f"{current['name']} rolled a {roll}"

        if current['position'] + roll > 100:
            self.message['text'] += "\nRoll exceeds final position. Try again next turn."
        else:
            current['position'] += roll

            if current['position'] in snakes:
                self.message['text'] += f"\nOops! {current['name']} landed on a snake at {current['position']}. Sliding down to {snakes[current['position']]}."
                current['position'] = snakes[current['position']]
            elif current['position'] in ladders:
                self.message['text'] += f"\nYay! {current['name']} landed on a ladder at {current['position']}. Climbing up to {ladders[current['position']]}."
                current['position'] = ladders[current['position']]

            self.message['text'] += f"\n{current['name']}'s new position: {current['position']}"
            self.update_board()

            if current['position'] == 100:
                self.message['text'] += f"\nCongratulations! {current['name']} has won the game."
                self.roll_button.config(state=tk.DISABLED)
            else:
                self.current_player = (self.current_player + 1) % self.num_players
                self.message['text'] += f"\n{self.players[self.current_player]['name']}'s turn."

    def update_board(self):
        for i, player in enumerate(self.players):
            if player['position'] > 100:
                player['position'] = 100
            x1, y1 = self.get_cell_top_left(player['position'])
            x2, y2 = x1 + self.cell_size, y1 + self.cell_size
            self.board.coords(self.player_ovals[i], x1, y1, x2, y2)

    def get_cell_top_left(self, position):
        row, col = divmod(99 - position, self.board_size)
        col = col if row % 2 == 1 else self.board_size - 1 - col
        x, y = col * self.cell_size, row * self.cell_size
        return x, y

    def play_game(self):
        self.move_player()

root = tk.Tk()
game = SnakeAndLadder(root)
root.mainloop()
