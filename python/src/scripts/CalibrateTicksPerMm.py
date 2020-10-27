from math import *
from ..API import API

class CalibrateTicksPerMm(API):
  
  def run(self):
    distance = 2000
    
    self.positionWatcher.setPos(0, 0, -pi/2)
    
    # STEP 1: on fait avancer le robot jusqu'a ce qu'il touche la bordure
    self.navigation.goTo(x=0, y=-200, speed=35, stopOnSlip=True)
    
    # STEP 2: on fait avancer deux mètres
    self.navigation.goTo(x=0, y=distance, speed=40, backward=True)
    
    # new_pulse_per_mm = old_pulse_per_mm * (real_distance / asked_distance);
    
    # new = (2400/200) * (2071 / 2000) = 12.426000000000002