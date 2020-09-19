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
    self.isPaused = False

  def saturation(self, minX, maxX, minY, maxY, value):
    if value <= minX:
      return minY
    elif value >= maxX:
      return maxY
    else:
      a = (maxY-minY)/(maxX - minX)
      b = minY - a*minX
      return a * value + b
  
  def goTo(self, **args):
    # x, y, theta = None, speed = 50, threshold = 5, stopOn = None
    targetX = args['x']
    targetY = args['y']
    orientation = None if 'theta' not in args else args['theta']
    speed = 50 if 'speed' not in args else args['speed']
    speed /= 2
    threshold = 10 if 'threshold' not in args else args['threshold']
    stopOn = None if 'stopOn' not in args else args['stopOn']
    backward = False if 'backward' not in args else args['backward']

    self.done = False
    self.logger.info("GoTo", {
      'x': targetX,
      'y': targetY,
      'theta': degrees(orientation) if orientation != None else None,
      'stopOn': stopOn,
      'speed': speed,
      'threshold': threshold,
      'backward': backward
    })

    p, i, d = 150, 0, 0
    sommeErreurs = differenceErreurs = erreurPre = orientationError = 0

    while not self.done:
      x, y, theta = self.positionWatcher.getPos()
      if theta > pi: theta -= 2*pi
      
      targetDistance = sqrt((targetX-x)*(targetX-x)+(targetY-y)*(targetY-y))
      targetTheta = atan2((targetY - y), (targetX - x))

      #if abs(orientationError)>pi/2: backward = not backward

      if not backward:
        orientationError = (targetTheta - theta)
      else:
        orientationError = (targetTheta - (theta-pi))
        if orientationError > pi: orientationError -= 2*pi

      tmpSpeed = self.saturation(10, 150, 15, speed, targetDistance)
      #tmpSpeed = speed

      cmdG = cmdD = tmpSpeed
      cmd = (orientationError*p) + (sommeErreurs*i) + (differenceErreurs*d)
      if abs(cmd) > 255: cmd = 255 * self.sign(cmd)
      cmd /= 255
      cmdD += cmd * tmpSpeed
      cmdG -= cmd * tmpSpeed

      differenceErreurs = orientationError - erreurPre
      sommeErreurs += orientationError
      erreurPre = orientationError

      if not backward:
        self.platform.setSpeed([cmdG, cmdD])
      else:
        self.platform.setSpeed([-cmdD, -cmdG])

      if targetDistance < threshold:
        self.done = True
      
      self.logger.debug({
        'x': round(x, 0),
        'y': round(y, 0),
        'theta': round(degrees(theta), 2),
        'targetTheta': round(degrees(targetTheta), 2),
        'targetDist': round(targetDistance, 2),
        'cmd': [cmd, cmdG, cmdD],
        'orientationError': round(degrees(orientationError), 2),
        'lastOrientationError': round(degrees(erreurPre), 2),
        'coef': [p, i, d]
      })

      # stop quand ya un robot
      while self.isPaused:
        self.platform.stop()
        sleep(1)

      if (not backward):
        self.platform.setSpeed([cmdG, cmdD])
      else:
        self.platform.setSpeed([-cmdD, -cmdG])

    self.platform.stop()
    self.logger.info("End of GoTo")

  def sign(self, num):
    if num > 0: return 1
    if num == 0: return 0
    if num < 0: return -1
    
  def orientTo(self, **args):
    targetTheta = args['theta']
    speed = 30 if 'speed' not in args else args['speed']
    threshold = pi/100 if 'threshold' not in args else args['threshold']

    self.done = False
    theta = self.positionWatcher.getTheta()
    self.logger.info("OrientTo", {
      'currentTheta': degrees(theta),
      'targetTheta': degrees(targetTheta),
      'speed': speed
    })

    p, i, d = 110, 2, 10
    sommeErreurs = differenceErreurs = erreurPre = orientationError = 0

    while not self.done:
      x, y, theta = self.positionWatcher.getPos()
      if theta > pi: theta -= 2*pi

      errorsChoice = [
        (targetTheta - theta),
        (targetTheta + 2*pi - theta),
        (targetTheta - 2*pi - theta)
      ]
      formattedChoices = list(map(lambda p: abs(p), errorsChoice))
      orientationError = errorsChoice[formattedChoices.index(min(formattedChoices))]

      cmdG = cmdD = 0
      cmd = (orientationError*p) + (sommeErreurs*i) + (differenceErreurs*d)
      if abs(cmd) > 255: cmd = 255 * self.sign(cmd)
      cmd /= 255
      cmdD += cmd * speed
      cmdG -= cmd * speed
      
      differenceErreurs = orientationError - erreurPre
      sommeErreurs += orientationError
      erreurPre = orientationError

      self.platform.setSpeed([cmdG, cmdD])

      if abs(orientationError) < threshold:
        self.done = True

    self.platform.stop()
    self.logger.info("End of OrientTo", round(degrees(theta), 2))

  '''
  Public
  '''
  def relativeGoTo(self, **args):
    x, y, theta = self.positionWatcher.computePosition()
    args['x'] = x + cos(theta)*args['y'] - sin(theta)*args['x']
    args['y'] = y + sin(theta)*args['y'] - cos(theta)*args['x']
    self.goTo(**args)

  '''
  Public
  '''
  def goToPath(self, path):
    for node in path:
      self.goTo(**node)
      sleep(0.5)

    self.platform.stop()
    self.logger.info("Path done")
    
  def stop(self):
    self.done = True

  def pause(self, state = True):
    self.isPaused = state
    self.logger.info('Navigation paused')

  def resume(self):
    self.isPaused = False
    self.logger.info('Navigation resumed')