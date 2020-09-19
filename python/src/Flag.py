from time import sleep
from .ThreadHelper import Thread

'''
Abstration of the flag component
Goal: to enable the flag at the 95'' second
'''
class Flag:

  driver = None
  
  # the last servo slot of the first slots block
  servoSlot = 3
  
  def __init__(self, container = None):
    self.logger = container.get('logger').get('Flag')
    self.driver = container.get('driver')
    if self.driver == None:
      self.logger.warn('mocked!')

  def open(self, values):
    self.driver.setAngle(self.servoSlot, 0, 'flag')
    self.logger.info('opened!')

  def close(self, values):
    self.driver.setAngle(self.servoSlot, 90, 'flag')
    self.logger.info('closed!')

  def start(self):
    self.mainThread = Thread(target=self.run)
    self.mainThread.start()
  
  def stop(self):
    self.mainThread.stop()
  
  def run(self):
    self.close()
    self.logger.info('started, ready to fire!')
    sleep(95)
    self.open()

