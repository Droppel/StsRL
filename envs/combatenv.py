import time
import gymnasium as gym
import numpy as np
import math
from gymnasium import spaces

from stssim.combat import Combat
from stssim.enemies.jawworm import JawWorm


class CombatEnv(gym.Env):
    """Custom Environment that follows gym interface."""

    metadata = {"render_modes": ["human"], "render_fps": 30}

    def __init__(self, render = False):
        super().__init__()

        # Define action and observation space
        # self.action_space = spaces.Discrete(4)
        self.action_space = spaces.Discrete(12)

        self.observation_space = spaces.Dict({
            "deck": spaces.Box(low=0, high=2, shape=(11,), dtype=np.int32),
            "player_health": spaces.Discrete(31),
            "player_energy": spaces.Discrete(4),
            "player_block": spaces.Discrete(21),
            "enemy_health": spaces.Discrete(47),
            "enemy_intent": spaces.Discrete(3),
            "enemy_block": spaces.Discrete(11),
            "enemy_strength": spaces.Discrete(100),
            "enemy_vulnerable": spaces.Discrete(6),
        })

        self.current_step = 0
        self.current_episode = 0

        self.misses = 0
        self.dorender = render

        self.reset()

    def get_info(self):
        """Here, relevant infos can be added as needed."""
        info = dict()
        info["current_step"] = self.current_step
        info["current_episode"] = self.current_episode
        return info

    def step(self, action):
        done, valid = self.combat.step(action)
        obs = self.compute_observation()

        reward = 0

        if done and self.combat.winner == 1:
            reward = 30 + self.combat.player.health
        elif done and self.combat.winner == 2:
            reward = -100 - self.combat.enemy.health
        # else:
        #     reward = self.combat.player.health - self.combat.enemy.health

        if not valid:
            self.misses += 1
            reward = -10

        terminated = done
        truncated = self.current_step > 50

        info = self.get_info()

        if terminated or truncated:
            info["player_health"] = self.combat.player.health
            info["enemy_health"] = self.combat.enemy.health
            info["is_success"] = self.combat.winner == 1
            info["turns"] = self.combat.current_turn
            info["misses"] = self.misses

        self.current_step += 1
        if self.dorender:
            self.combat.print()
        return obs, reward, terminated, truncated, info
    
    def compute_observation(self):
        deckstate = self.combat.get_deck_state()
        player = self.combat.player
        enemy = self.combat.enemy

        observation = {
            "deck": deckstate,
            "player_health": player.health,
            "player_energy": player.energy,
            "player_block": player.block,
            "enemy_health": enemy.health,
            "enemy_intent": enemy.intent,
            "enemy_block": enemy.block,
            "enemy_strength": enemy.strength,
            "enemy_vulnerable": enemy.vulnerable,
        }
        return observation

    def reset(self, seed=None, options=None):
        self.current_step = 0
        self.current_episode += 1
        self.misses = 0

        # observation = np.array(self.tetris.board)

        self.combat = Combat(JawWorm())

        observation = self.compute_observation()

        info = self.get_info()
        return observation, info