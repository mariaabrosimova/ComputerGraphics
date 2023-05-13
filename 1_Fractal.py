import numpy as np
import pandas as pd
import random
from pyglet import app
from pyglet.window import Window
from pyglet.gl import *
C = pd.DataFrame({
                  'a': [0.04, -0.02, 0.79, -0.03],
                  'b': [0.22, 0.0, 0.06, -0.3],
                  'c': [0.31, -0.32, -0.03, 0.35],
                  'd': [-0.03, 0.26, 0.73, -0.04],
                  'e': [0.63, -0.17, -0.02, -0.68],
                  'f': [-1.74, -1.35, 1.03, -0.94],
                  'probability': [0.13, 0.01, 0.74, 0.12]})


print("СИФ: ")
print(C)
probability = C['probability'].to_numpy()
#аффинное преобразование:
def point(bufx, bufy, C) :
        N = random.choices(C.index, probability)[0]
        bufx = bufx * C.iloc[N]['a'] + bufy * C.iloc[N]['b'] + C.iloc[N]['e']
        bufy = bufx * C.iloc[N]['c'] + bufy * C.iloc[N]['d'] + C.iloc[N]['f']
        #print(bufx, bufy)
        return bufx, bufy

number=70000; #количество точек
arr = np.empty((number, 2), dtype=object) #массив координат точек
# произвольная точка:
x0 = 0
y0 = 0
#начальная точка:
for i in range(100):
    buffer = point(x0, y0, C)
    x0 = buffer[0]
    y0 = buffer[1]

for i in range(number):
    buffer = point(x0, y0, C)
    x0 = buffer[0]
    y0 = buffer[1]
    arr[i, 0] = x0
    arr[i, 1] = y0
print("наш массив точек", arr)

#для определения в какой области находятся точки:
xmax = max(arr[:, 0])
xmin = min(arr[:, 0])
ymax = max(arr[:, 1])
ymin = min(arr[:, 1])
print("xmin", xmin)
print("ymin", ymin)
print("xmax", xmax)
print("ymax", ymax)
#каждой точке постараемся поставить в соотношение пиксель, для этого нужно осуществить их сдвиг:
for i in range(number):
    if ymin < 0:# координата пикселя не может быть отрицательной, поэтому осуществляем сдвиг
        arr[i, 1] += abs(ymin)+0.5
    if xmin < 0:
        arr[i, 0] += abs(xmin) +3
    arr[i, 0] *= 100  # координату 0.06, чтобы можно было приблизить целым числом (для индексации matrix), нужно *100
    arr[i, 1] *= 100

print("после сдвига точек")
print(arr)
W=1000
H=1000
matrix = np.full((W, H), 1, dtype='uint8')
for i in range(number):
    matrix[int(arr[i, 0])][int(arr[i, 1])] = 255
#преобразование двумерного массива к одномерному для использования ф-ии glDrawPixels
matrix = matrix.flatten()
matrix = (GLubyte * (W*H))(*matrix)
#создание окна
window = Window(visible = True, width = W, height = H,resizable=True, caption='лист')
window.set_location(0, 30)
#window = pyglet.window.Window(fullscreen=True )
@window.event
def on_draw():
    glDrawPixels(W, H, GL_GREEN, GL_UNSIGNED_BYTE, matrix)
app.run()




