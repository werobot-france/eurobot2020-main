from multiprocessing import Process

from .PWMDriver import PWMDriver
from .Container import Container
from .Detection import Detection
from .Lidar import Lidar
from .WebSocketClient import WebSocketClient
from time import sleep

class DetectionProcess:
  enabled = False
  
  def __init__(self, container):
    self.container = container
    self.logger = container.get('logger').get('DetectionProcess')
    
  def start(self, blindRange):
    self.enabled = True
    self.blindRange = blindRange
    self.process = Process(target=self.run)
    self.process.start()
    
  def stop(self):
    self.process.terminate()
    self.process.join()
    self.enabled = False
    
  def toggle(self):
    if self.enabled:
      self.stop()
    else:
      self.start()
  
  def run(self):
    container = Container()
    container.set('logger', self.container.get('logger'))

    container.set('driver', self.container.get('driver'))
    
    client = WebSocketClient('ws://localhost:8082', 'detection')
    client.start()
    container.set('client', client)

    detection = Detection(container)
    detection.blindRange = self.blindRange
    container.set('detection', detection)

    lidar = Lidar(container)
    container.set('lidar', lidar)
    
    lidar.start()
    
    while True:
      sleep(1)
