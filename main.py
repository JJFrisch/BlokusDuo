from board import Board
from orient import generatePiecesDict, pieces, generateCorners, generatePiecesFromBlockPos

# generateCorners(pieces[13][0][0])
# generatePiecesFromBlockPos()

pieces = generatePiecesDict(pieces)  
# print(pieces[0][0])
print(pieces[4][0])
print(pieces[4][3])
#read from file to get the pieces arrays
board = Board(14, pieces)   

board.print()
i = 0
while board.running:
  # break
  # run the first turn
  if board.finished == [True,True]:
    print("Game Over!!")
    print("Score for player 1 was: ", board.score[0])
    print("Score for player 2 was: ", board.score[1])
    board.state = 'end'
  
  if board.state == 'p1_turn':

    board.randomTurn()
    board.print()
    print("pieces left:", board.inv[0])

  if board.state == 'p2_turn':

    board.randomTurn()
    board.print()
    print("pieces left:", board.inv[1])

  if board.state == 'end':
    break

  i+=1