from math import *
from ..API import API
from time import sleep

class Blue3(API):
  
  def run(self):
    ## ACTIVATION DU PHARE
    self.navigation.goTo(x=143, y=204, speed=90)
    self.navigation.orientTo(theta=pi/2, speed=50)
    #self.navigation.goTo(x=self.positionWatcher.getX(), y=204, speed=40, backward=True)
    
    # Ouverture spéciale phare
    self.leftClaw.setAll([80, 80, 112])
    
    #input('>Confirm?')
    self.leftClaw.directGoTo(110)
    sleep(0.6)
    self.leftClaw.goTop()
    self.leftClaw.open()
    sleep(0.9)
    self.navigation.orientTo(theta=pi/2, speed=50)
    
    self.navigation.goTo(x=110, y=780, speed=60)
    self.navigation.orientTo(theta=pi/2, speed=50)
    self.navigation.orientTo(theta=pi/2, speed=30)
    
    input('>Confirm?')
    self.leftClaw.goMiddle()
    sleep(1)
    self.leftClaw.close()
    sleep(0.5)
    self.leftClaw.goTop()
    sleep(0.5)
    input('>Confirm?')
    self.navigation.orientTo(theta=3*pi/2, speed=60, clockwise=False)
    
    self.navigation.goTo(x=self.positionWatcher.getX(), y=945, speed=60, backward=True)
    
    # self.navigation.goTo(
    #   x=self.positionWatcher.defaultX,
    #   y=self.positionWatcher.defaultY, speed=80, backward=True)
    # self.navigation.orientTo(theta=pi, speed=50)
    

