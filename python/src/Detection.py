from math import *

class Detection:
  
  def __init__(self, container):
    self.positionWatcher = container.get('positionWatcher')
    self.navigation = container.get('navigation')
    self.mustStop = False
    self.mustStopTmp = False
  
  # this function is called when ever something is detected by the lidar
  def whenDetected(self, angle, dist):
    # when the angle passed is set to None, we consider this scanning plane as the reference (zero)
    if angle == None and dist == -1:
      # so this piece of code is called every roundtrip
      self.mustStop = self.mustStopTmp
      self.mustStopTmp = False
      # BILAN
      if self.mustStop:
        self.navigation.pause()
        print('STOP! STOP!')
      else:
        # TODO: add a timeout to prevent from too frequent stop/restart of the navigation
        self.navigation.resume()
        print('NOTHING')
      return
    
    angle *= 2 # the angle of the servo has a delta of 180 degrees because of the gear ratio
    dist *= 10 # convert the distanced sensored in millimiters
    
    angle = radians(angle)
    
    # Basic computation about this plane
    incli = radians(-10) # this is the angle at which the lidar is oriented
    H = 450 # the height at which the lidar sensor is (from the floor)
    horizontal = cos(incli) * dist # the horizontal position of the target in the scanned plane, relative to the lidar
    
    #print('hor', d)
    
    vertical = H + (sin(incli) * dist) # the vertical position of the target in the scanned plane, relative to the lidar
    
    #print('z', A)
    
    isRobot = vertical > 70 # A target is considered as a robot if his height is superior to a defined threshold
    if not isRobot:
      #print('Not a robot')
      return
    
    isClose = horizontal < 400 # A target is considered dangerous if it is in a radius inferiur to a defined threshold from the lidar
    
    if not isClose:
      #print('Not close enought')
      return
    
    # More advance computation to check if the target detected is in the table
    absoluteAngle = (self.positionWatcher.getTheta() + angle) % (2*pi) # (absolue)
    #print('absoluteAngle', absoluteAngle)
    margin = 300
    ma = self.getDistanceMax(absoluteAngle)
    isInTable = horizontal < (ma - margin)
    if not isInTable:
      print('Not in table')
      return
    print(horizontal, ma)
    
    newStop = isRobot and isClose and isInTable
    if newStop:
      self.mustStopTmp = True
      self.mustStop = True
      self.navigation.pause()
      print(degrees(angle), degrees(absoluteAngle), 'OWOWOWOWOWOOWO CALM DOWN')

  # Walls :
  #               0
  #        _______________
  #        |             |
  #        |             |
  #        |             |
  #      3 |             | 1
  #        |             |
  #        |             |
  #        _______________
  #               2
  Walls = [
    3000, #position y du mur 0
    2000, #position x du mur 1
    0, # position y du mur 2
    0  # position x du mur 3
  ]
  
  # retourne le mur détécté selon les trucs dessus
  def detectedWall(self, x, y, angle):
    # rapporter entre -pi et pi
    if angle > pi:
      angle -= 2*pi

    tr = atan2(self.Walls[0] - y, self.Walls[1] - x)
    tl = atan2(self.Walls[0] - y, -x)
    bl = atan2(-y, -x)
    br = atan2(-y, self.Walls[1] - x)
    
    if angle <= tl and angle >= tr:
      return 0
    if angle <= tr and angle >= br:
      return 1
    if angle >= bl and angle <= br:
      return 2
    if angle >= tl or angle <= bl:
      return 3

    return -1

  
  def detectWall(self, angle):
    # r = self.detectedWAll(angle)
    # return r
    return self.detectedWall(self.positionWatcher.getX(), self.positionWatcher.getY(), angle)

  # distance jusqu'à laquelle il peut y avoir un robot, qui correspond à la 
  # distance entre le Laser et le bord de la table selon la direction du détécteur
  def getDistanceMax(self, angle):
    wall0or2 = False
    if (self.detectWall(angle) == 1 or self.detectWall(angle) == 3) :
      coordoneeRobotAdequoite = self.positionWatcher.getX()
    else:
      wall0or2 = True
      coordoneeRobotAdequoite = self.positionWatcher.getY()

    a = abs(self.Walls[self.detectWall(angle)] - coordoneeRobotAdequoite)
    #print(a)
    
    if wall0or2:
      o = tan(abs(angle-pi/2))*a
    else:
      o = tan(abs(pi-angle))*a
    
    #print(o)

    return sqrt(a**2 + o**2)