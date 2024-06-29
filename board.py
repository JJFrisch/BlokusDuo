piece_id = {1: "i1", 2: "i1", 3: "triple line", 4: "quadruple line", 12: "f"}
pieces = {
    1: [
        #only has corners on the one block
        [],
        [[0, 0]],
        [[0, 0]],
        [[0, 0]],
        [[0, 0]]
    ],
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
            [[1, 1], [-1,0], [0,-1], [1,0]],
            [[1, -1]],
            [[1, -1], [0, 1]],
            [[0, 1], [-1, 0]],
            [[-1, 0], [0,-1]]
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

        #played pieces
        self.p1_pieces = [False] * 21
        self.p2_pieces = [False] * 21

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
        #we dont need these checks, eventually theyre prob gonna be removed anyways for that optimization
        if len(coord) != 2:
            raise IndexError
        if coord[0] < 0 or coord[0] >= len(
                self.board) or coord[1] < 0 or coord[1] >= len(self.board[0]):
            raise IndexError
        return self.board[coord[0]][coord[1]]

    def place(self, i, j, id, orientation, plr):
        print(pieces[id][orientation])
        piece = pieces[id][orientation]
        self.board[i][j] = plr
        for square in piece[0]:
            aj, ai = square
            self.board[i + ai][j + aj] = plr




