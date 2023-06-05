import pygame as pg
from math import cos, sin, radians, degrees, atan2, radians, dist
import random
import time
import pandas

# Trust me bro I'm an engineer 😎
# ok

pg.init()

DIS_SIZE = DIS_W, DIS_H = 480, 320
DISPLAY = pg.display.set_mode((DIS_W, DIS_H), flags=pg.SCALED | pg.RESIZABLE)

pg.mouse.set_visible(False)

EVENT = []

DRAWING_COEFICIENT = 1
TILE_SIZE = 8

FPS = 60
COLLISION_LAYERS = ["walls"]

