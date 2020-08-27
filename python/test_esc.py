
from src.PWMDriver import PWMDriver
from src.MotorizedPlatform import MotorizedPlatform
from src.Container import Container
from time import sleep
from src.Logger import LoggerManager
container = Container()

logger = LoggerManager()
logger.setLevel('debug')
container.set('logger', logger)

driver = PWMDriver()
container.set('driver', driver)

platform = MotorizedPlatform(container)
container.set('platform', platform)

platform.stop()
sleep(2)
platform.setSpeed([
  0,
  0
])

while True:
  sleep(1)