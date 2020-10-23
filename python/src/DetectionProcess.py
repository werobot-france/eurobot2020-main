from multiprocessing import Process

from .PWMDriver import PWMDriver
from .Container import Container
from .Detection import Detection
from .Lidar import Lidar
from .WebSocketClient import WebSocketClient
from time import sleep

class DetectionProcess:
  def __init__(self, container):
    self.container = container
    self.logger = container.get('logger').get('DetectionProcess')
    
  def start(self):
    self.process = Process(target=self.run)
    self.process.start()
    self.process.join()
  
  def run(self):
    sleep(1)
    container = Container()
    container.set('logger', self.container.get('logger'))

    container.set('driver', self.container.get('driver'))
    
    client = WebSocketClient('ws://localhost:8082', 'detection')
    client.start()
    container.set('client', client)

    detection = Detection(container)
    container.set('detection', detection)

    lidar = Lidar(container)
    container.set('lidar', lidar)
    
    lidar.start()
    

