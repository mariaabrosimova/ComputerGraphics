from pyglet.gl import *
import pyglet
from pyglet import app, graphics
from pyglet.window import Window, key
import numpy as np
from pyglet import clock
import math

#dx, dy = 25, 15 # Размеры прямоугольника
#dx2 = dx / 2
#dy2 = dy / 2
size = 20
a = int(size/2) #ширина
wx, wy = 1.5 * size, 1.5 * size # Параметры области визуализации
w, h = int(20 * wx), int(20 * wy) # Размеры окна вывода
#----------------------------------------------------
window = Window(visible = True, width = w, height = h,
                resizable = True, caption = 'А-05-19 Лабораторная работа № 4 Абросимова')
window.set_location(0, 50)
glClearColor(0.15, 0.15, 0.15, 1.0)
glClear(GL_COLOR_BUFFER_BIT)
glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
#----------------------------------------------------

angle = -3*math.pi/4
alfa = math.pi/4

tc = 1 # Число повторов текстуры
t_coords = ((0, 0), (0, tc), (tc, tc), (tc, 0)) # Координаты текстуры
n_rot = 0
color = 0

def texInit():
    r = GL_RGB
    p = GL_TEXTURE_2D
    vp = np.full((w, w, 3), 0, dtype='uint8')
    k = w // 4
    vp[:w, :k, 0] = 255
    vp[:w, k:2*k, :] = 255
    vp[:w, 2*k:3 * k, 1] = 255

    vp = vp.flatten()
    vp = (GLubyte * (w * w * 3))(*vp)

    gl.glTexParameterf(p, GL_TEXTURE_WRAP_S, GL_REPEAT)
    gl.glTexParameterf(p, GL_TEXTURE_WRAP_T, GL_REPEAT)
    gl.glTexParameterf(p, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    gl.glTexParameterf(p, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    gl.glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    gl.glTexImage2D(p, 0, r, w, w, 0, r, GL_UNSIGNED_BYTE, vp)
    gl.glEnable(p)


param1 = 1
param2 = 1

def update(dt):
    global n_rot, color, tc, param1, param2
    if n_rot >= 360:
        n_rot = 0
    if tc > 4 or tc < 1:
        param1 *= -1
    tc += param1 * 0.1
    n_rot += 1
    if color < 0 or color > 1:
        param2 *=-1
    color += param2 * 0.009


clock.schedule_interval(update, 0.01)
glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
glEnable(GL_DEPTH_TEST)
texInit()

@window.event
def on_draw():
    global n_rot, angle, alfa, color
    window.clear()

    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glRotatef(angle * 180 / math.pi, 1, 0, 0)
    glRotatef(-alfa * 180 / math.pi, 0, 1, 0)
    glRotatef(angle, 0, 1, 0)
    glOrtho(-wx, wx, -wx, wx, -wx, wx)

    glMatrixMode(gl.GL_MODELVIEW)
    glLoadIdentity()
    glRotatef(n_rot, 0, 1, 0)

    glDisable(GL_TEXTURE_2D)

    glBegin(GL_QUADS)
    glColor3f(color, 0, 1-color)

    glVertex3f(0, -a, 0)
    glVertex3f(-a, -a, -a)
    glVertex3f(-a, a, -a)
    glVertex3f(0, a, 0)

    glVertex3f(a, -a, -a)
    glVertex3f(0, -a, 0)
    glVertex3f(0, a, 0)
    glVertex3f(a, a, -a)
    glEnd()
    glEnable(GL_TEXTURE_2D)  # Включение текстуры

    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex3f(-a, -a, -a)
    glTexCoord2f(tc * 0.75, 0)
    glVertex3f(0, -a, 0)
    glTexCoord2f(tc * 0.75, tc)
    glVertex3f(0, a, 0)
    glTexCoord2f(0, tc)
    glVertex3f(-a, a, -a)

    glTexCoord2f(0, 0)
    glVertex3f(0, -a, 0)
    glTexCoord2f(tc * 0.75, 0)
    glVertex3f(a, -a, -a)
    glTexCoord2f(tc * 0.75, tc)
    glVertex3f(a, a, -a)
    glTexCoord2f(0, tc)
    glVertex3f(0, a, 0)
    glEnd()


app.run()
