
# Choropleth-CMA

This project processes bitmap images of choropleth maps, segments them into different states, extracts data values from the legends, and reconstructs the original metadata used to create the maps. It automates the extraction and analysis of geographic data for enhanced visualization and insights.


![precip_2021](https://github.com/GVCL/Choropleth-CMA/assets/111348225/d19dbb11-5326-46b0-a2d6-142477c4d3c4)
![precip_2021_seg](https://github.com/GVCL/Choropleth-CMA/assets/111348225/39db9ee7-20f0-4153-bee2-2c0215a4d3e5)
![precip_2021_annotate](https://github.com/GVCL/Choropleth-CMA/assets/111348225/3965eb00-af7a-4c83-be8b-4bdc78c14a60)

## Dataset

Download the custom data for training the model.  
- We have used [MapQA dataset](https://buckeyemailosu-my.sharepoint.com/personal/chang_1692_buckeyemail_osu_edu/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fchang%5F1692%5Fbuckeyemail%5Fosu%5Fedu%2FDocuments%2FMapQA&ga=1) for training the model.  
- For testing, we have curated choropleth map images from climate dataset from the United States Geological Survey [USGS](https://www.usgs.gov/) and Climate Research Unit [UK](https://www.uea.ac.uk/web/groups-and-centres/climatic-research-unit/data)

## Models Used  
- We have used ResNet50 for image classification, whether the image is discrete or continuous
- For the task of annotation and Segmentation of States we have used [Detectron2](https://github.com/facebookresearch/detectron2) model by Facebook Research
- We have proposed our approach to associate the color information from legends to states and finally generate the metadata.
## Setup

Entire project was developed on Google Colab utilizing NVIDIA T4 and NVIDIA L4 GPUs. 
## Inference

Using the code and model mentioned, you can test your custom dataset to get the results.  
- With input image as a choropleth map image, you can segment your dataset into different states, extract color from the respective state, get the legend color information and the data value associated.  
- Finally, you associate the state name with the data and generate the original metadata with which the choropleth map was created.
- Utilizing this metadata you can now generate different visualizations of your choice as well as generate insights from the metadata


## Authors

[Prince Nileshbhai Butani](https://www.linkedin.com/in/princebutani/), [Jaya Sreevalsan-Nair](https://www.linkedin.com/in/jayanair/) and Nilay Kamat
## Acknowledgment

The authors are grateful to IIIT Bangalore [IIIT-B](https://iiitb.ac.in/) to the Graphic Visualization and Computing Lab ([GVCL](https://www.iiitb.ac.in/GVCL/)) at IIIT-B, for their constant support.
