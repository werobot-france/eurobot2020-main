import json
from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo
from time import sleep

class Claw:

  def __init__(self, container, config = {
    'top': 10,
    'bottom': 115,
    'middle': 50,
    'elevator': 7,
    'claws': [6, 5, 4]
  }):
    self.base = '/home/pi/eurobot2020-main/python/tmp'
    self.driver = container.get('driver')
    
    self.container = container
    self.elevatorAngle = 0
    self.clawsAngle = [0, 0, 0]
    self.slotTmp = {}
    self.servoProfile = 'rev'
    
    self.clawsSlot = config['claws']
    self.elevatorSlot = config['elevator']
    
    self.bottomPos = config['bottom']
    self.middlePos = config['middle']
    self.topPos = config['top']
  
  def setAngle(self, slot, angle):
    self.driver.setAngle(slot, angle, self.servoProfile)
  
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
    
  def goMiddle(self):
    self.directGoTo(self.middlePos)
    
  def goTop(self):
    self.directGoTo(self.topPos)

  def goBottom(self):
    self.directGoTo(self.bottomPos)
    
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
    print('OPEN')
    self.setAll([
      60,
      140,
      140
    ])

  def close(self, selector = None):
    print('CLOSE')
    self.setAll([
      150,
      65,
      40
    ])
  
  def sleep(self, selector = None):
    self.setClawsAngle(50, selector)

  def stop(self):
    pass