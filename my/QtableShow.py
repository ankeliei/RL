import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

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

def show(time, episode, q_table, steps_log, show_q_table):
    try:
        os.mkdir("my/picture/"+str(time))
    except:
        pass
    data = np.zeros([MAZE_H*3, MAZE_W*3])
    data = data + LAND_R
    if show_q_table:
        for index, row in q_table.iterrows():
            index = index[1:-1].split(", ")
            x = int(index[0])
            y = int(index[1])
            data[x*3][y*3+1] = row[0]
            data[x*3+2][y*3+1] = row[1]
            data[x*3+1][y*3] = row[2]
            data[x*3+1][y*3+2] = row[3]

    # plt.rc('font',family='Youyuan',size='9')
    # plt.rc('axes',unicode_minus='False')
    
    plt.figure(dpi=200)
    for x in range(0, MAZE_H):
        for y in range(0, MAZE_W):
            shape = patches.Rectangle((y*3-0.5, x*3-0.5), 3, 3, ec='white', fc='None')
            plt.gca().add_patch(shape)


            if MAP[x][y] == "S":
                shape = patches.Rectangle((y*3-0.5, x*3-0.5), 3, 3, fc = 'grey', ec = 'green', alpha=0.5)
                plt.gca().add_patch(shape)
            if MAP[x][y] == "H":
                shape = patches.Rectangle((y*3-0.5, x*3-0.5), 3, 3, fc = 'black', ec = 'green', alpha=1)
                plt.gca().add_patch(shape)
            if MAP[x][y] == "D":
                shape = patches.Circle((y*3+1, x*3+1), radius=1.5, fc = 'red', ec = 'green', alpha=1)
                plt.gca().add_patch(shape)

    for step in steps_log:
        x = step[0]
        y = step[1]
        shape = patches.Rectangle((y*3+0.5, x*3+0.5), 1, 1, fc = 'blue', ec = 'blue')
        plt.gca().add_patch(shape)
    shape = patches.Rectangle((0.5, 0.5), 1, 1, fc = 'blue', ec = 'blue')
    plt.gca().add_patch(shape)

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
    

    # plt.text(-15, 15, text, size = 5)


    plt.imshow(data, cmap="OrRd")
    plt.colorbar()
    # plt.title("episode"+str(episode))
    
    # myxlable = [str(int((x-1)/3)) for x in range(0, MAZE_W*3-1) if (x-1)%3 == 0]
    # post_list_x = [x for x in range(0, MAZE_W*3-1) if (x-1)%3 == 0]
    # plt.xticks(post_list_x, myxlable)
    
    # myylable = [str(int((x-1)/3)) for x in range(0, MAZE_H*3-1) if (x-1)%3 == 0]
    # post_list_y = [x for x in range(0, MAZE_H*3-1) if (x-1)%3 == 0]
    # plt.yticks(post_list_y, myylable)


    # 以2为间隔
    myxlable = [str(int((x-1)/3)) for x in range(0, MAZE_W*3-1) if (x-1)%6 == 0]
    post_list_x = [x for x in range(0, MAZE_W*3-1) if (x-1)%6 == 0]
    plt.xticks(post_list_x, myxlable)
    
    myylable = [str(int((x-1)/3)) for x in range(0, MAZE_H*3-1) if (x-1)%6 == 0]
    post_list_y = [x for x in range(0, MAZE_H*3-1) if (x-1)%6 == 0]
    plt.yticks(post_list_y, myylable)

    plt.savefig(
        fname="my/picture/"+str(time)+"/"+str(episode)+".jpeg")
    plt.clf()