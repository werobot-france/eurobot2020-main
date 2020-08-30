from Adafruit_PCA9685 import PCA9685
from adafruit_motor import servo
from board import SCL, SDA
import busio

class PWMDriver:
  def __init__(self):
    self.driver = PCA9685()
    self.driver.set_pwm_freq(50)
    # i2c = busio.I2C(SCL, SDA)
    # self.pca = PCA9685(i2c)
    # self.pca.frequency = 50
    # self.slotTmp = {}
  
  def setAngle(self, slot, angle, config = 'default'):
    #self.driver.set_pwm(slot, 0, int(mappyt(angle, 0, 180, 75, 510))).
    # if str(slot) not in self.slotTmp:
    #   i = servo.Servo(self.pca.channels[slot])
    #   self.slotTmp.update({str(slot): i})
    #self.slotTmp[str(slot)].angle = angle
    #print(slot, angle)
    if config == 'lidar':
      _min = 65
      _max = 530
    elif type(config) is dict:
      _min = config['min']
      _max = config['max']
    else:
      _min = 75
      _max = 510

    self.driver.set_pwm(slot, 0, int(self.mappyt(angle, 0, 180, _min, _max)))

  def setPwm(self, slot, off, on):
    self.driver.set_pwm(slot, off, on)

  def mappyt(self, x, inMin, inMax, outMin, outMax):
    return (x - inMin) * (outMax - outMin) / (inMax - inMin) + outMin
