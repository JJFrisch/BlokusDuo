from board import Board
import math, random, time
import csv
import numpy as np
import pandas as pd
import time

number_of_simulations = 3
PRINT_BOARD = True 

file_name = 'Data/playing_data.pkl'
states_collected = []

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
  num_sims = [random.randint(50,1500), random.randint(50,1500)]  # preforms suprisingly well even at 50. Getting beyond 1000 just takes too long
  player_types = [board.rand_monte_carlo_turn, board.playSmart_v2, board.monte_carlo_turn]
  convert_func_names = {
        board.playSmart_v2 : 'playSmart_v2',
        board.playSmart : 'playSmart_v1',
        board.randomTurn : 'randomTurn',
        board.monte_carlo_turn: 'monteCarlo',
        board.rand_monte_carlo_turn: 'random_monteCarlo'
      }

  player_type = random.choices(player_types, weights=(25, 10, 50), k=1)[0]
  if player_type == board.monte_carlo_turn:
    opp_type = random.choices(player_types, weights=(25, 10, 50), k=1)[0]
  else:
    opp_type = board.monte_carlo_turn
    
  types = [player_type, opp_type]
  random.shuffle(types)
  player_type, opp_type = types
  
  if player_type == board.playSmart or player_type == board.playSmart_v2:
    num_levels = random.randint(0,2)
    min_moves = 500
    player_levels = []
    for lvl in range(num_levels):
      num_moves = random.randint(10-lvl, min_moves)
      min_moves = num_moves
      player_levels.append([num_moves, lvl+1])
    player_levels.append([0,num_levels+1])
    print("Player 1:", convert_func_names[player_type], player_levels)  
  else:
    print("Player 1:", convert_func_names[player_type], num_sims[0]) 
    
  if opp_type == board.playSmart or opp_type == board.playSmart_v2:  
    num_levels = random.randint(0,2)
    min_moves = 500
    opp_levels = []
    for lvl in range(num_levels):
      num_moves = random.randint(10-lvl, min_moves)
      min_moves = num_moves
      opp_levels.append([num_moves, lvl+1])
    opp_levels.append([0,num_levels+1])
    print("Player 2:", convert_func_names[opp_type], opp_levels)
  else:
    print("Player 2:", convert_func_names[opp_type], num_sims[1]) 
  
  p1_weights = randWeights()
  p2_weights = randWeights()


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
        states_collected[0] = player_type(p1_weights, 1, num_sims=num_sims[0])
      else:
        for level in player_levels:
          if poss_moves > level[0]:
            player_type(level[1], p1_weights)
            break
            
            
    elif board.state == 'p2_turn':
      if opp_type == board.rand_monte_carlo_turn or opp_type == board.monte_carlo_turn:
        states_collected[1] = opp_type(p2_weights, 2, num_sims=num_sims[1])
      else:
        for level in opp_levels:
          if poss_moves > level[0]:
            opp_type(level[1], p2_weights)
            break
      

    if board.finished == [True,True]:
      print("The number of rounds played is:", board.turn_count)
      finial_time = time.time()
      d_time = finial_time - init_time

      if states_collected[0] == [] and (player_type == board.rand_monte_carlo_turn or player_type == board.monte_carlo_turn):
        states_collected[0] = player_type(p1_weights, 1, num_sims=num_sims[0])
      if states_collected[1] == [] and (opp_type == board.rand_monte_carlo_turn or opp_type == board.monte_carlo_turn):
        states_collected[1] = opp_type(p2_weights, 2, num_sims=num_sims[1])

      # opened = False
      # while not opened:
      #   try:
      #     earlier_df = pd.read_pickle(file_name)
      #     opened = True
      #   except:
      #     pass
          
      data_dict = {
        'Board':[],
        'Moves':[],
        'Move_Probs':[], 
        'Reward': [],
        'Weights': [],
        'Num_Sims': [],
        'mc_type': [],
        'inv_left': []
      }
      weights = [p1_weights, p2_weights]
      mc_type = [convert_func_names[player_type], convert_func_names[opp_type]]
      inv_left = [board.inv[0], board.inv[1]]
      
      for n in range(len(states_collected)):
          if states_collected[n] == None:
            print('bruh')
          for row in states_collected[n]:
            if row == []:
              print('bruh bruh')
            data_dict['Board'].append(row[0])
            data_dict['Moves'].append(row[1])
            data_dict['Move_Probs'].append(row[2])
            data_dict['Reward'].append(row[3])
            data_dict['Weights'].append(weights[n])
            data_dict['Num_Sims'].append(num_sims[n])
            data_dict['mc_type'].append(mc_type[n])
            data_dict['inv_left'].append(inv_left[n])
        
      df = pd.DataFrame(data_dict)
      pd.to_pickle(df, file_name)

      # df_merged = pd.concat([earlier_df, df])
      # pd.to_pickle(df_merged, file_name)
            
      break

