from board import Board
from orient import generatePiecesDict, pieces, generateCorners, generatePiecesFromBlockPos

from collections import Counter
# import pandas as pd

PRINT_BOARD = False

# generateCorners(pieces[13][0][0])
# generatePiecesFromBlockPos()

pieces = generatePiecesDict(pieces)  
# print(pieces[0][0])
print(pieces[4][0])
print(pieces[4][1])

#read from file to get the pieces arrays
board = Board(14, pieces)   

if PRINT_BOARD:
  board.print()

scores = []
piecesPlaced = Counter()

for x in range(10):
  board = Board(14, pieces)
  while board.running:
    p1_done = False
    p2_done = False
    # break
    # run the first turn
    
    if board.state == 'p1_turn':
      
      board.randomTurn()
      if PRINT_BOARD:
        board.print()
      # print("pieces left:", board.inv[0])
  
    if board.state == 'p2_turn':
      
      board.randomTurn()
      if PRINT_BOARD:
        board.print()
      # print("pieces left:", board.inv[1])

    if board.finished == [True,True]:
      scores.append((board.score[0], board.score[1]))
      for inv in board.inv:
        for piece in inv:
          piecesPlaced[piece+1] += 1
      board.state = 'end'
      break

print(scores)
print(piecesPlaced)

wins = [0,0,0]
for scoreTup in scores: 
  if scoreTup[0] > scoreTup[1]:
    wins[0]+=1
  elif scoreTup[0] < scoreTup[1]:
    wins[1]+=1
  else: 
    wins[2]+=1
print("Player 1 and 2 wins and draws (respectively): " + str(wins))
print("Player 1 and 2 and draws percents (respectively): " + str(wins[0]/len(scores)) + ' '+ str(wins[1]/len(scores))  + ' '+ str(wins[2]/len(scores)))