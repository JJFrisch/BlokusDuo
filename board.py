import random
import copy

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

        self.dim = s
        self.board = [[0 for i in range(s)] for j in range(s)]
        self.turn = 1

        #change the color of the start positions
        self.board[s - 5][s - 5] = 2
        self.board[4][4] = 1

        # score is the # of tiles placed by each player
        self.score = [0,0] # player 1 and player 2

        # possible squares and corner avalibility (x,y,NE,SE,SW,NW)
        self.possible_squares = [
            [[4, 4, [True, True, True, True]]], #player 1 possible squares
            [[s-5, s-5, [True, True, True, True]]] #player 2 possible squares
        ]

        # available pieces
        self.inv = [
            [11], #1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21], #player 1
            [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21] #player 2
        ]

        self.pieces = pieces
        self.corner_diffs = [[-1,1], [-1,-1], [1,-1], [1,1]]

    def print(self):
        print(self)

    def __str__(self): 
        s = "   " + " ".join([chr(ord('@')+x+1) for x in list(range(len(self.board)))]) + "\n"
        n=1
        for line in self.board:
            rowNumStr = str(n)
            if len(rowNumStr) == 1:
                rowNumStr = " " + rowNumStr
            s+=rowNumStr + " "
            for col in line:
                if col == 0:
                    s+="□ "
                elif col == 1:
                    s+="\033[96m▣ \033[0m"
                else:
                    s+="\033[92m▣ \033[0m"
            s+="\n"
            n+=1
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
        
    def getEdges(self, x, y):
        edges = []
        edges.append([x+1, y])
        edges.append([x, y+1])
        edges.append([x-1, y])
        edges.append([x, y-1])
        return edges

    def getEdgesValues(self, x, y):
        edges_values = []
        edges_values.append(self.board[y][x+1])
        edges_values.append(self.board[y+1][x])
        edges_values.append(self.board[y][x-1])
        edges_values.append(self.board[y-1][x])
        return edges_values
    #legal moves

    def is_valid_to_place_here(self, x, y):
        valid = True
        edges_values = self.getEdgesValues(x, y)
        if self.turn in edges_values:
            valid = False
        # not already taken by either team
        if self.board[y][x] != 0:
            valid = False
        # not out of bounds
        if x >= self.dim or y >= self.dim or x < 0 or y < 0:
            valid = False
        return valid

    
    # returns a list of all legal moves for current player's turn
    def calculateLegalMoves(self): #JF
       # check all corners of the current player
        legal_placements = []
        for poss_squares_i in range(len(self.possible_squares[self.turn-1])):#[x,y,[NE,SE,SW,NW]] in self.possible_squares[self.turn-1]:
            # print([x,y,[NE,SE,SW,NW]])
            x,y,[NE,SE,SW,NW] = self.possible_squares[self.turn-1][poss_squares_i]
            if self.board[y][x] == 0 or self.score[self.turn-1] == 0:
                if self.turn not in self.getEdges(x,y):
                    for piece_num in self.inv[self.turn-1]:
                        for orientation_number in piece_possible_orientations[piece_num-1]:
                            
                            orientation = self.pieces[piece_num][orientation_number] # should contain [[blocks from center], [ne], [se], etc]
                            for dir in range(4):
                                direction_to_corner = [NE,SE,SW,NW][dir]
                                if direction_to_corner:
                                    # if the direction is True, then the piece can go to the corner
                                    for piece_corner in orientation[dir+1]: # a piece corner is a list of [x,y] for that corner in the NE for ex. array in the orientation
                                        valid = True
                                        center = [ x + self.corner_diffs[dir][0] + (-1*piece_corner[0]), y + self.corner_diffs[dir][1] + (-1*piece_corner[1]) ]
                                        for block in orientation[0]:
                                            x_prime = block[0]+center[0]
                                            y_prime = block[1]+center[1]
                                            if not self.is_valid_to_place_here(x_prime, y_prime):
                                                valid = False
                                        if valid:
                                            #moves append
                                            legal_placements.append([center[0], center[1], piece_num, orientation_number, poss_squares_i, dir])
        return legal_placements


    def is_legal_move(self, x, y, choice, orientaion):
        valid = True
        for block in self.pieces[choice][orientaion][0]:
            x_prime = block[0]+x
            y_prime = block[1]+y
            if not self.is_valid_to_place_here(x_prime, y_prime):
                valid = False

        # also need to check one of the corners is touching

        
        return valid
                                        
    def place_piece(self, move): #JF
        x, y, piece_num, orientation_number, poss_squares_i, dir = move
        print(x, 'x', y, 'y', dir, 'dir') # seems like the wrong dir is given TL=1, TR=2 BR=3 BL=0
        #quick fix but not really
        dir = (dir+2)%4
        dot_to_place_on_dirs = self.possible_squares[self.turn-1][poss_squares_i][2]
        dot_to_place_on_dirs[dir] = False
        if True not in dot_to_place_on_dirs :
            self.possible_squares[self.turn-1].remove(poss_squares_i)
            
        self.board[y][x] = self.turn
        for block in self.pieces[piece_num][orientation_number][0]:
            self.board[y+block[1]][x+block[0]] = self.turn

        # for each possible corner, check if it's legal
        # then add to possible squares


        #doesn't work yet!!!!! 
        NE,SE,SW,NW = self.pieces[piece_num][orientation_number][1:]
        # print(NE,SE,SW,NW)
        for dir in range(4):
            for corner in [NE,SE,SW,NW][dir]:
                # print(corner, "corner", -1*self.corner_diffs[dir][0], -1*self.corner_diffs[dir][1], x, y, 'x,y')
                possible_dot_x = x + (-1*self.corner_diffs[dir][0]) + corner[0]
                possible_dot_y = y + (-1*self.corner_diffs[dir][1]) + corner[1]
                # print(possible_dot_x, possible_dot_y, 'x, y', x, y)
                if self.is_valid_to_place_here(possible_dot_x, possible_dot_y):
                    # print('valid')
                    possible_corners = []
                    for possible_corner_dir in self.corner_diffs:
                        if self.is_valid_to_place_here(possible_dot_x+possible_corner_dir[0]*1, possible_dot_x+possible_corner_dir[1]*1):
                            possible_corners.append(True)
                        else:
                            possible_corners.append(False)
                    self.possible_squares[self.turn-1].append([possible_dot_x, possible_dot_y, possible_corners])

        # remove the piece from inventory
        # self.inv[self.turn-1].remove(piece_num)    
        # # change state and turn
        # if self.state == 'p1_turn':
        #     self.state = 'p2_turn'
        #     self.turn = 2
        # else:
        #     self.state = 'p1_turn'
        #     self.turn = 1
        # #update score
        # self.score[self.turn-1] += 1 + len(self.pieces[piece_num][orientation_number][0])
                


  

    def randomTurn(self):
        all_moves = self.calculateLegalMoves()
        print(self.possible_squares[self.turn-1])
        move = all_moves[random.randint(0,len(all_moves)-1)]
        self.place_piece(move)
        print(self.possible_squares[0])
        return
    
    # UI, etc. for a human to be able to play a piece
    def humanTurn(self):
        legal_move = False
        while legal_move == False:
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
        











pieces = [[[[], [[0, 0]], [[0, 0]], [[0, 0]], [[0, 0]]], [[], [[0, 0]], [[0, 0]], [[0, 0]], [[0, 0]]], [[], [[0, 0]], [[0, 0]], [[0, 0]], [[0, 0]]], [[], [[0, 0]], [[0, 0]], [[0, 0]], [[0, 0]]], [[], [[0, 0]], [[0, 0]], [[0, 0]], [[0, 0]]], [[], [[0, 0]], [[0, 0]], [[0, 0]], [[0, 0]]], [[], [[0, 0]], [[0, 0]], [[0, 0]], [[0, 0]]], [[], [[0, 0]], [[0, 0]], [[0, 0]], [[0, 0]]]], [[[[0, -1]], [[0, 0]], [[0, -1]], [[0, -1]], [[0, 0]]], [[[1, 0]], [[1, 0]], [[1, 0]], [[0, 0]], [[0, 0]]], [[[0, 1]], [[0, 0]], [[0, 1]], [[0, 1]], [[0, 0]]], [[[-1, 0]], [[0, 0]], [[0, 0]], [[-1, 0]], [[-1, 0]]], [[[0, -1]], [[0, 0]], [[0, -1]], [[0, -1]], [[0, 0]]], [[[1, 0]], [[1, 0]], [[1, 0]], [[0, 0]], [[0, 0]]], [[[0, 1]], [[0, 0]], [[0, 1]], [[0, 1]], [[0, 0]]], [[[-1, 0]], [[0, 0]], [[0, 0]], [[-1, 0]], [[-1, 0]]]], [[[[0, -1], [0, 1]], [[0, 1]], [[0, -1]], [[0, -1]], [[0, 1]]], [[[1, 0], [-1, 0]], [[1, 0]], [[1, 0]], [[-1, 0]], [[-1, 0]]], [[[0, 1], [0, -1]], [[0, -1]], [[0, 1]], [[0, 1]], [[0, -1]]], [[[-1, 0], [1, 0]], [[1, 0]], [[1, 0]], [[-1, 0]], [[-1, 0]]], [[[0, -1], [0, 1]], [[0, 1]], [[0, -1]], [[0, -1]], [[0, 1]]], [[[1, 0], [-1, 0]], [[1, 0]], [[1, 0]], [[-1, 0]], [[-1, 0]]], [[[0, 1], [0, -1]], [[0, -1]], [[0, 1]], [[0, 1]], [[0, -1]]], [[[-1, 0], [1, 0]], [[1, 0]], [[1, 0]], [[-1, 0]], [[-1, 0]]]], [[[[0, -1], [0, 1], [0, 2]], [[0, 2]], [[0, -1]], [[0, -1]], [[0, 2]]], [[[1, 0], [-1, 0], [-2, 0]], [[1, 0]], [[1, 0]], [[-2, 0]], [[-2, 0]]], [[[0, 1], [0, -1], [0, -2]], [[0, -2]], [[0, 1]], [[0, 1]], [[0, -2]]], [[[-1, 0], [1, 0], [2, 0]], [[2, 0]], [[2, 0]], [[-1, 0]], [[-1, 0]]], [[[0, -1], [0, 1], [0, 2]], [[0, 2]], [[0, -1]], [[0, -1]], [[0, 2]]], [[[1, 0], [-1, 0], [-2, 0]], [[1, 0]], [[1, 0]], [[-2, 0]], [[-2, 0]]], [[[0, 1], [0, -1], [0, -2]], [[0, -2]], [[0, 1]], [[0, 1]], [[0, -2]]], [[[-1, 0], [1, 0], [2, 0]], [[2, 0]], [[2, 0]], [[-1, 0]], [[-1, 0]]]], [[[[0, -1], [0, 1], [0, 2], [0, -2]], [[0, 2]], [[0, -2]], [[0, -2]], [[0, 2]]], [[[1, 0], [-1, 0], [-2, 0], [2, 0]], [[2, 0]], [[2, 0]], [[-2, 0]], [[-2, 0]]], [[[0, 1], [0, -1], [0, -2], [0, 2]], [[0, -2]], [[0, 2]], [[0, 2]], [[0, -2]]], [[[-1, 0], [1, 0], [2, 0], [-2, 0]], [[2, 0]], [[2, 0]], [[-2, 0]], [[-2, 0]]], [[[0, -1], [0, 1], [0, 2], [0, -2]], [[0, 2]], [[0, -2]], [[0, -2]], [[0, 2]]], [[[1, 0], [-1, 0], [-2, 0], [2, 0]], [[2, 0]], [[2, 0]], [[-2, 0]], [[-2, 0]]], [[[0, 1], [0, -1], [0, -2], [0, 2]], [[0, -2]], [[0, 2]], [[0, 2]], [[0, -2]]], [[[-1, 0], [1, 0], [2, 0], [-2, 0]], [[2, 0]], [[2, 0]], [[-2, 0]], [[-2, 0]]]], [[[[1, 0], [0, 1], [-1, 1]], [[0, 1], [1, 0]], [[1, 0]], [[0, 0], [-1, 1]], [[-1, 1]]], [[[0, 1], [-1, 0], [-1, -1]], [[-1, -1], [0, 0]], [[0, 1]], [[0, 1], [-1, 0]], [[-1, -1]]], [[[-1, 0], [0, -1], [1, -1]], [[1, -1]], [[1, -1], [0, 0]], [[-1, 0]], [[-1, 0], [0, -1]]], [[[0, -1], [1, 0], [1, 1]], [[0, -1], [1, 0]], [[1, 1]], [[1, 1], [0, 0]], [[0, -1]]], [[[-1, 0], [0, 1], [1, 1]], [[0, 1], [-1, 0]], [[-1, 0]], [[0, 0], [1, 1]], [[1, 1]]], [[[0, 1], [-1, 0], [-1, -1]], [[-1, -1], [0, 0]], [[0, 1]], [[0, 1], [-1, 0]], [[-1, -1]]], [[[-1, 0], [0, -1], [1, -1]], [[1, -1]], [[1, -1], [0, 0]], [[-1, 0]], [[-1, 0], [0, -1]]], [[[0, -1], [1, 0], [1, 1]], [[0, -1], [1, 0]], [[1, 1]], [[1, 1], [0, 0]], [[0, -1]]]], [[[[0, -1], [1, 0], [-1, 0]], [[1, 0]], [[1, 0], [0, -1]], [[0, -1], [-1, 0]], [[-1, 0]]], [[[1, 0], [0, 1], [0, -1]], [[1, 0], [0, -1]], [[1, 0], [0, 1]], [[0, 1]], [[0, -1]]], [[[0, 1], [-1, 0], [1, 0]], [[1, 0]], [[0, 1], [1, 0]], [[0, 1], [-1, 0]], [[-1, 0]]], [[[-1, 0], [0, -1], [0, 1]], [[0, -1]], [[0, 1]], [[-1, 0], [0, 1]], [[-1, 0], [0, -1]]], [[[0, -1], [-1, 0], [1, 0]], [[-1, 0]], [[-1, 0], [0, -1]], [[0, -1], [1, 0]], [[1, 0]]], [[[1, 0], [0, 1], [0, -1]], [[1, 0], [0, -1]], [[1, 0], [0, 1]], [[0, 1]], [[0, -1]]], [[[0, 1], [-1, 0], [1, 0]], [[1, 0]], [[0, 1], [1, 0]], [[0, 1], [-1, 0]], [[-1, 0]]], [[[-1, 0], [0, -1], [0, 1]], [[0, -1]], [[0, 1]], [[-1, 0], [0, 1]], [[-1, 0], [0, -1]]]], [[[[0, -1], [-1, 0], [-2, 0]], [[0, 0]], [[0, -1]], [[0, -1], [-2, 0]], [[-2, 0]]], [[[1, 0], [0, -1], [0, -2]], [[1, 0], [0, -2]], [[1, 0]], [[0, 0]], [[0, -2]]], [[[0, 1], [1, 0], [2, 0]], [[2, 0]], [[0, 1], [2, 0]], [[0, 1]], [[0, 0]]], [[[-1, 0], [0, 1], [0, 2]], [[0, 0]], [[0, 2]], [[-1, 0], [0, 2]], [[-1, 0]]], [[[0, -1], [1, 0], [2, 0]], [[0, 0]], [[0, -1]], [[0, -1], [2, 0]], [[2, 0]]], [[[1, 0], [0, -1], [0, -2]], [[1, 0], [0, -2]], [[1, 0]], [[0, 0]], [[0, -2]]], [[[0, 1], [1, 0], [2, 0]], [[2, 0]], [[0, 1], [2, 0]], [[0, 1]], [[0, 0]]], [[[-1, 0], [0, 1], [0, 2]], [[0, 0]], [[0, 2]], [[-1, 0], [0, 2]], [[-1, 0]]]], [[[[1, 0], [0, 1], [1, 1]], [[1, 1]], [[1, 0]], [[0, 0]], [[0, 1]]], [[[0, 1], [-1, 0], [-1, 1]], [[0, 0]], [[0, 1]], [[-1, 1]], [[-1, 0]]], [[[-1, 0], [0, -1], [-1, -1]], [[0, -1]], [[0, 0]], [[-1, 0]], [[-1, -1]]], [[[0, -1], [1, 0], [1, -1]], [[1, -1]], [[1, 0]], [[0, 0]], [[0, -1]]], [[[-1, 0], [0, 1], [-1, 1]], [[-1, 1]], [[-1, 0]], [[0, 0]], [[0, 1]]], [[[0, 1], [-1, 0], [-1, 1]], [[0, 0]], [[0, 1]], [[-1, 1]], [[-1, 0]]], [[[-1, 0], [0, -1], [-1, -1]], [[0, -1]], [[0, 0]], [[-1, 0]], [[-1, -1]]], [[[0, -1], [1, 0], [1, -1]], [[1, -1]], [[1, 0]], [[0, 0]], [[0, -1]]]], [[[[0, -1], [1, -1], [-1, 0], [-1, 1]], [[-1, 1], [0, 0], [1, -1]], [[1, -1]], [[0, -1], [-1, 0]], [[-1, 1]]], [[[1, 0], [1, 1], [0, -1], [-1, -1]], [[1, 0], [0, -1]], [[1, 1]], [[1, 1], [-1, -1], [0, 0]], [[-1, -1]]], [[[0, 1], [-1, 1], [1, 0], [1, -1]], [[1, -1]], [[0, 1], [1, 0]], [[-1, 1]], [[-1, 1], [1, -1], [0, 0]]], [[[-1, 0], [-1, -1], [0, 1], [1, 1]], [[-1, -1], [1, 1], [0, 0]], [[1, 1]], [[-1, 0], [0, 1]], [[-1, -1]]], [[[0, -1], [-1, -1], [1, 0], [1, 1]], [[1, 1], [0, 0], [-1, -1]], [[-1, -1]], [[0, -1], [1, 0]], [[1, 1]]], [[[1, 0], [1, 1], [0, -1], [-1, -1]], [[1, 0], [0, -1]], [[1, 1]], [[1, 1], [-1, -1], [0, 0]], [[-1, -1]]], [[[0, 1], [-1, 1], [1, 0], [1, -1]], [[1, -1]], [[0, 1], [1, 0]], [[-1, 1]], [[-1, 1], [1, -1], [0, 0]]], [[[-1, 0], [-1, -1], [0, 1], [1, 1]], [[-1, -1], [1, 1], [0, 0]], [[1, 1]], [[-1, 0], [0, 1]], [[-1, -1]]]], [[[[0, -1]], [[1, 0]], [[1, 1]], [[0, 1]], [[1, 1]], [[1, 0]], [[0, -1]], [[0, -1]], [[0, 1]]], [[[1, 0]], [[1, 0]], [[1, 0]], [[0, 0]], [[0, 0]]], [[[0, 1]], [[0, 0]], [[0, 1]], [[0, 1]], [[0, 0]]], [[[-1, 0]], [[0, 0]], [[0, 0]], [[-1, 0]], [[-1, 0]]], [[[0, -1]], [[-1, 0]], [[-1, 1]], [[0, 1]], [[-1, 1]], [[-1, 0]], [[0, -1]], [[0, -1]], [[0, 1]]], [[[1, 0]], [[1, 0]], [[1, 0]], [[0, 0]], [[0, 0]]], [[[0, 1]], [[0, 0]], [[0, 1]], [[0, 1]], [[0, 0]]], [[[-1, 0]], [[0, 0]], [[0, 0]], [[-1, 0]], [[-1, 0]]]], [[[[1, -1], [0, -1], [0, 1], [-1, 0]], [[1, -1]], [[0, 1], [1, -1]], [[0, 1], [-1, 0]], [[-1, 0], [0, -1]]], [[[1, 1], [1, 0], [-1, 0], [0, -1]], [[1, 0], [0, -1]], [[1, 1]], [[1, 1], [-1, 0]], [[-1, 0], [0, -1]]], [[[-1, 1], [0, 1], [0, -1], [1, 0]], [[0, -1], [1, 0]], [[0, 1], [1, 0]], [[-1, 1]], [[-1, 1], [0, -1]]], [[[-1, -1], [-1, 0], [1, 0], [0, 1]], [[-1, -1], [1, 0]], [[1, 0], [0, 1]], [[-1, 0], [0, 1]], [[-1, -1]]], [[[-1, -1], [0, -1], [0, 1], [1, 0]], [[-1, -1]], [[0, 1], [-1, -1]], [[0, 1], [1, 0]], [[1, 0], [0, -1]]], [[[1, 1], [1, 0], [-1, 0], [0, -1]], [[1, 0], [0, -1]], [[1, 1]], [[1, 1], [-1, 0]], [[-1, 0], [0, -1]]], [[[-1, 1], [0, 1], [0, -1], [1, 0]], [[0, -1], [1, 0]], [[0, 1], [1, 0]], [[-1, 1]], [[-1, 1], [0, -1]]], [[[-1, -1], [-1, 0], [1, 0], [0, 1]], [[-1, -1], [1, 0]], [[1, 0], [0, 1]], [[-1, 0], [0, 1]], [[-1, -1]]]], [[[[0, -1], [0, 1], [1, 1], [-1, 1]], [[1, 1]], [[1, 1], [0, -1]], [[0, -1], [-1, 1]], [[-1, 1]]], [[[1, 0], [-1, 0], [-1, 1], [-1, -1]], [[1, 0], [-1, -1]], [[1, 0], [-1, 1]], [[-1, 1]], [[-1, -1]]], [[[0, 1], [0, -1], [-1, -1], [1, -1]], [[1, -1]], [[0, 1], [1, -1]], [[0, 1], [-1, -1]], [[-1, -1]]], [[[-1, 0], [1, 0], [1, -1], [1, 1]], [[1, -1]], [[1, 1]], [[-1, 0], [1, 1]], [[-1, 0], [1, -1]]], [[[0, -1], [0, 1], [-1, 1], [1, 1]], [[-1, 1]], [[-1, 1], [0, -1]], [[0, -1], [1, 1]], [[1, 1]]], [[[1, 0], [-1, 0], [-1, 1], [-1, -1]], [[1, 0], [-1, -1]], [[1, 0], [-1, 1]], [[-1, 1]], [[-1, -1]]], [[[0, 1], [0, -1], [-1, -1], [1, -1]], [[1, -1]], [[0, 1], [1, -1]], [[0, 1], [-1, -1]], [[-1, -1]]], [[[-1, 0], [1, 0], [1, -1], [1, 1]], [[1, -1]], [[1, 1]], [[-1, 0], [1, 1]], [[-1, 0], [1, -1]]]], [[[[1, 0], [0, -1], [-1, 0], [0, 1]], [[0, 1], [1, 0]], [[1, 0], [0, -1]], [[0, -1], [-1, 0]], [[-1, 0], [0, 1]]], [[[0, 1], [1, 0], [0, -1], [-1, 0]], [[1, 0], [0, -1]], [[0, 1], [1, 0]], [[0, 1], [-1, 0]], [[0, -1], [-1, 0]]], [[[-1, 0], [0, 1], [1, 0], [0, -1]], [[1, 0], [0, -1]], [[0, 1], [1, 0]], [[-1, 0], [0, 1]], [[-1, 0], [0, -1]]], [[[0, -1], [-1, 0], [0, 1], [1, 0]], [[0, -1], [1, 0]], [[0, 1], [1, 0]], [[-1, 0], [0, 1]], [[0, -1], [-1, 0]]], [[[-1, 0], [0, -1], [1, 0], [0, 1]], [[0, 1], [-1, 0]], [[-1, 0], [0, -1]], [[0, -1], [1, 0]], [[1, 0], [0, 1]]], [[[0, 1], [1, 0], [0, -1], [-1, 0]], [[1, 0], [0, -1]], [[0, 1], [1, 0]], [[0, 1], [-1, 0]], [[0, -1], [-1, 0]]], [[[-1, 0], [0, 1], [1, 0], [0, -1]], [[1, 0], [0, -1]], [[0, 1], [1, 0]], [[-1, 0], [0, 1]], [[-1, 0], [0, -1]]], [[[0, -1], [-1, 0], [0, 1], [1, 0]], [[0, -1], [1, 0]], [[0, 1], [1, 0]], [[-1, 0], [0, 1]], [[0, -1], [-1, 0]]]], [[[[0, -1], [1, -1], [0, 1], [-1, 1]], [[0, 1], [1, -1]], [[1, -1]], [[0, -1], [-1, 1]], [[-1, 1]]], [[[1, 0], [1, 1], [-1, 0], [-1, -1]], [[1, 0], [-1, -1]], [[1, 1]], [[1, 1], [-1, 0]], [[-1, -1]]], [[[0, 1], [-1, 1], [0, -1], [1, -1]], [[1, -1]], [[0, 1], [1, -1]], [[-1, 1]], [[-1, 1], [0, -1]]], [[[-1, 0], [-1, -1], [1, 0], [1, 1]], [[-1, -1], [1, 0]], [[1, 1]], [[-1, 0], [1, 1]], [[-1, -1]]], [[[0, -1], [-1, -1], [0, 1], [1, 1]], [[0, 1], [-1, -1]], [[-1, -1]], [[0, -1], [1, 1]], [[1, 1]]], [[[1, 0], [1, 1], [-1, 0], [-1, -1]], [[1, 0], [-1, -1]], [[1, 1]], [[1, 1], [-1, 0]], [[-1, -1]]], [[[0, 1], [-1, 1], [0, -1], [1, -1]], [[1, -1]], [[0, 1], [1, -1]], [[-1, 1]], [[-1, 1], [0, -1]]], [[[-1, 0], [-1, -1], [1, 0], [1, 1]], [[-1, -1], [1, 0]], [[1, 1]], [[-1, 0], [1, 1]], [[-1, -1]]]], [[[[1, 0], [2, 0], [0, 1], [0, 2]], [[0, 2], [2, 0]], [[2, 0]], [[0, 0]], [[0, 2]]], [[[0, 1], [0, 2], [-1, 0], [-2, 0]], [[0, 0]], [[0, 2]], [[0, 2], [-2, 0]], [[-2, 0]]], [[[-1, 0], [-2, 0], [0, -1], [0, -2]], [[0, -2]], [[0, 0]], [[-2, 0]], [[-2, 0], [0, -2]]], [[[0, -1], [0, -2], [1, 0], [2, 0]], [[0, -2], [2, 0]], [[2, 0]], [[0, 0]], [[0, -2]]], [[[-1, 0], [-2, 0], [0, 1], [0, 2]], [[0, 2], [-2, 0]], [[-2, 0]], [[0, 0]], [[0, 2]]], [[[0, 1], [0, 2], [-1, 0], [-2, 0]], [[0, 0]], [[0, 2]], [[0, 2], [-2, 0]], [[-2, 0]]], [[[-1, 0], [-2, 0], [0, -1], [0, -2]], [[0, -2]], [[0, 0]], [[-2, 0]], [[-2, 0], [0, -2]]], [[[0, -1], [0, -2], [1, 0], [2, 0]], [[0, -2], [2, 0]], [[2, 0]], [[0, 0]], [[0, -2]]]], [[[[0, -1], [1, -1], [0, 1], [1, 1]], [[1, 1], [1, -1]], [[1, 1], [1, -1]], [[0, -1]], [[0, 1]]], [[[1, 0], [1, 1], [-1, 0], [-1, 1]], [[1, 0]], [[1, 1], [-1, 1]], [[1, 1], [-1, 1]], [[-1, 0]]], [[[0, 1], [-1, 1], [0, -1], [-1, -1]], [[0, -1]], [[0, 1]], [[-1, 1], [-1, -1]], [[-1, 1], [-1, -1]]], [[[-1, 0], [-1, -1], [1, 0], [1, -1]], [[-1, -1], [1, -1]], [[1, 0]], [[-1, 0]], [[-1, -1], [1, -1]]], [[[0, -1], [-1, -1], [0, 1], [-1, 1]], [[-1, 1], [-1, -1]], [[-1, 1], [-1, -1]], [[0, -1]], [[0, 1]]], [[[1, 0], [1, 1], [-1, 0], [-1, 1]], [[1, 0]], [[1, 1], [-1, 1]], [[1, 1], [-1, 1]], [[-1, 0]]], [[[0, 1], [-1, 1], [0, -1], [-1, -1]], [[0, -1]], [[0, 1]], [[-1, 1], [-1, -1]], [[-1, 1], [-1, -1]]], [[[-1, 0], [-1, -1], [1, 0], [1, -1]], [[-1, -1], [1, -1]], [[1, 0]], [[-1, 0]], [[-1, -1], [1, -1]]]], [[[[1, 0], [0, 1]], [[0, 1], [1, 0]], [[1, 0]], [[0, 0]], [[0, 1]]], [[[0, 1], [-1, 0]], [[0, 0]], [[0, 1]], [[0, 1], [-1, 0]], [[-1, 0]]], [[[-1, 0], [0, -1]], [[0, -1]], [[0, 0]], [[-1, 0]], [[-1, 0], [0, -1]]], [[[0, -1], [1, 0]], [[0, -1], [1, 0]], [[1, 0]], [[0, 0]], [[0, -1]]], [[[-1, 0], [0, 1]], [[0, 1], [-1, 0]], [[-1, 0]], [[0, 0]], [[0, 1]]], [[[0, 1], [-1, 0]], [[0, 0]], [[0, 1]], [[0, 1], [-1, 0]], [[-1, 0]]], [[[-1, 0], [0, -1]], [[0, -1]], [[0, 0]], [[-1, 0]], [[-1, 0], [0, -1]]], [[[0, -1], [1, 0]], [[0, -1], [1, 0]], [[1, 0]], [[0, 0]], [[0, -1]]]], [[[[0, -1], [1, -1], [-1, 0], [-2, 0]], [[0, 0], [1, -1]], [[1, -1]], [[0, -1], [-2, 0]], [[-2, 0]]], [[[1, 0], [1, 1], [0, -1], [0, -2]], [[1, 0], [0, -2]], [[1, 1]], [[1, 1], [0, 0]], [[0, -2]]], [[[0, 1], [-1, 1], [1, 0], [2, 0]], [[2, 0]], [[0, 1], [2, 0]], [[-1, 1]], [[-1, 1], [0, 0]]], [[[-1, 0], [-1, -1], [0, 1], [0, 2]], [[-1, -1], [0, 0]], [[0, 2]], [[-1, 0], [0, 2]], [[-1, -1]]], [[[0, -1], [-1, -1], [1, 0], [2, 0]], [[0, 0], [-1, -1]], [[-1, -1]], [[0, -1], [2, 0]], [[2, 0]]], [[[1, 0], [1, 1], [0, -1], [0, -2]], [[1, 0], [0, -2]], [[1, 1]], [[1, 1], [0, 0]], [[0, -2]]], [[[0, 1], [-1, 1], [1, 0], [2, 0]], [[2, 0]], [[0, 1], [2, 0]], [[-1, 1]], [[-1, 1], [0, 0]]], [[[-1, 0], [-1, -1], [0, 1], [0, 2]], [[-1, -1], [0, 0]], [[0, 2]], [[-1, 0], [0, 2]], [[-1, -1]]]], [[[[-2, 0], [-1, 0], [0, -1], [1, -1]], [[0, 0], [1, -1]], [[1, -1]], [[-2, 0], [0, -1]], [[-2, 0]]], [[[0, -2], [0, -1], [1, 0], [1, 1]], [[0, -2], [1, 0]], [[1, 1]], [[1, 1], [0, 0]], [[0, -2]]], [[[2, 0], [1, 0], [0, 1], [-1, 1]], [[2, 0]], [[2, 0], [0, 1]], [[-1, 1]], [[-1, 1], [0, 0]]], [[[0, 2], [0, 1], [-1, 0], [-1, -1]], [[-1, -1], [0, 0]], [[0, 2]], [[0, 2], [-1, 0]], [[-1, -1]]], [[[2, 0], [1, 0], [0, -1], [-1, -1]], [[0, 0], [-1, -1]], [[-1, -1]], [[2, 0], [0, -1]], [[2, 0]]], [[[0, -2], [0, -1], [1, 0], [1, 1]], [[0, -2], [1, 0]], [[1, 1]], [[1, 1], [0, 0]], [[0, -2]]], [[[2, 0], [1, 0], [0, 1], [-1, 1]], [[2, 0]], [[2, 0], [0, 1]], [[-1, 1]], [[-1, 1], [0, 0]]], [[[0, 2], [0, 1], [-1, 0], [-1, -1]], [[-1, -1], [0, 0]], [[0, 2]], [[0, 2], [-1, 0]], [[-1, -1]]]], [[[[0, -2], [0, -1], [0, 1], [0, 2]], [[0, 2]], [[0, -2]], [[0, -2]], [[0, 2]]], [[[2, 0], [1, 0], [-1, 0], [-2, 0]], [[2, 0]], [[2, 0]], [[-2, 0]], [[-2, 0]]], [[[0, 2], [0, 1], [0, -1], [0, -2]], [[0, -2]], [[0, 2]], [[0, 2]], [[0, -2]]], [[[-2, 0], [-1, 0], [1, 0], [2, 0]], [[2, 0]], [[2, 0]], [[-2, 0]], [[-2, 0]]], [[[0, -2], [0, -1], [0, 1], [0, 2]], [[0, 2]], [[0, -2]], [[0, -2]], [[0, 2]]], [[[2, 0], [1, 0], [-1, 0], [-2, 0]], [[2, 0]], [[2, 0]], [[-2, 0]], [[-2, 0]]], [[[0, 2], [0, 1], [0, -1], [0, -2]], [[0, -2]], [[0, 2]], [[0, 2]], [[0, -2]]], [[[-2, 0], [-1, 0], [1, 0], [2, 0]], [[2, 0]], [[2, 0]], [[-2, 0]], [[-2, 0]]]]]