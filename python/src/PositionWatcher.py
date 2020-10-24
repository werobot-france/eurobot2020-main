from gpiozero import DigitalInputDevice
from .ThreadHelper import Thread
import time
from math import *

'''
This class manage all the odometry operations
'''
class PositionWatcher:
  
  perimeter = 202.6 #200#207#210#205
  
  # 235
  axialDistance = 224.5 #235#236.5#233.5
  
  defaultX = 623.5 #900
  defaultY = 203 #200
  defaultTheta = pi

  # left (scotch rouge) encodeur
  phaseA = DigitalInputDevice(27, True)
  phaseB = DigitalInputDevice(17, True)
  
  # right (sans scotch) encodeur
  phaseC = DigitalInputDevice(5, True)
  phaseD = DigitalInputDevice(16, True)

  
  watchPositionThread = None
  watchTicksThread = None
  
  watchTicksEnabled = False
  watchPositionEnabled = False

  positionChangedHandler = None
  
  ignoreXChanges = False 

  def __init__(self, container):
    self.logger = container.get('logger').get('PositionWatcher')
    self.reset(False)
    
  def setIgnoreXChanges(self, val):
    self.logger.info('ignoreXChanges is now at', val)
    self.ignoreXChanges = val
  
  '''
  This thread will keep updated all the ticks counts
  '''
  def watchTicks(self):
    self.logger.info('WatchTicks thread START!')
    while self.watchTicksEnabled:
      leftFetchedState = (self.phaseA.value, self.phaseB.value)
      rightFetchedState = (self.phaseC.value, self.phaseD.value)
      
      if not self.ignoreXChanges:
        if leftFetchedState != self.leftState:
          self.leftState = leftFetchedState

          if self.leftState[0] == self.leftOldState[1]:
            self.leftTicks -= 1
          else:
            self.leftTicks += 1

          self.leftOldState = self.leftState

        if rightFetchedState != self.rightState:
          self.rightState = rightFetchedState

          if self.rightState[0] == self.rightOldState[1]:
            self.rightTicks -= 1
          else:
            self.rightTicks += 1

          self.rightOldState = self.rightState

    self.logger.info("WatchTicks thread QUIT!")

  '''
  /!\ Call once
  '''
  def computePosition(self):
    newTicks = (self.leftTicks, self.rightTicks)
    if (newTicks != self.oldTicks):
      deltaTicks = (
        newTicks[0] - self.oldTicks[0],
        newTicks[1] - self.oldTicks[1],
      )
      self.oldTicks = newTicks
      
      leftDistance = deltaTicks[0] / 2400 * self.perimeter
      rightDistance = deltaTicks[1] / 2400 * self.perimeter

      tb = (leftDistance + rightDistance) / 2
      deltaTheta = (rightDistance - leftDistance) / self.axialDistance
      
      
      self.theta += deltaTheta
      self.theta = self.theta % (2*pi)
      self.x += cos(self.theta) * tb
      self.y += sin(self.theta) * tb

      if self.positionChangedHandler != None:
        self.positionChangedHandler(self.x, self.y, self.theta)

    return (self.x, self.y, self.theta)

  def watchPosition(self):
    self.logger.info("WatchPosition thread START!")
    while self.watchPositionEnabled:
      self.computePosition()
      time.sleep(0.01)
    self.logger.info("WatchPosition thread QUIT!")

  def startWatchTicks(self):
    if not self.watchTicksEnabled:
      self.watchTicksEnabled = True
      self.watchTicksThread = Thread(target=self.watchTicks)
      self.watchTicksThread.start()
  
  def startWatchPosition(self):
    if not self.watchPositionEnabled:
      self.watchPositionEnabled = True
      self.watchPositionThread = Thread(target=self.watchPosition)
      self.watchPositionThread.start()
      
  def start(self):
    self.startWatchTicks()
    self.startWatchPosition()

  def stop(self):
    self.watchTicksEnabled = False
    self.watchPositionEnabled = False
    if self.watchTicksThread != None:
      self.watchTicksThread.stop()
    if self.watchPositionThread != None:
      self.watchPositionThread.stop()

  def pauseWatchPosition(self):
    self.watchPositionEnabled = False
    
  def resumeWatchPosition(self):
    self.startWatchPosition()

  def setPositionChangedHandler(self, handler):
    self.positionChangedHandler = handler

  def getTicks(self):
    return (self.leftTicks, self.rightTicks)
  
  def getPos(self):
    return (self.x, self.y, self.theta)

  def getData(self):
    return (self.x, self.y, self.theta)
  
  def getX(self):
    return self.x
  
  def getY(self):
    return self.y
  
  def getTheta(self):
    return self.theta

  def setPos(self, x = None, y = None, theta = None):
    if x != None:
      self.x = x
    if y != None:
      self.y = y
    if theta != None:
      self.theta = theta
    self.logger.info('Now set to', {
      'x': round(self.x, 0),
      'y': round(self.y, 0),
      'theta': round(degrees(self.theta), 2)
    })

  def reset(self, log = True):
    self.x = self.defaultX
    self.y = self.defaultY
    self.theta = self.defaultTheta

    self.leftTicks = 0
    self.rightTicks = 0
    self.backTicks = 0

    self.leftState = (0, 0)
    self.leftOldState = (0, 0)

    self.rightState = (0, 0)
    self.rightOldState = (0, 0)
    
    self.backState = (0, 0)
    self.backOldState = (0, 0)

    self.oldTicks = (0, 0, 0)

    if log:
      self.logger.info("Reset done: position and orientation are at the default values")
