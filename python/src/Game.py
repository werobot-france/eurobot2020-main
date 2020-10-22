from time import sleep
from gpiozero import Button

class Game:
  
  def __init__(self, container):
    self.container = container
    self.server = container.get('websocket')
    self.logger = self.container.get('logger').get('Game')
    self.score = 42
    
    # blue or yellow
    self.team = 'blue'
    
    # possible values 1, 2 or 3
    self.buosDisposition = 1
    
    self.startSwitch = Button(21, None, True)

  def arm(self, config):
    self.team = config['team']
    self.buosDisposition = config['buosDisposition']
    
    self.logger.info('Robot armed!', config)
    # wait for the switch to activate
    #sleep(3)
    self.startSwitch.wait_for_press()
    self.onStart()
  
  def onStart(self):
    self.logger.info('Started')
    print(self.server.sendData('gameStart', []))
    # start a 100s timer
    sleep(100)
    self.onEnd()
  
  def onEnd(self):
    self.logger.info('End!')
    print(self.server.sendData('gameEnd', [ self.score ]))

  def abort(self):
    self.logger.info('Aborted!')

