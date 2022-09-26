from Go import GO;

def play(player1, player2):
  go = GO(5)
  go.play(player1, player2)


def battle(board, player1, player2, iter, learn=False, show_result=True):
    p1_stats = [0, 0, 0] # draw, win, lose
    for i in range(0, iter):
        result = play(player1, player2, learn)
        p1_stats[result] += 1
      

    p1_stats = [round(x / iter * 100.0, 1) for x in p1_stats]
    if show_result:
        print('_' * 60)
        print('{:>15}(X) | Wins:{}% Draws:{}% Losses:{}%'.format(player1.__class__.__name__, p1_stats[1], p1_stats[0], p1_stats[2]).center(50))
        print('{:>15}(O) | Wins:{}% Draws:{}% Losses:{}%'.format(player2.__class__.__name__, p1_stats[2], p1_stats[0], p1_stats[1]).center(50))
        print('_' * 60)
        print()

    return p1_stats