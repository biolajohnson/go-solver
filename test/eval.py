from copy import deepcopy

game = [
        [0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 0, 0],
        [0, 1, 1, 2, 2, 0],
        [0, 2, 2, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],     
        [0, 0, 0, 0, 0, 0]     
        ]

def calc_liberties(game, piece_type):
  copy_game = deepcopy(game)
  result = 0
  for i in range(5):
    for j in range(5):
      if game[i][j] == piece_type:
        count = atari_check(i, j, copy_game)
        result += count
  return result
    

def check_corners(i, j, state):
  count = 0
  if i == 0 and j == 0:
    if state[i + 1][j] == 0:
      count += 1
      state[i + 1][j] = "X"
    if state[i][j + 1] == 0:
      count += 1
      state[i][j + 1] = "X"
  elif i == len(state) - 1 and j == 0:
    if state[i - 1][j] == 0:
      count += 1
      state[i - 1][j] = "X"
    if state[i][j + 1] == 0:
      count += 1
      state[i][j + 1] = "X"
  elif i == 0 and j == len(state) - 1:
    if state[i][j - 1] == 0:
      count += 1
      state[i][j - 1] = "X"
    if state[i + 1][j] == 0:
      count += 1
      state[i + 1][j] = "X"
  elif i == len(state) - 1 and j == len(state) - 1:
    if state[i - 1][j] == 0:
      count += 1
      state[i - 1][j] = "X"
    if state[i][j - 1] == 0:
      count += 1
      state[i][j - 1] = "X"
  return count


def check_sides(i, j, state):
  count = 0
  if i == 0 and j > 0:
    if state[i + 1][j] == 0:
      count += 1
      state[i + 1][j] = "X"
    if state[i][j - 1] == 0:
      count += 1
      state[i][j - 1] = "X"
    if state[i][j + 1] == 0:
      count += 1
      state[i][j + 1] = "X"
  elif i == len(state) - 1 and j > 0:
    if state[i - 1][j] == 0:
      count += 1
      state[i - 1][j] = "X"
    if state[i][j + 1] == 0:
      count += 1
      state[i][j + 1] = "X"
    if state[i][j - 1] == 0:
      count += 1
      state[i][j - 1] = "X"
  elif i > 0  and j == 0:
    if state[i][j + 1] == 0:
      count += 1
      state[i][j + 1] = "X"
    if state[i + 1][j] == 0:
      count += 1
      state[i + 1][j] = "X"
    if state[i - 1][j] == 0:
      count += 1
      state[i - 1][j] = "X"
  elif i > 0 and j == len(state) - 1:
    if state[i][j - 1] == 0:
      count += 1
      state[i][j - 1] = "X"
    if state[i + 1][j] == 0:
      count += 1
      state[i + 1][j] = "X"
    if state[i - 1][j] == 0:
      count += 1
      state[i - 1][j] = "X"
  return count



def check_middle(i, j, state):
  count = 0
  if state[i - 1][j] == 0:
    count += 1
    state[i - 1][j] = "X"
  if state[i][j + 1] == 0:
    count += 1
    state[i][j + 1] = "X"
  if state[i][j - 1] == 0:
    count += 1
    state[i][j - 1] = "X"
  if state[i + 1][j] == 0:
    count += 1
    state[i + 1][j] = "X"
  return count
  
def atari_check(i, j, state):
  count = 0 
  if (i == 0 and j == 0) or (i == len(state) - 1 and j == 0) or (i == 0 and j == len(state) - 1) or (i == len(state) - 1 and j == len(state) - 1):
    count += check_corners(i, j, state)
  elif (i == 0 and j > 0) or (i == len(state) - 1 and j > 0) or (i > 0  and j == 0) or (i > 0 and j == len(state) - 1):
    count += check_sides(i, j, state)
  else:
    count += check_middle(i, j, state)
  return count


def main():
  result = calc_liberties(game, 1)
  print(result)

if __name__ == "__main__":
  main()