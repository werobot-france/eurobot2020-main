from math import *
from ..API import API
from time import sleep

class EmergencyH(API):
  
  def run(self):
    self.rightClaw.goTop()
    self.rightClaw.open()
    self.leftClaw.goTop()
    self.leftClaw.open()
    input('>Confirm?')
    
    ## ACTIVATION DU PHARE
    self.navigation.goTo(x=140, y=204, speed=60)
    self.navigation.orientTo(theta=pi/2, speed=50)
    #self.navigation.goTo(x=self.positionWatcher.getX(), y=204, speed=40, backward=True)
    
    # Ouverture spéciale phare
    self.leftClaw.setAll([80, 80, 112])
    
    input('>Confirm?')
    self.leftClaw.directGoTo(110)
    sleep(0.6)
    self.leftClaw.goTop()
    self.leftClaw.open()
    
    input('>Confirm?')
    self.navigation.goTo(x=114, y=945, speed=60)
    self.navigation.orientTo(theta=pi/2, speed=50)
    input('>Confirm?')
    self.leftClaw.goMiddle()
    sleep(1)
    input('>Confirm?')
    self.leftClaw.close()
    self.leftClaw.goTop()
    
    

