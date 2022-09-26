from socket import timeout
import time
from test.eval import atari_check
import math


# Write output
# -----------------------------------------
def writeOutput(result, path="output.txt"):
   res = ""
   if result == "PASS":
        res = "PASS"
   else:
        res += str(result[0]) + ',' + str(result[1])
   with open(path, "w") as f:
      f.write(res)


def writePass(path="output.txt"):
   with open(path, 'w') as f:
      f.write("PASS")

def writeNextInput(piece_type, previous_board, board, path="input.txt"):
   res = ""
   res += str(piece_type) + "\n"
   for item in previous_board:
      res += "".join([str(x) for x in item])
      res += "\n"
        
   for item in board:
      res += "".join([str(x) for x in item])
      res += "\n"

   with open(path, 'w') as f:
      f.write(res[:-1])

# Read input 
# ---------------------------------------------
def readInput(n, path="input.txt"):

    with open(path, 'r') as f:
        lines = f.readlines()

        piece_type = int(lines[0])

        previous_board = [[int(x) for x in line.rstrip('\n')] for line in lines[1:n+1]]
        board = [[int(x) for x in line.rstrip('\n')] for line in lines[n+1: 2*n+1]]

        return piece_type, previous_board, board

def readOutput(path="output.txt"):
    with open(path, 'r') as f:
        position = f.readline().strip().split(',')

        if position[0] == "PASS":
            return "PASS", -1, -1

        x = int(position[0])
        y = int(position[1])

    return "MOVE", x, y

# Helper function to copy and create matrix
# ----------------------------------------
def copy(prev_state):
  moves = []
  res = []
  for i in range(0, 5):
    row = []
    for j in range(0, 5):
      col = prev_state[i][j]
      if col == 0:
        move = tuple([i, j])
        moves.append(move)
      row.append(col)
    res.append(row)
  return moves, res



# Board configuration
# ------------------------------------------
class State:
  def __init__(self, matrix, player, action):
    moves, new_state = copy(matrix)
    self.config = new_state
    self.moves = moves
    self.is_max_player = player
    self.children = []
    self.Value = 0
    self.action = action

  def move(self, action):
    copy_one_moves, copy_one_state  = copy(self.config)
    i, j = action
    copy_one_state[i][j] = 1
    new_state = State(copy_one_state, False, action)
    self.children.append(new_state)
    return new_state
    
  def terminal_state(self):
    # if no moves left on the board
    if len(self.moves) == 0:
      return True
    return False

  def utility(self):
    result = 0
    player = 1
    for i in range(5):
      for j in range(5):
        if self.config[i][j] == player:
          count = atari_check(i, j, self.config)
          result += count
    return result


# Alpha Beta algorithm
# ----------------------------------------------
class AlphaBetaPlayer():
  def __init__(self):
    self.timeout = False
    self.start = 0.0
    self.time_taken = 0.0
    self.time_limit = 10
    self.value = 0

  def alpha_beta_decision(self, state):
    self.start = time.time()
    init_depth = 3
    for d in range(0, 10):
      self.value = self.max_value_alpha_beta(init_depth +  d, state, -math.inf, math.inf)
      if self.timeout:
       return self.value

  def max_value_alpha_beta(self, depth, state, alpha, beta):
    if time.time() - self.start > self.time_limit:
      self.timeout = True
      return alpha
    if state.terminal_state():
      return state.utility()
    if depth == 0:
      return state.utility()
    v = -math.inf
    for action in state.moves:
      v = max(v, self.min_value_alpha_beta(depth - 1, state.move(action), alpha, beta))
    if v >= beta:
      state.value = v
      return v
    alpha = max(alpha, v)
    state.value = alpha
    return alpha

  def min_value_alpha_beta(self, depth, state, alpha, beta):
    if state.terminal_state():
      return state.utility()
    if depth == 0:
      return state.utility()
    v = math.inf
    for action in state.moves:
      v = min(v, self.max_value_alpha_beta(depth - 1, state.move(action), alpha, beta))
      if v <= beta:
        state.value = v
        return v
    beta = min(beta, v)
    state.value = beta
    return beta


# main (File Entry)
# -------------------------------------
def main():
  print("Starting program...\n")
  start = time.time()

  piece_type, previous_board, current_board = readInput(5)
  state = State(previous_board, True, action=None)
  
  start_alpha_beta = time.time()
  alpha_beta = AlphaBetaPlayer()
  best_move_alpha_beta = alpha_beta.alpha_beta_decision(state)
  print(best_move_alpha_beta)
  end_alpha_beta = time.time()
  print("Alpha-Beta: Time taken {:.3f} seconds \n".format(end_alpha_beta - start_alpha_beta))

  # writeOutput(best_move_alpha_beta)

  end = time.time()
  print("Execution took {:.3f} seconds \n".format(end - start))

if __name__ == "__main__":
  main()
