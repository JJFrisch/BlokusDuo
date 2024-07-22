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
        self.wins= [0,0]
        self.done = False

    def reset(self, seed=None, options=None):
        self.agents = copy(self.possible_agents)
        del self.board
        self.board = Board(14)                           # Blokus board
        self.done = False
        # self.state = self.board.asFlatNumpyArr()         # Flattened 14 by 14 (196) matrix of the board

        print(self.action_space(0))
        observations = {
            0: {
                'board': np.array(self.board.board),
                'pieces': np.ones([2,20]),
                # 'action_mask': self._get_action_mask(0),  # Initialize action mask
            }, 
            1: {
                'board': np.array(self.board.board),
                'pieces': np.ones([2,20]), 
                # 'action_mask': self._get_action_mask(0),  # Initialize action mask
            }, 
        }
        infos = {a: {} for a in self.agents}
        return observations, infos

    def step(self, actions):
        print("Actioning agents: ", actions.keys())
        print("Recorded agents: ", self.agents)
        print(actions)

        rewards = {agent: 0 for agent in self.possible_agents}
        # terminations = {0: False, 1: False}
        terminations = {a: a not in self.agents for a in self.possible_agents}
        #Get actions
        # Check if the move is valid and place it + reward
        # TODO: Action mask invalid moves
        if 0 in self.agents: 
            action1 = actions[0]
            # action1 = self._index_to_action(actions[0], self.action_space(0))
            valid1Found = False
            for action in self.board.calculateLegalMoves(): 
                if action1[0] == action[0] and action1[1] == action[1] and action1[2] == action[2] and action1[3] == action[3]: 
                    self.board.place_piece(action)
                    rewards[0] = piecesLenKey[action1[2]-1]
                    valid1Found = True
                    self.board.switchPlayer()
                    break
            if not valid1Found:
                self.board.randomTurn(None, None)
                rewards[0] = -50
                print("INVALID MOVE SELECTED")
            if self.board.calculateLegalMoves()==[]:
                terminations[0] = True

        if 1 in self.agents: 
            action2 = actions[1]
            valid2Found = False
            for action in self.board.calculateLegalMoves(): 
                if action2[0] == action[0] and action2[1] == action[1] and action2[2] == action[2] and action2[3] == action[3]: 
                    self.board.place_piece(action)
                    rewards[1] = piecesLenKey[action2[2]-1]
                    valid2Found = True
                    self.board.switchPlayer()
                    break
            if not valid2Found:
                self.board.randomTurn(None, None)
                rewards[1] = -50
                print("INVALID MOVE SELECTED")
            if self.board.calculateLegalMoves()==[]:
                terminations[1] = True
            # action2 = self._index_to_action(actions[1], self.action_space(1))

        # Check if game is over
        if 0 not in self.agents: 
            terminations[0] = True
        elif 0 in self.agents and self.board.calculateLegalMoves() == []: 
            terminations[0] = True
        self.board.switchPlayer()
        if 1 not in self.agents: 
            terminations[0] = True
        elif 1 in self.agents and self.board.calculateLegalMoves() == []: 
            terminations[1] = True
        self.board.switchPlayer()
        
        
        if terminations[0] and terminations[1]:
            print("GAME OVER")
            if self.board.score[0] > self.board.score[1]:
                rewards[0] += 100
                rewards[1] -= 100
                self.wins[0] += 1
            elif self.board.score[0] < self.board.score[1]:
                rewards[0] -= 100
                rewards[1] += 100
                self.wins[1] += 1
            self.done = True
            # self.reset()

        truncations = {a: False for a in self.agents}

        piecesMB = np.zeros([2,20])
        for piece in range(1,21): 
            if piece in self.board.inv[0]: 
                piecesMB[0][piece-1] = 1
            if piece in self.board.inv[1]: 
                piecesMB[1][piece-1] = 1

        # action_masks = {a: self._get_action_mask(a) for a in self.agents}
        # observations = {
        #     0: {
        #         'board': np.array(self.board.board),
        #         'pieces': np.array(piecesMB), 
        #         # 'action_mask': action_masks[0],  # Include action mask
        #     }, 
        #     1: {
        #         'board': np.array(self.board.board),
        #         'pieces': np.array(piecesMB), 
        #         # 'action_mask': action_masks[1],  # Include action mask
        #     },  
        # }
        observations = {a: {'board': np.array(self.board.board), 'pieces': np.array(piecesMB)} for a in self.agents}

        infos = {a: {} for a in self.agents}

        self.render()
        print(terminations)
        print("Before elimatination ", self.agents)

        if 0 in self.agents and 1 in self.agents and terminations[0]: 
            self.agents.pop(0)
        if 0 in self.agents and 1 not in self.agents and terminations[0]: 
            self.agents.pop(0)
        if 1 in self.agents and 0 not in self.agents and terminations[1]: 
            self.agents.pop(0)
        if 1 in self.agents and 0 in self.agents and terminations[1]: 
            self.agents.pop(1)

        print("After elimatination ", self.agents, "\n")

        return observations, rewards, terminations, truncations, infos

    def render(self):
        print(self.board)

    @functools.lru_cache(maxsize=None)
    def observation_space(self, agent):
        return spaces.Dict({
            "board": spaces.Box(low=0, high=2, shape=(14, 14), dtype=np.int8),  # self.state - flattened board arr - {0:"unused", 1:"p1 block", 2:"p2 block"}
            "pieces": spaces.MultiBinary([2, 20]),                              # pieces left for each player 
        })
    
    @functools.lru_cache(maxsize=None)
    def action_space(self, agent):
        return spaces.Tuple((
            spaces.Discrete(14),            # X Pos [0,14]
            spaces.Discrete(14),            # Y Pos [0,14]
            spaces.Discrete(21, start=1),   # Piece Number [1,21]
            spaces.Discrete(8),             # 4 rotations * 2 flips
                                            # poss squares index is only really for computation, can vary too much for model prediction;
                                            # dir [0,3] not neccesary
        ))
    
    def getWins(self): 
        return self.wins


if __name__ == "__main__":
    from pettingzoo.test import parallel_api_test
    env = BlokusEnv()
    parallel_api_test(env, num_cycles=500000)