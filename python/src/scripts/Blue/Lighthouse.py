from math import *
from time import sleep
from ..API import API

class Lighthouse(API):
  
  def run(self):
    self.elevator.lighthouse()
    
    ## DEPLOY LIGHTHOUSE
    # click with front
    self.navigation.goTo(x=200, y=200, theta=pi, speed=85)
    self.navigation.goTo(x=-500, y=200, theta=pi, stopOn='front', speed=40)
    self.positionWatcher.setPos(125, 200, pi)
    # click with left
    self.navigation.goTo(x=125, y=-500, theta=pi, stopOn='left', speed=40)
    self.positionWatcher.setPos(125, 159, pi)
    # click with front
    self.navigation.goTo(x=-500, y=159, theta=pi, stopOn='front', speed=40)
    self.positionWatcher.setPos(125, 159, pi)
    
    self.detectionProcess.blindRange = [67.5, 112.5]
    self.elevator.goTo(239)
    sleep(0.5)
    self.elevator.goTo(500)
    ## END OF LIGHTHOUSE DEPLOYMENT
    