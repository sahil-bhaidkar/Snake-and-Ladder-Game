import random

# Board configuration
snakes = {14: 7, 31: 26, 38: 1, 84: 28, 95: 73, 99: 78}
ladders = {3: 22, 5: 8, 11: 26, 20: 29, 27: 56, 39: 60, 50: 91, 63: 81, 72: 92}

# Function to roll the dice
def roll_dice():
    return random.randint(1, 6)

# Function to move the player
def move_player(position):
    roll = roll_dice()
    print(f"Rolled a {roll}")
    position += roll

    if position in snakes:
        print(f"Oops! Landed on a snake at {position}. Sliding down to {snakes[position]}.")
        position = snakes[position]
    elif position in ladders:
        print(f"Yay! Landed on a ladder at {position}. Climbing up to {ladders[position]}.")
        position = ladders[position]
    
    return position

# Main game loop
def play_game():
    position = 0
    while position < 100:
        input("Press Enter to roll the dice.")
        position = move_player(position)
        print(f"New position: {position}")
        
        if position >= 100:
            print("Congratulations! You've won the game.")
            break

# Start the game
play_game()
