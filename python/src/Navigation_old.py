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
  
  def goTo(self, **args):
    # x, y, theta = None, speed = 50, threshold = 5, stopOn = None
    targetX = args['x']
    targetY = args['y']
    orientation = None if 'theta' not in args else args['theta']
    speed = 40 if 'speed' not in args else args['speed']
    threshold = 5 if 'threshold' not in args else args['threshold']
    stopOn = None if 'stopOn' not in args else args['stopOn']
    backward = False if 'backward' not in args else (args['backward'] == 'True' or args['backward'])

    self.done = False
    self.logger.info("GoTo", {
      'x': targetX,
      'y': targetY,
      'theta': degrees(orientation) if orientation != None else None,
      'stopOn': stopOn,
      'speed': speed,
      'threshold': threshold
    })
    
    x, y, theta = self.positionWatcher.getPos()
    
    p, i, d = 3500, 0, 0
    sommeErreurs = differenceErreurs = erreurPre = 0
    distanceCibleI = sqrt((targetX-x)*(targetX-x)+(targetY-y)*(targetY-y))

    while not self.done:
      x, y, theta = self.positionWatcher.getPos()
      
      distanceCible = sqrt((targetX-x)*(targetX-x)+(targetY-y)*(targetY-y))
      targetTheta = atan2((targetY - y), (targetX - x))

      if (not backward):
          erreurOrientation = (targetTheta - theta)
      else:
          erreurOrientation = (targetTheta - (theta-pi))

      cmdG = cmdD = speed/100*10000

      if cmdD > 10000: cmdG = cmdD = 10000

      while abs(erreurOrientation) > pi:
          erreurOrientation += (-2*pi) * (erreurOrientation/abs(erreurOrientation))

      cmd = (erreurOrientation*p) + (sommeErreurs*i) + (differenceErreurs*d)
      cmdD += cmd
      cmdG -= cmd
      
      if abs(cmdD) > 10000: cmdD = 10000 * self.sign(cmdD) #if abs(cmdG)<vitesseR*10000 and cmdG != 0:cmdG = 10000*vitesseR * self.sign(cmdG)
      if abs(cmdG) > 10000: cmdG = 10000 * self.sign(cmdG) #if abs(cmdD)<vitesseR*10000 and cmdD != 0:cmdD = 10000*vitesseR * self.sign(cmdD)
      cmdD /= 100
      cmdG /= 100
      if abs(cmdD) < 1 : cmdD = 1 * self.sign(cmdD)
      if abs(cmdG) < 1 : cmdG = 1 * self.sign(cmdG)
      
      differenceErreurs = erreurOrientation - erreurPre
      sommeErreurs += erreurOrientation
      erreurPre = erreurOrientation

      if distanceCible < 100:
        cmdG/=2+2*distanceCible/distanceCibleI
        cmdD/=2+2*distanceCible/distanceCibleI

      if (not backward):
        self.platform.setSpeed([cmdG, cmdD])
      else:
        self.platform.setSpeed([-cmdD, -cmdG])

      if distanceCible < threshold:
        self.done = True
      
      self.logger.debug({
        'x': round(x, 0),
        'y': round(y, 0),
        'theta': round(degrees(targetTheta), 2),
        'targetTheta': round(degrees(targetTheta), 2),
        'targetDist': round(distanceCible, 2),
        'cmd': [cmd, cmdG, cmdD],
        'orientationError': round(degrees(erreurOrientation), 2),
        'lastOrientationError': round(degrees(erreurPre), 2),
        'coef': [p, i, d]
      })
      
      # stop quand ya un robot
      while self.isPaused:
        sleep(0.4)

    self.platform.stop()
    self.logger.info("End of GoTo")

  def sign(self, num):
    if num > 0: return 1
    if num == 0: return 0
    if num < 0: return -1
    
  def orientTo(self, **args):
    targetTheta = args['theta']
    speed = 30 if 'speed' not in args else args['speed']
    threshold = pi/50 if 'threshold' not in args else args['threshold']
    
    theta = self.positionWatcher.getPos()[2]
    self.logger.info("OrientTo", {
      'currentTheta': degrees(theta),
      'targetTheta': degrees(targetTheta),
      'speed': speed
    })

    if targetTheta > 3*pi/2 :
      targetTheta -= 2*pi

    cmd = 0
  
    self.done = False
    while not self.done:
      theta = self.positionWatcher.getPos()[2]
      deltaTheta = targetTheta - theta
      
      if deltaTheta < -pi :
        deltaTheta += 2*pi
      
      if deltaTheta >= 0:
        coeffG = -1
        coeffD = 1
      else:
        coeffG = 1
        coeffD = -1

      print(
        [
          abs(deltaTheta)/pi*100*coeffG,
          abs(deltaTheta)/pi*100*coeffD
        ],
        degrees(theta),
        [
          cmd*coeffG,
          cmd*coeffD
        ],
        deltaTheta
      )
      if abs(deltaTheta) > threshold:
        cmd = (abs(deltaTheta)/pi)/1.5*speed
        if cmd < 10 : cmd = 10
        self.platform.setSpeed([cmd*coeffG, cmd*coeffD])
      else:
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
    
  def resume(self):
    self.isPaused = False

    