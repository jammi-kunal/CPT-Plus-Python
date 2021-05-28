import PredictionTree
from PredictionTree import *

class CPTHelper():
  CPTPlusPredictor= None
  Encoder= None
  def __init__(self,Predictor= None):
    self.CPTPlusPredictor= Predictor
  
  def setEncoded(self,Encoder= None):
    self.Encoder= Encoder

  def getSequenceFromId(self,id):
    if self.Encoder is None:
      print("SET ENCODER !")
      #TELL THAT THE ENCODER NEEDS TO BE SET IN THE CPTPlusPredictor
    items= []
    curNode= PredictionTree()
    curNode= self.CPTPlusPredictor.LT.get(id)
    #print("HELLO   !!!!",curNode.item)
    items.append(curNode.item)
    while curNode.parent is not None and curNode.parent is not self.CPTPlusPredictor.Root:
      curNode= curNode.parent
      #print("IN HERE= ",curNode.item)
      if curNode.item is not None:
        items.append(curNode.item)
    #print("ITEMS NPON REV= ",items)
    items.reverse()
    sequence= self.Encoder.decode(items)
    return sequence

  def getCommonPrefix(self,A,B):
    if len(A)< 1 or len(B)< 1:
      return None
    commonSeq= []
    i=0
    while i< len(A) and i< len(B):
      if A[i] == B[i]:
        commonSeq.append(A[i])
      else:
        return commonSeq
      i= i+1
    return commonSeq
  
  def keepLastItems(self,Seq,leng):
    return Seq[len(Seq)-leng:len(Seq)]

  def getSimilarSequenceIds(self,sequence):
    if len(sequence)==0:
      return set()
    intersection= None
    i=0
    while i< len(sequence):
      if intersection== None:
        intersection= self.CPTPlusPredictor.II.get(sequence[i])
      else:
        other= self.CPTPlusPredictor.II.get(sequence[i])
        if other is not None:
          intersection.intersection(self.CPTPlusPredictor.II.get(sequence[i]))
      i= i+1
    return intersection

  '''
  def removeUnseenItems(self,Seq):
    target= Seq
    treshhold= 0
    selectedItems= []
    for item in target:
      if CPTPlusPredictor.II.get(item) is not None and CPTPlusPredictor.II.get(item).cardinality()>= threshhold: #this part is an issue. the II is a dictionary of integer and bitset. i dont know why a bitset is used here.
        selectedItems.append(item)
    return selectedItems
'''