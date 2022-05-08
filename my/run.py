from env import Maze
from brain import QLearningTable
import QtableShow
import time

import json
map_source = {}
with open('my/map.json', 'r') as f:
    map_source = json.load(f)

TOTAL_EPISODE = map_source['config']['total_episode']
CONVER = map_source['config']['conver']
SHOW_STEP = map_source['config']['show_step']

def update(t):
    steps_log = []
    same_road_count = 0
    for episode in range(TOTAL_EPISODE):
        agent_coord = env.reset()
        steps_log_ = []
        steps = 0
        done = False

        while True:

            action = RL.choose_action(str(agent_coord))
            agent_coord_, reward, done = env.step(action)
            if agent_coord != agent_coord_:
                steps += 1
                steps_log_ += [agent_coord_]
            RL.learn(str(agent_coord), action, reward, str(agent_coord_), done)
            agent_coord = agent_coord_.copy()

            if done:
                print(str(episode) + "episode" + "__" + str(steps) + "steps__" + str(agent_coord == env.destination))
                print(steps_log_)
                # print(RL.q_table)
                break

        if steps_log_ == steps_log:
            same_road_count += 1
        else:
            steps_log = steps_log_.copy()
            same_road_count = 0
        if same_road_count == CONVER and done:
            print("已经"+str(CONVER)+"轮收敛稳定")
            break

        if episode % SHOW_STEP == 0:
            print("==============showing============")
            reward_sum, steps_log_tmp = RL.policy(env)
            QtableShow.show(t, episode, RL.q_table, steps_log_tmp)

    reward_sum, steps_log_tmp = RL.policy(env)
    print("==============showing============")
    print("total reward:"+str(reward_sum))
    QtableShow.show(t, TOTAL_EPISODE+1, RL.q_table, steps_log_tmp)
    print("game over")


if __name__ == "__main__":
    env = Maze()
    env.build_maze()
    RL = QLearningTable(
        width = env.width,
        height = env.height,
        actions=list(range(env.n_actions)))
    t = time.time()
    QtableShow.show(t, -1, RL.q_table, [[0,0]])

    update()
    