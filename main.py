from board import Board
from orient import generatePiecesDict, pieces

pieces = generatePiecesDict(pieces)

#read from file to get the pieces arrays

board = Board(14, pieces)   
board.board[4][5] = 1
board.board[3][4] = 1
board.board[3][5] = 1
board.print()

while board.running:
  if board.state == 'p1_turn':
    #player 1's turn
    board.randomTurn()
    board.print()
    break

  if board.state == 'p2_turn':
    #player 2's turn
    board.humanTurn()
    board.print()

  if board.state == 'end':
    break
