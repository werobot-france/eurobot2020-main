from math import *
from ..API import API
from time import sleep

class CalibrateAxialDistance(API):
  
  def run(self):
    # on considère l'avant du robot comme l'arrière ici
    # condition initiale: le robot a son avant dirigé vers la bordure
    baseAngle = -pi/2
    
    self.positionWatcher.setPos(0, 0, baseAngle)
    
    # STEP 1: Go back until it hits the reference edge
    self.navigation.goTo(x=0, y=-200, speed=40, stopOnSlip=True)
    
    # STEP 2: reset heading
    self.positionWatcher.setPos(0, 0, baseAngle)
    
    # STEP 3: Move away from the reference edge enough to be able to rotate.
    self.navigation.goTo(x=0, y=100, speed=35, backward=True)
    
    sleep(1)
    
    turnCount = 3
    
    # STEP 4: TURN 2Pi clockwise
    # for i in range(0, turnCount):
    #   self.navigation.orientTo(theta=baseAngle, speed=25, fullRotation=True, clockwise=True)
    #   sleep(1)

    # STEP 4: TURN 2Pi clockwise
    for i in range(0, turnCount):
      self.navigation.orientTo(theta=baseAngle, speed=25, fullRotation=True, clockwise=False)
      sleep(1)
    
    # STEP 5: Go back until it hits the reference edge
    self.navigation.goTo(x=0, y=-800, speed=55, stopOnSlip=True)
    
    input('Confirm good wall hit ? Go for computation ?')
    
    oldAxialDistance = self.positionWatcher.axialDistance
    theta = self.positionWatcher.getTheta()
    if theta > pi: theta -= 2*pi
    
    deltaAngle = self.deltaAngle(0, theta - baseAngle)
    newAxialDistance = oldAxialDistance * (1 + (deltaAngle / (2*pi*(turnCount))))
    
    print('delta:', degrees(deltaAngle))
    print('old:', oldAxialDistance)
    print('new:', newAxialDistance)
  
  def deltaAngle(self, start, end):
    res = fmod(end - start + pi, 2 * pi) - pi;
    res_conj = 2 * pi - res;

    if res < fabs(res_conj):
      return res
    else:
      return res_conj