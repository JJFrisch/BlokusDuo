from board import Board
from orient import generatePiecesDict, pieces

pieces = generatePiecesDict(pieces)


#read from file to get the pieces arrays

board = Board(14, pieces)   
# board.board[4][5] = 1
# board.board[3][4] = 1
# board.board[3][5] = 1
# board.board[6][4] = 1
board.print()

while board.running:
  if board.state == 'p1_turn':
    if board.number_of_rounds >= 3:
      break

    print(board.possible_squares[0])
    board.randomTurn()
    if board.number_of_rounds == 1:
      board.possible_squares[0].pop(0)
      
    board.print()
    print(board.inv[0])
    print(board.possible_squares[0])
    break

  if board.state == 'p2_turn':

    if board.number_of_rounds >= 3:
      break
    
    #player 2's turn
    board.randomTurn()
    if board.number_of_rounds == 2:
      board.possible_squares[1].pop(0)
    board.print()
    print(board.inv[0])
    print(board.possible_squares[1])

  # break

  if board.state == 'end':
    break
