'''
    aimodel.py 

            v0.1: AI Model class design&implementation
'''
import sys, os
# add module path
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
# import keras modules
stderr = sys.stderr
sys.stderr = open(os.devnull, 'w')
from keras import layers
from keras import models
from keras import metrics
from keras import losses
from keras import optimizers
from keras import datasets              
from keras.utils import np_utils
from keras.layers import Dropout
from keras.models import load_model
import numpy as np
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
# import utils
from utils.FileUtils import *
from model.FeatureExtractor import *
sys.stderr = stderr
# randomforest
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix 
import pickle
from keras import backend

class AIModel():
    '''
    AI Model class 
    '''    
    def __init__(self, modelPath='browser_model.h5'):
        # init variables 
        self.basePath = os.getcwd()
        self.modelPath = self.basePath + '/model/' + modelPath
        self.model = load_model(self.modelPath)
        self.sensitivity = 1

    def PredictFile(self, filename):
        npfeature = []
        extractor = FeatureExtractor()
        features = extractor.getFeature(filename)
        if features == False:
            return 0
        npfeature.append(features)
        npfeature = np.array(npfeature ,dtype=np.float32)
        return self.Predict(npfeature)

    def Predict(self, feature):
        result = 0
        result = self.model.predict(feature)
        return round(result[0][0],3)
    
    def setSensitivity(self, sensitivity):
        self.sensitivity = sensitivity

    def ClassifyFile(self, filename):
        result = { 
            'point':0, 
            'class':'Normal', 
            'predict':False,
            'desc':''
        } # porint: 0~100, class: normal / suspicious / malicious
        predictResult = False

        ###################################
        # RandomForest AI
        npfeature = []
        extractor = FeatureExtractor()
        features = extractor.getFeature(filename)
        if features == False:
            return False
        npfeature.append(features)
        npfeature = np.array(npfeature ,dtype=np.float32)
        model = pickle.load(open('model/rf.model','rb'))
        p = model.predict(npfeature)
        point = float(str(p[0])[:4])
        if point > 0.5:
            predictResult = True
        else:
            predictResult = False

        ###################################
        # DNN AI
        p2 = self.Predict(npfeature)
        result['predict'] = predictResult
        if p2-0.1 <= 0:
            result['point'] = float(str(p2-0.1)[1:4])
        else:         
            result['point'] = float(str(p2-0.1)[:4])     
        
        # status
        if predictResult:
            result['class'] = 'Malicious'
        
        # description (adjust sensitivity)
        if self.sensitivity == 0:
            if result['point'] > 0.8:  # mal
                result['desc'] = '{}% (Suspicious)'.format(str(result['point']*100)[:4])
            else:
                result['desc'] = '{}%'.format(str(result['point']*100)[:4])
        if self.sensitivity == 1:
            if result['point'] > 0.85:  # mal
                result['desc'] = '{}% (Suspicious)'.format(str(result['point']*100)[:4])
            else:
                result['desc'] = '{}%'.format(str(result['point']*100)[:4])
        if self.sensitivity == 2:
            if result['point'] > 0.9:  # mal
                result['desc'] = '{}% (Suspicious)'.format(str(result['point']*100)[:4])
            else:
                result['desc'] = '{}%'.format(str(result['point']*100)[:4])
                            
        return result

    def clearSession(self):
        backend.clear_session()
