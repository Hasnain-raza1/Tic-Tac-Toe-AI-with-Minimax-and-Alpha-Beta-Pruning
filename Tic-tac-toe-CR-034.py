# tic_tac_toe_ai.py

import math
import time
from copy import deepcopy

# Constants
HUMAN = 'O'
AI = 'X'
EMPTY = ' '

class Game:
    def __init__(self):
        self.board = [EMPTY] * 9

    def display(self):
        for i in range(3):
            print(" | ".join(self.board[i*3:(i+1)*3]))
            if i < 2:
                print("--+---+--")

    def is_winner(self, player):
        wins = [
            [0,1,2], [3,4,5], [6,7,8],  # Rows
            [0,3,6], [1,4,7], [2,5,8],  # Cols
            [0,4,8], [2,4,6]            # Diags
        ]
        return any(all(self.board[i] == player for i in line) for line in wins)

    def is_draw(self):
        return EMPTY not in self.board and not self.is_winner(AI) and not self.is_winner(HUMAN)

    def get_moves(self):
        return [i for i, cell in enumerate(self.board) if cell == EMPTY]

    def make_move(self, pos, player):
        if self.board[pos] == EMPTY:
            self.board[pos] = player
            return True
        return False

    def undo_move(self, pos):
        self.board[pos] = EMPTY

    def game_over(self):
        return self.is_winner(AI) or self.is_winner(HUMAN) or self.is_draw()

# --- Minimax without Alpha-Beta ---
def minimax(game, depth, is_max):
    if game.is_winner(AI):
        return 10 - depth
    elif game.is_winner(HUMAN):
        return depth - 10
    elif game.is_draw():
        return 0

    if is_max:
        max_score = -math.inf
        for move in game.get_moves():
            game.make_move(move, AI)
            score = minimax(game, depth + 1, False)
            game.undo_move(move)
            max_score = max(score, max_score)
        return max_score
    else:
        min_score = math.inf
        for move in game.get_moves():
            game.make_move(move, HUMAN)
            score = minimax(game, depth + 1, True)
            game.undo_move(move)
            min_score = min(score, min_score)
        return min_score

# --- Minimax with Alpha-Beta ---
def alphabeta(game, depth, alpha, beta, is_max):
    if game.is_winner(AI):
        return 10 - depth
    elif game.is_winner(HUMAN):
        return depth - 10
    elif game.is_draw():
        return 0

    if is_max:
        max_eval = -math.inf
        for move in game.get_moves():
            game.make_move(move, AI)
            eval = alphabeta(game, depth + 1, alpha, beta, False)
            game.undo_move(move)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = math.inf
        for move in game.get_moves():
            game.make_move(move, HUMAN)
            eval = alphabeta(game, depth + 1, alpha, beta, True)
            game.undo_move(move)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

# --- Get Best Move for AI ---
def get_best_move(game, use_alpha_beta=False):
    best_val = -math.inf
    best_move = None

    for move in game.get_moves():
        game.make_move(move, AI)
        if use_alpha_beta:
            move_val = alphabeta(game, 0, -math.inf, math.inf, False)
        else:
            move_val = minimax(game, 0, False)
        game.undo_move(move)

        if move_val > best_val:
            best_val = move_val
            best_move = move

    return best_move

# --- Compare Performance ---
def compare():
    trials = 5
    total_minimax = 0
    total_ab = 0

    for _ in range(trials):
        g1 = Game()
        g2 = Game()

        t1 = time.time()
        get_best_move(g1, use_alpha_beta=False)
        total_minimax += time.time() - t1

        t2 = time.time()
        get_best_move(g2, use_alpha_beta=True)
        total_ab += time.time() - t2

    print(f"\nPerformance over {trials} trials:")
    print(f"Minimax:     {total_minimax / trials:.6f} sec")
    print(f"Alpha-Beta:  {total_ab / trials:.6f} sec")

# --- Main Execution ---
if __name__ == "__main__":
    game = Game()
    print("Tic-Tac-Toe AI Comparison")
    game.display()

    print("\nBest move by Minimax:", get_best_move(deepcopy(game), use_alpha_beta=False))
    print("Best move by Alpha-Beta:", get_best_move(deepcopy(game), use_alpha_beta=True))

    compare()
