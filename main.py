from board import Board
from orient import generatePiecesDict, pieces


PRINT_BOARD = True
pieces = generatePiecesDict(pieces)  
board = Board(14, pieces)   

while board.running:
  
  print()
  print(board.finished)
  # break
  # run the first turn
  
  if board.state == 'p1_turn':
    
    if PRINT_BOARD:
      board.print()
      
    poss_moves = len(board.calculateLegalMoves())
    
    # board.playSmart_v2(3)
    if poss_moves > 400:
      board.playSmart_v2(1)
    else:
      board.playSmart_v2(3)

    
  elif board.state == 'p2_turn':
      
    poss_moves = len(board.calculateLegalMoves())
    print("Turn: ", board.turn_count)
    
    if poss_moves > 400:
      board.playSmart(0)
    else:
      board.playSmart(2)

      
      
    if PRINT_BOARD:
      board.print()
    # print("pieces left:", board.inv[1])

  if board.finished == [True,True]:
    board.displayStateOfGame()
    print("The number of rounds played is:", board.turn_count)
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