import pygame as pg
from math import cos, sin, radians, degrees, atan2, radians, dist
import random
import time
pg.init()

DIS_SIZE = DIS_W, DIS_H = 800, 700
DISPLAY = pg.display.set_mode((DIS_W, DIS_H))

FPS = 60  # bcz my potato laptop cannot handle 100 fps
clock = pg.time.Clock()

EVENT = []


def calculate_angle_to_point(point1, point2):
    x_change = point1[0] - point2[0]
    y_change = point1[1] - point2[1]

    return degrees(atan2(-y_change, x_change))
