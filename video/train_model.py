# Dépendances 
import torch
from torch.autograd import Variable
from PIL import Image
import os
import pandas as pd
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
import numpy as np

# Fonction de récupération des features dans une image
def get_vector(image_name):

    # Charger une image avec la librarie Pillow
    img = Image.open(image_name)
    # Créer une variable Pytorch afin de 
    t_img = Variable(normalize(to_tensor(scaler(img))).unsqueeze(0))
    # Créer un vecteur de 0 qui contiendra les features 
    my_embedding = torch.zeros(512)
    # Définir une fonction qui copy les résultats dans les couches
    def copy_data(m, i, o):
        my_embedding.copy_(o.data.reshape(o.data.size(1)))
    h = layer.register_forward_hook(copy_data)
    # Lancer le modèle sur l'image 
    model(t_img)
    h.remove()
    # Renvoyer les features
    return my_embedding.numpy()

# Fonction qui boucle sur toutes les images d'un jeu de données
def features_train(directory):

    # On instancie les listes qui stockeront les informations
    features = []
    totaldir = []
    y = []
    
    no_damage = os.listdir(directory)
    for i in no_damage :
        totaldir.append(str(directory + i))
        y.append(i.split(".")[0])

    # Récupération des features dans les images
    for dir in totaldir : 
        features.append(get_vector(dir))

    features = pd.DataFrame(features)

    return features, y


# Chemin des différents datasets
photos = "./photos/"

# Charger un modèle pré-entraîné
model = models.resnet18(pretrained=True)

# Utiliser ce modèle pour obtenir la couche qui nous intérésse
layer = model._modules.get('avgpool')

# Evaluer ce modèle
model.eval()

# Transformer les images dans le bon format, normalisation et conversion en Tenseur
scaler = transforms.Resize((150, 150))
normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
to_tensor = transforms.ToTensor()

X_train, y_train = features_train(photos)

np.save('./extract_features/reference_data.npy', X_train)
np.save('./extract_features/reference_names.npy', y_train)