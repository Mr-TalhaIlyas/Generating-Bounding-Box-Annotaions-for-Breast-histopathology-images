import json
from dicttoxml import dicttoxml
from xml.dom.minidom import parseString
import xml.etree.ElementTree as gfg
import glob, os
from tqdm import tqdm, trange
import xml.etree.ElementTree as ET
import seaborn as sns
from xml.dom import minidom
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 300
# give file path
json_dir = 'D:/Anaconda/Datasets/Breast Biopsy/groundTruth/'
img_dir = 'D:/Anaconda/Datasets/Breast Biopsy/images/'
op_dir = 'D:/Anaconda/Datasets/Breast Biopsy/xml_boxes/'
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

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = gfg.tostring(elem, 'utf-8')  # form byte to string 
    reparsed = minidom.parseString(rough_string)
    
    return reparsed.toprettyxml(indent="    ", encoding = 'utf-8') # form string to byte

json_filepaths = glob.glob( os.path.join( json_dir , '*.json' ) )
img_filepaths = glob.glob( os.path.join( img_dir , '*.tif' ) )
colors = sns.color_palette("bright")
#%
for i in trange(len(json_filepaths)):
    # xml file will have same name as the original json file
    name = os.path.basename(json_filepaths[i])[:-5] # -5 b/c .josn is 5 characters
    # read the json file from given path
    with open(json_filepaths[i]) as json_file: 
        # start a xml file root
        root = gfg.Element("annotation") 
        #element
        e1 = gfg.Element("filename") 
        e1.text = str(name+'.tif')
        root.append (e1) 
        # here json_file will be a text wrapped
        # and json will be python dict type containing data
        j_son = json.load(json_file) 
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
                coords.append((int(center[k]['x']*w), int(center[k]['y']*h), 30, 30)) 
            coords =  np.array(coords).astype(np.int16)
            all_boxes = []
            for points in coords:
                facebox  = xywh_2_xyminmax(points).astype(np.int16)
                all_boxes.append(facebox)
            all_boxes = np.asarray(all_boxes)
            
            for l in range(len(all_boxes)):
                e2 = gfg.Element('object')
                root.append(e2)
                #sub-element
                se1 = gfg.SubElement(e2, 'name')
                se1.text = str(j)
                se3 = gfg.SubElement(e2, 'bndbox')
                #sub-sub-element
                sse1 = gfg.SubElement(se3, 'xmin')
                sse1.text = str((all_boxes[l][0]).astype(np.int16))
                sse2 = gfg.SubElement(se3, 'ymin')
                sse2.text = str((all_boxes[l][1]).astype(np.int16))
                sse3 = gfg.SubElement(se3, 'xmax')
                sse3.text = str((all_boxes[l][2]).astype(np.int16))
                sse4 = gfg.SubElement(se3, 'ymax')
                sse4.text = str((all_boxes[l][3]).astype(np.int16))
                
        xml_path = op_dir + name +'.xml'
        root = prettify(root)
        
        with open (xml_path, "wb") as files : 
           files.write(root)
        
        
        
        
        
        
        
        
        
        
        