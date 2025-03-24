import numpy as np
from stable_baselines3 import SAC, TD3, PPO
import wandb
from envs.combatenv import CombatEnv
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.callbacks import CheckpointCallback, EveryNTimesteps, EvalCallback
from wandb.integration.sb3 import WandbCallback
from stable_baselines3.common.logger import configure
from episode_end_callback import EpisodeEndCallback

render = False
disable_wandb = False
experiment = "CurrentTurn"

if not disable_wandb:
    wandb.init(project="sts_rl", entity="s6cawisw-university-of-bonn", name=experiment, sync_tensorboard=True)

env = CombatEnv(render=render)

check_env(env, warn=True)
model = PPO("MultiInputPolicy", env)

# model = PPO.load(f"experiments/{experiment}/rl_model_10200000_steps.zip", env=env)

checkpoint_on_event = CheckpointCallback(save_freq=1, save_path=f"experiments/{experiment}/")
# event_callback = EveryNTimesteps(n_steps=10000, callback=checkpoint_on_event)

evaluation_callback = EvalCallback(model.get_env(), n_eval_episodes=100, eval_freq=10000, callback_on_new_best=checkpoint_on_event)
episode_end_callback = EpisodeEndCallback()

callbacks = [evaluation_callback, episode_end_callback]

if not disable_wandb:
    wandbcallback = WandbCallback(
                model_save_path=f"wandb/{experiment}",
                verbose=2,
            )
    callbacks.append(wandbcallback)

logger = configure(folder=f"experiments/{experiment}/", format_strings=["stdout", "tensorboard"])
model.set_logger(logger)

# Define and Train the agent
# if show:
#     obs, info = env.reset()
#     while True:
#         action, states = model.predict(obs, deterministic=True)
#         obs, rewards, terminated, truncated, info = env.step(action)
#         env.render(obs["board"].reshape(tetris_height, tetris_width))
#         if terminated:
#             obs, info = env.reset()

model.learn(total_timesteps=100000000, progress_bar=True, callback=callbacks)