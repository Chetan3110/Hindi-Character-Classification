# -*- coding: utf-8 -*-
"""chetan.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1r8WdlsFAlqUxwTsrVSueBFBn5jirryjT
"""

import numpy as np # linear algebra
import os
import json
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split

from google.colab import drive
drive.mount('/content/drive')

from tensorflow.keras.layers import Input, Lambda, Dense, Flatten
from tensorflow.keras.models import Model
from keras.applications.vgg16 import VGG16
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator,load_img
from tensorflow.keras.models import Sequential
import numpy as np
from glob import glob

IMAGE_SIZE = [64, 64]

train_path = '/content/drive/MyDrive/dataset/training'
valid_path = '/content/drive/MyDrive/dataset/test'

vgg = VGG16(input_shape=IMAGE_SIZE + [3], weights='imagenet', include_top=False)

for layer in vgg.layers:
  layer.trainable = False

folders = glob('/content/drive/MyDrive/dataset/training/*')

x = Flatten()(vgg.output)

prediction = Dense(len(folders), activation='softmax')(x)

model = Model(inputs=vgg.input, outputs=prediction)

model.summary()

model.compile(
  loss='categorical_crossentropy',
  optimizer='adam',
  metrics=['accuracy']
)

from keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(rescale = 1./255,
                                   shear_range = 0.2,
                                   zoom_range = 0.2,
                                   horizontal_flip = True)
test_datagen = ImageDataGenerator(rescale = 1./255)

training_set = train_datagen.flow_from_directory('/content/drive/MyDrive/dataset/training',
                                                 target_size = (64 , 64),
                                                 batch_size = 32,
                                                 class_mode = 'categorical')

test_set = test_datagen.flow_from_directory('/content/drive/MyDrive/dataset/test',
                                            target_size = (64 , 64),
                                            batch_size = 32,
                                            class_mode = 'categorical')

r = model.fit(
  training_set,
  validation_data=test_set,
  epochs=16,
  steps_per_epoch=len(training_set),
  validation_steps=len(test_set)
)

test_images = []

for img in os.listdir(valid_path):
    test_image = plt.imread(os.path.join(valid_path,img))
    test_images.append(test_image.reshape([64,64,3]))
test_images = np.array(test_images)

final_preds=[]
model_predictions = model.predict(test_images)
for i in model_predictions:
    if (i >= 1).all:
        final_preds.append(1)
    if (i < 1).all:
        final_preds.append(0)

dictio={}
for i,j in enumerate(os.listdir(valid_path)):
    dictio[j] = final_preds[i]

def write_json(filename, result):
    with open(filename, 'w') as outfile:
        json.dump(result, outfile)

def generate_sample_file(filename):
    write_json(filename, dictio)


generate_sample_file('./hackathonresult.json')