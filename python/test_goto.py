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

driver = PWMDriver()
container.set('PWMDriver', driver)

platform = MotorizedPlatform(container)
container.set('platform', platform)

nav = Navigation(container)
container.set('navigation', nav)

nav = Navigation(container)

positionWatcher.start()

def logPos():
  a = positionWatcher.getPos()
  print("\n\nx:", a[0], "y:", a[1], "theta:", degrees(a[2]))

def app():  
  platform.stop()
  sleep(0.5)
  
  input('Start ?')
  positionWatcher.reset()
  sleep(0.3)

  nav.goTo(x=-500, y=500)
  nav.orientTo(theta=pi/2)
  logPos()
  input("continue...")
  nav.goTo(x=-500, y=0)
  nav.orientTo(theta=pi)
  logPos()
  input("continue...")
  nav.goTo(x=0, y=-500)
  nav.orientTo(theta=3*pi/2)
  logPos()
  input("continue...")
  nav.goTo(x=0, y=0)
  nav.orientTo(theta=pi/2)
  logPos()
  input("continue...")

try:
  app()
except KeyboardInterrupt:
  print("\n KeyboardInterrupt")
  positionWatcher.stop()
  platform.stop()
  sys.exit()

