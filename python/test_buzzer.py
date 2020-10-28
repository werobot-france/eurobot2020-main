import sys
from math import *
from src.Container import Container
from src.Buzzer import Buzzer
from time import sleep
from src.PowerMonitor import PowerMonitor

from src.Logger import LoggerManager

container = Container()

logger = LoggerManager()
logger.setLevel('debug')
container.set('logger', logger)

buzzer = Buzzer(container)
container.set('buzzer', buzzer)

powerMonitor = PowerMonitor()
powerMonitor.start()