from OpenGL.GL import *
from OpenGL.GLU import *

import sys
cupy_module_name = 'cupy'
if cupy_module_name in sys.modules:
    import cupy as np
else:
    import numpy as np
    
from bvhModel import *
from camManager import *

def draw_frame():
    glLineWidth(3)
    glBegin(GL_LINES)
    glColor3ub(255,0,0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([1.,0.,0.]))
    glColor3ub(0,255,0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,1.,0.]))
    glColor3ub(0,0,255)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,0.,1.]))
    glEnd()
    glLineWidth(1)

def draw_grid(row, col):
    glBegin(GL_LINES)
    glColor3ub(255,255,255)
    
    for i in range(row + 1):
        glVertex3f(i - row / 2, 0, -col/2)
        glVertex3f(i - row / 2, 0, col/2)
    
    for i in range(col + 1):
        glVertex3f(-row/2, 0, i - col / 2)
        glVertex3f(row/2, 0, i - col / 2)
    
    glEnd()

# draw a cube of side 2, centered at the origin.
def drawCube():
    glBegin(GL_QUADS)
    glVertex3f( 1.0, 1.0,-1.0)
    glVertex3f(-1.0, 1.0,-1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f( 1.0, 1.0, 1.0)
    glVertex3f( 1.0,-1.0, 1.0)
    glVertex3f(-1.0,-1.0, 1.0)
    glVertex3f(-1.0,-1.0,-1.0)
    glVertex3f( 1.0,-1.0,-1.0)
    glVertex3f( 1.0, 1.0, 1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f(-1.0,-1.0, 1.0)
    glVertex3f( 1.0,-1.0, 1.0)
    glVertex3f( 1.0,-1.0,-1.0)
    glVertex3f(-1.0,-1.0,-1.0)
    glVertex3f(-1.0, 1.0,-1.0)
    glVertex3f( 1.0, 1.0,-1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f(-1.0, 1.0,-1.0)
    glVertex3f(-1.0,-1.0,-1.0)
    glVertex3f(-1.0,-1.0, 1.0)
    glVertex3f( 1.0, 1.0,-1.0)
    glVertex3f( 1.0, 1.0, 1.0)
    glVertex3f( 1.0,-1.0, 1.0)
    glVertex3f( 1.0,-1.0,-1.0)
    glEnd()
    
# draw a sphere of radius 1, centered at the origin.
# numLats: number of latitude segments
# numLongs: number of longitude segments
def drawSphere(numLats=12, numLongs=12):
    for i in range(0, numLats + 1):
        lat0 = np.pi * (-0.5 + float(float(i - 1) / float(numLats)))
        z0 = np.sin(lat0)
        zr0 = np.cos(lat0)
        lat1 = np.pi * (-0.5 + float(float(i) / float(numLats)))
        z1 = np.sin(lat1)
        zr1 = np.cos(lat1)
        # Use Quad strips to draw the sphere
        glBegin(GL_QUAD_STRIP)
        for j in range(0, numLongs + 1):
            lng = 2 * np.pi * float(float(j - 1) / float(numLongs))
            x = np.cos(lng)
            y = np.sin(lng)
            glVertex3f(x * zr0, y * zr0, z0)
            glVertex3f(x * zr1, y * zr1, z1)
        glEnd()

def render_animation_wiered(animation:BvhAnimation, index_of_motion: int):
    parent_index_stack = []
    
    parent_index_stack.append(0)
    
    for joint in animation.skeleton.joints:
        
        while joint.parent_index != parent_index_stack[-1]:
            parent_index_stack.pop()
            glPopMatrix()
        
        glPushMatrix()
        parent_index_stack.append(joint.index)
        
        
        for i in range(joint.num_channel):
            M = np.identity(4)
            if joint.channels[i].upper() == "Xposition".upper():
                translation = joint.movement_infos[index_of_motion].movement_per_channel[i]
                glTranslatef(translation, 0, 0)
            elif joint.channels[i].upper() == "Yposition".upper():
                translation = joint.movement_infos[index_of_motion].movement_per_channel[i]
                glTranslatef(0,translation, 0)
            elif joint.channels[i].upper() == "Zposition".upper():
                translation = joint.movement_infos[index_of_motion].movement_per_channel[i]
                glTranslatef(0, 0, translation)
            elif joint.channels[i].upper() == "Xrotation".upper():
                ang = joint.movement_infos[index_of_motion].movement_per_channel[i]
                glRotatef(ang, 1, 0, 0)
            elif joint.channels[i].upper() == "Yrotation".upper():
                ang = joint.movement_infos[index_of_motion].movement_per_channel[i]
                glRotatef(ang, 0, 1, 0)
            elif joint.channels[i].upper() == "Zrotation".upper():
                ang = joint.movement_infos[index_of_motion].movement_per_channel[i]
                glRotatef(ang, 0, 0, 1)
            else :
                print("error! undefined channel - ", joint.channels[i])
                
            
        if joint.index != 0:
            glPushMatrix()
            glBegin(GL_LINES)
            glVertex3f(joint.offsets[0], joint.offsets[1], joint.offsets[2])
            glVertex2f(0,0,0)
            glEnd()
            glPopMatrix()
            
        
        glTranslatef(joint.offsets[0], joint.offsets[1], joint.offsets[2])
        
    while len(parent_index_stack) > 1:
        glPopMatrix()
        parent_index_stack.pop()
        

def render_animation(animation:BvhAnimation, index_of_motion: int):
    parent_index_stack = []
    
    parent_index_stack.append(0)
    
    for joint in animation.skeleton.joints:
        
        while joint.parent_index != parent_index_stack[-1]:
            parent_index_stack.pop()
            glPopMatrix()
        
        glPushMatrix()
        parent_index_stack.append(joint.index)
        if joint.index != 0:
            glPushMatrix()
            glBegin(GL_LINES)
            glVertex3f(joint.offsets[0], joint.offsets[1], joint.offsets[2])
            glVertex2f(0,0,0)
            glEnd()
            glPopMatrix()
            
        
        glTranslatef(joint.offsets[0], joint.offsets[1], joint.offsets[2])
        
        for i in range(joint.num_channel):
            M = np.identity(4)
            if joint.channels[i].upper() == "Xposition".upper():
                translation = joint.movement_infos[index_of_motion].movement_per_channel[i]
                glTranslatef(translation, 0, 0)
            elif joint.channels[i].upper() == "Yposition".upper():
                translation = joint.movement_infos[index_of_motion].movement_per_channel[i]
                glTranslatef(0,translation, 0)
            elif joint.channels[i].upper() == "Zposition".upper():
                translation = joint.movement_infos[index_of_motion].movement_per_channel[i]
                glTranslatef(0, 0, translation)
            elif joint.channels[i].upper() == "Xrotation".upper():
                ang = joint.movement_infos[index_of_motion].movement_per_channel[i]
                glRotatef(ang, 1, 0, 0)
            elif joint.channels[i].upper() == "Yrotation".upper():
                ang = joint.movement_infos[index_of_motion].movement_per_channel[i]
                glRotatef(ang, 0, 1, 0)
            elif joint.channels[i].upper() == "Zrotation".upper():
                ang = joint.movement_infos[index_of_motion].movement_per_channel[i]
                glRotatef(ang, 0, 0, 1)
            else :
                print("error! undefined channel - ", joint.channels[i])
                
            
        
        
    while len(parent_index_stack) > 1:
        glPopMatrix()
        parent_index_stack.pop()
        


def render_model(animation:BvhAnimation):
    if animation == None:
        return
    parent_index_stack = []
    
    parent_index_stack.append(0)
    
    for joint in animation.skeleton.joints:
        
        while joint.parent_index != parent_index_stack[-1]:
            parent_index_stack.pop()
            glPopMatrix()
        
        glPushMatrix()
        parent_index_stack.append(joint.index)
        
        if joint.index != 0:
            glPushMatrix()
            glBegin(GL_LINES)
            glVertex3f(joint.offsets[0], joint.offsets[1], joint.offsets[2])
            glVertex2f(0,0,0)
            glEnd()
            glPopMatrix()
        
        glTranslatef(joint.offsets[0], joint.offsets[1], joint.offsets[2])
        
    while len(parent_index_stack) > 1:
        glPopMatrix()
        parent_index_stack.pop()
        
