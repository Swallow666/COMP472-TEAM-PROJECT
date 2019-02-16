#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-02-03 17-03-32
# @Author  : Minimax Team
# @Link    : https://github.com/Swallow666/COMP472-TEAM-PROJECT
# @Version : Py-3.72

import numpy as np
# import re

moving_times = 0

win = False

last_added_card = []	# stance 1-8, A-H, 1-12

game_dict = {}  # key = player 1 & player 2 , value = dot & color

card_dict = {}  # key = (A-H, 1-12), value = stances 1-8

board_values = [] 
for i in range(0,96):
	board_values.append('   ')

board = np.array(board_values)
board.resize(12,8)

def print_board():		# print board as name said
	sepa = ' | '
	for i in range(0,12):
		print('|| ' + sepa.join(board[i]) + ' ||')  # [0-11] => 12-1   [][0-7] => A-H

def regular_move_judge(player_move):		# check all illegal input and illegal regular moves

	move_info = player_move.split(' ')

	if (len(move_info) != 4):	#check length
		return False

	if (len(move_info[0]) != 1): # check first char
		return False
	if (ord(move_info[0]) != 48):
		return False

	if (len(move_info[1]) != 1):	#check second char
		return False
	if ((ord(move_info[1]) < 49) or (ord(move_info[1]) > 56)):	
		return False

	if (len(move_info[2]) != 1):	#check third char
		return False
	if ((ord(move_info[2]) < 65) or (ord(move_info[2]) > 72)):	
		return False

	if (len(move_info[3]) != 1) and (len(move_info[3]) != 2):	#check fourth
		return False
	if (len(move_info[3]) == 1):
		if ((ord(move_info[3]) < 49) or (ord(move_info[3]) > 57)):
			return False
	if (len(move_info[3]) == 2):
		if (ord(move_info[3][0]) != 49):
			return False
		if (not(48 <= ord(move_info[3][1]) <= 50)):
			return False

	# check if there is card in the two positions
	if board[12 - int(move_info[3])][ord(move_info[2]) - 65] != '   ':
		return False

	if (move_info[1] in ('1','3','5','7')):
		#check if there is illegal space below cases 1357

		if (move_info[2] == 'H'):	#check out of limit
			return False

		if (int(move_info[3]) != 1):	# pass if it is 1, no space below, else check if below exists space
			if ((board[13 - int(move_info[3])][ord(move_info[2]) - 65] == '   ') or (board[13 - int(move_info[3])][ord(move_info[2]) - 64] == '   ')):
				return False

		if board[12 - int(move_info[3])][ord(move_info[2]) - 64] != '   ':	# check if there is card exists 
			return False

	if (move_info[1] in ('2','4','6','8')):
		#check if there is illegal space below cases 2468

		if (int(move_info[3]) == 12):	#check out of limit
			return False

		if (int(move_info[3]) != 1):
			if (board[13 - int(move_info[3])][ord(move_info[2]) - 65] == '   '):
				return False

		if board[11 - int(move_info[3])][ord(move_info[2]) - 64] != '   ':	# check if there is card exists 
			return False


	return True

	# these code is using if we are not allowed to have space between characters of a command
	# so we have a backup just in case, better keep it
	'''
	if ((len(player_move) < 4) or (len(player_move) > 5)):	#check length
		return False
	elif (int(player_move[0]) != 0):	#check first char
		return False
	elif ((ord(player_move[1]) < 49) or (ord(player_move[1]) > 56)):	#check second char
		return False
	elif ((ord(player_move[2]) < 65) or (ord(player_move[2]) > 72)):	#check third char
		return False
	elif (len(player_move) == 4):	#check remaining chars in two length cases
		if ((ord(player_move[3]) < 49) or (ord(player_move[3]) > 57)):
			return False
	elif (len(player_move) == 5):
		if (not((ord(player_move[3]) == 49) and (48 <= ord(player_move[4]) <= 50))):
			return False
	elif ((player_move[1] == '1') or (player_move[1] == '3') or (player_move[1] == '5') or (player_move[1] == '7')):
		#check if there is illegal space below cases 1357
		char_chars = re.findall(r'[A-H]', player_move)
		int_chars = re.split('[A-H]', player_move)
		if (player_move[2] == 'H'):	#check out of limit
			return False
		if (int_chars[1] != '1'):	# 13 = 12 + 1, 64 = 65 - 1
			if ((board[13 - int(int_chars[1])][ord(char_chars[0]) - 65] == '  ') or (board[13 - int(int_chars[1])][ord(char_chars[0]) - 64] == '  ')):
				return False
	elif ((player_move[1] == '2') or (player_move[1] == '4') or (player_move[1] == '6') or (player_move[1] == '8')):
		#check if there is illegal space below cases 2468
		char_chars = re.findall(r'[A-H]', player_move)
		int_chars = re.split('[A-H]', player_move)
		if (int(int_chars[1]) == 12):	#check out of limit
			return False
		if (int_chars[1] != '1'):	# 13 = 12 + 1, 64 = 65 - 1
			if (board[13 - int(int_chars[1])][ord(char_chars[0]) - 65] == '  '):
				return False
	else:
		return True
	'''

def regular_move(player_move):	# do regular moving

	global board

	move_info = player_move.split(' ')

	stance_str_list = stances(int(move_info[1]))

	board[12 - int(move_info[3])][ord(move_info[2]) - 65] = stance_str_list[0]

	if (move_info[1] in ('1','3','5','7')):
		board[12 - int(move_info[3])][ord(move_info[2]) - 64] = stance_str_list[1]

	if (move_info[1] in ('2','4','6','8')):
		board[11 - int(move_info[3])][ord(move_info[2]) - 65] = stance_str_list[1]

	card_added = []
	card_added.append(move_info[1])
	card_added.append(move_info[2])
	card_added.append(move_info[3])

	global last_added_card
	last_added_card = card_added

	global moving_times
	moving_times += 1

	global card_dict
	card_dict[move_info[2],move_info[3]] = move_info[1]

def recycle_move_judge(player_move):	# check all illegal input and illegal recycle moves

	move_info = player_move.split(' ')

	if (len(move_info) != 7):	#check length
		return False

	if (len(move_info[0]) != 1):	#check first char A-F
		return False
	if ((ord(move_info[0]) < 65) or (ord(move_info[0]) > 72)):	
		return False

	if (len(move_info[2]) != 1):	#check third char A-F
		return False
	if ((ord(move_info[2]) < 65) or (ord(move_info[2]) > 72)):	
		return False

	if (len(move_info[5]) != 1):	#check 6th char A-F
		return False
	if ((ord(move_info[5]) < 65) or (ord(move_info[5]) > 72)):	
		return False

	if (len(move_info[4]) != 1):	#check 5th char
		return False
	if ((ord(move_info[4]) < 49) or (ord(move_info[4]) > 56)):	
		return False

	if (len(move_info[1]) != 1) and (len(move_info[1]) != 2):	#check 2nd
		return False
	if (len(move_info[1]) == 1):
		if ((ord(move_info[1]) < 49) or (ord(move_info[1]) > 57)):
			return False
	if (len(move_info[1]) == 2):
		if (ord(move_info[1][0]) != 49):
			return False
		if (not(48 <= ord(move_info[1][1]) <= 50)):
			return False

	if (len(move_info[3]) != 1) and (len(move_info[3]) != 2):	#check 4th
		return False
	if (len(move_info[3]) == 1):
		if ((ord(move_info[3]) < 49) or (ord(move_info[3]) > 57)):
			return False
	if (len(move_info[3]) == 2):
		if (ord(move_info[3][0]) != 49):
			return False
		if (not(48 <= ord(move_info[3][1]) <= 50)):
			return False

	if (len(move_info[6]) != 1) and (len(move_info[6]) != 2):	#check 7th
		return False
	if (len(move_info[6]) == 1):
		if ((ord(move_info[6]) < 49) or (ord(move_info[6]) > 57)):
			return False
	if (len(move_info[6]) == 2):
		if (ord(move_info[6][0]) != 49):
			return False
		if (not(48 <= ord(move_info[6][1]) <= 50)):
			return False

	# check if two position entered for picking the card correct or not
	if not(((move_info[0] == move_info[2]) and (int(move_info[1]) == (int(move_info[3]) - 1))) or ((move_info[1] == move_info[3]) and (ord(move_info[0]) == (ord(move_info[2]) - 1)))):
		return False

	# check if there exists a card as the input positions
	if (move_info[0],move_info[1]) not in card_dict:
		return False
	if (move_info[0],move_info[1]) in card_dict:
		if card_dict[move_info[0],move_info[1]] in ('1','3','5','7'):
			if not((move_info[1] == move_info[3]) and (ord(move_info[0]) == (ord(move_info[2]) - 1))):
				return False
		if card_dict[move_info[0],move_info[1]] in ('2','4','6','8'):
			if not((move_info[0] == move_info[2]) and (int(move_info[1]) == (int(move_info[3]) - 1))):
				return False

	# check if the card choose is opponent just placed
	if ((move_info[0] == last_added_card[1]) and (move_info[1] == last_added_card[2])):
		return False

	# check if the card put back to same position and NOT changing orientation
	if ((move_info[5] == move_info[0]) and (move_info[6] == move_info[1])):
		if (card_dict[move_info[0],move_info[1]] == move_info[4]):
			return False

	# check if recycle a card that would temporarily leave the board in an illegal state
	# means recycle a card that has something on top of it
	if (move_info[0] == move_info[2]):
		if (int(move_info[3]) != 12):
			if (board[11 - int(move_info[3])][ord(move_info[0]) - 65] != '   '):
				return False
	if (move_info[1] == moving_times[3]):
		if (int(move_info[3]) != 12):
			if ((board[11 - int(move_info[3])][ord(move_info[0]) - 65] != '   ') or (board[11 - int(move_info[3])][ord(move_info[2]) - 65] != '   ')):
				return False

	# check if there is card exists on put back position
	if board[12 - int(move_info[6])][ord(move_info[5]) - 65] != '   ':
		return False

	# check if after recycle, below illegal space and out of limit
	if (move_info[4] in ('1','3','5','7')):
		#check if there is illegal space below cases 1357

		if (move_info[5] == 'H'):	#check out of limit
			return False

		if (int(move_info[6]) != 1):	# pass if it is 1, no space below, else check if below exists space
			if ((board[13 - int(move_info[6])][ord(move_info[5]) - 65] == '   ') or (board[13 - int(move_info[6])][ord(move_info[5]) - 64] == '   ')):
				return False

		if board[12 - int(move_info[6])][ord(move_info[5]) - 64] != '   ':	# check if there is card exists 
			return False

	if (move_info[4] in ('2','4','6','8')):
		#check if there is illegal space below cases 2468

		if (int(move_info[6]) == 12):	#check out of limit
			return False

		if (int(move_info[6]) != 1):
			if (board[13 - int(move_info[6])][ord(move_info[5]) - 65] == '   '):
				return False

		if board[11 - int(move_info[6])][ord(move_info[5]) - 64] != '   ':	# check if there is card exists 
			return False


	return True

def recycle_move(player_move): # simply do recycle moving

	global board

	move_info = player_move.split(' ')

	stance_str_list = stances(int(move_info[4]))

	board[12 - int(move_info[6])][ord(move_info[5]) - 65] = stance_str_list[0]

	if (move_info[4] in ('1','3','5','7')):
		board[12 - int(move_info[6])][ord(move_info[5]) - 64] = stance_str_list[1]

	if (move_info[4] in ('2','4','6','8')):
		board[11 - int(move_info[6])][ord(move_info[5]) - 65] = stance_str_list[1]

	# remove recycle original positions
	board[12 - int(move_info[1])][ord(move_info[0]) - 65] = '   '
	board[12 - int(move_info[3])][ord(move_info[2]) - 65] = '   '

	card_added = []
	card_added.append(move_info[4])
	card_added.append(move_info[5])
	card_added.append(move_info[6])

	global last_added_card
	last_added_card = card_added

	global moving_times
	moving_times += 1

	global card_dict
	card_dict.pop((move_info[0],move_info[1]))
	card_dict[move_info[5],move_info[6]] = move_info[4]

def winning_detect_for_dot():	# detect winning for dot

	global last_added_card
	repeat_dot_count = 0
	repeat_same_dot_count = 0

	if (last_added_card[0] in ('1','3','5','7')):

		# check last added card 1 row
		for i in range(0,8):
			if (board[12 - int(last_added_card[2])][i][1] == ' '):
				repeat_dot_count = 0
			else:
				repeat_dot_count += 1
			if (i != 0):
				if (board[12 - int(last_added_card[2])][i][1] == board[12 - int(last_added_card[2])][i - 1][1]):
					repeat_same_dot_count = repeat_dot_count
				else:
					repeat_same_dot_count = 0
					repeat_dot_count = 1
			if (repeat_same_dot_count == 4):
				return True

		# check last added card 2 columns
		repeat_dot_count = 0
		repeat_same_dot_count = 0
		for i in range(0,12):
			if (board[i][ord(last_added_card[1]) - 65][1] == ' '):
				repeat_dot_count = 0
			else:
				repeat_dot_count += 1
			if (i != 0):
				if (board[i][ord(last_added_card[1]) - 65][1] == board[i - 1][ord(last_added_card[1]) - 65][1]):
					repeat_same_dot_count = repeat_dot_count
				else:
					repeat_same_dot_count = 0
					repeat_dot_count = 1
			if (repeat_same_dot_count == 4):
				return True

		repeat_dot_count = 0
		repeat_same_dot_count = 0
		for i in range(0,12):
			if (board[i][ord(last_added_card[1]) - 64][1] == ' '):
				repeat_dot_count = 0
			else:
				repeat_dot_count += 1
			if (i != 0):
				if (board[i][ord(last_added_card[1]) - 64][1] == board[i - 1][ord(last_added_card[1]) - 64][1]):
					repeat_same_dot_count = repeat_dot_count
				else:
					repeat_same_dot_count = 0
					repeat_dot_count = 1
			if (repeat_same_dot_count == 4):
				return True

		# check last added card diagonally 4 times in different lines
		repeat_same_dot_count = 0
		repeat_dot_count = 0
		first_one = 0
		start_row_index = 12 - int(last_added_card[2])
		start_col_index = ord(last_added_card[1]) - 65
		while ((start_row_index != 11) and (start_col_index != 0)):
			start_row_index += 1
			start_col_index -= 1
		while ((start_row_index != 0) and (start_col_index != 7)):
			if (board[start_row_index][start_col_index][1] == ' '):
				repeat_dot_count = 0
			else:
				repeat_dot_count += 1
			if (first_one != 0):
				if (board[start_row_index][start_col_index][1] == board[start_row_index + 1][start_col_index - 1][1]):
					repeat_same_dot_count = repeat_dot_count
				else:
					repeat_same_dot_count = 0
					repeat_dot_count = 1
			if (repeat_same_dot_count == 4):
				return True
			first_one += 1
			start_row_index -= 1
			start_col_index += 1

		repeat_same_dot_count = 0
		repeat_dot_count = 0
		first_one = 0
		start_row_index = 12 - int(last_added_card[2])
		start_col_index = ord(last_added_card[1]) - 65
		while ((start_row_index != 0) and (start_col_index != 0)):
			start_row_index -= 1
			start_col_index -= 1
		while ((start_row_index != 11) and (start_col_index != 7)):
			if (board[start_row_index][start_col_index][1] == ' '):
				repeat_dot_count = 0
			else:
				repeat_dot_count += 1
			if (first_one != 0):
				if (board[start_row_index][start_col_index][1] == board[start_row_index - 1][start_col_index - 1][1]):
					repeat_same_dot_count = repeat_dot_count
				else:
					repeat_same_dot_count = 0
					repeat_dot_count = 1
			if (repeat_same_dot_count == 4):
				return True
			first_one += 1
			start_row_index += 1
			start_col_index += 1

		repeat_same_dot_count = 0
		repeat_dot_count = 0
		first_one = 0
		start_row_index = 12 - int(last_added_card[2])
		start_col_index = ord(last_added_card[1]) - 64
		while ((start_row_index != 11) and (start_col_index != 0)):
			start_row_index += 1
			start_col_index -= 1
		while ((start_row_index != 0) and (start_col_index != 7)):
			if (board[start_row_index][start_col_index][1] == ' '):
				repeat_dot_count = 0
			else:
				repeat_dot_count += 1
			if (first_one != 0):
				if (board[start_row_index][start_col_index][1] == board[start_row_index + 1][start_col_index - 1][1]):
					repeat_same_dot_count = repeat_dot_count
				else:
					repeat_same_dot_count = 0
					repeat_dot_count = 1
			if (repeat_same_dot_count == 4):
				return True
			first_one += 1
			start_row_index -= 1
			start_col_index += 1

		repeat_same_dot_count = 0
		repeat_dot_count = 0
		first_one = 0
		start_row_index = 12 - int(last_added_card[2])
		start_col_index = ord(last_added_card[1]) - 64
		while ((start_row_index != 0) and (start_col_index != 0)):
			start_row_index -= 1
			start_col_index -= 1
		while ((start_row_index != 11) and (start_col_index != 7)):
			if (board[start_row_index][start_col_index][1] == ' '):
				repeat_dot_count = 0
			else:
				repeat_dot_count += 1
			if (first_one != 0):
				if (board[start_row_index][start_col_index][1] == board[start_row_index - 1][start_col_index - 1][1]):
					repeat_same_dot_count = repeat_dot_count
				else:
					repeat_same_dot_count = 0
					repeat_dot_count = 1
			if (repeat_same_dot_count == 4):
				return True
			first_one += 1
			start_row_index += 1
			start_col_index += 1

	if (last_added_card[0] in ('2','4','6','8')):

		# check last added card 2 rows
		for i in range(0,8):
			if (board[12 - int(last_added_card[2])][i][1] == ' '):
				repeat_dot_count = 0
			else:
				repeat_dot_count += 1
			if (i != 0):
				if (board[12 - int(last_added_card[2])][i][1] == board[12 - int(last_added_card[2])][i - 1][1]):
					repeat_same_dot_count = repeat_dot_count
				else:
					repeat_same_dot_count = 0
					repeat_dot_count = 1
			if (repeat_same_dot_count == 4):
				return True

		repeat_dot_count = 0
		repeat_same_dot_count = 0
		for i in range(0,8):
			if (board[11 - int(last_added_card[2])][i][1] == ' '):
				repeat_dot_count = 0
			else:
				repeat_dot_count += 1
			if (i != 0):
				if (board[11 - int(last_added_card[2])][i][1] == board[11 - int(last_added_card[2])][i - 1][1]):
					repeat_same_dot_count = repeat_dot_count
				else:
					repeat_same_dot_count = 0
					repeat_dot_count = 1
			if (repeat_same_dot_count == 4):
				return True

		# check last added card 1 column
		repeat_dot_count = 0
		repeat_same_dot_count = 0
		for i in range(0,12):
			if (board[i][ord(last_added_card[1]) - 65][1] == ' '):
				repeat_dot_count = 0
			else:
				repeat_dot_count += 1
			if (i != 0):
				if (board[i][ord(last_added_card[1]) - 65][1] == board[i - 1][ord(last_added_card[1]) - 65][1]):
					repeat_same_dot_count = repeat_dot_count
				else:
					repeat_same_dot_count = 0
					repeat_dot_count = 1
			if (repeat_same_dot_count == 4):
				return True

		# check last added card diagonally 4 times in different lines
		repeat_same_dot_count = 0
		repeat_dot_count = 0
		first_one = 0
		start_row_index = 12 - int(last_added_card[2])
		start_col_index = ord(last_added_card[1]) - 65
		while ((start_row_index != 11) and (start_col_index != 0)):
			start_row_index += 1
			start_col_index -= 1
		while ((start_row_index != 0) and (start_col_index != 7)):
			if (board[start_row_index][start_col_index][1] == ' '):
				repeat_dot_count = 0
			else:
				repeat_dot_count += 1
			if (first_one != 0):
				if (board[start_row_index][start_col_index][1] == board[start_row_index + 1][start_col_index - 1][1]):
					repeat_same_dot_count = repeat_dot_count
				else:
					repeat_same_dot_count = 0
					repeat_dot_count = 1
			if (repeat_same_dot_count == 4):
				return True
			first_one += 1
			start_row_index -= 1
			start_col_index += 1

		repeat_same_dot_count = 0
		repeat_dot_count = 0
		first_one = 0
		start_row_index = 12 - int(last_added_card[2])
		start_col_index = ord(last_added_card[1]) - 65
		while ((start_row_index != 0) and (start_col_index != 0)):
			start_row_index -= 1
			start_col_index -= 1
		while ((start_row_index != 11) and (start_col_index != 7)):
			if (board[start_row_index][start_col_index][1] == ' '):
				repeat_dot_count = 0
			else:
				repeat_dot_count += 1
			if (first_one != 0):
				if (board[start_row_index][start_col_index][1] == board[start_row_index - 1][start_col_index - 1][1]):
					repeat_same_dot_count = repeat_dot_count
				else:
					repeat_same_dot_count = 0
					repeat_dot_count = 1
			if (repeat_same_dot_count == 4):
				return True
			first_one += 1
			start_row_index += 1
			start_col_index += 1

		repeat_same_dot_count = 0
		repeat_dot_count = 0
		first_one = 0
		start_row_index = 11 - int(last_added_card[2])
		start_col_index = ord(last_added_card[1]) - 65
		while ((start_row_index != 11) and (start_col_index != 0)):
			start_row_index += 1
			start_col_index -= 1
		while ((start_row_index != 0) and (start_col_index != 7)):
			if (board[start_row_index][start_col_index][1] == ' '):
				repeat_dot_count = 0
			else:
				repeat_dot_count += 1
			if (first_one != 0):
				if (board[start_row_index][start_col_index][1] == board[start_row_index + 1][start_col_index - 1][1]):
					repeat_same_dot_count = repeat_dot_count
				else:
					repeat_same_dot_count = 0
					repeat_dot_count = 1
			if (repeat_same_dot_count == 4):
				return True
			first_one += 1
			start_row_index -= 1
			start_col_index += 1

		repeat_same_dot_count = 0
		repeat_dot_count = 0
		first_one = 0
		start_row_index = 11 - int(last_added_card[2])
		start_col_index = ord(last_added_card[1]) - 65
		while ((start_row_index != 0) and (start_col_index != 0)):
			start_row_index -= 1
			start_col_index -= 1
		while ((start_row_index != 11) and (start_col_index != 7)):
			if (board[start_row_index][start_col_index][1] == ' '):
				repeat_dot_count = 0
			else:
				repeat_dot_count += 1
			if (first_one != 0):
				if (board[start_row_index][start_col_index][1] == board[start_row_index - 1][start_col_index - 1][1]):
					repeat_same_dot_count = repeat_dot_count
				else:
					repeat_same_dot_count = 0
					repeat_dot_count = 1
			if (repeat_same_dot_count == 4):
				return True
			first_one += 1
			start_row_index += 1
			start_col_index += 1

def winning_detect_for_color():
	# detect color winning 

	global last_added_card
	repeat_color_count = 0
	repeat_same_color_count = 0

	if (last_added_card[0] in ('1','3','5','7')):

		# check last added card 1 row
		for i in range(0,8):
			if (board[12 - int(last_added_card[2])][i][0] == ' '):
				repeat_color_count = 0
			else:
				repeat_color_count += 1
			if (i != 0):
				if (board[12 - int(last_added_card[2])][i][0] == board[12 - int(last_added_card[2])][i - 1][0]):
					repeat_same_color_count = repeat_color_count
				else:
					repeat_same_color_count = 0
					repeat_color_count = 1
			if (repeat_same_color_count == 4):
				return True

		# check last added card 2 columns
		repeat_color_count = 0
		repeat_same_color_count = 0
		for i in range(0,12):
			if (board[i][ord(last_added_card[1]) - 65][0] == ' '):
				repeat_color_count = 0
			else:
				repeat_color_count += 1
			if (i != 0):
				if (board[i][ord(last_added_card[1]) - 65][0] == board[i - 1][ord(last_added_card[1]) - 65][0]):
					repeat_same_color_count = repeat_color_count
				else:
					repeat_same_color_count = 0
					repeat_color_count = 1
			if (repeat_same_color_count == 4):
				return True

		repeat_color_count = 0
		repeat_same_color_count = 0
		for i in range(0,12):
			if (board[i][ord(last_added_card[1]) - 64][0] == ' '):
				repeat_color_count = 0
			else:
				repeat_color_count += 1
			if (i != 0):
				if (board[i][ord(last_added_card[1]) - 64][0] == board[i - 1][ord(last_added_card[1]) - 64][0]):
					repeat_same_color_count = repeat_color_count
				else:
					repeat_same_color_count = 0
					repeat_color_count = 1
			if (repeat_same_color_count == 4):
				return True

		# check last added card diagonally 4 times in different lines
		repeat_same_color_count = 0
		repeat_color_count = 0
		first_one = 0
		start_row_index = 12 - int(last_added_card[2])
		start_col_index = ord(last_added_card[1]) - 65
		while ((start_row_index != 11) and (start_col_index != 0)):
			start_row_index += 1
			start_col_index -= 1
		while ((start_row_index != 0) and (start_col_index != 7)):
			if (board[start_row_index][start_col_index][0] == ' '):
				repeat_color_count = 0
			else:
				repeat_color_count += 1
			if (first_one != 0):
				if (board[start_row_index][start_col_index][0] == board[start_row_index + 1][start_col_index - 1][0]):
					repeat_same_color_count = repeat_color_count
				else:
					repeat_same_color_count = 0
					repeat_color_count = 1
			if (repeat_same_color_count == 4):
				return True
			first_one += 1
			start_row_index -= 1
			start_col_index += 1

		repeat_same_color_count = 0
		repeat_color_count = 0
		first_one = 0
		start_row_index = 12 - int(last_added_card[2])
		start_col_index = ord(last_added_card[1]) - 65
		while ((start_row_index != 0) and (start_col_index != 0)):
			start_row_index -= 1
			start_col_index -= 1
		while ((start_row_index != 11) and (start_col_index != 7)):
			if (board[start_row_index][start_col_index][0] == ' '):
				repeat_color_count = 0
			else:
				repeat_color_count += 1
			if (first_one != 0):
				if (board[start_row_index][start_col_index][0] == board[start_row_index - 1][start_col_index - 1][0]):
					repeat_same_color_count = repeat_color_count
				else:
					repeat_same_color_count = 0
					repeat_color_count = 1
			if (repeat_same_color_count == 4):
				return True
			first_one += 1
			start_row_index += 1
			start_col_index += 1

		repeat_same_color_count = 0
		repeat_color_count = 0
		first_one = 0
		start_row_index = 12 - int(last_added_card[2])
		start_col_index = ord(last_added_card[1]) - 64
		while ((start_row_index != 11) and (start_col_index != 0)):
			start_row_index += 1
			start_col_index -= 1
		while ((start_row_index != 0) and (start_col_index != 7)):
			if (board[start_row_index][start_col_index][0] == ' '):
				repeat_color_count = 0
			else:
				repeat_color_count += 1
			if (first_one != 0):
				if (board[start_row_index][start_col_index][0] == board[start_row_index + 1][start_col_index - 1][0]):
					repeat_same_color_count = repeat_color_count
				else:
					repeat_same_color_count = 0
					repeat_color_count = 1
			if (repeat_same_color_count == 4):
				return True
			first_one += 1
			start_row_index -= 1
			start_col_index += 1

		repeat_same_color_count = 0
		repeat_color_count = 0
		first_one = 0
		start_row_index = 12 - int(last_added_card[2])
		start_col_index = ord(last_added_card[1]) - 64
		while ((start_row_index != 0) and (start_col_index != 0)):
			start_row_index -= 1
			start_col_index -= 1
		while ((start_row_index != 11) and (start_col_index != 7)):
			if (board[start_row_index][start_col_index][0] == ' '):
				repeat_color_count = 0
			else:
				repeat_color_count += 1
			if (first_one != 0):
				if (board[start_row_index][start_col_index][0] == board[start_row_index - 1][start_col_index - 1][0]):
					repeat_same_color_count = repeat_color_count
				else:
					repeat_same_color_count = 0
					repeat_color_count = 1
			if (repeat_same_color_count == 4):
				return True
			first_one += 1
			start_row_index += 1
			start_col_index += 1

	if (last_added_card[0] in ('2','4','6','8')):

		# check last added card 2 rows
		for i in range(0,8):
			if (board[12 - int(last_added_card[2])][i][0] == ' '):
				repeat_color_count = 0
			else:
				repeat_color_count += 1
			if (i != 0):
				if (board[12 - int(last_added_card[2])][i][0] == board[12 - int(last_added_card[2])][i - 1][0]):
					repeat_same_color_count = repeat_color_count
				else:
					repeat_same_color_count = 0
					repeat_color_count = 1
			if (repeat_same_color_count == 4):
				return True

		repeat_color_count = 0
		repeat_same_color_count = 0
		for i in range(0,8):
			if (board[11 - int(last_added_card[2])][i][0] == ' '):
				repeat_color_count = 0
			else:
				repeat_color_count += 1
			if (i != 0):
				if (board[11 - int(last_added_card[2])][i][0] == board[11 - int(last_added_card[2])][i - 1][0]):
					repeat_same_color_count = repeat_color_count
				else:
					repeat_same_color_count = 0
					repeat_color_count = 1
			if (repeat_same_color_count == 4):
				return True

		# check last added card 1 column
		repeat_color_count = 0
		repeat_same_color_count = 0
		for i in range(0,12):
			if (board[i][ord(last_added_card[1]) - 65][0] == ' '):
				repeat_color_count = 0
			else:
				repeat_color_count += 1
			if (i != 0):
				if (board[i][ord(last_added_card[1]) - 65][0] == board[i - 1][ord(last_added_card[1]) - 65][0]):
					repeat_same_color_count = repeat_color_count
				else:
					repeat_same_color_count = 0
					repeat_color_count = 1
			if (repeat_same_color_count == 4):
				return True

		# check last added card diagonally 4 times in different lines
		repeat_same_color_count = 0
		repeat_color_count = 0
		first_one = 0
		start_row_index = 12 - int(last_added_card[2])
		start_col_index = ord(last_added_card[1]) - 65
		while ((start_row_index != 11) and (start_col_index != 0)):
			start_row_index += 1
			start_col_index -= 1
		while ((start_row_index != 0) and (start_col_index != 7)):
			if (board[start_row_index][start_col_index][0] == ' '):
				repeat_color_count = 0
			else:
				repeat_color_count += 1
			if (first_one != 0):
				if (board[start_row_index][start_col_index][0] == board[start_row_index + 1][start_col_index - 1][0]):
					repeat_same_color_count = repeat_color_count
				else:
					repeat_same_color_count = 0
					repeat_color_count = 1
			if (repeat_same_color_count == 4):
				return True
			first_one += 1
			start_row_index -= 1
			start_col_index += 1

		repeat_same_color_count = 0
		repeat_color_count = 0
		first_one = 0
		start_row_index = 12 - int(last_added_card[2])
		start_col_index = ord(last_added_card[1]) - 65
		while ((start_row_index != 0) and (start_col_index != 0)):
			start_row_index -= 1
			start_col_index -= 1
		while ((start_row_index != 11) and (start_col_index != 7)):
			if (board[start_row_index][start_col_index][0] == ' '):
				repeat_color_count = 0
			else:
				repeat_color_count += 1
			if (first_one != 0):
				if (board[start_row_index][start_col_index][0] == board[start_row_index - 1][start_col_index - 1][0]):
					repeat_same_color_count = repeat_color_count
				else:
					repeat_same_color_count = 0
					repeat_color_count = 1
			if (repeat_same_color_count == 4):
				return True
			first_one += 1
			start_row_index += 1
			start_col_index += 1

		repeat_same_color_count = 0
		repeat_color_count = 0
		first_one = 0
		start_row_index = 11 - int(last_added_card[2])
		start_col_index = ord(last_added_card[1]) - 65
		while ((start_row_index != 11) and (start_col_index != 0)):
			start_row_index += 1
			start_col_index -= 1
		while ((start_row_index != 0) and (start_col_index != 7)):
			if (board[start_row_index][start_col_index][0] == ' '):
				repeat_color_count = 0
			else:
				repeat_color_count += 1
			if (first_one != 0):
				if (board[start_row_index][start_col_index][0] == board[start_row_index + 1][start_col_index - 1][0]):
					repeat_same_color_count = repeat_color_count
				else:
					repeat_same_color_count = 0
					repeat_color_count = 1
			if (repeat_same_color_count == 4):
				return True
			first_one += 1
			start_row_index -= 1
			start_col_index += 1

		repeat_same_color_count = 0
		repeat_color_count = 0
		first_one = 0
		start_row_index = 11 - int(last_added_card[2])
		start_col_index = ord(last_added_card[1]) - 65
		while ((start_row_index != 0) and (start_col_index != 0)):
			start_row_index -= 1
			start_col_index -= 1
		while ((start_row_index != 11) and (start_col_index != 7)):
			if (board[start_row_index][start_col_index][0] == ' '):
				repeat_color_count = 0
			else:
				repeat_color_count += 1
			if (first_one != 0):
				if (board[start_row_index][start_col_index][0] == board[start_row_index - 1][start_col_index - 1][0]):
					repeat_same_color_count = repeat_color_count
				else:
					repeat_same_color_count = 0
					repeat_color_count = 1
			if (repeat_same_color_count == 4):
				return True
			first_one += 1
			start_row_index += 1
			start_col_index += 1

def stances(stance):	# choose board values from orientation/stances

	stance_str_list = []

	if ((stance == 1) or (stance == 4)):
		stance_str_list.append('R\u26AB')
		stance_str_list.append('W\u26AA')

	elif ((stance == 2) or (stance == 3)):
		stance_str_list.append('W\u26AA')
		stance_str_list.append('R\u26AB')

	elif ((stance == 5) or (stance == 8)):
		stance_str_list.append('R\u26AA')
		stance_str_list.append('W\u26AB')

	elif ((stance == 6) or (stance ==7)):
		stance_str_list.append('W\u26AB')
		stance_str_list.append('R\u26AA')

	return stance_str_list


# main program starts here, we can change below to main function later for sure

print(''' 
Welcome to the DOUBLE card game!


=======================
|                     |
|                     |
|       DOUBLE CARD   |
|                     |
|        1. PVE       |
|        2. PVP       |
|                     |
|                     |
|======================

					  
	''')

player_choice = input()

while (player_choice not in ('0','1','2')):
	print('Invalid gaming type, enter again.')
	player_choice = input()

if (player_choice == str(0)):
	print('YOU ARE IN SECRET DEMO MODE NOW.\nNOW YOU CAN COPY & PASTE TONS OF COMMANDS AS 1 INPUT TO THE CONSOLE.\nTHE SYSTEM WILL RUN AUTOMATICALLY.')
	# will add code here before the demo for one shot copy & paste input

if (player_choice == str(1)):
	print('Not add AI yet.')

if (player_choice == str(2)):
	print('Starting PVP game!')
	print_board()

	print('Now choose "dot" or "color" for player1, player2 will automatically get the other.')
	print('Enter "dot" or "color" for player1>>')
	player_choice = input()
	while ((player_choice != 'color') and (player_choice != 'dot')):
		print('Invalid choice, enter again.')
		player_choice = input()
	game_dict['player1'] = player_choice
	if (player_choice == 'dot'):
		game_dict['player2'] = 'color'
	else:
		game_dict['player2'] = 'dot'

	while(moving_times < 60):           # play until 60 rounds

		if(moving_times < 24):		# regular until 24 rounds
			print('player1_regular>> ')
			player1_move = input()
			while (regular_move_judge(player1_move) == False):
				print('Illegal Move! I will give ya a chance to move it again.')
				player1_move = input()
			regular_move(player1_move)
			print_board()
			if (game_dict['player1'] == 'dot'):
				if (winning_detect_for_dot() == True):
					print('Game ends. Winner is player1.')
					win = True
					break
				if (winning_detect_for_color() == True):
					print('Game ends. Winner is player2')
					win = True
					break
			else:
				if (winning_detect_for_color() == True):
					print('Game ends. Winner is player1.')
					win = True
					break
				if (winning_detect_for_dot() == True):
					print('Game ends. Winner is player2.')
					win = True
					break

			print('player2_regular>> ')
			player2_move = input()
			while (regular_move_judge(player2_move) == False):
				print('Illegal Move! I will give ya a chance to move it again.')
				player2_move = input()
			regular_move(player2_move)
			print_board()
			if (game_dict['player2'] == 'dot'):
				if (winning_detect_for_dot() == True):
					print('Game ends. Winner is player2.')
					win = True
					break
				if (winning_detect_for_color() == True):
					print('Game ends. Winner is player1')
					win = True
					break
			else:
				if (winning_detect_for_color() == True):
					print('Game ends. Winner is player2.')
					win = True
					break
				if (winning_detect_for_dot() == True):
					print('Game ends. Winner is player1.')
					win = True
					break

		else: 			# recycle
			print('player1_recycle>> ')
			player1_move = input()
			while (recycle_move_judge(player1_move) == False):
				print('Illegal Move! I will give ya a chance to move it again.')
				player1_move = input()
			recycle_move(player1_move)
			print_board()
			if (game_dict['player1'] == 'dot'):
				if (winning_detect_for_dot() == True):
					print('Game ends. Winner is player1.')
					win = True
					break
				if (winning_detect_for_color() == True):
					print('Game ends. Winner is player2')
					win = True
					break
			else:
				if (winning_detect_for_color() == True):
					print('Game ends. Winner is player1.')
					win = True
					break
				if (winning_detect_for_dot() == True):
					print('Game ends. Winner is player2.')
					win = True
					break

			print('player2_recycle>> ')
			player2_move = input()
			while (recycle_move_judge(player2_move) == False):
				print('Illegal Move! I will give ya a chance to move it again.')
				player2_move = input()
			recycle_move(player2_move)
			print_board()
			if (game_dict['player2'] == 'dot'):
				if (winning_detect_for_dot() == True):
					print('Game ends. Winner is player2.')
					win = True
					break
				if (winning_detect_for_color() == True):
					print('Game ends. Winner is player1')
					win = True
					break
			else:
				if (winning_detect_for_color() == True):
					print('Game ends. Winner is player2.')
					win = True
					break
				if (winning_detect_for_dot() == True):
					print('Game ends. Winner is player1.')
					win = True
					break

	if (win == False):
		print('Draw. No winner this game.')