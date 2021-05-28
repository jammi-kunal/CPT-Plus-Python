

import copy

class FIFRaw():
  itemFrequencies= {} #item and integer
  isets= []

  def __init__(self):
    itemFrequencies= {}
    isets= []

  def findFrequentItemsets(self,seqs,minLen,maxLen,minSup):
    #print("HELLO",seqs,minLen,maxLen,minSup)
    support= None
    frequents= [] #this list is a list of sequences
    frequencies= {} #this is a dictionary which stores the support and the itemsets. it has a integer as key and list of lists as value
    #itemList= [] this is a list of list used as the value in frequencies
    if maxLen<=1 or minLen> maxLen:
      return frequents
    for seq in seqs:
      if len(seq)> minLen:
        i=0
        while i<len(seq)-1:
          itemset= []
          offset= i
          while offset-i < maxLen and offset <len(seq):
            itemset.append(seq[offset])
            if len(itemset) >= minLen:
              keys= list(frequencies.keys())
              vals= list(frequencies.values())  #vals is a list of list. acts as a hashtable(java version) in the original code. Can store duplicates.
              #print(keys,vals)
              try:  
                if vals is not None:
                  for val in vals:
                    if val is not None:
                      index = val.index(itemset) if itemset in val else -1
                      if index is not -1:
                        support= keys[vals.index(val)]
                        break
                      else:
                        support= None
              except ValueError:
                #print("Value Error")
                support= None
              if support is None:
                support= 0
              itemList= []
              if len(keys)>=1 and support+1 in keys:
                itemList= frequencies.get(support+1)
              if itemList is None:
                itemList= []
              itemList.append(itemset)
              frequencies[support+1]= copy.deepcopy(itemList)
            offset= offset+1
          #print(frequencies)
          #print(frequents)
          keys= list(self.itemFrequencies.keys())
          vals= list(self.itemFrequencies.values())
          try:
            index= vals.index(seq[i])
            support= keys[i]
          except (ValueError,IndexError):
            support= None
          if support is None:
            support= 0
          support= support+1
          self.itemFrequencies[support]= seq[i]  
          i= i+1
    #print("ITEMFREQUENCIES= ",self.itemFrequencies)
    for key,value in frequencies.items():
      #print("Key= ",key,"    Value= ",value)
      if key>= minSup:
        for val in value:
          #print("Val= ",val,"  Length of val= ",len(val))
          if len(val)>1:
            frequents.append(val)
    return frequents

