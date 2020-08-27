import json
from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo
from time import sleep

class Claw:

  def __init__(self, container, slots = {'elevator': 7, 'claws': [6, 5, 4]}):
    self.base = '/home/pi/eurobot2020-main/python/tmp'
    self.driver = container.get('driver')
    self.setAngle = self.driver.setAngle
    
    self.container = container
    self.elevatorAngle = 0
    self.clawsAngle = [0, 0, 0]
    self.slotTmp = {}
    
    self.clawsSlot = slots['claws']
    self.elevatorSlot = slots['elevator']
  
  def fetchStatus(self):
    status = open(self.base + '/claw-status.json')
    s = json.loads(status.read())
    status.close()
    self.elevatorAngle = s['elevator']
    self.clawsAngle = s['claws']
  
  def saveStatus(self):
    status = open(self.base + '/claw-status.json', 'w')
    status.write(json.dumps({
      'elevator': self.elevatorAngle,
      'claws': self.clawsAngle
    }))
    status.close()
    
  def directGoTo(self, target):
    self.elevatorAngle = target
    self.setAngle(self.elevatorSlot, target)

  def goTo(self, target, d = 0.20):
    self.fetchStatus()
    delta = target - self.elevatorAngle
    interstice = 30
    print('initial elevator angle', self.elevatorAngle)
    print('target', target)
    while delta != 0:
      print('delta', delta)
      if delta > 0:
        self.elevatorAngle += interstice if abs(delta) >= interstice else delta
      else:
        self.elevatorAngle -= interstice if abs(delta) >= interstice else delta
      print('angle', self.elevatorAngle)
      self.setAngle(self.elevatorSlot, self.elevatorAngle)
      delta = target - self.elevatorAngle
      sleep(d)
    self.saveStatus()
  
  '''
  Function to manage the angle of the claws
  '''
  def setClawsAngle(self, angle, selector = None):
    a =   angle
    if selector == None:
      selector = ['left', 'mid', 'right']
    if 'left' in selector:
      self.setAngle(self.clawsSlot[0], 180 - a)
      self.clawsAngle[0] = 180 - a
    if 'mid' in selector:
      self.setAngle(self.clawsSlot[1], a)
      self.clawsAngle[1] = a
    if 'right' in selector:
      self.setAngle(self.clawsSlot[2], a)
      self.clawsAngle[2] = a

  def open(self, selector = None):
    self.setClawsAngle(120, selector)

  def close(self, selector = None):
    self.setClawsAngle(30, selector)
  
  def sleep(self, selector = None):
    self.setClawsAngle(50, selector)

  def stop(self):
    pass