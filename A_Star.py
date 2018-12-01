# Created by Minbiao Han and Roman Sharykin
# AI fall 2018
import heapq
from scipy.spatial import distance
def search(maze, start, end):

    ### Your code should go here ###
    h_maze = [[manhattan([i,ii], [end[0],end[1]]) for ii in range(0, len(maze[0]))] for i in range(0, len(maze))]
    closed = set()
    frindge =[  (h_maze[start[0]][start[1]], start, [start])  ]
    heapq.heapify(frindge)
    path = []
    num_nodes_expanded = 0
    while True:
        if len(frindge) == 0: 
            return False
        #node = frindge.pop()
        node = heapq.heappop(frindge)
        path = node[2]
        if node[1] == end:
            #print("A* implementation: {}".format(num_nodes_expanded))
            return path, num_nodes_expanded
        if node[1] not in closed:  
            i = node[1][0]
            j = node[1][1]
            #Below
            if maze[i+1][j] != "%" and (i+1, j) not in closed:
                #print("Adding node below")
                temp = path[:]
                temp.append((i+1,j))
                heapq.heappush(frindge, ( h_maze[i+1][j] + len(temp),(i+1,j), temp))
                num_nodes_expanded+=1
            #Left
            if maze[i][j-1] != "%" and (i, j-1) not in closed:
                #print("Adding node to the left")
                temp = path[:]
                temp.append((i,j-1))
                heapq.heappush(frindge, ( h_maze[i][j-1] + len(temp), (i,j-1), temp))
                num_nodes_expanded+=1
            #Right
            if maze[i][j+1] != "%" and (i, j+1) not in closed:
                #print("Adding node to the right")
                temp = path[:]
                temp.append((i,j+1))
                heapq.heappush(frindge, ( h_maze[i][j+1] + len(temp), (i,j+1), temp))
                num_nodes_expanded+=1
            #Above
            if maze[i-1][j] != "%" and (i-1, j) not in closed:
                #print("Adding node above")
                temp = path[:]
                temp.append((i-1,j))
                heapq.heappush(frindge, ( h_maze[i-1][j] + len(temp),(i-1,j), temp))
                num_nodes_expanded+=1
        closed.add(node[1])        
    
    
    
    
    
    
    
    ### Your search function should return the
    # path for the agent to take,
    # as well as the number of nodes your algorithm searches  ###

    return path, num_nodes_expanded

### feel free to add any aditional support functions for your search here ###

def manhattan(x,y):
    val = abs(x[0] - y[0])
    val += abs(x[1] - y[1])
    return val



