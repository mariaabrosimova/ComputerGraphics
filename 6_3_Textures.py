from pyglet.gl import *
import pyglet
from pyglet import app, graphics
from pyglet.window import Window, key
import numpy as np
from pyglet import clock
import math

base = 20
wx = 1.5 * base
wy = 1.2 * base
a = int(base/2)
w = int(20 * wx)
h = w
window = Window(visible = True, width = w, height = h,
                resizable = True, caption = 'Кр')
glClearColor(0.15, 0.15, 0.15, 1.0)
glClear(GL_COLOR_BUFFER_BIT)
glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

n_rot = 0
color = 0


tc = 1 # Число повторов текстуры
t_coords = ((0, 0), (0, tc), (tc, tc), (tc, 0)) # Координаты текстуры


def texInit():
    iWidth = iHeight = 64
    n = 3 * iWidth * iHeight
    img = np.zeros((iWidth, iHeight, 3), dtype = 'uint8')
    for i in range(iHeight):
     for j in range(iWidth):
        img[i, j, :] = (i & 16 ^ j & 16) * 255
    img = img.reshape(n)
    img = (GLubyte * n)(*img)
    p, r = GL_TEXTURE_2D, GL_RGB
    glTexParameterf(p, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(p, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(p, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(p, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    glTexImage2D(p, 0, r, iWidth, iHeight, 0, r, GL_UNSIGNED_BYTE, img)
    glEnable(p)


param1 = 1
param2 = 1

def update(dt):
    global n_rot, color, tc, param1, param2
    if n_rot >= 360:
        n_rot = 0
    if color < 0 or color > 1:
        param2 *= -1
    color += param2 * 0.01
    if tc > 3 or tc < 1:
        param1 *= -1
    tc += param1 * 0.1
    n_rot += 1


clock.schedule_interval(update, 0.05)
glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
glEnable(GL_DEPTH_TEST)
texInit()

@window.event
def on_draw():
    global n_rot, phi, psy, color
    window.clear()

    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-wx, wx, -wx, wx, -wx, wx)

    glMatrixMode(gl.GL_MODELVIEW)
    glLoadIdentity()
    glRotatef(n_rot, 0, 1, 0)

    glDisable(GL_TEXTURE_2D)

    glBegin(GL_QUADS)
    glColor3f(0, 1-color, color)
    glVertex3f(-a, -a, 0)
    glVertex3f(0, -a, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(-a, 0, 0)
    
    glColor3f(1-color, color, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(a, 0, 0)
    glVertex3f(a, a, 0)
    glVertex3f(0, a, 0)
    glEnd()

    glEnable(GL_TEXTURE_2D)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex3f(0, -a, 0)
    glTexCoord2f(tc, 0)
    glVertex3f(a, -a, 0)
    glTexCoord2f(tc, tc)
    glVertex3f(a, 0, 0)
    glTexCoord2f(0, tc)
    glVertex3f(0, 0, 0)

    glTexCoord2f(0, 0)
    glVertex3f(-a, 0, 0)
    glTexCoord2f(3-tc, 0)
    glVertex3f(0, 0, 0)
    glTexCoord2f(3-tc, 3-tc)
    glVertex3f(0, a, 0)
    glTexCoord2f(0, 3-tc)
    glVertex3f(-a, a, 0)
    glEnd()


    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex3f(-a, -a, 0)
    glTexCoord2f(tc*1/2, 0)
    glVertex3f(-a, a, 0)
    glTexCoord2f(tc*1/2, tc)
    glVertex3f(a, a, 0)
    glTexCoord2f(0, tc)
    glVertex3f(a, -a, 0)
    glEnd()
    

app.run()