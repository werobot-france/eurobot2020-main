from .ThreadHelper import Thread

class Toner:
  
  def __init__(self, container):
    self.logger = container.get('logger').get('Switches')
    self.arduino = container.get('arduinoSwitches')
    
  def play(self, freq = 440, duration = 1000):
    line = self.arduino.sendCommand(
      name = "TONE",
      params = [freq, duration]
    )