import sys
from pathlib import Path
sys.path.insert(1, str(Path.cwd()))
from test.random_player2 import RandomPlayer
from GoLearner import GoLearner
from Go import GO
import copy 
from State import State



PLAYER_X = 1
PLAYER_O = 2

def play(host, player1, player2, verbose=False):
		'''
		The game starts!

		:param player1: Player instance.
		:param player2: Player instance.
		:param verbose: whether print input hint and error information
		:return: piece type of winner of the game (0 if it's a tie).
		'''
		host.init_board(host.size)
		# Print input hints and error message if there is a manual player
		if player1.type == 'manual' or player2.type == 'manual':
			host.verbose = True
			print('----------Input "exit" to exit the program----------')
			print('X stands for black chess, O stands for white chess.')
			host.visualize_board()
		
		verbose = host.verbose
		# Game starts!
		while 1:
			piece_type = 1 if host.X_move else 2

			# Judge if the game should end
			if host.game_end(piece_type):       
				result = host.judge_winner()
				if verbose:
					print('Game ended.')
					if result == 0: 
						print('The game is a tie.')
					else: 
						print('The winner is {}'.format('X' if result == 1 else 'O'))
				return result

			if verbose:
				player = "X" if piece_type == 1 else "O"
				print(player + " makes move...")

			# Game continues
			if piece_type == 1: action = player1.get_input(host, piece_type)
			else: action = player2.get_input(host, piece_type)

			if verbose:
				player = "X" if piece_type == 1 else "O"
				print(action)

			if action != "PASS":
				# If invalid input, continue the loop. Else it places a chess on the board.
				if not host.place_chess(action[0], action[1], piece_type):
					if verbose:
						host.visualize_board() 
					continue

				host.died_pieces = host.remove_died_pieces(3 - piece_type) # Remove the dead pieces of opponent
			else:
				host.previous_board = copy.deepcopy(host.board)

			if verbose:
				host.visualize_board() # Visualize the board again
				print()

			host.n_move += 1
			host.X_move = not host.X_move # Players take turn




def battle(host, player1, player2, iter, learn=False, show_result=True):
		p1_stats = [0, 0, 0] # draw, win, lose
		for i in range(0, iter):
				result = play(host, player1, player2, learn)
				p1_stats[result] += 1
				host.reset()

		p1_stats = [round(x / iter * 100.0, 1) for x in p1_stats]
		if show_result:
				print('_' * 60)
				print('{:>15}(X) | Wins:{}% Draws:{}% Losses:{}%'.format(player1.__class__.__name__, p1_stats[1], p1_stats[0], p1_stats[2]).center(50))
				print('{:>15}(O) | Wins:{}% Draws:{}% Losses:{}%'.format(player2.__class__.__name__, p1_stats[2], p1_stats[0], p1_stats[1]).center(50))
				print('_' * 60)
				print()

		return p1_stats


if __name__ == "__main__":

		# Example Usage
		# battle(Board(show_board=True, show_result=True), RandomPlayer(), RandomPlayer(), 1, learn=False, show_result=True)
		# battle(Board(), RandomPlayer(), RandomPlayer(), 100, learn=False, show_result=True)
		# battle(Board(), RandomPlayer(), SmartPlayer(), 100, learn=False, show_result=True)
		# battle(Board(), RandomPlayer(), PerfectPlayer(), 100, learn=False, show_result=True)
		# battle(Board(), SmartPlayer(), PerfectPlayer(), 100, learn=False, show_result=True)

		Golearner = GoLearner()
		NUM = Golearner.GAME_NUM

		# train: play NUM games against players who only make random moves
		print('Training QLearner against RandomPlayer for {} times......'.format(NUM))
		host = GO(5)
		battle(host, RandomPlayer(), GoLearner(), NUM, learn=True, show_result=True)
		battle(host, GoLearner(), RandomPlayer(), NUM, learn=True, show_result=False)

		# test: play 1000 games against each opponent
		print('Playing GoLearner against RandomPlayer for 1000 times......')
		q_rand = battle(host, GoLearner(), RandomPlayer(), 500)
		rand_q = battle(host, RandomPlayer(), GoLearner(), 500)
		# print('Playing GoLearner against SmartPlayer for 1000 times......')
		# q_smart = battle(board, GoLearner, SmartPlayer(), 500)
		# smart_q = battle(board, SmartPlayer(), GoLearner, 500)
		# print('Playing GoLearner against PerfectPlayer for 1000 times......')
		# q_perfect = battle(board, GoLearner, PerfectPlayer(), 500)
		# perfect_q = battle(board, PerfectPlayer(), GoLearner, 500)

		# summarize game results
		winning_rate_w_random_player  = round(100 -  (q_rand[2] + rand_q[1]) / 2, 2)
		# winning_rate_w_smart_player   = round(100 - (q_smart[2] + smart_q[1]) / 2, 2)
		# winning_rate_w_perfect_player = round(100 - (q_perfect[2] + perfect_q[1]) / 2, 2)

		print("Summary:")
		print("_" * 60)
		print("GoLearner VS  RandomPlayer |  Win/Draw Rate = {}%".format(winning_rate_w_random_player))
		# print("GoLearner VS   SmartPlayer |  Win/Draw Rate = {}%".format(winning_rate_w_smart_player))
		# print("GoLearner VS PerfectPlayer |  Win/Draw Rate = {}%".format(winning_rate_w_perfect_player))
		print("_" * 60)

		grade = 0
		if winning_rate_w_random_player >= 85:
				grade += 25 if winning_rate_w_random_player >= 95 else winning_rate_w_random_player * 0.15
		# if winning_rate_w_smart_player >= 85:
		# 		grade += 25 if winning_rate_w_smart_player >= 95 else winning_rate_w_smart_player * 0.15
		# if winning_rate_w_perfect_player >= 85:
		# 		grade += 20 if winning_rate_w_perfect_player >= 95 else winning_rate_w_perfect_player * 0.10
		grade = round(grade, 1)

		print("\nTask 2 Grade: {} / 70 \n".format(grade))

#   output_file = sys.argv[1]
#    with open(output_file, 'w') as f:
#        f.write(str(grade) + '\n')

