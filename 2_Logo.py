import pyglet
import math
from pyglet import app, gl, graphics
from pyglet.window import Window, key
wx=wy=20
d = 12
d2 = 6
x=y=0
width, height = int(20 * wx), int(20 * wy) # Размеры окна вывода
window = Window(visible = True, width = width, height = height,
                resizable = True, caption = 'Логотип')
#window.set_location(0, 30)
gl.glClearColor(0.1, 0.1, 0.1, 1.0)
gl.glClear(gl.GL_COLOR_BUFFER_BIT)
gl.glEnable(gl.GL_POINT_SMOOTH)
gl.glPointSize(8)
x = 0
y = 0
@window.event
def on_draw():
    window.clear()
    gl.glMatrixMode(gl.GL_MODELVIEW)
    gl.glRotatef(180 * x, 1, 0, 0)  # Поворот вокруг оси X
    gl.glRotatef(180 * y, 0, 1, 0)
    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glLoadIdentity()
    gl.glOrtho(-20*wx, 20*wx, -20*wy, 20* wy, -1, 1)
    # квадрат
    gl.glPolygonMode(gl.GL_FRONT, gl.GL_FILL)
    gl.glBegin(gl.GL_QUADS)
    gl.glColor3f(1, 1, 1)
    gl.glVertex2f(100, 100)
    gl.glVertex2f(300, 100)
    gl.glVertex2f(300, 300)
    gl.glColor3f(0, 0, 1)
    gl.glVertex2f(100, 300)
    gl.glEnd()
    # треугольник
    gl.glPolygonMode(gl.GL_FRONT, gl.GL_FILL)
    gl.glBegin(gl.GL_TRIANGLES)
    gl.glColor3d(1, 0, 0)
    gl.glVertex2f(100, 100)
    gl.glColor3d(0, 0, 1)
    gl.glVertex2f(300, 100)
    gl.glColor3d(0, 1, 0)
    gl.glVertex2f(200, 300)
    gl.glEnd()
    #окружность
    gl.glLineWidth(1)
    gl.glPointSize(3)
    pattern1 = '1111100110011111'
    #pattern1 = '1111111111111111'
    gl.glLineStipple(2, int(pattern1, 2))
    gl.glPolygonMode(gl.GL_FRONT, gl.GL_LINE) #по умолчанию gl.GL_FILL (заливка)
    n = 100
    r = 100
    gl.glPointSize(1)
    gl.glColor3d(0, 0, 1)
    gl.glBegin(gl.GL_POLYGON)
    for i in range(n):
        x0 = r * math.cos((2 * math.pi * i) / n) + 200
        y0 = r * math.sin((2 * math.pi * i) / n) + 200
        gl.glVertex2f(x0, y0)
    gl.glEnd()
    #gl.glShadeModel(gl.GL_FLAT)
    #линия
    gl.glLineWidth(1)
    gl.glPointSize(1)
    pattern = '0b1111100110011111'
    gl.glLineStipple(2, int(pattern, 2))
    gl.glBegin(gl.GL_LINES)
    gl.glColor3d(1, 0, 1)
    gl.glVertex2f(200, 100)
    gl.glColor3d(0.5, 0.5, 1)
    gl.glVertex2f(200, 300)
    gl.glEnd()
@window.event
def on_key_press(symbol, modifiers):
    global x, y
    mode_b = None
    if symbol == key.DOWN:
        x = 1 - x
        y = 0
    elif symbol == key.LEFT:
        y = 1 - y
        x = 0
    elif symbol == key._1:
        mode_b = gl.GL_LINE #изнанка- линии
        shade_model = gl.GL_SMOOTH

    elif symbol == key._2:
        mode_b = gl.GL_POINT#изнанка- вершины
        shade_model = gl.GL_SMOOTH

    elif symbol == key._3:
        mode_b = gl.GL_FILL  # изнанка- с заливкой
        shade_model = gl.GL_SMOOTH # интерполяция разрешена
    elif symbol == key._4:
        mode_b = gl.GL_FILL# лицевая, изнанка с заливкой
        shade_model = gl.GL_FLAT #интерполяция запрещена

    elif symbol == key._5:
        gl.glEnable(gl.GL_LINE_STIPPLE)

    elif symbol == key._6:
        gl.glDisable(gl.GL_LINE_STIPPLE)
    if mode_b is not None:
        gl.glPolygonMode(gl.GL_BACK, mode_b)
        gl.glShadeModel(shade_model)
app.run()

