import random
import copy
import math
import numpy as np
from orient import generatePiecesDict, pieces

PLAYERS = {
    1: 'human',
    2: 'random'   
}

piece_id = {1: "i1", 2: "i2", 3: "i3", 4: "quadruple line", 5: "quintuple line", 6: "z4", 7: "t4", 8: "l4", 9: "square", 10: "w", 11: "p", 12: "f", 13: "t5", 14: "x", 15: "z5", 16: "v5", 17: "u", 18: "v3", 19: "n", 20: "y", 21: "l5"}
piece_possible_orientations = [[0], [0,1], [0,1], [0,1], [0,1], [0,1,4,5], [0,1,2,3], [0,1,2,3,4,5,6,7], [0], [0,1,2,3], [0,1,2,3,4,5,6,7], [0,1,2,3,4,5,6,7], [0,1,2,3], [0], [0,1,4,5], [0,1,2,3], [0,1,2,3], [0,1,2,3], [0,1,2,3,4,5,6,7], [0,1,2,3,4,5,6,7], [0,1,2,3,4,5,6,7]]
pieces = generatePiecesDict(pieces) 

class Board:
    '''
    Board class initialization
    s - The length of the sides of the board in number of blocks
    where 0,0 represents the top left corner

    1 represents player 1's placed pieces
    2 represents player 2's placed pieces
    '''

    def __init__(self, s: int):

        self.running = True
        self.state = "p1_turn"
        self.show_dots = False

        self.dim = s
        self.board = [[0 for i in range(s)] for j in range(s)]
        self.turn = 1
        self.to_play = 1
        self.turn_count = 1
        self.finished = [False, False]

        self.train_examples = []

        # score is the # of tiles placed by each player
        self.score = [0,0] # player 1 and player 2

        # possible squares and corner avalibility (x,y,NE,SE,SW,NW)
        self.possible_squares = [
            [[4, 4, [True, True, True, True]]], #player 1 possible squares
            [[s-5, s-5, [True, True, True, True]]] #player 2 possible squares
        ]

        # available pieces
        self.inv = [
            [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20], #player 1
            [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20] #player 2
        ]

        self.piece_diff_ord = [13, 4, 14, 15, 12, 16, 9, 3, 20, 11,19,5,6,2,7,17]

        # pieces = pieces..
        self.corner_diffs = [[-1,1], [-1,-1], [1,-1], [1,1]]

    def print(self):
        print(self)

    def isPossiblePrinterHelper(self, player, x, y): 
        for turn in self.possible_squares[player]: 
            if turn[0] == x and turn[1] == y:
                return True
        return False

    def __str__(self): 
        s = "   " + " ".join([chr(ord('@')+x+1) for x in list(range(len(self.board)))]) + "\n"
        n=1
        colIdx, rowIdx = 0, 0
        for line in self.board:
            rowNumStr = str(n)
            if len(rowNumStr) == 1:
                rowNumStr = " " + rowNumStr
            s+=rowNumStr + " "
            for col in line:
                if col == 0:
                    if self.show_dots: 
                        if (self.isPossiblePrinterHelper(0, colIdx, rowIdx)) :
                            s+="\033[96m◉ \033[0m"
                        elif self.isPossiblePrinterHelper(1, colIdx, rowIdx): 
                            s+="\033[91m◉ \033[0m"
                        else:  
                            s+="□ "
                    else: 
                        s+="□ "
                elif col == 1:
                    s+="\033[96m▣ \033[0m"
                else:
                    s+="\033[91m▣ \033[0m"
                colIdx+=1
            s+="\n"
            n+=1
            rowIdx+=1
            colIdx=0
        return s

    def getItem(self, coord: tuple[int]):
        #we dont need these checks, eventually theyre prob gonna be removed anyways for that optimization # Always good to have checks!!!! # never know when it'll help with our errors
        if len(coord) != 2:
            raise IndexError
        if coord[0] < 0 or coord[0] >= len(
                self.board) or coord[1] < 0 or coord[1] >= len(self.board[0]):
            raise IndexError
        return self.board[coord[0]][coord[1]]

    def __getitem__(self, coord: tuple[int]):
        return self.getItem(coord)

    def getCorners(self, x, y):
        corners = []
        corners.append([x+1, y-1])
        corners.append([x+1, y+1])
        corners.append([x-1, y+1])
        corners.append([x-1, y-1])
        return corners

    def check_possible_squares(self):
        new_possible_squares = [[], []]
        for possible_square in self.possible_squares[self.turn-1]:
            if self.is_valid_to_place_here(possible_square[0], possible_square[1]):
                new_possible_squares[self.turn-1].append(possible_square)

        for possible_square in self.possible_squares[2-self.turn]:
            if self.board[possible_square[1]][possible_square[0]] != self.turn:
                new_possible_squares[2-self.turn].append(possible_square)
        return new_possible_squares

    def getEdges(self, x, y):
        edges = []
        edges.append([x+1, y])
        edges.append([x, y+1])
        edges.append([x-1, y])
        edges.append([x, y-1])
        return edges

    def inBounds(self, x, y):
        return x >= 0 and x < len(self.board) and y >= 0 and y < len(self.board[0])

    def getEdgesValues(self, x, y): #JF
        edges_values = []
        if self.inBounds(x+1,y):
            edges_values.append(self.board[y][x+1])
        if self.inBounds(x,y+1):
            edges_values.append(self.board[y+1][x])
        if self.inBounds(x-1,y):
            edges_values.append(self.board[y][x-1])
        if self.inBounds(x,y-1):
            edges_values.append(self.board[y-1][x])
        return edges_values
    #legal moves

    def is_valid_to_place_here(self, x, y): #JF
        valid = True
        if self.inBounds(x,y):
            edges_values = self.getEdgesValues(x, y)
            if self.to_play in edges_values:
                valid = False
            # not already taken by either team
            if self.board[y][x] != 0:
                valid = False
            # not out of bounds
            if x >= self.dim or y >= self.dim or x < 0 or y < 0:
                valid = False
        else:
            return False
        return valid


    # returns a list of all legal moves for current player's turn

    def calculateLegalMoves(self, only_fives_rounds=0): #JF
        # check all corners of the current player
        legal_placements = []
        
        x_y = set()
        for poss_squares_index in range(len(self.possible_squares[self.turn-1])):#[x,y,[NE,SE,SW,NW]] in self.possible_squares[self.turn-1]:
            x,y,[NE,SE,SW,NW] = self.possible_squares[self.turn-1][poss_squares_index]
            x_y.add((x, y))
            
        for piece_num in self.inv[self.turn-1]:
            if (self.turn_count < only_fives_rounds and len(pieces[piece_num][0][0]) == 4) or self.turn_count >= only_fives_rounds:
                for orientation_number in piece_possible_orientations[piece_num]:
                    # print("checking this orientation now:", orientation_number)
                    orientation = pieces[piece_num][orientation_number] # should contain [[blocks from center], [ne], [se], etc]          
                    for x, y in x_y:
                        if self.board[y][x] == 0:
                            if self.turn not in self.getEdgesValues(x,y):
                                centers = set()
                                for dir in range(4):
                                    for pieceBlock in orientation[dir + 1]:
                                        center = (x + (-1*pieceBlock[0]), y + (-1*pieceBlock[1]))
                                        if not self.is_valid_to_place_here(center[0], center[1]):
                                            break
                                        centers.add(center)
                                for center in centers:
                                    for block in orientation[0]:
                                        x_prime = block[0]+center[0]
                                        y_prime = block[1]+center[1]                                            
                                        if not self.is_valid_to_place_here(x_prime, y_prime):
                                            break
                                    else:
                                        legal_placements.append([center[0], center[1], piece_num, orientation_number])
        return legal_placements


    def calculateLegalMovesEarly(self, number_of_pieces, only_fives_rounds=0): #JF
        # check all corners of the current player
        piece_diff_ord = self.piece_diff_ord[:number_of_pieces]
        piece_diff_ord = list(set(piece_diff_ord) & set(self.inv[self.turn-1]))
        legal_placements = []
        for poss_squares_index in range(len(self.possible_squares[self.turn-1])):#[x,y,[NE,SE,SW,NW]] in self.possible_squares[self.turn-1]:
            x,y,[NE,SE,SW,NW] = self.possible_squares[self.turn-1][poss_squares_index]
            if self.board[y][x] == 0:
                if self.turn not in self.getEdgesValues(x,y):
                    # print('edges check out: none of them are same team')
                    for piece_num in piece_diff_ord:
                        if (self.turn_count < only_fives_rounds and len(pieces[piece_num][0][0]) == 4) or self.turn_count >= only_fives_rounds:
                            for orientation_number in piece_possible_orientations[piece_num]:
                                # print("checking this orientation now:", orientation_number)
                                orientation = pieces[piece_num][orientation_number] # should contain [[blocks from center], [ne], [se], etc]
                                valid_move = False
                                for dir in range(4):
                                    for pieceBlock in orientation[dir + 1]:
                                        center = [ x + (-1*pieceBlock[0]), y + (-1*pieceBlock[1]) ]
                                        if not self.is_valid_to_place_here(center[0], center[1]):
                                            break

                                        for block in orientation[0]:
                                            x_prime = block[0]+center[0]
                                            y_prime = block[1]+center[1]                                            
                                            if not self.is_valid_to_place_here(x_prime, y_prime):
                                                break
                                        else:
                                            valid_move = True
                                            legal_placements.append([center[0], center[1], piece_num, orientation_number, poss_squares_index])
                                            break
                                    if valid_move:
                                        break
                                            
        return legal_placements

    def place_piece(self, move): #JF
        # print(move)
        x, y, piece_num, orientation_number = move

        #update score
        self.score[self.turn-1] += 1 + len(pieces[piece_num][orientation_number][0])

        #change board by putting down the peice
        self.board[y][x] = self.to_play
        for block in pieces[piece_num][orientation_number][0]:
            self.board[y+block[1]][x+block[0]] = self.to_play

        # update the possible squares
        #check the existing possible squares in case they are no longer placeable
        self.possible_squares = self.check_possible_squares()
        # add in the new avalible possible squares
        NE,SE,SW,NW = pieces[piece_num][orientation_number][1:]
        for dir in range(4):
            for corner in [NE,SE,SW,NW][dir]:
                possible_dot_x = x + (-1*self.corner_diffs[dir][0]) + corner[0]
                possible_dot_y = y + (-1*self.corner_diffs[dir][1]) + corner[1]
                if self.is_valid_to_place_here(possible_dot_x, possible_dot_y):
                    possible_corners = []
                    for possible_corner_dir in self.corner_diffs:
                        if self.is_valid_to_place_here(possible_dot_x+possible_corner_dir[0]*-1, possible_dot_y+possible_corner_dir[1]*-1):
                            possible_corners.append(True)
                        else:
                            possible_corners.append(False)
                    self.possible_squares[self.turn-1].append([possible_dot_x, possible_dot_y, possible_corners])

        # remove the piece from inventory
        self.inv[self.turn-1].remove(piece_num)    



    def randomTurn(self, not_to_use, not_to_use2): #JF
        all_moves = self.calculateLegalMoves(only_fives_rounds=3)

        if len(all_moves) > 0:
            move = random.choice(all_moves)
            self.place_piece(move)
        else:
            self.finished[self.turn-1] = True

        self.switchPlayer()

    def displayStateOfGame(self): #JF
        print(self.turn, 'turn', self.to_play, 'to play')
        print(self.score, " Player 1 and Player 2 scores")
        print(self.inv, " Player 1 and Player 2 inventories")

    def switchPlayer(self): #JF
        self.turn_count += 1
        self.to_play *= -1
        self.turn = 3 - self.turn
        if self.state == 'p1_turn':
            self.state = 'p2_turn'
        else:
            self.state = 'p1_turn'

    def checkWin(self, tempBoard): #JF
        if tempBoard.finished[2-tempBoard.turn-1] and tempBoard.score[2-tempBoard.turn] < tempBoard.score[tempBoard.turn-1]:
            return True
        return False

    def is_win(self, board, player): #JF
        if player == -1:
            spot = 1
        if player == 1:
            spot = 0
        if board.finished[spot-1] and board.score[spot] > board.score[spot-1]:
            return True
        return False


    def calculateBoardScore_dots(self, board, weights): #JF
        # w1, w2, w3, w4, w5, w6, w7, w8, w9, w10 = weights
        score = 0
        starting_pos = [[4,4], [9,9]]
        w1, w2, w3, w4, w5, w6, w7, w8, w9, x, y, z = weights

        if board.turn_count >= 35:
            score += w7 * (board.score[self.turn-1] - board.score[2-board.turn])

        else:
            for opp_dot in board.possible_squares[2 - self.turn]:
                score -= w1 + (w2- math.log(0.001 * board.turn_count)) * (20 - ( math.sqrt( (opp_dot[0] - starting_pos[board.turn-1][0])**2 + (opp_dot[1] - starting_pos[board.turn-1][0])**2 ) ) )
                score -= w3 * sum(opp_dot[2])
            for my_dot in board.possible_squares[self.turn-1]:
                score += w4 + (w5- math.log(0.001 * board.turn_count)) * (20 - ( math.sqrt( (my_dot[0] - starting_pos[2-board.turn][0])**2 + (my_dot[1] - starting_pos[2-board.turn][1])**2 ) ) )
                score += w6 * sum(my_dot[2])

            score += w7 * board.score[self.turn-1]
            score -= w8 * board.score[2-board.turn]
            # add in score += w9 * (total_inv_score - current_inv_score)

        return score

    def calculateBoardScore_squares(self, board): #JF
        score = 0
        w1 = 1
        w2 = 1
        w3 =  0
        score += w1 * board.score[self.turn-1]
        score -= w2 * board.score[2-self.turn]
        return score 


    def lookahead(self, board, depth, weights): #JF
        if depth == 0:
            return board.calculateBoardScore_dots(board, weights)
        else:
            board.switchPlayer()
            move_list = board.calculateLegalMoves(only_fives_rounds=6)
            best_val = -9999
            for my_move in move_list:
                tempBoard = copy.deepcopy(board)
                tempBoard.place_piece(my_move)
                if board.checkWin(tempBoard):
                    return (-10000)
                val = tempBoard.lookahead(tempBoard,depth-1, weights)
                if val > best_val:
                    best_val = val
            return (-1*best_val)

    def minimax(self, board, depth, isMaximizingPlayer, alpha, beta, weights):
        if depth == 0:
            return board.calculateBoardScore_dots(board, weights)
        else:
            board.switchPlayer()


        if isMaximizingPlayer:
            move_list = board.calculateLegalMoves(only_fives_rounds=weights[9])
            best_val = -9999
            for my_move in move_list:
                tempBoard = copy.deepcopy(board)
                tempBoard.place_piece(my_move)
                value = board.minimax(tempBoard, depth-1, False, alpha, beta, weights)
                best_val = max( best_val, value) 
                alpha = max( alpha, best_val)
                if beta <= alpha:
                    break
            return best_val

        elif not isMaximizingPlayer:
            move_list = board.calculateLegalMoves(only_fives_rounds=weights[9])
            best_val = 9999
            for my_move in move_list:
                tempBoard = copy.deepcopy(board)
                tempBoard.place_piece(my_move)
                value = board.minimax(tempBoard, depth-1, True, alpha, beta, weights)
                best_val = min( best_val, value) 
                beta = min( beta, best_val)
                if beta <= alpha:
                    break
            return best_val

    def smartTurn(self, level, weights): #JF
        move_list = self.calculateLegalMoves(only_fives_rounds=weights[9])
        random.shuffle(move_list)
        best_val = -10001
        best_move = []
        for my_move in move_list:
            tempBoard = copy.deepcopy(self)
            tempBoard.place_piece(my_move)
            if tempBoard.checkWin(tempBoard):
                return (my_move)

            val = self.minimax(tempBoard, level, False, 999999, -999999, weights)

            if val > best_val:
                best_val = val
                best_move = copy.copy(my_move)
        return best_move

    def max_value(self, board, level, alpha, beta, weights):
        """
        Returns the maximum value for the current player on the board 
        using alpha-beta pruning.
        """

        if level == 0:
            return board.calculateBoardScore_dots(board, weights)

        val = -math.inf
        for move in board.calculateLegalMoves(only_fives_rounds=weights[9]):
            val = max(val, board.min_value(board.result(board, move), level-1, alpha, beta, weights))
            alpha = max(alpha, val)
            if alpha >= beta:
                break

        return val

    def min_value(self, board, level, alpha, beta, weights):
        """
        Returns the maximum value for the current player on the board 
        using alpha-beta pruning.
        """
        if level == 0:
            return board.calculateBoardScore_dots(board, weights)

        val = math.inf
        for move in board.calculateLegalMoves(only_fives_rounds=weights[9]):
            val = min(val, board.max_value(board.result(board, move), level-1, alpha, beta, weights))
            beta = min(alpha, val) 
            if alpha >= beta:
                break

        return val

    def result(self, board, move):
        if move not in board.calculateLegalMoves():
            print("How did this move get here???")
            raise Exception("Invalid Action")

        tempBoard = copy.deepcopy(board)
        tempBoard.place_piece(move)
        tempBoard.switchPlayer()

        return tempBoard

    def minimax_v2(self, board, level, isMaximizingPlayer, weights):
        # print(level, level==0)
        if level == 0:
            return 

        # will only look at the hard to place 5 peices as options for the first 2 turns
        # if board.turn_count <= weights[10]:
        #     moves = board.calculateLegalMovesEarly(weights[11], only_fives_rounds=weights[9])
        # else:
        moves = board.calculateLegalMoves(only_fives_rounds=weights[9])

        print(len(moves), len(moves)**level, ": moves, possibilities")
        i = 1
        if isMaximizingPlayer:
            val = -math.inf
            best_move = []
            for move in moves:
                if i % 100 == 0:
                    print(i)
                new_val = board.min_value(board.result(board, move), level-1, -math.inf, math.inf, weights)
                if new_val > val:
                    val = new_val
                    best_move = move
                i += 1

        elif not isMaximizingPlayer:
            val = math.inf
            best_move = []
            for move in moves:
                if i % 100 == 0:
                    print(i)
                new_val = board.max_value(board.result(board, move), level-1, -math.inf, math.inf, weights)
                if new_val < val:
                    val = new_val
                    best_move = move

                i += 1

        return best_move


    def playSmart_v2(self, level, weights):
        tempBoard = copy.deepcopy(self)
        # print(level)
        if level % 2 == 0:
            move = self.minimax_v2(tempBoard, level, True, weights)
        elif level % 2 == 1:
            move = self.minimax_v2(tempBoard, level, False, weights)
        # print(move)


        if move == []:
            self.finished[self.turn-1] = True
        else:
            self.place_piece(move)

        self.switchPlayer()



    def playSmart(self, level, weights): #JF
        best_move = self.smartTurn(0, weights)
        if best_move == []:
            self.finished[self.turn-1] = True
        else:
            self.place_piece(best_move)

        self.switchPlayer()

    # UI, etc. for a human to be able to play a piece
    def humanTurn(self): #JF
        legal_move = False
        while not legal_move:
            choice = int(input(f"Player {self.turn}'s turn. Choose a piece to place: "))

            if choice == 'exit' or choice == 'quit':
                self.running = False
                return

            x = int(input(f"Player {self.turn}'s turn. Choose the x coordinate of the piece: "))
            y = int(input(f"Player {self.turn}'s turn. Choose the y coordinate of the piece: "))
            orientaion = int(input(f"Player {self.turn}'s turn. Choose the orientation of the piece: "))
            legal_move = self.is_valid_to_place_here(x,y)
            move = [x, y, choice, orientaion, 0, 0]
            # if legal_move:
            #     legal_move = self.is_legal_move(x, y, choice, orientaion)
            # if legal_move:
            #     break
            # print("NOOOOOOOOOOOOOOOOOO try again")

        self.place_piece(move)
        print(self.inv[self.turn-1])
        print(self.score)
        # self.switchPlayer()


        def squareDiff(self): 
            return self.score[0]-self.score[1]

        # def is_legal_move(self, x, y, choice, orientation):
        #     valid = True
        #     for block in pieces[choice][orientation][0]:
        #         x_prime = block[0]+x
        #         y_prime = block[1]+y
        #         # checks out of bounds, and not occupied by either player
        #         if not self.is_valid_to_place_here(x_prime, y_prime):
        #             valid = False

        #     # also need to check one of the corners is touching
        #     for block in pieces[choice][orientation][0]:
        #         xx = block[0] + x
        #         yy = block[1] + y
        #         # if xx-1 >= 0 and self.board[yy][xx-1] is not self.turn or xx + 1 < self.dim and self.board[yy][xx+1] is not self.turn or yy-1 >= 0 and self.board[yy-1][xx] is not self.turn or yy + 1 < self.dim and self.board[yy+1][xx] is not self.turn:
        #         #     valid = False

        #     return valid

    # def monte_carlo_turn(self, weights, num_sims=5):
    #     root = self.monte_carlo_search(self, self.to_play, weights, num_sims)
    #     most_visited = None
    #     most_visits = -1
    #     root.info()
    #     for child in root.children.values():
    #         if child.visit_count > most_visits:
    #             most_visits = child.visit_count
    #             most_visited = child

    #     print('most visited')
    #     most_visited.info()

    #     if most_visited == None:
    #         self.finished[self.turn-1] = True
    #     else:
    #         self.board = most_visited.state.board

        # self.switchPlayer()

    def rand_monte_carlo_turn(self, weights, current_player, num_sims=50, rand_select=True):
        return self.monte_carlo_turn(weights, current_player, num_sims=num_sims, rand_select=rand_select)


    def monte_carlo_turn(self, weights, player, num_sims=50, rand_select=False):
        current_player = 1
        canonical_board = copy.deepcopy(self)
        canonical_board.board = self.get_flipped_board(self, current_player)

        num_moves = len(canonical_board.calculateLegalMoves())

        if num_moves == 0:
            print("DONE : num_moves == 0")
            self.finished[2-self.turn] = True
            reward = self.get_reward_for_player(self, player)
            print(reward, 'reward!')
            ret = []
            for hist_state, hist_current_player, hist_action_probs, hist_moves in self.train_examples:
                # [Board, currentPlayer, actionProbabilities, Reward]
                ret.append( [hist_state, hist_moves, list(hist_action_probs), reward * ((-1) ** (hist_current_player != current_player))] )
            return ret
        else:
            root = self.monte_carlo_search(canonical_board, current_player, weights, player, num_sims)

            action_probs = []
            moves = []
            for move, node in root.children:
                action_probs.append(node.visit_count)
                moves.append(move)

            action_probs = action_probs / np.sum(action_probs)
            self.train_examples.append([canonical_board.board, current_player, action_probs, moves])

            action = root.choose_move(rand_select=rand_select)
            print(action, "this is the root's selected action") 

            self.place_piece(action)

            self.turn_count += 1
            self.to_play *= -1
            self.turn = 3 - self.turn
            if self.state == 'p1_turn':
                self.state = 'p2_turn'
            else:
                self.state = 'p1_turn'




    def get_reward_for_player(self, board, player):
        # return None if not ended, 1 if player 1 wins, -1 if player 1 lost
        print(player, 'end of player')
        if board.score[player-1] < board.score[2-player]:
            print('THIS IS A LOSING MOVE')
            return -1
        elif board.score[player-1] > board.score[2-player]:
            print('THIS IS A WINNING MOVE')
            return 1
        else:
            return 0


    def monte_carlo_search(self, state, to_play, weights, player, num_sims):   #https://github.com/JoshVarty/AlphaZeroSimple/blob/master/monte_carlo_tree_search.py
        root = Node(0, to_play)

        poss_moves = state.calculateLegalMoves()
        # num_sims = len(poss_moves)*2
        # use a model.predict to get the action probabilities #will have to mask out illegal moves as well
        move_probs = [1/len(poss_moves) for i in range(len(poss_moves))] # for now will set all of the probs to be equal
        root.expand(copy.deepcopy(state), to_play, move_probs, poss_moves) #will set all the weights to 1/len(poss_moves) until the model actually gets good
        print(num_sims, 'num sims')
        for i in range(num_sims):
            # if i % 1 == 0:
            #     print(i, ' the itteration of simulations') # lag occurs between here and score / value calculations
            node = root
            search_path = [root]
            j = 1
            while node.expanded():
                j +=1
                move, node = node.select_best_child()
                search_path.append(node)

            # print(j, 'num loops of expanded')    

            parent = search_path[-2]
            next_state = parent.state.get_next_state(parent.state, move, parent)
            value = next_state.move_reward(next_state, weights, player)
            if value == 1:
                i = num_sims

            if value != 0:
                # if the game has not ended
                # expand!!

                # #eventually will want to use a model to predict the next state's 
                # probability to choose each of the next actions. Will have to make sure to 
                # get rid of any illegal moves still predicted by the model
                poss_moves = next_state.calculateLegalMoves()
                move_probs = [1/len(poss_moves) for i in range(len(poss_moves))]
                node.expand(next_state, parent.to_play *-1, move_probs, poss_moves)

            self.monte_back_prop(search_path, value, parent.to_play*-1)


        return root


    def move_reward(self, board, weights, player_num):
        # this function is extremely messy and improper,  pls ignore but is there is a better way lmk. There def is a better way
        if player_num == 1:
            player = 1
            if len(board.calculateLegalMoves()) != 0:
                score = -board.calculate_board_score_mcts(board, weights)
                # print(score, 'the score of the possible move')
                return score # must be between (1, -1)    
            else:
                # print(board.score, player, 'score and turn 1 -- ', board.to_play, 'to play')
                if board.score[player-1] < board.score[2-player]:
                    # print('loss move', (-1 - abs(board.score[2-player] - board.score[player-1])))
                    return -1 - abs(board.score[2-player] - board.score[player-1])
                elif board.score[player-1] > board.score[2-player]:
                    # print('win move', (1 + abs(board.score[2-player] - board.score[player-1])))
                    return 1 + abs(board.score[2-player] - board.score[player-1])
                elif board.score[0] == board.score[1]:
                    # print('tie move')
                    return 0
                else:
                    print('HUUUUHHH')
        if player_num == 2:
            player = 2
            if len(board.calculateLegalMoves()) != 0:
                score = -board.calculate_board_score_mcts(board, weights)
                # print(score, 'the score of the possible move')
                return score # must be between (1, -1)
            else:
                # print(board.score, player, 'score and turn 2')
                if board.score[player-1] < board.score[2-player]:
                    # print('loss move', (-1 - abs(board.score[2-player] - board.score[player-1])))
                    return (-1 - abs(board.score[2-player] - board.score[player-1]))
                elif board.score[player-1] > board.score[2-player]:
                    # print('win move', (1 + abs(board.score[2-player] - board.score[player-1])))
                    return (1 + abs(board.score[2-player] - board.score[player-1]))
                elif board.score[0] == board.score[1]:
                    # print('tie move')
                    return 0
                else:
                    print('HUUUUHHH')

    def monte_back_prop(self, search_path, value, to_play):
        # NEED TO MAKE VALUE BETWEEN 0-1
        for node in reversed(search_path):
            node.visit_count += 1
            if node.to_play == to_play:
                node.value_sum += value 
            else:
                node.value_sum -= value 
        return


    def get_flipped_board(self, board, player): # i lie
        return [[j*player for j in i] for i in board.board]


    def get_next_state(self, board1, move, node):   
        board = copy.deepcopy(board1)
        board.place_piece(move)

        board.turn_count += 1
        board.to_play *= -1
        board.turn = 3 - board.turn
        if board.state == 'p1_turn':
            board.state = 'p2_turn'
        else:
            board.state = 'p1_turn'

        return board


    def calculate_board_score_mcts(self, board, weights): #JF
        # w1, w2, w3, w4, w5, w6, w7, w8, w9, w10 = weights
        score = 0
        starting_pos = [[4,4], [9,9]]
        w1, w2, w3, w4, w5, w6, w7, w8, w9, x, y, z = weights

        if board.turn_count > 4:
            score += w7 * (board.score[board.turn-1] - board.score[2-board.turn])
            best_possible_score = 30 * w7
            score = score/best_possible_score
            
        else:
            for opp_dot in board.possible_squares[2 - board.turn]:
                score -= w1 + (w2- math.log(0.001 * board.turn_count)) * (20 - ( math.sqrt( (opp_dot[0] - starting_pos[board.turn-1][0])**2 + (opp_dot[1] - starting_pos[board.turn-1][0])**2 ) ) )
                score -= w3 * sum(opp_dot[2])
            for my_dot in board.possible_squares[board.turn-1]:
                score += w4 + (w5- math.log(0.001 * board.turn_count)) * (20 - ( math.sqrt( (my_dot[0] - starting_pos[2-board.turn][0])**2 + (my_dot[1] - starting_pos[2-board.turn][1])**2 ) ) )
                score += w6 * sum(my_dot[2])

            score += w7 * board.score[board.turn-1]
            score -= w8 * board.score[2-board.turn]
            # add in score += w9 * (total_inv_score - current_inv_score)


            best_possible_score = 0
            worst_possible_score = 0
            worst_possible_score -= w1 + (w2- math.log(0.001 * 40)) * (20)
            worst_possible_score -= w3 * 4
            worst_possible_score *=  30#len(board.possible_squares[board.turn-1]) # 30   # could be # of actual dots not the guessed 'max' for the # of opp_dots
            best_possible_score += w4 + (w5- math.log(0.001 * 40)) * (20)
            best_possible_score += w6 * 4
            best_possible_score *=  30#len(board.possible_squares[2 - board.turn]) # 30   # could be # of actual dots not the guessed 'max' for the # of opp_dots
            worst_possible_score -= 75 * w8
            best_possible_score += 75 * w7
    
            if score > 0:
                score = score/best_possible_score
            elif score < 0:
                score = score/abs(worst_possible_score)
            # print(score, 'score make sure between 0-1')
            if abs(score) >= 1:
                print('ERROR SCORE TOO HIGH, is more than 1,-1')
        return score


class Node:
    def __init__(self, prior, to_play):
        self.prior = prior
        self.to_play = to_play

        self.children = [] # moves maps to the next node
        self.visit_count = 0
        self.value_sum = 0
        self.state = None

    def value(self):
        if self.visit_count == 0:
            return 0
        return self.value_sum / self.visit_count

    def expanded(self):
        return 0 < len(self.children)

    def expand(self, state, to_play, move_probabilities, moves):
        self.to_play = to_play
        self.state = state
        for a, prob in enumerate(move_probabilities):
            if prob != 0:
                self.children.append([moves[a], Node(prior=prob, to_play=self.to_play * -1)])

        random.shuffle(self.children)

    def select_best_child(self):
        #get the child with the best ucb score
        best_child = None 
        best_move =  -1
        best_ucb = -math.inf
        # children_shuffled = list(self.children.items())
        # random.shuffle(children_shuffled)
        # newlist = [i**2 for i in range(1, 100) if i%2==0]
        for move, child in self.children:
            ucb_score = self.ucb_score(self, child)
            if ucb_score > best_ucb:
                best_ucb = ucb_score
                best_child = child
                best_move = move

        return best_move, best_child


    def ucb_score(self, parent, child):
        prior_score = child.prior * math.sqrt(np.log(parent.visit_count+1) / (child.visit_count + 1))
        if child.visit_count > 0:
            value_score = child.value() # might be negative, check later
        else:
            value_score = 0

        return value_score + prior_score


    def choose_move(self, rand_select=False):
        if rand_select:
            return random.choice(self.children)[0]

        best_move = -1
        most_visits = -math.inf

        for move, child in self.children:
            if most_visits < child.visit_count:
                best_move = move
                most_visits = child.visit_count

        return best_move

    def info(self):
        prior = "{0:.2f}".format(self.prior)
        print("{} Prior: {} Count: {} Value: {}".format(self.state.__str__(), prior, self.visit_count, self.value()))
        print('children ', dict(list(self.children)[0: 5]))