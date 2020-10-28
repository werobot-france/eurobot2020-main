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
  leftDistance = positionWatcher.leftTicks*positionWatcher.leftGain/positionWatcher.pulsePerMm
  rightDistance = positionWatcher.rightTicks*positionWatcher.rightGain/positionWatcher.pulsePerMm
  
  print(leftDistance, rightDistance)

def app():
  positionWatcher.setPositionChangedHandler(onChange)
  positionWatcher.start()

try:
  app()
except KeyboardInterrupt:
  print("\n KeyboardInterrupt")
  positionWatcher.stop()
  sys.exit()

