from OpenGL.GL import *
from OpenGL.GL import shaders
#from OpenGL.GLU  import *
from OpenGL.GLUT import *

from PIL import Image

import numpy

import time
import math
import sys

width = 600
height = 600
depth = 10

tile_width = 32
tile_height = 32
tile_depth = 1

texture = None
tex_coords = []

VBO = None
shader_program = None


def stop():
    glutDestroyWindow(glutGetWindow())
    sys.exit(0)
    
def draw():
    #print("drawing...")
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # Clear all pixels.
    
    
    #glDrawArrays(GL_TRIANGLES, 0, 6)
    #glDrawElements(GL_TRIANGLES, 6*(width//tile_width)*(height//tile_height), GL_UNSIGNED_INT, None)
    glDrawElements(GL_TRIANGLES, 6 * 4, GL_UNSIGNED_INT, None)
    """glDrawElements(
     GL_TRIANGLES,      # mode
     6, #width//tile_width * height//tile_height,    # count
     GL_UNSIGNED_INT,   # type
     0           # element array buffer offset
    )"""
    
    #glutSwapBuffers()
    glutPostRedisplay()
    glFlush()
    
def update():
    pass
    
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
            gl_FragColor = texture2D(u_image, v_texCoords);
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
    
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
glEnable(GL_BLEND)

glEnable(GL_TEXTURE_2D)



# Load the texture
texture = glGenTextures(1)
glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
glBindTexture(GL_TEXTURE_2D, texture)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

image = Image.open('tiles.png').transpose(Image.FLIP_TOP_BOTTOM)
iwidth, iheight = image.size
image = image.tobytes("raw", "RGBA", 0, -1)

glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, iwidth, iheight, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)

for row in range(height // 16):
    for col in range(width // 16):

        w = iwidth / 16
        h = iheight / 16
    
        tex_x_step = 1 / w;
        tex_y_step = 1 / h;
    
        x = col*tex_x_step;
        y = row*tex_y_step;
    
        tex_coords.append([
            x, y,
            x+tex_x_step, y,
            x, y+tex_y_step,
            x, y+tex_y_step,
            x+tex_x_step, y,
            x+tex_x_step, y+tex_y_step])

    
glGenerateMipmap(GL_TEXTURE_2D)

#texture_coords = [[0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0]]
    
shader_program = build_shader()

glUseProgram(shader_program)

buffers = None
vertices = []
indices = []#[0, 1, 2, 2, 1, 3]
             
textures = [ 0.1,  0.1,   
             0.2,  0.1,            
             0.1,  0.0,     
             0.2,  0.0 ]
             
#textures = tex_coords[9]
textures = []

buffers = glGenBuffers(3)

index_buffer = buffers[0]
vertex_buffer = buffers[1]
tex_buffer = buffers[2]

def convert_to_ndc(x, y, z):
    return [ x * 2.0 / width - 1,
             y * 2.0 / height - 1,
             z * 2.0 / depth - 1 ]
rows = (height // tile_height)#+1
cols = (width // tile_width)# + 1
for row in range(rows):
    for col in range(cols):
        x, y, z = convert_to_ndc(col*tile_width, row*tile_height, 0)
        vertices.append([x, y, z])

        #indices.append( [col+(row*cols), col+((row+1)*cols), (col+1)+(row*cols),
        #                (col+1)+(row*cols),  col+((row+1)*cols), (col+1)+((row+1)*colswi
        textures.extend( [ 0.1,  0.1,
             0.2,  0.1,
             0.1,  0.0,
             0.2,  0.0 ] )
             
indices.append([0, 18, 1, 1, 18, 19])

indices.append([1, 19, 2, 2, 19, 20])

indices.append([18, 36, 19, 19, 36, 37])
indices.append([19, 37, 20, 20, 37, 38])
        
#vertices.append(convert_to_ndc(0, 0, 0))
#vertices.append(convert_to_ndc(128, 0, 0))
#vertices.append(convert_to_ndc(0, 128, 0))
#vertices.append(convert_to_ndc(128, 128, 0))

nvertices = numpy.array(vertices, numpy.float32)
#print(nvertices)
nindices = numpy.array(indices, numpy.int32)
print(nindices)
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

glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, index_buffer)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, nindices.nbytes, nindices, GL_STATIC_DRAW)


#vertices = glGetAttribLocation(shader_program, 'a_position')
#glEnableVertexAttribArray(vertices



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