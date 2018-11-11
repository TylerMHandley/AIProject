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


def reflex(agent, world_state, position, grid):
    time.sleep(0.1)
    illegalgrid = illegalMoves(world_state, grid)
    legalLST = ["right", "left", "forward", "back"]
    for x in illegalgrid:
        if x in legalLST:
            legalLST.remove(x)
    y = randint(0, len(legalLST) - 1)
    togo = legalLST[y]
    if togo == "right":
        moveRight(agent)

    elif togo == "left":
        moveLeft(agent)

    elif togo == "forward":
        moveStraight(agent)

    elif togo == "back":
        moveBack(agent)

    print("Called Reflex")

def moveRight(ah):
    ah.sendCommand("strafe 1")
    #print("I have moved right")
    time.sleep(0.1)


def moveLeft(ah):
    ah.sendCommand("strafe -1")
    #print("I have moved left")
    time.sleep(0.1)


def moveStraight(ah):
    ah.sendCommand("move 1")
    #print("I have moved Straight")
    time.sleep(0.1)


def moveBack(ah):
    ah.sendCommand("move -1")
    #print("I have moved back")
    time.sleep(0.1)

def illegalMoves(world_state, grid):
    blocks = []
    if world_state.number_of_observations_since_last_state > 0:
        #msg = world_state.observations[-1].text
        #observations = json.loads(msg)
        #grid = observations.get(u'floor3x3W', 0)
        print(grid)
        if grid[3] == u'stone':
            blocks.append("right")
        if grid[1] == u'stone':
            blocks.append("back")
        if grid[5] == u'stone':
            blocks.append("left")
        if grid[7] == u'stone':
            blocks.append("forward")

        return blocks
