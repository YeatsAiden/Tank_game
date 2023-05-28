from settings import *
import settings
from player import Player
import text

# initialize permanent variables
player = Player()

camera = [0, 0]

font = text.Font("assets/fonts/font.png", 1)

clock = pg.time.Clock()
FPS = 60  # bcz my potato laptop cannot handle 100 fps

while True:
    keys_pressed = pg.key.get_pressed()
    dt = clock.tick(FPS)/1000

    settings.event = pg.event.get()
    for event in settings.event:
        if event.type == pg.QUIT:
            pg.quit()
            quit()

    # update gamestate
    player.move(keys_pressed, dt)

    camera[0] += (player.pos[0] - camera[0])/10
    camera[1] += (player.pos[1] - camera[1])/10

    pg.display.set_caption(f"FPS: {clock.get_fps()}, cam_pos: {camera}")

    # update the screen
    DISPLAY.fill((250, 250, 250))

    player.draw(DISPLAY, camera)


    pg.display.update()



