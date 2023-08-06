import envpool
from easydict import EasyDict
from ding.envs import BaseEnvTimestep


class PoolEnvManager:
    config = dict(
        env_id="Pong-v5",
        env_num=8,
        batch_size=8,
    )

    def __init__(self, cfg):
        self._cfg = cfg
        self._env_num = cfg.env_num
        self._batch_size = cfg.batch_size

    @property
    def env_num(self):
        return self._env_num

    @property
    def ready_obs(self):
        pass

    def launch(self):
        self._envs = envpool.make(self._cfg.env_id, env_type="gym", num_envs=self._env_num, batch_size=self._batch_size)
        self._envs.async_reset()

    def reset(self):
        return self._envs.reset()

    def step(self, action):
        env_id = list(action.keys())
        action = list(action.values())
        self._envs.send(action, env_id)

        obs, rew, done, info = self._envs.recv()
        env_id = info['env_id']
        timesteps = {}
        for i in range(len(env_id)):
            timesteps[env_id[i]] = BaseEnvTimestep(obs[i], rew[i], done[i], info={'env_id': i, 'final_eval_reward': 0.})
        return timesteps

    def close(self):
        pass
