from pyxel import *
import random

WIDTH = 704#720#1280
HEIGHT = 512#720

SIZE = 32

class Wiz(Sprite):

    def __init__(self, frame=0, x=0, y=0, z=0, width=32, height=32):
        super().__init__(frame=frame, x=x, y=y, z=z, width=width, height=height, speed=128)
        
        self.direction = -1
        self.destination = None
    
    def update(self):
        super().update()
        if len(my_game.action_queue) > 0:
            target_destination = my_game.action_queue[0]
            if self.z != target_destination.z: # shortcut to save pathfinding looking EVERYWHERE
                path = my_scene.find_path(self, target_destination)
                self.set_path( path )
                
        if self.destination:
            #print("x: {}  y: {}     to      x: {}  y: {}".format(self.x, self.y, self.destination[0], self.destination[1]))
            if self.y < self.destination[1]:
                wiz.set_animation('walk_down')
            elif self.y > self.destination[1]:
                wiz.set_animation('walk_up')
            elif self.x < self.destination[0]:
                wiz.set_animation('walk_right')
            elif self.x > self.destination[0]:
                wiz.set_animation('walk_left')
        else:
            wiz.set_animation('idle')
            
        my_scene.centre_viewport(self.x+self.width//2, self.y-self.height//2)
        
    """def set_destination(self, tile):
        self.destination = my_scene.find_path(self, tile)
        
        print(self.destination)"""
        # plot path
        
        
class Orc(Sprite):

    def __init__(self, frame=0, x=0, y=0, z=0, width=32, height=32, speed=64):
        super().__init__(frame=frame, x=x, y=y, z=z, width=width, height=height, speed=speed)
        
        self.patrol_start = Tile(frame=0, x=x, y=y, z=z, width=height, height=height)
        self.patrol_end = Tile(frame=0, x=x+256, y=y, z=z, width=height, height=height)
        self.destination = None
    
    def update(self):
        super().update()
        
        if self.x == self.patrol_start.x and self.y == self.patrol_start.y and not self.destination:
            path = my_scene.find_path(self.patrol_start, self.patrol_end)
            self.set_path (path)
        elif self.x == self.patrol_end.x and self.y == self.patrol_end.y and not self.destination:
            path = my_scene.find_path(self.patrol_end, self.patrol_start)
            self.set_path  (path)
            
    def __repr__(self):
        return "<Orc at x:{} y:{} z:{} frame:{}".format(self.x, self.y, self.z, self.frame)
        
    

class Rock(Tile):
    def use(self):
        if my_game.scene == my_scene:
            my_game.set_active_scene(my_scene_2)
        else:
            my_game.set_active_scene(my_scene)
        
    def use2(self):
        print("Hey! A Rock!")
    


my_game = Game(width=WIDTH, height=HEIGHT)

sprite_sheet = SpriteSheet(image_path='tiles.png')

my_scene = Scene(width=WIDTH*4, height=HEIGHT*4, sprite_sheet=sprite_sheet)



wiz = Wiz(x=128, y=192, z=1*SIZE, frame=50)
wiz.add_animation('walk_down', [50, 51, 52, 53])
wiz.add_animation('walk_up', [60, 61, 62, 63])
wiz.add_animation('walk_right', [70, 71, 72, 73])
wiz.add_animation('walk_left', [80, 81, 82, 83])
wiz.set_animation('idle')

my_scene.add_sprite(wiz)

orc = Orc(x=96, y=96, z=1*SIZE, frame=42, width=SIZE, height=SIZE)

my_scene.add_sprite(orc)

orc = Orc(x=256, y=256, z=1*SIZE, frame=42, width=SIZE, height=SIZE, speed=32)

my_scene.add_sprite(orc)

#for i in range(12):
#    sprite = Orc(frame=60, x=random.randint(0, WIDTH*4), y=random.randint(0, HEIGHT*4), z=1*SIZE, width=SIZE, height=SIZE)
#    my_scene.add_sprite(sprite)

for y in range((HEIGHT*4)//SIZE):
    for x in range((WIDTH*4)//SIZE):
        if random.randint(0, 1000) % 9 == 0:
            tile = Tile(frame=1, x=x*SIZE, y=y*SIZE, width=SIZE, height=SIZE)
        else:
            tile = Tile(frame=0, x=x*SIZE, y=y*SIZE, width=SIZE, height=SIZE)
        my_scene.add_tile(tile)
        

tile = Tile(frame=20, x=96, y=256, z=1*SIZE, width=SIZE, height=SIZE)
my_scene.add_tile(tile)
tile = Tile(frame=21, x=96+SIZE, y=256, z=1*SIZE, width=SIZE, height=SIZE)
my_scene.add_tile(tile)

tile = Tile(frame=10, x=96, y=256, z=2*SIZE, width=SIZE, height=SIZE)
my_scene.add_tile(tile)
tile = Tile(frame=11, x=96+SIZE, y=256, z=2*SIZE, width=SIZE, height=SIZE)
my_scene.add_tile(tile)


tile = Tile(frame=20, x=64, y=128, z=1*SIZE, width=SIZE, height=SIZE)
my_scene.add_tile(tile)
tile = Tile(frame=21, x=64+SIZE, y=128, z=1*SIZE, width=SIZE, height=SIZE)
my_scene.add_tile(tile)

tile = Tile(frame=10, x=64, y=128, z=2*SIZE, width=SIZE, height=SIZE)
my_scene.add_tile(tile)
tile = Tile(frame=11, x=64+SIZE, y=128, z=2*SIZE, width=SIZE, height=SIZE)
my_scene.add_tile(tile)

tile = Rock(frame=9, x=192, y=256, z=1*SIZE, width=SIZE, height=SIZE)
my_scene.add_tile(tile)

my_scene_2 = Scene(width=WIDTH, height=HEIGHT, sprite_sheet=sprite_sheet)
for y in range(HEIGHT//SIZE):
    for x in range(WIDTH//SIZE):
        if random.randint(0, 1000) % 9 == 0:
            tile = Tile(frame=3, x=x*SIZE, y=y*SIZE, width=SIZE, height=SIZE)
        else:
            tile = Tile(frame=2, x=x*SIZE, y=y*SIZE, width=SIZE, height=SIZE)
        my_scene_2.add_tile(tile)
        
tile = Rock(frame=9, x=192, y=256, z=1*SIZE, width=SIZE, height=SIZE)
my_scene_2.add_tile(tile)

my_scene_2.add_sprite(wiz)

my_game.set_active_scene(my_scene)
my_game.start() # This Blocks.

# Cleanup?