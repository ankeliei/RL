from env import Maze
from brain import QLearningTable
import QtableShow
import time
import trainChangeShow

import json
map_source = {}
with open('my/map.json', 'r') as f:
    map_source = json.load(f)

TOTAL_EPISODE = map_source['config']['total_episode']
CONVER = map_source['config']['conver']
SHOW_STEP = map_source['config']['show_step']

def update(t):
    steps_count_log = []       #每轮步数记录
    mean_q_log = []            #每轮q平均值记录
    ifsuccess_log = []         #每轮是否到达奖励点记录
    steps_log = []
    same_road_count = 0
    for episode in range(TOTAL_EPISODE):
        agent_coord = env.reset()
        steps_log_ = []
        steps = 0
        done = False

        while True:

            action = RL.choose_action(str(agent_coord))
            agent_coord_, reward, done = env.step(action)       # done表示本轮结束，无关是否到达终点
            if agent_coord != agent_coord_:                     # 表示是否产生实际移动
                steps += 1
                steps_log_ += [agent_coord_]
            mean_of_q = RL.learn(str(agent_coord), action, reward, str(agent_coord_), done)
            agent_coord = agent_coord_.copy()

            if done:
                print(str(episode) + "episode" + "__" + str(steps) + "steps__" + str(agent_coord == env.destination))   #done表示到达终点
                
                steps_count_log += [steps]
                mean_q_log += [mean_of_q]
                ifsuccess_log += [str(agent_coord == env.destination)]
                # print(steps_log_)
                # print(RL.q_table)
                break

        # if steps_log_ == steps_log:
        #     same_road_count += 1
        # else:
        #     steps_log = steps_log_.copy()
        #     same_road_count = 0
        # if same_road_count == CONVER and done:
        #     print("已经"+str(CONVER)+"轮收敛稳定")
        #     break

        if episode % SHOW_STEP == 0:
            print("==============showing============")
            reward_sum, steps_log_tmp = RL.policy(env)
            QtableShow.show(t, episode, RL.q_table, steps_log_tmp, show_q_table=True)

    reward_sum, steps_log_tmp = RL.policy(env)
    print("==============showing============")
    print("total reward:"+str(reward_sum))
    QtableShow.show(t, TOTAL_EPISODE+1, RL.q_table, steps_log_tmp, show_q_table=True)
    QtableShow.show(t, TOTAL_EPISODE+2, RL.q_table, steps_log_tmp, show_q_table=False)
    QtableShow.show(t, TOTAL_EPISODE+3, RL.q_table, [], show_q_table=True)
    trainChangeShow.show(t, steps_count_log, mean_q_log, ifsuccess_log)
    trainChangeShow.show_q_(t, mean_q_log)  #显示Q值及其变化率
    print("game over")


if __name__ == "__main__":
    env = Maze()
    env.build_maze()
    RL = QLearningTable(
        width = env.width,
        height = env.height,
        actions=list(range(env.n_actions)))
    t = time.time()
    QtableShow.show(t, -1, RL.q_table, [[0,0]], show_q_table=True)

    update(t)

    