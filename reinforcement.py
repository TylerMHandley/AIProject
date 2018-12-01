def Q(state, action, map):
    x, y = state[0], state[1] 
    if action == "north":
        
    if action == "south":
        
    if action == "east":
        
    if action == "west":
        
        
def reinforcement(ah, agent_pos, enemy_pos, grid, map):
    map_size = len(map)
    q_map = [ [0.0 for i in range(0,int(map_size))] for j in range(0,int(map_size))]