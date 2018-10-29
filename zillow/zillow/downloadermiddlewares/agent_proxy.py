class Agent(object):
  """ Specify single proxy agent object
      Atttribute:
          proxy: like "http://45.78.34.180:8080"
          success: this proxy's life value (just like solder's blood value in game),\
                  it minus one if failed and plus one if successed
          percentage: proxy's percentage of successful useage, successful_times/total_using-times,default 100%
          absolute_threshold:
          percentage_threshold:
          label: valid or invalid
          last_condition: the success condition of last useage
  """
  def __init__(self,proxy, success=800, percentage=0.8, absolute_threshold=300, percentage_threshold=0.50):
    self.proxy = "http://" + str(proxy)   if not proxy.startswith("http://") else proxy
    self.success = int(success) 
    self.percentage = percentage
    self.total = int(self.success/self.percentage)
    self.absolute_threshold = absolute_threshold
    self.percentage_threshold = percentage_threshold 
    self._set_label()
    self._set_last_condition()  

  def _set_label(self):
    """set label according to other absolute and relative parameter
    """
    if self.success < self.absolute_threshold or \
        self.percentage < self.percentage_threshold:
      self.label = "invalid" 
    else:
      self.label = 'valid'

  def _set_last_condition(self,condition=True):
    """ Set last success use condition of the agent: True or False
    """
    self.last_condition = True if condition else False

  def weaken(self):
    """ After an failed usage
    """  
    self.total = self.total + 1
    self.success = self.success - 1
    self.percentage = self.success/self.total
    self._set_last_condition(condition=False)
    self._set_label()

  def stronger(self):         
    """ After a successful usage
    """       
    self.total = self.total + 1
    self.success = self.success + 1
    self.percentage = self.success/self.total
    self._set_last_condition(condition=True)
    self._set_label()

  def set_invalid(self):
    """direct way to change validation condition
    """
    self.last_condition = False
    self.label = "invalid"

  def is_valid(self):
    """bool"""
    return self.label == "valid"

  def __eq__(self,other):
    return self.proxy == other.proxy
