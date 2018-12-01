from __future__ import print_function


from builtins import range
import MalmoPython
import json
import logging
import math
import os
import random
import sys
import time
import malmoutils
import expectimax
import minimax
import reflex
import hiddenMarkov
import randomagent
import smartrandomagent
import AStarReflex
    
def run(size, algo1, algo2):    
    #algorithms = {"reflex": reflex.reflex, "hiddenMarkov": hiddenMarkov.hiddenMarkov, "minimax":minimax.minimax, "expectimax": expectimax.expectimax}
    algorithms = {"reflex": reflex.reflex, 'random': randomagent.randommove, 'smartrandom': smartrandomagent.randommove, 'astarreflex': AStarReflex.search}
    #assert len(sys.argv) == 4, "Wrong number of arguments, the form is: mapSize, agent algorithm, enemy alogrithm" 




    malmoutils.fix_print()

    # -- set up two agent hosts --
    agent_host1 = MalmoPython.AgentHost()
    agent_host2 = MalmoPython.AgentHost()
    #map_size = str(sys.argv[1])
    map_size = int(size)
    map_minus = str(map_size - 1)
    agentAlgo = algorithms[algo1]
    enemyAlgo = algorithms[algo2]
    #agentAlgo =  algorithms[sys.argv[2]]
    #enemyAlgo = algorithms[sys.argv[3]]

    # Use agent_host1 for parsing the command-line options.
    # (This is why agent_host1 is passed in to all the subsequent malmoutils calls, even for
    # agent 2's setup.)
    malmoutils.parse_command_line(agent_host1)


    missionXML='''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
                <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                
                  <About>
                    <Summary>Hello world!</Summary>
                  </About>
                  
                  <ServerSection>
                    <ServerInitialConditions>
                      <Time>
                        <StartTime>12000</StartTime>
                        <AllowPassageOfTime>false</AllowPassageOfTime>
                      </Time>
                    </ServerInitialConditions>
                    <ServerHandlers>
                      <FlatWorldGenerator generatorString="3;7,220*1,5*3,2;3;,biome_1"/>
                      <DrawingDecorator>
                        <!-- coordinates for cuboid are inclusive -->
                        <DrawCuboid x1="0" y1="45" z1="0" x2=''' + '"' + map_minus + '"' + ''' y2="300" z2=''' + '"'+ map_minus + '"'+  ''' type="air" />            <!-- limits of our arena -->
                        <DrawCuboid x1="0" y1="40" z1="0" x2='''+ '"'+ map_minus + '"'+ ''' y2="44" z2='''+ '"'+ map_minus+ '"' +''' type="lava" />           <!-- lava floor -->
                        <DrawCuboid x1="0"  y1="46" z1="0"  x2='''+ '"'+ map_minus  + '"'+ ''' y2="46" z2='''+ '"'+ map_minus + '"' +''' type="snow" />
                      </DrawingDecorator>
                      <ServerQuitFromTimeUp timeLimitMs="30000"/>
                      
                    </ServerHandlers>
                  </ServerSection>
                  
                  <AgentSection mode="Survival">
                    <Name>Agent</Name>
                    <AgentStart>
                        <Inventory>
                            <InventoryItem slot="0" type="diamond_shovel"/>
                        </Inventory>
                        <Placement x="0.5" y="47.0" z="0.5" pitch="50" yaw="0"/>
                    </AgentStart>
                    <AgentHandlers>
                      <ObservationFromFullStats/>
                      <ObservationFromGrid>
                          <Grid name="floor3x3W">
                            <min x="-1" y="0" z="-1"/>
                            <max x="1" y="0" z="1"/>
                          </Grid>
                          <Grid name="floor3x3F">
                            <min x="-1" y="-1" z="-1"/>
                            <max x="1" y="-1" z="1"/>
                          </Grid>
                      </ObservationFromGrid>
                      <DiscreteMovementCommands/>
                    </AgentHandlers>
                  </AgentSection>
                  
                  <AgentSection mode="Survival">
                    <Name>Enemy</Name>
                    <AgentStart>
                        <Inventory>
                            <InventoryItem slot="0" type="diamond_shovel"/>
                        </Inventory>
                        <Placement x='''+ '"'+ str(float(map_size) - 0.5) + '"'+ ''' y="47.0" z='''+ '"'+ str(float(map_size) - 0.5)+ '"'+ ''' pitch="50" yaw="180"/>
                    </AgentStart>
                    
                    <AgentHandlers>
                      <ObservationFromFullStats/>
                      <DiscreteMovementCommands/>
                      <ObservationFromGrid>
                          <Grid name="floor3x3W">
                            <min x="-1" y="0" z="-1"/>
                            <max x="1" y="0" z="1"/>
                          </Grid>
                          <Grid name="floor3x3F">
                            <min x="-1" y="-1" z="-1"/>
                            <max x="1" y="-1" z="1"/>
                          </Grid>
                      </ObservationFromGrid>
                      <RewardForTouchingBlockType>
                        <Block reward="-100.0" type="lava" behaviour="onceOnly"/>
                      </RewardForTouchingBlockType>
                      <AgentQuitFromTouchingBlockType>
                        <Block type="lava" />
                      </AgentQuitFromTouchingBlockType>
                    </AgentHandlers>
                  </AgentSection>
                </Mission>'''

    # Create default Malmo objects:
    my_mission = MalmoPython.MissionSpec(missionXML, True)

    client_pool = MalmoPython.ClientPool()
    client_pool.add( MalmoPython.ClientInfo('127.0.0.1',10000) )
    client_pool.add( MalmoPython.ClientInfo('127.0.0.1',10001) )

    MalmoPython.setLogging("", MalmoPython.LoggingSeverityLevel.LOG_OFF)
    my_mission_record = MalmoPython.MissionRecordSpec()

    def safeStartMission(agent_host, mission, client_pool, recording, role, experimentId):
        used_attempts = 0
        max_attempts = 5
        print("Calling startMission for role", role)
        while True:
            try:
                agent_host.startMission(mission, client_pool, recording, role, experimentId)
                break
            except MalmoPython.MissionException as e:
                errorCode = e.details.errorCode
                if errorCode == MalmoPython.MissionErrorCode.MISSION_SERVER_WARMING_UP:
                    print("Server not quite ready yet - waiting...")
                    time.sleep(2)
                elif errorCode == MalmoPython.MissionErrorCode.MISSION_INSUFFICIENT_CLIENTS_AVAILABLE:
                    print("Not enough available Minecraft instances running.")
                    used_attempts += 1
                    if used_attempts < max_attempts:
                        print("Will wait in case they are starting up.", max_attempts - used_attempts, "attempts left.")
                        time.sleep(2)
                elif errorCode == MalmoPython.MissionErrorCode.MISSION_SERVER_NOT_FOUND:
                    print("Server not found - has the mission with role 0 been started yet?")
                    used_attempts += 1
                    if used_attempts < max_attempts:
                        print("Will wait and retry.", max_attempts - used_attempts, "attempts left.")
                        time.sleep(2)
                else:
                    print("Other error:", e.message)
                    print("Waiting will not help here - bailing immediately.")
                    exit(1)
            if used_attempts == max_attempts:
                print("All chances used up - bailing now.")
                exit(1)
        print("startMission called okay.")

    def safeWaitForStart(agent_hosts):
        print("Waiting for the mission to start", end=' ')
        start_flags = [False for a in agent_hosts]
        start_time = time.time()
        time_out = 120  # Allow two minutes for mission to start.
        while not all(start_flags) and time.time() - start_time < time_out:
            states = [a.peekWorldState() for a in agent_hosts]
            start_flags = [w.has_mission_begun for w in states]
            errors = [e for w in states for e in w.errors]
            if len(errors) > 0:
                print("Errors waiting for mission start:")
                for e in errors:
                    print(e.text)
                print("Bailing now.")
                exit(1)
            time.sleep(0.1)
            print(".", end=' ')
        print()
        if time.time() - start_time >= time_out:
            print("Timed out waiting for mission to begin. Bailing.")
            exit(1)
        print("Mission has started.")

    safeStartMission(agent_host1, my_mission, client_pool, my_mission_record, 0, '' )
    safeStartMission(agent_host2, my_mission, client_pool, my_mission_record, 1, '' )
    safeWaitForStart([agent_host1, agent_host2])

    def movement(ah, direction, pos):
        if direction == "north":
            ah.sendCommand("movenorth 1")
            position = (pos[0], pos[1]-1)
        if direction == "south":
            ah.sendCommand("movesouth 1")
            position = (pos[0], pos[1]+1)
        if direction == "west":
            ah.sendCommand("movewest 1")
            position = (pos[0]-1, pos[1])
        if direction == "east":
            ah.sendCommand("moveeast 1")
            position = (pos[0]+1, pos[1])
        time.sleep(0.1)
        return position
    def attack(ah, index, pos, map, enemy=False):
        #We are going to make it so the agent can only break the blocks immediately around them. 
        #So a location will be one of the 8 locations around it  
        #Enemy starts facing north (1), Agent starts facing south (3)
        #  Enemy: 0 1 0  Agent: 0 3 0
        #         4 X 2         2 X 4
        #         0 3 0         0 1 0
        x,y = math.floor(pos[0]),math.floor(pos[1])
        #print("Player position: {},{} Direction: {}".format(x,y, index))
        did_Break = False
        if enemy:
            if index =="north":
                # print("Index 1")
                ah.sendCommand("attack 1")
                time.sleep(0.1)
                y-=1
                did_Break = True
            if index =="east":
                # print("Index 2")
                ah.sendCommand("turn 1")
                time.sleep(0.1)
                ah.sendCommand("attack 1")
                time.sleep(0.1)
                ah.sendCommand("turn -1")
                time.sleep(0.1)
                x+=1
                did_Break = True
            if index == "west":
                # print("Index 4")
                ah.sendCommand("turn -1")
                time.sleep(0.1)
                ah.sendCommand("attack 1")
                time.sleep(0.1)
                ah.sendCommand("turn 1")
                time.sleep(0.1)
                x-=1
                did_Break = True
            if index == "south":
                # print("Index 3")
                ah.sendCommand("turn 1")
                time.sleep(0.1)
                ah.sendCommand("turn 1")
                time.sleep(0.1)
                ah.sendCommand("attack 1")
                time.sleep(0.1)
                ah.sendCommand("turn -1")
                time.sleep(0.1)
                ah.sendCommand("turn -1")
                time.sleep(0.1)
                y+=1
                did_Break = True
        else:
            # Agent: 0 3 0
            #        2 X 4
            #        0 1 0
            if index =="south":
                # print("Index 3")
                ah.sendCommand("attack 1")
                time.sleep(0.1)
                y+=1
                did_Break = True
            if index =="west":
                # print("Index 4")
                ah.sendCommand("turn 1")
                time.sleep(0.1)
                ah.sendCommand("attack 1")
                time.sleep(0.1)
                ah.sendCommand("turn -1")
                time.sleep(0.1)
                x-=1
                did_Break = True
            if index == "east":
                # print("Index 2")
                ah.sendCommand("turn -1")
                time.sleep(0.1)
                ah.sendCommand("attack 1")
                time.sleep(0.1)
                ah.sendCommand("turn 1")
                time.sleep(0.1)
                x+=1
                did_Break = True
            if index == "north":
                # print("Index 3")
                ah.sendCommand("turn 1")
                time.sleep(0.1)
                ah.sendCommand("turn 1")
                time.sleep(0.1)
                ah.sendCommand("attack 1")
                time.sleep(0.1)
                ah.sendCommand("turn -1")
                time.sleep(0.1)
                ah.sendCommand("turn -1")
                time.sleep(0.1)
                y-=1
                did_Break = True
        if did_Break:
             map[x-1][y-1] = False

    '''
    Sample Observation:
    {"DistanceTravelled":0,"TimeAlive":50,"MobsKilled":0,"PlayersKilled":0,"DamageTaken":0,"DamageDealt":0,
    "Life":20.0,"Score":0,"Food":20,"XP":0,"IsAlive":true,"Air":300,"Name":"Enemy","XPos":5.5,"YPos":47.0,
    "ZPos":5.5,"Pitch":50.0,"Yaw":180.0,"WorldTime":12000,"TotalTime":57}

    '''

    agent_score = 0
    #count = 0
    agent_ob = None
    enemy_ob = None

    map = [ [True for i in range(0,int(map_size))] for j in range(0,int(map_size))]
    # for i in map:
        # print(i)

    while True:
        #Scores should decrease with time and get a bonus if they win
        agent_score-=1
        agent_state = agent_host1.peekWorldState()
        enemy_state = agent_host2.peekWorldState()
        if agent_state.number_of_observations_since_last_state > 0:
            agent_ob = json.loads(agent_state.observations[-1].text)

        if enemy_state.number_of_observations_since_last_state > 0:
            enemy_ob = json.loads(enemy_state.observations[-1].text)
        if agent_ob is None or enemy_ob is None:
            continue
        if agent_state.is_mission_running == False:
            break
        agent_position = (agent_ob["XPos"], agent_ob["ZPos"])
        enemy_position = (enemy_ob["XPos"], enemy_ob["ZPos"])
        
        agent_grid = agent_ob.get(u'floor3x3F', 0)
        enemy_grid = enemy_ob.get(u'floor3x3F', 0)
        
        if "lava" in agent_grid:
            print("Enemy Won!")
            agent_score-=100
            return 0
            break
        if "lava" in enemy_grid:
            print("Agent Won!")
            agent_score+=100
            return 1
            break
        
        
        agentMoveString, agentBreakIndex = agentAlgo(agent_host1, agent_position, enemy_position, agent_grid, map)
        enemyMoveString, enemyBreakIndex = enemyAlgo(agent_host2, enemy_position, agent_position, enemy_grid, map)
        
        # #Agent Turn to Break
        attack(agent_host1, agentBreakIndex, agent_position, map)
        # #Enemy Turn to Move
        pos = movement(agent_host2, enemyMoveString, enemy_position)
        
        # #Enemy Turn to Break
        attack(agent_host2, enemyBreakIndex, pos, map, enemy=True)
        # #Agent Turn to Move
        movement(agent_host1, agentMoveString, agent_position)
    for i in map:
        print(i)
    return 2

