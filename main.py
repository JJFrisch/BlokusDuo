import json

from board import Board
from orient import generatePiecesDict, rotate

#read from file to get the pieces arrays
orientation = [[0,0,[0,0], [0,0]], [[0,0], [1,1]], [[0,0], [99,1]], [[0,0], [1,1]], [[0,0], [1,1]] ]
NE,SE,SW,NW = orientation[1:]
print(SE)


# board = Board(14, pieces)

# # new_pieces = generatePiecesDict(pieces)
# board.print()

# # board.place(5, 5, 12, 0, 1)
# print(board.legalMoves())

# print(new_pieces[12][0])
# print(new_pieces[12][4])  # to check the generatePiecesDict function

while board.running:
  if board.state == 'p1_turn':
    #player 1's turn

    # board.print()
    break
    # what is it that happens on each turn?
    #
    # identify places to put pieces

  if board.state == 'p2_turn':
    #player 2's turn
    board.print()
    break

  if board.state == 'end':
    break
