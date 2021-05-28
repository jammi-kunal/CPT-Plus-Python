
# -*- coding: utf-8 -*-
"""CPTPlusPredictor.py

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1QNjUP6NMVdb8JdpJkI5okMnHQx04aVrJ
"""

import sys
import pandas as pd
from google.colab import drive
sys.path.insert(0,'/content/drive/My Drive/Colab Notebooks')
import PredictionTree
from PredictionTree import *
import CPTHelper
from CPTHelper import *
import Encoder
from Encoder import *
import Paramable
from Paramable import *
import FIFRaw
from FIFRaw import *
import CountTable
from CountTable import *
import math
import global_vars
import matplotlib.pyplot as plt


class CPTPlusPredictor():
  unique_eles= set()
  LT= {}  #this dictionary consists of Integer and PredictionTree
  II= {}  #this dictionary consists of Integer and BitVector
  Root= PredictionTree()
  parameters= Paramable()
  helper= None 
  encoder= Encoder()
  CCF= False
  CBS= True
  
  def __init__(self,optParameters):
    self.unique_eles= set()
    self.Root= PredictionTree()
    self.LT= {}
    self.II= {}
    self.parameters= Paramable()
    self.helper= CPTHelper(self) 
    self.encoder= Encoder()
    if optParameters is not None:
      self.parameters.setParameters(optParameters)  

  def Train(self,trainingSequences):
    self.helper.setEncoded(self.encoder)
    nodeNumber= 0
    seqId= 0
    curNone= None
    finder= FIFRaw()
    if self.parameters.paramBoolOrDefault("CCF",self.CCF):
      itemsets= finder.findFrequentItemsets(trainingSequences,self.parameters.paramInt("CCFmin"),self.parameters.paramInt("CCFmax"),self.parameters.paramInt("CCFsup"))      
      
      for itemset in itemsets:
        
        self.encoder.addEntry(itemset)
    for seqid,seq in enumerate(trainingSequences):
      
      if self.parameters.paramInt("splitMethod") > 0:
        seq= self.helper.keepLastItems(seq,self.parameters.paramInt("splitLength"))
      #print("Original Sequence= ",seq)
      seqCompressed= self.encoder.encode(seq)
      #print("Compressed Sequence= ",seqCompressed)
      #seqDecompressed= self.encoder.decode(seqCompressed)
      #print("DeCompressed Sequence= ",seqDecompressed)#this is to check if the encoder and decoder functions are working perfectly or not. THEY ARE!!!
      curNode= self.Root
      for itemCompressed in seqCompressed:
        itemset= self.encoder.getEntry(itemCompressed)
        for item in itemset:
         if self.II.get(item) is None: 
           self.II[item]= set()
         self.II[item].add(seqid)
         self.unique_eles.add(item)
         
        if curNode.hasChild(itemCompressed)== False:
         #print("No Child of CurNode. So inserting child= ",itemCompressed)
         curNode.addChild(itemCompressed)
         curNode= curNode.getChild(itemCompressed)
        else:
          #print("Child Found. Not inserting into curNode!")
          curNode= curNode.getChild(itemCompressed)
      
      self.LT[seqid]= curNode
      seqid= seqid+1
    if self.parameters.paramBoolOrDefault("CBS",self.CBS):
      print("\n")
      #self.pathCollapse()
    print("---------------PRINTING TREE---------------")
    
    self.Root.printTree()
    print("\n\n")
    '''    
    Uncomment this to check and verify if all the three data structures are getting created perfectly. THEY ARE!

    for seq in trainingSequences:
      seqCompressed= self.encoder.encode(seq)
      print("Hello: ",seqCompressed)
    self.Root.printTree()
  
    print("Inverted Index= ",self.II)
    for key,item in self.LT.items():
      print("Lookup Table= ",key,item.item)
    print("Unique elements= ",self.unique_eles)
  '''    
    return True

  def Predict(self,target):
    ct= CountTable(self.helper)
    ct= self.predictionByActiveNoiseReduction(target)
    if global_vars.xception== True:
      return
    predicted= ct.getBestSequence(1)
    print(ct.temp_sd_dict)
    print("\nThe Pie chart of scores with their chance of occuring next")
    keys= list(ct.temp_sd_dict.keys())
    vals= []
    for i in list(ct.temp_sd_dict.values()):
      vals.append(i[0])
    plt.pie(keys,labels= vals) 
    plt.show()
    print("\n")
    return predicted

  def getNoise(self,target,noiseRatio):
    noiseCount= math.floor(len(target)*noiseRatio)
    if noiseCount <= 0:
      minSup= sys.maxsize
      itemVal= -1
      for item in target:
        if len(self.II.get(item)) < minSup:
          minSup= len(self.II.get(item))
          itemVal= item
      noises= []
      noises.append(itemVal)
      return noises
    else:
      noises= target
      return noises[len(target)-noiseCount:len(target)]
  
  def predictionByActiveNoiseReduction(self,target):
    seen= [] #a list of sequence. list of list
    queue= [] #list of list
    queue.append(target)
    maxPredictionCount= 1+ (len(target) * self.parameters.paramDouble("minPredictionRatio"))
    predictionCount=0
    noiseRatio= self.parameters.paramDouble("noiseRatio")
    initialTargetSize= len(target)
    ct= CountTable(self.helper)
    ct.update(target,len(target))
    predicted= ct.getBestSequence(1)
    if len(predicted) > 0:
      predictionCount= predictionCount+1
    seq= []
    temp_seq= queue.pop(0)
    while temp_seq is not None and predictionCount < maxPredictionCount:
      if temp_seq not in seen:
        seen.append(temp_seq)
        noises= []
        noises= self.getNoise(temp_seq,noiseRatio)                   #list of integers
        for noise in noises:
          candidate= copy.deepcopy(temp_seq)
          i=0
          while i<len(candidate):
            if candidate[i]== noise:
              candidate.remove(candidate[i])
              break
            i= i+1
          if len(candidate)> 1:
            queue.append(candidate)
          candidateItems= candidate
          branches= ct.update(candidateItems,initialTargetSize)
          if global_vars.xception== True:
            return
          if branches>0:
            predicted= ct.getBestSequence(1)
            if len(predicted)> 0:
              predictionCount= predictionCount+1
        
      try:
        temp_seq= queue.pop(0)
      except IndexError:
        break
    return ct      

  '''def pathCollapse(self):
    nodeSaved= 0
    for item, node in self.LT.items():
      cur= copy.deepcopy(node)
      leaf= copy.deepcopy(cur)
      last= None
      itemset= []
      pathL= 0
      singlePath= True

      if len(cur.getChildren())== 0:
        while singlePath== True:
          if cur== None or len(cur.getChildren()) >1:
            if pathL is not 1:
              newId= self.encoder.getIdorAdd(itemset)
              leaf.item= newId
              leaf.parent= cur
              cur.removeChild(last.item)
              cur.addChild(leaf)
              nodeSaved+= pathL-1
            singlePath= False
          else:
            curItemset= self.encoder.getEntry(cur.item)
            tmp= itemset
            itemset= []
            itemset.append(curItemset)
            itemset.append(tmp)
            cur.getChildren().clear()
            pathL+=1
            last= cur
            cur= cur.parent
    nodeNumber-= nodeSaved
'''