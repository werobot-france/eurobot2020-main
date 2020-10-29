from time import sleep
from gpiozero import Button
from .API import API
from .ThreadHelper import Thread
from math import *

# WARN: being a child of the API class is a privilege reserved to the script classes
class Game(API):
  
  def __init__(self, container):
    self.container = container
    self.server = container.get('websocket')
    self.switches = self.container.get('switches')
    self.logger = self.container.get('logger').get('Game')
    self.toner = self.container.get('toner')
    self.score = 42
    
    # blue or yellow
    self.team = 'blue'
    
    # possible values 1, 2 or 3
    self.buosDisposition = 1
    
    self.script = None
    self.mainThread = None
    self.startSwitch = None
    self.started = False

  def arm(self, config = None, script = None):
    # load API
    super().__init__(self.container)
    if self.mainThread != None:
      self.mainThread.stop()
    
    if 'team' in config and 'buosDisp' in config:
      self.team = config['team']
      self.buosDisposition = config['buosDisp']
      script = self.team.title() + str(self.buosDisposition)
      # script name always as follow : Blue1, Yellow1, Yellow2
    if script != None and not self.scripts.exists(script):
      self.logger.error('Invalid script name supplied!', script)
      return
    self.script = script
    self.mainThread = Thread(target=self.run)
    self.mainThread.start()
  
  def run(self):
    # BOUCLE DE CONFIG
    # On attend pour un click
    configLoop = True
    wasEnabled = False
    count = 0
    while configLoop:
      sleep(0.2)
      state = self.switches.getState('emerg')
      if state:
        wasEnabled = True
        count += 1
      if not state and wasEnabled:
        count = 0
        wasEnabled = False
        # changement de team
        if self.team == 'blue':
          self.team = 'yellow'
          self.toner.play(880, 500)
          self.logger.info('NOW SET TO YELLOW TEAM')
        else:
          self.team = 'blue'
          self.toner.play(220, 500)
          self.logger.info('NOW SET TO BLUE TEAM')
      if count >= 6:
        # click long qui signifie que le robot est sur la table
        self.logger.info('On the table')
        configLoop = False
        for i in range(0, 6):
          self.toner.play(293, 200)
          sleep(0.3)

    # IL est sur la table, on initialize
    self.positionWatcher.reset()
    self.positionWatcher.setIgnoreSidesChanges(False)
    self.positionWatcher.setIgnoreBackChanges(False)
    
    self.flag.close()
    self.schlager.close()
    
    # TO CHANGE!!!
    self.detectionProcess.start([0, 360])
    
    self.elevator.open()
    # go to origin
    self.elevator.reset()
    self.elevator.lighthouse()
    self.elevator.goTo(500)
    #self.schlager.close()
    
    # 1 - on attend pour un click long de l'emerg
    # 2 - on attend pour un click
    # self.startSwitch = Button(21)
    # self.logger.info('Robot armed!', self.team, self.buosDisposition, self.script)
    # # wait for the switch to activate
    # #sleep(3)
    # self.startSwitch.when_released = self.onStart
    # self.started = False
    # wait = True
    # while wait:
    #   sleep(0.2)
    #   print(self.switches.getState('start'))
    self.switches.onGroup('start', self.onStart)
    print('callback set')
  
  def onStart(self):
    self.started = True
    self.logger.info('Started')
    
    # game start intialization routine
    self.flag.start()
    self.positionWatcher.setPos(979, 200, pi)
    self.switches.onGroup('start', None)
    
    print(self.server.sendData('gameStart', []))
    
    # en fonction de la team choisi on run un script différent
    if self.team == 'blue':
      # on run une série de script dans le dossier bleu
      self.scripts.run('NewBlue')
    if self.team == 'yellow':
      self.scripts.run('Yellow')
      # on run une série de script dans le dossier jaune
    
    # start a 100s timer
    sleep(100)
    
    # ───────────────────────────────────────────────────────────
    #                            STOP                            
    # ───────────────────────────────────────────────────────────
    self.logger.info('End!')
    # kill current scripts, stop navigation
    self.scripts.stop()
    self.navigation.stop()
    self.platform.stop()
    self.detectionProcess.stop()
    # display score
    print(self.server.sendData('gameEnd', [ self.score ]))

  def abort(self):
    self.logger.info('Aborted!')

