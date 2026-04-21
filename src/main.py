import matplotlib
matplotlib.use('Agg')
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import image as img
from skimage import transform as tf
import cv2

print("chargement de l'image")
I = img.imread('images/a.tif')
print(np.mean(I))
rows, cols= I.shape
print("rows="+str(rows)+" cols="+str(cols))

plt.figure(1)
plt.imshow(I,cmap="gray")
plt.title("01887u")
plt.axis('off')
#plt.show()



#Appliquer une translation à une image (Python)
def translation (I, a, b):
    tform = tf.EuclideanTransform(rotation=0, translation= (a,b))
    #print("ok")
    return (tf.warp(I, tform))


#Pour diviser l'image en 3 parties égales
def division(im): 
    height,width = im.shape
    #print("Height:", height, "Width: ", width)
    div_height = height//3


    print(div_height)

    

    part1 = im[0:div_height, :]
    part2 = im[div_height: 2*div_height, :]
    part3 = im[2*div_height:3*div_height, :]

    plt.imsave('part1.png', part1)
    plt.imsave('part2.png', part2)
    plt.imsave('part3.png', part3)

    
    fig, axs = plt.subplots(3, 1, figsize=(5, 5))  

    # Afficher chaque partie
    axs[0].imshow(part1)
    axs[0].set_title("Partie 1")
    axs[0].axis('off')  

    axs[1].imshow(part2)
    axs[1].set_title("Partie 2")
    axs[1].axis('off')  

    axs[2].imshow(part3)
    axs[2].set_title("Partie 3")
    axs[2].axis('off')  

    plt.show()

    return part1, part2, part3


#Pour recaler 2 images en utilisant la translation
def recalage(image1, image2, max_translation):
    meilleure_translation = (0, 0)
    meilleure_info = 0
    meilleure_image = image2

    # Parcourir toutes les combinaisons de translations
    for a in range(-max_translation, max_translation + 1):
        for b in range(-max_translation, max_translation + 1):
            print("Calcul")
            # Appliquer la translation à image2
            translated_image2 = translation(image2, a, b)

            # Calcul de l'info mutuelle
            hist_2d, _, _ = np.histogram2d(
                image1.ravel(),
                translated_image2.ravel(),
                bins=20
            )
            info_mutuelle = mutual_information(hist_2d)

            # Mettre à jour si une meilleure translation est trouvée
            if info_mutuelle > meilleure_info:
                meilleure_info = info_mutuelle
                meilleure_translation = (a, b)
                meilleure_image = translated_image2

    plt.figure(1)
    plt.imshow(translated_image2)
    plt.title("Image translateee de 2")
    plt.axis('off')
    #plt.show()

    return meilleure_image


#SSD
def ssd(I,J):
    return np.sum((np.array(I, dtype=np.float32) - np.array(J, dtype=np.float32))**2)


#Dans la doc fourni par le prof avec une petite modif au niveau de l'entrée
def mutual_information(hgram):
    ## Mutual information for joint histogram
    ##
    # Convert bins counts to probability values
    pxy = hgram / float(np.sum(hgram))
    px = np.sum(pxy, axis=1) # marginal for x over y
    py = np.sum(pxy, axis=0) # marginal for y over x
    px_py = px[:, None] * py[None, :] # Broadcast to multiply marginals
    # Now we can do the calculation using the pxy, px_py 2D arrays
    nzs = pxy > 0 # Only non-zero pxy values contribute to the sum
    return np.sum(pxy[nzs] * np.log(pxy[nzs] / px_py[nzs]))


#Pour fusionner les 3 images
def fusionner_images(par1, par2, par3):
    min_width = min(par1.shape[1], par2.shape[1], par3.shape[1])

    height = par3.shape[0]
    print(height, min_width)
    image_fusionnee = np.zeros((height, min_width, 3), dtype=np.int32)

    #image_fusionnee[:, :, 2]=par1[:, :min_width]
    image_fusionnee[:, :, 0]=par3[:, :min_width]
    image_fusionnee[:, :, 1]=par2[:, :min_width]
    image_fusionnee[:, :, 2]=par1[:, :min_width]
    

    #plt.imsave('imagefusionnee.png', image_fusionnee)
    
    plt.figure(4)
    plt.imshow(image_fusionnee)
    plt.title("Image Fusionnée")
    plt.savefig('resultat_final.png')
    # plt.show()
    
    #return image_fusionnee



one,two,three = division (I)
#print(one.shape, two.shape, three.shape)
recalage2= recalage(one, two,1)
recalage3=recalage(one, three,1)

#print("tchêpo  ssd:", ssd(recalage2,two))

#recalage2 = alignement_multi_echelle(one, two, 5, niveaux=3)
#recalage3 = alignement_multi_echelle(one, three, 5, niveaux=3)


#print(recalage2.shape, recalage3.shape)

plt.imsave('Image2Recalee.png', recalage2)
plt.imsave('Image3Recalée.png', recalage3)

fusionner_images(one, recalage2, recalage3)




#hist_2d, x_edges, y_edges = np.histogram2d(
#    one.ravel(),
#    two.ravel(),
#    bins=20)
#plt.imshow(hist_2d.T, origin='lower')
#plt.show()


#print("L'information mutuelle est:",mutual_information(hist_2d))
#print ("La SSD est : ",ssd(one,two))