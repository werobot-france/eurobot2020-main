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
    #stopOn = None if 'stopOn' not in args else args['stopOn']
    backward = False if 'backward' not in args else args['backward']
    
    
    # stop on slips marche comme  ça:
    # on regarde tout les 10 cycles de combien le robot à avancé avec deltaDist
    # si la dist avancé pendant ces 10 derniers cycles est infé à un threshold on se stoppe
    # quand stopOnSlip est à True, il n'y a plus de check pour savoir si le robot est arrivé
    # WARNING: VERY UNSTABLE WHEN TRAVELING BIG DISTANCES
    stopOnSlip = False if 'stopOnSlip' not in args else args['stopOnSlip']

    self.done = False
    self.logger.info("GoTo", {
      'x': targetX,
      'y': targetY,
      'theta': degrees(orientation) if orientation != None else None,
      'stopOnSlip': stopOnSlip,
      'speed': speed,
      'threshold': threshold,
      'backward': backward
    })

    p, i, d = 250, 0, 0
    sommeErreurs = differenceErreurs = erreurPre = orientationError = 0
    
    lastSlipPeriodDist = None
    slipCheckThreshold = 5
    slipCheckCount = 0
    
    while not self.done:
      x, y, theta = self.positionWatcher.getPos()
      if theta > pi: theta -= 2*pi
      
      # if backward:
      #   theta -= pi
      
      targetDistance = sqrt((targetX-x)*(targetX-x)+(targetY-y)*(targetY-y))
      targetTheta = atan2((targetY - y), (targetX - x))

      #if abs(orientationError)>pi/2: backward = not backward

      # if not backward:
      #   orientationError = (targetTheta - theta)
      # else:
      #   orientationError = (targetTheta - (theta-pi))
      #   if orientationError > pi: orientationError -= 2*pi
      if backward:
        orientationError = (targetTheta - (theta-pi))
        if orientationError > pi: orientationError -= 2*pi
        elif orientationError <= -pi: orientationError += 2*pi
      else:
        orientationError = (targetTheta - theta)%(2*pi)
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
      
      #self.platform.setSpeed([cmdG, cmdD])
      if backward:
        self.platform.setSpeed([-cmdD, -cmdG])
      else:
        self.platform.setSpeed([cmdG, cmdD])

      if targetDistance < threshold and not stopOnSlip:
        self.done = True
      
      # Check if a slip is happening
      slipCheckCount += 1
      if slipCheckCount >= 10:
        if lastSlipPeriodDist != None:
          if abs(lastSlipPeriodDist - targetDistance) < slipCheckThreshold:
            self.done = True
        slipCheckCount = 0
        lastSlipPeriodDist = targetDistance
      
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

      # Pause the navigation
      while self.isPaused:
        self.platform.stop()
        sleep(1)
      
      if backward:
        self.platform.setSpeed([-cmdD, -cmdG])
      else:
        self.platform.setSpeed([cmdG, cmdD])

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
    clockwise = None if 'clockwise' not in args else args['clockwise']
    fullRotation = None if 'fullRotation' not in args else args['fullRotation']
    
    theta = self.positionWatcher.getTheta()
    fullRotationMiddle = (theta + 0.85*pi)%(2*pi)
    print(degrees(theta))
    print(degrees(theta+pi/4))
    print(degrees(fullRotationMiddle))
    
    self.done = False
    self.logger.info("OrientTo", {
      'threshold': degrees(threshold),
      'currentTheta': degrees(theta),
      'targetTheta': degrees(targetTheta),
      'speed': speed,
      'fullRotation': fullRotation,
      'clockwise': clockwise
    })

    p, i, d = 120, 0, 0
    sommeErreurs = differenceErreurs = erreurPre = orientationError = 0

    stopCount = 0
    once = False
    while not self.done:
      x, y, theta = self.positionWatcher.getPos()
      if theta > pi:
        theta -= 2*pi
        if fullRotationMiddle > pi:
          fullRotationMiddle -= 2*pi

      if not once and fullRotation and theta < fullRotationMiddle:
        orientationError = 2*pi
        if clockwise:
          orientationError *= -1
        print('INF')
      else:
        print('SUP')
        once = True
        errorsChoice = [
          (targetTheta - theta),
          (targetTheta + 2*pi - theta),
          (targetTheta - 2*pi - theta)
        ]
        formattedChoices = list(map(lambda p: abs(p), errorsChoice))
        minO = min(formattedChoices)
        
        if clockwise == None:
          orientationError = errorsChoice[formattedChoices.index(minO)]
        elif clockwise:
          orientationError = -1*minO
        else:
          orientationError = minO

      cmdG = cmdD = 0
      cmd = (orientationError*p) + (sommeErreurs*i) + (differenceErreurs*d)
      if abs(cmd*speed/255) < 10: cmd = 10*255/speed * self.sign(cmd)
      if abs(cmd) > 255: cmd = 255 * self.sign(cmd)
      cmd /= 255
      
      cmdD += cmd * speed
      cmdG -= cmd * speed
      
      differenceErreurs = orientationError - erreurPre
      sommeErreurs += orientationError
      erreurPre = orientationError

      self.platform.setSpeed([cmdG, cmdD])

      self.logger.debug({
        'theta': round(degrees(theta), 3),
        'targetTheta': round(degrees(targetTheta), 3),
        'cmd': [cmd, cmdG, cmdD],
        'orientationError': round(degrees(orientationError), 3),
        'lastOrientationError': round(degrees(erreurPre), 2),
        'coef': [p, i, d]
      })
      
      if abs(orientationError) < pi/4:
        clockwise = None
      
      # we disable the threshold
      
      if not (fullRotation and not once) and abs(orientationError) < threshold:
        stopCount += 1
        if stopCount > 4:
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