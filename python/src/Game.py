from time import sleep
from gpiozero import Button
from .API import API
from .ThreadHelper import Thread

# WARN: being a child of the API class is a privilege reserved to the script classes
class Game(API):
  
  def __init__(self, container):
    self.container = container
    self.server = container.get('websocket')
    self.logger = self.container.get('logger').get('Game')
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
    self.startSwitch = Button(21)
    self.logger.info('Robot armed!', self.team, self.buosDisposition, self.script)
    # wait for the switch to activate
    #sleep(3)
    self.startSwitch.when_released = self.onStart
    self.started = False
    while not self.started:
      sleep(0.5)
  
  def onStart(self):
    self.started = True
    self.logger.info('Started')
    
    # game start intialization routine
    self.leftClaw.goTop()
    self.leftClaw.open()
    self.rightClaw.goTop()
    self.rightClaw.open()
    
    #self.flag.start()
    
    print(self.server.sendData('gameStart', []))
    # start the script
    self.scripts.run(self.script)
    
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
    # display score
    print(self.server.sendData('gameEnd', [ self.score ]))
  
  # def onStart(self):
    
  #   self.onEnd()
  
  # def onEnd(self):
    

  def abort(self):
    self.logger.info('Aborted!')

