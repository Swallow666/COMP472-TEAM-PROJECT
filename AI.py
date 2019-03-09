#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-03-05 14-02-39
# @Author  : Minimax Team
# @Link    : https://github.com/Swallow666/COMP472-TEAM-PROJECT
# @Version : Py-3.72

import numpy
import math

class StateNode:

	def __init__(self, board, level):
		self.board = board
		self.children = []
		self.score = 0
		self.level = level

	def add_child(self, child_node):
		self.children.append(child_node)

	def heuristic(self):
		sum = 0
		for i in range(12):
			for j in range(8):
				if (self.board[i][j] == 'W\u26AA'):
					sum += (1 * ((11 - i) * 10 + j + 1))
				if (self.board[i][j] == 'W\u26AB'):
					sum += (3 * ((11 - i) * 10 + j + 1))
				if (self.board[i][j] == 'R\u26AA'):
					sum += (-1.5 * ((11 - i) * 10 + j + 1))
				if (self.board[i][j] == 'R\u26AB'):
					sum += (-2 * ((11 - i) * 10 + j + 1))
		self.score = sum

	def minimax(self, min_max, level):
		self.set_max_min(-min_max)
		self.level = level - 1
		if self.level > 1:
			for cc in self.children:
				cc.minimax(self.max_min, self.level)
				if self.max_min == 1:
					if cc.score > self.score:
						self.score = cc.score
				if self.max_min == -1:
					if cc.score < self.score:
						self.score = cc.score
		else:
			self.heuristic()
			
	def ai_algorithm(self): 
		for child in self.children:
			child.minimax(self.max_min, self.level)
			if self.max_min == 1:
				if child.score > self.score:
					self.score = child.score
					self.add_move(child.move_from_parent)
			if self.max_min == -1:
				if child.score < self.score:
					self.score = child.score
					self.add_move(child.move_from_parent)

	def set_max_min(self, max_min):	
		# max -> 1 ; min -> -1
		self.max_min = max_min
		if max_min == 1:
			self.score = -math.inf
		else:
			self.score = math.inf

	def trace(self):
		level_three_num = 0
		for child in self.children:
			level_three_num += len(child.children)
		file_handler = open('tracemm.txt', 'a')
		file_handler.write(str(level_three_num))
		file_handler.write('\n')
		file_handler.write("{:.1f}".format(self.score))
		file_handler.write('\n\n')
		for child in self.children:
			file_handler.write("{:.1f}".format(child.score))
			file_handler.write('\n')
		file_handler.write('\n')
		file_handler.close()

	def add_move(self, move):
		self.move_from_parent = move

	def get_next_move(self):
		return self.move_from_parent
