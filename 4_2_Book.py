from pyglet.gl import *
import pyglet
from pyglet import app, graphics
from pyglet.window import Window, key
import numpy as np
from pyglet import clock
import math

base = 20
#wx = 1.5 * base
#wy = 1.2 * base
wx = 1.5 * base
wy = 1.5 * base
a = int(base/2)

w =int(20 * wx)
h = w
window = Window(visible = True, width = w, height = h,
                resizable = True, caption = 'А-05-19 Лабораторная работа № 4 Абросимова')
#window.set_location(0, 30)


#glClearColor(0.15, 0.15, 0.15, 1.0)#определяет значения красного, зеленого, синего и альфа-канала, используемые glClear для очистки цветовых буферов.
# Значения, указанные в glClearColor, ограничены диапазоном 0 1.
glClear(GL_COLOR_BUFFER_BIT)#здесь уже буфер действительно отчищается до нужного нам цвета
glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)#выбор режима растеризации полигона
#GL_FRONT_AND_BACK для многоугольников, обращенных вперед и назад.



phi = math.asin(math.sqrt(1/3))
#print(phi)
#psy = math.asin(math.sqrt(1/2))#30 градусов или pi/6
psy = math.pi/6
#print(psy)
#psy = 30
#psydegree = 30
n_rot = 0
color = 0


tc = 1 # Число повторов текстуры
t_coords = ((0, 0), (0, tc), (tc, tc), (tc, 0)) # Координаты текстуры


def texInit():
    r = GL_RGB
    p = GL_TEXTURE_2D
    vp = np.full((w, w, 3), 0, dtype='uint8')
    #из примера вывода растровых данных
    for i in range(w):
        i0, i2 = i - 2, i + 2
        vp[i0:i2, i0:i2] = [0, 255, 0]
        #vp[i0:i2, i0:i2] = [255, 0, 0] #линия с правого верхнего в нижний
        i00, i20 = w - i0 - 1, w - i2 - 1
        vp[i0:i2, i20:i00] = [0, 255, 0]
    vp[-5:, :] = vp[:5, :] = [0, 0, 255]
    vp[:, -5:] = vp[:, :5] = [0, 0, 255]
    k = w // 4
    k2 = 3 * k
    #vp[k:k2, k:k2] = [255, 0, 0] # красный квадрат
    vp[k:k2, k:k2] = [0, 255, 255] #биризовый квадратик
    vp = vp.flatten()
    vp = (GLubyte * (w * w * 3))(*vp)
    # Задаем параметры текстуры
    gl.glTexParameterf(p, GL_TEXTURE_WRAP_S, GL_REPEAT)
    gl.glTexParameterf(p, GL_TEXTURE_WRAP_T, GL_REPEAT)
    gl.glTexParameterf(p, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    gl.glTexParameterf(p, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    # Способ взаимодействия с текущим фрагментом изображения
    gl.glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    # Создаем 2d-текстуру на основе образа img
    gl.glTexImage2D(p, 0, r, w, w, 0, r, GL_UNSIGNED_BYTE, vp)
    gl.glEnable(p)


param1 = 1
param2 = 1

def update(dt):
    global n_rot, color, tc, param1, param2
    if n_rot >= 360:
        n_rot = 0
    if color < 0 or color > 1:
        param2 *= -1
    color += param2 * 0.01
    if tc > 5 or tc < 1:
        param1 *= -1
    tc += param1 * 0.1
    n_rot += 1


clock.schedule_interval(update, 0.01)
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
    glRotatef(phi * 180 / math.pi, 1, 0, 0)  #угол в градусах
    glRotatef(-psy * 180 / math.pi, 0, 1, 0)

    # ---------------------------------------
    #glRotatef(-psydegree, 0, 1, 0)
    # ---------------------------------------
    glOrtho(-wx, wx, -wx, wx, -wx, wx)

    glMatrixMode(gl.GL_MODELVIEW)
    glLoadIdentity()
    glRotatef(n_rot, 0, 1, 0) #если убрать, то не вертится книжка вокруг оси y

    #glDisable(GL_TEXTURE_2D)
    glPushMatrix()
    #1-ый прямоугольник
    glBegin(GL_QUADS)
    glColor3f(0, 1, color)
    glColor3f(1, 0, 0)
    glVertex3f(-a, -a, -a)
    #glColor3f(1, 0, 0)
    glVertex3f(-a, a, -a)
    #glColor3f(1, 0, 0)
    glVertex3f(0, a, 0)
    #glColor3f(1, 0, 0)
    glVertex3f(0, -a, 0)
    # 2-ой прямоугольник
    glVertex3f(0, -a, 0)
    glVertex3f(0, a, 0)
    glVertex3f(a, a, -a)
    glVertex3f(a, -a, -a)
    glEnd()
    glPopMatrix()

    #glEnable(GL_TEXTURE_2D)  # Включение текстуры
    #glPushMatrix()
    #задать вершины по часовой, а не против
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex3f(-a, -a, -a)
    glTexCoord2f(tc*1/2, 0)
    glVertex3f(0, -a, 0)
    glTexCoord2f(tc*1/2, tc)
    glVertex3f(0, a, 0)
    glTexCoord2f(0, tc)
    glVertex3f(-a, a, -a)
    #glPopMatrix()

    glTexCoord2f(0, 0)
    glVertex3f(0, -a, 0)
    glTexCoord2f(tc*1/2, 0)
    glVertex3f(a, -a, -a)
    glTexCoord2f(tc*1/2, tc)
    glVertex3f(a, a, -a)
    glTexCoord2f(0, tc)
    glVertex3f(0, a, 0)
    glEnd()

app.run()