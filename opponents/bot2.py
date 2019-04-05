# uncompyle6 version 3.2.5
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.5.2 (default, Nov 12 2018, 13:43:14) 
# [GCC 5.4.0 20160609]
# Embedded file name: /mnt/c/Users/Teja Dhondu/Desktop/jai-ballaya/bot.py
# Compiled at: 2019-03-03 16:35:30
from copy import deepcopy
from time import time
from random import randint

class Bot:

    def __init__(self):
        self.my_flag = 'x'
        self.opp_flag = 'o'
        self.start_time = 0
        self.first = True
        self.draw_utility = 0
        self.win_utility = long(1000000000000000000)
        self.lose_utility = long(-1 * 1000000000000000000)
        self.heuristic_store = {}
        self.block_store = {}
        self.ab_store = {}
        self.bit_string = [ [ [ [ long(0) for k in range(2) ] for j in range(9) ] for i in range(9) ] for y in range(2) ]
        self.board_hash = long(0)
        self.block_hash = [ [ [ long(0) for j in range(3) ] for i in range(3) ] for y in range(2) ]
        self.init_hash()
        self.count = 0
        self.score_block = 1000.0
        self.score1 = 100.0
        self.score2 = 10.0
        self.attack_weight = 37729
        self.game_weight = 8.2034

    def init_hash(self):
        for y in range(0, 2):
            for i in range(9):
                for j in range(9):
                    for k in range(2):
                        self.bit_string[y][i][j][k] = long(randint(1, 18446744073709551616))

    def add_to_hash(self, action, ply):
        x = action[0]
        y = action[1]
        z = action[2]
        self.board_hash ^= self.bit_string[x][y][z][ply]
        self.block_hash[x][y / 3][(z / 3)] ^= self.bit_string[x][y][z][ply]

    def calculate_hashes(self, board):
        self.board_hash = long(0)
        self.block_hash = [ [ [ long(0) for j in range(3) ] for i in range(3) ] for y in range(2) ]
        for i in range(2):
            for j in range(9):
                for k in range(9):
                    if board.big_boards_status[i][j][k] == self.my_flag:
                        self.board_hash ^= self.bit_string[i][j][k][0]
                        self.block_hash[i][j / 3][(k / 3)] ^= self.bit_string[i][j][k][0]
                    elif board.big_boards_status[i][j][k] == self.opp_flag:
                        self.board_hash ^= self.bit_string[i][j][k][1]
                        self.block_hash[i][j / 3][(k / 3)] ^= self.bit_string[i][j][k][1]

    def opposite_flag(self, flag):
        if flag == 'x':
            return 'o'
        return 'x'

    def update(self, board, old_move, new_move, ply):
        board.big_boards_status[new_move[0]][new_move[1]][new_move[2]] = ply
        x = new_move[1] / 3
        y = new_move[2] / 3
        k = new_move[0]
        bs = board.big_boards_status[k]
        for i in range(3):
            if bs[3 * x + i][3 * y] == bs[3 * x + i][3 * y + 1] == bs[3 * x + i][3 * y + 2] and bs[3 * x + i][3 * y] == ply:
                board.small_boards_status[k][x][y] = ply
                return True
            if bs[3 * x][3 * y + i] == bs[3 * x + 1][3 * y + i] == bs[3 * x + 2][3 * y + i] and bs[3 * x][3 * y + i] == ply:
                board.small_boards_status[k][x][y] = ply
                return True

        if bs[3 * x][3 * y] == bs[3 * x + 1][3 * y + 1] == bs[3 * x + 2][3 * y + 2] and bs[3 * x][3 * y] == ply:
            board.small_boards_status[k][x][y] = ply
            return True
        if bs[3 * x][3 * y + 2] == bs[3 * x + 1][3 * y + 1] == bs[3 * x + 2][3 * y] and bs[3 * x][3 * y + 2] == ply:
            board.small_boards_status[k][x][y] = ply
            return True
        for i in range(3):
            for j in range(3):
                if bs[3 * x + i][3 * y + j] == '-':
                    return False

        board.small_boards_status[k][x][y] = 'd'
        return False

    def block_score(self, board, board_num, block_num, ply):
        b1 = block_num / 3
        b2 = block_num % 3
        if (
         self.block_hash[board_num][b1][b2], ply) in self.block_store:
            return self.block_store[(self.block_hash[board_num][b1][b2], ply)]
        if board.small_boards_status[board_num][b1][b2] == ply:
            return self.score_block
        if board.small_boards_status[board_num][b1][b2] == self.opposite_flag(ply) or board.small_boards_status[board_num][b1][b2] == 'd':
            return 0

        def convert2num(flag):
            if flag == ply:
                return 1
            if flag == '-':
                return 0
            return -2

        lines = [
         0, 0, 0, 0, 0, 0, 0, 0]
        lines[0] = convert2num(board.big_boards_status[board_num][3 * b1][3 * b2]) + convert2num(board.big_boards_status[board_num][3 * b1][3 * b2 + 1]) + convert2num(board.big_boards_status[board_num][3 * b1][3 * b2 + 2])
        lines[1] = convert2num(board.big_boards_status[board_num][3 * b1 + 1][3 * b2]) + convert2num(board.big_boards_status[board_num][3 * b1 + 1][3 * b2 + 1]) + convert2num(board.big_boards_status[board_num][3 * b1 + 1][3 * b2 + 2])
        lines[2] = convert2num(board.big_boards_status[board_num][3 * b1 + 2][3 * b2]) + convert2num(board.big_boards_status[board_num][3 * b1 + 2][3 * b2 + 1]) + convert2num(board.big_boards_status[board_num][3 * b1 + 2][3 * b2 + 2])
        lines[3] = convert2num(board.big_boards_status[board_num][3 * b1][3 * b2]) + convert2num(board.big_boards_status[board_num][3 * b1 + 1][3 * b2]) + convert2num(board.big_boards_status[board_num][3 * b1 + 2][3 * b2])
        lines[4] = convert2num(board.big_boards_status[board_num][3 * b1][3 * b2 + 1]) + convert2num(board.big_boards_status[board_num][3 * b1 + 1][3 * b2 + 1]) + convert2num(board.big_boards_status[board_num][3 * b1 + 2][3 * b2 + 1])
        lines[5] = convert2num(board.big_boards_status[board_num][3 * b1][3 * b2 + 2]) + convert2num(board.big_boards_status[board_num][3 * b1 + 1][3 * b2 + 2]) + convert2num(board.big_boards_status[board_num][3 * b1 + 2][3 * b2 + 2])
        lines[6] = convert2num(board.big_boards_status[board_num][3 * b1][3 * b2]) + convert2num(board.big_boards_status[board_num][3 * b1 + 1][3 * b2 + 1]) + convert2num(board.big_boards_status[board_num][3 * b1 + 2][3 * b2 + 2])
        lines[7] = convert2num(board.big_boards_status[board_num][3 * b1][3 * b2 + 2]) + convert2num(board.big_boards_status[board_num][3 * b1 + 1][3 * b2 + 1]) + convert2num(board.big_boards_status[board_num][3 * b1 + 2][3 * b2])
        two_attacks = 0
        one_attacks = 0
        for i in range(0, 8):
            if lines[i] == 1:
                two_attacks += 1.0
            elif lines[i] == 2:
                one_attacks += 1.0

        my_block_score = self.score1 * one_attacks + self.score2 * two_attacks
        self.block_store[(self.block_hash[board_num][b1][b2], ply)] = my_block_score
        return my_block_score

    def game_score(self, board, board_num, ply):
        my_block1 = self.block_score(board, board_num, 0, ply)
        my_block2 = self.block_score(board, board_num, 1, ply)
        my_block3 = self.block_score(board, board_num, 2, ply)
        my_block4 = self.block_score(board, board_num, 3, ply)
        my_block5 = self.block_score(board, board_num, 4, ply)
        my_block6 = self.block_score(board, board_num, 5, ply)
        my_block7 = self.block_score(board, board_num, 6, ply)
        my_block8 = self.block_score(board, board_num, 7, ply)
        my_block9 = self.block_score(board, board_num, 8, ply)
        line_score = 0
        line_score += my_block1 * my_block2 * my_block3
        line_score += my_block1 * my_block4 * my_block7
        line_score += my_block1 * my_block5 * my_block9
        line_score += my_block2 * my_block5 * my_block8
        line_score += my_block3 * my_block5 * my_block7
        line_score += my_block3 * my_block6 * my_block9
        line_score += my_block4 * my_block5 * my_block6
        line_score += my_block7 * my_block8 * my_block9
        return line_score

    def heuristic(self, board):
        if time() - self.start_time >= 10:
            return -1
        if self.board_hash in self.heuristic_store:
            return self.heuristic_store[self.board_hash]
        my_attack_score = 0
        my_attack_score += 4 * (self.block_score(board, 0, 0, self.my_flag) + self.block_score(board, 1, 0, self.my_flag))
        my_attack_score += 6 * (self.block_score(board, 0, 1, self.my_flag) + self.block_score(board, 1, 1, self.my_flag))
        my_attack_score += 4 * (self.block_score(board, 0, 2, self.my_flag) + self.block_score(board, 1, 2, self.my_flag))
        my_attack_score += 6 * (self.block_score(board, 0, 3, self.my_flag) + self.block_score(board, 1, 3, self.my_flag))
        my_attack_score += 3 * (self.block_score(board, 0, 4, self.my_flag) + self.block_score(board, 1, 4, self.my_flag))
        my_attack_score += 6 * (self.block_score(board, 0, 5, self.my_flag) + self.block_score(board, 1, 5, self.my_flag))
        my_attack_score += 4 * (self.block_score(board, 0, 6, self.my_flag) + self.block_score(board, 1, 6, self.my_flag))
        my_attack_score += 6 * (self.block_score(board, 0, 7, self.my_flag) + self.block_score(board, 1, 7, self.my_flag))
        my_attack_score += 4 * (self.block_score(board, 0, 8, self.my_flag) + self.block_score(board, 1, 8, self.my_flag))
        if time() - self.start_time >= 10:
            return -1
        opp_attack_score = 0
        opp_attack_score += 4 * (self.block_score(board, 0, 0, self.opp_flag) + self.block_score(board, 1, 0, self.opp_flag))
        opp_attack_score += 6 * (self.block_score(board, 0, 1, self.opp_flag) + self.block_score(board, 1, 1, self.opp_flag))
        opp_attack_score += 4 * (self.block_score(board, 0, 2, self.opp_flag) + self.block_score(board, 1, 2, self.opp_flag))
        opp_attack_score += 6 * (self.block_score(board, 0, 3, self.opp_flag) + self.block_score(board, 1, 3, self.opp_flag))
        opp_attack_score += 3 * (self.block_score(board, 0, 4, self.opp_flag) + self.block_score(board, 1, 4, self.opp_flag))
        opp_attack_score += 6 * (self.block_score(board, 0, 5, self.opp_flag) + self.block_score(board, 1, 5, self.opp_flag))
        opp_attack_score += 4 * (self.block_score(board, 0, 6, self.opp_flag) + self.block_score(board, 1, 6, self.opp_flag))
        opp_attack_score += 6 * (self.block_score(board, 0, 7, self.opp_flag) + self.block_score(board, 1, 7, self.opp_flag))
        opp_attack_score += 4 * (self.block_score(board, 0, 8, self.opp_flag) + self.block_score(board, 1, 8, self.opp_flag))
        if time() - self.start_time >= 10:
            return -1
        my_game_score = self.game_score(board, 0, self.my_flag) + self.game_score(board, 1, self.my_flag)
        if time() - self.start_time >= 10:
            return -1
        opp_game_score = self.game_score(board, 0, self.opp_flag) + self.game_score(board, 1, self.opp_flag)
        x1 = my_attack_score - opp_attack_score
        x2 = my_game_score - opp_game_score
        c1 = 3.77497239 * 10000
        c2 = 8.20172422
        c3 = 0.49628911
        c4 = -9.94908108 / 1000000
        c5 = 5.71747239 / 10000000000
        h = c1 * x1 + c2 * x2 + c3 * x1 ** 2 + c4 * x1 * x2 + c5 * x2 ** 2
        self.heuristic_store[self.board_hash] = h
        return h

    def eval(self, board, terminal_check):
        if terminal_check[1] == 'WON':
            if terminal_check[0] == self.my_flag:
                return self.win_utility
            return self.lose_utility
        else:
            if terminal_check[1] == 'DRAW':
                return self.draw_utility
        return self.heuristic(board)

    def max_value(self, board, alpha, beta, depth, old_move, bonus):
        self.count += 1
        if time() - self.start_time >= 10:
            return (-1, (-1, -1, -1))
        if (
         self.board_hash, old_move[1] % 3, old_move[2] % 3, 0) in self.ab_store:
            return self.ab_store[(self.board_hash, old_move[1] % 3, old_move[2] % 3, 0)]
        terminal_check = board.find_terminal_state()
        if time() - self.start_time >= 10:
            return (-1, (-1, -1, -1))
        if terminal_check[0] != 'CONTINUE' or depth == 0:
            return (self.eval(board, terminal_check), (-1, -1, -1))
        best_utility = float('-inf')
        best_action = (-1, -1, -1)
        for action in board.find_valid_move_cells(old_move):
            if time() - self.start_time >= 10:
                return (-1, (-1, -1, -1))
            self.add_to_hash(action, 0)
            if self.update(board, old_move, action, self.my_flag) and not bonus:
                utility, _ = self.max_value(board, alpha, beta, depth - 1, action, True)
            else:
                utility, _ = self.min_value(board, alpha, beta, depth - 1, action, False)
            if time() - self.start_time >= 10:
                return (-1, (-1, -1, -1))
            board.big_boards_status[action[0]][action[1]][action[2]] = '-'
            board.small_boards_status[action[0]][action[1] / 3][action[2] / 3] = '-'
            self.add_to_hash(action, 0)
            if utility > best_utility:
                best_utility = utility
                best_action = action
            if best_utility >= beta:
                self.ab_store[(self.board_hash, old_move[1] % 3, old_move[2] % 3, 0)] = (
                 best_utility, best_action)
                return (
                 best_utility, best_action)
            alpha = max(alpha, best_utility)

        self.ab_store[(self.board_hash, old_move[1] % 3, old_move[2] % 3, 0)] = (best_utility, best_action)
        return (
         best_utility, best_action)

    def min_value(self, board, alpha, beta, depth, old_move, bonus):
        self.count += 1
        if time() - self.start_time >= 10:
            return (-1, (-1, -1, -1))
        if (
         self.board_hash, old_move[1] % 3, old_move[2] % 3, 1) in self.ab_store:
            return self.ab_store[(self.board_hash, old_move[1] % 3, old_move[2] % 3, 1)]
        terminal_check = board.find_terminal_state()
        if time() - self.start_time >= 10:
            return (-1, (-1, -1, -1))
        if terminal_check[0] != 'CONTINUE' or depth == 0:
            return (self.eval(board, terminal_check), (-1, -1, -1))
        best_utility = float('inf')
        best_action = (-1, -1, -1)
        for action in board.find_valid_move_cells(old_move):
            if time() - self.start_time >= 10:
                return (-1, (-1, -1, -1))
            self.add_to_hash(action, 1)
            if self.update(board, old_move, action, self.opp_flag) and not bonus:
                utility, _ = self.min_value(board, alpha, beta, depth - 1, action, True)
            else:
                utility, _ = self.max_value(board, alpha, beta, depth - 1, action, False)
            if time() - self.start_time >= 10:
                return (float('-inf'), (-1, -1, -1))
            board.big_boards_status[action[0]][action[1]][action[2]] = '-'
            board.small_boards_status[action[0]][action[1] / 3][action[2] / 3] = '-'
            self.add_to_hash(action, 1)
            if utility < best_utility:
                best_utility = utility
                best_action = action
            if best_utility <= alpha:
                self.ab_store[(self.board_hash, old_move[1] % 3, old_move[2] % 3, 1)] = (
                 best_utility, best_action)
                return (
                 best_utility, best_action)
            beta = min(beta, best_utility)

        self.ab_store[(self.board_hash, old_move[1] % 3, old_move[2] % 3, 1)] = (best_utility, best_action)
        return (
         best_utility, best_action)

    def alpha_beta_search(self, board, depth, old_move):
        if board.big_boards_status[old_move[0]][old_move[1]][old_move[2]] == self.my_flag:
            utility, action = self.max_value(board, float('-inf'), float('inf'), depth, old_move, True)
        else:
            utility, action = self.max_value(board, float('-inf'), float('inf'), depth, old_move, False)
        return (utility, action)

    def move(self, board, old_move, flag):
        self.start_time = time()
        self.count = 0
        if self.first:
            self.my_flag = flag
            self.opp_flag = self.opposite_flag(self.my_flag)
            self.first = False
        board_copy = deepcopy(board)
        self.calculate_hashes(board_copy)
        self.ab_store = {}
        best_action = board_copy.find_valid_move_cells(old_move)[0]
        best_utility = float('-inf')
        depth = 3
        while True:
            utility, action = self.alpha_beta_search(board_copy, depth, old_move)
            if time() - self.start_time >= 10:
                break
            best_action = action
            best_utility = utility
            depth += 2
            self.ab_store = {}

        return best_action
