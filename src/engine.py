import numpy as np
from matplotlib import pyplot as plt
from matplotlib import image as img
from utils import *

from timeit import default_timer as timer
import time



#start=timer()



print("chargement de l'image ..........................................")
I = img.imread('../data/raw/00998u.tif')
print(I.shape)
print(np.mean(I))
rows, cols= I.shape
#img_np = asarray(I)
#print(img_np.shape[0])
#print("Img to numpy", asarray(I))
#print(I.shape)
print("rows="+ str(rows)+" cols="+str(cols))

plt.figure(1)
plt.imshow(I, cmap="gray")
plt.title("01887u")
plt.axis('off')
#plt.show()


'''
I_trans = translation(I, -1000, -1000)
plt.figure(2)
plt.imshow(I_trans, cmap="gray")
plt.title("Image transformée")
plt.axis('off')
'''

#Separation des composantes B, G, R
B_comp, G_comp, R_comp = splitImg(I,250,250)
plt.figure(2)
plt.subplot(1, 3, 1)
plt.imshow(B_comp, cmap = "gray")
plt.title("composante B")

plt.subplot(1, 3, 2)
plt.imshow(G_comp, cmap = "gray")
plt.title("composante G")

plt.subplot(1, 3, 3)
plt.imshow(R_comp, cmap = "gray")
plt.title("composante R")




#Recalage des 3 composantes
begin=time.time()
G_comp_recal = recalageM(B_comp, G_comp, 5)
end=time.time()
print("Total runtime:",end-begin)
plt.figure(3)
plt.subplot(1, 2, 1)
plt.imshow(G_comp_recal, cmap = "gray")
plt.title("composante G recalée")

#print("PSNR:", calculate_psnr(G_comp,G_comp))

begin=time.time()
R_comp_recal = recalageM(B_comp, R_comp, 5)
end=time.time()
print("Total runtime:",end-begin)
plt.figure(3)
plt.subplot(1, 2, 2)
plt.imshow(R_comp_recal, cmap = "gray")
plt.title("composante R recalée")

plt.imsave('../data/output/ImageGRecalee.png', G_comp_recal)
plt.imsave('../data/output/ImageRRecalée.png', R_comp_recal)

#Concatenation des composantes
imgGl = np.zeros((B_comp.shape[0], B_comp.shape[1], 3), dtype = np.int32)
imgGl[:, :, 0] = R_comp_recal
imgGl[:, :, 1] = G_comp_recal
imgGl[:, :, 2] = B_comp

plt.figure(4)
plt.imshow(imgGl)
plt.title("composante Resultante")

#end=timer()
#print("Temps pour realiser ce travail: " + str(end - start))



plt.show()