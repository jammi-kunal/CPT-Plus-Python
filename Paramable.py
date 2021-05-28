class Paramable():
  parameters= {}

  def __init__(self,Parameters= None):
    self.parameters= Parameters

  def setParameters(self,Parameters):
    self.parameters= Parameters

  def paramDouble(self,name):
    value= self.parameters.get(name)
    return self.parameters.get(name) if value is not None else None

  def paramDoubleOrDefault(self,paramName,defaultValue):
    param= self.paramDouble(paramName)  
    return param if param is not None else defaultValue
  
  def paramInt(self,name):
    value= self.parameters.get(name)
    return self.parameters.get(name) if value is not None else None

  def paramIntOrDefault(self,paramName,defaultValue):
    param= self.paramInt(paramName)  
    return param if param is not None else defaultValue
  
  def paramFloat(self,name):
    value= self.parameters.get(name)
    return self.parameters.get(name) if value is not None else None

  def paramFloatOrDefault(self,paramName,defaultValue):
    param= self.paramFloat(paramName)  
    return param if param is not None else defaultValue
  
  def paramBool(self,name):
    value= self.parameters.get(name)
    return self.parameters.get(name) if value is not None else None

  def paramBoolOrDefault(self,paramName,defaultValue):
    param= self.paramBool(paramName)  
    return param if param is not None else defaultValue
  