from board import Board, pieces
from orient import generatePiecesDict, rotate




board = Board(14)

board.place(5, 5, 12, 1, 2)  #the manual 2nd rotation of block '12'
board.print()

print(rotate(pieces[12][0]))  # to check the rotate_ function, see if it lines up with the manual rotation
new_pieces = generatePiecesDict(pieces)
print(new_pieces[12][1])  # to check the generatePiecesDict function
print(new_pieces[1][1])  # to check the generatePiecesDict function

while board.running:
  if board.state == 'p1_turn':
    #player 1's turn
    board.print()

    # what is it that happens on each turn?
    # 
    # identify places to put pieces

  
  if board.state == 'p2_turn':
    #player 2's turn
    board.print()
