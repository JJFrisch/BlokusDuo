from board import Board
from orient import generatePiecesDict, pieces, generateCorners, generatePiecesFromBlockPos

# generateCorners(pieces[13][0][0])
# generatePiecesFromBlockPos()

pieces = generatePiecesDict(pieces)  
print(pieces[10][0])
print(pieces[10][3])
#read from file to get the pieces arrays
board = Board(14, pieces)   

board.print()
i = 0
while board.running:
  # run the first turn
  # board.firstMove('random')

  
  if board.state == 'p1_turn':
    # break
    # if board.turn_count < 2:
    #   board.firstRandomTurn()
    #   board.print()
      # continue
    #player 1's turn
    board.randomTurn()
    board.print()
    print("pieces left:", board.inv[0])
    if i >=15:
      break
    # break
  if board.state == 'p2_turn':
    # if board.turn_count < 2:
    #   board.firstRandomTurn()
    #   board.print()
    #   continue
    #player 2's turn
    board.randomTurn()
    board.print()
    print("pieces left:", board.inv[1])

  if board.state == 'end':
    break

  i+=1