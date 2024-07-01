piece_id = {1: "i1", 2: "i2", 3: "i3", 4: "quadruple line", 12: "f"}
pieces = {
    1: [[
        #only has corners on the one block
        [],
        [[0, 0]],
        [[0, 0]],
        [[0, 0]],
        [[0, 0]]
    ]],
    2: [[
        # orientation #1
        [[0, -1]],
        [[0, -1]],
        [[0, 0]],
        [[0, 0]],
        [[0, -1]]
    ]],
    3: [[
        # orientation #1
        [[0, -1]],
        [[0, -1]],
        [[0, 0]],
        [[0, 0]],
        [[0, -1]]
    ]],
    # fill in the first forms of the other pieces
    12: [
        # orientation #1
        [
            # attached squares
            [[1, -1], [0, -1], [0, 1], [-1, 0]],
            # has northeast corners
            [[0, -1], [1, 0]],
            # has southeast corners
            [[1, 0], [0, 1]],
            # has southwest corners
            [[-1, -1], [0, 1]],
            # has northwest corners
            [[-1, -1]]
        ],
        #orientation #2
        [
            # attached squares
            [[1, 1], [-1, 0], [0, -1], [1, 0]],
            [[1, -1]],
            [[1, -1], [0, 1]],
            [[0, 1], [-1, 0]],
            [[-1, 0], [0, -1]]
        ],
    ]
}


class Board:
    '''
	Board class initialization
	s - The length of the sides of the board in number of blocks
	where 0,0 represents the top left corner
	'''

    def __init__(self, s: int):
        self.running = True
        self.state = "p1_turn"

        self.dim = s
        self.board = [[0 for i in range(s)] for j in range(s)]
        self.turn = 1

        #change the color of the start positions
        self.board[s - 5][s - 5] = 1

        # score is the # of tiles placed by each player
        self.p1_score = 0
        self.p2_score = 0

        # possible squares and corner avalibility (x,y,NE,SE,SW,NW)
        self.p1_possible_squares = [[5, 5, True, True, True, True]]
        self.p2_possible_squares = [[9, 9, True, True, True, True]]

        #played pieces  # We may want to flip this and say the pieces that have not been played
        # or rather the pieces avalible to play (feels more intuitive)
        self.played = {
            "1": [],  # player 1 pieces
            "2": []  # player 2 pieces
        }

    def print(self):
        for line in self.board:
            for col in line:
                if col == 0:
                    print("□ ", end="")
                elif col == 1:
                    print("\033[96m▣ \033[0m", end="")
                else:
                    print("\033[92m▣ \033[0m", end="")
            print()

    def getItem(self, coord: tuple[int]):
        #we dont need these checks, eventually theyre prob gonna be removed anyways for that optimization # Always good to have checks!!!! # never know when it'll help with our errors
        if len(coord) != 2:
            raise IndexError
        if coord[0] < 0 or coord[0] >= len(
                self.board) or coord[1] < 0 or coord[1] >= len(self.board[0]):
            raise IndexError
        return self.board[coord[0]][coord[1]]

    def place(self, i, j, id, orientation, plr):
        print(pieces[id][orientation])
        piece = pieces[id][orientation]

        # check if peice is valid
        if id in self.played[plr]:
            return  # unable to play

        #check if piece is inbounds
        if self.inBounds(i, j, id, orientation):
            return  # unable to play

        self.board[i][j] = plr
        for square in piece[0]:
            aj, ai = square
            self.board[i + ai][j + aj] = plr

    def inBounds(self, x, y, id, orientation):
        # we could for ease of inbounds on board keep values of dist from center x,y for each orientation
        # along the lines of more processing beforehand is better

        if x - pieces[id][orientation]['left'] < 0 and x - pieces[id][
                orientation]['right'] >= self.dim:
            return False

        if y - pieces[id][orientation]['top'] < 0 and x - pieces[id][
                orientation]['bottom'] >= self.dim:
            return False

        return True
