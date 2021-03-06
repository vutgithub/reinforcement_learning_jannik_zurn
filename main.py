import time
import numpy as np
from collections import deque
from my_package import RoadEnv, DQNAgent


# Initialize environment
env = RoadEnv.RoadEnv()

# size of input image
state_size = 40 * 40 * 1

# size of possible actions
action_size = env.action_space.n

# Deep-Q-Learning agent
agent = DQNAgent.DQNAgent(state_size, action_size)

# How many time steps will be analyzed during replay?
batch_size = 32

# How many time steps should one episode contain at most?
max_steps = 500

# Total number of episodes for training
n_episodes = 20 #20000

scores_deque = deque()
deque_length = 100
all_avg_scores = []

training = True

for e in range(n_episodes):
    state = env.reset()
    reward = 0.0
    start = time.time()

    for step in range(max_steps):
        done = False

        action = agent.act(state)
        next_state, reward_step, done, _ = env.step(action)

        reward += reward_step

        agent.remember(state, action, reward, next_state, done)
        state = next_state

        if done:
            scores_deque.append(reward)
            if len(scores_deque) > deque_length:
                scores_deque.popleft()

            scores_average = np.array(scores_deque).mean()
            all_avg_scores.append(scores_average)

            print("episode: {}/{}, #steps: {},reward: {}, e: {}, scores average = {}"
                  .format(e, n_episodes, step, reward, agent.epsilon, scores_average))
            break

    if training:
        if len(agent.memory) > batch_size:
            agent.replay(batch_size)
