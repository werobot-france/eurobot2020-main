from Adafruit_PCA9685 import PCA9685

class PWMDriver:
  def __init__(self):
    self.driver = PCA9685()
    self.driver.set_pwm_freq(50)
    self.servoProfiles = {
      'default': {'range': 180, 'min': 65, 'max': 530},
      'lidar': {'range': 180, 'min': 75, 'max': 510},
      'china': {'range': 180, 'min': 75, 'max': 510},
      'flag': {'range': 180, 'min': 100, 'max': 480},
      'rev': {'range': 270, 'min': 95, 'max': 552},
    }
  
  def setAngle(self, slot, angle, profileName = 'default'):
    profile = None
    if type(profileName) is dict:
      profile = profileName
    if profile == None:
      if profileName not in self.servoProfiles:
        profileName = 'default'
      profile = self.servoProfiles[profileName]
    if 'range' not in profile:
      profile['range'] = 180
    if angle < 0 or angle > profile['range']:
      print('PWMDriver: Invalid range passed ' + angle + ' but range is ' + profile['range'])
    
    print('setting slot', slot, 'to angle', angle, 'with profile', profileName, profile)
    pulse = int(self.mappyt(angle, 0, profile['range'], profile['min'], profile['max']))
    self.driver.set_pwm(slot, 0, pulse)

  def setPwm(self, slot, off, on):
    self.driver.set_pwm(slot, off, on)

  def mappyt(self, x, inMin, inMax, outMin, outMax):
    return (x - inMin) * (outMax - outMin) / (inMax - inMin) + outMin
