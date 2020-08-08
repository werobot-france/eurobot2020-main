import sys
from math import *
from src.Container import Container
from src.PWMDriver import PWMDriver
from src.MotorizedPlatform import MotorizedPlatform
from src.Navigation import Navigation
from src.PositionWatcher import PositionWatcher
from time import sleep

container = Container()

positionWatcher = PositionWatcher()
positionWatcher.start()
container.set('positionWatcher', positionWatcher)

driver = PWMDriver()
container.set('PWMDriver', driver)

platform = MotorizedPlatform(container)
container.set('platform', platform)

nav = Navigation(container)
container.set('navigation', nav)

nav = Navigation(container)

def app():  
  platform.stop()
  sleep(1.5)
  
  input('Start ?')

  positionWatcher.start()
  
  nav.orientTo(0)

try:
  app()
except KeyboardInterrupt:
  print("\n KeyboardInterrupt")
  positionWatcher.stop()
  platform.stop()
  sys.exit()

