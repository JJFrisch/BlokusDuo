from board import Board
from orient import generatePiecesDict, rotate, pieces

better_pieces = generatePiecesDict(pieces)

#read from file to get the pieces arrays

print(len(better_pieces[12]), 'pp')
board = Board(14, better_pieces)
board.place_piece([2, 2, 11, 0, 0, 0])  #JF
board.place_piece([3, 8, 11, 1, 0, 0])  #JF
board.place_piece([8, 3, 11, 2, 0, 0])  #JF
board.place_piece([7, 7, 11, 3, 0, 0])  #JF
# # new_pieces = generatePiecesDict(pieces)
board.print()
board.running = False

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
