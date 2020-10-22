import json
from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo
from time import sleep

class Claw:

  def __init__(self, container, config = {
    'elevatorPos': {
      'top': 50,
      'middle': 100,
      'bottom': 150
    },
    'clawsPos': {
      'open': [90, 90, 90],
      'close': [90, 90, 90]
    },
    'elevatorSlot': 7,
    'clawsSlot': [6, 5, 4]
  }):
    self.base = '/home/pi/eurobot2020-main/python/tmp'
    self.driver = container.get('driver')
    
    self.container = container
    self.elevatorAngle = 0
    self.clawsAngle = [0, 0, 0]
    self.slotTmp = {}
    
    self.clawsSlot = config['clawsSlot']
    self.elevatorSlot = config['elevatorSlot']
    
    self.clawsPos = config['clawsPos']
    self.elevatorPos = config['elevatorPos']

    self.clawsProfile = config['clawsProfile']
    self.elevatorProfile = config['elevatorProfile']
    self.id = config['id']
  
  def setAngle(self, slot, angle):
    if slot == self.elevatorSlot:
      profile = self.elevatorProfile
    else:
      profile = self.clawsProfile
    self.driver.setAngle(slot, angle, profile)
  
  def fetchStatus(self):
    status = open(self.base + '/claw-' + self.id + '-status.json')
    s = json.loads(status.read())
    status.close()
    self.elevatorAngle = s['elevator']
    #self.clawsAngle = s['claws']
  
  def saveStatus(self):
    status = open(self.base + '/claw-' + self.id + '-status.json', 'w')
    d = json.dumps({
      'id': self.id,
      'elevator': self.elevatorAngle,
      #'claws': self.clawsAngle
    })
    print(self.id, 'saving status of claw', d)
    status.write(d)
    status.close()
    
  def goMiddle(self):
    self.directGoTo(self.elevatorPos['middle'])
    
  def goTop(self):
    self.directGoTo(self.elevatorPos['top'])

  def goBottom(self):
    self.directGoTo(self.elevatorPos['bottom'])
    
  def directGoTo(self, target):
    # self.elevatorAngle = target
    # self.setAngle(self.elevatorSlot, target)
    self.goTo(target)

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
        self.elevatorAngle -= interstice if abs(delta) >= interstice else -delta
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
      b = a
      b -= 10
      self.setAngle(self.clawsSlot[0], 180 - b)
      self.clawsAngle[0] = 180 - b
    if 'mid' in selector:
      self.setAngle(self.clawsSlot[1], a)
      self.clawsAngle[1] = a
    if 'right' in selector:
      self.setAngle(self.clawsSlot[2], a)
      self.clawsAngle[2] = a
  
  def setAll(self, angles):
    print('SET ALL CLAWS!', angles)
    self.clawsAngles = angles

    self.setAngle(self.clawsSlot[0], angles[0])
    self.setAngle(self.clawsSlot[1], angles[1])
    self.setAngle(self.clawsSlot[2], angles[2])

  def open(self, selector = None):
    self.setAll([
      self.clawsPos['open'][0],
      self.clawsPos['open'][1],
      self.clawsPos['open'][2]
    ])

  def sleep(self, selector = None):
    self.setAll([
      self.clawsPos['sleep'][0],
      self.clawsPos['sleep'][1],
      self.clawsPos['sleep'][2]
    ])

  def close(self, selector = None):
    self.setAll([
      self.clawsPos['close'][0],
      self.clawsPos['close'][1],
      self.clawsPos['close'][2]
    ])
  
  # def sleep(self, selector = None):
  #   self.setClawsAngle(50, selector)

  def stop(self):
    pass