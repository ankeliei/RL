import numpy as np
import pandas as pd

import json
map_source = {}
with open('my/map.json', 'r') as f:
    map_source = json.load(f)
LAND_R = map_source['landform']['land']['reward']
ALPHA = map_source['config']['alpha']
GAMMA = map_source['config']['gamma']
EPSILON = map_source['config']['epsilon']

class QLearningTable:
    def __init__(self, height, width, actions, learning_rate=ALPHA, reward_decay=GAMMA, e_greedy=EPSILON) -> None:
        self.actions = actions  # a list
        self.lr = learning_rate #学习率 旧信息的重要性
        self.gamma = reward_decay   #衰减率 未来奖励的重要性
        self.epsilon = e_greedy     #贪婪度
        self.q_table = pd.DataFrame(columns=self.actions, dtype=np.float64)

        for x in range(height):
            for y in range(width):
                self.q_table.loc[str([x, y])] = LAND_R

    def choose_action(self, observation):
        if np.random.uniform() < self.epsilon:
            state_action = self.q_table.loc[observation, :]
            action = np.random.choice(state_action[state_action == np.max(state_action)].index)
        else:
            action = np.random.choice(self.actions)
        return action
    
    def learn(self, s, a, r, s_, done):
        q_predict = self.q_table.loc[s, a]
        if done:
            q_target = r
        else:
            q_target = r + self.gamma* self.q_table.loc[s_, :].max()
        self.q_table.loc[s, a] += self.lr * (q_target - q_predict)

        if done:
            return np.mean(self.q_table.values.tolist())

    def policy(self, env):
        observation = env.reset()
        done = False
        steps_log = []
        reward_sum = 0
        self.epsilon = 1
        while not done:
            action = self.choose_action(str(observation))
            observation_, reward, done = env.step(action)
            steps_log += [observation_]
            reward_sum += reward
            observation = observation_.copy()
        self.epsilon = EPSILON
        return reward_sum, steps_log
