import json

map_source = {}
with open('my/map.json', 'r') as f:
    map_source = json.load(f)

MAZE_H = map_source['config']['height']  # grid height
MAZE_W = map_source['config']['width']  # grid width

MAP = map_source['map']

#   几种不同的地形
LAND_R = map_source['landform']['land']['reward']
SWAMP_R = map_source['landform']['swamp']['reward']
HELL_R = map_source['landform']['hell']['reward']
DESTINATION_R = map_source['landform']['destination']['reward']

class Maze():
    
    def __init__(self) -> None:
        self.height = MAZE_H
        self.width = MAZE_W
        self.action_space = ['u', 'd', 'l', 'r']
        self.n_actions = len(self.action_space)
        self.destination = ()
        self.hell = []
        self.swamp = []
        self.agent_coord = [0, 0]

    def build_maze(self):
        for x in range(0, MAZE_H):
            for y in range(0, MAZE_W):

                if MAP[x][y] == "S":
                    self.swamp += [[x, y]]
                if MAP[x][y] == "H":
                    self.hell += [[x, y]]
                if MAP[x][y] == "D":
                    self.destination = [x, y]
        print(self.destination)
        print(self.hell)
        print(self.swamp)

    def reset(self):
        self.agent_coord = [0, 0]
        return self.agent_coord.copy()

    def step(self, action):

        if action == 0:
            if self.agent_coord[0] > 0 :
                self.agent_coord[0] -= 1
        if action == 1:
            if self.agent_coord[0] < MAZE_H-1 :
                self.agent_coord[0] += 1
        if action == 2:
            if self.agent_coord[1] > 0 :
                self.agent_coord[1] -= 1
        if action == 3:
            if self.agent_coord[1] < MAZE_W-1 :
                self.agent_coord[1] += 1

        done = False
        if self.agent_coord in self.hell or self.agent_coord == self.destination:
            done = True
        reward_f = MAP[self.agent_coord[0]][self.agent_coord[1]]
        if reward_f == "H":
            reward = HELL_R
        if reward_f == "D":
            reward = DESTINATION_R
        if reward_f == "S":
            reward = SWAMP_R
        if reward_f == "L":
            reward = LAND_R

        return self.agent_coord.copy(), reward, done