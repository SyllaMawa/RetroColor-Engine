from matplotlib import pyplot as plt
from skimage import transform as tf
from numpy import asarray
import numpy as np
from skimage.transform import pyramid_gaussian
from PIL import Image 

import math

#Translation d'image
def translation(I, a , b):
      tform = tf.EuclideanTransform(rotation=0, translation=( a, b)) #ATTENTION X ET Y SONT INVERSES
      #return(tf.warp(I, tform))
      return(tf.warp(I, tform))


def normalize(img):
    return (img - np.mean(img)) / np.std(img)


#Division de l'image en 3 parties égales
#def splitImg(img):
#      img_np = asarray(img)
#      same_height = img_np.shape[0] // 3
#      same_width = img_np.shape[1]
#      R_comp = np.eye(same_height, same_width)
#      B_comp = np.eye(same_height, same_width)
#      G_comp = np.eye(same_height, same_width)

#      print(f"Same height: {same_height}")
#      print(f"Same width: {same_width}")

#      for i in range(same_height):
#            for j in range(same_width):
#                B_comp[i][j] = img_np[i][j]
#                G_comp[i][j] = img_np[i + same_height][j]         #G_comp[i][j] = img_np[i + same_height + 1][j]
#                R_comp[i][j] = img_np[i + 2 * same_height][j]     #R_comp[i][j] = img_np[i + 2 * same_height + 1][j]

#      plt.imsave('B_comp.png', B_comp, cmap="gray")
#      plt.imsave('G_comp.png', G_comp, cmap="gray")
#      plt.imsave('R_comp.png', R_comp, cmap="gray")

      #On retourne les composantes B, G, R de l'image
#      return B_comp, G_comp, R_comp 


def splitImg(img, al1, al2):
    img_np = asarray(img)
    same_height = img_np.shape[0] // 3
    same_width = img_np.shape[1]
    R_comp = np.zeros((same_height, same_width))
    B_comp = np.zeros((same_height, same_width))
    G_comp = np.zeros((same_height, same_width))

    print(f"Same height: {same_height}")
    print(f"Same width: {same_width}")

    for i in range(same_height):
        for j in range(same_width):
            B_comp[i][j] = img_np[i][j]
            G_comp[i][j] = img_np[i + same_height][j]         #G_comp[i][j] = img_np[i + same_height + 1][j]
            R_comp[i][j] = img_np[i + 2 * same_height][j]     #R_comp[i][j] = img_np[i + 2 * same_height + 1][j]

    #Resizer les images
    B = Image.fromarray(B_comp)
    G = Image.fromarray(G_comp)
    R = Image.fromarray(R_comp)

    crop_box = (al1, al2, same_width - al1, same_height - al2)

    B_cropped = B.crop(crop_box)
    G_cropped = G.crop(crop_box)
    R_cropped = R.crop(crop_box)

      #On retourne les composantes B, G, R de l'image
    #return B_comp, G_comp, R_comp 
    return np.array(B_cropped), np.array(G_cropped), np.array(R_cropped)



#Critere de similarité
#Information mutuelle
def histo_mut(img1, img2):
      img_np1 = asarray(img1)
      img_np2 = asarray(img2)
      H, _, _ = np.histogram2d(img_np1.ravel(), img_np2.ravel(), density = True)
      return H



def mutual_information(hgram):
    """ Mutual information for joint histogram
    """
    # Convert bins counts to probability values
    pxy = hgram / float(np.sum(hgram))
    px = np.sum(pxy, axis=1) # marginal for x over y
    py = np.sum(pxy, axis=0) # marginal for y over x
    px_py = px[:, None] * py[None, :] # Broadcast to multiply marginals
    # Now we can do the calculation using the pxy, px_py 2D arrays
    nzs = pxy > 0 # Only non-zero pxy values contribute to the sum
    return np.sum(pxy[nzs] * np.log(pxy[nzs] / px_py[nzs]))




def recalage(img1, img2):
      
      max_MI = 0.1
      a = 0
      b = 0
      max_b = 2
      min_b = -2
      max_a = 2
      min_a = -2
      
      for a in range(min_b, max_b):
            for b in range(min_a, max_a):
                  img_trans = translation(img2, a, b)
                  H = histo_mut(img1, img_trans)
                  MI = mutual_information(H)
                  if(MI >= max_MI):
                        img2 = img_trans

      return img2, (img2 - img1)



def recalageM(image1, image2, max_translation):
    meilleure_translation = (0, 0)
    meilleure_info = 0

    # Parcourir toutes les combinaisons de translations
    for a in range(-max_translation, max_translation + 1):
        for b in range(-max_translation, max_translation + 1):
            print("..................................\n")
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

    '''plt.figure(1)
    plt.imshow(translated_image2)
    plt.title("Image translateee de 2")
    plt.axis('off')
    plt.show()
      '''
    return translated_image2

def ssd(img1, img2):
    return np.sum((img1 - img2) ** 2)

def recalageM_ssd(image1, image2, max_translation):
    meilleure_translation = (0, 0)
    meilleure_ssd = float('inf')

    for a in range(-max_translation, max_translation + 1):
        for b in range(-max_translation, max_translation + 1):
            translated_image2 = translation(image2, a, b)
            current_ssd = ssd(image1, translated_image2)

            if current_ssd < meilleure_ssd:
                meilleure_ssd = current_ssd
                meilleure_translation = (a, b)

    dx_final, dy_final = meilleure_translation
    image_recalee = translation(image2, dx_final, dy_final)
    return image_recalee

def correlation_coefficient(img1, img2):
    img1_mean = np.mean(img1)
    img2_mean = np.mean(img2)
    numerator = np.sum((img1-img1_mean)*(img2 - img2_mean))
    denominator = np.sqrt(np.sum((img1-img1_mean)**2) * np.sum((img2-img2_mean)**2))
    return numerator / denominator if denominator != 0 else 0

# Recalage utilisant le coefficient de corrélation
def recalageM_corr(image1, image2, max_translation):
    meilleure_translation = (0, 0)
    meilleure_correlation = -1 

    for a in range(-max_translation, max_translation + 1):
        for b in range(-max_translation, max_translation + 1):
            translated_image2 = translation(image2, a, b)
            current_corr = correlation_coefficient(image1, translated_image2)

            if current_corr > meilleure_correlation:
                meilleure_correlation = current_corr
                meilleure_translation = (a, b)

    dx_final, dy_final = meilleure_translation
    image_recalee = translation(image2, dx_final, dy_final)
    return image_recalee



def calculate_psnr(original, recal):
    mse = np.mean((original - recal) ** 2)
    if mse == 0:
        return float('inf')  # Pas d'erreur, PSNR infini
    max_pixel = 255.0  # Valeur maximale pour des images sur 8 bits
    psnr = 20 * math.log10(max_pixel / math.sqrt(mse))
    return psnr



