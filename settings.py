import pygame as pg
from math import cos, sin, radians, degrees, atan2, radians
import random
import time
pg.init()

DIS_SIZE = DIS_W, DIS_H = 800, 700
DISPLAY = pg.display.set_mode((DIS_W, DIS_H))

EVENT = []
