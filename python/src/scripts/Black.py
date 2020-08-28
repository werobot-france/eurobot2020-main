from math import *
from ..API import API
from time import sleep

class Black(API):
  
  def run(self):
    self.rightClaw.open()
    self.rightClaw.directGoTo(0)
    
    self.navigation.goTo(x=300, y=1300, speed=85)
    self.navigation.orientTo(theta=radians(200))
    self.navigation.goTo(x=165, y=945, speed=70)
    
    input('>Confirm?')

    self.navigation.orientTo(theta=radians(270))
    
    input('>Confirm?')

    self.rightClaw.directGoTo(180)
    sleep(1)
    self.rightClaw.close()
    sleep(0.7)
    self.rightClaw.directGoTo(0)
    sleep(1)

    self.navigation.goTo(x=134, y=1200, speed=25, backward=True)
    sleep(0.5)
    self.navigation.goTo(x=675, y=200, speed=25)
    sleep(0.5)
    self.navigation.orientTo(theta=radians(270), speed=75)
    
    self.rightClaw.directGoTo(180)
    sleep(0.5)
    self.rightClaw.open()
    
    
