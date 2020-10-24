from time import sleep
from .ThreadHelper import Thread
from ina219 import INA219
from ina219 import DeviceRangeError

'''
Abstration of the Power monitor using the INA219 I2C sensor

some ressources:

https://www.rototron.info/raspberry-pi-ina219-tutorial/
https://github.com/chrisb2/pi_ina219

'''
class PowerMonitor:

  driver = None
  monitorThread = None
  
  # Resistance in ohms of the on board shunt resistor
  shuntResistance = 0.1
  
  # Max expected curernt (for auto gain max resolution), in amps
  maxExpected = 2
  
  # the alert level in amps
  threshold = 1
  
  address = 0x44
  
  def __init__(self, container = None, slot = 3):
    self.logger = container.get('logger').get('PowerMoni')
    self.buzzer = container.get('buzzer')
    self.ws = container.get('ws')

  def stop(self):
    self.logger.debug('Stopped')
    self.monitorThread.stop()
    
  def start(self):
    self.logger.debug('Started')
    
    self.driver = INA219(
      self.shuntResistance,
      address=self.address
    )
    self.driver.configure()
    
    self.monitorThread = Thread(target=self.monitor)
    self.monitorThread.start()
    
  def monitor(self):
    while True:
      voltage = self.driver.voltage()
      supplyVoltage = self.driver.supply_voltage()
      
      current = self.driver.current()/1000
      power = self.driver.power()
      shuntVoltage = self.driver.shunt_voltage()
      currentOverflow = self.driver.current_overflow()
      
      if current > threshold:
        self.logger.info('Level 1 reached!')
        self.buzzer.currentDefectSound()
        
      # Send the data to a websocket subscriber ?
      self.ws.sendData('mainPower', {
        'power': power,
        'current': current,
        'supplyVoltage': supplyVoltage,
        'shuntVoltage': shuntVoltage,
        'voltage': voltage,
        'currentOverflow': currentOverflow
      })
        
      # monitor period (every X seconds)
      sleep(2)
