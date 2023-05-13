import pyglet.gl
from pyglet.gl import *
import pyglet
from pyglet import app, graphics
from pyglet.window import Window, key
import numpy as np
from pyglet import clock
import math
size = 20
a = int(size/2) #ширина
wx, wy = 2* size, 2 * size # Параметры области визуализации
w, h = int(20 * wx), int(20 * wy) # Размеры окна вывода
h0 = 20
h1 = h0/2
n = 20
r = 10
ch = 2 * n #кол-во вершин
#-------------------------------
vrts_top = []# Координаты вершин крышки
vrts_bottom = []# Координаты вершин крышки
vrts1=[]
#материал
#mtClr0 = [1, 1, 1, 0]
mtClr0 = [1, 1, 1, 0]
mtClr = (gl.GLfloat * 4)()
for k in range(4): mtClr[k] = mtClr0[k]
#1-ый источник света
light_position0 = [0, -10, 10, 0] # light_position0 = [-20, 30, 20, 0] # Позиция источника света
lghtClr0 = [1, 0, 0, 0]
light_position = (gl.GLfloat * 4)()
lghtClr = (gl.GLfloat * 4)()
for k in range(4): light_position[k] = light_position0[k]
for k in range(4): lghtClr[k] = lghtClr0[k]
#2-ой источник света
light_position2 = [0, -30, 30, 0]#[15, 20, 10, 0] #полностью красный
lghtClr2 = [0, 0, 0.5, 0]
light_position1 = (gl.GLfloat * 4)()
lghtClr1 = (gl.GLfloat * 4)()
for k in range(4): light_position1[k] = light_position2[k]
for k in range(4): lghtClr1[k] = lghtClr2[k]
#3-ий источник света
#light_position03 = [15, 20, 10, 0]# #полностью красный
light_position03 = [10, 20, 10, 0]
lghtClr03 = [0.75, 0, 1, 0]
light_position3 = (gl.GLfloat * 4)()
lghtClr3 = (gl.GLfloat * 4)()
for k in range(4): light_position3[k] = light_position03[k]
for k in range(4): lghtClr3[k] = lghtClr03[k]
vrts = [] # Координаты вершин призмы
nrms = [] # Координаты нормалей к граням (рассчитываются для каждой вершины)
nrms0 = []
nrms_top = []
nrms_bottom=[]
indexnormal=0
indexbase = 1
indexrotate1=0
indexrotate2 = 0
indexdepthtest = 0
indexCullFace = 0
indexsource =0
indexLighting = 0
indexnormalize = 0
indexnormalize2 = 0
indexDiffuse = 0
#----------------------------------------------------
window = Window(visible = True, width = w, height = h,
                resizable = True, caption = 'А-05-19 Лабораторная работа № 5 Абросимова')
window.set_location(0, 50)
glClearColor(0.15, 0.15, 0.15, 1.0)
glClear(GL_COLOR_BUFFER_BIT)
glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
gl.glDisable(gl.GL_LIGHTING)
#gl.glDisable(gl.GL_SMOOTH)
gl.glLineWidth(3)
gl.glPointSize(1)
#----------------------------------------------------
#начальное положение углов
rot_x = 10 # Углы поворота вокруг осей X, Y и Z
rot_y = -30 # (15, 25, 15) или (-25, 215, -15)
rot_z = 0
angle_x = 0
angle_y = 0
angle_z = 0
n_rot = 0
#начальный сдвиг источника
x = 0
y = 0
z = 0
param1 = 1
param2 = 1
color = 1
def update(dt):
    global n_rot, color, param1, param2
    if n_rot >= 360:
        n_rot = 0
    if color < 0 or color > 1:
        param2 *= -1
    color += param2 * 0.1
    n_rot += 1
clock.schedule_interval(update, 0.01)
glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

def rotate(angle_x, angle_y, angle_z):
    gl.glRotatef(angle_x, 1, 0, 0)  # Поворот относительно оси X
    gl.glRotatef(angle_y, 0, 1, 0)  # Поворот относительно оси Y
    gl.glRotatef(angle_z, 0, 0, 1)  # Поворот относительно оси Z
def normal(v,sn):
    kn = 2
    gl.glVertex3f(v[0], v[1], v[2])
    sx = kn * sn[0]
    sy = kn * sn[1]
    sz = kn * sn[2]
    gl.glVertex3f(v[0] + sx, v[1] + sy, v[2] + sz)


@window.event
def on_draw():
    global n_rot, angle, alfa, color, base
    window.clear()
    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glLoadIdentity()
    glOrtho(-wx, wx, -wx, wx, -wx, wx)
    glMatrixMode(gl.GL_MODELVIEW)
    glLoadIdentity()


    #начальное положение
    rotate(rot_x, rot_y, rot_z)
    #повороты
    if (indexrotate1 %2 == 1):
        rotate(angle_x, angle_y, angle_z) #при одинарном нажатии поворот, при двойном - возврат
    if  (indexrotate2 %2 == 1):
        rotate(angle_x, angle_y, angle_z)
    if (indexdepthtest %2 == 1):
        glEnable(GL_DEPTH_TEST)
    else:
        glDisable(GL_DEPTH_TEST)
    if (indexCullFace %2 == 1):

        glDisable(GL_CULL_FACE)
    else:
        glCullFace(GL_BACK)
        glEnable(GL_CULL_FACE)
        glFrontFace(GL_CCW)
        glFrontFace(GL_CW)

    if (indexLighting %2 == 1):
        glEnable(gl.GL_LIGHTING)
    else:
        glDisable((gl.GL_LIGHTING))

    if (indexnormalize2 %2 == 1):
        glEnable(gl.GL_NORMALIZE)
    else:
        glDisable(gl.GL_NORMALIZE)


    if (indexDiffuse % 2 == 1):
        gl.glMaterialfv(gl.GL_FRONT, gl.GL_DIFFUSE, mtClr)
    else:
        gl.glMaterialfv(gl.GL_FRONT, gl.GL_SPECULAR, mtClr)

    #оси координат
    #oсь Oz
    gl.glColor3d(1, 0, 0)
    gl.glBegin(gl.GL_LINES)
    gl.glVertex3f(0, 0, 0)
    gl.glVertex3f(0, 0, 50)
    gl.glEnd()
    #ось Oy
    gl.glBegin(gl.GL_LINES)
    gl.glColor3d(1, 1, 1)
    gl.glVertex3f(0, 0, 0)
    gl.glVertex3f(0, 50, 0)
    gl.glEnd()
    # ось Ox
    gl.glBegin(gl.GL_LINES)
    gl.glColor3d(0, 0, 1)
    gl.glVertex3f(0, 0, 0)
    gl.glVertex3f(50, 0, 0)
    gl.glEnd()
    # многоугольники
    #верхнее основание
    x_arr = [(r * math.cos((2 * math.pi * i) / n))for i in range(n)]
    z_arr = [(r * math.sin((2 * math.pi * i) / n)) for i in range(n)]
    vrts_top = [0 for i in range(n)]#координаты вершин n-угольника
    for i in range(n):
        vrts_top[i] = np.array([x_arr[n-1-i], h1, z_arr[n-1-i]]) #обратный обход для вывода лицевой стороны
    #нижнее основание
    vrts_bottom = [0 for i in range(n)]
    for i in range(n):
        vrts_bottom[i] = np.array([x_arr[i], -h1, z_arr[i]])
     # боковая поверхность
    #------------------------
    for i in range(n):
        v0 = np.array([x_arr[i], h1, z_arr[i]])
        if (i + 1) < n:
            v1 = np.array([x_arr[i + 1], h1, z_arr[i + 1]])
            v2 = np.array([x_arr[i + 1], -h1, z_arr[i + 1]])
        else:
            v1 = np.array([x_arr[0], h1, z_arr[0]])
            v2 = np.array([x_arr[0], -h1, z_arr[0]])
        v3 = np.array([x_arr[i], -h1, z_arr[i]])
        vrts.append([v0, v1, v2, v3])
        a = v1 - v0
        b = v3 - v0
        sab = np.cross(a, b)  # Векторное произведение
        sab = sab / np.linalg.norm(sab)  # Нормализация
        if (indexnormalize % 2 == 0):
            sab = sab / np.linalg.norm(sab)
        nrms.append(sab)  # Координаты нормали

        a = v1 - v0
        b = v3 - v0
        sab1 = np.cross(a, b)  # Векторное произведение [x,y,z]-вектор
        if (indexnormalize % 2 == 0):
            sab1 = sab1 / np.linalg.norm(sab1)

        s1 = np.array(sab1)
        nrms0.append(sab1)  # Координаты нормали
        c = v2 - v1
        d = v0 - v1
        sab2 = np.cross(c, d)  # Векторное произведение
        if (indexnormalize % 2 == 0):
            sab2 = sab2 / np.linalg.norm(sab2)  # Нормализация

        s2 = np.array(sab2)
        nrms0.append(sab2)  # Координаты нормали
        e = v3 - v2
        f = v1 - v2
        sab3 = np.cross(e, f)  # Векторное произведение
        if (indexnormalize % 2 == 0):
            sab3 = sab3 / np.linalg.norm(sab3)  # Нормализация

        s3 = np.array(sab3)
        nrms0.append(sab3)  # Координаты нормали
        g = v0 - v3
        h = v2 - v3
        sab4 = np.cross(g, h)  # Векторное произведение
        if (indexnormalize % 2 == 0):
            sab4 = sab4 / np.linalg.norm(sab4)  # Нормализация

        nrms0.append(sab4)  # Координаты нормали
        s4 = np.array(sab4)
        #nrms1.append([s1, s2, s3, s4])
    n_vrts = len(vrts)

    for j in range(n):
        nrms.append(nrms[n_vrts - n + j])
    #вывод боковых граней и нормалей к ним
    glPushMatrix()
    #glRotatef(n_rot, 0, 1, 0)
    gl.glBegin(gl.GL_QUADS)
    gl.glColor3f(1, 1, 0.8)

    k = -1
    for i in range(n):
        k += 1
        v = vrts[k]
        v0 = v[0]
        v1 = v[1]
        v2 = v[2]
        v3 = v[3]
        #относится к v0
        sn = nrms[k]
        #sn = nrms[k]  # Нормаль к вершине (она же нормаль к грани)
        gl.glNormal3f(sn[0], sn[1], sn[2])
        #gl.glColor3d(1, 1, 1)
        gl.glColor3d(0.5, 1, 0)
        gl.glVertex3f(v0[0], v0[1], v0[2])

        #sn = nrms[k + 1]
        sn = nrms[k + 1]
        gl.glNormal3f(sn[0], sn[1], sn[2])
        gl.glColor3d(1, 0, 0)
        #gl.glColor3d(1, 1, 1)
        gl.glVertex3f(v1[0], v1[1], v1[2])

        sn = nrms[k + 2]
        #sn = nrms[k + 1]
        #sn = nrms[2]
        #sn = nrms[k + n]
        gl.glNormal3f(sn[0], sn[1], sn[2])
        gl.glColor3d(1, 1, 1)
        gl.glVertex3f(v2[0], v2[1], v2[2])


        #sn = nrms[k + n - 1]
        #sn = nrms[3]
        sn = nrms[k + 3]
        gl.glNormal3f(sn[0], sn[1], sn[2])
        #gl.glColor3d(0, 0, 1)
        gl.glColor3d(0.5, 0.7, 0)
        #gl.glColor3d(1, 1, 1)
        gl.glVertex3f(v3[0], v3[1], v3[2])
    gl.glEnd()
    glPopMatrix()
 #---------------------------------нормали к вершинам боковых граней-------------------------------------
    #nrms = []  # Координаты нормалей к граням (рассчитываются для каждой вершины)
    if (indexnormal %2 == 1):
        gl.glLineWidth(2)  # Задание толщины линии
        #нормали для верхних вершин
        gl.glBegin(gl.GL_LINES)
        k = -1
        gl.glColor3f(0, 0, 0)#белые линии
        for j in range(n):
            k += 1
            sn = nrms0[k]
            v = vrts[k][0]
            normal(v, sn)
        gl.glColor3f(0, 1, 0)#салатовые линии
        #k = -1
        for j in range(n):
            k += 1
            sn = nrms0[k]
            v = vrts[k][1]
            normal(v, sn)
        gl.glColor3f(0, 0, 1) #синий

        for j in range(n):
            k += 1
            sn = nrms0[k]
            v = vrts[k][2]
            normal(v, sn)
        gl.glColor3f(1, 0, 0) # красный

        for j in range(n):
            k += 1
            sn = nrms0[k]
            v = vrts[k][3]
            normal(v, sn)

        gl.glEnd()


    #------------------------------нормаль к верхней грани------------------------------
    for i in range(n):
        v0 = np.array(vrts_top[0])
        v1 = np.array(vrts_top[1])
        vn = np.array(vrts_top[n - 1])
        nrm_top = np.cross(v1 - v0, vn - v0)  # Нормаль к крышке
        nrm_top = nrm_top / np.linalg.norm(nrm_top)
        nrms_top.append(nrm_top)
    if (indexnormal % 2 == 1):
        gl.glBegin(gl.GL_LINES)
        k = -1
        gl.glColor3f(0.75, 0, 1)
        for i in range(ch):
            for j in range(n):
                k += 1
                sn = nrms_top[1]*2
                v = vrts[j][0]
                normal(v, sn)
        gl.glEnd()
    # ------------------------------векторное произведение для векторов нижней грани------------------------------
    for i in range(n):
        v0 = np.array(vrts_bottom[0])
        v1 = np.array(vrts_bottom[1])
        vn = np.array(vrts_bottom[n - 1])
        nrm_bottom = np.cross(v1 - v0, vn - v0)  # Нормаль к крышке
        nrm_bottom = nrm_bottom / np.linalg.norm(nrm_bottom)
        nrms_bottom.append(nrm_bottom)
    # ------------------------------вывод нормалей к нижней грани------------------------------
    if (indexnormal % 2 == 1):
        gl.glBegin(gl.GL_LINES)
        k = -1
        gl.glColor3f(0.75, 0, 1)
        for i in range(ch):
            for j in range(n):
                k += 1
                sn = nrms_bottom[1] * 2
                v = vrts[j][2]
                normal(v, sn)
        gl.glEnd()
#-------------------------------------вывод основания и установление текущего вектора нормали --------------------------------

    if (indexbase % 2 == 1):
        gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL)
        gl.glBegin(gl.GL_POLYGON)
        gl.glColor3d(1, 0, 0)
        for i in range(n):
            sn = nrms_top[1]
            #gl.glNormal3f(-sn[0], -sn[1], -sn[2]) #если + то тень, - все тоже
            gl.glNormal3f(sn[0], sn[1], sn[2])
            gl.glNormal3f(1, 0, 0)
            gl.glVertex3f(vrts_top[i][0], h1, vrts_top[i][2])
        gl.glEnd()
    if (indexbase % 2 == 1):
        gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL)
        gl.glBegin(gl.GL_POLYGON)
        gl.glColor3d(0, 1, 0)
        for i in range(n):
            sn = nrms_bottom[1]
            gl.glNormal3f(sn[0], sn[1], sn[2])
            gl.glVertex3f(vrts_bottom[i][0], -h1, vrts_bottom[i][2])
        gl.glEnd()

    gl.glMaterialfv(gl.GL_FRONT, gl.GL_SPECULAR, mtClr)
    gl.glMaterialfv(gl.GL_FRONT, pyglet.gl.GL_DIFFUSE, mtClr)
#-------------------------------освещенность--------------------------
    # источник света 1
    if (indexsource % 2 == 1):
        gl.glDisable(gl.GL_LIGHT0)
    else:
        gl.glPointSize(10)
        gl.glBegin(gl.GL_POINTS)
        gl.glColor3d(lghtClr0[0], lghtClr0[1], lghtClr0[2])
        #light_position0 = [vrts_top[0][0], vrts_top[0][1], vrts_top[0][2], 0]
        gl.glVertex3f(light_position0[0], light_position0[1], light_position0[2])
        gl.glEnd()
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_POSITION, light_position)
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_SPECULAR, lghtClr)  # отраженное/зеркальное освещение
        glLightf(GL_LIGHT0, GL_SPOT_CUTOFF, 90)
        gl.glEnable(gl.GL_LIGHT0)
    #источник света 2
    gl.glPointSize(7)
    gl.glBegin(gl.GL_POINTS)
    gl.glColor3d(lghtClr1[0], lghtClr1[1], lghtClr1[2])
    light_position2 = [vrts_bottom[1][0]+10+x, vrts_bottom[1][1]+10+y, vrts_bottom[1][2]+10+ z, 0]
    gl.glVertex3f(light_position2[0], light_position2[1], light_position2[2])
    gl.glEnd()
    for i in range(4):
        light_position1[i] = light_position2[i]

    gl.glLightfv(gl.GL_LIGHT1, gl.GL_POSITION, light_position1)
    gl.glLightfv(gl.GL_LIGHT1, gl.GL_SPECULAR, lghtClr1)
    gl.glEnable(gl.GL_LIGHT1)

    # 3 источник
    glPushMatrix()
    glRotatef(n_rot, 0, 1, 0)
    gl.glPointSize(7)
    gl.glBegin(gl.GL_POINTS)
    gl.glColor3d(lghtClr03[0], lghtClr03[1], lghtClr03[2])
    gl.glVertex3f(light_position03[0], light_position03[1], light_position03[2])
    gl.glEnd()
    for i in range(4):
        light_position3[i] = light_position03[i]
    gl.glLightfv(gl.GL_LIGHT3, gl.GL_POSITION, light_position3)
    gl.glLightfv(gl.GL_LIGHT3, gl.GL_SPECULAR, lghtClr3)
    gl.glLightfv(gl.GL_LIGHT3, pyglet.gl.GL_DIFFUSE, lghtClr3)
    gl.glEnable(gl.GL_LIGHT3)
    glPopMatrix()



    @window.event
    def on_key_press(symbol, modifiers):
        global base, x, y, show_normal,indexbase, indexnormal,angle_x, angle_y,angle_z,indexrotate1,indexrotate2
        global x, y, z, indexdepthtest, indexCullFace, indexsource, indexLighting, indexnormalize
        global indexnormalize2, indexDiffuse

        mode_b = None
        if symbol == key._1:
            indexbase += 1 #Отключение / включение вывода оснований.
        elif symbol == key._2:
            indexnormal += 1#Включение / отключение отображения нормалей
        elif symbol == key._3: #Произвольное изменение ориентации фигуры 1 вариант
            #посмотреть нижнее основание
            angle_x = 30
            angle_y = 90
            angle_z = 0
            indexrotate1 +=1
        elif symbol == key._4:#Произвольное изменение ориентации фигуры 2 вариант
            #посмотреть верхнее основание
            angle_x = -45
            angle_y = 0
            angle_z = 90
            indexrotate2 += 1
        elif symbol == key._5:#Произвольное изменение положения одного источника света.
            #изменение положения одного источника света
            x = 10
            y = -10
            z = -10 #источник 2 на Ox
        elif symbol == key._5:
            #изменение положения одного источника света
            x = 10
            y = -10
            z = -10 #источник 2 на Ox
        elif symbol == key._6:#Отключение / включение теста глубины.
            indexdepthtest +=1
        elif symbol == key._7:#Отключение / включение режима отсечение нелицевых сторон.
            indexCullFace +=1
        elif symbol == key._8:#Отключение / включение неподвижного источника.
             indexsource += 1
        elif symbol == key._9:
             indexnormalize+=1 #9.Нормализацию / отказ от нормализации нормалей при их расчете.

        elif symbol == key.F1:#10.Нормализацию / отказ от нормализации нормалей посредством glEnable(GL_NORMALIZE).
             indexnormalize2+=1
        elif symbol == key.ENTER:#11.Отключение / включение режима расчета освещенности.
             indexLighting+=1
        elif symbol == key.F2:  #12.Отключение / включение компоненты материала GL_DIFFUSE.
             indexDiffuse += 1


app.run()

