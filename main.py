from board import Board
from orient import generatePiecesDict, pieces, generateCorners, generatePiecesFromBlockPos

# generateCorners(pieces[13][0][0])
# generatePiecesFromBlockPos()

pieces = generatePiecesDict(pieces)  
#read from file to get the pieces arrays

board = Board(14, pieces)   
# board.board[4][5] = 1
# board.board[3][4] = 1
# board.board[3][5] = 1
# board.board[6][4] = 1
board.print()
i = 0
while board.running:
  # run the first turn
  # board.firstTurn()
    
  if board.state == 'p1_turn':
    #player 1's turn
    board.randomTurn()
    board.print()
    #print("main.py: board.calculateLegalMoves(): ", board.calculateLegalMoves())
    if i >= 3:
      break
    # break
  if board.state == 'p2_turn':
    #player 2's turn
    board.randomTurn()
    board.print()

  if board.state == 'end':
    break