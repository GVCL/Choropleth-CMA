# -*- coding: utf-8 -*-
"""Segmentation of States.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Ykc2p3MkLvBlurNbnbkQhI6Y72U-y3DY
"""

from google.colab import drive
drive.mount('/content/drive')

!python -m pip install pyyaml
import sys, os, distutils.core
!git clone 'https://github.com/facebookresearch/detectron2'
dist = distutils.core.run_setup("./detectron2/setup.py")
!python -m pip install {' '.join([f"'{x}'" for x in dist.install_requires])}
sys.path.insert(0, os.path.abspath('./detectron2'))

import torch, detectron2
!nvcc --version
TORCH_VERSION = ".".join(torch.__version__.split(".")[:2])
CUDA_VERSION = torch.__version__.split("+")[-1]
print("torch: ", TORCH_VERSION, "; cuda: ", CUDA_VERSION)
print("detectron2:", detectron2.__version__)

import detectron2
from detectron2.utils.logger import setup_logger
setup_logger()

import numpy as np
import os, json, cv2, random
from google.colab.patches import cv2_imshow

from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog, DatasetCatalog

im = cv2.imread("/content/drive/MyDrive/map_detect/R.jpeg")
cv2_imshow(im)

cfg = get_cfg()
cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
predictor = DefaultPredictor(cfg)
outputs = predictor(im)

print(outputs["instances"].pred_classes)
print(outputs["instances"].pred_boxes)

v = Visualizer(im[:, :, ::-1], MetadataCatalog.get(cfg.DATASETS.TRAIN[0]), scale=0.8)
out = v.draw_instance_predictions(outputs["instances"].to("cpu"))
cv2_imshow(out.get_image()[:, :, ::-1])

from detectron2.data.datasets import register_coco_instances
register_coco_instances("my_dataset_train", {}, "/content/drive/MyDrive/map_detect/final/train/final_train_02.json", "/content/drive/MyDrive/map_detect/final/train")
register_coco_instances("my_dataset_val", {}, "/content/drive/MyDrive/map_detect/final/val/final_val_01.json", "/content/drive/MyDrive/map_detect/final/val")

train_metadata = MetadataCatalog.get("my_dataset_train")
train_dataset_dicts = DatasetCatalog.get("my_dataset_train")

val_metadata = MetadataCatalog.get("my_dataset_val")
val_dataset_dicts = DatasetCatalog.get("my_dataset_val")

from matplotlib import pyplot as plt

for d in random.sample(train_dataset_dicts, 2):
    img = cv2.imread(d["file_name"])
    visualizer = Visualizer(img[:, :, ::-1], metadata=train_metadata, scale=0.5)
    vis = visualizer.draw_dataset_dict(d)
    plt.imshow(vis.get_image()[:, :, ::-1])
    plt.show()

from detectron2.engine import DefaultTrainer

cfg = get_cfg()
cfg.OUTPUT_DIR = "/content/drive/MyDrive/models/Detectron2_Models"
cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
cfg.DATASETS.TRAIN = ("my_dataset_train",)
cfg.DATASETS.TEST = ("my_dataset_val",)
cfg.DATALOADER.NUM_WORKERS = 2
cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
cfg.SOLVER.IMS_PER_BATCH = 2
cfg.SOLVER.BASE_LR = 0.0001
cfg.SOLVER.MAX_ITER = 7500
cfg.SOLVER.STEPS = []
cfg.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = 256
cfg.MODEL.ROI_HEADS.NUM_CLASSES = 50

os.makedirs(cfg.OUTPUT_DIR, exist_ok=True)
trainer = DefaultTrainer(cfg)
trainer.resume_or_load(resume=False)

trainer.train()

import yaml
config_yaml_path = "/content/drive/MyDrive/models/Detectron2_Models/final/config.yaml"
with open(config_yaml_path, 'w') as file:
    yaml.dump(cfg, file)

cfg.MODEL.WEIGHTS = os.path.join(cfg.OUTPUT_DIR, "model_final.pth")
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
predictor = DefaultPredictor(cfg)

from detectron2.utils.visualizer import ColorMode

for d in random.sample(val_dataset_dicts, 1):
    im = cv2.imread(d["file_name"])
    outputs = predictor(im)
    v = Visualizer(im[:, :, ::-1],
                   metadata=val_metadata,
                   scale=0.5,
                   instance_mode=ColorMode.IMAGE_BW
    )
    out = v.draw_instance_predictions(outputs["instances"].to("cpu"))
    cv2_imshow(out.get_image()[:, :, ::-1])

from detectron2.evaluation import COCOEvaluator, inference_on_dataset
from detectron2.data import build_detection_test_loader
evaluator = COCOEvaluator("my_dataset_val", output_dir="./output")
val_loader = build_detection_test_loader(cfg, "my_dataset_val")
print(inference_on_dataset(predictor.model, val_loader, evaluator))

new_im = cv2.imread("/content/drive/MyDrive/map_detect/final/test/test_set/dtemp_2017.png")
outputs = predictor(new_im)

v = Visualizer(new_im[:, :, ::-1], metadata=train_metadata)
out = v.draw_instance_predictions(outputs["instances"].to("cpu"))

cv2_imshow(out.get_image()[:, :, ::-1])

# import os
# import cv2
# import csv
# from skimage.measure import regionprops, label
# from detectron2.engine import DefaultPredictor
# from detectron2.utils.visualizer import Visualizer

# input_images_directory = "/content/drive/MyDrive/map_detect/final/test/test_set_1/"
# output_directory = "/content/drive/MyDrive/map_detect/final/result/set_1/"
# # output_csv_path = "/content/drive/MyDrive/map_detect/test_result_03/output_objects.csv"

# # Assuming `predictor` and `train_metadata` are defined elsewhere
# # predictor = ...
# # train_metadata = ...

# with open(output_csv_path, 'w', newline='') as csvfile:
#     csvwriter = csv.writer(csvfile)
#     csvwriter.writerow(["File Name", "Class Name", "Object Number", "Centroid", "BoundingBox", "RGB Color"])

#     for image_filename in os.listdir(input_images_directory):
#         image_path = os.path.join(input_images_directory, image_filename)
#         new_im = cv2.imread(image_path)

#         outputs = predictor(new_im)

#         mask = outputs["instances"].pred_masks.to("cpu").numpy().astype(bool)
#         class_labels = outputs["instances"].pred_classes.to("cpu").numpy()
#         labeled_mask = label(mask)
#         props = regionprops(labeled_mask)

#         v = Visualizer(new_im[:, :, ::-1], metadata=train_metadata)

#         for i, prop in enumerate(props):
#             object_number = i + 1
#             centroid = prop.centroid
#             bounding_box = prop.bbox

#             if i < len(class_labels):
#                 class_label = class_labels[i]
#                 class_name = train_metadata.thing_classes[class_label]
#             else:
#                 class_name = 'Unknown'

#             # Extract RGB color value from the centroid position
#             centroid_x, centroid_y = int(centroid[1]), int(centroid[0])
#             rgb_color = new_im[centroid_y, centroid_x]

#             csvwriter.writerow([image_filename, class_name, object_number, centroid, bounding_box, rgb_color])

#             # Draw bounding box and save the result image
#             out = v.draw_instance_predictions(outputs["instances"].to("cpu"))
#             result_filename = os.path.splitext(image_filename)[0] + "_result.png"
#             output_path = os.path.join(output_directory, result_filename)
#             cv2.imwrite(output_path, out.get_image()[:, :, ::-1])

# print("Object-level information saved to CSV file.")
# print("Segmentation of all images completed.")

input_images_directory = "/content/drive/MyDrive/map_detect/final/test/test_set/2017/"

output_directory = "/content/drive/MyDrive/map_detect/final/result/set/2017/"

for image_filename in os.listdir(input_images_directory):
    image_path = os.path.join(input_images_directory, image_filename)
    new_im = cv2.imread(image_path)

    outputs = predictor(new_im)

    v = Visualizer(new_im[:, :, ::-1], metadata=train_metadata)
    out = v.draw_instance_predictions(outputs["instances"].to("cpu"))

    result_filename = os.path.splitext(image_filename)[0] + "_result.png"
    output_path = os.path.join(output_directory, result_filename)

    cv2.imwrite(output_path, out.get_image()[:, :, ::-1])

print("Segmentation of all images completed")

import csv
from skimage.measure import regionprops, label


# Assuming you have already defined the 'predictor' object and loaded the model.
# Also, make sure 'metadata' is defined appropriately.

# Directory path to the input images folder
input_images_directory = "/content/drive/MyDrive/map_detect/final/test/test_set/temp"

# Output directory where the CSV file will be saved
output_csv_path = "/content/drive/MyDrive/map_detect/final/result/set/temp/output_objects.csv"  # Replace this with the path to your desired output CSV file

# Open the CSV file for writing
with open(output_csv_path, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)

    # Write the header row in the CSV file
    csvwriter.writerow(["File Name", "Class Name", "Centroid", "BoundingBox"])  # Add more columns as needed for other properties

    # Loop over the images in the input folder
    for image_filename in os.listdir(input_images_directory):
        image_path = os.path.join(input_images_directory, image_filename)
        new_im = cv2.imread(image_path)

        # Perform prediction on the new image
        outputs = predictor(new_im)  # Format is documented at https://detectron2.readthedocs.io/tutorials/models.html#model-output-format

        # Convert the predicted mask to a binary mask
        mask = outputs["instances"].pred_masks.to("cpu").numpy().astype(bool)

        # Get the predicted class labels
        class_labels = outputs["instances"].pred_classes.to("cpu").numpy()

        # Debugging: print class_labels and metadata.thing_classes
        #print("Class Labels:", class_labels)
        #print("Thing Classes:", train_metadata.thing_classes)

        # Use skimage.measure.regionprops to calculate object parameters
        labeled_mask = label(mask)
        props = regionprops(labeled_mask)

        # Write the object-level information to the CSV file
        for i, prop in enumerate(props):
            centroid = prop.centroid
            bounding_box = prop.bbox[1:3] + prop.bbox[4:]
            n = int(centroid[0])
            # Check if the corresponding class label exists
            if i < len(class_labels):
                class_label = class_labels[n]
                class_name = train_metadata.thing_classes[class_label]
            else:
                # If class label is not available (should not happen), use 'Unknown' as class name
                class_name = 'Unknown'

            # Write the object-level information to the CSV file
            csvwriter.writerow([image_filename, class_name, centroid, bounding_box])  # Add more columns as needed for other properties

print("Object-level information saved to CSV file.")

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

csv_file_path = "/content/drive/MyDrive/map_detect/final/result/set/2017/output_objects.csv"

df = pd.read_csv(csv_file_path)

class_names = train_metadata.thing_classes

avg_objects_per_class = df.groupby(["File Name", "Class Name"])["Object Number"].count().reset_index()
avg_objects_per_class = avg_objects_per_class.groupby("Class Name")["Object Number"].mean().reset_index()

plt.figure(figsize=(10, 6))
sns.barplot(x="Class Name", y="Object Number", data=avg_objects_per_class, ci=None, order=class_names)
plt.xticks(rotation=45)
plt.xlabel("Class Name")
plt.ylabel("Average Number of Objects per Image")
plt.title("Average Number of Objects per Image for Each Class")
plt.tight_layout()
plt.show()

