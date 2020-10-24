from math import *
from ..API import API
from time import sleep

class Blue3(API):
  
  def run(self):
    # routine d'initialization
    print('hahah')
    self.leftClaw.goTop()
    self.leftClaw.open()
    self.rightClaw.goTop()
    self.rightClaw.open()
    
    ## 1 - ACTIVATION DU PHARE
    self.navigation.goTo(x=145, y=204, speed=90)
    self.navigation.orientTo(theta=pi/2, speed=50)
    # Ouverture spéciale phare
    self.leftClaw.setAll([73, 70, 125])
    #input('>Confirm?')
    self.leftClaw.directGoTo(85)
    sleep(0.6)
    self.leftClaw.goTop()
    self.leftClaw.open()
    sleep(0.9)
    self.navigation.orientTo(theta=pi/2, speed=50)
    ## FIN DE L'ACTIVATION DU PHARE
  
    input('>Confirm?')
    ## 2 - ECEUIL COMMUN VERT
    self.navigation.goTo(x=145, y=775, speed=60, threshold=7)
    self.navigation.orientTo(theta=pi/2, speed=50)
    self.navigation.orientTo(theta=pi/2, speed=30)
    
    # routine d'apprension
    input('>Confirm?')
    self.leftClaw.goMiddle()
    sleep(1.1)
    self.leftClaw.close()
    sleep(1.1)
    self.leftClaw.goTop()
    sleep(1.5)
    input('>Confirm?')
    
    ## 3 - ECEUIL COMMUN ROUGE
    self.navigation.orientTo(theta=3*pi/2, speed=30, clockwise=False)
    self.navigation.orientTo(theta=3*pi/2, speed=40)
    self.navigation.goTo(x=self.positionWatcher.getX()-14, y=946, speed=60, backward=True)
    self.navigation.orientTo(theta=3*pi/2, speed=50)

    # routine d'apprension
    input('>Confirm?')
    self.rightClaw.goMiddle()
    sleep(1.5)
    self.rightClaw.close()
    sleep(1.1)
    self.rightClaw.goTop()
    sleep(1)
    input('>Confirm?')
    
    ## 4 - ALLER AU PORT VERT
    self.navigation.goTo(x=290, y=150, speed=60)
    self.navigation.orientTo(theta=3*pi/2, speed=50)
    
    # routine de déposage gobelets verts
    self.leftClaw.goBottom()
    sleep(1)
    self.leftClaw.open()
    sleep(0.2)
    self.leftClaw.goTop()
    sleep(1)
    
    ## 5 - ALLER  AU PORT ROUGE
    self.navigation.goTo(x=300, y=400, speed=75, backward=True)
    self.navigation.goTo(x=900, y=600, speed=75, backward=True)
    self.navigation.orientTo(theta=pi/2, speed=50, threshold=pi/6)
    self.navigation.goTo(x=890, y=150, speed=70, backward=True)
    
    self.navigation.orientTo(theta=pi/2, speed=50)
    
    # routine de déposage gobelets verts
    self.leftClaw.goBottom()
    sleep(1)
    self.leftClaw.open()
    sleep(0.2)
    self.leftClaw.goTop()
    sleep(1)
    
    # routine de déposage gobelets verts
    self.leftClaw.goBottom()
    sleep(1)
    self.leftClaw.open()
    sleep(0.2)
    self.leftClaw.goTop()
    
    
    # self.navigation.goTo(
    #   x=self.positionWatcher.defaultX,
    #   y=self.positionWatcher.defaultY, speed=80, backward=True)
    # self.navigation.orientTo(theta=pi, speed=50)
    

