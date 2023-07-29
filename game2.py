import math
import time
import tkinter as tk
from tkinter import messagebox 
from player import HumanPlayer, RandomComputerPlayer, SmartComputerPlayer


class TicTacToe:
    def __init__(self):
        self.board = self.make_board()
        self.current_winner = None

    @staticmethod
    def make_board():
        return [' ' for _ in range(9)]

    def print_board(self):
        for row in [self.board[i * 3:(i + 1) * 3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')

    @staticmethod
    def print_board_nums():
        # 0 | 1 | 2
        number_board = [[str(i) for i in range(j * 3, (j + 1) * 3)] for j in range(3)]
        for row in number_board:
            print('| ' + ' | '.join(row) + ' |')

    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        # check the row
        row_ind = math.floor(square / 3)
        row = self.board[row_ind * 3:(row_ind + 1) * 3]
        if all([s == letter for s in row]):
            return True
        col_ind = square % 3
        column = [self.board[col_ind + i * 3] for i in range(3)]
        if all([s == letter for s in column]):
            return True
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            if all([s == letter for s in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([s == letter for s in diagonal2]):
                return True
        return False

    def empty_squares(self):
        return ' ' in self.board

    def num_empty_squares(self):
        return self.board.count(' ')

    def available_moves(self):
        return [i for i, x in enumerate(self.board) if x == " "]


class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")

        self.board_buttons = []
        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack()

        self.game = TicTacToe()
        self.x_player = SmartComputerPlayer('X')
        self.o_player = HumanPlayer('O')

        self.create_board()

    def create_board(self):
        for i in range(3):
            row = []
            for j in range(3):
                button = tk.Button(self.board_frame, text=" ", width=10, height=4,
                                   command=lambda row=i, col=j: self.make_move(row, col))
                button.grid(row=i, column=j)
                row.append(button)
            self.board_buttons.append(row)

    def make_move(self, row, col):
        if self.game.make_move(row * 3 + col, self.o_player.letter):
            self.update_board()
            if not self.game.current_winner and self.game.empty_squares():
                self.root.after(800, self.make_computer_move)

    def make_computer_move(self):
        square = self.x_player.get_move(self.game)
        self.game.make_move(square, self.x_player.letter)
        self.update_board()

    def update_board(self):
        for i in range(3):
            for j in range(3):
                self.board_buttons[i][j]["text"] = self.game.board[i * 3 + j]
                self.board_buttons[i][j]["state"] = tk.DISABLED if self.game.board[i * 3 + j] != " " else tk.NORMAL

        if self.game.current_winner:
            winner = self.game.current_winner
            self.root.after(800, lambda: self.display_winner(winner))
        elif not self.game.empty_squares():
            self.root.after(800, self.display_tie)

    def display_winner(self, winner):
        tk.messagebox.showinfo("Game Over", f"{winner} wins!")
        self.reset_game()

    def display_tie(self):
        tk.messagebox.showinfo("Game Over", "It's a tie!")
        self.reset_game()

    def reset_game(self):
        self.game = TicTacToe()
        for i in range(3):
            for j in range(3):
                self.board_buttons[i][j]["text"] = " "
                self.board_buttons[i][j]["state"] = tk.NORMAL


if __name__ == '__main__':
    root = tk.Tk()
    game_gui = TicTacToeGUI(root)
    root.mainloop()
