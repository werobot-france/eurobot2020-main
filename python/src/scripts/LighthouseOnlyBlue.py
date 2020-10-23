from math import *
from ..API import API
from time import sleep

class LighthouseOnlyBlue(API):
  
  def run(self):
    ## ACTIVATION DU PHARE
    self.navigation.goTo(x=143, y=204, speed=90)
    self.navigation.orientTo(theta=pi/2, speed=60)
    #self.navigation.goTo(x=self.positionWatcher.getX(), y=204, speed=40, backward=True)
    
    # Ouverture spéciale phare
    self.leftClaw.setAll([80, 80, 112])
    
    #input('>Confirm?')
    self.leftClaw.directGoTo(110)
    sleep(0.6)
    self.leftClaw.goTop()
    self.leftClaw.open()
    
    #input('>Confirm?')
    self.navigation.orientTo(theta=pi, speed=70)
    self.navigation.goTo(
      x=self.positionWatcher.defaultX,
      y=self.positionWatcher.defaultY, speed=80, backward=True)
    self.navigation.orientTo(theta=pi, speed=50)
    

