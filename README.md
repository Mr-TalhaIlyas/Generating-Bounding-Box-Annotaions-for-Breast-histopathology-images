# Converting Breast Histopathology Tumor Dignosis Data into Detection Dataset

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

For details on this data set you can read the original paper [here](https://bmcresnotes.biomedcentral.com/articles/10.1186/s13104-019-4121-7)

You can download the full dataset from [here](https://figshare.com/articles/BreCaHAD_A_Dataset_for_Breast_Cancer_Histopathological_Annotation_and_Diagnosis/7379186)

### Usage 

Displaying annotations in `breast_histology_display.py` give the file path to see the annotations plotted on the image

```python


json_filepath = 'D:/Anaconda/Datasets/Breast Biopsy/groundTruth/Case_1-02.json'
img_filepath = 'D:/Anaconda/Datasets/Breast Biopsy/images/Case_1-02.tif'

# annotatio_type : circel or bnd_box, The default is 'circle'.
plot_annotations(img_filepath, json_filepath, annotatio_type = 'circle')

```
Circels
```python
plot_annotations(img_filepath, json_filepath, annotatio_type = 'circle')
```
![alt text](https://github.com/Mr-TalhaIlyas/Generating-Bounding-Box-Annotaions-for-Breast-histopathology-images/blob/master/screens/img(3).png)
Boxes

```python
plot_annotations(img_filepath, json_filepath, annotatio_type = 'bnd_box')
```
![alt text](https://github.com/Mr-TalhaIlyas/Generating-Bounding-Box-Annotaions-for-Breast-histopathology-images/blob/master/screens/img(5).png)
## Converting the annotations to XML (bounding boxes)
in `breast_jsonpts2xmlbox.py` set the file path to convert the annotations.
### Usage

```python
json_dir = '../Breast Biopsy/groundTruth/' # path to json files
img_dir = '../Breast Biopsy/images/'       # path to image files
op_dir = '../Breast Biopsy/xml_boxes/'     # path to output xml files
```
### Sample Output

![alt text](https://github.com/Mr-TalhaIlyas/Generating-Bounding-Box-Annotaions-for-Breast-histopathology-images/blob/master/screens/img(2).png)
![alt text](https://github.com/Mr-TalhaIlyas/Generating-Bounding-Box-Annotaions-for-Breast-histopathology-images/blob/master/screens/img(1).png)

## Data Augumentation 

As shown in above images we can clearly see that the images are densely annotated and the resolution is very high. Morover a lot of cells of different type are cluttered together, which will make it difficult for the network to precisely localize and classify them. As the cells alread have very little inter-class variations, we need to find a way to process the data which will increase spatial resolution of the data. But if we directly upscaled an image of resolution 1360x1024 to an even bigger resolution the computation time of CNN will explode. So one solution could be resizing all the images.But resizing them will reduce the WSI resolution, we might lose a lot of useful information.
So to cope with this problem we can do upscale cropping or also called SSD crop data augumentation. 
### SSD Crop
Instead of resizing the images directly first we will crop a part of the image (with predefined aspect ratio) and then rescale it to the input size. This might sound simple but its actully not, because you don't only have to resize the image but also you will have to update its corresponding annotations in the `.xml` file to the new rescaled coordinates.
So from a single image we will get 9 crops form different parts (i.e. 'center','left-top', 'left-center', 'left-bottom', 'center-top','center-bottom', 'right-top', 'right-center', 'right-bottom') as shown in figure below,
![alt text](https://github.com/Mr-TalhaIlyas/Generating-Bounding-Box-Annotaions-for-Breast-histopathology-images/blob/master/screens/win_s.png)
Shaded regions show the each crop. Each crop has the same aspect ratio as the original image and is have 10~15% overlap with its adjecent neighbour.
Using this technique we can avoid reduce in WSI resolution and quality. For details on how to **augument detection dataset** check out my repo [here](https://github.com/Mr-TalhaIlyas/Augumenting_Detection_Dataset)
Using SSD crop will give us two major benefits,
* Spatially enhance the data for the CNN for better performance
* Increase the data size from 162 original images to 1458 SSD crop images.
Note: This data is not the rotated or flipped version of the image (as in typical data augmentation), but actually each image in data is unique becaues we cropped the original image from different parts and then rescaled it to make the new set.

## Results

Following images are SSD crops of original ones along with their scaled annotations. Form the follwing images we can clearly see that we have simplified the data quite a bit.

![alt text](https://github.com/Mr-TalhaIlyas/Generating-Bounding-Box-Annotaions-for-Breast-histopathology-images/blob/master/screens/img_(2).png)
![alt text](https://github.com/Mr-TalhaIlyas/Generating-Bounding-Box-Annotaions-for-Breast-histopathology-images/blob/master/screens/img_(3).png)
![alt text](https://github.com/Mr-TalhaIlyas/Generating-Bounding-Box-Annotaions-for-Breast-histopathology-images/blob/master/screens/img_(4).png)
![alt text](https://github.com/Mr-TalhaIlyas/Generating-Bounding-Box-Annotaions-for-Breast-histopathology-images/blob/master/screens/img_(5).png)
![alt text](https://github.com/Mr-TalhaIlyas/Generating-Bounding-Box-Annotaions-for-Breast-histopathology-images/blob/master/screens/img_(6).png)

### PS
________
As for getting the prediction on the original data,
* we can just crop it into 9 parts as shown above 
* pass each crop through the trained detection network
* after getting all the predictions for each crop we can simply tile them back together in their respective place in the original image.
