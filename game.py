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

last_added_card = []

game_dict = {}

board_values = [] 
for i in range(0,96):
	board_values.append('  ')

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

	if ((move_info[1] == '1') or (move_info[1] == '3') or (move_info[1] == '5') or (move_info[1] == '7')):
		#check if there is illegal space below cases 1357

		if (move_info[2] == 'H'):	#check out of limit
			return False

		if (int(move_info[3]) != 1):	# pass if it is 1, no space below, else check if below exists space
			if ((board[13 - int(move_info[3])][ord(move_info[2]) - 65] == '  ') or (board[13 - int(move_info[3])][ord(move_info[2]) - 64] == '  ')):
				return False

	if ((move_info[1] == '2') or (move_info[1] == '4') or (move_info[1] == '6') or (move_info[1] == '8')):
		#check if there is illegal space below cases 2468

		if (int(move_info[3]) == 12):	#check out of limit
			return False

		if (int(move_info[3]) != 1):
			if (board[13 - int(move_info[3])][ord(move_info[2]) - 65] == '  '):
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

	if ((move_info[1] == '1') or (move_info[1] == '3') or (move_info[1] == '5') or (move_info[1] == '7')):
		board[12 - int(move_info[3])][ord(move_info[2]) - 64] = stance_str_list[1]

	if ((move_info[1] == '2') or (move_info[1] == '4') or (move_info[1] == '6') or (move_info[1] == '8')):
		board[11 - int(move_info[3])][ord(move_info[2]) - 65] = stance_str_list[1]

	card_added = []
	card_added.append(move_info[1])
	card_added.append(move_info[2])
	card_added.append(move_info[3])

	global last_added_card
	last_added_card = card_added

	global moving_times
	moving_times += 1

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

	# check if the card choose is opponent just placed
	if ((move_info[0] == last_added_card[1]) and (move_info[1] == last_added_card[2])):
		return False

	# check if the card put back to same position and NOT changing orientation


	# check if recycle a card that would temporarily leave the board in an illegal state
	# means recycle a card that has something on top of it
	if (move_info[0] == move_info[2]):
		if (int(move_info[3]) != 12):
			if (board[11 - int(move_info[3])][ord(move_info[0]) - 65] != '  '):
				return False
	if (move_info[1] == moving_times[3]):
		if (int(move_info[3]) != 12):
			if ((board[11 - int(move_info[3])][ord(move_info[0]) - 65] != '  ') or (board[11 - int(move_info[3])][ord(move_info[2]) - 65] != '  ')):
				return False

	# check if after recycle, below illegal space and out of limit
	if ((move_info[4] == '1') or (move_info[4] == '3') or (move_info[4] == '5') or (move_info[4] == '7')):
		#check if there is illegal space below cases 1357

		if (move_info[5] == 'H'):	#check out of limit
			return False

		if (int(move_info[6]) != 1):	# pass if it is 1, no space below, else check if below exists space
			if ((board[13 - int(move_info[6])][ord(move_info[5]) - 65] == '  ') or (board[13 - int(move_info[6])][ord(move_info[5]) - 64] == '  ')):
				return False

	if ((move_info[4] == '2') or (move_info[4] == '4') or (move_info[4] == '6') or (move_info[4] == '8')):
		#check if there is illegal space below cases 2468

		if (int(move_info[6]) == 12):	#check out of limit
			return False

		if (int(move_info[6]) != 1):
			if (board[13 - int(move_info[6])][ord(move_info[5]) - 65] == '  '):
				return False
	return True

def recycle_move(player_move): # simply do recycle moving

	global board

	move_info = player_move.split(' ')

	stance_str_list = stances(int(move_info[4]))

	board[12 - int(move_info[6])][ord(move_info[5]) - 65] = stance_str_list[0]

	if ((move_info[4] == '1') or (move_info[4] == '3') or (move_info[4] == '5') or (move_info[4] == '7')):
		board[12 - int(move_info[6])][ord(move_info[5]) - 64] = stance_str_list[1]

	if ((move_info[4] == '2') or (move_info[4] == '4') or (move_info[4] == '6') or (move_info[4] == '8')):
		board[11 - int(move_info[6])][ord(move_info[5]) - 65] = stance_str_list[1]

	# remove recycle original positions
	board[12 - int(move_info[1])][ord(move_info[0]) - 65] = '  '
	board[12 - int(move_info[3])][ord(move_info[2]) - 65] = '  '

	card_added = []
	card_added.append(move_info[4])
	card_added.append(move_info[5])
	card_added.append(move_info[6])

	global last_added_card
	last_added_card = card_added

	global moving_times
	moving_times += 1

def winning_judge():	# detect winning

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


# main program starts here, we can change below to main function in OOP class later for sure

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

while ((player_choice != str(1)) and (player_choice != str(2))):
	print('Invalid gaming type, enter again.')
	player_choice = input()

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

	while(moving_times < 60):           # play

		if(moving_times < 24):		# regular
			print('player1_regular>> ')
			player1_move = input()
			while (regular_move_judge(player1_move) == False):
				print('Illegal Move! I will give ya a chance to move it again.')
				player1_move = input()
			regular_move(player1_move)
			print_board()
			if (winning_judge() == True):
				print('Game ends. Winner is Player1.')
				win = True;
				break;

			print('player2_regular>> ')
			player2_move = input()
			while (regular_move_judge(player2_move) == False):
				print('Illegal Move! I will give ya a chance to move it again.')
				player2_move = input()
			regular_move(player2_move)
			print_board()
			if (winning_judge() == True):
				print('Game ends. Winner is Player2.')
				win = True;
				break;

		else: 			# recycle
			print('player1_recycle>> ')
			player1_move = input()
			while (recycle_move_judge(player1_move) == False):
				print('Illegal Move! I will give ya a chance to move it again.')
				player1_move = input()
			recycle_move(player1_move)
			print_board()
			if (winning_judge() == True):
				print('Game ends. Winner is Player1.')
				win = True;
				break;

			print('player2_recycle>> ')
			player2_move = input()
			while (recycle_move_judge(player2_move) == False):
				print('Illegal Move! I will give ya a chance to move it again.')
				player2_move = input()
			recycle_move(player2_move)
			print_board()
			if (winning_judge() == True):
				print('Game ends. Winner is Player2.')
				win = True;
				break;

	if (win = False):
		print('Draw.')