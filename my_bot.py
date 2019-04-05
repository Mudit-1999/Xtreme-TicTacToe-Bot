import random
import datetime
import copy


flaged=True

class MyBot():
    def __init__(self,tle):
        self.ALPHA  = -100000000
        self.BETA   = 100000000
        self.dict = {}
        self.heuristic_basic ={
            (0,0):0.523,(0,1):0.509,(0,2):0.493,
            (1,0):0.452,(1,1):0.652,(1,2):0.599,
            (2,0):0.111,(2,1):0.901,(2,2):0.503,
        }
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
        self.WIN_UTILITY = 1000000000000
        self.cell_win = 2000

    def minimax(self, old_move, depth, max_depth, alpha, \
        beta, isMax, copy_board,player1_flag, player2_flag, best_node,prev_bonus):
        if datetime.datetime.utcnow() - self.begin > self.timeLimit:
            return (0, (-1, -1, -1))

        terminal_state = copy_board.find_terminal_state()
        if terminal_state[1] == 'WON':
            print copy_board.print_board()
            if terminal_state[0] == player1_flag:  #Max_wins myplayer wins
				return (self.WIN_UTILITY,old_move)
            else:                                   # Min_wins opposite player wins
                return (-1*self.WIN_UTILITY,old_move)

        if depth == max_depth:
            utility = self.check_utility(copy_board)      # if i were to be x then calulate utility
            if player1_flag == 'x':
                return (utility,old_move)
            else:
                return (-1*utility,old_move)

        else:
            children_list = copy_board.find_valid_move_cells(old_move)
            # random.shuffle(children_list)

            if len(children_list) == 0:              # leaf node
                utility = self.check_utility(copy_board)
                if player1_flag == 'x':
                    return (utility,old_move)
                else:
                    return (-1*utility,old_move)

            for child in children_list:
                (lorem, bonus) = copy_board.update(old_move,\
                     child, player1_flag if isMax else player2_flag)

                if isMax:
                    if bonus == True and prev_bonus == False:
                        (curr_alpha,curr_node) = self.minimax(child, depth+1, max_depth, alpha, \
                            beta, True, copy_board, player1_flag, player2_flag, best_node,True)
                    else:
                        (curr_alpha,curr_node) = self.minimax(child, depth+1, max_depth, alpha, \
                            beta, False, copy_board, player1_flag, player2_flag, best_node,False)

                    if datetime.datetime.utcnow() - self.begin > self.timeLimit:
                        copy_board.big_boards_status[child[0]][child[1]][child[2]] = '-'
                        copy_board.small_boards_status[child[0]][child[1]/3][child[2]/3] = '-'
                        return (0, (-1,-1, -1))

                    if (curr_alpha > alpha and curr_node!=(-1,-1,-1)):
                        alpha = curr_alpha
                        best_node = child

                else:
                    if bonus == True and prev_bonus == False:
                        (curr_beta,curr_node) = self.minimax(child, depth+1, max_depth, alpha, \
                            beta, False, copy_board, player1_flag, player2_flag, best_node,True)
                    else:
                        (curr_beta,curr_node) = self.minimax(child, depth+1, max_depth, alpha, \
                            beta, True, copy_board, player1_flag, player2_flag, best_node,False)

                    if datetime.datetime.utcnow() - self.begin > self.timeLimit:
                        copy_board.big_boards_status[child[0]][child[1]][child[2]] = '-'
                        copy_board.small_boards_status[child[0]][child[1]/3][child[2]/3] = '-'
                        return (0, (-1,-1,-1))

                    if (curr_beta < beta and curr_node!= (-1,-1,-1)):
                        beta = curr_beta
                        best_node = child

                copy_board.big_boards_status[child[0]][child[1]][child[2]] = '-'
                copy_board.small_boards_status[child[0]][child[1]/3][child[2]/3] = '-'
                if (alpha >= beta):
                    break
            print ("Alpha",alpha, best_node) if isMax else ("Beta",beta, best_node)
            return (alpha, best_node) if isMax else (beta, best_node)

    def check_utility(self, board):
        ans=0
        for bb in range(2):                            # number of cell filled  opposition domination mein jayada chalna 
            ans += 45 * \
                self.block_utility(board.small_boards_status[bb], 1, 'x')
            ans -= 45 * \
                self.block_utility(board.small_boards_status[bb], 1, 'o')
            # print "child"
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
        player2_flag= 'o' if flag == 'x' else 'x'
        # Approaching diagonal win
        for pattern in self.APPR_DIAG:

            op_cnt = 0
            us_cnt = 0

            for pos in pattern:
                if block[pos[0]][pos[1]] in op_flag:
                    ans-= 4*self.heuristic_basic[(pos[0],pos[1])]
                if block[pos[0]][pos[1]] == flag:
                    ans+= 2*self.heuristic_basic[(pos[0],pos[1])]

        # Approaching line win
        for pattern in self.APPR_LINE:

            op_cnt = 0
            us_cnt = 0

            for pos in pattern:
                if block[pos[0]][pos[1]] in op_flag:
                    ans-= 4*self.heuristic_basic[(pos[0],pos[1])]
                if block[pos[0]][pos[1]] == flag:
                    ans+= 2*self.heuristic_basic[(pos[0],pos[1])]


        # Approaching V shape (sure draw state)
        for pattern in self.GOT_V:

            op_cnt = 0
            us_cnt = 0

            for pos in pattern:
                if block[pos[0]][pos[1]] in op_flag:
                    ans-= 2*self.heuristic_basic[(pos[0],pos[1])]
                if block[pos[0]][pos[1]] == flag:
                    ans+= 1*self.heuristic_basic[(pos[0],pos[1])]

        # Approaching X shape (winning chance better) - 50(opp), 225(u)
        for pattern in self.APPR_X:

            op_cnt = 0
            us_cnt = 0

            for pos in pattern:
                if block[pos[0]][pos[1]] in op_flag:
                    ans-= 4*self.heuristic_basic[(pos[0],pos[1])]
                if block[pos[0]][pos[1]] == flag:
                    ans+= 2*self.heuristic_basic[(pos[0],pos[1])]
        

        # Penalty for opponent  
        # Approaching line win
        for pattern in self.APPR_LINE:

            op_cnt = 0
            us_cnt = 0

            for pos in pattern:
                if block[pos[0]][pos[1]] in op_flag[0]:
                    op_cnt+=1
                if block[pos[0]][pos[1]] == flag or block[pos[0]][pos[1]]=='d':
                    us_cnt+=1
            if us_cnt==0 and op_cnt==2:
                # print "hi"
                ans=-1000
        return ans


    def move(self, game_board, old_move, player1_flag):    # player1_flag  === myplayer_flag
        self.begin = datetime.datetime.utcnow()
        copy_board = copy.deepcopy(game_board) # copy of game_board
        player2_flag = 'o' if player1_flag == 'x' else 'x'
        
        
        
        childern = game_board.find_valid_move_cells(old_move)
        if (0,4,4) in childern and old_move == (-1,-1,-1):
            return (0,4,4)
        best_node=childern[random.randrange(len(childern))]
        my_val=0
        max_depth =3
        while datetime.datetime.utcnow() - self.begin < self.timeLimit:
            (node_val, node) = self.minimax(old_move, 0, max_depth, \
                self.ALPHA,self.BETA,True,copy_board, player1_flag, player2_flag, best_node,False)
            
            if node != (-1,-1,-1):
                my_val=node_val
                best_node = node
            max_depth += 1
        
        print my_val," ", max_depth
        return best_node
