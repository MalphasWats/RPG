from pyxel_tk import *
import random

WIDTH = 720#400
HEIGHT = 512#320
SCALE = 2

class Orc(Sprite):

    def __init__(self, frames=None, image=None, x=0, y=0, z=0, scale=1, frame_duration=0.08):
        super().__init__(frames, image, x, y, z, scale, frame_duration)
        
        self.direction = 1
        self.light_radius = 0#35
        
        self.tether_x = x
        self.tether_y = y
    
    def update(self):
        super().update()
        
        self.x += 3 * self.direction
        max_x = self.tether_x+200
        if max_x > WIDTH:
            max_x = WIDTH
        min_x = self.tether_x-200
        if min_x < 0:
            min_x = 0
            
        if self.x > max_x or self.x < min_x:
            self.direction *= -1
        self.redraw = True
        #scene1.centre_on(self)
        
        
class Wiz(Sprite):

    def __init__(self, frames=None, image=None, x=0, y=0, z=0, scale=1, frame_duration=0.08):
        super().__init__(frames, image, x, y, z, scale, frame_duration)
        
        self.direction = 1
        self.light_radius = 50
    
    def update(self):
        super().update()
        
        self.y += ( 2 * self.direction )
        if self.y > 200-self.height or self.y < 32+self.height:
            #self.y = 0
            self.direction *= -1
            
        scene1.centre_on(self)
        self.redraw = True


my_game = Game(width=WIDTH, height=HEIGHT)

scene1 = Scene(width=WIDTH*2, height=HEIGHT*2, ambient_light=96)
#scene1 = Scene(width=32*8, height=32*8, ambient_light=164)

sprite_sheet = SpriteSheet(image_path='tiles.png', frame_width=16, frame_height=16, scale=SCALE)

sprite = Wiz(frames=sprite_sheet[50:54], x=4*32, y=90, z=1)
scene1.add_sprite(sprite)

sprite = Orc(image=sprite_sheet[42], x=2*32, y=1*32, z=1)
scene1.add_sprite(sprite)

for i in range(10):
    sprite = Orc(image=sprite_sheet[40], x=random.randint(0, WIDTH), y=random.randint(0, HEIGHT), z=1)
    scene1.add_sprite(sprite)

for y in range((HEIGHT*2)//(16 * SCALE)):
    for x in range((WIDTH*2)//(16 * SCALE)):
        if random.randint(0, 1000) % 9 == 0:
            tile = Tile(image=sprite_sheet[1], x=x*(16*SCALE)+16, y=y*(16*SCALE)+16)
        else:
            tile = Tile(image=sprite_sheet[0], x=x*(16*SCALE)+16, y=y*(16*SCALE)+16)
        scene1.add_tile(tile)
        
"""for y in range((32*8)//(16 * SCALE)):
    for x in range((32*8)//(16 * SCALE)):
        if random.randint(0, 1000) % 9 == 0:
            tile = Tile(image=sprite_sheet[1], x=x*(16*SCALE)+16, y=y*(16*SCALE)+16)
        else:
            tile = Tile(image=sprite_sheet[0], x=x*(16*SCALE)+16, y=y*(16*SCALE)+16)
        scene1.add_tile(tile)"""
        
tile = Tile(image=sprite_sheet[20], x=96+16, y=256+16, z=1)
scene1.add_tile(tile)
tile = Tile(image=sprite_sheet[21], x=96+16+(16*SCALE), y=256+(8*SCALE), z=1)
scene1.add_tile(tile)

tile = Tile(image=sprite_sheet[10], x=96+16, y=256+(8*SCALE), z=2)
scene1.add_tile(tile)
tile = Tile(image=sprite_sheet[11], x=96+16+32, y=256+(8*SCALE), z=2)
scene1.add_tile(tile)


tile = Tile(image=sprite_sheet[20], x=64+16, y=128+16, z=1)
scene1.add_tile(tile)
tile = Tile(image=sprite_sheet[21], x=64+16+32, y=128+16, z=1)
scene1.add_tile(tile)

tile = Tile(image=sprite_sheet[10], x=64+16, y=128+16, z=2)
scene1.add_tile(tile)
tile = Tile(image=sprite_sheet[11], x=64+16+32, y=128+16, z=2)
scene1.add_tile(tile)

tile = Tile(image=sprite_sheet[9], x=192+16+32, y=256+16, z=1)
tile.light_radius = 1
scene1.add_tile(tile)

my_game.set_scene(scene1)

my_game.start() # This Blocks.

# Cleanup?