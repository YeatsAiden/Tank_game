import pygame as pg
from math import cos, sin, radians, degrees, atan2, radians, dist, acos
import random
import time
import pandas
import asyncio

# Trust me bro I'm an engineer 😎
# ok

pg.init()

DIS_SIZE = DIS_W, DIS_H = 480, 320
DISPLAY = pg.display.set_mode((DIS_W, DIS_H), flags=pg.SCALED | pg.RESIZABLE)
pg.display.set_caption("driftin'n'tankin")

pg.mouse.set_visible(False)

EVENT = []

DRAWING_COEFICIENT = 1
TILE_SIZE = 8

FPS = 60
COLLISION_LAYERS = ["walls", "barriers"]
INVISIBLE_LAYERS = ["spawns"]
VISIBLE_LAYERS = ["walls, barriers", "floor"]

# loading all sfx
BIG_CHUNGUS = pg.mixer.Sound("assets/sounds/big_chungus.wav")
CRASHING = pg.mixer.Sound("assets/sounds/crashing.wav")
DEATH = pg.mixer.Sound("assets/sounds/death.wav")
DESTRUCTION_OF_TURRET = pg.mixer.Sound("assets/sounds/destruction_of_turret.wav")
EL_BOMBE = pg.mixer.Sound("assets/sounds/el_bombe.wav")
HURT = pg.mixer.Sound("assets/sounds/hurt.wav")
KILL = pg.mixer.Sound("assets/sounds/kill.wav")
MINI_TURRET = pg.mixer.Sound("assets/sounds/mini_turret.wav")
MINIGUN = pg.mixer.Sound("assets/sounds/minigun.wav")
NORMAL_CANNON = pg.mixer.Sound("assets/sounds/normal_cannon.wav")
# Le Music
MUSIC = pg.mixer.music.load("assets/sounds/a_song.wav")

