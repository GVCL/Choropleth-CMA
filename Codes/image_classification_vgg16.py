# -*- coding: utf-8 -*-
"""map_image_classification_complete.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1_OSN9biTC5_pIlg5LpS9ahXHWggNZqqg
"""

from keras.layers import Input, Lambda, Dense, Flatten
from keras.models import Model
from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
import numpy as np
from keras.models import load_model
from glob import glob
import matplotlib.pyplot as plt
import os
import cv2

from google.colab import drive
drive.mount('/content/drive')

IMAGE_SIZE = [224,224]

train_path = '/content/drive/MyDrive/legend_classification/train'
valid_path = '/content/drive/MyDrive/legend_classification/val'

vgg = VGG16(input_shape=IMAGE_SIZE + [3], weights='imagenet', include_top=False)
for layer in vgg.layers:
  layer.trainable = False

folders = glob('/content/drive/MyDrive/legend_classification/train/*')
len(folders)

x = Flatten()(vgg.output)
x = Dense(1000, activation='relu')(x)
prediction = Dense(len(folders), activation='softmax')(x)
model = Model(inputs=vgg.input, outputs=prediction)
model.summary()

from keras import optimizers

model.compile(loss='categorical_crossentropy', optimizer=optimizers.Adam(learning_rate = 0.0001), metrics=['accuracy'])
train_datagen = ImageDataGenerator(rescale=1./225, width_shift_range=0.1, height_shift_range=0.1)
test_datagen = ImageDataGenerator(rescale=1./225)

training_set = train_datagen.flow_from_directory('/content/drive/MyDrive/legend_classification/train', target_size=(224, 224), batch_size=1, class_mode='categorical')
test_set = test_datagen.flow_from_directory('/content/drive/MyDrive/legend_classification/val', target_size=(224, 224), batch_size=1, class_mode='categorical')

cla = test_set.classes
print(cla)

r = model.fit(training_set, validation_batch_size=test_set, epochs=20, steps_per_epoch=len(training_set), validation_steps=len(test_set))

save_model(model, '/content/drive/MyDrive/legend_classification/vgg16.h5')

path = '/content/drive/MyDrive/legend_classification/final_test/2017/dtemp_2017.png'

from keras.preprocessing import image
from keras.utils import load_img
img = load_img(path, target_size=(224,224))
img = np.asarray(img)
plt.imshow(img)
img = np.expand_dims(img, axis=0)
output = model.predict(img)
print(output)

output

# predictions = np.array([[1, 0], [0, 1]])

# predicted_labels = np.argmax(predictions, axis=1)
# print(predicted_labels)

# images_directory = '/content/drive/MyDrive/legend_classification/test/'

# for filename in os.listdir(images_directory):
#     if filename.endswith('.png'):
#         path = os.path.join(images_directory, filename)

#         img = load_img(path, target_size=(224, 224))
#         img = np.asarray(img) / 255
#         img = np.expand_dims(img, axis=0)

#         output = model.predict(img)
#         print(output)

#         if output[0][0] > 0.5:
#             save_path = os.path.join('/content/drive/MyDrive/legend_classification/results/choropleth/', filename)
#         else:
#             save_path = os.path.join('/content/drive/MyDrive/pdf_image_classifier/results/isocline/', filename)

#         cv2.imwrite(save_path, cv2.imread(path))

import os
import cv2
import numpy as np
from tensorflow.keras.preprocessing.image import load_img
import csv

csv_file = '/content/drive/MyDrive/legend_classification/final_results/2017/classification_results.csv'
with open(csv_file, mode='w') as file:
    writer = csv.writer(file)
    writer.writerow(['file name', 'Type'])

images_directory = '/content/drive/MyDrive/legend_classification/final_test/2017'

for filename in os.listdir(images_directory):
    if filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.jpeg'):
        path = os.path.join(images_directory, filename)

        img = load_img(path, target_size=(224, 224))
        img = np.asarray(img) / 255
        img = np.expand_dims(img, axis=0)

        output = model.predict(img)
        print(output)

        if output[0][0] > 0.5:
            file_type = 'continuous'
            save_path = os.path.join('/content/drive/MyDrive/legend_classification/final_results/2017/continuous', filename)
        else:
            file_type = 'discrete'
            save_path = os.path.join('/content/drive/MyDrive/legend_classification/final_results/2017/discrete', filename)

        with open(csv_file, mode='a') as file:
            writer = csv.writer(file)
            writer.writerow([filename, file_type])

        cv2.imwrite(save_path, cv2.imread(path))

import pandas as pd

df1 = pd.read_csv("/content/drive/MyDrive/legend_classification/final_test/2019/final_annotation_output.csv")
df2 = pd.read_csv("/content/drive/MyDrive/legend_classification/final_results/2019/classification_results.csv")

result = pd.merge(df1, df2, on='file name')

result.to_csv("/content/drive/MyDrive/legend_classification/final_results/2019/final.csv", index=False)