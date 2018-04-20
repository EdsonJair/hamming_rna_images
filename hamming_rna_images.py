import cv2 as cv
import numpy as np

cero_one = cv.imread('cero_1.jpg', 0)
cero_two = cv.imread('cero_2.jpg', 0)
cero_tree = cv.imread('cero_3.jpg', 0)
cero_four = cv.imread('cero_4.jpg', 0)
cero_five = cv.imread('cero_5.jpg', 0)

one_one = cv.imread('uno_1.jpg', 0)
one_two = cv.imread('uno_2.jpg', 0)
one_tree = cv.imread('uno_3.jpg', 0)
one_four = cv.imread('uno_4.jpg', 0)
one_five = cv.imread('uno_5.jpg', 0)

two_one = cv.imread('dos_1.jpg', 0)
two_two = cv.imread('dos_2.jpg', 0)
two_tree = cv.imread('dos_3.jpg', 0)
two_four = cv.imread('dos_4.jpg', 0)
two_five = cv.imread('dos_5.jpg', 0)

tree_one = cv.imread('tres_1.jpg', 0)
tree_two = cv.imread('tres_2.jpg', 0)
tree_tree = cv.imread('tres_3.jpg', 0)
tree_four = cv.imread('tres_4.jpg', 0)
tree_five = cv.imread('tres_5.jpg', 0)

train_images = [cero_one, cero_two, cero_tree, cero_four, cero_five,
                two_one, two_two, two_tree, two_four, two_five, one_one, one_two, one_tree, one_four, one_five,
                tree_one, tree_two, tree_tree, tree_four, tree_five]
'''cambiar valores de 0 - 255 a -1 y 1'''
bipolar_images = []
for i in train_images:
    vector_imagen = np.ravel(i)
    bipolar_images.append(vector_imagen)
i = 0
j = 0

w = np.zeros([len(train_images), len(bipolar_images[0])])
wi = np.zeros([len(train_images), len(bipolar_images[0])])
print(len(bipolar_images[0]))
for i in range(len(train_images)):
    for j in range(len(bipolar_images[0])):
        if (bipolar_images[i][j] < 240):
            wi[i, j] = -1 / 2
        else:
            wi[i, j] = 1 / 2

w = +wi
print("++++++++  Matrices   De   Pesos: ++++++")
print(w)

vias = []
for i in range(len(train_images)):
    valor_vias = len(bipolar_images[i]) / 2
    vias.append(valor_vias)
vias = np.array(vias).reshape(len(train_images), 1)
print("+++++++++++  VIAS: +++++++++++++")
print(vias)

#####    Patron   ######
prueba = train_images[1]  ### ACA SE AGREGA LA PRUEBA
cv.imshow("PRUEBA", prueba)
vector_prueba = []
for x in range(0, prueba.shape[0]):
    for y in range(0, prueba.shape[1]):
        if prueba[x][y] < 240:
            valor_prueba = -1
        else:
            valor_prueba = 1
        vector_prueba.append(valor_prueba)

##############  PRUEBA   #######
patron = np.array(vector_prueba).reshape(1, len(vector_prueba))
patron_t = np.transpose(patron)
u = np.dot(w, patron_t) + vias

u0 = []
for i in u:
    j = i * (1 / len(bipolar_images[0]))
    u0.append(j)
u0 = np.array(u0).reshape(1, len(train_images))
# print("u0",u0)

###FUNCION DE TRANSFERENCIA
x = 0
y1 = []
for x in u0:
    if x.all() > 1:
        y1.append(1)
    elif x.all() >= 0 or x.all() <= 1:
        y1.append(x)
    else:
        y1.append(0)
y1 = np.array(y1).reshape(u0.shape)
y1_1 = y1[0]
convergencia = False
E = (1 / (len(bipolar_images[0]) - 1))
c = 0
suma = 0
aux = 0
n_iter = 1
while convergencia != True:
    y = []
    y0 = []
    for j in range(len(y1_1)):
        suma += y1_1[j]
    for i in range(len(y1_1)):
        value = y1_1[i] - (E * (suma - y1_1[i]))
        y0.append(value)

    for x in y0:
        if x > 1:
            y.append(1)
        elif x >= 0 and x <= 1:
            y.append(x)
        else:
            y.append(0)
    veces = y.count(0)
    if veces == (len(y) - 1):
        convergencia = True
        maximo = max(y)
        posicion = y.index(maximo)
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        # print(y,"iteracion",n_iter)
        print("La red converge y asocia con el patron", posicion, train_images[posicion])
        cv.imshow("Asocia", train_images[posicion])
    else:
        y1_1 = y
        # print(y1_1,"iteracion",n_iter)
        n_iter += 1
        suma = 0
        maximo = max(y1_1)
        valor = y1_1.count(maximo)
        if (valor >= 2):
            print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            print("La red NO converge y NO asocia con NINGUN patron porque tienes mas de un valor igual")
            print(y1_1)
            break
cv.waitKey()
cv.destroyAllWindows()
