import gymnasium as gym
from gymnasium import Env, spaces
import random 
import numpy as np 
import os
from board import Board
from pettingzoo import ParallelEnv, AECEnv
from pettingzoo.utils import agent_selector
import functools
import random
from copy import copy, deepcopy

# NUmber of block (the reward) for each piece
piecesLenKey = [ 1, 2, 3, 4, 5, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 3, 5, 5, 5, ]

def discreteToAction(action):
    x = action // (14 * 21 * 8)
    action %= (14 * 21 * 8)
    y = action // (21 * 8)
    action %= (21 * 8)
    piece = action // 8
    orientation = action % 8
    return (x, y, piece, orientation)

def toTwos(arr): 
    arr2d = deepcopy(arr)
    for row in arr2d: 
        for i in range(len(row)): 
            if row[i] == -1: 
                row[i] = 2
    return arr2d

def actionToDiscrete(action):
    return (((action[0] * 14 + action[1]) * 21 + action[2]) * 8) + action[3]

# class BlokusEnv(ParallelEnv): 
class BlokusEnv(AECEnv): 
    def __init__(self):
        self.metadata = {
            "is_parallelizable": True,
            "name": "BlokusDuo",
        }

        self.board = Board(14)                           # Blokus board
        # self.state = self.board.asFlatNumpyArr()         # Flattened 14 by 14 (196) matrix of the board
        self.possible_agents = [0,1]
        self.agents = copy(self.possible_agents)
        self.wins= [0,0]
        self.done = False

        self.rewards = {i: 0 for i in self.agents}
        self.terminations = {i: False for i in self.agents}
        self.truncations = {i: False for i in self.agents}
        self.infos = {i: {} for i in self.agents}

        self._agent_selector = agent_selector(self.agents)
        self.agent_selection = self._agent_selector.reset()

        self.observation_spaces = {
            i: spaces.Dict({
                "observation": spaces.MultiDiscrete([3]*196+[2]*42, dtype=np.int8),
                "action_mask": spaces.MultiBinary(14 * 14 * 21 * 8),                    # action mask for each player
            })
            for i in self.agents
        }
 
        self.action_spaces = {i: spaces.Discrete(14*14*21*8) for i in self.agents}

    def observe(self, agent):
        if agent == 0:
            agent = 1
        elif agent == 1: 
            agent = -1

        piecesMB = np.zeros([2,21])
        for piece in range(1,22): 
            if piece in self.board.inv[0]: 
                piecesMB[0][piece-1] = 1
            if piece in self.board.inv[1]: 
                piecesMB[1][piece-1] = 1
        
        if agent == 1: 
            retPieces = piecesMB
        elif agent == -1:
            retPieces = piecesMB[::-1]
        return {
            "observation": np.concatenate((np.array(toTwos(self.board.get_flipped_board(self.board, agent))).flatten(), np.array(retPieces).flatten()) ).astype(np.int8),  # self.state - flattened board arr - {0:"unused", 1:"p1 block", 2:"p2 block"}                             # pieces left for each player 
            "action_mask": self.genActionMask(),                      # action mask for each player
        }

    def reset(self, seed=None, options=None):
        # print("RESET CALLED")
        self.agents = copy(self.possible_agents)
        del self.board
        self.board = Board(14)                           # Blokus board
        self.done = False
        self._cumulative_rewards = {i: 0 for i in self.agents}

        self.rewards = {i: 0 for i in self.agents}
        self.terminations = {i: False for i in self.agents}
        self.truncations = {i: False for i in self.agents}
        self.infos = {i: {} for i in self.agents}
        
        # self.state = self.board.asFlatNumpyArr()         # Flattened 14 by 14 (196) matrix of the board


        # masks = [self.genActionMask()]
        # self.board.switchPlayer()
        # masks.append(self.genActionMask())
        # self.board.switchPlayer()
        
        # observations = {
        #     0: {
        #         "observation":  np.concatenate((np.array(self.board.board, dtype=np.int8).flatten(), np.ones([2,21]).flatten())).astype(np.int8),
        #         'action_mask': masks[0],  # Initialize action mask
        #     }, 
        #     1: {
        #         "observation":  np.concatenate((np.array(self.board.board, dtype=np.int8).flatten(), np.ones([2,21]).flatten())).astype(np.int8),
        #         'action_mask': masks[1],  # Initialize action mask
        #     }, 
        # }

    def env(**kwargs): 
        return BlokusEnv()

    def step(self, actions):
        # print("STEP CALLED")
        if (
            self.terminations[self.agent_selection]
            or self.truncations[self.agent_selection]
        ):
            self.board.switchPlayer()
            return self._was_dead_step(actions)

        current_agent = self.agent_selection
        # current_index = self.agents.index(current_agent)
        actions = int(actions)
        actionArr = discreteToAction(actions)
        self.rewards = {i: 0 for i in self.agents}

        valid1Found = False

        for action in self.board.calculateLegalMoves(): 
            if actionArr[0] == action[0] and actionArr[1] == action[1] and actionArr[2] == action[2] and actionArr[3] == action[3]: 
                self.board.place_piece(action)
                # self.rewards[current_agent] = piecesLenKey[actionArr[2]-1]
                valid1Found = True
                break
        if not valid1Found:
            if self.board.calculateLegalMoves() != []:
                self.render()
                # print(self.board.calculateLegalMoves())
                # Should never be called
                self.board.randomTurn(None, None)
                print("INVALID MOVE SELECTED", actionArr)
        if self.board.calculateLegalMoves()==[]:
            self.terminations[current_agent] = True


        # Check if game is over
        if 0 not in self.agents: 
            self.terminations[0] = True
        elif 0 in self.agents and self.board.calculateLegalMoves() == []: 
            self.terminations[0] = True
        self.board.switchPlayer()
        if 1 not in self.agents: 
            self.terminations[0] = True
        elif 1 in self.agents and self.board.calculateLegalMoves() == []: 
            self.terminations[1] = True
        self.board.switchPlayer()
        
        if self.terminations[0] and self.terminations[1]:
            if self.board.score[0] > self.board.score[1]:
                self.rewards[0] += 1
                self.rewards[1] -= 1
                self.wins[0] += 1
                # print("Player 1 wins")
            elif self.board.score[0] < self.board.score[1]:
                self.rewards[0] -= 1
                self.rewards[1] += 1
                self.wins[1] += 1
                # print("Player 2 wins")
            
            # print()
            self.done = True
            # self.reset()

        truncations = {a: False for a in self.agents}

        piecesMB = np.zeros([2,21])
        for piece in range(1,22): 
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
        
        # masks = [self.genActionMask()]
        # self.board.switchPlayer()
        # masks.append(self.genActionMask())
        # self.board.switchPlayer()

        # returnPieces = [piecesMB, [piecesMB[1], piecesMB[0]]]

        # returnBoards = [toTwos(self.board.board), toTwos(self.board.get_flipped_board(self.board, -1))]

        # observations = {
        #     a: {
        #         'observation': np.concatenate((np.array(returnBoards[a], dtype=np.int8).flatten(), np.array(returnPieces[a]).flatten() )).astype(np.int8), 
        #         'action_mask': masks[a]
        #     }
        #     for a in self.agents
        # }

        # infos = {a: {} for a in self.agents}

        # self.render()

        self._accumulate_rewards()

        self.board.switchPlayer()
        self.agent_selection = self._agent_selector.next() # Give turn to the next agent

    def render(self):
        print(self.board)

    # @functools.lru_cache(maxsize=None)
    # def observation_space(self, agent):
    #     return spaces.Dict({
    #         "board": spaces.Box(low=0, high=2, shape=(14, 14), dtype=np.int8),  # self.state - flattened board arr - {0:"unused", 1:"p1 block", 2:"p2 block"}
    #         "pieces": spaces.MultiBinary([2, 20]),                              # pieces left for each player 
    #         "action_mask": spaces.MultiBinary(14 * 14 * 21 * 8),                      # action mask for each player
    #     })
    
    @functools.lru_cache(maxsize=None)
    def action_space(self, agent):
        return spaces.Discrete(14*14*21*8)
    
    def getWins(self): 
        return self.wins
    
    # Generates the aciton mask for the CURRENT PLAYER according to the BOARD OBJECT
    def genActionMask(self): 
        mask = np.zeros([14, 14, 21, 8], np.int8)
        for move in self.board.calculateLegalMoves():
            x, y, piece, orientation = move
            mask[x][y][piece][orientation] = 1
        return mask.flatten()
    def genActionMaskArgs(self, _): return self.genActionMask()

    def close(self): pass


if __name__ == "__main__":
    from pettingzoo.test import parallel_api_test, api_test
    env = BlokusEnv()
    # parallel_api_test(env, num_cycles=500000)
    api_test(env, num_cycles=500000)