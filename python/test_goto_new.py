import sys
from math import *
from src.Container import Container
from src.Game import Game
from src.PWMDriver import PWMDriver
from src.MotorizedPlatform import MotorizedPlatform
from src.Navigation import Navigation
from src.PositionWatcher import PositionWatcher
from src.Lidar import Lidar
from src.Switches import Switches
from src.WebSocketServer import WebSocketServer
from src.CommandsManager import CommandsManager
from src.ArduinoManager import ArduinoManager
from src.Scripts import Scripts
from src.DetectionProcess import DetectionProcess
#from src.Elevator import Elevator
from src.Claw import Claw
from time import sleep
from src.Logger import LoggerManager

container = Container()

logger = LoggerManager()
logger.setLevel('debug')
container.set('logger', logger)

if __name__ == '__main__':
  root = logger.get('Root')

  ws = WebSocketServer(container)
  container.set('websocket', ws)

  # arduinoManager = ArduinoManager(container)
  # arduinoManager.identify()
  # container.set('arduinoManager', arduinoManager)
  
  scripts = Scripts(container)
  container.set('scripts', scripts)

  game = Game(container)
  container.set('game', game)
  
  commandsManager = CommandsManager(container)
  container.set('commandsManager', commandsManager)

  positionWatcher = PositionWatcher(container)
  #positionWatcher.start()
  container.set('positionWatcher', positionWatcher)
  
  detectionProcess = DetectionProcess(container)
  container.set('detectionProcess', detectionProcess)

  # switches = Switches(container)
  # container.set('switches', switches)

  driver = PWMDriver()
  container.set('driver', driver)

  platform = MotorizedPlatform(container)
  container.set('platform', platform)

  navigation = Navigation(container)
  container.set('navigation', navigation)
  
  rightClaw = Claw(container, {'elevator': 7, 'claws': [6, 5, 4]})
  container.set('rightClaw', rightClaw)
  
  # elevator = Elevator(container)
  # container.set('elevator', elevator)
  commandsManager.init()

  def onPos(x, y, t):
    ws.sendData('mainPosition', [x, y, t])

  positionWatcher.setPositionChangedHandler(onPos)

  def app():
    #switches.start()
    ws.start()
    #lidar.start()
    platform.stop()
    positionWatcher.reset()
    positionWatcher.start()
    #lidar.start()
    #detection.whenDetected(90, 30)
    
    #detectionProcess.start()
    
    root.info('App ready')
    navigation.goTo(x=500, y=500, theta=pi)

  try:
    app()
  except KeyboardInterrupt:
    print('')
    root.error('KeyboardInterrupt: App will shutdown in a few moments')
    #switches.stop()
    scripts.stop()
    navigation.stop()
    positionWatcher.stop()
    platform.stop()
    #elevator.stop()
    ws.stop()
    platform.stop()
    sys.exit()

