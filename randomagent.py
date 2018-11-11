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


def randommove(agent, agent_position, enemy_position, grid):
    time.sleep(0.1)
    
    legalgrid = legalMoves(grid)
    try:
        random = choice(legalgrid)
    except:
        print("Banzai")
        badgrid = badMoves(grid)
        return choice(badgrid), 0
    randomindex = 0
    if len(legalgrid) != 0:
        randomindex2 = choice(legalgrid)
        if len(legalgrid) == 1 or random == randomindex2:
            randomindex = 0
        elif randomindex2 == 'north':
            randomindex = 1
        elif randomindex2 == 'south':
            randomindex = 3
        elif randomindex2 == 'east':
            randomindex = 2
        elif randomindex2 == 'west':
            randomindex = 4
    return random, randomindex

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