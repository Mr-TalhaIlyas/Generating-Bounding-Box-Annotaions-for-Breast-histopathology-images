import json
from dicttoxml import dicttoxml
from xml.dom.minidom import parseString
import glob, os
from tqdm import tqdm, trange
import xml.etree.ElementTree as ET
import seaborn as sns
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 300

def xywh_2_xyminmax(box):
    '''
    input_box : (x, y, w, h)
    output_box : (xmin, ymin, xmax, ymax) @ un_normalized
    '''
    xmin = box[0] - (box[2] / 2)
    ymin = box[1] - (box[3] / 2)
    xmax = box[0] + (box[2] / 2)
    ymax = box[1] + (box[3] / 2)
    
    box_minmax = np.array([xmin, ymin, xmax, ymax])
    
    return box_minmax

def plot_annotations(img_filepath, json_filepath, annotatio_type = 'circle'):
    '''
    Parameters
    ----------
    img_filepath : path to image file
    json_filepath : path to json file
    annotatio_type : circel or bnd_box, The default is 'circle'.
    Returns
    -------
    image with annotaions plotted
    '''
    colors = sns.color_palette("bright")
    
    # read the json file from given path
    with open(json_filepath) as json_file: 
        # here json_file will be a text wrapped
        # and json will be python dict type containing data
        j_son = json.load(json_file) 
    if annotatio_type == 'circle':
    #####################################################
    #    If want to plot circles at center of cells
    #####################################################
        img = cv2.imread(img_filepath) / 255      
        h, w, _ = img.shape
        # get all the classes in the GT file and make a list of them
        keys = list(j_son.keys())
        # get the values of those classes 
        for idx, j in enumerate(keys):
            
            center = j_son[j]
            coords = []
            for k in range(len(center)):
                # unnormalize the center points so that they can be plotted
                coords.append((int(center[k]['x']*w), int(center[k]['y']*h))) 
            coords =  np.array(coords).astype(np.int16)
            
            for points in coords:
                cv2.circle(img, tuple(points), 10, colors[idx], cv2.FILLED)
                
        plt.imshow(img)
    if annotatio_type == 'bnd_box':
    ##############################################################
    #    If want to plot boxes centered at center of cells
    ##############################################################
        img = cv2.imread(img_filepaths[i]) / 255
        h, w, _ = img.shape
        # get all the classes in the GT file and make a list of them
        keys = list(j_son.keys())
        # get the values of those classes 
        for idx, j in enumerate(keys):
            
            center = j_son[j]
            coords = []
            for k in range(len(center)):
                # unnormalize the center points so that they can be plotted
                coords.append((int(center[k]['x']*w), int(center[k]['y']*h), 25, 25)) 
            coords =  np.array(coords).astype(np.int16)
            
            for points in coords:
                facebox  = xywh_2_xyminmax(points).astype(np.int16)
                cv2.rectangle(img, (facebox[0], facebox[1]),(facebox[2], facebox[3]), colors[idx], 2)
                
        plt.imshow(img)
    return img
#%%
json_filepath = 'D:/Anaconda/Datasets/Breast Biopsy/groundTruth/Case_1-02.json'
img_filepath = 'D:/Anaconda/Datasets/Breast Biopsy/images/Case_1-02.tif'


plot_annotations(img_filepath, json_filepath, annotatio_type = 'circle')

















