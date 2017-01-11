## Pyxel ##
from tkinter import Tk, Canvas, Label, StringVar
from PIL import Image
from PIL.ImageTk import PhotoImage

import time
import math

DEFAULT_WIDTH = 400
DEFAULT_HEIGHT = 400

########################
##                    ##
##     Game Class     ##
##                    ##
########################

class Game:

    def __init__(self, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT, title="Pyxel Game"):
        self.window = Tk()                          # Create a new window
        self.window.title(title)                    # Set the window title
        
        self.window_width = width
        self.window_height = height
    
        self.canvas = Canvas(self.window, width=self.window_width, height=self.window_height, background='black')
        self.canvas.pack()
        
        self.current_scene = Scene() # Empty Scene
        self.running = False
        
        ## TODO make this canvas text
        self.status_text = StringVar()
        self.status_bar = Label(self.window, textvariable=self.status_text)
        
        self.status_bar.place(x=0, y=0)
        
        self.MAX_SAMPLE = 60
        self.status_text.set( "fps: 0" )
        self.fps_history = [1] * self.MAX_SAMPLE
        
        buffer = Image.new('RGBA', (self.window_width, self.window_height))
        buffer.paste('black', (0,0, self.window_width, self.window_height))
        self.buffer = PhotoImage( buffer )
        self.buffer_id = self.canvas.create_image((self.window_width//2, self.window_height//2), image=self.buffer)
        ## TODO ##
        # register listeners #
        self.window.protocol("WM_DELETE_WINDOW", self.stop)
        
        self.mouse_x = 0
        self.mouse_y = 0
        self.window.bind('<Motion>', self._update_mouse)
        
        
    def start(self):
        self.running = True
        #self.window.mainloop()
        self.gameloop()
        
    def stop(self):
        self.running = False
        
    def gameloop(self):
        time_since_last_frame = time.clock()
        while self.running:
            now = time.clock()
            delta = now - time_since_last_frame
            if delta >= 0.033: # ~30fps    #0.0166: # ~60fps
                time_since_last_frame = time.clock()
                self.window.after_idle(self._update)
                self.window.after_idle(self._draw)
                self.fps_history = self.fps_history[1:]
                self.fps_history.append(delta)
                
                self.window.after_idle(self.status_text.set,  "fps: {fps:.1f}".format(fps = 1 / (sum(self.fps_history) / self.MAX_SAMPLE)) )
                
            self.window.update()

        ##########################
        ## Close button clicked ##
        ##########################
        self.window.destroy()
        
    def set_scene(self, scene):
        self.current_scene = scene
        self.current_scene.set_viewport(self.window_width, self.window_height)
        
    def _update_mouse(self, event):
        self.mouse_x = event.x
        self.mouse_y = event.y
        
    def _update(self):
        self.current_scene.update()
        
    def _draw(self):
        #st = time.clock()
        scene_image = self.current_scene._draw()#self.buffer)
        #dr = time.clock()
        self.buffer = PhotoImage(scene_image)
        #pi = time.clock()
        self.canvas.itemconfigure( self.buffer_id, image=self.buffer )
        #ic = time.clock()
        #print("Total: {:.5f}    draw: {:.5f}    Pbuff: {:.5f}   Configure: {:.5f}".format(ic-st, dr-st, pi-dr, ic-pi))

        
########################
##                    ##
##    Scene Class     ##
##                    ##
########################

class Scene:

    def __init__(self, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT, ambient_light=255):
        self.width = width
        self.height = height 
        self.viewport_width = 0
        self.viewport_height = 0
        
        self.viewport_x = 0
        self.viewport_y = 0
        
        self.sprites = []
        self.tiles = []

        self.graph = []
        
        self._scene_image = Image.new('RGBA', (self.width, self.height))
        
        self.ambient_light = ambient_light
        
        # TODO: replace this with light sources generated at sprite creation
        #       or provided as part of a sprite sheet.
        self.medium_light = self.generate_lightsource(radius=80, ambient=self.ambient_light)
        
        self.buffer = None
        self.mask = None
        self.darkness = None
        
    def set_viewport(self, width, height):
        if width > self.width:
            self.viewport_width = self.width
        else:
            self.viewport_width = width
        if height > self.height:
            self.viewport_height = self.height
        else:
            self.viewport_height = height
            
        self.darkness = Image.new('RGBA', (self.viewport_width, self.viewport_height))
        self.darkness.paste('black')
        
        self.mask = Image.new('L', (self.viewport_width, self.viewport_height))
        self.mask.paste(self.ambient_light)
        
        self.buffer = Image.new('RGBA', (self.viewport_width, self.viewport_height))
        self.buffer.paste('black')
        
        self.viewport_x = 0
        self.viewport_y = 0
        self.viewport_x_prev = 0
        self.viewport_y_prev = 0
        
    def add_sprite(self, sprite):
        self.sprites.append(sprite)
        
        self.graph.append(sprite)
        pos = sprite.get_position()
        self._scene_image.paste(sprite.image, (pos[0]-self.viewport_x, pos[1]-self.viewport_y), sprite.image)
            
    def add_tile(self, tile):
        self.tiles.append(tile)
        
        self.graph.append(tile)
        pos = tile.get_position()
        self._scene_image.paste(tile.image, (pos[0]-self.viewport_x, pos[1]-self.viewport_y), tile.image )
        
    def centre_on(self, item):
        self.viewport_x_prev = self.viewport_x
        self.viewport_y_prev = self.viewport_y
    
        self.viewport_x = item.x - self.viewport_width // 2
        self.viewport_y = item.y - self.viewport_height // 2
        
        if self.viewport_x < 0:
            self.viewport_x = 0
        if self.viewport_y < 0:
            self.viewport_y = 0
            
        if self.viewport_x + self.viewport_width > self.width:
            self.viewport_x = self.width - self.viewport_width
        if self.viewport_y + self.viewport_height > self.height:
            self.viewport_y = self.height - self.viewport_height
        
    def generate_lightsource(self, radius=200, ambient=0):
        image = Image.new('L', (radius*2, radius*2))
        
        for y in range(radius*2):
            for x in range(radius*2):
            
                delta = math.sqrt( (x - radius) ** 2 + (y - radius) ** 2 )
                if delta >= radius:
                    alpha = 0
                else:
                    step = (255-ambient) / radius     # TODO: Is this actually right? light should also fall off in square
                    alpha = 255 - int(delta * step)
            
                image.putpixel((x, y), alpha)
        return image
        
    def item_is_visible(self, item):
        # TODO: should use get_position to incorporate z
        return (item.x+item.width > self.viewport_x and item.x-item.width < self.viewport_x+self.viewport_width and
                item.y+item.height > self.viewport_y and item.y-item.height < self.viewport_y+self.viewport_height)
                
                
    def update(self):
        for item in self.graph:
            item.update()
            
        self.graph = sorted(self.graph)

        
    def _draw(self):
        vi = filter(self.item_is_visible, self.graph)
        visible_items = sorted(vi, reverse=True)
        
        self.mask.paste(self.ambient_light) # Draw new ambient light value
        x = self.viewport_x
        y = self.viewport_y
        #self.buffer = self._scene_image.crop( (x, y, x+self.viewport_width, y+self.viewport_height) )
        #self.buffer.paste( self._scene_image.crop( (self.viewport_x, self.viewport_y, self.viewport_x+self.viewport_width, self.viewport_y+self.viewport_height) ) )

        for item in visible_items:
            #item.update()
            if item.light_radius > 0:
                # TODO: This needs to be blended better. Custom paste 
                #self.mask.paste(self.medium_light, (item.x-self.viewport_x-self.medium_light.size[0]//2, item.y-self.viewport_y-self.medium_light.size[1]//2), self.medium_light)
                self.mask.paste(self.medium_light, (item.x-x-self.medium_light.size[0]//2, item.y-y-self.medium_light.size[1]//2), self.medium_light)
            
            if item.redraw:
                redraw = filter(item.is_touching, visible_items)
                #redraw.append(item)
                redraw = sorted(redraw)
                
                for r in redraw:
                    #print(type(r), r.x, r.y, r.z, r.y-r.z*r.height)
                    pos = r.get_position()
                    self.buffer.paste(r.image, (pos[0]-x, pos[1]-y), r.image )
                    #r.redraw = False
                #pos = item.get_position()
                #self.buffer.paste( item.image, (pos[0]-x, pos[1]-y), item.image )
            item.redraw = False
            #pos = item.get_position()
            #self.buffer.paste( item.image, (pos[0]-x, pos[1]-y), item.image )
        
        #self._scene_image.paste(self.buffer, (x, y))
        
        return Image.composite(self.buffer, self.darkness, self.mask)
        
        
########################
##                    ##
## SpriteSheet Class  ##
##                    ##
########################

class SpriteSheet:
    
    def __init__(self, image_path=None, image=None, frame_width=16, frame_height=16, scale=1):
            
        if image_path:
            image = Image.open(image_path)
            image = image.resize( (image.size[0] * scale, image.size[1] * scale), Image.NEAREST)
            
        self.frame_width = frame_width * scale
        self.frame_height = frame_height * scale
        
        self.frames = []
        
        if image:
            for y in range(image.size[1] // self.frame_height):
                for x in range(image.size[0] // self.frame_width):
                    box = (x * self.frame_width, y * self.frame_height, 
                           x * self.frame_width + self.frame_width, y * self.frame_height + self.frame_height)
      
                    self.frames.append( image.crop( box ) )
                    
    def __iter__(self):
        return self.frames.__iter__()
        
    def __getitem__(self, key):
        return self.frames.__getitem__(key)
        
    def __len__(self):
        return len(self.frames)

        
########################
##                    ##
##    Sprite Class    ##
##                    ##
########################

class Sprite:

    def __init__(self, frames=None, image=None, x=0, y=0, z=0, scale=1, frame_duration=0.08):
        self.x = x
        self.y = y
        self.z = z
        
        self.id = None
        
        self.redraw = True
        
        self.frames = frames
        
        if image:
            self.frames = [image]
            
        self.frame_count = len(self.frames)
        
        self.frame = 0
        self.image = self.frames[self.frame]
        self.animation_timer = time.clock()
        self.frame_duration = frame_duration
        
        self.width = self.image.size[0]
        self.height = self.image.size[1]
        
        self.light_radius = 0
        
    def update(self):
        if self.frame_count > 1:
            ts = time.clock()
            if ts - self.animation_timer >= self.frame_duration:
                self.frame += 1
                if self.frame >= self.frame_count:
                    self.frame = 0
                self.image = self.frames[self.frame]
                self.redraw = True
                self.animation_timer = ts
    
    def get_position(self):
        z = self.z-1
        if z < 0:
            z=0
        return (self.x-self.width//2, self.y-z*self.height-self.height//2)
        
    def is_touching(self, item): # TODO: I think the box is the wrong size
        #box = (item.x-self.width, (item.y-self.height)-(item.z*item.height), item.x+self.width*2, item.y+self.height*2)
        if self is item:
            return True
        d = 1
        item_pos = item.get_position()
        self_pos = self.get_position()
        box = ( item_pos[0], item_pos[1], item_pos[0]+item.width, item_pos[1]+item.height)
        return ( (self_pos[0]-d > box[0] and self_pos[0]-d < box[2] and self_pos[1]-d > box[1] and self_pos[1]-d < box[3]) or
                 (self_pos[0]+self.width+d > box[0] and self_pos[0]+self.width+d < box[2] and self_pos[1]-d > box[1] and self_pos[1]-d < box[3]) or
                 (self_pos[0]+self.width+d > box[0] and self_pos[0]+self.width+d < box[2] and self_pos[1]+self.height+d > box[1] and self_pos[1]+self.height+d < box[3]) or
                 (self_pos[0]-d > box[0] and self_pos[0]-d < box[2] and self_pos[1]+self.height+d > box[1] and self_pos[1]+self.height+d < box[3]) )
        #return self.x+1 > box[0] and self.y+1 > box[1] and self.x-1 < box[2] and self.y-1 < box[3]
                
    def _set_id(self, id):
        self.id = id
        
    def __lt__(self, other):
        if self.y+(self.z*self.height) == other.y+(other.z*self.height):
            return self.x < other.x
        return self.y+(self.z*self.height) < other.y+(other.z*self.height)
        
# Alias for Sprite. I like the distinction and eventually sprites and tiles 
# could be different.
class Tile(Sprite):
    pass
    #def __init__(self, frames=None, image=None, x=0, y=0, z=0, scale=1, frame_duration=0.08):
    #    super().__init__(frames=frames, image=image, x=x, y=y, z=z, frame_duration=frame_duration)
