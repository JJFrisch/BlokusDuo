from board import Board
import math, random, time
import os
import pandas as pd
import tensorflow as tf
import numpy as np
import time
from datetime import datetime
import pytz
import pickle
import gzip

print("Numpy Version: ", np.__version__)
print("TF Version: ", tf.__version__)
if np.__version__ == '2.0.0':
   raise ValueError('WRONG VERSION OF NUMPY')

number_of_simulations = 1
PRINT_BOARD = True 

new_file = False
file_num = 1

while not new_file:
  file_name = 'Data/playing_data/c' + str(file_num) + '.pkl'
  if not os.path.exists(file_name): 
      with open(file_name, 'w') as file: 
          file.write("") 
          break
  else: 
    file_num = int(file_num) + 1

file_name = 'Data/playing_data/c' + str(file_num) + '.pkl'
print("Printing to " + file_name)
states_collected = []
data = pd.DataFrame()

standard_weights = [37, 12, 31, 12, 20, 15, 25, 25, 25, 0,0,0]

def randWeights():
    w1 = random.uniform(1, 15)
    w2 = random.uniform(1, 2)
    w3 = random.uniform(1, 2)
    w4 = random.uniform(1, 15)
    w5 = random.uniform(1, 2)
    w6 = random.uniform(1, 3)
    w7 = random.uniform(1, 20)
    w8 = random.uniform(1, 20)
    w9 = random.uniform(1, 3)
    
    rounds_only_5s = random.randint(0,10)
    rounds_choosing_only_difficult_pieces = random.randint(0,8)
    num_of_difficult_pieces_included = random.randint(rounds_choosing_only_difficult_pieces+1,10)
    
    return [w1, w2, w3, w4, w5, w6, w7, w8, w9, rounds_only_5s, rounds_choosing_only_difficult_pieces, num_of_difficult_pieces_included] 
  

def loadall(filename):
  data = []
  with open(filename, "rb") as f:
      while True:
          try:
              df = pickle.load(f)
              data.append(df)
          except EOFError:
              break
  return data

# load in models
value_net_path = "models/value_net_basic.keras"
value_network = tf.keras.models.load_model(value_net_path)
value_network.summary()

# policy_net_path = "models/policy_net_basic.keras"
# policy_network_saved = tf.keras.models.load_model(policy_net_path)
# policy_network_saved.summary()


sim_num = 0
while sim_num < number_of_simulations:
  sim_num += 1
  init_time = time.time()
  board = Board(14)  
  num_sims = [random.randint(700,2300), random.randint(700,2300)]  
  # num_sims = [random.randint(400,420), random.randint(400,420)]  
  # num_sims = [random.randint(50,51), random.randint(50,51)]  # preforms suprisingly well even at 50. Getting beyond 1000 just takes too long
  player_types = [board.rand_monte_carlo_turn, board.playSmart_v2, board.monte_carlo_turn]

  convert_func_names = {
        board.playSmart_v2 : 'playSmart_v2',
        board.playSmart : 'playSmart_v1',
        board.randomTurn : 'randomTurn',
        board.monte_carlo_turn: 'monteCarlo',
        board.rand_monte_carlo_turn: 'random_monteCarlo'
      }

  player_type = random.choices(player_types, weights=(25, 10, 70), k=1)[0]
  if player_type == board.monte_carlo_turn:
    opp_type = random.choices(player_types, weights=(25, 10, 70), k=1)[0]
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
        states_collected[0] = player_type(p1_weights, 1, num_sims=num_sims[0], value_net=None)
      else:
        for level in player_levels:
          if poss_moves > level[0]:
            player_type(level[1], p1_weights)
            break
            
            
    elif board.state == 'p2_turn':
      if opp_type == board.rand_monte_carlo_turn or opp_type == board.monte_carlo_turn:
        states_collected[1] = opp_type(p2_weights, 2, num_sims=num_sims[1], value_net=None)
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

      data = pd.concat([data, pd.DataFrame(data_dict)])
  

      t = datetime.now(pytz.timezone('America/Chicago')) # one hour early
      print(t)

      if (t.hour+1 >= 1 and t.minute >= 0) and (t.hour+1 <= 3):
          print('time is up!')
          sim_num = math.inf
          break
      elif  t.minute % 60 <= 28:
          hourly_saves.append(data)
          print('hourly save to file!', file_name)
          with gzip.open(file_name, "wb", compresslevel=9) as f:
            for value in hourly_saves:
                try:
                  pickle.dump(value, f)
                  print("sent")
                except:
                    print("failed the hourly save")
          data = pd.DataFrame()

    
      break

hourly_saves.append(data)

with gzip.open(file_name, "wb", compresslevel=9) as f:
    for value in hourly_saves:
        print(value.shape)
        try:
          pickle.dump(value, f)
        except:
           print("couldn't save the hour")
           pass

print('finial save : ', file_name)