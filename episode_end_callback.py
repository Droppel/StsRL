from stable_baselines3.common.callbacks import BaseCallback


class EpisodeEndCallback(BaseCallback):
    """
    A custom callback that derives from ``BaseCallback``.

    :param verbose: Verbosity level: 0 for no output, 1 for info messages, 2 for debug messages
    """
    def __init__(self, verbose: int = 0):
        super().__init__(verbose)

    def _on_step(self) -> bool:
        """
        This method will be called by the model after each call to `env.step()`.

        For child callback (of an `EventCallback`), this will be called
        when the event is triggered.

        :return: If the callback returns False, training is aborted early.
        """
        # Check if this step terminated the episode
        # if self.locals.get("done", False):
        if self.locals.get("dones", [False])[0]:
            infos = self.locals.get("infos", {})[0]
            self.logger.record_mean("rollout/player_health", infos.get("player_health", 0))
            self.logger.record_mean("rollout/enemy_health", infos.get("enemy_health", 0))
            self.logger.record_mean("rollout/turns", infos.get("turns", 0))
        return True