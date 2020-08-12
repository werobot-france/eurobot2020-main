from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

class Elevator:
  
  def __init__(self, container):
    i2c = busio.I2C(SCL, SDA)
    self.pca = PCA9685(i2c)
    self.pca.frequency = 50

    self.left  = servo.Servo(self.pca.channels[11])
    self.mid   = servo.Servo(self.pca.channels[10])
    self.right = servo.Servo(self.pca.channels[9])
    
    self.arduino = container.get('arduinoStepper')

  def setClawsAngle(self, angle):
    self.left.angle = (180 - angle) 
    self.mid.angle = angle - 5
    self.right.angle = angle - 5

  # def setClawAngle(self, index, angle):
  #   if index == 0:
  #       self.right.angle = angle
  #   if index == 1:
  #       self.mid.angle = angle
  #   if index == 2:
  #       self.left.angle = 190 - angle

  def open(self):
    self.setClawsAngle(120)

  def close(self):
    self.setClawsAngle(40)

  def goTo(self, position, speed):
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
