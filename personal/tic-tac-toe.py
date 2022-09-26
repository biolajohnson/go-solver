import math
import copy
import time



class Board():
  def __init__(self, player, board=None):
    if not board:
      self.board = [[".", ".", "."],
                    [".", ".", "."],
                    [".", ".", "."]] 
    else:
      self.board = board

    self.children = []
    self.player = player
    self.create_children()

  def create_children(self):
    if self.terminal():
      return
    for i in range(0, 3):
      for j in range(0, 3):
          if self.board[i][j] == ".":
            self.board[i][j] = self.player
            self.children.append(Board(-self.player, copy.deepcopy(self.board)))
            self.board[i][j] = "."

  def is_valid(self, x, y):
    if x > 2 or x < 0 or y < 0 or y > 2:
      return False
    if self.board[x][y] != ".":
      return False
    return True
  
  def terminal(self):
    result = self.evaluate()
    if result is not None:
      return True
    if self.is_full():
      return True
    return False
  

  def print_board(self):
      for i in range(0, 3):
        for j in range(0, 3):
          if self.board[i][j] == 1:
            piece = "X"
          elif self.board[i][j] == -1:
            piece = "O"
          else :
            piece = "."
          print("{}".format(piece), end="  |")
        print()

  def check_horizontal(self):
    for i in range(0, 3):
      if self.board[i] == [1, 1, 1]:
        return "X"
      if self.board[i] == [-1, -1, -1]:
        return "O"
  def check_vertical(self):
    for i in range(0, 3):
      if self.board[0][i] != "." and self.board[1][i] == self.board[0][i] and self.board[2][i] == self.board[1][i]:
        return self.board[0][i]

  def check_diagonals(self):
    for i in range(0, 3):
      if self.board[0][0] != "." and self.board[1][1] == self.board[0][0] and self.board[2][2] == self.board[1][1]:
        return self.board[0][0]
    for i in range(0, 3):
      if self.board[0][2] != "." and self.board[1][1] == self.board[0][2] and self.board[2][0] == self.board[1][1]:
        return self.board[2][0]

  def is_full(self):
    for i in range(0, 3):
      for j in range(0, 3):
        if self.board[i][j] == ".":
          return None

  def evaluate(self):
    vertical = self.check_vertical()
    horizontal = self.check_horizontal()
    diagonal = self.check_diagonals()
    if vertical is not None:
      return vertical
    elif horizontal is not None:
      return horizontal
    elif diagonal is not None:
      return diagonal
    else:
      return None


  def evaluation(self):
    result = self.evaluate()
    if result == 1:
      return 1
    elif result == -1:
      return -1
    else:
      return 0




class Game():
  def __init__(self):
    self.current_state = Board(1)
    
  def move(self, player, i, j):
    if self.is_valid(i, j):
      self.current_state.board[i][j] = player
      return Board(-player, self.current_state.board)
    else: 
      print("Invalid move")
  
  def is_valid(self, x, y):
    return self.current_state.is_valid(x, y)
  
  def game_over(self, current_state):
    if current_state.terminal():
      return True
    return False
      
# Minimax

def minimax_decison(state):
  return min_value(state)[0]

def max_value(state):
  if state.terminal():
    return state, state.evaluation()
  v = -math.inf
  return_state = None
  for child in state.children:
    child_state, value = min_value(child)
    if value > v:
      v = value
      return_state = child
  return return_state, v

def min_value(state):
  if state.terminal():
    return state, state.evaluation()
  v = math.inf
  return_state = None
  for child in state.children:
    child_state, value = max_value(child)
    if value < v:
      v = value
      return_state = child
  return return_state, v

# Alpha Beta

def alpha_beta_decision(state):
  return min_value_alpha_beta(state, -math.inf, math.inf)[0]

def max_value_alpha_beta(state, alpha, beta):
  if state.terminal():
    return state, state.evaluation()
  v = -math.inf
  return_state = None
  for child in state.children:
    child_state, value = min_value(child, alpha, beta)
    if value > v:
      v = value
      return_state = child
    if v >= beta:
      return return_state, v
    alpha = max(v, alpha)
  return return_state, v

def min_value_alpha_beta(state, alpha, beta):
  if state.terminal():
    return state, state.evaluation()
  v = math.inf
  return_state = None
  for child in state.children:
    child_state, value = max_value(child, alpha, beta)
    if value < v:
      v = value
      return_state = child
    if v <= alpha:
      return return_state, v
    beta = min(v, beta)
  return return_state, v


def main():
  print("Starting game...")
  game = Game()
 
  player = 1
  game.current_state.print_board()
  new_board = game.current_state
  while not game.game_over(new_board):
    player_input = input("Move?: ")
    moves = player_input.split(" ")
    i = int(moves[0])
    j = int(moves[1])
    new_board = game.move(player, i, j)
    new_board.print_board()
    print("----------------------")
    start = time.time()
    best_move = minimax_decison(new_board)
    end = time.time()
    game.current_state = best_move
    best_move.print_board()
    print("----------------------")
    print("it took {} seconds".format(round(end - start, 4)))
    
 
if __name__ == "__main__":
  main()