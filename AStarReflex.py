# Created by Minbiao Han and Roman Sharykin
# AI fall 2018
import heapq
from scipy.spatial import distance
import reflex

def search(agent, agent_position, enemy_position, grid, map):
    ### Your code should go here ###
    if (manhattan(agent_position, enemy_position) >= 4):
        h_map = [[manhattan([i, ii], [int(enemy_position[0]), int(enemy_position[1])]) for ii in range(0, len(map[0]))] for i in range(0, len(map))]
        closed = set()
        print(len(map[0]), len(map[1]))
        print(int(agent_position[0]))
        frindge = [(h_map[int(agent_position[0])][int(agent_position[1])], (int(agent_position[0]), int(agent_position[1])), [(int(agent_position[0]), int(agent_position[1]))])]
        heapq.heapify(frindge)
        path = []
        num_nodes_expanded = 0
        while True:
            if len(frindge) == 0:
                return "none", 0
            # node = frindge.pop()
            node = heapq.heappop(frindge)
            path = node[2]
            if node[1][0] == int(enemy_position[0]) and node[1][1] == int(enemy_position[1]):
                # print("A* implementation: {}".format(num_nodes_expanded))
                if path[1][0] - int(agent_position[0]) == 0:
                    if path[1][1] - int(agent_position[1]) == 1:
                        return "south", 0
                    else:
                        return "north", 0
                elif path[1][0] - int(agent_position[0]) == -1:
                    return "west", 0
                else:
                    return "east", 0

            if node[1] not in closed:
                i = node[1][0]
                j = node[1][1]
                # Below
                if i+1 < len(map):
                    if map[i + 1][j] != "False" and (i + 1, j) not in closed:
                        # print("Adding node below")
                        temp = path[:]
                        temp.append((i + 1, j))
                        heapq.heappush(frindge, (h_map[i + 1][j] + len(temp), (i + 1, j), temp))
                        num_nodes_expanded += 1
                # Left
                if j-1 >=0:
                    if map[i][j - 1] != "False" and (i, j - 1) not in closed:
                        # print("Adding node to the left")
                        temp = path[:]
                        temp.append((i, j - 1))
                        heapq.heappush(frindge, (h_map[i][j - 1] + len(temp), (i, j - 1), temp))
                        num_nodes_expanded += 1
                # Right
                if j+1 < len(map):
                    if map[i][j + 1] != "False" and (i, j + 1) not in closed:
                        # print("Adding node to the right")
                        temp = path[:]
                        temp.append((i, j + 1))
                        heapq.heappush(frindge, (h_map[i][j + 1] + len(temp), (i, j + 1), temp))
                        num_nodes_expanded += 1
                # Above
                if i-1 >= 0:
                    if map[i - 1][j] != "False" and (i - 1, j) not in closed:
                        # print("Adding node above")
                        temp = path[:]
                        temp.append((i - 1, j))
                        heapq.heappush(frindge, (h_map[i - 1][j] + len(temp), (i - 1, j), temp))
                        num_nodes_expanded += 1

            closed.add(node[1])
    else:
        reflex.reflex(agent, agent_position, enemy_position, grid, map)

### feel free to add any aditional support functions for your search here ###

def manhattan(x, y):
    val = abs(x[0] - y[0])
    val += abs(x[1] - y[1])
    return val
