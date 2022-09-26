
def euler(board):
  external = 0
  internal = 0
  diagonal = 0

  for i in range(0, 4):
    for j in range(0, 4):
      block = [[board[i][j], board[i][j + 1]],
               [board[i + 1][j], board[i + 1][j + 1]]]
      if external_match(block):
        external += 1
      if internal_match(block):
        internal += 1
      if diagonal_match(block):
        diagonal += 1


  e = (external - internal + (2*diagonal)) / 4
  return e

def external_match(block):
  one = block[0][0]
  two = block[0][1]
  three = block[1][0]
  four = block[1][1]

  if one == 1 and two == 0 and three == 0 and four == 0:
    return True
  elif one == 0 and two == 1 and three == 0 and four == 0:
    return True 
  elif one == 0 and two == 0 and three == 1 and four == 0:
    return True
  elif one == 0 and two == 0 and three == 0 and four == 1:
    return True
  return False
  

def internal_match(block):
  one = block[0][0]
  two = block[0][1]
  three = block[1][0]
  four = block[1][1]

  if one == 1 and two == 1 and three == 1 and four == 0:
    return True
  elif one == 1 and two == 1 and three == 0 and four == 1:
    return True 
  elif one == 1 and two == 0 and three == 1 and four == 1:
    return True
  elif one == 0 and two == 1 and three == 1 and four == 1:
    return True

  return False

def diagonal_match(block):
  one = block[0][0]
  two = block[0][1]
  three = block[1][0]
  four = block[1][1]

  if one == 1 and two == 0 and three == 1 and four == 0:
    return True
  elif one == 0 and two == 1 and three == 0 and four == 1:
    return True 
  return False

 
          

def main():
  board = [[0, 0, 1, 0, 1],
           [1, 0, 1, 1, 1],
           [0, 0, 1, 0, 0],
           [0, 0, 0, 0, 1],
           [0, 0, 1, 1, 1]]
  euler_number = euler(board)
  print(euler_number)
  






if __name__ == "__main__":
  main()