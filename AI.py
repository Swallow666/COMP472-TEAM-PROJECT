#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-03-05 14-02-39
# @Author  : Minimax Team
# @Link    : https://github.com/Swallow666/COMP472-TEAM-PROJECT
# @Version : Py-3.72

import numpy as np
import math

class StateNode:

	def __init__(self, board_list, level):
		self.board_list = board_list
		self.children = []
		self.score = 0
		self.level = level

	def add_child(self, child_node):
		self.children.append(child_node)

	def heuristic(self):
		sum = 0
		brd = np.array(self.board_list)
		brd.resize(12,8)

		color_counter = 0
		dot_counter = 0
		for i in range(12):		# counter=n => n+1 same together, row
			for j in range(1,8):
				if ((brd[i][j][0] == brd[i][j-1][0]) and (brd[i][j] != '   ')):
					color_counter += 1
				else:
					sum += 10**color_counter
					color_counter = 0
				if ((brd[i][j][1] == brd[i][j-1][1]) and (brd[i][j] != '   ')):
					dot_counter += 1
				else:
					sum -= 10**dot_counter
					dot_counter = 0
			sum += 10**color_counter
			sum -= 10**dot_counter
			color_counter = 0
			dot_counter = 0

		for j in range(8):		# column
			for i in range(1,12):
				if ((brd[i][j][0] == brd[i-1][j][0]) and (brd[i][j] != '   ')):
					color_counter += 1
				else:
					sum += 10**color_counter
					color_counter = 0
				if ((brd[i][j][1] == brd[i-1][j][1]) and (brd[i][j] != '   ')):
					dot_counter += 1
				else:
					sum -= 10**dot_counter
					dot_counter = 0
			sum += 10**color_counter
			sum -= 10**dot_counter
			color_counter = 0
			dot_counter = 0

		for i in range(3,16):		#dignal/  3-15
			if i < 8:		# i=3-7
				for j in range(1,i+1):
					if ((brd[i-j][j][0] == brd[i-j+1][j-1][0]) and (brd[i-j][j] != '   ')):
						color_counter += 1
					else:
						sum += 10**color_counter
						color_counter = 0
					if ((brd[i-j][j][1] == brd[i-j+1][j-1][1]) and (brd[i-j][j] != '   ')):
						dot_counter += 1
					else:
						sum -= 10**dot_counter
						dot_counter = 0
				sum += 10**color_counter
				sum -= 10**dot_counter
				color_counter = 0
				dot_counter = 0
			elif i < 12:		# i=8-11
				for j in range(1,8):
					if ((brd[i-j][j][0] == brd[i-j+1][j-1][0]) and (brd[i-j][j] != '   ')):
						color_counter += 1
					else:
						sum += 10**color_counter
						color_counter = 0
					if ((brd[i-j][j][1] == brd[i-j+1][j-1][1]) and (brd[i-j][j] != '   ')):
						dot_counter += 1
					else:
						sum -= 10**dot_counter
						dot_counter = 0
				sum += 10**color_counter
				sum -= 10**dot_counter
				color_counter = 0
				dot_counter = 0
			else:		# i=12-15
				for j in range(i-10,8):
					if ((brd[i-j][j][0] == brd[i-j+1][j-1][0]) and (brd[i-j][j] != '   ')):
						color_counter += 1
					else:
						sum += 10**color_counter
						color_counter = 0
					if ((brd[i-j][j][1] == brd[i-j+1][j-1][1]) and (brd[i-j][j] != '   ')):
						dot_counter += 1
					else:
						sum -= 10**dot_counter
						dot_counter = 0
				sum += 10**color_counter
				sum -= 10**dot_counter
				color_counter = 0
				dot_counter = 0

		for i in range(3,16):		#dignal\  3-15 
			if i < 8:		# i=3-7
				for j in range(1,i+1):
					if ((brd[11-i+j][j][0] == brd[10-i+j][j-1][0]) and (brd[11-i+j][j] != '   ')):
						color_counter += 1
					else:
						sum += 10**color_counter
						color_counter = 0
					if ((brd[11-i+j][j][1] == brd[10-i+j][j-1][1]) and (brd[11-i+j][j] != '   ')):
						dot_counter += 1
					else:
						sum -= 10**dot_counter
						dot_counter = 0
				sum += 10**color_counter
				sum -= 10**dot_counter
				color_counter = 0
				dot_counter = 0
			elif i < 12:		# i=8-11
				for j in range(1,8):
					if ((brd[11-i+j][j][0] == brd[10-i+j][j-1][0]) and (brd[11-i+j][j] != '   ')):
						color_counter += 1
					else:
						sum += 10**color_counter
						color_counter = 0
					if ((brd[11-i+j][j][1] == brd[10-i+j][j-1][1]) and (brd[11-i+j][j] != '   ')):
						dot_counter += 1
					else:
						sum -= 10**dot_counter
						dot_counter = 0
				sum += 10**color_counter
				sum -= 10**dot_counter
				color_counter = 0
				dot_counter = 0
			else:		# i=12-15
				for j in range(i-10,8):
					if ((brd[11-i+j][j][0] == brd[10-i+j][j-1][0]) and (brd[11-i+j][j] != '   ')):
						color_counter += 1
					else:
						sum += 10**color_counter
						color_counter = 0
					if ((brd[11-i+j][j][1] == brd[10-i+j][j-1][1]) and (brd[11-i+j][j] != '   ')):
						dot_counter += 1
					else:
						sum -= 10**dot_counter
						dot_counter = 0
				sum += 10**color_counter
				sum -= 10**dot_counter
				color_counter = 0
				dot_counter = 0

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
