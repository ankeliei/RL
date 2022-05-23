import matplotlib.pyplot as plt
import json

map_source = {}
with open('my/map.json', 'r') as f:
    map_source = json.load(f)
MAZE_H = map_source['config']['height']  # grid height
MAZE_W = map_source['config']['width']  # grid width
LAND_R = map_source['landform']['land']['reward']
SWAMP_R = map_source['landform']['swamp']['reward']
HELL_R = map_source['landform']['hell']['reward']
DESTINATION_R = map_source['landform']['destination']['reward']
MAP = map_source['map']

def show(t, steps_count_log, mean_q_log, ifsuccess_log):
    episode = len(steps_count_log)
    x = [x for x in range(episode)]
    
    # 二值一起打印
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.plot(x, steps_count_log, 'g', label = 'steps per episode')
    ax1.legend()
    ax1.set_ylabel('steps-episode')
    ax1.set_xlabel('episode')

    ax2 = ax1.twinx()  # this is the important function
    ax2.plot(x, mean_q_log, 'r', label = 'mean of Q table')
    ax2.set_ylabel('mean_Q-episode')
    ax2.set_xlabel('episode')
    ax2.legend()

    plt.savefig(
        fname="my/picture/"+str(t)+"/"+"统计"+str(episode)+"轮.jpeg")

    # 打印steps情况
    text=""
    text += "alpha = "+str(map_source['config']['alpha']) + "\n"
    text += "gamma = "+str(map_source['config']['gamma']) + "\n"
    text += "epsilon = "+str(map_source['config']['epsilon']) + "\n"
    text += "height = "+str(map_source['config']['height']) + "\n"
    text += "width = "+str(map_source['config']['width']) + "\n"
    text += "\n"
    plt.clf()
    ax1 = fig.add_subplot(111)
    ax1.text(int(episode/3*2), int(max(steps_count_log)/2), text)
    ax1.plot(x, steps_count_log, 'g')
    ax1.set_xlabel('episode')
    ax1.set_ylabel('steps-episode')
    plt.savefig(
        fname="my/picture/"+str(t)+"/"+"统计steps"+str(episode)+"轮.jpeg")

    # 打印Q值情况
    text += "reword of land : " + str(LAND_R) + "\n"
    text += "reword of swamp : " + str(SWAMP_R) + "\n"
    text += "reword of hell : " + str(HELL_R) + "\n"
    text += "reword of destination : " + str(DESTINATION_R) + "\n"
    plt.clf()
    ax1 = fig.add_subplot(111)
    ax1.text(int(episode/2), int((max(mean_q_log)-min(mean_q_log))/5+min(mean_q_log)), text)
    ax1.plot(x, mean_q_log, 'r')
    ax1.set_xlabel('episode')
    ax1.set_ylabel('mean_q-episode')
    plt.savefig(
        fname="my/picture/"+str(t)+"/"+"统计Q值"+str(episode)+"轮.jpeg")

    text=""
    text += "alpha = "+str(map_source['config']['alpha']) + "\n"
    text += "gamma = "+str(map_source['config']['gamma']) + "\n"
    text += "epsilon = "+str(map_source['config']['epsilon']) + "\n"
    text += "height = "+str(map_source['config']['height']) + "\n"
    text += "width = "+str(map_source['config']['width']) + "\n"
    text += "\n"
    text += "reword of land : " + str(LAND_R) + "\n"
    text += "reword of swamp : " + str(SWAMP_R) + "\n"
    text += "reword of hell : " + str(HELL_R) + "\n"
    text += "reword of destination : " + str(DESTINATION_R) + "\n"
    text += "\n"
    text += "black_block : hell\n"
    text += "grey_block : swamp\n"
    text += "red_circle : destination\n"
    text += "small_blue_block : steps"
    plt.clf()
    plt.text(0, 0, text, size=10)
    plt.savefig(
        fname="my/picture/"+str(t)+"/"+"info.jpeg")
    plt.clf()

    info = text
    info += "\nsteps_count_log="
    info += str(steps_count_log)
    info += "\nmean_q_log="
    info += str(mean_q_log)
    info += "\nifsuccess_log="
    info += str(ifsuccess_log)

    f = open("my/picture/"+str(t)+"/"+"info.txt", mode='w')
    f.write(info)
    f.close()

def show_q_(t, mean_q_log):    #显示Q表及其导数
    episode = len(mean_q_log)
    x = [x for x in range(episode)]
    f_q = [x-y for (x, y) in zip(mean_q_log[1:], mean_q_log[:-1])]

    plt.clf()
    fig = plt.figure(dpi=200)
    
    ax1 = fig.add_subplot(111)
    ax1.plot(x[1:], f_q, 'g', linewidth=0.5, label='rate of change of Q')
    ax1.set_xlabel('episode')
    ax1.set_ylabel('rate of change')
    ax1.legend()

    ax2 = ax1.twinx()
    ax2.plot(x, mean_q_log, 'r', linewidth=0.5, label='mean of Q table', linestyle='dashdot')
    ax2.set_xlabel('episode')
    ax2.set_ylabel('mean_q-episode')
    ax2.legend()
    

    plt.savefig(
        fname="my/picture/"+str(t)+"/"+"Q值变化率"+str(episode)+"轮.jpeg")
    plt.clf()