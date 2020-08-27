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

  
  #-OLDHOLONOMIC%START
  # '''
  # Private
  # '''
  # def getSpeedFromAngle(self, targetAngle, speed):
  #   ta = pi - (targetAngle - self.positionWatcher.theta)
  #   return [
  #     cos(ta+3*pi/4) * speed,
  #     sin(ta+3*pi/4) * speed,
  #     sin(ta+3*pi/4) * speed,
  #     cos(ta+3*pi/4) * speed,
  #   ]
  
  # '''
  # @Private
  # '''
  # def getPlatformSpeed(self, initialDist, dist, maxSpeed, minSpeed):
  #   p = abs(initialDist - dist)
  #   if p <= 25:
  #     return self.saturation(0, 25, minSpeed, maxSpeed, p)
  #   else:
  #     l = maxSpeed - minSpeed
  #     k = 0.04
  #     o = 100
  #     return (l/(1+exp(-(k*(dist - o))))) + minSpeed

  # '''
  # @Private
  # '''
  # def saturation(self, minX, maxX, minY, maxY, value):
  #   # minX = 10*10
  #   # maxX = 100*10
  #   # minY = 10
  #   # maxY = 100
  #   minX *= 10
  #   maxX *= 10
  #   if value <= minX:
  #     #print('Very start thing case')
  #     return minY
  #   elif value >= maxX:
  #     #print('Normal cruise')
  #     return maxY
  #   else:
  #     #print('Start thing case')
  #     a = (maxY-minY)/(maxX - minX)
  #     b = minY - a*minX
  #     return a * value + b

  # '''
  # Public
  # '''
  # def goTo(self, **args):
  #   # x, y, theta = None, speed = 50, threshold = 5, stopOn = None
  #   targetX = args['x']
  #   targetY = args['y']
  #   orientation = None if 'theta' not in args else args['theta']
  #   speed = 40 if 'speed' not in args else args['speed']
  #   threshold = 5 if 'threshold' not in args else args['threshold']
  #   stopOn = None if 'stopOn' not in args else args['stopOn']
  #   # targetX, targetY, speed=50, threshold=5, orientation=None

  #   #self.positionWatcher.pauseWatchPosition()
  #   minSpeed = 25
  #   if speed < minSpeed:
  #     speed = minSpeed
  #   self.done = False
  #   targetAngle = atan2(targetY, targetX)
  #   self.logger.info("GoTo", {
  #     'x': targetX,
  #     'y': targetY,
  #     'theta': degrees(orientation),
  #     'stopOn': stopOn,
  #     'speed': speed,
  #     'threshold': threshold
  #   })
  #   #self.setSpeed(self.getSpeedFromAngle(targetAngle, speed))
  #   initialDist = None
  #   while not self.done:
  #     #x, y, theta = self.positionWatcher.computePosition()
  #     x, y, theta = self.positionWatcher.getPos()
  #     dist = sqrt((targetX - x)**2 + (targetY - y)**2)

  #     self.logger.debug({
  #       'x': round(x, 0),
  #       'y': round(y, 0),
  #       'theta': round(degrees(theta), 0),
  #       'targetAngle': round(degrees(targetAngle), 2)
  #     })

  #     if initialDist == None:
  #       initialDist = dist
  #     if dist <= threshold:
  #       self.done = True
  #     else:
  #       targetAngle = (atan2(targetY - y, targetX - x))%(2*pi)
  #       #print("targetAngle:", round(degrees(targetAngle), 2))
  #       s = self.getPlatformSpeed(initialDist, dist, speed, minSpeed)
  #       #print("speed", s)
  #       b = self.getSpeedFromAngle(targetAngle, s)

  #       if orientation != None:
  #         c = (theta - orientation)/2*pi
  #         if abs(c*speed) <= speed/4:
  #           cmd = c*speed
  #         else:
  #           cmd = speed/4*c/abs(c)
  #         cmds = [
  #           cmd,
  #           cmd,
  #           -cmd,
  #           -cmd
  #         ]
  #         for i in range(4):
  #           b[i] += cmds[i]
            
  #       #print("\nMotors:", b, "\n\n\n\n")
  #       self.platform.setSpeed(b)
        
  #       if stopOn != None:
  #         self.done = self.switches.getState(stopOn)

  #   #self.positionWatcher.resumeWatchPosition()
  #   self.platform.stop()
  #   self.logger.info("End of GoTo")

  # '''
  # Public
  # '''
  # def orientTo(self, **args):
  #   orientation = args['theta']
  #   speed = 30 if 'speed' not in args else args['speed']
  #   threshold = pi/32 if 'threshold' not in args else args['threshold']
  #   # orientation, speed=30, threshold=pi/32
    
  #   #self.positionWatcher.pauseWatchPosition()
    
  #   theta = self.positionWatcher.computePosition()[2]
    
  #   self.logger.info("OrientTo", {
  #     'currentTheta': degrees(theta),
  #     'targetTheta': degrees(orientation),
  #     'speed': speed
  #   })
    
  #   while abs(theta - orientation) > threshold:
  #     theta = self.positionWatcher.computePosition()[2]
  #     c = (theta - orientation)/abs(theta - orientation)
  #     speeds = [
  #       c*speed,
  #       c*speed,
  #       -c*speed,
  #       -c*speed
  #     ]
  #     self.platform.setSpeed(speeds)
  #     self.logger.debug({
  #       'c': c,
  #       'deltaOrientation': round(degrees(theta - orientation), 2)
  #     })
    
  #   #self.positionWatcher.resumeWatchPosition()
  #   self.platform.stop()
  #   self.logger.info("End of OrientTo")
  #-OLDHOLONOMIC%END

  def goTo(self, **args):
    # x, y, theta = None, speed = 50, threshold = 5, stopOn = None
    targetX = args['x']
    targetY = args['y']
    orientation = None if 'theta' not in args else args['theta']
    speed = 40 if 'speed' not in args else args['speed']
    threshold = 5 if 'threshold' not in args else args['threshold']
    stopOn = None if 'stopOn' not in args else args['stopOn']
    backward = False if 'backward' not in args else (args['backward'] == 'True')

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

      # self.logger.debug({
      #   'x': round(x, 0),
      #   'y': round(y, 0),
      #   'theta': round(degrees(theta), 0)
      # })
      
      distanceCible = sqrt((targetX-x)*(targetX-x)+(targetY-y)*(targetY-y))
      targetTheta = atan2((targetY - y), (targetX - x))

      # if abs(targetTheta - theta) > pi:
      #   backward = not backward

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
      
      # if distanceCible < 100:
      #   cmdD *= distanceCible/50
      #   cmdG *= distanceCible/50

      # print('\n\nposition Cible: ', (targetX, targetY))
      # print('position Robot: ', (x, y, degrees(theta)))
      # print('targetTheta: ', degrees(targetTheta))
      # print('erreur actuelle', degrees(erreurOrientation))
      # print('erreur précédente',degrees(erreurPre))
      # print('distance à la cible',distanceCible)
      # print((('CMD', cmd), ('G', cmdG), ('D', cmdD)))
      # print('Coeffs PID: ', (p, i, d))
      
      
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

      differenceErreurs = erreurOrientation - erreurPre
      sommeErreurs += erreurOrientation
      erreurPre = erreurOrientation

      if (not backward):
        self.platform.setSpeed([cmdG, cmdD])
      else:
        self.platform.setSpeed([-cmdD, -cmdG])

      if distanceCible < threshold:
        self.done = True

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
  
    self.done = False
    while not self.done:
      theta = self.positionWatcher.getPos()[2]
      deltaTheta = targetTheta - theta
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
        degrees(theta)
      )
      if abs(deltaTheta) > threshold:
        cmd = (abs(deltaTheta)/pi)/1.5*100
        if cmd < 10 : cmd = 10
        self.platform.setSpeed([cmd*coeffG,cmd*coeffD])
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
