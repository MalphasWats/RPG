## Pyxel ##
from OpenGL.GL import *
from OpenGL.GL import shaders
#from OpenGL.GLU  import *
from OpenGL.GLUT import *

from PIL import Image

import numpy

from datetime import datetime
import time
import sys

DEFAULT_WIDTH = 400
DEFAULT_HEIGHT = 400

########################
##                    ##
##     Game Class     ##
##                    ##
########################

class Game:

    def __init__(self, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT, title="Pyxel Game"):
        self.width = width
        self.height = height
        
        glutInit()  # If this fails, it's probably because pyOpenGL didn't install .dlls properly
        glutInitWindowSize(self.width, self.height)
        glutCreateWindow(bytes(title, 'utf-8')) # On windows, pyOpenGL doesn't like py3 strings :(
        
        # Just request them all and don't worry about it.
        #glutInitDisplayMode(GLUT_DOUBLE|GLUT_RGBA|GLUT_DEPTH)
        glutInitDisplayMode(GLUT_SINGLE|GLUT_RGBA|GLUT_DEPTH)
        
        glClearColor(0, 0, 0, 0)
        
        #glutReshapeFunc(self.reshape)      # TODO: resizing the window screws up mouse clicks.
        #glutKeyboardFunc(self.keyboard)
        glutDisplayFunc(self._draw)
        glutIdleFunc(self._update)
        
        glutMouseFunc(self._mouse)
        self.action_queue = []
        
        if sys.platform == 'darwin':
            glutWMCloseFunc(self.stop)
        
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        
        self.scene = Scene()
        self._clock = 0
        
    def start(self):
        self._clock = datetime.now()
        glutMainLoop()
        
    def stop(self):
        glutDestroyWindow(glutGetWindow())
        sys.exit(0)
        
    def set_active_scene(self, scene):
        self.scene = scene
        scene.set_viewport(self.width, self.height)
        
        # TODO: if scene already initialised, don't need to do this?
        scene._initialise_buffers()
        
    def _mouse(self, button, state, x, y):
        if button == 0 and state == 1:
            item = self.scene.get_top_item_at(x, y)
            if item:
                self.action_queue.append(item)
        
    def _update(self):
        ts = self.clock()
        self.scene.update()
        for item in self.action_queue:
            item.use()
        self.action_queue.clear()
        glutPostRedisplay()
        #print("updated in: {:.6f}".format(self.clock() - ts))
        
    def _draw(self):
        ts = self.clock()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # Clear all pixels.
        
        self.scene._draw()
        #glutSwapBuffers()
        #glutPostRedisplay()
        
        glFlush()
        #print("drawn in: {}".format(self.clock() - ts))
        
    def clock(self):
        delta = datetime.now() - self._clock
        return delta.total_seconds() * 1000

        
########################
##                    ##
##    Scene Class     ##
##                    ##
########################

class Scene:

    def __init__(self, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT, sprite_sheet=None):
        self.width = width
        self.height = height 
        self.viewport_width = self.width
        self.viewport_height = self.height
        
        self.viewport_x = 0
        self.viewport_y = 0
        
        self.sprites = []
        self.tiles = []
        
        #self.graph = []
        
        self.sprite_sheet = sprite_sheet
        if not self.sprite_sheet:
            self.sprite_sheet = SpriteSheet()
        
        self.shader_program = self.build_shader()
        
        glUseProgram(self.shader_program)
        
        self.transform_matrix = glGetUniformLocation(self.shader_program, 't_matrix')
        
        self.tile_vertex_buffer = None
        self.tile_texture_buffer = None
        self.sprite_vertex_buffer = None
        self.sprite_texture_buffer = None
        
        self.tile_vertex_count = 0
        self.sprite_vertex_count = 0
        
        self.ambient_light_uniform = glGetUniformLocation(self.shader_program, 'ambient_light')
        self.ambient_light = [0.15, 0.15, 0.15]#[0.8, 0.8, 0.8]#[0.3, 0.3, 0.3]
        
        self.light_positions_uniform = glGetUniformLocation(self.shader_program, 'light_positions')
        self.light_positions = [-0.4, 0.3, 
                                0.1, 0.3,
                                0.1, -0.3]
        
        self.tile_vertex_array = None
        self.tile_tex_coord_array = None
        self.sprite_vertex_array = None
        self.sprite_tex_coord_array = None
        
        self.tilemap = {}
        
        self.viewport_matrix = [
                                    1, 0, 0, self.viewport_x * 2.0 / self.width,
                                    0, 1, 0, self.viewport_y * 2.0 / self.height,
                                    0, 0, 1, 0, 
                                    0, 0, 0, 1,
                                ]
        
    def build_shader(self):
        vertex_shader = shaders.compileShader("""
            attribute vec3 a_position;
            attribute vec2 a_texCoords;
            
            uniform mat4 t_matrix;
            
            varying vec2 v_texCoords;
            varying vec2 v_position;
            
            void main() 
            { 
                gl_Position = t_matrix * vec4(a_position, 1.0);
                
                v_position = a_position.xy;                
                v_texCoords = a_texCoords;
            }
        """, GL_VERTEX_SHADER)
        
        fragment_shader = shaders.compileShader("""
            uniform sampler2D u_image;
        
            varying vec2 v_texCoords;
            varying vec2 v_position;
            
            uniform vec3 ambient_light;
            
            uniform vec2 light_positions[3];
            vec2 point_light_pos = vec2(-0.4, 0.3);//, 0.0);
            vec3 point_light_col = vec3(0.65, 0.65, 0.65); //vec3(1.0, 1.0, 1.0);
            float point_light_intensity = 0.65;
        
            void main() 
            {
                vec4 frag_color = texture2D(u_image, v_texCoords);
                if(frag_color.a < 1.0)
                  discard;
                
                float diffuse = 0.0;
                float distance; 
                for (int i=0 ; i<3 ; i++)
                {
                    //distance = abs(distance(point_light_pos, v_position));
                    distance = distance(light_positions[i], v_position);
                    
                    if (distance < point_light_intensity)
                    {
                        //diffuse =  max(diffuse, (1.0 - distance / point_light_intensity));
                        diffuse +=  (1.0 - distance / point_light_intensity);
                    }    
                }
                //float diffuse = abs(1.0 - distance(point_light_pos, v_position.xyz));
                //gl_FragColor = vec4(frag_color.rgb * ambient_light, 1.0);
                
                gl_FragColor = vec4(min(frag_color.rgb * ((point_light_col * diffuse) + ambient_light), frag_color.rgb), 1.0);
            }
        """, GL_FRAGMENT_SHADER)
        
        return shaders.compileProgram(vertex_shader, fragment_shader)
        
    def set_viewport(self, width, height):
        self.viewport_width = width
        if self.viewport_width > self.width:
            self.viewport_width = self.width
            
        self.viewport_height = height
        if self.viewport_height > self.height:
            self.viewport_height = self.height
        
        self.viewport_x = 0
        self.viewport_y = 0
        
        self.viewport_matrix = [
                                    1, 0, 0, self.viewport_x * 2.0 / self.viewport_width,
                                    0, 1, 0, self.viewport_y * 2.0 / self.viewport_height,
                                    0, 0, 1, 0,
                                    0, 0, 0, 1,
                                ]
        
    def centre_viewport(self, x, y):
        x = -x+self.viewport_width//2
        y = y-self.viewport_height//2
        if x > 0:
            x = 0
        if y < 0:
            y = 0
        if x - self.viewport_width < -self.width:
            x = -self.width + self.viewport_width
        if y + self.viewport_height > self.height:
            y = self.height - self.viewport_height
        self.viewport_x = x
        self.viewport_y = y
        
        self.viewport_matrix = [
                                    1, 0, 0, self.viewport_x * 2.0 / self.viewport_width,
                                    0, 1, 0, self.viewport_y * 2.0 / self.viewport_height,
                                    0, 0, 1, 0, 
                                    0, 0, 0, 1,
                                ]
        
        
    def add_sprite(self, sprite):
        self.sprites.append(sprite)
        
        #self.graph.append(sprite)
            
    def add_tile(self, tile):
        self.tiles.append(tile)
        
        d = tile.z // tile.height
        col = tile.x // tile.width
        row = (tile.y-tile.z) // tile.height
        
        try:
            self.tilemap[d][(col, row)] = tile
        except KeyError:
            self.tilemap[d] = {}
            self.tilemap[d][(col, row)] = tile
        #self.graph.append(tile)
        
    def get_top_item_at(self, x, y):
        # TODO: I think this might be faster with the new tilemap?
        x -= self.viewport_x
        y += self.viewport_y
        def item_is_at(x, y, item):
            return item.x < x and item.y-item.z < y and item.x+item.width > x and item.y-item.z+item.height > y
        
        items = filter(lambda i: item_is_at(x, y, i), self.tiles)
        max_z = -1
        top_item = None
        for item in items:
            if item.z > max_z:
                top_item = item
                max_z = item.z
        return top_item
        
    def find_path(self, item, destination):
        # TODO: Implement ramps / stairs / etc
        depth = item.z // item.height
        
        s_col = item.x // item.width
        s_row = (item.y-item.z) // item.height
        
        d_col = destination.x // item.width
        d_row = (destination.y-destination.z) // item.height
        
        cols = self.width // item.width         # TODO: When the Scene is VERY large, this takes
        rows = self.height // item.height       # AGES because it looks through everything. Needs
                                                # to be limited to just current viewport.
        
        max_distance = cols + rows + 1
        
        open_nodes = [ [None for r in range(rows)] for c in range(cols) ]
        closed_nodes = [ [None for r in range(rows)] for c in range(cols) ]
        
        def crow_flies(from_node, to_node):
            return abs(to_node[0]-from_node[0]) + abs(to_node[1]-from_node[1])
            
        col = s_col
        row = s_row
        
        step = 0
        
        while not ( col == d_col and row == d_row):
            moore_neighbourhood = []
            
            if col > 0:
                moore_neighbourhood.append( (col-1, row) )
                if row > 0:
                    moore_neighbourhood.append( (col-1, row-1) )
            if col < cols - 1:
                moore_neighbourhood.append( (col+1, row) )
                if row < rows - 1:
                    moore_neighbourhood.append( (col+1, row+1) )
            if row > 0:
                moore_neighbourhood.append( (col, row-1) )
                if col < cols - 1:
                    moore_neighbourhood.append( (col+1, row-1) )
            if row < rows - 1:
                moore_neighbourhood.append( (col, row+1) )
                if col > 0:
                    moore_neighbourhood.append( (col-1, row+1) )
                    
            for node in moore_neighbourhood:
                c = node[0]
                r = node[1]
                
                # TODO: should probably check that depth is in tilemap earlier?
                if ( depth not in self.tilemap or 
                     (c, r) not in self.tilemap[depth] ) and not closed_nodes[c][r] :
                        # TODO: Want to have 'path' tiles, so need feature to modify score per tile
                        #       so that the algo favours walking on paths when present
                        score = step + 1 + crow_flies( (c, r), (d_col, d_row) )
                        
                        open_nodes[c][r] = {'parent': (col, row), 'G': step+1, 'score': score}
                        
            best_node = {'node': None, 'parent': None, 'score': max_distance, 'G': 0}
            for c in range(cols):
                for r in range(rows):
                    if open_nodes[c][r] and open_nodes[c][r]['score'] < best_node['score']:
                        best_node['node'] = (c, r)
                        best_node['parent'] = open_nodes[c][r]['parent']
                        best_node['score'] = open_nodes[c][r]['score']
                        best_node['G'] = open_nodes[c][r]['G']
            
            if not best_node['node']:
                return None             # No route found.
                
            open_nodes[best_node['node'][0]][best_node['node'][1]] = None
            
            col = best_node['node'][0]
            row = best_node['node'][1]
            step = best_node['G'];
        
            closed_nodes[col][row] = {'parent': best_node['parent']};
            
        # Path has been found. Construct it
        path = []
        current_node = closed_nodes[col][row]
        
        path.insert(0, (col*item.width, row*item.height+item.z) )
        while( not (col == s_col and row == s_row) ):
            col = current_node['parent'][0]
            row = current_node['parent'][1]
            path.insert(0, (col*item.width, row*item.height+item.z) )
            current_node = closed_nodes[col][row]
        
        return path
        
    def convert_to_ndc(self, x, y, z):
        return [ x * 2.0 / self.viewport_width - 1,
                 2.0 - ((y-z) * 2.0 / self.viewport_height) - 1,
                 2.0 - (y * 2.0 / self.height) - 1 - 0.0000001, ]
        
    def update(self):
        
        # TODO: implement tile animation (but needs cleverness to stop being slow)
        #for tile in self.tiles:
        #    tile.update()
            
        vertices = []
        tex_coords = []
        for sprite in self.sprites:
            sprite.update()
            # Normalised Device Coordinates (I think. Seems to work anyway).
            # TODO: these calculations should be cached.
            x1, y1, z = self.convert_to_ndc(sprite.x, sprite.y-sprite.height//2, sprite.z)
            x2, y2, _ = self.convert_to_ndc(sprite.x+sprite.width, sprite.y+sprite.height-sprite.height//2, sprite.z)
            
            vertices.extend([x1,     y1,     z,
                             x2,     y1,     z,
                             x1,     y2,     z,
                             x1,     y2,     z,
                             x2,     y1,     z,
                             x2,     y2,     z, ])
            
            tex_coords.extend( self.sprite_sheet[sprite.frame] )
        
        # TODO: modify self.sprite_vertex_array etc, directly for items that need redraw    
        self.sprite_vertex_array = numpy.array(vertices, numpy.float32)
        self.sprite_tex_coord_array = numpy.array(tex_coords, numpy.float32)
        
        # TODO: only buffer things that have changed.
        glBindBuffer(GL_ARRAY_BUFFER, self.sprite_vertex_buffer)
        glBufferSubData(GL_ARRAY_BUFFER, 0, self.sprite_vertex_array.nbytes, self.sprite_vertex_array)
        
        glBindBuffer(GL_ARRAY_BUFFER, self.sprite_texture_buffer)
        glBufferSubData(GL_ARRAY_BUFFER, 0, self.sprite_tex_coord_array.nbytes, self.sprite_tex_coord_array)

    def _initialise_buffers(self):
        self.sprite_sheet.activate()
        
        # Create buffers somewhere else to allow reuse of scenes.
        ( self.tile_vertex_buffer, 
          self.tile_texture_buffer, 
          self.sprite_vertex_buffer, 
          self.sprite_texture_buffer ) = glGenBuffers(4)

        vertices = []
        tex_coords = []

        for tile in self.tiles:
            # Normalised Device Coordinates (I think. Seems to work anyway).
            x1, y1, z = self.convert_to_ndc(tile.x, tile.y, tile.z)
            x2, y2, _ = self.convert_to_ndc(tile.x+tile.width, tile.y+tile.height, tile.z)
            
            vertices.extend([x1,     y1,     z,
                             x2,     y1,     z,
                             x1,     y2,     z,
                             x1,     y2,     z,
                             x2,     y1,     z,
                             x2,     y2,     z, ])
                                
            tex_coords.extend( self.sprite_sheet[tile.frame] )
            
            self.tile_vertex_count += 6
        
        self.tile_vertex_array = numpy.array(vertices, numpy.float32)
        self.tile_tex_coord_array = numpy.array(tex_coords, numpy.float32)
        
        glBindBuffer(GL_ARRAY_BUFFER, self.tile_vertex_buffer)
        glBufferData(GL_ARRAY_BUFFER, self.tile_vertex_array.nbytes, self.tile_vertex_array, GL_STATIC_DRAW)
        
        glBindBuffer(GL_ARRAY_BUFFER, self.tile_texture_buffer)
        glBufferData(GL_ARRAY_BUFFER, self.tile_tex_coord_array.nbytes, self.tile_tex_coord_array, GL_STATIC_DRAW)
        
        vertices = []
        tex_coords = []
        
        for sprite in self.sprites:
            # Normalised Device Coordinates (I think. Seems to work anyway).
            x1, y1, z = self.convert_to_ndc(sprite.x, sprite.y-sprite.height//2, sprite.z)
            x2, y2, _ = self.convert_to_ndc(sprite.x+sprite.width, sprite.y+sprite.height-sprite.height//2, sprite.z)
            
            vertices.extend([x1,     y1,     z,
                             x2,     y1,     z,
                             x1,     y2,     z,
                             x1,     y2,     z,
                             x2,     y1,     z,
                             x2,     y2,     z, ])
                                
            tex_coords.extend( self.sprite_sheet[sprite.frame] )
            
            self.sprite_vertex_count += 6
            
        self.sprite_vertex_array = numpy.array(vertices, numpy.float32)
        self.sprite_tex_coord_array = numpy.array(tex_coords, numpy.float32)
        
        glBindBuffer(GL_ARRAY_BUFFER, self.sprite_vertex_buffer)
        glBufferData(GL_ARRAY_BUFFER, self.sprite_vertex_array.nbytes, self.sprite_vertex_array, GL_DYNAMIC_DRAW)
        
        self.vertices = glGetAttribLocation(self.shader_program, 'a_position')
        glEnableVertexAttribArray(self.vertices)
        #glVertexAttribPointer(self.vertices, 3, GL_FLOAT, GL_FALSE, 0, None)
        
        glBindBuffer(GL_ARRAY_BUFFER, self.sprite_texture_buffer)
        glBufferData(GL_ARRAY_BUFFER, self.sprite_tex_coord_array.nbytes, self.sprite_tex_coord_array, GL_DYNAMIC_DRAW)
        
        self.tex_coords = glGetAttribLocation(self.shader_program, 'a_texCoords')
        glEnableVertexAttribArray(self.tex_coords)
        #glVertexAttribPointer(self.tex_coords, 2, GL_FLOAT, GL_TRUE, 0, None)
        
        glUniform3fv(self.ambient_light_uniform, 1, self.ambient_light)
        
        glUniform2fv(self.light_positions_uniform, 2, self.light_positions)
        
    def _draw(self):
        
        glUniformMatrix4fv(self.transform_matrix, 1, True, self.viewport_matrix)
        
        glBindBuffer(GL_ARRAY_BUFFER, self.sprite_vertex_buffer)
        glVertexAttribPointer(self.vertices, 3, GL_FLOAT, GL_FALSE, 0, None)
        
        glBindBuffer(GL_ARRAY_BUFFER, self.sprite_texture_buffer)
        glVertexAttribPointer(self.tex_coords, 2, GL_FLOAT, GL_TRUE, 0, None)
        
        glDrawArrays(GL_TRIANGLES, 0, self.sprite_vertex_count)
        
        
        glBindBuffer(GL_ARRAY_BUFFER, self.tile_vertex_buffer)
        #vertices = glGetAttribLocation(self.shader_program, 'a_position')
        #glEnableVertexAttribArray(self.vertices)
        glVertexAttribPointer(self.vertices, 3, GL_FLOAT, GL_FALSE, 0, None)
        glBindBuffer(GL_ARRAY_BUFFER, self.tile_texture_buffer)
        #tex_coords = glGetAttribLocation(self.shader_program, 'a_texCoords')
        #glEnableVertexAttribArray(self.tex_coords)
        glVertexAttribPointer(self.tex_coords, 2, GL_FLOAT, GL_TRUE, 0, None)
        
        
        glDrawArrays(GL_TRIANGLES, 0, self.tile_vertex_count)
        
########################
##                    ##
## SpriteSheet Class  ##    
##                    ## 
########################

class SpriteSheet:
    
    def __init__(self, image_path=None, frame_width=16, frame_height=16):
        
        self.frame_width = frame_width
        self.frame_height = frame_height
            
        if image_path:
            self.image = Image.open(image_path).transpose(Image.FLIP_TOP_BOTTOM)
            
            self.width, self.height = self.image.size
            self.image = self.image.tobytes("raw", "RGBA", 0, -1)
            
            self.frames = []
            
            for row in range(self.height // self.frame_height):
                for col in range(self.width // self.frame_width):
            
                    w = self.width / self.frame_width
                    h = self.height / self.frame_height
                
                    tex_x_step = 1 / w;
                    tex_y_step = 1 / h;
                
                    x = col*tex_x_step;
                    y = row*tex_y_step;
                
                    self.frames.append([
                        x, y,
                        x+tex_x_step, y,
                        x, y+tex_y_step,
                        x, y+tex_y_step,
                        x+tex_x_step, y,
                        x+tex_x_step, y+tex_y_step,
                    ])
            
        else:
            self.image = [255, 0, 255, 255]
            self.width = 1
            self.height = 1
            self.frames = [[0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1]]
            
        self.texture = glGenTextures(1)
        
    def activate(self):
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.width, self.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, self.image)
        
        glGenerateMipmap(GL_TEXTURE_2D)
        
    def __iter__(self):
        return self.frames.__iter__()
        
    def __getitem__(self, key):
        if key >= len(self):
            return self.frames.__getitem__(0)
        return self.frames.__getitem__(key)
        
    def __len__(self):
        return len(self.frames)

        
########################
##                    ##
##    Sprite Class    ##
##                    ##
########################

class Sprite:

    def __init__(self, x=0, y=0, z=0, width=16, height=16, frame=0, speed=128):
        self.x = x
        self.y = y
        self.z = z
        
        self.frame = frame
        
        self.width = width
        self.height = height
        
        self.speed = speed # pixels / second
        
        self.animations = {'idle': (5000, [frame], 1)}
        self.current_animation_name = 'idle'
        self.current_animation = self.animations[self.current_animation_name]
        self.animation_frame = 0
        #self.animation_length = 1
        
        self.animation_timer = time.clock()
        self._clock = datetime.now() #time.clock() #datetime.now()
        
        self.path = []
        self.destination = None
        self.move_timer = 0
        self.x_step_rem = 0
        self.y_step_rem = 0
        
    def add_animation(self, name, frames, frame_duration=120):
        self.animations[name] = (frame_duration, frames, len(frames))
        
    def set_animation(self, name):
        if name != self.current_animation_name:
            self.current_animation_name = name
            self.current_animation = self.animations[self.current_animation_name]
            self.animation_frame = 0
            self.frame = self.current_animation[1][self.animation_frame]
        #self.animation_length = self.current_animation[2]
        
    def update(self):
        if self.current_animation[2] > 1:
            ts = self.clock()
            if ts - self.animation_timer >= self.current_animation[0]:
                self.animation_timer = ts
                self.animation_frame += 1
                if self.animation_frame >= self.current_animation[2]:
                    self.animation_frame = 0
                self.frame = self.current_animation[1][self.animation_frame]
                
        if self.destination:
            now = self.clock()
            
            delta = now - self.move_timer
            
            step = self.speed / 1000 * delta + self.x_step_rem
            if step >= 1.0:
                fl_step = step//1
                self.x_step_rem = step - fl_step
                dx = self.x - self.destination[0]
                if abs(dx) < step:
                    fl_step = 1
                if dx != 0:
                    self.x -= int(fl_step // 1 * (dx / abs(dx)))
                    self.move_timer = now
            
            step = self.speed / 1000 * delta + self.y_step_rem
            if step >= 1.0:
                fl_step = step // 1
                self.y_step_rem = step - fl_step
                dy = self.y - self.destination[1]
                if abs(dy) < step:
                    fl_step = 1
                if dy != 0:
                    self.y -= int(fl_step // 1 * (dy / abs(dy)))
                    self.move_timer = now
            
            # TODO: This messes up on the bottom row :(
            if self.x == self.destination[0] and self.y == self.destination[1]:
                if len(self.path) > 0:
                    self.destination = self.path.pop(0)
                else:
                    self.destination = None
                    #print("took {:.1f} to move".format(self.clock() - self.start))
            
    def use(self):
        pass
            
    def set_path(self, path):
        self.path = path
        self.destination = self.path.pop(0)
        
        self.start = self.clock()
        
        
    
    def clock(self):
        #return (time.clock() - self._clock) * 1000
        delta = datetime.now() - self._clock
        return delta.total_seconds() * 1000
        
    def __repr__(self):
        return "<Sprite at x:{} y:{} z:{} frame:{}".format(self.x, self.y, self.z, self.frame)
        
# Alias for Sprite. I like the distinction and eventually sprites and tiles 
# could be different.
class Tile(Sprite):
    #def update(self):
    def __repr__(self):
        return "<Tile at x:{} y:{} z:{} frame:{}".format(self.x, self.y, self.z, self.frame)
