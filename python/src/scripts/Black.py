from math import *
from ..API import API
from time import sleep

class Black(API):
  
  def run(self):
    self.rightClaw.directGoTo(80)
    input('>Confirm?')
    self.rightClaw.open()
    self.rightClaw.goTop()
    input('>Confirm?')
    
    self.navigation.goTo(x=180, y=1000)
    sleep(0.6)
    self.navigation.orientTo(theta=radians(270))
    
    input('>Confirm?')

    self.rightClaw.directGoTo(155)
    input('>Confirm?')
    self.rightClaw.close()
    sleep(1)
    self.rightClaw.goTop()
    sleep(3)
    input('>Confirm?')
    
    self.navigation.goTo(x=400, y=1300, backward=1, threshold=100)
    
    self.navigation.goTo(x=800, y=200)

    self.navigation.orientTo(theta=radians(90))
    
    input('>Confirm?')
    self.rightClaw.directGoTo(180)
    sleep(0.5)
    self.rightClaw.open()
    sleep(1)
    self.rightClaw.goTop()

