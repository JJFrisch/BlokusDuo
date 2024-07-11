from board import Board
from orient import generatePiecesDict, pieces
import math, random
import pandas as pd
from csv import writer


PRINT_BOARD = False
pieces = generatePiecesDict(pieces)  
board = Board(14, pieces)  
# board.running = False



def randWeights():
  weights = []
  w1 = random.uniform(1, 60)
  w2 = random.uniform(1, 60)
  w3 = random.uniform(1, 60)
  w4 = random.uniform(1, 60)
  w5 = random.uniform(1, 60)
  w6 = random.uniform(1, 60)
  w7 = random.uniform(1, 60)
  w8 = random.uniform(1, 60)
  w9 = random.uniform(1, 60)
  
  rounds_only_5s = random.randint(0,10)
  rounds_choosing_only_difficult_pieces = random.randint(0,10)
  num_of_difficult_pieces_included = random.randint(0,10)
  
  return [w1, w2, w3, w4, w5, w6, w7, w8, w9, rounds_only_5s, rounds_choosing_only_difficult_pieces, num_of_difficult_pieces_included] 

p1_weights = randWeights()
p2_weights = randWeights()
# p2_weights = [5,1,1,5,1,1,12,15,0,2,4,6]
while board.running:
  
  print()
  print(board.finished, board.score)

  poss_moves = len(board.calculateLegalMoves())
  print("Turn: ", board.turn_count)
  
  if board.state == 'p1_turn':
    
    if PRINT_BOARD:
      board.print()
          
    # if poss_moves > 0:
    #   board.playSmart_v2(1, p1_weights)
    # elif poss_moves > 100:
    #   board.playSmart_v2(2, p1_weights)
    # else:
    #   board.playSmart_v2(3, p1_weights)


    board.playSmart(0, p1_weights)
    # board.playSmart(0)

    
  elif board.state == 'p2_turn':
      
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
    
    # List that we want to add as a new row
    # Player Type	Player Levels ex. poss_moves = i. if i > 400: depth =1, i>100: depth=2, i>0:depth=3	Opponent Type	Opponent Levels	Player Score	Opponent Score	Score Differential	Player Pieces Left	Opponent Pieces Left	# rounds	w1 - score per opp dot	w2 - opp dot dist from player start	w3 - score per opp dot open corners #	w4 - score per player dot	w5 - player dot dist from opp start	w6 - score per player dot open corners #	w7 - player score multiplier	w8 - opponent score multiplier	w9 - piece difficulty weight	only 5's rounds	rounds choosing only difficult peices	# of difficult pieces included	
    List = []
    
    # Open our existing CSV file in append mode
    # Create a file object for this file
    with open('event.csv', 'a') as f_object:
    
        # Pass this file object to csv.writer()
        # and get a writer object
        writer_object = writer(f_object)
    
        # Pass the list as an argument into
        # the writerow()
        writer_object.writerow(List)
    
        # Close the file object
        f_object.close()
    
    
    
    break

