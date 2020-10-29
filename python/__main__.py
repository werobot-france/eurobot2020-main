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
from src.Elevator import Elevator
from src.Claw import Claw
from time import sleep
from src.Logger import LoggerManager
from src.Flag import Flag
from src.Toner import Toner
from src.Schlager import Schlager

container = Container()

logger = LoggerManager()
logger.setLevel('debug')
container.set('logger', logger)

if __name__ == '__main__':
  root = logger.get('Root')
  root.info('Starting app...')

  ws = WebSocketServer(container)
  container.set('websocket', ws)

  arduinoManager = ArduinoManager(container)
  arduinoManager.identify()
  container.set('arduinoManager', arduinoManager)
  
  scripts = Scripts(container)
  container.set('scripts', scripts)

  schlager = Schlager(container)
  container.set('schlager', schlager)
  
  commandsManager = CommandsManager(container)
  container.set('commandsManager', commandsManager)
  
  toner = Toner(container)
  container.set('toner', toner)
  toner.play(500)

  positionWatcher = PositionWatcher(container)
  #positionWatcher.start()
  positionWatcher.setPos(2000-165, 175, pi)
  container.set('positionWatcher', positionWatcher)
  
  detectionProcess = DetectionProcess(container)
  container.set('detectionProcess', detectionProcess)

  switches = Switches(container)
  container.set('switches', switches)
  
  game = Game(container)
  container.set('game', game)

  driver = PWMDriver()
  container.set('driver', driver)

  platform = MotorizedPlatform(container)
  container.set('platform', platform)

  navigation = Navigation(container)
  container.set('navigation', navigation)
  
  flag = Flag(container)
  container.set('flag', flag)
  
  elevator = Elevator(container)
  container.set('elevator', elevator)
  commandsManager.init()

  def onPos(x, y, t):
    ws.sendData('mainPosition', [x, y, t])

  positionWatcher.setPositionChangedHandler(onPos)

  def app():
    switches.start()
    ws.start()
    platform.stop()
    sleep(0.4)
    positionWatcher.reset()
    positionWatcher.start()
    
    # REMOVE BEFORE FLIGHT
    
    #detectionProcess.start([67.5, 112.5])
    #detectionProcess.start()
    
    root.info('App ready')
    # sleep(1)
    # navigation.goTo({'x':600, 'y':600, 'orientation':pi })
    # input('You confirm?')
    # navigation.goTo({ 'x': 979, 'y': 1500, 'orientation': pi, 'speed': 40 })
    # sleep(5)
    # detectionProcess.blindRange = [40, 40]
    while True:
      sleep(100)

  try:
    app()
  except KeyboardInterrupt:
    print('')
    root.error('KeyboardInterrupt: App will shutdown in a few moments')
    switches.stop()
    scripts.stop()
    navigation.stop()
    positionWatcher.stop()
    platform.stop()
    elevator.stop()
    ws.stop()
    platform.stop()
    sys.exit()

