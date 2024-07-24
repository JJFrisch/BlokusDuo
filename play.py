import glob
import os
import time

from sb3_contrib import MaskablePPO
from sb3_contrib.common.maskable.policies import MaskableActorCriticPolicy
from sb3_contrib.common.wrappers import ActionMasker

import numpy as np

import pettingzoo.utils
from blokusEnv import BlokusEnv, actionToDiscrete

print(actionToDiscrete([10, 4, 9, 2]))

env = BlokusEnv.env()

try:
    latest_policy = max(
        glob.glob(f"{env.metadata['name']}*.zip"), key=os.path.getctime
    )
except ValueError:
    print("Policy not found.")
    exit(0)

model = MaskablePPO.load(latest_policy)


for i in range(1):
    env.reset(seed=i)
    env.action_space(env.possible_agents[1]).seed(i)

    scores = {agent: 0 for agent in env.possible_agents}
    total_rewards = {agent: 0 for agent in env.possible_agents}
    round_rewards = []

    for agent in env.agent_iter():
        obs, reward, termination, truncation, info = env.last()

        # Separate observation and action mask
        observation, action_mask = obs.values()

        if termination or truncation:
            # If there is a winner, keep track, otherwise don't change the scores (tie)
            if (
                env.rewards[env.possible_agents[0]]
                != env.rewards[env.possible_agents[1]]
            ):
                winner = max(env.rewards, key=env.rewards.get)
                scores[winner] += env.rewards[
                    winner
                ]  # only tracks the largest reward (winner of game)
            # Also track negative and positive rewards (penalizes illegal moves)
            for a in env.possible_agents:
                total_rewards[a] += env.rewards[a]
            # List of rewards by round, for reference
            round_rewards.append(env.rewards)
            break
        else:
            if agent == env.possible_agents[1]:
                # act = env.action_space(agent).sample(action_mask)
                env.render()
                print(env.board.calculateLegalMoves())
                x      = int(input(": "))
                y      = int(input(": "))
                piece  = int(input(": "))
                orient = int(input(": "))
                act = actionToDiscrete([x, y, piece, orient])
            else:
                # Note: PettingZoo expects integer actions # TODO: change chess to cast actions to type int?
                act = int(
                    model.predict(
                        observation, action_masks=action_mask, deterministic=True
                    )[0]
                )
        env.step(act)
    env.close()