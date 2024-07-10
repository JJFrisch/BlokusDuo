import random
import copy
import math


# random.seed(32)

PLAYERS = {
    1: 'human',
    2: 'random'   
}

piece_id = {1: "i1", 2: "i2", 3: "i3", 4: "quadruple line", 5: "quintuple line", 6: "z4", 7: "t4", 8: "l4", 9: "square", 10: "w", 11: "p", 12: "f", 13: "t5", 14: "x", 15: "z5", 16: "v5", 17: "u", 18: "v3", 19: "n", 20: "y", 21: "l5"}
piece_possible_orientations = [[0], [0,1], [0,1], [0,1], [0,1], [0,1,4,5], [0,1,2,3], [0,1,2,3,4,5,6,7], [0], [0,1,2,3], [0,1,2,3,4,5,6,7], [0,1,2,3,4,5,6,7], [0,1,2,3], [0], [0,1,4,5], [0,1,2,3], [0,1,2,3], [0,1,2,3], [0,1,2,3,4,5,6,7], [0,1,2,3,4,5,6,7], [0,1,2,3,4,5,6,7]]


class Board:
    '''
    Board class initialization
    s - The length of the sides of the board in number of blocks
    where 0,0 represents the top left corner

    1 represents player 1's placed pieces
    2 represents player 2's placed pieces
    '''

    def __init__(self, s: int, pieces):

        self.running = True
        self.state = "p1_turn"
        self.show_dots = False

        self.dim = s
        self.board = [[0 for i in range(s)] for j in range(s)]
        self.turn = 1
        self.turn_count = 1
        self.finished = [False, False]
        
        # score is the # of tiles placed by each player
        self.score = [0,0] # player 1 and player 2

        # possible squares and corner avalibility (x,y,NE,SE,SW,NW)
        self.possible_squares = [
            [[4, 4, [True, True, True, True]]], #player 1 possible squares
            [[s-5, s-5, [True, True, True, True]]] #player 2 possible squares
        ]

        # available pieces
        self.inv = [
            [0,1,2,3,4,5,6,7,9,11,12,13,14,15,16,17,19,20], #player 1
            [0,1,2,3,4,5,6,7,9,11,12,13,14,15,16,17,19,20] #player 2
        ]
        

        self.pieces = pieces
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
            if self.turn in edges_values:
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
        for poss_squares_index in range(len(self.possible_squares[self.turn-1])):#[x,y,[NE,SE,SW,NW]] in self.possible_squares[self.turn-1]:
            x,y,[NE,SE,SW,NW] = self.possible_squares[self.turn-1][poss_squares_index]
            if self.board[y][x] == 0:
                # print(x,y,[NE,SE,SW,NW], "this is one choice")
                if self.turn not in self.getEdgesValues(x,y):
                    # print('edges check out: none of them are same team')
                    for piece_num in self.inv[self.turn-1]:
                        if (self.turn_count < only_fives_rounds and len(self.pieces[piece_num][0][0]) == 4) or self.turn_count >= only_fives_rounds:
                            for orientation_number in piece_possible_orientations[piece_num]:
                                # print("checking this orientation now:", orientation_number)
                                orientation = self.pieces[piece_num][orientation_number] # should contain [[blocks from center], [ne], [se], etc]
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
                                            legal_placements.append([center[0], center[1], piece_num, orientation_number, poss_squares_index, dir])
        return legal_placements
    
        
    def place_piece(self, move): #JF
        # print(move)
        x, y, piece_num, orientation_number, poss_squares_i, dir = move

        #update score
        self.score[self.turn-1] += 1 + len(self.pieces[piece_num][orientation_number][0])
        self.possible_squares[self.turn-1].pop(poss_squares_i)

        #change board by putting down the peice
        self.board[y][x] = self.turn
        for block in self.pieces[piece_num][orientation_number][0]:
            self.board[y+block[1]][x+block[0]] = self.turn

        # update the possible squares
        #check the existing possible squares in case they are no longer placeable
        self.possible_squares = self.check_possible_squares()
        # add in the new avalible possible squares
        NE,SE,SW,NW = self.pieces[piece_num][orientation_number][1:]
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


        
    def randomTurn(self): #JF
        all_moves = self.calculateLegalMoves(only_fives_rounds=3)

        if all_moves != []:
            move = random.choice(all_moves)
            self.place_piece(move)
        else:
            self.finished[self.turn-1] = True

        self.switchPlayer()

    def displayStateOfGame(self): #JF
        print(self.score, " Player 1 and Player 2 scores")
        print(self.inv, " Player 1 and Player 2 inventories")

    def switchPlayer(self): #JF
        self.turn_count += 1
        self.turn = 3 - self.turn
        if self.state == 'p1_turn':
            self.state = 'p2_turn'
        else:
            self.state = 'p1_turn'
    
    def checkWin(self, tempBoard): #JF
        if tempBoard.finished[tempBoard.turn-1] and tempBoard.score[2-tempBoard.turn] > tempBoard.score[tempBoard.turn-1]:
            return True
        return False

        
    def calculateBoardScore_dots(self, board): #JF
        score = 0
        starting_pos = [[4,4], [9,9]]
        w1 = 10 * (100-board.turn*2)
        w2 = 2 - math.log(0.001 * board.turn_count)
        w3 = 0.1
        w4 = 8
        w5 = 2 - math.log(0.001 * board.turn_count)
        w6 = 0.1
        w7 = 20
        # w8 = 1.2

        if board.turn_count >= 25:
            score += w7 * (board.score[self.turn-1] - board.score[2-board.turn])
        
        else:
            for opp_dot in board.possible_squares[2 - self.turn]:
                score -= w1 #+ w2 * (20 - ( math.sqrt( (opp_dot[0] - starting_pos[board.turn-1][0])**2 + (opp_dot[1] - starting_pos[board.turn-1][0])**2 ) ) )
                score -= w3 * sum(opp_dot[2])
            for my_dot in board.possible_squares[self.turn-1]:
                score += w4 #+ w5 * (20 - ( math.sqrt( (my_dot[0] - starting_pos[2-board.turn][0])**2 + (my_dot[1] - starting_pos[2-board.turn][1])**2 ) ) )
                score += w6 * sum(my_dot[2])

            score += w7 * (board.score[self.turn-1] - board.score[2-board.turn])
            # add in score += w8 * (total_inv_score - current_inv_score)
            
        return score

    def calculateBoardScore_squares(self, board): #JF
        score = 0
        w1 = 1
        w2 = 1
        w3 =  0
        score += w1 * board.score[self.turn-1]
        score -= w2 * board.score[2-self.turn]
        return score 

        
    def lookahead(self, board, depth): #JF
        if depth == 0:
            return board.calculateBoardScore_dots(board)
        else:
            board.switchPlayer()
            move_list = board.calculateLegalMoves(only_fives_rounds=6)
            best_val = -9999
            for my_move in move_list:
                tempBoard = copy.deepcopy(board)
                tempBoard.place_piece(my_move)
                if board.checkWin(tempBoard):
                    return (-10000)
                val = tempBoard.lookahead(tempBoard,depth-1)
                if val > best_val:
                    best_val = val
            return (-1*best_val)

    def minimax(self, board, depth, isMaximizingPlayer, alpha, beta):
        if depth == 0:
            return board.calculateBoardScore_dots(board)
        # else:
        #     board.switchPlayer()
        
        if isMaximizingPlayer:
            move_list = board.calculateLegalMoves(only_fives_rounds=6)
            best_val = -9999
            for my_move in move_list:
                tempBoard = copy.deepcopy(board)
                tempBoard.place_piece(my_move)
                board.switchPlayer()
                value = board.minimax(tempBoard, depth-1, False, alpha, beta)
                best_val = max( best_val, value) 
                alpha = max( alpha, best_val)
                if beta <= alpha:
                    break
            return best_val

        else:
            move_list = board.calculateLegalMoves(only_fives_rounds=6)
            best_val = 9999
            for my_move in move_list:
                tempBoard = copy.deepcopy(board)
                tempBoard.place_piece(my_move)
                tempBoard.switchPlayer()
                value = board.minimax(tempBoard, depth-1, True, alpha, beta)
                best_val = min( best_val, value) 
                beta = min( beta, best_val)
                if beta <= alpha:
                    break
            return best_val
        
    def smartTurn(self, level): #JF
        move_list = self.calculateLegalMoves(only_fives_rounds=4)
        random.shuffle(move_list)
        print("Number of moves available: ", len(move_list))
        best_val = -10001
        best_move = []
        # ind = 1
        for my_move in move_list:
            tempBoard = copy.deepcopy(self)
            tempBoard.place_piece(my_move)
            if tempBoard.checkWin(tempBoard):
                return (my_move)
            # val = self.lookahead(tempBoard, level)
            val = self.minimax(tempBoard, level, True, 999999, -999999)
            if val > best_val:
                best_val = val
                best_move = copy.copy(my_move)
            # ind += 1
        return best_move

        
    def playSmart(self, level): #JF
        best_move = self.smartTurn(level)
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
            if legal_move:
                legal_move = self.is_legal_move(x, y, choice, orientaion)
            if legal_move:
                break
            print("NOOOOOOOOOOOOOOOOOO try again")

        self.place_piece(x, y, choice, orientaion)


        def squareDiff(self): 
            return self.score[0]-self.score[1]

        # def is_legal_move(self, x, y, choice, orientation):
        #     valid = True
        #     for block in self.pieces[choice][orientation][0]:
        #         x_prime = block[0]+x
        #         y_prime = block[1]+y
        #         # checks out of bounds, and not occupied by either player
        #         if not self.is_valid_to_place_here(x_prime, y_prime):
        #             valid = False

        #     # also need to check one of the corners is touching
        #     for block in self.pieces[choice][orientation][0]:
        #         xx = block[0] + x
        #         yy = block[1] + y
        #         # if xx-1 >= 0 and self.board[yy][xx-1] is not self.turn or xx + 1 < self.dim and self.board[yy][xx+1] is not self.turn or yy-1 >= 0 and self.board[yy-1][xx] is not self.turn or yy + 1 < self.dim and self.board[yy+1][xx] is not self.turn:
        #         #     valid = False

        #     return valid