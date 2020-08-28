from board import SCL, SDA
from time import sleep
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo
import serial
import math
from threading import Thread
from multiprocessing import Process

class Lidar:

  enabled = False

  inc = False
  dist = 0
  angle = 0
  period = 0
  newPeriodTimestamp = 0
  buffer = []
  clockwise = True

  mainThread = None
  watchDistancesThread = None
  communicateThread = None
  
  servoSlot = 0

  def __init__(self, container):
    self.serial = serial.Serial("/dev/ttyAMA0", 115200)
    self.websocket = container.get('websocket')
    self.container = container
    self.positionWatcher = container.get('positionWatcher')
    self.navigation = container.get('navigation')
    self.logger = container.get('logger').get('Lidar')
    self.driver = container.get('driver')
    self.detection = container.get('detection')
    # i2c = busio.I2C(SCL, SDA)
    # self.pca = PCA9685(i2c)
    # self.pca.frequency = 50

    # self.servo = servo.Servo(self.pca.channels[8])
    # self.servo.set_pulse_width_range(400, 2600)

  # def setAngle(self, angle):
  #   #self.servo.angle = angle
  #   self.driver.setAngle(self.servoSlot, angle)
    

  def computePointPosition(self, angle, distance):
    p = self.positionWatcher.getData()
    if self.inc : offset = -35
    else : offset = 35
    angle = math.radians(angle + 180 + offset) + p[2]
    distance += 33
    return [
      p[0] + math.cos(angle) * distance,
      p[1] + math.sin(angle) * distance
    ]

  '''
  Will try to keep up to date the 'distance' variable
  '''
  def watchDistances(self):
    while self.enabled:
      sleep(0.01)
      count = self.serial.in_waiting
      if count > 8:
        recv = self.serial.read(9)
        self.serial.reset_input_buffer()
        if recv[0] == 0x59 and recv[1] == 0x59:
          self.dist = recv[2] + recv[3] * 256
          # self.buffer.append([self.angle, self.dist])
          Thread(target=self.communication, args = [[self.angle, self.dist]]).start()
          #if debug: print("angel:", self.angle*2, inc, pos)
  
  def run(self, debug=False):
    self.angle = 0
    self.inc = False
    delta = 3
    while self.enabled:
      sleep(0.015)
      if self.angle >= 180 or self.angle <= 0:
        self.inc = not self.inc
      if self.angle >= 180:
        self.angle = 180
      if self.angle <= 0:
        self.angle = 0
        Thread(target=self.communication, args = [False]).start()
      
      self.driver.setAngle(self.servoSlot, self.angle, 'lidar')

      if self.inc:
        self.angle += delta
      else:
        self.angle -= delta

  def communication(self, d):
    #print(, )
    #pos = self.computePointPosition(d[0]*2, d[1]*10)
    #self.websocket.sendData('lidar', pos)
    #self.logger.debug([angle, dist])
    if d == False:
      self.detection.whenDetected(None, -1)
    else:
      self.detection.whenDetected(d[0], d[1])
  
  '''
  Will start to keep up to date the obstacles points
  '''
  def start(self):
    self.logger.info('Started')
    self.enabled = True
    self.inc = False

    self.distanceWatcherThread = Thread(target=self.watchDistances)
    self.distanceWatcherThread.start()
    
    self.mainThread = Thread(target=self.run)
    self.mainThread.start()

    # self.distanceWatcherThread = Thread(target=self.watchDistances)
    # self.distanceWatcherThread.start()

    
    # self.communicateThread = Thread(target=self.communication)
    # self.communicateThread.start()

  def stop(self):
    self.logger.info('Stopped')
    self.enabled = False
