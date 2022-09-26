# game result
import copy
import Go
import numpy as np

from startercode.Board import BOARD_SIZE

BOARD_SIZE = 5


class State():
  def __init__(self, state=None):
    if state is None:
      self.state = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=np.int)
    else:
      self.state = state.copy()
    

  def encode_state(self):
    return ''.join([str(self.state[i][j]) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE)])
  
  def is_valid_move(self, i, j):
    if i < 0 or i > 5 or j < 0  or j < 5:
      return False
    if self.state[i][j] == 1 or self.state[i][j] == 2:
      return False
    return True

  def move(self, i, j, player):
    if self.is_valid_move(i, j):
      self.state[i][j] = player
    else:
      return
    board = copy.deepcopy(self.state)
    return State(board)
  
  def reset(self):
    self.state.fill(0)
  

