import pygame as pg
from math import cos, sin, radians, degrees, atan2, radians
import random
import time
from pytmx.util_pygame import load_pygame
pg.init()

DIS_SIZE = DIS_W, DIS_H = 480, 320
DISPLAY = pg.display.set_mode((DIS_W, DIS_H), flags=pg.SCALED | pg.RESIZABLE)

pg.mouse.set_visible(False)

EVENT = []

DRAWING_COEFICIENT = 1
TILE_SIZE = 8

def clip_img(surf, x, y, width, height):
    # It makes clips of all your FAILURES
    img_copy = surf.copy()
    clip_rect = pg.Rect(x, y, width, height)
    img_copy.set_clip(clip_rect)
    return img_copy.subsurface(img_copy.get_clip())