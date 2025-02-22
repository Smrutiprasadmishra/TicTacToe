import os
import platform
import random


class Board:
    def __init__(self):
        self.cells = [" "] * 10  # Index 0 is unused

    def display(self):
        print("\n")
        print(" %s | %s | %s " % (self.cells[1], self.cells[2], self.cells[3]))
        print("-----------")
        print(" %s | %s | %s " % (self.cells[4], self.cells[5], self.cells[6]))
        print("-----------")
        print(" %s | %s | %s " % (self.cells[7], self.cells[8], self.cells[9]))
        print("\n")

    def update_cell(self, cell_no, player):
        if self.cells[cell_no] == " ":
            self.cells[cell_no] = player

    def is_winner(self, player):
        winning_combinations = [
            [1, 2, 3], [4, 5, 6], [7, 8, 9],
            [1, 4, 7], [2, 5, 8], [3, 6, 9],
            [1, 5, 9], [3, 5, 7]
        ]
        return any(all(self.cells[cell] == player for cell in combo) for combo in winning_combinations)

    def is_tie(self):
        return all(cell != " " for cell in self.cells[1:])

    def reset(self):
        self.cells = [" "] * 10

    def ai_move(self, player, difficulty):
        """AI chooses the next move based on difficulty level."""
        opponent = "X" if player == "O" else "O"

        if difficulty == "Easy":
            # Random move
            available_moves = [i for i in range(1, 10) if self.cells[i] == " "]
            if available_moves:
                self.update_cell(random.choice(available_moves), player)

        elif difficulty == "Medium":
            # Try to win or block opponent
            for i in range(1, 10):
                if self.cells[i] == " ":
                    self.cells[i] = player
                    if self.is_winner(player):
                        return
                    self.cells[i] = " "  # Undo move

            for i in range(1, 10):
                if self.cells[i] == " ":
                    self.cells[i] = opponent
                    if self.is_winner(opponent):
                        self.cells[i] = player
                        return
                    self.cells[i] = " "  # Undo move

            # Otherwise, play center if available
            if self.cells[5] == " ":
                self.update_cell(5, player)
                return

            # Otherwise, pick a random move
            available_moves = [i for i in range(1, 10) if self.cells[i] == " "]
            if available_moves:
                self.update_cell(random.choice(available_moves), player)

        elif difficulty == "Hard":
            # Use Minimax algorithm for best move
            best_score = -float("inf")
            best_move = None

            for i in range(1, 10):
                if self.cells[i] == " ":
                    self.cells[i] = player
                    score = self.minimax(False, player, opponent)
                    self.cells[i] = " "  # Undo move
                    if score > best_score:
                        best_score = score
                        best_move = i

            if best_move is not None:
                self.update_cell(best_move, player)

    def minimax(self, is_maximizing, player, opponent):
        """Minimax algorithm to find the best possible move."""
        if self.is_winner(player):
            return 1
        if self.is_winner(opponent):
            return -1
        if self.is_tie():
            return 0

        if is_maximizing:
            best_score = -float("inf")
            for i in range(1, 10):
                if self.cells[i] == " ":
                    self.cells[i] = player
                    score = self.minimax(False, player, opponent)
                    self.cells[i] = " "  # Undo move
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float("inf")
            for i in range(1, 10):
                if self.cells[i] == " ":
                    self.cells[i] = opponent
                    score = self.minimax(True, player, opponent)
                    self.cells[i] = " "  # Undo move
                    best_score = min(score, best_score)
            return best_score


board = Board()


def refresh_screen():
    # clear_screen()
    os.system("clear")
    board.display()


# Print header once

print("Welcome to Tic-Tac-Toe\n")
print("Select the mode to play for:")
print("1.Multiplayer   2.With PC")
mode = input("Enter the mode(1 or 2):")
if mode == "2":

    while True:
        # Ask for difficulty level before each game
        print("Select Difficulty Level:")
        print("1 - Easy  |  2 - Medium  |  3 - Hard")
        difficulty_choice = input("Enter your choice (1/2/3): ")

        if difficulty_choice == "1":
            difficulty = "Easy"
        elif difficulty_choice == "2":
            difficulty = "Medium"
        else:
            difficulty = "Hard"

        board.reset()  # Reset the board at the start of each round

        while True:
            refresh_screen()

            # Get X input
            while True:
                try:
                    x_choice = int(input("\nX) Choose 1 - 9: "))
                    if 1 <= x_choice <= 9 and board.cells[x_choice] == " ":
                        break
                    else:
                        print("Invalid move, try again.")
                except ValueError:
                    print("Please enter a valid number.")

            board.update_cell(x_choice, "X")

            if board.is_winner("X"):
                refresh_screen()
                print("\nX wins!\n")
                break

            if board.is_tie():
                refresh_screen()
                print("\nIt's a tie!\n")
                break

            # AI Move (O)
            board.ai_move("O", difficulty)

            if board.is_winner("O"):
                refresh_screen()
                print("\nO wins!\n")
                break

            if board.is_tie():
                refresh_screen()
                print("\nIt's a tie!\n")
                break

        # Ask if the user wants to play again
        if input("Play again? (Y/N): ").upper() != "Y":
            break
else:
    while True:
        refresh_screen()

        # Get X input
        while True:
            try:
                x_choice = int(input("\nX) Choose 1 - 9: "))
                if 1 <= x_choice <= 9 and board.cells[x_choice] == " ":
                    break
                else:
                    print("Invalid move, try again.")
            except ValueError:
                print("Please enter a valid number.")
        board.update_cell(x_choice, "X")

        if board.is_winner("X"):
            refresh_screen()
            print("\n X wins \n")
            play_again = input("Would you like to play again? (Y/N) > ").upper()
            if play_again == "Y":
                board.reset()
                continue
            else:
                break

        if board.is_tie():
            refresh_screen()
            print("\n Tie game \n")
            play_again = input("Would you like to play again? (Y/N) > ").upper()
            if play_again == "Y":
                board.reset()
                continue
            else:
                break

        refresh_screen()

        # Get O input
        while True:
            try:
                o_choice = int(input("\nO) Choose 1 - 9: "))
                if 1 <= o_choice <= 9 and board.cells[o_choice] == " ":
                    break
                else:
                    print("Invalid move, try again.")
            except ValueError:
                print("Please enter a valid number.")
        board.update_cell(o_choice, "O")
        if board.is_winner("O"):
            refresh_screen()
            print("\n O  wins \n")
            play_again = input("Would you like to play again? (Y/N) > ").upper()
            if play_again == "Y":
                board.reset()
                continue
            else:
                break

        if board.is_tie():
            refresh_screen()
            print("\n Tie game \n")
            play_again = input("Would you like to play again? (Y/N) > ").upper()
            if play_again == "Y":
                board.reset()
                continue
            else:
                break

