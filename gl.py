from OpenGL.GL import *
from OpenGL.GL import shaders
#from OpenGL.GLU  import *
from OpenGL.GLUT import *

from PIL import Image

import numpy

#import time
from datetime import datetime#, timedelta
import math
import sys
import random

_clock = datetime.now()

width = 1280
height = 720
depth = height

tile_width = 32
tile_height = 32
tile_depth = tile_height

texture = None
tex_coords = []

VBO = None
shader_program = None

wiz_y = 0
wiz_t = 0

counter = 0

def clock():
    dt = datetime.now() - _clock
    ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
    return ms



def stop():
    glutDestroyWindow(glutGetWindow())
    sys.exit(0)
    
def draw():
    st = clock()
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # Clear all pixels.
    
    glBindBuffer(GL_ARRAY_BUFFER, sprite_buffer)
    #glBufferData(GL_ARRAY_BUFFER, nvertices.nbytes, nvertices, GL_DYNAMIC_DRAW)
    vertices = glGetAttribLocation(shader_program, 'a_position')
    glEnableVertexAttribArray(vertices)
    glVertexAttribPointer(vertices, 3, GL_FLOAT, GL_FALSE, 0, None)

   

    glBindBuffer(GL_ARRAY_BUFFER, sprite_tex_buf)
    #glBufferData(GL_ARRAY_BUFFER, ntexture.nbytes, ntexture, GL_DYNAMIC_DRAW)
    tex = glGetAttribLocation(shader_program, 'a_texCoords')
    glEnableVertexAttribArray(tex)
    glVertexAttribPointer(tex, 2, GL_FLOAT, GL_TRUE, 0, None)
    
    glDrawArrays(GL_TRIANGLES, 0, 6*2)
    
    #glDepthMask(GL_FALSE)
    
    glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)
    vertices = glGetAttribLocation(shader_program, 'a_position')
    glEnableVertexAttribArray(vertices)
    glVertexAttribPointer(vertices, 3, GL_FLOAT, GL_FALSE, 0, None)
    glBindBuffer(GL_ARRAY_BUFFER, tex_buffer)
    tex = glGetAttribLocation(shader_program, 'a_texCoords')
    glEnableVertexAttribArray(tex)
    glVertexAttribPointer(tex, 2, GL_FLOAT, GL_TRUE, 0, None)
    glDrawArrays(GL_TRIANGLES, 0, 6*((width//tile_width)+1)*((height//tile_height)+1)+(6*4))#6*2)
    
    #drtl = time.clock()
    
    #glDepthMask(GL_FALSE)
    
    """glBindBuffer(GL_ARRAY_BUFFER, sprite_buffer)
    #glBufferData(GL_ARRAY_BUFFER, nvertices.nbytes, nvertices, GL_DYNAMIC_DRAW)
    vertices = glGetAttribLocation(shader_program, 'a_position')
    glEnableVertexAttribArray(vertices)
    glVertexAttribPointer(vertices, 3, GL_FLOAT, GL_FALSE, 0, None)

   

    glBindBuffer(GL_ARRAY_BUFFER, sprite_tex_buf)
    #glBufferData(GL_ARRAY_BUFFER, ntexture.nbytes, ntexture, GL_DYNAMIC_DRAW)
    tex = glGetAttribLocation(shader_program, 'a_texCoords')
    glEnableVertexAttribArray(tex)
    glVertexAttribPointer(tex, 2, GL_FLOAT, GL_TRUE, 0, None)
    glDrawArrays(GL_TRIANGLES, 0, 6*3)"""
    
    
    
    
    
    
    
    #glDrawElements(GL_TRIANGLES, 6*(width//tile_width)*(height//tile_height), GL_UNSIGNED_INT, None)
    #glDrawElements(GL_TRIANGLES, 6 * 4, GL_UNSIGNED_INT, None)
    """glDrawElements(
     GL_TRIANGLES,      # mode
     6, #width//tile_width * height//tile_height,    # count
     GL_UNSIGNED_INT,   # type
     0           # element array buffer offset
    )"""
    
    #glutSwapBuffers()
    glutPostRedisplay()
    glFlush()
    sp = clock()
    print("Draw Time: {:.6f}".format(sp-st))
    
def update():
    st = clock()
    global wiz_y, wiz_t
    #print(st - wiz_t)
    if st - wiz_t < 16.66667:
        return
    sprites = []
    #spr_tex = []

    x = 1*tile_width+16+16
    y = wiz_y#*tile_height
    
    x1, y1, z1 = convert_to_ndc(x, y, 1*tile_depth)
    x2, y2, z2 = convert_to_ndc(x+32, y+32, 1*tile_depth)
    sprites.extend([x1,     y1,     z1, 
                    x2,     y1,     z1,
                    x1,     y2,     z1,
                    x1,     y2,     z1,
                    x2,     y1,     z1,
                    x2,     y2,     z1 ])
    #print("wiz: {}".format(z1))


    #spr_tex.extend( tex_coords[50] )
    
    x = 2*tile_width+16
    y = 3*tile_height#+16#+16
    
    x1, y1, z1 = convert_to_ndc(x, y+4, 1*tile_depth)
    x2, y2, z2 = convert_to_ndc(x+32, y+32, 1*tile_depth)
    sprites.extend([x1,     y1,     z1, 
                    x2,     y1,     z1,
                    x1,     y2,     z1,
                    x1,     y2,     z1,
                    x2,     y1,     z1,
                    x2,     y2,     z1 ])
    #print("orc: y: {}, z: {}".format(y1, z1))

    nvertices = numpy.array(sprites, numpy.float32)
    #ntextures = numpy.array(spr_tex, numpy.float32)

    glBindBuffer(GL_ARRAY_BUFFER, sprite_buffer)
    glBufferData(GL_ARRAY_BUFFER, nvertices.nbytes, nvertices, GL_STATIC_DRAW)
    vertices = glGetAttribLocation(shader_program, 'a_position')
    glEnableVertexAttribArray(vertices)
    glVertexAttribPointer(vertices, 3, GL_FLOAT, GL_FALSE, 0, None)
    
    #glBindBuffer(GL_ARRAY_BUFFER, sprite_tex_buf)
    #glBufferData(GL_ARRAY_BUFFER, ntexture.nbytes, ntexture, GL_STATIC_DRAW)
    #tex = glGetAttribLocation(shader_program, 'a_texCoords')
    #glEnableVertexAttribArray(tex)
    #glVertexAttribPointer(tex, 2, GL_FLOAT, GL_TRUE, 0, None)
    
    wiz_y += 6
    if wiz_y >= 18*tile_height:
        wiz_y = 0
    sp = clock()
    wiz_t = sp
    
    global counter
    counter += 1
    if counter > 30:
        glViewport(-60, -20, width, height)
    
    print("Update Time: {:.6f}".format(sp-st))
    
    
def build_shader():
    vertex_shader = shaders.compileShader("""
        attribute vec3 a_position;
        attribute vec2 a_texCoords;
        
        varying vec2 v_texCoords; 
        
        void main() 
        { 
            gl_Position = vec4(a_position, 1); 
            
            v_texCoords = a_texCoords; 
        }
    """, GL_VERTEX_SHADER)
    
    #vertex_shader = shaders.compileShader("""attribute vec3 a_position; void main() { gl_Position = vec4(a_position, 1); }""", GL_VERTEX_SHADER)
    
    fragment_shader = shaders.compileShader("""
        uniform sampler2D u_image;
        
        varying vec2 v_texCoords;
        
        void main() 
        {
            vec4 tex = texture2D(u_image, v_texCoords);
            if(tex.a < 1.0)
              discard;
            gl_FragColor = tex; //texture2D(u_image, v_texCoords);
        }
    """, GL_FRAGMENT_SHADER)
    
    #fragment_shader = shaders.compileShader("""void main() { gl_FragColor = vec4(0,1,0,1); }""", GL_FRAGMENT_SHADER)
    
    return shaders.compileProgram(vertex_shader, fragment_shader)


glutInit()  # If this fails, it's probably because pyOpenGL didn't install .dlls properly
glutInitWindowSize(width, height)
glutCreateWindow(bytes("GL Test", 'utf-8')) # On windows, pyOpenGL doesn't like py3 strings :(
        
# Just request them all and don't worry about it.
glutInitDisplayMode(GLUT_DOUBLE|GLUT_RGBA|GLUT_DEPTH)
        
glClearColor(0, 0, 0, 0)
        
#glutReshapeFunc(self.reshape)
#glutKeyboardFunc(self.keyboard)
glutDisplayFunc(draw)
#glutIdleFunc(self._draw)
glutIdleFunc(update)
#glutMouseFunc(self.mouse)

if sys.platform == 'darwin':
    glutWMCloseFunc(stop)
    
#glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
#glEnable(GL_BLEND)

#glEnable(GL_TEXTURE_2D)

glDepthFunc(GL_LESS)
glEnable(GL_DEPTH_TEST)


#glFrustum (-1.0, 1.0, -1.0, 1.0, 10.0, 2.0)

# Load the texture
texture = glGenTextures(1)
glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
glBindTexture(GL_TEXTURE_2D, texture)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

image = Image.open('tiles.png').transpose(Image.FLIP_TOP_BOTTOM)#.transpose(Image.FLIP_LEFT_RIGHT)
iwidth, iheight = image.size
image = image.tobytes("raw", "RGBA", 0, -1)

glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, iwidth, iheight, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)

for row in range(iheight // 16):
    for col in range(iwidth // 16):

        w = iwidth / 16
        h = iheight / 16
    
        tex_x_step = 1 / w
        tex_y_step = 1 / h
    
        x = col*tex_x_step
        y = row*tex_y_step
            
        """tex_coords.append([
            x, y+tex_y_step,
            x+tex_x_step, y+tex_y_step,
            x, y,
            x, y,
            x+tex_x_step, y+tex_y_step,
            x+tex_x_step, y,
        ])"""
        
        tex_coords.append([
            x, y,
            x+tex_x_step, y,
            x, y+tex_y_step,
            x, y+tex_y_step,
            x+tex_x_step, y,
            x+tex_x_step, y+tex_y_step,
        ])
  
glGenerateMipmap(GL_TEXTURE_2D)

shader_program = build_shader()

glUseProgram(shader_program)

buffers = None
vertices = []
             
textures = []

buffers = glGenBuffers(4)
vertex_buffer = buffers[0]
tex_buffer = buffers[1]
sprite_buffer = buffers[2]
sprite_tex_buf = buffers[3]

def convert_to_ndc(x, y, z):
    return [ x * 2.0 / width - 1,
             2.0 - ((y-z) * 2.0 / height) - 1,
             2.0 - (y * 2.0 / height) - 1 - 0.0000001]           #  - 0.0000001
             
#x, y, z = convert_to_ndc(2*tile_width, 0*tile_height+1, 0*tile_depth)
#print("y0+1: z: 0", y, z)
#print("#######")
             
rows = (height // tile_height)+1
cols = (width // tile_width) + 1
for row in range(rows):
    for col in range(cols):

        #x1 = item.x * 2.0 / self.width - 1
        #y1 = (item.y+z*item.height) * 2.0 / self.height - 1
            
        #x2 = (item.x+item.width) * 2.0 / self.width - 1
        #y2 = ((item.y+z*item.height)+item.height) * 2.0 / self.height - 1
    
        x1, y1, z1 = convert_to_ndc(col*tile_width, row*tile_height, 0*tile_depth)
        x2, y2, z2 = convert_to_ndc((col+1)*tile_width, (row+1)*tile_height, 0*tile_depth)
        vertices.extend([x1,     y1,     z1,
                         x2,     y1,     z1,
                         x1,     y2,     z1,
                         x1,     y2,     z1,
                         x2,     y1,     z1,
                         x2,     y2,     z1 ])
        #print("grass: y: {}, z: {}".format(y1, z1))
        
        #if row > rows//2 or col > cols//2:
        #    print("adding water")
        #    if random.randint(0, 1000) % 9 == 0:
        #        textures.extend( tex_coords[3] ) 
        #    else:
        #        textures.extend( tex_coords[2] )
        #else:
        if random.randint(0, 1000) % 9 == 0:
            textures.extend( tex_coords[1] ) 
        else:
            textures.extend( tex_coords[0] )
            
"""x1, y1, z1 = convert_to_ndc(0*tile_width, 0*tile_height, 0*tile_depth)
x2, y2, z2 = convert_to_ndc((0+1)*tile_width, (0+1)*tile_height, 0*tile_depth)
vertices.extend([x1,     y1,     z1,
                 x2,     y1,     z1,
                 x1,     y2,     z1,
                 x1,     y2,     z1,
                 x2,     y1,     z1,
                 x2,     y2,     z1 ])
textures.extend( tex_coords[0] )
print("grass: y: {}, z: {}".format(y1, z1))"""
        
                     
x1, y1, z1 = convert_to_ndc(2*tile_width, 6*tile_height, 1*tile_depth)
x2, y2, z2 = convert_to_ndc((2+1)*tile_width, (6+1)*tile_height, 1*tile_depth)
vertices.extend([x1,     y1,     z1,
                 x2,     y1,     z1,
                 x1,     y2,     z1,
                 x1,     y2,     z1,
                 x2,     y1,     z1,
                 x2,     y2,     z1 ])
print("treebl: {}".format(z1))
        
textures.extend( tex_coords[20] )

x1, y1, z1 = convert_to_ndc(3*tile_width, 6*tile_height, 1*tile_depth)
x2, y2, z2 = convert_to_ndc((3+1)*tile_width, (6+1)*tile_height, 1*tile_depth)
vertices.extend([x1,     y1,     z1,
                 x2,     y1,     z1,
                 x1,     y2,     z1,
                 x1,     y2,     z1,
                 x2,     y1,     z1,
                 x2,     y2,     z1 ])
print("treebr: {}".format(z1))
        
textures.extend( tex_coords[21] )

x1, y1, z1 = convert_to_ndc(2*tile_width, 6*tile_height, 2*tile_depth)
x2, y2, z2 = convert_to_ndc((2+1)*tile_width, (6+1)*tile_height, 2*tile_depth)
vertices.extend([x1,     y1,     z1,
                 x2,     y1,     z1,
                 x1,     y2,     z1,
                 x1,     y2,     z1,
                 x2,     y1,     z1,
                 x2,     y2,     z1 ])
print("treetl: {}".format(z1))
        
textures.extend( tex_coords[10] )

x1, y1, z1 = convert_to_ndc(3*tile_width, 6*tile_height, 2*tile_depth)
x2, y2, z2 = convert_to_ndc((3+1)*tile_width, (6+1)*tile_height, 2*tile_depth)
vertices.extend([x1,     y1,     z1,
                 x2,     y1,     z1,
                 x1,     y2,     z1,
                 x1,     y2,     z1,
                 x2,     y1,     z1,
                 x2,     y2,     z1 ])
print("treetr: {}".format(z1))
        
textures.extend( tex_coords[11] )

nvertices = numpy.array(vertices, numpy.float32)
#print(nvertices)
ntexture = numpy.array(textures, numpy.float32)
#print(ntexture)


glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)
glBufferData(GL_ARRAY_BUFFER, nvertices.nbytes, nvertices, GL_STATIC_DRAW)
vertices = glGetAttribLocation(shader_program, 'a_position')
glEnableVertexAttribArray(vertices)
glVertexAttribPointer(vertices, 3, GL_FLOAT, GL_FALSE, 0, None)

glBindBuffer(GL_ARRAY_BUFFER, tex_buffer)
glBufferData(GL_ARRAY_BUFFER, ntexture.nbytes, ntexture, GL_STATIC_DRAW)
tex = glGetAttribLocation(shader_program, 'a_texCoords')
glEnableVertexAttribArray(tex)
glVertexAttribPointer(tex, 2, GL_FLOAT, GL_TRUE, 0, None)


sprites = []
spr_tex = []

x = 1*tile_width+16+16
y = 6*tile_height

x1, y1, z1 = convert_to_ndc(x, y, 1*tile_depth)
x2, y2, z2 = convert_to_ndc(x+32, y+32, 1*tile_depth)
sprites.extend([x1,     y1,     z1, 
                x2,     y1,     z1,
                x1,     y2,     z1,
                x1,     y2,     z1,
                x2,     y1,     z1,
                x2,     y2,     z1 ])
print("wiz: {}".format(z1))


spr_tex.extend( tex_coords[50] )

#nvertices = numpy.array(vertices, numpy.float32)
#print(nvertices)
#ntexture = numpy.array(textures, numpy.float32)
#print(ntexture)

x = 2*tile_width#+16
y = 2*tile_height+16#+16

x1, y1, z1 = convert_to_ndc(x, y+4, 1*tile_depth)
x2, y2, z2 = convert_to_ndc(x+32, y+32, 1*tile_depth)
sprites.extend([x1,     y1,     z1, 
                x2,     y1,     z1,
                x1,     y2,     z1,
                x1,     y2,     z1,
                x2,     y1,     z1,
                x2,     y2,     z1 ])
print("orc: y: {}, z: {}".format(y1, z1))


spr_tex.extend( tex_coords[42] )

"""x = 1*tile_width+16
y = 3*tile_height+16

x1, y1, z1 = convert_to_ndc(x, y, 1)
x2, y2, z2 = convert_to_ndc(x+32, y+32, 1)
sprites.extend([x1,     y1,     z1, 
                x2,     y1,     z1,
                x1,     y2,     z1,
                x1,     y2,     z1,
                x2,     y1,     z1,
                x2,     y2,     z1 ])



spr_tex.extend( tex_coords[40] )"""



nvertices = numpy.array(sprites, numpy.float32)
ntexture = numpy.array(spr_tex, numpy.float32)

glBindBuffer(GL_ARRAY_BUFFER, sprite_buffer)
glBufferData(GL_ARRAY_BUFFER, nvertices.nbytes, nvertices, GL_STATIC_DRAW)
vertices = glGetAttribLocation(shader_program, 'a_position')
glEnableVertexAttribArray(vertices)
glVertexAttribPointer(vertices, 3, GL_FLOAT, GL_FALSE, 0, None)


glBindBuffer(GL_ARRAY_BUFFER, sprite_tex_buf)
glBufferData(GL_ARRAY_BUFFER, ntexture.nbytes, ntexture, GL_STATIC_DRAW)
tex = glGetAttribLocation(shader_program, 'a_texCoords')
glEnableVertexAttribArray(tex)
glVertexAttribPointer(tex, 2, GL_FLOAT, GL_TRUE, 0, None)


"""wiz = {'x': 250, 'y': 250, 'z': 0, 'width': 32, 'height': 32, 'depth': 1}

#z = item.z - 1
#            if z < 0:
#                z = 0
#x1 = item.x * 2.0 / self.width - 1
#y1 = (item.y+z*item.height) * 2.0 / self.height - 1
            
x2 = (item.x+item.width) * 2.0 / self.width - 1
y2 = ((item.y+z*item.height)+item.height) * 2.0 / self.height - 1

vertices.append([
            # X,    Y,      Z     U,                                V
            wiz.x * 2.0 / width - 1,     y2,     0.0,  
            x2,     y2,     0.0,  
            x1,     y1,     0.0,  
            x1,     y1,     0.0,  
            x2,     y2,     0.0,  
            x2,     y1,     0.0,
            ])"""



glutMainLoop()