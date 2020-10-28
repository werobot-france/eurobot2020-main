from math import *
import time
from time import sleep

'''
This class manage all the movement of the robot motorized platform
'''
class Navigation:
  def __init__(self, container):
    self.logger = container.get('logger').get('Navigation')
    self.platform = container.get('platform')
    self.positionWatcher = container.get('positionWatcher')
    self.switches = container.get('switches')
    self.enabled = False

  '''
  Private
  '''
  def getSpeedFromAngle(self, targetAngle, speed):
    ta = pi - (targetAngle - self.positionWatcher.theta)
    return [
      cos(ta+3*pi/4) * speed,
      sin(ta+3*pi/4) * speed,
      sin(ta+3*pi/4) * speed,
      cos(ta+3*pi/4) * speed,
    ]

  '''
  @Private
  '''
  def getPlatformSpeed(self, initialDist, dist, maxSpeed, minSpeed):
    p = abs(initialDist - dist)
    if p <= 25:
      return self.saturation(0, 25, minSpeed, maxSpeed, p)
    else:
      l = maxSpeed - minSpeed
      k = 0.04
      o = 100
      return (l/(1+exp(-(k*(dist - o))))) + minSpeed

  '''
  @Private
  '''
  def saturation(self, minX, maxX, minY, maxY, value):
    # minX = 10*10
    # maxX = 100*10
    # minY = 10
    # maxY = 100
    minX *= 10
    maxX *= 10
    if value <= minX:
      #print('Very start thing case')
      return minY
    elif value >= maxX:
      #print('Normal cruise')
      return maxY
    else:
      #print('Start thing case')
      a = (maxY-minY)/(maxX - minX)
      b = minY - a*minX
      return a * value + b

  '''
  Public
  '''
  def goTo(self, **args):
    # x, y, theta = None, speed = 50, threshold = 5, stopOn = None
    targetX = args['x']
    targetY = args['y']
    orientation = None if 'theta' not in args else args['theta']
    speed = 40 if 'speed' not in args else args['speed']
    threshold = 5 if 'threshold' not in args else args['threshold']
    stopOn = None if 'stopOn' not in args else args['stopOn']
  
    # stop on slips marche comme  ça:
    # on regarde tout les 10 cycles de combien le robot à avancé avec deltaDist
    # si la dist avancé pendant ces 10 derniers cycles est infé à un threshold on se stoppe
    # quand stopOnSlip est à True, il n'y a plus de check pour savoir si le robot est arrivé
    # WARNING: VERY UNSTABLE WHEN TRAVELING BIG DISTANCES
    stopOnSlip = False if 'stopOnSlip' not in args else args['stopOnSlip']
    
    # targetX, targetY, speed=50, threshold=5, orientation=None

    #self.positionWatcher.pauseWatchPosition()
    minSpeed = 25
    if speed < minSpeed:
      speed = minSpeed
    self.done = False
    targetAngle = atan2(targetY, targetX)
    self.logger.info("GoTo", {
      'x': targetX,
      'y': targetY,
      'theta': degrees(orientation),
      'stopOn': stopOn,
      'stopOnSlip': stopOnSlip,
      'speed': speed,
      'threshold': threshold
    })
    
    lastSlipPeriodDist = None
    slipCheckThreshold = 5
    slipCheckCount = 0

    #self.setSpeed(self.getSpeedFromAngle(targetAngle, speed))
    initialDist = None
    while not self.done:
      #x, y, theta = self.positionWatcher.computePosition()
      x, y, theta = self.positionWatcher.getPos()
      dist = sqrt((targetX - x)**2 + (targetY - y)**2)

      self.logger.debug({
        'x': round(x, 0),
        'y': round(y, 0),
        'theta': round(degrees(theta), 0),
        'targetAngle': round(degrees(targetAngle), 2)
      })

      if initialDist == None:
        initialDist = dist

      # Check if a slip is happening
      if stopOnSlip:
        slipCheckCount += 1
      if slipCheckCount >= 3:
        if lastSlipPeriodDist != None:
          if abs(lastSlipPeriodDist - dist) < slipCheckThreshold:
            self.done = True
        slipCheckCount = 0
        lastSlipPeriodDist = dist

      if dist <= threshold:
        self.done = True
      else:
        targetAngle = (atan2(targetY - y, targetX - x))%(2*pi)
        #print("targetAngle:", round(degrees(targetAngle), 2))
        s = self.getPlatformSpeed(initialDist, dist, speed, minSpeed)
        #print("speed", s)
        b = self.getSpeedFromAngle(targetAngle, s)

        if orientation != None:
          c = (theta - orientation)/2*pi
          if abs(c*speed) <= speed/4:
            cmd = c*speed
          else:
            cmd = speed/4*c/abs(c)
          cmds = [
            cmd,
            cmd,
            -cmd,
            -cmd
          ]
          for i in range(4):
            b[i] += cmds[i]
            
        #print("\nMotors:", b, "\n\n\n\n")
        self.platform.setSpeed(b)
        
        if stopOn != None:
          self.done = self.switches.getState(stopOn)

    #self.positionWatcher.resumeWatchPosition()
    self.platform.stop()
    self.logger.info("End of GoTo")

  '''
  Public
  '''
  def relativeGoTo(self, **args):
    # args = targetDeltaX, targetDeltaY, speed=50, threshold=5, orientation=None
    #self.positionWatcher.pauseWatchPosition()
    x, y, theta = self.positionWatcher.computePosition()
    args['x'] = x + cos(theta)*args['y'] - sin(theta)*args['x']
    args['y'] = y + sin(theta)*args['y'] - cos(theta)*args['x']
    self.goTo(**args)

  '''
  Public
  '''
  def orientTo(self, **args):
    orientation = args['theta']
    speed = 30 if 'speed' not in args else args['speed']
    threshold = pi/32 if 'threshold' not in args else args['threshold']
    # orientation, speed=30, threshold=pi/32
    
    #self.positionWatcher.pauseWatchPosition()
    
    theta = self.positionWatcher.computePosition()[2]
    
    self.logger.info("OrientTo", {
      'currentTheta': degrees(theta),
      'targetTheta': degrees(orientation),
      'speed': speed
    })
    
    while abs(theta - orientation) > threshold:
      theta = self.positionWatcher.computePosition()[2]
      c = (theta - orientation)/abs(theta - orientation)
      speeds = [
        c*speed,
        c*speed,
        -c*speed,
        -c*speed
      ]
      self.platform.setSpeed(speeds)
      self.logger.debug({
        'c': c,
        'deltaOrientation': round(degrees(theta - orientation), 2)
      })
    
    #self.positionWatcher.resumeWatchPosition()
    self.platform.stop()
    self.logger.info("End of OrientTo")

  '''
  Public
  '''
  def goToPath(self, path):
    for node in path:
      self.goTo(node)
      sleep(0.5)

    self.platform.stop()
    self.logger.info("Path done")
    
  def stop(self):
    self.done = True