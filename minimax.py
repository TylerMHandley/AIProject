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

#CITATION for structure
#https://github.com/takeitallsource/berkeley-cs-188/blob/master/project-2/multiagent/multiAgents.py
#http://ai.berkeley.edu/multiagent.html#Q2

#For now will use eval func for reflex, but look into future moves
def minmax(agent, agent_position, enemy_position, grid, map):
	legalgrid = legalMoves(grid)
	x, y = agent_position
	trackScore = -math.inf
	north_score  = -math.inf
	south_score  = -math.inf
	east_score  = -math.inf
	west_score = -math.inf
	#placeholder "north"
	west_break_score = -math.inf
	east_break_score = -math.inf
	south_break_score = -math.inf
	north_break_score = -math.inf
	#This will just consider the scored that are calculated recursively, so that they 
	#are just kept track of and returned
	if "north" in legalgrid:
		new_pos = (x, y - 1)
		north_score = maxvalue( agent, new_pos, enemy_position,2, grid)
		north_break_score = chooseBreak(agent, new_pos, enemy_position, grid)
	if "south" in legalgrid:
		new_pos = (x, y + 1)
		south_score = maxvalue(agent, new_pos, enemy_position,2, grid)
		south_break_score = chooseBreak(agent, new_pos, enemy_position, grid)
	if "west" in legalgrid:
		new_pos = (x - 1, y)
		west_score = maxvalue(agent, new_pos, enemy_position,2, grid)
		west_break_score = chooseBreak(agent, new_pos, enemy_position, grid)
	if "east" in legalgrid:
		new_pos = (x + 1, y)
		east_score = maxvalue(agent, new_pos, enemy_position, 2,  grid)
		east_break_score = chooseBreak(agent, new_pos, enemy_position, grid)
	
	# for action in legalgrid:
	# 	oldScore = trackScore
	# 	#the 3 is the depth
	# 	trackScore = maxvalue(agent, agent_position, enemy_position, 0, grid)
	# 	if trackScore > oldScore:
	# 		direction = action

	scores = [north_score, south_score, west_score, east_score]
	direction = ["north", "south", "west", "east"]
	breakscores = [north_break_score, south_break_score, west_break_score, east_break_score]
	max = (-math.inf, "")
	for i in range(0, len(scores)):
		if scores[i] > max[0]:
			max = (scores[i], direction[i])
		if scores[i] == max[0]:
			max = (scores[i], choice([max[1], direction[i]]))
	#the breaking is temperorarly random, replace with the break function later.
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
		return max[1], breaksecond[1]
	elif breakmax[1] != max[1] and manhattan_distance(agent_position, enemy_position) <= 4:
		return max[1], breakmax[1]
	else:
		return max[1], 0
	return max[1], breakmax

def maxvalue(agent, agent_position, enemy_position, depth, grid):
	legalgrid = legalMoves(grid)
	x, y = agent_position
	if depth == 0 or len(legalgrid) == 0:
		return evalfunc(agent, agent_position,enemy_position, grid)
	var = -math.inf
	for action in legalgrid:
		new_pos=""
		if action == "north":
			new_pos = (x, y - 1)
		if action =="south":
			new_pos = (x, y + 1)
		if action == "west":
			new_pos = (x - 1, y)
		if action == "east":
			new_pos = (x + 1, y)
		var = max(var, minvalue(agent, new_pos, enemy_position, depth - 1, grid))
	return var

def minvalue(agent, agent_position, enemy_position, depth, grid):
	#This minimises the enemy move
	x, y = enemy_position
	legalgrid = legalMoves(grid)
	if depth == 0 or len(legalgrid) == 0:
		return evalfunc(agent, agent_position, enemy_position, grid)
	var = math.inf
	for action in legalgrid:
		new_pos=""
		if action == "north":
			new_pos = (x, y - 1)
		if action =="south":
			new_pos = (x, y + 1)
		if action == "west":
			new_pos = (x - 1, y)
		if action == "east":
			new_pos = (x + 1, y)
		var = min(var, maxvalue(agent, agent_position, new_pos, depth - 1, grid))
	return var

#The eval func can't return a number, but has to have a direction as well
def evalfunc(agent, agent_position,enemy_position, grid):
	legalgrid = legalMoves(grid)
	x, y = agent_position
	north_score  = -math.inf
	south_score  = -math.inf
	east_score  = -math.inf
	west_score = -math.inf
	if len(legalgrid) == 0:
		badgrid = badMoves(grid)
		return choice(badgrid)
	if "north" in legalgrid:
		new_pos = (x, y - 1)
		north_score = chooseAction("north", agent, new_pos, enemy_position, grid)
	if "south" in legalgrid:
		new_pos = (x, y + 1)
		south_score = chooseAction("south", agent, new_pos, enemy_position, grid)
	if "west" in legalgrid:
		new_pos = (x - 1, y)
		west_score = chooseAction("west", agent, new_pos, enemy_position, grid)
	if "east" in legalgrid:
		new_pos = (x + 1, y)
		east_score = chooseAction("east", agent, new_pos, enemy_position, grid)
	scores = [north_score, south_score, west_score, east_score]
	# direction = ["north", "south", "west", "east"]
	# max = (-math.inf, "")
	# for i in range(0, len(scores)):
	# 	if scores[i] > max[0]:
	# 		max = (scores[i], direction[i])
	# 	if scores[i] == max[0]:
	# 		max = (scores[i], choice([max[1], direction[i]]))
	return max(scores)	

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