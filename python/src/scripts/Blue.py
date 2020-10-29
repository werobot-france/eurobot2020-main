from math import *
from time import sleep
from ..API import API

class Blue(API):
  
  def run(self):
    self.elevator.lighthouse()
    
    ## DEPLOY LIGHTHOUSE
    # click with front
    self.navigation.goTo(x=-500, y=159, theta=pi, stopOn='front', speed=85)
    # click with left
    self.navigation.goTo(x=0, y=-500, theta=pi, stopOn='left', speed=60)
    # click with front
    self.navigation.goTo(x=-500, y=159, theta=pi, stopOn='front', speed=60)
    self.positionWatcher.setPos(125, 159, pi)
    
    self.elevator.goTo(239)
    sleep(0.5)
    self.elevator.goTo(500)
    sleep(0.5)
    ## END OF LIGHTHOUSE DEPLOYMENT
    
    # PRENDRE LES GOBELETS VERTS
    self.positionWatcher.setIgnoreSidesChanges(True)
    self.navigation.goTo(x=125, y=773, theta=pi, speed=60)
    self.positionWatcher.setIgnoreSidesChanges(False)
    self.navigation.goTo(x=-500, y=773, theta=pi, stopOn='front', speed=85)
    
    input('>> CONFIRM ??')
    # ROUTINE POUR PRENDRE
    self.elevator.open()
    self.elevator.goTo(100)
    input('>> continue?')
    self.elevator.close()
    sleep(1)
    self.elevator.goTo(780)
    
    # ALLER POUR TRIER en passant par le lighthouse
    self.positionWatcher.setIgnoreSidesChanges(True)
    self.navigation.goTo(x=0, y=-500, theta=pi, stopOn='left', speed=60)
    self.positionWatcher.setIgnoreSidesChanges(False)
    self.navigation.goTo(x=-500, y=159, theta=pi, stopOn='front', speed=85)
    self.navigation.goTo(x=0, y=-500, theta=pi, stopOn='left', speed=60)
    self.positionWatcher.setPos(125, 159, pi)
    
    self.positionWatcher.setIgnoreBackChanges(True)
    self.navigation.goTo(x=700, y=159, theta=pi, speed=60)
    self.positionWatcher.setIgnoreBackChanges(False)
    
    # Lâcher les gobelets
    self.elevator.goTo(150)
    self.elevator.open()
    sleep(1)
    self.elevator.goTo(600)
    
    # se réorienter pour aller vers les manches à air
    self.navigation.goTo(x=800, y=250, theta=pi, speed=60)
    self.navigation.orientTo(theta=pi/2, speed=50)
    
    self.navigation.goTo(x=1750, y=250, theta=pi/2, speed=60)

    self.navigation.goTo(x=2500, y=250, theta=pi/2, stopOn='right', speed=60)
        
    self.positionWatcher.setPos(1875, 250, pi/2)
    
    # on se recale par rapport au mur de derrière
    self.navigation.goTo(x=1875, y=-600, theta=pi/2, stopOnSlip=True, speed=70)
    
    self.positionWatcher.setPos(1875, 159, pi/2)
    
    self.navigation.goTo(x=2600, y=250, theta=pi/2, stopOn='right', speed=80)
    
    self.positionWatcher.setPos(1875, 159, pi/2)
    
    self.schlager.open()
    
    self.positionWatcher.setIgnoreSidesChanges(False)
    self.positionWatcher.setIgnoreBackChanges(True)
    self.navigation.goTo(x=1875, y=500, theta=pi/2, speed=85)
    
    self.navigation.goTo(x=2600, y=500, theta=pi/2, stopOn='right', speed=80)
    self.positionWatcher.setPos(1875, 450, pi/2)
    
    self.navigation.goTo(x=1875, y=750, theta=pi/2, speed=85)
    self.positionWatcher.setIgnoreBackChanges(False)
    # fin du schlagague
    
    #  RETOUR AU SUD ??
    self.navigation.goTo(x=1700, y=750, theta=pi/2, speed=85)
    self.navigation.orientTo(theta=3*pi/2, speed=50)
    
    # on se recalle en y = 0
    self.positionWatcher.setIgnoreBackChanges(True)
    self.navigation.goTo(x=1700, y=-500, theta=3*pi/2, stopOn='front', speed=80)
    self.positionWatcher.setIgnoreBackChanges(False)
    self.positionWatcher.setPos(1700, 159, 3*pi/2)
    self.navigation.goTo(x=2600, y=-500, theta=3*pi/2, stopOn='left', speed=80)
    self.positionWatcher.setPos(1875, 159, 3*pi/2)
    
    # INSERT GOBLEET??? PRIVE
    
    self.positionWatcher.setIgnoreSidesChanges(True)
    # retour approximatif dans la zone sud
    self.navigation.goTo(x=700, y=159, theta=3*pi/2, speed=80)
    self.positionWatcher.setIgnoreSidesChanges(False)
    
