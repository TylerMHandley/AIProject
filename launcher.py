# This file just calls the malmo code over and over again for a 100 interations. This should be able to be done in 
# malmo itself but there was issues
import sys
import spleef
iterations = int(sys.argv[1])
map_size = str(sys.argv[2])
agentAlgo =  sys.argv[3]
enemyAlgo = sys.argv[4]
try:
    save = sys.argv[5]
except:
    save = False
agent_wins = 0.0
draws = 0.0
for i in range(1, iterations+1):
    print("\n\n----------------------------------------------")
    print("Running iteration: ", i)
    print("----------------------------------------------\n\n")
    val = spleef.run(map_size, agentAlgo, enemyAlgo)
    if val == 2:
        draws +=1
    else:
        agent_wins += val
chance = (agent_wins/iterations) * 100
draw_chance = (draws/iterations) * 100
string = "An agent with a {} algorithm has a win chance of {}% and a draw chance of {}% against an enemy with a {} algorithm".format(agentAlgo, chance, draw_chance, enemyAlgo)
print(string)
if save == "true":
    with open("results.txt", "a") as file:
        file.write(string)
    print("Save Complete")