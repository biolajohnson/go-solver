from copy import deepcopy
import queue
from random import random
from read import readInput
from write import writeOutput
from host import GO
from time import time
from math import inf, sqrt
import random
from eval import calc_liberties
from queue import PriorityQueue






# EULER METHOD

def find_euler(board, piece_type):
	external = 0
	internal = 0
	diagonal = 0

	for i in range(0, 6):
		for j in range(0, 6):
			block = [[board[i][j], board[i][j + 1]],
							 [board[i + 1][j], board[i + 1][j + 1]]]
			if external_match(block, piece_type):
				external += 1
			if internal_match(block, piece_type):
				internal += 1
			if diagonal_match(block, piece_type):
				diagonal += 1


	e = (external - internal + (2*diagonal)) / 4
	return e

def external_match(block, piece_type):
	one = block[0][0]
	two = block[0][1]
	three = block[1][0]
	four = block[1][1]

	if one == piece_type and two == 0 and three == 0 and four == 0:
		return True
	elif one == 0 and two == piece_type and three == 0 and four == 0:
		return True 
	elif one == 0 and two == 0 and three == piece_type and four == 0:
		return True
	elif one == 0 and two == 0 and three == 0 and four == piece_type:
		return True
	return False
	

def internal_match(block, piece_type):
	one = block[0][0]
	two = block[0][1]
	three = block[1][0]
	four = block[1][1]

	if one == piece_type and two == piece_type and three == piece_type and four == 0:
		return True
	elif one == piece_type and two == piece_type and three == 0 and four == piece_type:
		return True 
	elif one == piece_type and two == 0 and three == piece_type and four == piece_type:
		return True
	elif one == 0 and two == piece_type and three == piece_type and four == piece_type:
		return True

	return False

def diagonal_match(block, piece_type):
	one = block[0][0]
	two = block[0][1]
	three = block[1][0]
	four = block[1][1]



	if one == piece_type and two == 0 and three == piece_type and four == 0:
		return True
	elif one == 0 and two == piece_type and three == 0 and four == piece_type:
		return True 
	return False



# ALPHA - BETA PLAYER

class AlphaBetaPlayer():
	def __init__(self):
				self.type = 'alpha beta'

	def get_input(self, go, piece_type, board, prev_board):
		go_copy = deepcopy(go) 
		board_state = Board(board, piece_type, None) 
		start = time()
		best_move = alpha_beta_decision(board_state, piece_type, start)
		if best_move != "PASS" and not go_copy.valid_place_check(best_move[0], best_move[1], piece_type, test_check=True):
			return "PASS"
		end = time()
		print("move: {} it took {:.2f} secs".format(best_move, end - start))
		return best_move
	
	def is_empty(self, board):
		for i in range(5):
			for j in range(5):
				if board[i][j] != 0:
					return False
		return True




# BOARD DATA STRUCTURE

class Board():
	def __init__(self, board, player, prev):
		self.board = board
		self.prev = prev
		if player == 1:
			self.player = 1
			self.opp = 2
		else:
			self.player = 2
			self.opp = 1
		self.actions = self.get_actions()
	
		self.komi = 2.5


	def move(self, action, piece_type):
		board = self.board
		if action == "PASS":
			return Board(board, self.opp, action)
		board[action[0]][action[1]] = piece_type
		self.remove_died_pieces(self.opp)
		return Board(board, self.opp, action)

	def get_actions(self):
		actions = []
		queue = PriorityQueue()
		for i in range(0, 5):
			for j in range(0, 5):
				if self.board[i][j] == 0:
					position = euclid_distance(i, j)
					queue.put((position, (i, j)))

		while not queue.empty():
			tups = queue.get()
			actions.append(tups[1])
		return actions

	def detect_neighbor(self, i, j):
		board = self.board
		neighbors = []
		if i > 0:
			neighbors.append((i-1, j))
		if i < len(board) - 1: 
			neighbors.append((i+1, j))
		if j > 0:
			neighbors.append((i, j-1))
		if j < len(board) - 1: 
			neighbors.append((i, j+1))
		return neighbors

	def detect_neighbor_ally(self, i, j):
		board = self.board
		neighbors = self.detect_neighbor(i, j)
		group_allies = []
		for piece in neighbors:
			if board[piece[0]][piece[1]] == board[i][j]:
				group_allies.append(piece)
		return group_allies

	def ally_dfs(self, i, j):
		stack = [(i, j)]
		ally_members = []
		while stack:
			piece = stack.pop()
			ally_members.append(piece)
			neighbor_allies = self.detect_neighbor_ally(piece[0], piece[1])
			for ally in neighbor_allies:
				if ally not in stack and ally not in ally_members:
					stack.append(ally)
		return ally_members

	def find_liberty(self, i, j):
		board = self.board
		ally_members = self.ally_dfs(i, j)
		for member in ally_members:
			neighbors = self.detect_neighbor(member[0], member[1])
			for piece in neighbors:
				if board[piece[0]][piece[1]] == 0:
					return True
		return False

	def find_died_pieces(self, piece_type):
		board = self.board
		died_pieces = []
		for i in range(len(board)):
			for j in range(len(board)):
				if board[i][j] == piece_type:
					if not self.find_liberty(i, j):
						died_pieces.append((i,j))
		return died_pieces

	def remove_died_pieces(self, piece_type):
		died_pieces = self.find_died_pieces(piece_type)
		if not died_pieces: 
			return []
		self.remove_certain_pieces(died_pieces)
		return died_pieces

	def remove_certain_pieces(self, positions):
		board = self.board
		for piece in positions:
			board[piece[0]][piece[1]] = 0
			self.update_board(board)

	def update_board(self, new_board):
		self.board = new_board
		

	def terminal(self):
		if not self.actions:
			return True
		return False


	def score(self, piece_type):
		board = self.board
		cnt = 0
		for i in range(0, 5):
			for j in range(0, 5):
				if board[i][j] == piece_type:
					cnt += 1
		return cnt  


	def utility(self):
		player_score = self.score(self.player)
		opp_score = self.score(self.opp)
		if self.player == 1:
			if player_score > opp_score + self.komi:
				return 1000
			elif player_score < opp_score + self.komi:
				return -1000
			else:
				return 0
		else:
			if player_score + self.komi > opp_score:
				return 1000
			elif player_score + self.komi < opp_score:
				return -1000
			else:
				return 0

	def scan(self, player):
		player_count = 0
		opp_count = 0
		edge_piece = 0
		opp_edge_piece = 0
		player_edge_piece = 0
		for i in range(0, 5):
			for j in range(0, 5):
				if self.board[i][j] != 0:
					if(i == 0 or j == 0):
						if self.board[i][j] == 3 - player:
							opp_edge_piece += 1
						else:
							player_edge_piece += 1
					if self.board[i][j] == player:
						player_count += 1
					else:
						opp_count += 1
		edge_piece = opp_edge_piece - player_edge_piece					
		count = player_count - opp_count
		return count, edge_piece, 


	def pre_evaluation(self, player):
		if player == self.player:
			players_liberties = calc_liberties(self.board, self.player)
			opp_liberties = calc_liberties(self.board, self.opp)
		else:
			players_liberties = calc_liberties(self.board, self.opp)
			opp_liberties = calc_liberties(self.board, self.player)
		lib = players_liberties - opp_liberties
		count, edge_pieces = self.scan(player)
		return count, edge_pieces, lib


	def threshold(self, piece_type):
		board = deepcopy(self.board)
		new_board = [[0, 0, 0, 0, 0, 0, 0]]
		for i in range(5):
			for j in range(5):
				if board[i][j] != piece_type:
					board[i][j] = 0

		for i in range(5):
			row = []
			for j in range(7):
				if j == 0 or j == 6:
					row.append(0)
				else:
					row.append(board[i][j - 1])
			new_board.append(row)
		new_board.append([0, 0, 0, 0, 0, 0, 0])
		return new_board

	def evaluation(self, player):
		a = 4
		e = -4
		n = 5
		edge = 2
		num_pieces, edge_pieces, liberties = self.pre_evaluation(player)
		num_of_pieces = num_pieces
		euler_board_player = self.threshold(player)
		euler_board_opp = self.threshold(3 - player)
		player_euler = find_euler(euler_board_player, player)
		opp_euler = find_euler(euler_board_opp, 3 - player)
		euler = player_euler - opp_euler
		score = min(max(liberties,-a), a) + (e * euler) + (n * num_of_pieces) + (edge * edge_pieces)
		return score



# ALPHA-BETA ALGORITHM

def alpha_beta_decision(state, piece_type, start):
	player = piece_type
	alpha = -inf
	beta = inf
	depth = 0
	new_state = deepcopy(state)
	result = max_value(player, piece_type, new_state, alpha, beta, depth, start)
	print("Current evaluation: {}".format(result[1]))
	return result[0]


def max_value(player, piece_type, state, alpha, beta, depth, start):
	if cutoff(state, depth, start):
		return state.prev, evaluation(state, player)
	v = -inf
	best_move = None
	for action in state.actions:
		new_state = deepcopy(state)
		child = new_state.move(action, piece_type)
		value = min_value(player, 3 - piece_type, child, alpha, beta, depth + 1, start)
		if value[1] > v:
			v = value[1]
			best_move = action
		if v >= beta:
			return best_move, v
		alpha = max(v, alpha)
	return best_move, v


def min_value(player, piece_type, state, alpha, beta, depth, start):
	if cutoff(state, depth, start):
		return state.prev, evaluation(state, player)
	v = inf
	best_move = None
	for action in state.actions:
		new_state = deepcopy(state)
		child = new_state.move(action, piece_type)
		value = max_value(player, 3 - piece_type, child, alpha, beta, depth + 1, start)
		if value[1] < v:
			v = value[1]
			best_move = action
		if v <= alpha:
			return best_move, v
		beta = min(v, beta)
	return best_move, v



# HELPER FUNCTIONS

def cutoff(state, depth, start):
	current_time  = time()
	cutoff_time = current_time - start
	if cutoff_time > 8 or depth > 3 or state.terminal():
		return True
	return False

def evaluation(state, player):
	if state.terminal():
		return  state.utility()
	return state.evaluation(player)

		
def euclid_distance(i, j):
	result = int(sqrt(pow(abs(i - 2), 2) + pow(abs(j - 2), 2)))
	return result

def is_equal(prev_board, curr_board):
	for i in range(0, 5):
		for j in range(0, 5):
			if (prev_board[i][j] != curr_board[i][j]):
				return False
	return True

def is_first_move(curr_board):
	for i in range(0, 5):
		for j in range(0, 5):
			if (curr_board[i][j] != 0):
				return False
	return True


def start_game():
	N = 5
	piece_type, previous_board, board = readInput(N)

	go = GO(N)
	go.set_board(piece_type, previous_board, board)
	player = AlphaBetaPlayer()
	action = player.get_input(go, piece_type, board, previous_board)
	writeOutput(action)






def main():
	start_game()


	

if __name__ == "__main__":
	main()