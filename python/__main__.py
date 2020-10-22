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
  
  leftClaw = Claw(container, {
    'id': 'left',
    'clawsProfile': 'china',
    'elevatorProfile': 'lidar',
    'elevatorSlot': 12,
    'clawsSlot': [15, 13, 14], # front, mid, back
    'elevatorPos': {
      'top': 32,
      'middle': 165,
      'bottom': 180
    },
    'clawsPos': {
      'open': [80, 134, 112], # 85, 120, 100
      'sleep': [143, 66, 48],
      'close': [163, 46, 28] # [170, 52, 30]
    }
  })
  rightClaw = Claw(container, {
    'id': 'right',
    'clawsProfile': 'rev',
    'elevatorProfile': 'rev',
    'elevatorSlot': 11,
    'clawsSlot': [10, 9, 8],
    'elevatorPos': {
      'top': 0,
      'middle': 130,
      'bottom': 165
    },
    'clawsPos': {
      'open': [66, 159, 145],
      'sleep': [145, 82, 82],
      'close': [165, 62, 62]
    }
  })
  container.set('leftClaw', leftClaw)
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
    platform.stop()
    sleep(0.4)
    positionWatcher.reset()
    positionWatcher.start()
    #lidar.start()
    #detection.whenDetected(90, 30)
    
    # REMOVE BEFORE FLIGHT
    #detectionProcess.start()
    
    root.info('App ready')
    # sleep(1)
    # navigation.goTo({'x':600, 'y':600, 'orientation':pi })
    # input('You confirm?')
    # navigation.goTo({ 'x': 979, 'y': 1500, 'orientation': pi, 'speed': 40 })
    while True:
      sleep(100)

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

