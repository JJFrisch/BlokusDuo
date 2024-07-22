import gymnasium as gym
from gymnasium import Env, spaces
import random 
import numpy as np 
import os
from board import Board
from pettingzoo import ParallelEnv
import functools
import random
from copy import copy

# NUmber of block (the reward) for each piece
piecesLenKey = [ 1, 2, 3, 4, 5, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 3, 5, 5, 5, ]

class BlokusEnv(ParallelEnv): 
    def __init__(self):
        self.board = Board(14)                           # Blokus board
        # self.state = self.board.asFlatNumpyArr()         # Flattened 14 by 14 (196) matrix of the board
        self.possible_agents = [0,1]

    def reset(self, seed=None, options=None):
        self.agents = copy(self.possible_agents)
        self.board = Board(14)                           # Blokus board
        # self.state = self.board.asFlatNumpyArr()         # Flattened 14 by 14 (196) matrix of the board

        observations = {
            # 0: {
            #     'board': self.state,
            #     'pieces': self.board.inv,
            # }, 
            # 1: {
            #     'board': self.state,
            #     'pieces': self.board.inv,
            # }, 
            0: {
                'board': np.array(self.board.board),
                'pieces': np.ones([2,20]), 
            }, 
            1: {
                'board': np.array(self.board.board),
                'pieces': np.ones([2,20]), 
            }, 
        }
        infos = {a: {} for a in self.agents}
        return observations, infos

    def step(self, actions):
        #Get actions
        action1 = actions[0]
        action2 = actions[1]

        # Do the actions
        action_mask = [0,0,0,0,0]; 


        rewards = {0: 0, 1: 0}

        # Check if the move is valid and place it + reward
        # TODO: Action mask invalid moves
        valid1Found = False
        for action in self.board.calculateLegalMoves(): 
            if action1[0] == action[0] and action1[1] == action[1] and action1[2] == action[2] and action1[3] == action[3] and action1[4] == action[5]: 
                self.board.place_piece(action)
                rewards[0] = piecesLenKey[action1[2]-1]
                valid1Found = True
                break
        if not valid1Found:
            rewards[0] = -50

        self.board.switchPlayer()

        valid2Found = False
        for action in self.board.calculateLegalMoves(): 
            if action2[0] == action[0] and action2[1] == action[1] and action2[2] == action[2] and action2[3] == action[3] and action2[4] == action[5]: 
                self.board.place_piece(action)
                rewards[1] = piecesLenKey[action2[2]-1]
                valid2Found = True
                break
        if not valid2Found:
            rewards[1] = -50

        self.board.switchPlayer()
        
        # self.state = self.board.asFlatNumpyArr()

        # Check if game is over
        terminations = {0: False, 1: False}
        if self.board.finished[0]: 
            terminations[0] = True
        if self.board.finished[1]: 
            terminations[1] = True

        truncations = {a: False for a in self.agents}

        piecesMB = np.zeros([2,20])
        for piece in range(1,21): 
            if piece in self.board.inv[0]: 
                piecesMB[0][piece-1] = 1
            if piece in self.board.inv[1]: 
                piecesMB[1][piece-1] = 1


        observations = {
            # 0: {
            #     'board': self.state,
            #     'pieces': piecesMB,
            # }, 
            # 1: {
            #     'board': self.state,
            #     'pieces': piecesMB,
            # },
            0: {
                'board': np.array(self.board.board),
                'pieces': np.ones([2,20]), 
            }, 
            1: {
                'board': np.array(self.board.board),
                'pieces': np.ones([2,20]), 
            },  
        }

        infos = {a: {} for a in self.agents}

        return observations, rewards, terminations, truncations, infos

    def render(self):
        print(self.board)

    @functools.lru_cache(maxsize=None)
    def observation_space(self, agent):
        return spaces.Dict({
            "board": spaces.Box(low=0, high=2, shape=(14, 14), dtype=np.int8),  # self.state - flattened board arr - {0:"unused", 1:"p1 block", 2:"p2 block"}
            "pieces": spaces.MultiBinary([2, 20]),                              # pieces left for each player 
            # "action_mask": spaces.Box(low=0, high=1, shape=(14, 14, 21, 8, 4), dtype=np.int8)  # action mask
        })
    
    @functools.lru_cache(maxsize=None)
    def action_space(self, agent):
        return spaces.Tuple((
            spaces.Discrete(14),            # X Pos [0,14]
            spaces.Discrete(14),            # Y Pos [0,14]
            spaces.Discrete(21, start=1),   # Piece Number [1,21]
            spaces.Discrete(8),             # 4 rotations * 2 flips
                                            # poss squares index is only really for computation, can vary too much for model prediction;
            spaces.Discrete(4)              # dir [0,3]
        ))
    

if __name__ == "__main__":
    from pettingzoo.test import parallel_api_test
    env = BlokusEnv()
    parallel_api_test(env, num_cycles=50)