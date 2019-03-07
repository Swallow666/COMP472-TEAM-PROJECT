#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-03-05 14-02-39
# @Author  : Minimax Team
# @Link    : https://github.com/Swallow666/COMP472-TEAM-PROJECT
# @Version : Py-3.72

import numpy as np

class StateNode:

	def __init__(self, board):
		self.board = board
		self.children = []
		self.score = 0

	def add_child(self, child_node):
		self.children.append(child_node)

	def get_children_num(self):
		return len(self.children)

	def heuristic(self):

	def minimax(self):

	def trace(self):
		level_three_num = 0
		for child in self.children:
			
	def get_next_move(self):