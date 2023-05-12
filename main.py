import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import numpy as np
import matplotlib.pyplot as plt
from tensorflow import keras
import keras.backend as K
import time
from keras.models import load_model
import random
from sklearn.preprocessing import StandardScaler # Стандартизация данных

#--------------------const--------------------------
num_classes = 2
n1 = 1000 #элементов 1 множества
n2 =1000 #элементов 2 множества
myclass1 = 0
myclass2 = 1
numberepochs =10 #2
isBiasUse = False
fl_standart = False
suff = '.txt'
pathToData = 'C:\\Users\\Мария\\PycharmProjects\\Lab8'
fn_model1 = pathToData +'m1'+ 'lk3.h5'
pathToHistory = 'C:\\Users\\Мария\\PycharmProjects\\Lab8\\'
# Имена файлов, в которые сохраняется история обучения
fn_loss = pathToHistory + 'loss_' + suff
fn_acc = pathToHistory + 'acc_' + suff
fn_val_loss = pathToHistory + 'val_loss_' + suff
fn_val_acc = pathToHistory + 'val_acc_' + suff

def generateData( n, x1, x2, y1, y2, myclass):
    set = np.zeros(shape=(n, 2), dtype=float)
    for i in range(n):
        set[i][0] = random.uniform(x1, x2)
        set[i][1] = random.uniform(y1, y2)
    y = np.array([myclass] * n)
    return set, y

def generateDataSet(bufn1, bufn2):
    set1, y1 = generateData(bufn1, 0, 2, 2, 4, myclass1)
    set2, y2 = generateData(bufn2, 3, 5, 0, 2, myclass2)
    set = np.concatenate((set1, set2))
    y = np.concatenate((y1, y2))
    return set, y

def PaintSET(set, bufn1, bufn2, message):
    plt.figure(message)
    for i in range(bufn1):
        x1= set[i][0]
        y1= set[i][1]
        plt.plot(x1, y1, 'r^')
    for i in range(bufn1, bufn1+bufn2):
        x2 = set[i][0]
        y2 = set[i][1]
        plt.plot(x2, y2, 'b^')
    plt.show()

def func_y(x):
    n = len(x)
    y = np.zeros(shape=(n), dtype=float)
    # получить веса
    weights = model1.layers[0].get_weights()
    w1 = weights[0][0][0]
    w2 = weights[0][1][0]
    if (not (isBiasUse)):
        bias = 0
    else:
        bias = weights[1][0]
        print("bias: ", bias)
    print("w1: ", w1)
    print("w2: ", w2)

    for i in range (n):
        if (w2 !=0):
            y[i] = -bias / w2 - w1 / w2 * x[i]
        else:
             print("попытка деления на 0")
    return y
def Standart(set):
    scaler = StandardScaler(copy=False).fit(set)  # fit- вычисляет среднее значение и стандартное отклонение (для стандартизации)
    set = scaler.transform(set)  # Стандартизация за счет центрирования и масштабирования
    return set
def OutputSetLine(set):
    plt.figure("обучающее множество")
    for i in range(n1):
        x1 = set[i][0]
        y1 = set[i][1]
        plt.plot(x1, y1, 'r^')
    for i in range(n1, n1 + n2):
        x2 = set[i][0]
        y2 = set[i][1]
        plt.plot(x2, y2, 'b^')
def WriteHistorytoTextFile(history_buf):
    with open(fn_loss, 'w') as output:
        for val in history_buf['loss']:output.write(str(val) + '\n')
    with open(fn_acc, 'w') as output:
        for val in history_buf['accuracy']: output.write(str(val) + '\n')
    with open(fn_val_loss, 'w') as output:
        for val in history_buf['val_loss']: output.write(str(val) + '\n')
    with open(fn_val_acc, 'w') as output:
        for val in history_buf['val_accuracy']: output.write(str(val) + '\n')
def one_plot(n, y_lb, loss_acc, val_loss_acc):
    plt.subplot(1, 2, n)
    if n == 1:
        lb, lb2 = 'loss', 'val_loss'
        yMin = 0
        yMax = 1.05 * max(max(loss_acc), max(val_loss_acc))
    else:
        lb, lb2 = 'acc', 'val_acc'
        yMin = min(min(loss_acc), min(val_loss_acc))
        yMax = 1.0
    plt.plot(loss_acc, color = 'r', label = lb, linestyle = '--')
    plt.plot(val_loss_acc, color = 'g', label = lb2)
    plt.ylabel(y_lb)
    plt.xlabel('Эпоха')
    plt.ylim([0.95 * yMin, yMax])
    plt.legend()
def BuildPlot(history):
    plt.figure(figsize=(9, 4))
    plt.subplots_adjust(wspace=0.5)
    one_plot(1, 'Потери', history['loss'], history['val_loss'])
    one_plot(2, 'Точность', history['accuracy'], history['val_accuracy'])
    plt.suptitle('Потери и точность')
    plt.show()

def predict(n_test, predicted_classes, true_classes, m, lst_false, m_max, false_classified, model):
    #print('Индекс  | Прогноз  |  Правильный класс')
    for i in range(n_test):  #
        cls_pred = predicted_classes[i]  # Предсказанное моделью имя класса
        cls_true = true_classes[i]  # Истинное имя класса
        if cls_pred != cls_true:
            m += 1
            lst_false.append([i, cls_pred, cls_true])
            if (m == min(m_max, false_classified)): break
            print("%-i%10i%10i" % (i, cls_pred, cls_true))

def Forecast(fn_model_x, fl_standart):
    model = load_model(fn_model_x)
    score = model.evaluate(x_test, y_test, verbose = 0)
    print('Потери при тестировании:', round(score[0], 4))
    print('Точность при тестировании: {}{}'.format(score[1] * 100, '%'))
    y_pred = model.predict(x_test) #метки классов, предсказанных моделью НС
    pred = np.round(y_pred.flatten()) #округляет сплющенный в одинарный массив
    plt.figure("прогноз на проверочном множестве")
    plt.plot(x_test[pred == 0, 0], x_test[pred == 0, 1], 'r^')
    plt.plot(x_test[pred == 1, 0], x_test[pred == 1, 1], 'b^')

    if (fl_standart):
        x = np.linspace(-1.5, 1.5, 2)
    else:
        x = np.linspace(0, 5, 2)
    plt.plot(x, func_y(x),
         linestyle='-',
         linewidth=1,
         color='crimson')

    plt.show()

    predicted_classes = np.array([np.argmax(m) for m in y_pred])
    true_classes = np.array([np.argmax(m) for m in y_test])
    n_test = len(y_test)
    print("Всего изображений в тестовой выборке: ", n_test)
    true_classified = np.sum(predicted_classes == true_classes)
    print("Число верно классифицированных элементов: ", true_classified)
    false_classified = n_test - true_classified
    acc = 100.0 * true_classified / n_test
    print('Точность: {}{}'.format(acc, '%'))
    m, m_max = 0, 15
    lst_false = []
    i = 0
    predict(n_test, predicted_classes, true_classes, m, lst_false, m_max, false_classified, model)


#------------------------------------------------------main------------------------------------------------------------
#флажки
fl_standart = True
#fl_standart = False
isBiasUse = False
#isBiasUse = True

set, y = generateDataSet(n1, n2)
PaintSET(set, n1, n2, "обучающее множество после генерации")
num_elem_set = len (set[:, 0])
print("количество данных в обучающем множестве: ", num_elem_set )

if (fl_standart):
    set = Standart(set)
PaintSET(set, n1, n2, "обучающее множество после стандартизации")

n1_test = int(1/4 * n1) #кол-во элементов в тестовом множестве
n2_test = int(1/4 * n2)
n_test = n1_test + n2_test
set_test, y_test = generateDataSet(n1_test, n2_test)
PaintSET(set_test, n1_test, n2_test, "тестовое множество после генерации")
if (fl_standart):
    set_test = Standart(set_test)
PaintSET(set_test, n1_test, n2_test, "тестовое множество после стандартизации")
print ("количество данных в тестовом множестве:", len (set_test[:, 0]))

x_train, y_train = set, y
x_test, y_test = set_test, y_test

#---------------------------------
K.clear_session()
size = 2
x_train = x_train.reshape(-1, 2)
x_test = x_test.reshape(-1, 2)
input_shape = (2)  # 784

model1 = keras.models.Sequential()
model1.add(keras.layers.Dense(1, input_dim=2, activation='sigmoid', use_bias=isBiasUse))
print(model1.summary())
model1.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

start = time.time()
history = model1.fit(
 x_train,
y_train,
batch_size=32,
epochs=numberepochs,
validation_data=(x_train.reshape(-1, 2 * 1), y_train)

)
# end = time.time()
# weights = model1.layers[0].get_weights()
# # print(weights[0][0][0])
# # print(weights[0][1][0])




# model2 = load_model(fn_model1)
# weights = model2.layers[0].get_weights()
# print(weights[0][0][0])
# print(weights[0][1][0])
# exit()
#
# print("Прогноз ")
# Forecast(fn_model1, fl_standart)




