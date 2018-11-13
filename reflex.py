from __future__ import print_function
from __future__ import division

from builtins import range
from past.utils import old_div
import MalmoPython
import json
import logging
import math
import os
import random
import sys
import time
import re
import uuid
from collections import namedtuple
from operator import add
from random import *
import numpy as np


def reflex(agent, agent_position, enemy_position, grid):
    legalgrid = legalMoves(grid)
    x, y = agent_position
    north_score  = -math.inf
    north_break_score = -math.inf
    south_score  = -math.inf
    south_break_score = -math.inf
    east_score  = -math.inf
    east_break_score = -math.inf
    west_score = -math.inf
    west_break_score = -math.inf
    if len(legalgrid) == 0:
        print("Banzai")
        badgrid = badMoves(grid)
        return choice(badgrid), 0
    if "north" in legalgrid:
        new_pos = (x, y - 1)
        north_score = chooseAction("north", agent, new_pos, enemy_position, grid)

        north_break_score = chooseBreak(agent, new_pos, enemy_position, grid)
    if "south" in legalgrid:
        new_pos = (x, y + 1)
        south_score = chooseAction("south", agent, new_pos, enemy_position, grid)
        south_break_score = chooseBreak(agent, new_pos, enemy_position, grid)
    if "west" in legalgrid:
        new_pos = (x - 1, y)
        west_score = chooseAction("west", agent, new_pos, enemy_position, grid)
        west_break_score = chooseBreak(agent, new_pos, enemy_position, grid)
    if "east" in legalgrid:
        new_pos = (x + 1, y)
        east_score = chooseAction("east", agent, new_pos, enemy_position, grid)
        east_break_score = chooseBreak(agent, new_pos, enemy_position, grid)
    
    scores = [north_score, south_score, west_score, east_score]
    breakscores = [north_break_score, south_break_score, west_break_score, east_break_score]
    direction = ["north", "south", "west", "east"]
    max = (-math.inf, "")
    for i in range(0, len(scores)):
        if scores[i] > max[0]:
            max = (scores[i], direction[i])
        if scores[i] == max[0]:
            max = (scores[i], choice([max[1], direction[i]]))
    breakmax = (-math.inf, "")
    breaksecond = (-math.inf, 0)
    for i in range(0, len(breakscores)):
        temp = breakmax[0]
        tempdirection = breakmax[1]
        if breakscores[i] > breakmax[0]:
            breakmax = (breakscores[i], direction[i])
        if len(breakscores) >= 2:
            if temp < breakmax[0]:
                breaksecond = (temp, tempdirection)
            elif breakscores[i] > breaksecond[0]:
                breaksecond = (breakscores[i], direction[i])


    index = 0
    if breakmax[1] == max[1] and manhattan_distance(agent_position, enemy_position) <= 4:
        # if breaksecond[1] == 'north':
            # index = 1
        # elif breaksecond[1] == 'south':
            # index = 3
        # elif breaksecond[1] == 'east':
            # index = 2
        # elif breaksecond[1] == 'west':
            # index = 4
        #print(index)
        return max[1], breaksecond[1]
    elif breakmax[1] != max[1] and manhattan_distance(agent_position, enemy_position) <= 4:
        # if breakmax[1] == 'north':
            # index = 1
        # elif breakmax[1] == 'south':
            # index = 3
        # elif breakmax[1] == 'east':
            # index = 2
        # elif breakmax[1] == 'west':
            # index = 4
        return max[1], breakmax[1]
    else:
        #print(max[0], max[1], "true")
        return max[1], 0

def chooseAction(direction, agent, pos, enemy_pos,grid):
    x = [pos[0], pos[1]]
    x[0] = int(x[0])
    x[1] = int(x[1])

    maximum = 0
    if direction == 'north':
        if grid[0] != u'snow':
            maximum -=1
        if grid[2] != u'snow':
            maximum -=1
    elif direction == 'south':
        if grid[6] != u'snow':
            maximum -=1
        if grid[8] != u'snow':
            maximum -=1
    elif direction == 'east':
        if grid[2] != u'snow':
            maximum -=1
        if grid[4] != u'snow':
            maximum -=1
    elif direction == 'west':
        if grid[4] != u'snow':
            maximum -=1
        if grid[6] != u'snow':
            maximum -=1
    if manhattan_distance(pos, enemy_pos) == 0:
        maximum -= 100
    elif manhattan_distance(pos, enemy_pos) == 1:
        maximum -= 3
    else:
        maximum += 1 + 20 / manhattan_distance(pos, enemy_pos)
    #print(direction, maximum, manhattan_distance(pos, enemy_pos))
    return maximum

def chooseBreak(agent, pos, enemy_pos,grid):
    time.sleep(0.1)
    x = [pos[0], pos[1]]
    x[0] = int(x[0])
    x[1] = int(x[1])

    maximum = 10

    if manhattan_distance(pos, enemy_pos) == 0:
        maximum += 100
    elif manhattan_distance(pos, enemy_pos) == 1:
        maximum += 3
    else:
        maximum += 2 / manhattan_distance(pos, enemy_pos)

    return maximum

def manhattan_distance(start, end):
    sx, sy = start
    ex, ey = end
    return abs(ex - sx) + abs(ey - sy)


def legalMoves(grid):
    blocks = []

    if grid[3] == u'snow':
        blocks.append("west")
    if grid[1] == u'snow':
        blocks.append("north")
    if grid[5] == u'snow':
        blocks.append("east")
    if grid[7] == u'snow':
        blocks.append("south")
    return blocks


def badMoves(grid):
    blocks = []

    if grid[3] != u'stone':
        blocks.append("west")
    if grid[1] != u'stone':
        blocks.append("north")
    if grid[5] != u'stone':
        blocks.append("east")
    if grid[7] != u'stone':
        blocks.append("south")
    return blocks