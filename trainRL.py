import ray
from ray import tune
from ray.rllib.algorithms.ppo import PPO
from ray.rllib.env import ParallelPettingZooEnv
from ray.tune.registry import register_env

import traceback

import GPUtil

from blokusEnv import BlokusEnv

def env_creator(config):
    return ParallelPettingZooEnv(BlokusEnv())

# Register the environment
register_env("blokus_env", env_creator)

def policy_mapping_fn(agent_id, *args, **kwargs):
    return "player_0" if agent_id == "player_0" else "player_1"

if __name__ == "__main__":
    try: 
        ray.init()

        tune.run(
            PPO,
            config={
                "env": "blokus_env",
                "framework": "torch",
                "num_workers": 1,  # Increase this for parallelism
                "num_gpus": 0,  # Set to 1 if you have a GPU
                "multiagent": {
                    "policies": {
                        "player_0": (None, env_creator({}).observation_space[0], env_creator({}).action_space[0], {}),
                        "player_1": (None, env_creator({}).observation_space[1], env_creator({}).action_space[1], {}),
                    },
                    "policy_mapping_fn": policy_mapping_fn,
                },
                "checkpoint_config": {
                    "checkpoint_frequency": 50,
                },
            },
            stop={
                "training_iteration": 1000,
            },
            # checkpoint_freq=50,
            storage_path="file:///Users/etashjhanji/Documents/GitHub/BlokusDuo/RL_Results",
        )

        ray.shutdown()
    except Exception as e:
        traceback.print_exc()
        ray.shutdown()