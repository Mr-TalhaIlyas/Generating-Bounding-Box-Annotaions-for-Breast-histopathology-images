# Converting Brease Histopathology Dignosis Data into Detection Dataset

The annotatoins provided with the BreCaHAD are json files for each image the corresponding file contains the normalized center points of the different cell types.
This repo converts those center points into the un-normalized bounding boxes with width and hight of 30x30 pixels (I choose this area because with this size the box completely contains a single cell).
Ususally this type of prblem is solved via FCNs to do multi-class semantic segmentation or just by croping a patch of the WSI (whole slide image) and the classify each patch seperately.
So I'd try to solve this problem via detection pipeline (SSD, Faseter_RCNN etc) for that first I need to convert this dataset as the dataset is a main component in training a CNN. So, I'll generate bounding boxes annotation of this dataset from given .json files, this repo will do just that.
The task associated with this dataset is to automatically classify histological structures in these hematoxylin and eosin (H&E) stained images into six classes:
* mitosis
* apoptosis
* tumor 
* non-tumor 
* tubule
* non-tubule.

### BreCaHAD: a dataset for breast cancer histopathological annotation and diagnosis

For details on this data set you can read the followin paper here(https://bmcresnotes.biomedcentral.com/articles/10.1186/s13104-019-4121-7)
You can download the full dataset from here (https://figshare.com/articles/BreCaHAD_A_Dataset_for_Breast_Cancer_Histopathological_Annotation_and_Diagnosis/7379186)

### Usage 

Displaying annotations

```python
# in breast_histology_display.py give the file path to see the annotations plotted on the image

json_filepath = 'D:/Anaconda/Datasets/Breast Biopsy/groundTruth/Case_1-02.json'
img_filepath = 'D:/Anaconda/Datasets/Breast Biopsy/images/Case_1-02.tif'

# annotatio_type : circel or bnd_box, The default is 'circle'.
plot_annotations(img_filepath, json_filepath, annotatio_type = 'circle')

```
Circels
```
plot_annotations(img_filepath, json_filepath, annotatio_type = 'circle')
```

Boxes

```
plot_annotations(img_filepath, json_filepath, annotatio_type = 'bnd_box')
```
## Converting the annotations to XML (bounding boxes)

```python
json_dir = '../Breast Biopsy/groundTruth/' # path to json files
img_dir = '../Breast Biopsy/images/'       # path to image files
op_dir = '../Breast Biopsy/xml_boxes/'     # path to output xml files
```
