from board import Board
from orient import generatePiecesDict, pieces

import csv
from collections import Counter
# import pandas as pd

PRINT_BOARD = True

# generateCorners(pieces[13][0][0])
# generatePiecesFromBlockPos()

pieces = generatePiecesDict(pieces)  


#read from file to get the pieces arrays
board = Board(14, pieces)   

if PRINT_BOARD:
  board.print()

scores = []
piecesPlaced = Counter()

for x in range(1):
  board = Board(14, pieces)
  while board.running:

    # break
    # run the first turn
    
    if board.state == 'p1_turn':
      
      board.randomTurn()
      if PRINT_BOARD:
        board.print()
      # print("pieces left:", board.inv[0])
  
    if board.state == 'p2_turn':
      
      board.playSmart(1)
      if PRINT_BOARD:
        board.print()
      # print("pieces left:", board.inv[1])

    if board.finished == [True,True]:
      board.displayStateOfGame()
      # scores.append((board.score[0], board.score[1]))
      # for inv in board.inv:
      #   for piece in inv:
      #     piecesPlaced[piece+1] += 1
      # board.state = 'end'
      # print(str(x) + " completed")
      break

# print(scores)
# print(piecesPlaced)

# wins = [0,0,0]
# for scoreTup in scores: 
#   if scoreTup[0] > scoreTup[1]:
#     wins[0]+=1
#   elif scoreTup[0] < scoreTup[1]:
#     wins[1]+=1
#   else: 
#     wins[2]+=1
# print("Player 1 and 2 wins and draws (respectively): " + str(wins))
# print("Player 1 and 2 and draws percents (respectively): " + str(wins[0]/len(scores)) + ' '+ str(wins[1]/len(scores))  + ' '+ str(wins[2]/len(scores)))

# with open("scores_temp.csv", 'w', newline='') as f:
#   writer = csv.writer(f)
#   for score in scores:
#     writer.writerow(score)