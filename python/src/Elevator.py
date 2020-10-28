from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

class Elevator:
  
  def __init__(self, container):
    i2c = busio.I2C(SCL, SDA)
    self.pca = PCA9685(i2c)
    self.pca.frequency = 50

    self.left  = servo.Servo(self.pca.channels[1])
    self.mid   = servo.Servo(self.pca.channels[0], min_pulse=500, max_pulse=2000)
    self.right = servo.Servo(self.pca.channels[2])
    
    self.arduino = container.get('arduinoStepper')

  def setClawsAngle(self, angle, selector = None):
    if selector == None:
      selector = ['left', 'mid', 'right']
    if 'left' in selector:
      self.left.angle = (180 - angle)
    if 'mid' in selector:
      self.mid.angle = angle - 5
    if 'right' in selector:
      self.right.angle = angle - 5

  # def setClawAngle(self, index, angle):
  #   if index == 0:
  #       self.right.angle = angle
  #   if index == 1:
  #       self.mid.angle = angle
  #   if index == 2:
  #       self.left.angle = 190 - angle

  def open(self, selector = None):
    self.left.angle = 135
    self.mid.angle = 158
    self.right.angle = 55

  def close(self, selector = None):
    self.left.angle = 15
    self.mid.angle = 23
    self.right.angle = 163

  def sleep(self, selector = None):
    self.left.angle = 90
    self.mid.angle = 90
    self.right.angle = 90
  
  def lighthouse(self, selector = None):
    self.left.angle = 90
    self.mid.angle = 50
    self.right.angle = 90

  def setAll(self, angles):
    print('SET ALL CLAWS!', angles)
    self.left.angle = angles[0]
    self.mid.angle = angles[1]
    self.right.angle = angles[2]

  # top
  # lighthouse enable: 40

  def goTo(self, position, speed = 300):
    # pos haute: 500 steps
    # pos basse: 80
    self.arduino.sendCommand(
      name = "TWIN_GO_TO",
      params = [position, speed],
      expectResponse = True
    )
    self.stop()


  # elevator go to TOP
  # elevator go to TAKE
  # elevator go to BOTTOM
  def reset(self, speed = 350):
    self.arduino.sendCommand(
      name = "TWIN_SET_SPEED",
      params = [-speed],
      expectResponse = True
    )

  def stop(self):
    self.arduino.sendCommand(
      name = "STOP",
      params = [],
      expectResponse = False
    )

