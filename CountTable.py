#from pytreemap import TreeMap
import sys
import CPTHelper
from CPTHelper import *
import global_vars

class CountTable():
  table= {}
  branchVisited= []
  helper= CPTHelper()
  temp_sd_dict= {}

  def __init__(self,helper):
    self.table= {}
    self.branchVisited= []
    self.helper= helper
    self.temp_sd_dict= {}

  def push(self,key,curSeqLength,fullSeqLength,nOfSeqSameLength,dist):
    #print("key= ",key)
    #print("cursewlem= ",curSeqLength)
    #print("fullseqlen= ",fullSeqLength)
    #print("noOf= ",nOfSeqSameLength)
    #print("dist= ",dist)
    #print("\n")
    weightLevel= 1/nOfSeqSameLength
    weightDistance= 1/dist
    curValue= (weightLevel)+1+(weightDistance*0.0001)
    oldVal= self.table.get(key)
    if oldVal== None:
      self.table[key]= curValue
    else:
      self.table[key]= oldVal*curValue

  def update(self,Seq,initialSeqSize):
    #print("Seq= ",Seq)
    branchesUsed= 0
    ids= self.helper.getSimilarSequenceIds(Seq)
    #print(ids)
    if ids is None:
      #sys.exit("\nPrediction cannot be made for this sequence according to the Compact Prediction Tree! Please check the Target Sequence.")
      global_vars.xception= True
      return
    for id in ids:
      #print("ID= ",id)
      if id in self.branchVisited:
        continue
      self.branchVisited.append(id)
      seq= self.helper.getSequenceFromId(id)
      #print("seq= ",seq)
      toAvoid= []
      for item in Seq:
        toAvoid.append(item)
      #print("TOAVOID= ",toAvoid)
      max= 99
      count=1
      for item in seq:
        if len(toAvoid)== 0 and count < max:
          self.push(item,len(Seq),initialSeqSize,len(ids),count)
          count= count+1
        elif item in toAvoid:
          toAvoid.remove(item)
      if count>1:
        branchesUsed= branchesUsed+1
    #print(branchesUsed)
    #print(self.temp_sd_dict,"\n")
    return branchesUsed
  
  def getBestSequence(self,count):
    sd= {}
    #print("TABLE= ",self.table)
    for key,value in self.table.items():
      #print("KEYS= ",key,"VALUE= ",value)
      self.put_sd(key,value)
    #print("temp_keys= ",self.temp_sd_dict)
    seq= []
    bestItems= self.getBest(self.temp_sd_dict,1.002)
    if bestItems is not None and len(bestItems) > 0:
      i=0
      while i <count and i< len(bestItems):
        seq.append(bestItems[i])
        i=i+1
    return seq

  def getBest(self,sd,minThreshold):
    if len(sd)== 0:
      return None
    elif len(sd)==1:
      return list(sd.values())[len(sd)-1]
    key_list= list(sd.keys())
    #print("UNSORTED= ",key_list)
    key_list.sort()
    #print("SORTED= ",key_list)
    temp_len= len(key_list)
    bestval1= key_list[temp_len-1]
    bestval2= key_list[temp_len-2]
    #print(bestval1,bestval2)
    #print(bestval1/bestval2)
    if (bestval1/bestval2) < minThreshold:
      return None
    else:
      val_list= list(sd.values())
      index= list(sd.keys()).index(bestval1)
      return (val_list[index])
    
  def put_sd(self,key,score):
    val_list= list(self.temp_sd_dict.values())
    key_list= list(self.temp_sd_dict.keys())
    t_list= []
    if score in key_list:
      index= key_list.index(score)
      t_list= val_list[index]
      t_list.append(key)
      self.temp_sd_dict[score]= t_list
    else:
      t_list.append(key)
      self.temp_sd_dict[score]= t_list
      #print(self.temp_sd_dict,"\n")
