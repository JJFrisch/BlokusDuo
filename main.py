from board import Board
from orient import generatePiecesDict, pieces
import math, random


PRINT_BOARD = True
pieces = generatePiecesDict(pieces)  
board = Board(14, pieces)  
# board.running = False

def randWeights():
  weights = []
  w1 = random.uniform(0, 60)
  w2 = random.uniform(0, 60)
  w3 = random.uniform(0, 60)
  w4 = random.uniform(0, 60)
  w5 = random.uniform(0, 60)
  w6 = random.uniform(0, 60)
  w7 = random.uniform(0, 60)
  w8 = random.uniform(0, 60)
  w9 = random.uniform(0, 60)
  
  rounds_only_5s = random.randint(0,10)
  rounds_choosing_only_difficult_pieces = random.randint(0,10)
  num_of_difficult_pieces_included = random.randint(0,10)
  
  return [w1, w2, w3, w4, w5, w6, w7, w8, w9, rounds_only_5s, rounds_choosing_only_difficult_pieces, num_of_difficult_pieces_included] 
p1_weights = randWeights()
print(p1_weights)
p2_weights = [0.000001,0,0,0,0,0,0,00,0,0,4,6]
p2_weights = randWeights()
p2_weights = [5,1,1,3,1,1,8,12,0,0,4,6]

while board.running:
  
  print()
  print(board.finished, board.score)

  poss_moves = len(board.calculateLegalMoves())
  print("Turn: ", board.turn_count)
  
  if board.state == 'p2_turn':
    
    if PRINT_BOARD:
      board.print()
          
    if poss_moves > 0:
      # print(p1_weights)
      board.playSmart_v2(1, p1_weights)
    elif poss_moves > 100:
      board.playSmart_v2(2, p1_weights)
    else:
      board.playSmart_v2(3, p1_weights)


    # board.playSmart_v2(2)
    # board.playSmart(0)

    
  elif board.state == 'p1_turn':
      
    if PRINT_BOARD:
      board.print()
    
    
    board.playSmart(0, p2_weights)
    # board.randomTurn()
    # board.humanTurn()
    
    # if poss_moves > 400:
    #   board.playSmart(0)
    # elif poss_moves > 100:
    #   board.playSmart(1)
    # else:
    #   board.playSmart(2)




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