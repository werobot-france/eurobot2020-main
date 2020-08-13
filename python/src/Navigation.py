from math import *
import time
from time import sleep

'''
This class manage all the movement of the robot motorized platform
'''
class Navigation:
  def __init__(self, container):
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
      print('Very start thing case')
      return minY
    elif value >= maxX:
      print('Normal cruise')
      return maxY
    else:
      print('Start thing case')
      a = (maxY-minY)/(maxX - minX)
      b = minY - a*minX
      return a * value + b

  '''
  Public
  '''
  def goTo(self, **args):
    print(args)
    # x, y, theta = None, speed = 50, threshold = 5, stopOn = None
    targetX = args['x']
    targetY = args['y']
    orientation = None if 'theta' not in args else args['theta']
    orientationError = 0
    speed = 40 if 'speed' not in args else args['speed']
    threshold = 5 if 'threshold' not in args else args['threshold']
    stopOn = None if 'stopOn' not in args else args['stopOn']
    # targetX, targetY, speed=50, threshold=5, orientation=None

    #self.positionWatcher.pauseWatchPosition()
    minSpeed = 25
    if speed < minSpeed:
      speed = minSpeed
    self.done = False
    targetAngle = atan2(targetY, targetX)
    print("> Navigation: going to (x: %(x)f y: %(y)f) with a angle of %(a)f deg" % {
      'x': targetX,
      'y': targetY,
      'a': degrees(targetAngle)
    })
    #self.setSpeed(self.getSpeedFromAngle(targetAngle, speed))
    initialDist = None
    while not self.done:
      #x, y, theta = self.positionWatcher.computePosition()
      x, y, theta = self.positionWatcher.getPos()
      dist = sqrt((targetX - x)**2 + (targetY - y)**2)

      print("\n\nx:", round(x, 0))
      print("y:", round(y, 0))
      print("theta:", round(degrees(theta), 0))

      if initialDist == None:
        initialDist = dist


      if dist <= threshold and orientationError <= pi/32:
        self.done = True
      else:
        targetAngle = (atan2(targetY - y, targetX - x))%(2*pi)
        print("targetAngle:", round(degrees(targetAngle), 2))
        s = self.getPlatformSpeed(initialDist, dist, speed, minSpeed)
        #print("speed", s)
        b = self.getSpeedFromAngle(targetAngle, s)

        if orientation != None:
          orientationError = (theta - orientation)/2*pi
          if abs(orientationError*speed) <= speed/4:
            cmd = orientationError*speed
          else:
            cmd = speed/4*orientationError/abs(orientationError)
          if cmd < 15: cmd = 15
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
    print('> Navigation: End of goTo')

  '''
  Public
  '''
  def relativeGoTo(self, **args):
    # args = targetDeltaX, targetDeltaY, speed=50, threshold=5, orientation=None
    #self.positionWatcher.pauseWatchPosition()
    x, y, theta = self.positionWatcher.computePosition()
    args['x'] = x + cos(theta)*args['y'] + sin(theta)*args['x']
    args['y'] = y + sin(theta)*args['y'] - cos(theta)*args['x']
    self.goTo(**args)

  '''
  Public
  '''
  def orientTo(self, **args):
    x, y, theta = self.positionWatcher.getPos()
    targetTheta = theta+args["theta"] if args["relative"] in args else args['theta']
    self.goTo(x=x, y=y, theta=targetTheta)

  '''
  Public
  '''
  def goToPath(self, path):
    for node in path:
      self.goTo(node)
      sleep(0.5)

    self.platform.stop()
    print('Path done')
    
  def stop(self):
    self.done = True
