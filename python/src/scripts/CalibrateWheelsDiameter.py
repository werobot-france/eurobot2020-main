from math import *
from ..API import API

class CalibrateWheelsDiameter(API):
  
  def run(self):
    # on considère l'avant du robot comme l'arrière ici
    # condition initiale: le robot a son avant dirigé vers la bordure
    distance = 1000
    
    leftGain = oldLeftGain = self.positionWatcher.leftGain
    rightGain = oldRightGain = self.positionWatcher.rightGain
    
    self.positionWatcher.setPos(0, 0, -pi/2)
    
    # STEP 1: on fait avancer le robot jusqu'a ce qu'il touche la bordure
    self.navigation.goTo(x=0, y=-200, speed=35, stopOnSlip=True)
    
    # STEP 2: reset heading
    self.positionWatcher.setPos(0, 0, -pi/2)
    
    # START OF THE LOOP
    for i in range(0, 6):
      # STEP 3: Move forward (so backward) as much as possible (on fait 1 metre)
      oldX = self.positionWatcher.x
      oldY = self.positionWatcher.y
      self.navigation.goTo(x=oldX, y=oldY+distance, speed=40, backward=True)
      
      # STEP 4: Turn 180° in one direction.
      self.navigation.orientTo(theta=pi/2, speed=35, clockwise=True)
      
      # STEP 5: Move forward (so backward) in the same distance.
      self.navigation.goTo(x=oldX, y=oldY, speed=40, backward=True)
      
      # STEP 6: Turn -180° (in the other direction).
      self.navigation.orientTo(theta=-pi/2, speed=35, clockwise=False)
      
      # STEP 7: Move back (so forward) until the robot hits the reference edge again.
      self.navigation.goTo(x=oldX, y=oldY-600, speed=50, stopOnSlip=True)
      
      input('Confirm computation of the new gains?')
      # CALIBRATE WHEEL TRACKS ROUTINE
      # if we are in a calibration routine we can compute the left and right gain:
      # total_distance is the average between the left wheel and right wheel
      leftTicks, rightTicks = self.positionWatcher.leftTicks, self.positionWatcher.rightTicks
      
      leftDistance = leftTicks * leftGain/self.positionWatcher.pulsePerMm
      rightDistance = rightTicks * rightGain/self.positionWatcher.pulsePerMm
      
      totalDistance = (leftDistance + rightDistance)/2
      deltaAngle = (rightDistance - leftDistance)/2
      
      oldLeftGain = leftGain
      oldRightGain = rightGain
      
      factor = deltaAngle / totalDistance
      leftGain = (1 + factor) * oldLeftGain
      rightGain = (1 - factor) * oldRightGain
      
      print('suggested new gains', leftGain, rightGain)
      
      input('Confirm new calibration loop?')