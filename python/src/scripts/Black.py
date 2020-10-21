from math import *
from ..API import API
from time import sleep

class Black(API):
  
  def run(self):
    self.rightClaw.goTop()
    self.rightClaw.open()
    input('>Confirm?')
    
    self.navigation.goTo(x=150, y=925)
    sleep(0.6)
    self.navigation.orientTo(theta=radians(270))
    
    input('>Confirm?')

    self.rightClaw.goMiddle()
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
    self.rightClaw.goBottom()
    sleep(0.7)
    self.rightClaw.open()
    sleep(1)
    self.rightClaw.goTop()

