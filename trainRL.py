import ray
from ray import tune
from ray.rllib.algorithms.ppo import PPO
from ray.rllib.env import ParallelPettingZooEnv
from ray.tune.registry import register_env
from ray.rllib.algorithms.callbacks import DefaultCallbacks

import traceback

import GPUtil

from blokusEnv import BlokusEnv

def env_creator(config):
    return ParallelPettingZooEnv(BlokusEnv())

# Register the environment
register_env("blokus_env", env_creator)

def policy_mapping_fn(agent_id, *args, **kwargs):
    return "player_0" if agent_id == "player_0" else "player_1"

class CustomCallbacks(DefaultCallbacks):
    def on_postprocess_trajectory(self, *, worker, episode, agent_id, policy_id, postprocessed_batch, **kwargs):
        # Log win rate (assuming you have a way to track wins)
        win_rate = worker.env.getWins()
        self.logger.info(f"Episode {episode.episode_id} wins [p1, p2]: {win_rate}")

    def on_train_result(self, *, trainer, result: dict, **kwargs):
        # Log learning rate
        learning_rate = result.get("config", {}).get("lr", 0)
        self.logger.info(f"Training iteration {result['training_iteration']} learning rate: {learning_rate}")

        # You can also log other metrics like win rate if available in the result dictionary
        # win_rate = result.get("custom_metrics", {}).get("win_rate", 0)
        # self.logger.info(f"Training iteration {result['training_iteration']} win rate: {win_rate}")

if __name__ == "__main__":
    try: 
        ray.init()

        env = env_creator({})
        env.reset()

        tune.run(
            PPO,
            config={
                "env": "blokus_env",
                "framework": "torch",
                "num_workers": 1,  # Increase this for parallelism
                "num_gpus": 0,  # Set to 1 if you have a GPU
                "multiagent": {
                    "policies": {
                        "player_0": (None, env.observation_space[0], env.action_space[0], {}),
                        "player_1": (None, env.observation_space[1], env.action_space[1], {}),
                    },
                    "policy_mapping_fn": policy_mapping_fn,
                },
                # "callbacks": CustomCallbacks,
                "env_config": {"max_episode_steps": None}, 
                "checkpoint_config": {
                    "checkpoint_frequency": 5,
                },
                "no_done_at_end": False, 
            },
            stop={
                "training_iteration": 10,
            },
            # checkpoint_freq=50,
            storage_path="file:///Users/etashjhanji/Documents/GitHub/BlokusDuo/RL_Results",
        )

        ray.shutdown()
    except Exception as e:
        traceback.print_exc()
        ray.shutdown()