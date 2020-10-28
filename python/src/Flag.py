from time import sleep
from .ThreadHelper import Thread

'''
Abstration of the flag component
Goal: to enable the flag at the 95 second
'''
class Flag:

  opened = False
  driver = None
  servoSlot = 6
  
  def __init__(self, container = None):
    self.logger = container.get('logger').get('Flag')
    self.driver = container.get('driver')
    if self.driver == None:
      self.logger.warn('mocked!')

  def open(self):
    self.opened = True
    self.driver.setAngle(self.servoSlot, 90, 'flag')
    self.logger.info('Opened!')

  def close(self):
    self.opened = False
    self.driver.setAngle(self.servoSlot, 180, 'flag')
    self.logger.info('Closed!')
  
  def toggle(self):
    if self.opened:
      self.close()
    else:
      self.open()

  def start(self):
    self.mainThread = Thread(target=self.run)
    self.mainThread.start()
  
  def stop(self):
    self.mainThread.stop()
  
  def run(self):
    self.close()
    self.logger.info('Starting timer, ready to fire!')
    sleep(95)
    self.logger.info('95 seconds ellapsed!')
    self.open()

