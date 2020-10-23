import sys
from math import *
from src.Container import Container
from src.Lidar import Lidar
from src.WebSocketClient import WebSocketClient
from src.PWMDriver import PWMDriver
from src.Detection import Detection

container = Container()

logger = LoggerManager()
logger.setLevel('debug')
container.set('logger', logger)

driver = PWMDriver()
container.set('driver', driver)

client = WebSocketClient('ws://localhost:8082', 'detection')
client.start()
container.set('client', client)

detection = Detection(container)
container.set('detection', detection)

lidar = Lidar(container)
container.set('lidar', lidar)

lidar.start()