# -*- coding: utf-8 -*-
"""MainTestCPTPlus.py

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZXT2XkOd3bUChIHCHWD6wzBV6aIBnMel
"""

import sys
import pandas as pd
from google.colab import drive
sys.path.insert(0,'/content/drive/My Drive/Colab Notebooks')
import SequenceDatabase
from SequenceDatabase import *
import CPTPlusPredictor
from CPTPlusPredictor import *
#import TargetData
import datetime
import global_vars

class MainTestCPTPlus():
  inputPath= "/content/drive/My Drive/Colab Notebooks/original_data/test_cpt_data12.csv"
  targetPath= "/content/drive/My Drive/Colab Notebooks/original_data/targetData.csv"
  trainingSet= SequenceDatabase()
  data,target= trainingSet.loadFileCustomFormat(inputPath,targetPath, sys.maxsize, 0, sys.maxsize)
  print("------------------------- Training Sequences --------------------------")
  for temp in trainingSet.getSequences():
    print(temp)
  trainingSet.getStats("Training Sequences")

  optionalParameters= {
    "CCF": True,
    "CBS": True,
    "CCFmin": 2,
    "CCFmax": 4,
    "CCFsup": 2,
    "splitMethod": 0,
    "splitLength": 4,
    "minPredictionRatio": 1.0,
    "noiseRatio": 1.0,
  }

  predictionModel= CPTPlusPredictor(optionalParameters)
  predictionModel.Train(trainingSet.getSequences())
  f= open("/content/drive/My Drive/Colab Notebooks/Predictions.txt","a")
  for seq in trainingSet.getModel():
    if seq is not None:
      if None not in seq:  
        prediction= predictionModel.Predict(seq)
        if global_vars.xception== True:
          print("\nPrediction cannot be made for this sequence according to the Compact Prediction Tree! Please check the Target Sequence.")
          global_vars.xception= False
          continue
        pred_str= "\nFor the sequence "+str(seq)+" the prediction for the next symbol is: "+str(prediction)
        print(pred_str)
        f.write("------------------------------"+str(datetime.datetime.now())+"------------------------------"+pred_str+"\n------------------------------"+str(datetime.datetime.now())+"------------------------------"+"\n\n")
