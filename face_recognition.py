import cv2
import numpy as np
import matplotlib.pyplot as plt
import os,glob
import mtcnn
from mtcnn.mtcnn import MTCNN
from keras.models import load_model
from keras_facenet import FaceNet
from scipy.spatial import distance

detector = MTCNN()
def extract_face(img, required_size=(160, 160)):
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results = detector.detect_faces(img)
    if(results):
        x1, y1, w, h = results[0]['box']
        x1, y1 = abs(x1), abs(y1)
        x2, y2 = x1 + w, y1 + h
        # extract the face
        face = img[y1:y2, x1:x2]
        # resize pixels to the model size
        image = cv2.resize(face,required_size,cv2.INTER_AREA)
        return image
x=[]
for i in glob.glob(r'D:\IEEE paper\deep learning completed project\srinidhiface\images\*\*.jpeg'):
    img = cv2.imread(i)
    img=extract_face(img)
    x.append(img)
x=np.stack(x)    
embedder = FaceNet()
embeddings = embedder.embeddings(x)   
a=[]
for root,dirp,file in os.walk(r'D:\IEEE paper\deep learning completed project\srinidhiface\images'):
    a.append(dirp)
dictq={}
for i in range(len(a[0])):
    dictq[a[0][i]]=embeddings[i]
for key,value in dictq.items():
    value.shape=[512,1]
