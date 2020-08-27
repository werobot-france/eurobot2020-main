import sys
from math import *
from src.Container import Container
from src.PWMDriver import PWMDriver
from src.MotorizedPlatform import MotorizedPlatform
from src.Navigation import Navigation
from src.PositionWatcher import PositionWatcher
from time import sleep

from src.Logger import LoggerManager

container = Container()

logger = LoggerManager()
logger.setLevel('debug')
container.set('logger', logger)


positionWatcher = PositionWatcher(container)
positionWatcher.start()
container.set('positionWatcher', positionWatcher)

def onChange(x, y, theta):
  print(round(x, 2), round(y, 2), round(degrees(theta), 3))

def app():
  positionWatcher.setPositionChangedHandler(onChange)
  positionWatcher.start()

try:
  app()
except KeyboardInterrupt:
  print("\n KeyboardInterrupt")
  positionWatcher.stop()
  sys.exit()

