import random
import datetime
import copy


class Player7:

    def __init__(self, tle):
        self.ALPHA = -100000000
        self.BETA = 100000000
        self.dict = {}
        self.FIRST_POS = [
            [(0, 0), (1, 1), (0, 2)],
            [(0, 0), (1, 1), (2, 0)],
            [(0, 2), (1, 1), (2, 2)],
            [(2, 0), (1, 1), (2, 2)]
        ]
        self.APPR_DIAG = [
            [(0, 0), (1, 1), (2, 2)],
            [(0, 2), (1, 1), (2, 0)],
        ]
        self.APPR_LINE = [
            # Horizontal Wins
            [(0, 0), (0, 1), (0, 2)],
            [(1, 0), (1, 1), (1, 2)],
            [(2, 0), (2, 1), (2, 2)],

            # Vertical Wins
            [(0, 0), (1, 0), (2, 0)],
            [(0, 1), (1, 1), (2, 1)],
            [(0, 2), (1, 2), (2, 2)],
        ]
        self.GOT_V = [
            [(0, 0), (1, 1), (0, 2)],
            [(0, 0), (1, 1), (2, 0)],
            [(2, 0), (1, 1), (2, 2)],
            [(0, 2), (1, 1), (2, 2)]
        ]
        self.APPR_X = [
            [(0, 0), (0, 2), (1, 1), (2, 0), (2, 2)]
        ]
        self.timeLimit = datetime.timedelta(seconds=tle)
        self.begin = 0
        self.WIN_UTILITY = 10000000000000
        self.cell_win = 2000

    def minimax(self, old_move, depth, max_depth, alpha, beta, isMax, p_board, flag1, flag2, best_node):
        if datetime.datetime.utcnow() - self.begin > self.timeLimit:
            return (-111, (-1, -1))

        terminal_state = p_board.find_terminal_state()
        if terminal_state[1] == 'WON':
            # print "terminal_state",terminal_state
            if terminal_state[0] == flag1:
				return (self.WIN_UTILITY,old_move)
            if terminal_state[0] == flag2:
                return (-self.WIN_UTILITY,old_move)


        if depth == max_depth:
            utility = self.check_utility(p_board)
            return (utility if flag1 == 'x' else -utility, old_move)

        else:
            children_list = p_board.find_valid_move_cells(old_move)
            random.shuffle(children_list)

            if len(children_list) == 0:
                utility = self.check_utility(p_board)
                return (utility if flag1 == 'x' else -utility, old_move)

            for child in children_list:
                (_, bonus) = p_board.update(
                    old_move, child, flag1 if isMax else flag2)

                if isMax:
                    score = self.minimax(
                        child, depth+1, max_depth, alpha, beta, True if bonus else False, p_board, flag1, flag2, best_node)

                    if datetime.datetime.utcnow() - self.begin > self.timeLimit:
                        p_board.big_boards_status[child[0]
                                                  ][child[1]][child[2]] = '-'
                        p_board.small_boards_status[child[0]
                                                    ][child[1]/3][child[2]/3] = '-'
                        return (-111, (-1, -1))

                    if (score[0] > alpha):
                        alpha = score[0]
                        best_node = child

                else:
                    score = self.minimax(
                        child, depth+1, max_depth, alpha, beta, False if bonus else True, p_board, flag1, flag2, best_node)

                    if datetime.datetime.utcnow() - self.begin > self.timeLimit:
                        p_board.big_boards_status[child[0]
                                                  ][child[1]][child[2]] = '-'
                        p_board.small_boards_status[child[0]
                                                    ][child[1]/3][child[2]/3] = '-'
                        return (-111, (-1, -1))

                    if (score[0] < beta):
                        beta = score[0]
                        best_node = child

                p_board.big_boards_status[child[0]][child[1]][child[2]] = '-'
                p_board.small_boards_status[child[0]
                                            ][child[1]/3][child[2]/3] = '-'
                if (alpha >= beta):
                    break

            return (alpha, best_node) if isMax else (beta, best_node)

    def check_utility(self, board):

        ans = 0

        for bb in range(2):                            # number of cell filled  opposition domination mein jayada chalna 
            ans += 100 * \
                self.block_utility(board.small_boards_status[bb], 1, 'x')
            ans -= 100 * \
                self.block_utility(board.small_boards_status[bb], 1, 'o')

            temp_block = []
            for i in range(0, 3):
                for j in range(0, 3):

                    if board.small_boards_status[bb][i][j] == '-':
                        temp_block = [[board.big_boards_status[bb][3*i + k][3*j + l]
                                       for l in range(0, 3)] for k in range(0, 3)]
                        ans += self.block_utility(temp_block, 1, 'x')
                        ans -= self.block_utility(temp_block, 1, 'o')

                    elif board.small_boards_status[bb][i][j] == 'x':
                        ans += self.cell_win

                    elif board.small_boards_status[bb][i][j] == 'o':
                        ans -= self.cell_win

        return ans


    def block_utility(self, block, value, flag):

        # be optimistic
        ans = 0
        op_flag = ['o', 'd'] if flag == 'x' else ['x', 'd']

        # Approaching diagonal win
        for pattern in self.APPR_DIAG:

            op_cnt = 0
            us_cnt = 0

            for pos in pattern:
                if block[pos[0]][pos[1]] in op_flag:
                    op_cnt += 1
                if block[pos[0]][pos[1]] == flag:
                    us_cnt += 1

            if op_cnt == 2 and us_cnt!=0:
                ans -= 500
            if op_cnt == 2 and us_cnt==0:
                ans -= 1000
            if us_cnt == 2 :
                ans += 850

        # Approaching line win
        for pattern in self.APPR_LINE:

            op_cnt = 0
            us_cnt = 0

            for pos in pattern:
                if block[pos[0]][pos[1]] in op_flag:
                    op_cnt += 1
                if block[pos[0]][pos[1]] == flag:
                    us_cnt += 1

            if op_cnt == 2 and us_cnt!=0:
                ans -= 550
            if op_cnt == 2 and us_cnt==0:
                ans -= 1000
            if us_cnt == 2:
                ans += 900

        # Approaching V shape (sure draw state)
        for pattern in self.GOT_V:

            op_cnt = 0
            us_cnt = 0

            for pos in pattern:
                if block[pos[0]][pos[1]] in op_flag:
                    op_cnt += 1
                if block[pos[0]][pos[1]] == flag:
                    us_cnt += 1

            if op_cnt == 3:
                ans -= 700
            if us_cnt == 3:
                ans += 1050

        # Approaching X shape (winning chance better) - 50(opp), 225(u)
        for pattern in self.APPR_X:

            op_cnt = 0
            us_cnt = 0

            for pos in pattern:
                if block[pos[0]][pos[1]] in op_flag:
                    op_cnt += 1
                if block[pos[0]][pos[1]] == flag:
                    us_cnt += 1

            ans -= op_cnt*50
            ans += us_cnt*225

        return ans

    def move(self, board, old_move, flag1):
        self.begin = datetime.datetime.utcnow()

        temp_board = copy.deepcopy(board)
        flag2 = 'o' if flag1 == 'x' else 'x'

        temp_childs = board.find_valid_move_cells(old_move)
        best_node = temp_childs[random.randrange(len(temp_childs))]
        # print temp_childs
        # print "best_node",best_node
        my_val=0

        maxDepth = 3
        while datetime.datetime.utcnow() - self.begin < self.timeLimit:
            (g, g_node) = self.minimax(old_move, 0, maxDepth, self.ALPHA,
                                       self.BETA, True, temp_board, flag1, flag2, best_node)

            if g != -111:
                my_val=g
                best_node = g_node

            maxDepth += 1
        # print my_val
        # print best_node
        return best_node