
import os
import sys
from .ThreadHelper import Thread
import imp

class Scripts:
  def __init__(self, container):
    self.container = container
    self.logger = container.get('logger').get('Scripts')
    self.scriptThread = None
    # module = list(map(__import__, ['src.scripts.test_script']))[0].__dict__['scripts'].__dict__['test_script'].__dict__['TestScript']()
    # print(module)
    # sys.exit()
    
  # Now take in account nested script
  def exists(self, name):
    path = 'src/scripts'
    compo = name.split('/')
    if len(compo) == 1:
      name = compo[0]
    if len(compo) == 2:
      path += '/' + compo[0]
      name = compo[1]
    if (name + '.py') not in os.listdir(path):
      return False
    return True

  def run(self, name):
    if not self.exists(name):
      return "Invalid script name"
    # different way of importing thing wheter we have a simple or a complex path
    compo = name.split('/')
    if len(compo) == 1:
      module = list(
        map(
          __import__,
          ['src.scripts.' + name]
        )
      )[0].__dict__['scripts'].__dict__[name]
      imp.reload(module)
      script = module.__dict__[name](self.container)
    else:
      module = list(
        map(
          __import__,
          ['src.scripts.' + compo[0] + '.' + compo[1]]
        )
      )[0].__dict__['scripts'].__dict__[compo[1]]
      imp.reload(module)
      script = module.__dict__[compo[1]](self.container)
    self.logger.info('Starting', name, 'script')
    self.scriptThread = Thread(target=script.run)
    self.scriptThread.start()
    return None

  def list(self):
    return os.listdir('src/scripts')

  def stop(self):
    if self.scriptThread != None:
      self.logger.info('A script was stopped')
      self.scriptThread.stop()