import sys
from math import *
from src.Container import Container
from src.PWMDriver import PWMDriver
from src.MotorizedPlatform import MotorizedPlatform
from src.Navigation import Navigation
from src.PositionWatcher import PositionWatcher
from src.Claw import Claw
from time import sleep

from src.Logger import LoggerManager

container = Container()

logger = LoggerManager()
logger.setLevel('debug')
container.set('logger', logger)

claw = Claw(container)

# def app():
  

# try:
#   app()
# except KeyboardInterrupt:
#   print("\n KeyboardInterrupt")
#   sys.exit()

