from math import *
from time import sleep
from ..API import API

class NewBlue(API):
  
  def run(self):
    self.positionWatcher.setPos(655, 172, pi)
    # self.positionWatcher.setPos(1100, 159, 3*pi/2)

    self.elevator.lighthouse()
    #self.elevator.reset()
    #self.elevator.goTo(500)
    #self.navigation.goTo(x=655, y=-500, theta=pi, speed=40, stopOn='left')
    self.positionWatcher.setPos(655, 165, pi)
    
    self.positionWatcher.setIgnoreBackChanges(True)
    self.navigation.goTo(x=275, y=165, theta=pi, speed=79, threshold=20, stopOn='front')
    self.positionWatcher.setIgnoreBackChanges(False)
    
    # on recale le x
    self.navigation.goTo(x=-200, y=165, theta=pi, speed=40, stopOn='front')
    self.positionWatcher.setPos(125, 165, pi)
    # là le x est recalé
    self.navigation.goTo(x=125, y=-500, theta=pi, speed=40, stopOn='left')
    self.positionWatcher.setPos(125, 165, pi)
    
    # activer le phare
    self.elevator.goTo(239)
    sleep(0.5)
    self.elevator.goTo(500)
    sleep(0.5)
    # fin de l'activation du phare
    
    # récupérer les gobelets
    self.positionWatcher.setIgnoreSidesChanges(True)
    self.navigation.goTo(x=125, y=760, theta=pi, speed=40, threshold=4)
    self.positionWatcher.setIgnoreSidesChanges(False)
    
    # se recaler en x
    self.navigation.goTo(x=-500, y=760, theta=pi, speed=30, stopOn='front')
    self.positionWatcher.setPos(125, 760, pi)
    
    # # ROUTINE POUR PRENDRE
    #input('>> CONFIRM??')
    sleep(0.4)
    self.elevator.open()
    self.elevator.goTo(78)
    sleep(0.2)
    self.elevator.close()
    sleep(0.9)
    self.elevator.goTo(770)
    
    # on revient pour donner les gobelets
    
    # on recale le y
    self.navigation.goTo(x=125, y=-500, theta=pi, speed=50, stopOn='left')
    self.positionWatcher.setPos(125, 169, pi)
    
    # on recale le x
    self.navigation.goTo(x=-200, y=169, theta=pi, speed=40, stopOn='front')
    self.positionWatcher.setPos(125, 169, pi)
    
    self.positionWatcher.setIgnoreBackChanges(True)
    # on se rend à l'endroit pour drop
    self.navigation.goTo(x=619, y=169, theta=pi, speed=50, threshold=7)
    self.positionWatcher.setIgnoreBackChanges(False)
    
    # Lâcher les gobelets
    #input('>> CONFIRM??')
    sleep(0.5)
    self.elevator.goTo(150)
    self.elevator.open()
    sleep(1)
    self.elevator.goTo(600)
    sleep(1)
    self.elevator.close()
    
    # ON SE REORIENTE
    #self.navigation.goTo(x=1000, y=-169, theta=pi, speed=50)
    self.navigation.goTo(x=629, y=350, theta=pi, speed=50)
    self.navigation.goTo(x=820, y=350, theta=pi, speed=50)
    
    self.navigation.orientTo(theta=0.8*3*pi/2, speed=50)
    
    # recaler le y
    #self.navigation.goTo(x=1650, y=500, theta=pi, speed=50, stopOn='right')
    
    # on recale le x
    self.navigation.goTo(x=820, y=-500, theta=3*pi/2, speed=50, stopOn='front')
    
    # ok donc à ce niveau là, ça marche
    
    self.positionWatcher.setPos(820, 169, 3*pi/2)
    
    self.navigation.goTo(x=2500, y=169, theta=3*pi/2, speed=50, stopOn='left')
    
    self.positionWatcher.setPos(2000-125, 169, 3*pi/2)
    
    self.navigation.goTo(x=2000-125, y=-500, theta=3*pi/2, speed=40, stopOn='front')
    
    self.positionWatcher.setPos(2000-125, 169, 3*pi/2)
    
    # on se pose pour prendre les goblets
    self.positionWatcher.setIgnoreSidesChanges(True)
    self.navigation.goTo(x=2000-325, y=169, theta=3*pi/2, speed=40, threshold=7)
    self.positionWatcher.setIgnoreSidesChanges(False)
    
    self.navigation.goTo(x=2000-325, y=-500, theta=3*pi/2, speed=40, stopOn='front')
    
    self.positionWatcher.setPos(2000-(325-60), 169, 3*pi/2)
    
    #input('>> confirm??')
    sleep(0.5)
    # # ROUTINE POUR PRENDRE
    self.elevator.open()
    self.elevator.goTo(90)
    sleep(0.2)
    self.elevator.close()
    sleep(0.9)
    self.elevator.goTo(770)
    
    # donc on recule pas mal des eceuils
    self.navigation.goTo(x=2000-(325-60), y=300, theta=3*pi/2, speed=40)
    self.elevator.goTo(160)
    # on se décalle sur les x de 225 mm
    self.navigation.goTo(x=2000-500, y=300, theta=3*pi/2, speed=40)
    # on peut s'orienter. Mais on ne sait pas si c'est la bonne orientation
    # 5/6*pi
    self.navigation.orientTo(theta=pi, speed=50)
    
    # on se recale
    self.navigation.goTo(x=2000-500, y=-500, theta=pi, speed=50, stopOn='left')
    self.positionWatcher.setPos(2000-750, 169, pi)
    
    # on recule ou on avance pour pouvoir ensuite déposer le reste des gobelets
    self.navigation.goTo(x=2000-500, y=169, theta=pi, speed=40, threshold=7)
    
    # on se recale 
    self.navigation.goTo(x=2000-500, y=-500, theta=pi, speed=50, stopOn='left')
    self.positionWatcher.setPos(2000-700, 165, pi)
    
    # Lâcher les gobelets
    self.elevator.goTo(150)
    self.elevator.open()
    sleep(1)
    self.elevator.goTo(600)
    self.elevator.sleep()
    
    '''  
    ## DEBUT DU SCHLAGUAGE
    self.schlager.open()
    
    self.positionWatcher.setIgnoreBackChanges(False)
    self.navigation.goTo(x=2000-135, y=-300, theta=pi/2, speed=80)
    # 1er recalage intermédiaire
    self.navigation.goTo(x=2500, y=-300, theta=pi/2, speed=40, stopOn='right')
    self.positionWatcher.setPos(2000-125, -300, pi/2)
    
    self.navigation.goTo(x=2000-135, y=-500, theta=pi/2, speed=80)
    # 2ème recalage intermédiaire
    self.navigation.goTo(x=2500, y=-500, theta=pi/2, speed=40, stopOn='right')
    self.positionWatcher.setPos(2000-125, -500, pi/2)
    
    self.navigation.goTo(x=2000-135, y=-710, theta=pi/2, speed=80)
    # 3ème recalage intermédiaire
    self.navigation.goTo(x=2500, y=-710, theta=pi/2, speed=40, stopOn='right')
    self.positionWatcher.setPos(2000-125, -710, pi/2)
    
    self.navigation.goTo(x=2000-135, y=-750, theta=pi/2, speed=80)
    self.positionWatcher.setIgnoreBackChanges(False)
    ## END OF SCHLAGUAGE
    sleep(0.4)
    self.schlager.close()
    
    # on se recale
    self.navigation.goTo(x=2000-205, y=-750, theta=pi/2, speed=60)
    
    self.navigation.goTo(x=2000-205, y=300, theta=pi/2, speed=40, stopOn='front')
    self.positionWatcher.setPos(2000-205, -169, pi/2)
    
    self.navigation.goTo(x=2500, y=-169, speed=40, stopOn='right')
    self.positionWatcher.setPos(2000-125, -169, pi/2)
    
    self.navigation.goTo(x=2000-125, y=300, theta=pi/2, speed=40, stopOn='front')
    self.positionWatcher.setPos(2000-125, -169, pi/2)
    
    '''
    
    # ## DEPLOY LIGHTHOUSE
    # # click with right
    # self.positionWatcher.setIgnoreSidesChanges(True)
    # self.navigation.goTo(x=200, y=159, theta=3*pi/2, speed=89)
    # self.positionWatcher.setIgnoreSidesChanges(False)
    
    # self.navigation.goTo(x=-500, y=159, theta=3*pi/2, speed=40, stopOn='right')
    # self.positionWatcher.setPos(125, 159, 3*pi/2)
    # # click with front
    # self.navigation.goTo(x=125, y=-500, theta=3*pi/2, speed=40, stopOn='front')
    # self.positionWatcher.setPos(125, 159, 3*pi/2)
    
    # # click with right
    # self.navigation.goTo(x=-500, y=159, theta=3*pi/2, speed=40, stopOn='right')
    # self.positionWatcher.setPos(125, 159, 3*pi/2)
    
    # self.navigation.goTo(x=135, y=159, theta=3*pi/2, speed=40)
    
    # self.schlager.open()
    
    # self.positionWatcher.setIgnoreBackChanges(False)
    # self.navigation.goTo(x=135, y=300, theta=3*pi/2, speed=80)
    # # 1er recalage intermédiaire
    # self.navigation.goTo(x=-500, y=300, theta=3*pi/2, speed=40, stopOn='right')
    # self.positionWatcher.setPos(125, 300, 3*pi/2)
    
    # self.navigation.goTo(x=135, y=500, theta=3*pi/2, speed=80)
    # # 2ème recalage intermédiaire
    # self.navigation.goTo(x=-500, y=500, theta=3*pi/2, speed=40, stopOn='right')
    # self.positionWatcher.setPos(125, 500, 3*pi/2)
    
    # self.navigation.goTo(x=135, y=710, theta=3*pi/2, speed=80)
    # # 3ème recalage intermédiaire
    # self.navigation.goTo(x=-500, y=710, theta=3*pi/2, speed=40, stopOn='right')
    # self.positionWatcher.setPos(125, 710, 3*pi/2)
    
    # self.navigation.goTo(x=135, y=750, theta=3*pi/2, speed=80)
    # self.positionWatcher.setIgnoreBackChanges(False)
    # input('end')
    
    # self.elevator.goTo(239)
    # sleep(0.5)
    # self.elevator.goTo(500)
    # sleep(0.5)
    # ## END OF LIGHTHOUSE DEPLOYMENT
    
    # # PRENDRE LES GOBELETS VERTS
    # self.positionWatcher.setIgnoreXChanges(True)
    # self.navigation.goTo(x=125, y=773, theta=0, speed=60)
    # self.positionWatcher.setIgnoreXChanges(False)
    # self.navigation.goTo(x=-500, y=773, theta=0, stopOn='front', speed=85)
    
    # # ROUTINE POUR PRENDRE
    # self.elevator.open()
    # self.elevator.goTo(100)
    # input('>> continue?')
    # self.elevator.close()
    # sleep(1)
    # self.elevator.goTo(860)
    
    # # ALLER POUR TRIER en passant par le lighthouse
    # self.positionWatcher.setIgnoreXChanges(True)
    # self.navigation.goTo(x=0, y=-500, theta=pi, stopOn='left', speed=60)
    # self.positionWatcher.setIgnoreXChanges(False)
    # self.navigation.goTo(x=-500, y=159, theta=pi, stopOn='front', speed=85)
    # self.navigation.goTo(x=0, y=-500, theta=pi, stopOn='left', speed=60)
    # self.positionWatcher.setPos(125, 159, pi)
    
    # self.positionWatcher.setIgnoreYChanges(True)
    # self.navigation.goTo(x=700, y=159, theta=pi, speed=60)
    # self.positionWatcher.setIgnoreYChanges(False)
    
    # # Lâcher les gobelets
    # self.elevator.goTo(150)
    # self.elevator.open()
    # sleep(1)
    # self.elevator.goTo(600)
    
    # # se réorienter pour aller vers les manches à air
    # self.navigation.goTo(x=800, y=250, theta=pi, speed=60)
    # self.navigation.orientTo(theta=pi/2, speed=50)
    
    # self.navigation.goTo(x=1750, y=250, theta=pi/2, speed=60)

    # self.navigation.goTo(x=2500, y=250, theta=pi/2, stopOn='right', speed=60)
        
    # self.positionWatcher.setPos(1875, 250, pi/2)
    
    # # on se recale par rapport au mur de derrière
    # self.navigation.goTo(x=1875, y=-600, theta=pi/2, stopOnSlip=True, speed=70)
    
    # self.positionWatcher.setPos(1875, 159, pi/2)
    
    # self.navigation.goTo(x=2600, y=250, theta=pi/2, stopOn='right', speed=80)
    
    # self.positionWatcher.setPos(1875, 159, pi/2)
    
    # self.schlager.open()
    
    # self.positionWatcher.setIgnoreXChanges(False)
    # self.positionWatcher.setIgnoreYChanges(True)
    # self.navigation.goTo(x=1875, y=500, theta=pi/2, speed=85)
    
    # self.navigation.goTo(x=2600, y=500, theta=pi/2, stopOn='right', speed=80)
    # self.positionWatcher.setPos(1875, 450, pi/2)
    
    # self.navigation.goTo(x=1875, y=750, theta=pi/2, speed=85)
    # self.positionWatcher.setIgnoreYChanges(False)
    # # fin du schlagague
    
    # #  RETOUR AU SUD ??
    # self.navigation.goTo(x=1700, y=750, theta=pi/2, speed=85)
    # self.navigation.orientTo(theta=3*pi/2, speed=50)
    
    # # on se recalle en y = 0
    # self.positionWatcher.setIgnoreYChanges(True)
    # self.navigation.goTo(x=1700, y=-500, theta=3*pi/2, stopOn='front', speed=80)
    # self.positionWatcher.setIgnoreYChanges(False)
    # self.positionWatcher.setPos(1700, 159, 3*pi/2)
    # self.navigation.goTo(x=2600, y=-500, theta=3*pi/2, stopOn='left', speed=80)
    # self.positionWatcher.setPos(1875, 159, 3*pi/2)
    
    # # INSERT GOBLEET??? PRIVE
    
    # self.positionWatcher.setIgnoreXChanges(True)
    # # retour approximatif dans la zone sud
    # self.navigation.goTo(x=700, y=159, theta=3*pi/2, speed=80)
    # self.positionWatcher.setIgnoreXChanges(False)
