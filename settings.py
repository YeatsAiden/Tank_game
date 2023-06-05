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


def clip_img(surf, x, y, width, height):
    # It makes clips of all your FAILURES
    img_copy = surf.copy()
    clip_rect = pg.Rect(x, y, width, height)
    img_copy.set_clip(clip_rect)
    return img_copy.subsurface(img_copy.get_clip())


def calculate_angle_to_point(point1, point2):
    x_change = point1[0] - point2[0]
    y_change = point1[1] - point2[1]

    return degrees(atan2(-y_change, x_change))


def calculate_smallest_angle(A, B):
    # given angles A and B find the smallest value to append to angle A and make it become angle B
    diff = B - A
    diff = (diff + 180) % 360 - 180
    return diff

