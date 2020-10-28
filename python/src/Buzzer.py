from time import sleep
from .ThreadHelper import Thread
from gpiozero import TonalBuzzer
from gpiozero import Tone

'''
Abstration of the buzzer
'''
class Buzzer:

  buzzerSlot = 6
  driver = None
  playingThread = None
  currentMelody = None
  
  def __init__(self, container = None, slot = 3):
    self.logger = container.get('logger').get('Buzzer')
    self.buzzerSlot = slot
    self.driver = TonalBuzzer(slot)

  def stop(self):
    self.logger.debug('Stopping a melody', self.currentMelody)
    self.playingThread.stop()
    
  def playMelody(self, schema, name = None):
    self.currentMelody = name
    self.logger.debug('Starting to play a melody', name)
    self.playingThread = Thread(target=self.runMelody, args=(schema))
    self.playingThread.start()
    
  def runMelody(self, schema):
    count = 0
    while count < schema['repeats']:
      for note in schema['notes']:
        self.driver.play(note[0])
        sleep(note[1])
      count += 1

  def armedSound(self):
    self.playMelody({
      'count': 1,
      'notes': [
        [220.0, 1]
      ]
    })
    
  def readySound(self):
    self.playMelody({
      'count': 1,
      'notes': [
        [440.0, 1]
      ]
    })
    
  def currentDefectSound(self):
    self.playMelody({
      'count': 1,
      'notes': [
        [960, -1]
      ]
    })