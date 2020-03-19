import gym
from gym import spaces
import numpy as np
from gym import utils
from random import randint


class Obstacle:

    def __init__(self):
        self.hole_top = randint(0, 30)
        self.hole_bottom = self.hole_top + 10
        self.pos_x = 40

    def reset(self):
        self.hole_top = randint(0, 30)
        self.hole_bottom = self.hole_top + 10
        self.pos_x = 40

    def step(self):
        self.pos_x -= 1         # increment x-position by -1 (the obstacle moves to the left)
        if self.pos_x > 0:      # reset if the obstacle is outside the environment
            self.reset()

    def set_pos_x(self, pos_x):
        self.pos_x = pos_x

    def get_pos_x(self):
        return self.pos_x

    def get_hole(self):
        return self.hole_top, self.hole_bottom


class Robot:

    def __init__(self):
        self.height = 0

    def move(self, direction):
        if direction == 0 and self.height > 0:          # move up
            self.height -= 2
        elif direction == 1 and self.height < 40-5:     # move down, why 40-5 ?
            self.height += 2
        else:                                           # stay
            self.height = self.height

    def set_height(self, height):
        self.height = height

    def get_height(self):
        return self.height

    def get_x(self):
        return 20

    def reset(self):
        self.height = randint(5, 35)


class RoadEnv(gym.Env, utils.EzPickle):

    def __init__(self):
        from gym.envs.classic_control import rendering

        self.viewer = rendering.SimpleImageViewer()

        self._action_set = {0, 1}                                       # go up, go down
        self.action_space = spaces.Discrete(len(self._action_set))

        # init obstacle
        self.wall = Obstacle()

        # init robot
        self.agent = Robot()

    # if game is over, it resets itself
    def reset_game(self):
        self.wall.reset()
        self.agent.reset()

    # a single time step in the environment
    def step(self, a):
        obs = self._get_obs()
        reward, game_over = self.act(a)
        info = {}

        return obs, reward, game_over, info

    # perform action a
    def act(self, a):
        self.wall.step()
        self.agent.move(a)

        agent_pos_x = self.agent.get_x()
        agent_pos_y = self.agent.get_height()

        hole_top, hole_bottom = self.wall.get_hole()
        wall_pos_x = self.wall.get_pos_x()

        distance_x = abs(agent_pos_x - wall_pos_x)

        collide_x = distance_x < 5
        collide_y = agent_pos_y < hole_top or (agent_pos_y + 5 > hole_bottom)

        game_over = False
        reward = 0.0

        if collide_x or collide_y:
            game_over = True
        else:
            reward = 0.1

        return reward, game_over

    @property
    def _n_actions(self):
        return len(self._action_set)

    def reset(self):
        self.reset_game()
        return self._get_obs()

    def _get_obs(self):
        img = self._get_image

        # image must be expanded along the first dimension for keras
        return np.expand_dims(img, axis=0)

    def render(self):
        img = self._get_image

        # image must be expanded into three color-channels to be shown
        img = np.repeat(img, axis=2)

        # show frame on display
        self.viewer.imshow(img)

        return self.viewer.isopen

    @property
    def _get_image(self):
        img = np.zeros(shape=(40, 40, 1), dtype=np.uint8)

        wall_pos_x = self.wall.get_pos_x()
        width = 4
        img[:, wall_pos_x: wall_pos_x + width, 0] = 128

        hole_top, hole_bottom = self.wall.get_hole()
        img[hole_top: hole_bottom, wall_pos_x: wall_pos_x + width, 0] = 0

        agent_pos_x = self.agent.get_x()
        agent_pos_y = self.agent.get_height()
        img[agent_pos_y: agent_pos_y + width, agent_pos_x: agent_pos_x + width, 0] = 255

        return img

    def close(self):
        if self.viewer is not None:
            self.viewer.close()
            self.viewer = None
