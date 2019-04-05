import random
import datetime
import copy

class PlayerOld:

	def __init__(self):
		self.two_value = 10
		self.three_value = 100
		self.four_value = 500
		self.ALPHA = -100000000
		self.BETA = 100000000
		self.dict = {}
		self.lenght = 0
		self.FIRST_POS = [
			[(0,0),(1,1),(0,2)],
			[(0,0),(1,1),(2,0)],
			[(0,2),(1,1),(2,2)],
			[(2,0),(1,1),(2,2)]
		]
		self.timeLimit = datetime.timedelta(seconds = 14.9)
		self.begin = 0
		self.WIN_UTILITY = 1000000
		self.cell_win = 1000


	def minimax(self, old_move, depth, max_depth, alpha, beta, isMax, p_board, p_block, flag1, flag2, best_node):
		if datetime.datetime.utcnow() - self.begin > self.timeLimit:
			return (-111, (-1, -1))
		
		terminal_state = p_board.find_terminal_state()
		if terminal_state[1] == 'WON':
			if terminal_state[0] == flag1 :
				return (self.WIN_UTILITY, old_move)
			if terminal_state[0] == flag2 :
				return (-self.WIN_UTILITY, old_move)

		if depth == max_depth:
			utility = self.check_utility(p_block, p_board)
			if flag1 == 'o':
				return (-utility, old_move)
			return (utility, old_move)
		
		else:
			children_list = p_board.find_valid_move_cells(old_move)
			random.shuffle(children_list)

			if len(children_list) == 0:
				utility = self.check_utility(p_block, p_board)
				if flag1 == 'o':
					return (-utility, old_move)
				return (utility, old_move)
			
			for child in children_list:
                		if isMax:
					(message, bonus) = p_board.update(old_move, child, flag1)
				else:
					(message, bonus) = p_board.update(old_move, child, flag2)
				
				if isMax:

                    			if bonus:
                        			score = self.minimax (child, depth+1, max_depth, alpha, beta, True, p_board, p_block, flag1, flag2, best_node)
                    			else:
						score = self.minimax (child, depth+1, max_depth, alpha, beta, False, p_board, p_block, flag1, flag2, best_node)
					
					if datetime.datetime.utcnow() - self.begin > self.timeLimit:
						p_board.big_boards_status[child[0]][child[1]][child[2]] = '-'
						p_board.small_boards_status[child[0]][child[1]/3][child[2]/3] = '-'
						return (-111, (-1, -1))
					
					if (score[0] > alpha):
						alpha = score[0]
						best_node = child
				
				else:	
                    			if bonus:
                        			score = self.minimax (child, depth+1, max_depth, alpha, beta, False, p_board, p_block, flag1, flag2, best_node)
                    			else:
						score = self.minimax (child, depth+1, max_depth, alpha, beta, True, p_board, p_block, flag1, flag2, best_node)
					

					if datetime.datetime.utcnow() - self.begin > self.timeLimit:
						p_board.big_boards_status[child[0]][child[1]][child[2]] = '-'
						p_board.small_boards_status[child[0]][child[1]/3][child[2]/3] = '-'
						return (-111, (-1, -1))
					
					if (score[0] < beta):
						beta = score[0]
						best_node = child
				
				p_board.big_boards_status[child[0]][child[1]][child[2]] = '-'
				p_board.small_boards_status[child[0]][child[1]/3][child[2]/3] = '-'
				if (alpha >= beta):
					break
			
			if isMax:
				return (alpha, best_node)
			else:
				return (beta, best_node)

	def check_utility(self, block, board):
		ans = 0

		for bb in range(2):
			ans += 100*self.block_utility(board.small_boards_status[bb], 1, 'x')
			ans -= 100*self.block_utility(board.small_boards_status[bb], 1, 'o')
			
			temp_block = []
			for i in range(0, 3):
				for j in range(0, 3):

					if board.small_boards_status[bb][i][j] == '-':
						temp_block = [[board.big_boards_status[bb][3*i + k][3*j + l] for l in range(0, 3)] for k in range(0, 3)]
						ans += self.block_utility(temp_block, 1, 'x')
						ans -= self.block_utility(temp_block, 1, 'o')
					
					elif board.small_boards_status[bb][i][j] == 'x':
						ans += self.cell_win
					
					elif board.small_boards_status[bb][i][j] == 'o':
						ans -= self.cell_win
		
		return ans

	def move(self, board, old_move, flag1) :
		self.timeLimit = datetime.timedelta(seconds = 5)
		
		self.begin = 0
		self.begin = datetime.datetime.utcnow()
		
		temp_board = copy.deepcopy(board)
		if flag1 == 'x':
			flag2 = 'o'
		else:
			flag2 = 'x'
		
		maxDepth = 3
		while datetime.datetime.utcnow() - self.begin < self.timeLimit:
			(g, g_node) = self.minimax(old_move, 0, maxDepth, self.ALPHA, self.BETA, True, temp_board, (1, 1), flag1, flag2, (5, 5))

			if g != -111:
				best_node = g_node
			maxDepth += 1
            
            		# if maxDepth == 10:
                	# 	break
		
		return best_node

	def block_utility(self, block, value, flag):
            for pattern in self.FIRST_POS:
                match=True
                ans = 0
                for pos in pattern:
                    if block[pos[0]][pos[1]]!=flag:
                        match=False
                        break
                if match:
                    ans+= 1000
                return ans 
            # for pattern in self.SECOND_POS:
            #     bool match=True
            #     for pos in pattern:
            #         if block_1[pos[0]][pos[1]]!=flag:
            #             match=False
            #             break
            #     if match:
            #         ans+= 1000
			# print ans


            for row in range(3):
                myflag=0
                opflag=0
                ans = 0
                for col in range(3):
                    if block[row][col] == flag:
                        myflag+=1
                    else:
                        opflag+=1
                
                if block[1][1]== flag:
                    if myflag==1:
                        ans+=200
                    elif myflag==2:
                        ans+=600
                    elif myflag==3:
                        ans+=750
                else:
                    if myflag==1:
                        ans+=50
                    elif myflag==2:
                        ans+=400
                return ans


