import glob
import random
from enum import Enum
from dataclasses import dataclass

from sb3_contrib import MaskablePPO
from sb3_contrib.common.maskable.policies import MaskableActorCriticPolicy
from sb3_contrib.common.wrappers import ActionMasker

import tensorflow as tf

from board import Board
from blokusEnv import BlokusEnv, actionToDiscrete, discreteToAction

@dataclass
class RANDOM():
    pass

@dataclass
class MINIMAX():
    weights: list

@dataclass
class MCTS():
    weights: list
    num_sims: int

@dataclass
class MCTSNN():
    weights: list
    num_sims: int
    value_net: any

@dataclass
class PPO():
    model: MaskablePPO
    env: BlokusEnv

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

    rounds_only_5s = random.randint(0, 10)
    rounds_choosing_only_difficult_pieces = random.randint(0, 8)
    num_of_difficult_pieces_included = random.randint(
    rounds_choosing_only_difficult_pieces + 1, 10)

    return [
        w1, w2, w3, w4, w5, w6, w7, w8, w9, rounds_only_5s,
        rounds_choosing_only_difficult_pieces, num_of_difficult_pieces_included
    ]

# RANDOM()
# MINIMAX(randWeights())
# MCTS(randWeights(), 100)
# MCTSNN(randWeights(), 100, tf.keras.models.load_model('models/value_net_basic.keras'))
# PPO(MaskablePPO.load('BlokusDuo_20240724-142902.zip'), BlokusEnv.env())

# Set players
PLAYER_1 = PPO(MaskablePPO.load('BlokusDuo_20240724-142902.zip'), BlokusEnv.env())
PLAYER_2 = MCTS(randWeights(), 100)
NUM_SIMULATIONS = 5

PRINT_BOARD = False




def getMove(board: Board, player, playerOrder, i):
    pt = type(player)
    if pt == RANDOM:
        return board.randomTurn(place=False)
    elif pt == MINIMAX:
        return board.playSmart(0, player.weights, place=False)
    elif pt == MCTS:
        return board.monte_carlo_turn(player.weights, 1, num_sims=player.num_sims, value_net=None, place=False)
    elif pt == MCTSNN:
        return board.monte_carlo_turn(player.weights, 1, num_sims=player.num_sims, value_net=None, place=False)
    elif pt == PPO:
        env = player.env

        env.reset(seed=i)

        env.board = board
        env.action_space(env.possible_agents[playerOrder]).seed(i)

        obs, reward, termination, truncation, info = env.last()
        observation, action_mask = obs.values()

        act = int(player.model.predict(observation, action_masks=action_mask, deterministic=True)[0])
        return discreteToAction(act)
        
    return None


for i in range(NUM_SIMULATIONS):
    board = Board(14)

    while board.running:
        if board.finished == [True, True]:
            board.displayStateOfGame()
            if PRINT_BOARD:
                print(board)
            break

        if board.finished[board.turn - 1] or board.calculateLegalMoves() == []:
            board.finished[board.turn - 1] = True
            board.switchPlayer()
        else:
            if board.state == 'p1_turn':
                move = getMove(board, PLAYER_1, 0, i)
            elif board.state == 'p2_turn':
                move = getMove(board, PLAYER_2, 1, i)
            board.place_piece(move)
            board.switchPlayer()