from board import Board
import math, random, time
import csv
import numpy as np
import pandas as pd
import time

number_of_simulations = 1
PRINT_BOARD = True

file_name = 'Data/mcts_rand_trial_data.pkl'
states_collected = []
num_sims = random.randint(50,1600)

standard_weights = [37, 12, 31, 12, 20, 15, 25, 25, 25, 0,0,0]

def randWeights():
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
    rounds_choosing_only_difficult_pieces = random.randint(0,8)
    num_of_difficult_pieces_included = random.randint(rounds_choosing_only_difficult_pieces+1,10)
    
    return [w1, w2, w3, w4, w5, w6, w7, w8, w9, rounds_only_5s, rounds_choosing_only_difficult_pieces, num_of_difficult_pieces_included] 
  

for i in range(number_of_simulations):
  init_time = time.time()
  board = Board(14)  
  player_types = [board.rand_monte_carlo_turn, board.playSmart, board.playSmart_v2, board.monte_carlo_turn]
  convert_func_names = {
        board.playSmart_v2 : 'playSmart_v2',
        board.playSmart : 'playSmart_v1',
        board.randomTurn : 'randomTurn',
        board.monte_carlo_turn: 'monteCarlo',
        board.rand_monte_carlo_turn: 'random_monteCarlo'
      }

  player_type = random.choices(player_types, weights=(25, 5, 10, 60), k=1)[0]
  num_levels = random.randint(0,2)
  min_moves = 500
  player_levels = []
  for lvl in range(num_levels):
    num_moves = random.randint(10-lvl, min_moves)
    min_moves = num_moves
    player_levels.append([num_moves, lvl+1])
  player_levels.append([0,num_levels+1])

  if player_type == board.monte_carlo_turn:
    opp_type = random.choices(player_types, weights=(30, 10, 20, 40), k=1)[0]
  else:
    opp_type = board.monte_carlo_turn
  num_levels = random.randint(0,2)
  min_moves = 500
  opp_levels = []
  for lvl in range(num_levels):
    num_moves = random.randint(10-lvl, min_moves)
    min_moves = num_moves
    opp_levels.append([num_moves, lvl+1])
  opp_levels.append([0,num_levels+1])
  
  p1_weights = randWeights()
  p2_weights = randWeights()


  print("Player 1:", convert_func_names[player_type], player_levels)  
  print("Player 2:", convert_func_names[opp_type], opp_levels)

  while board.running:
    poss_moves = len(board.calculateLegalMoves())
    if poss_moves == 0:
      board.finished[board.turn-1] = True
      board.switchPlayer()

    if PRINT_BOARD:
      print()
      board.print()
        
    print("Turn: ", board.turn_count)
    print(board.finished, board.score)
    print(board.state, 'state', board.to_play, 'to play', poss_moves, "moves")
    states_collected = [[], []]
    
    if board.state == 'p1_turn':

      if player_type == board.rand_monte_carlo_turn or player_type == board.monte_carlo_turn:
        states_collected[0] = player_type(p1_weights, 1, num_sims=num_sims)
      else:
        for level in player_levels:
          if poss_moves > level[0]:
            player_type(level[1], p1_weights)
            break
            
            
    elif board.state == 'p2_turn':
      if opp_type == board.rand_monte_carlo_turn or opp_type == board.monte_carlo_turn:
        states_collected[1] = opp_type(p2_weights, 2, num_sims=num_sims)
      else:
        for level in opp_levels:
          if poss_moves > level[0]:
            opp_type(level[1], p2_weights)
            break
      
    # break

    if board.finished == [True,True]:
      board.displayStateOfGame()
      print("The number of rounds played is:", board.turn_count)
      finial_time = time.time()
      d_time = finial_time - init_time

      if states_collected[0] == [] and (player_type == board.rand_monte_carlo_turn or player_type == board.monte_carlo_turn):
        states_collected[0] = player_type(p1_weights, 1, num_sims=num_sims)
      if states_collected[1] == [] and (opp_type == board.rand_monte_carlo_turn or opp_type == board.monte_carlo_turn):
        states_collected[1] = opp_type(p2_weights, 2, num_sims=num_sims)

      # print(len(states_collected), len(states_collected[0]), len(states_collected[1]), 'lens of states collected')
      earlier_df = pd.read_pickle(file_name)
      data_dict = {
        'Board':[],
        'Moves':[],
        'Move_Probs':[], 
        'Reward': [],
        'Weights': [],
        'Num_Sims': []
      }
      weights = [p1_weights, p2_weights]
      
      for n in range(len(states_collected)):
          if states_collected[n] == []:
            print('bruh')
          for row in states_collected[n]:
            if row == []:
              print('bruh bruh')
            data_dict['Board'].append(row[0])
            data_dict['Moves'].append(row[1])
            data_dict['Move_Probs'].append(row[2])
            data_dict['Reward'].append(row[3])
            data_dict['Weights'].append(weights[n])
            data_dict['Num_Sims'].append(num_sims)

          # print(n)
          # print(len(states_collected[n]), len(states_collected[n][0]), len(data_dict))
        
      df = pd.DataFrame(data_dict)
      # pd.to_pickle(df, file_name)

      df_merged = pd.concat([earlier_df, df])
      pd.to_pickle(df_merged, file_name)
            
      
      #######      THIS code below is used to collect data on what weights towards what works best. Random selection of type of player
      # if convert_func_names[player_type] == 'playSmart_v1' :
      #   player_levels = [0,1]
      # if convert_func_names[player_type] == 'randomTurn':
      #   player_levels = 0
      # if convert_func_names[opp_type] == 'playSmart_v1' :
      #   opp_levels = [0,1]
      # if convert_func_names[opp_type] == 'randomTurn':
      #   opp_levels = 0
      # # List that we want to add as a new row
      # # Player Type	Player Levels ex. poss_moves = i. if i > 400: depth =1, i>100: depth=2, i>0:depth=3	Opponent Type	Opponent Levels	Player Score	Opponent Score	Score Differential	Player Pieces Left	Opponent Pieces Left	# rounds	w1 - score per opp dot	w2 - opp dot dist from player start	w3 - score per opp dot open corners #	w4 - score per player dot	w5 - player dot dist from opp start	w6 - score per player dot open corners #	w7 - player score multiplier	w8 - opponent score multiplier	w9 - piece difficulty weight	only 5's rounds	rounds choosing only difficult peices	# of difficult pieces included	
      # p1_list = [convert_func_names[player_type], player_levels, convert_func_names[opp_type], opp_levels, board.score[0], board.score[1], board.score[0]-board.score[1], board.inv[0], board.inv[1], board.turn_count, ]
      # for w in p1_weights:
      #   p1_list.append(w)
      # p1_list.append(d_time)
      # p2_list = [convert_func_names[opp_type], opp_levels, convert_func_names[player_type], player_levels, board.score[1], board.score[0], board.score[1]-board.score[0], board.inv[1], board.inv[0], board.turn_count]
      # for w in p2_weights:
      #   p2_list.append(w)
      # p2_list.append(d_time)
        
      # # Open our existing CSV file in append mode
      # # Create a file object for this file
      # with open(file_name, 'a') as f_object:
      
      #     # Pass this file object to csv.writer()
      #     # and get a writer object
      #     writer_object = writer(f_object)
      
      #     # Pass the list as an argument into
      #     # the writerow()
            
      #     writer_object.writerow(p1_list)
      #     writer_object.writerow(p2_list)
      
      #     # Close the file object
      #     f_object.close()
      
      
      break

