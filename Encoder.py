import numpy as np

class Encoder():
  Dict= []
  InvDict= {}

  def __init__(self):
    Dict = [] 
    InvDict = {} # dictionary of list and an integer

  def getId(self,entry):
    entry= list(entry)
    #print("ENtry each time= ",entry)
    id=0
    keys= list(self.InvDict.keys())
    values= list(self.InvDict.values())
    #print("KEYS= ",keys,"          VALUES= ",values)
    try:
        id= values.index(entry)
        return keys[id] 
    except ValueError:
      return None

  def addEntry(self,entry):
    e_id= self.getId(entry)
    #print("EID VAL= ",e_id)
    if e_id is None:
      self.Dict.append(entry)
      e_id= len(self.Dict)-1
      self.InvDict[e_id]= entry
    #print(" INVDICT: ENCODER= ",self.InvDict)
    #print(" DICT: ENCODER= ",self.Dict)
    return e_id

  def getEntry(self,id):
    if id is not None:
      return self.Dict[id]

  def getIdorAdd(self,entry):
    return self.addEntry(entry)

  def encode(self,seq):
    #print("----------------------------")
    #print("DICT= ",self.Dict)
    #print("INVDICT= ",self.InvDict)
    #print("----------------------------")
    if len(seq) == 0:
      return seq
    encoded= []
    seqSize= len(seq)
    i=0
    while i< seqSize:
      #print("EVERY ITER: ",i)
      candidate= seq[i:seqSize]
      #print("Candidate= ",candidate)
      idFound= None
      while idFound is None and len(candidate) >0:
        idFound= self.getId(candidate)
        #print("FOUND THE ID: ",idFound, " for ",candidate)
        if idFound is not None:
          #print("**************ENCODED APPENDED")
          encoded.append(idFound)
          i+= len(candidate)-1
        elif len(candidate)== 1:
          idFound= self.addEntry(candidate)
          encoded.append(idFound)
        else:
          candidate= candidate[:len(candidate)-1]
          #print("Reduced the length of candidate= ",candidate)
        #print("ENCODED LIST= ",encoded)
      i= i+1    
    #print(" INVDICT: ENCODER= ",self.InvDict)
    #print(" DICT: ENCODER= ",self.Dict)
    return encoded

  def decode(self,seq):
    if len(seq) == 0:
      return seq
    decoded= []
    for encodedItem in seq:
      #print("ENCODED ITEM= ",encodedItem)
      itemset= self.getEntry(encodedItem)
      if itemset is not None:
        for decodedItem in itemset:
          decoded.append(decodedItem)
      else:
        print("Could not find item: ", encodedItem)
    return decoded