import copy
from math import pi, radians, degrees

class CommandsManager:
  def __init__(self, container):
    self.container = container
    goToArgs = [
      ['x', True], ['y', True],
      ['theta', False],
      ['speed', False], ['stopOn', False], ['backward', False]
    ]
    self.commands = [
      {
        'name': 'ping',
        'description': 'Answer with pong!',
        'handler': self.ping
      },
      {
        'name': 'listCommands',
        'description': 'List all commands',
        'handler': self.listCommands
      },
      {
        'name': 'help',
        'description': 'Help',
        'arguments': [['name', False]],
        'handler': self.help
      },
      {
        'name': 'reset',
        'description': "Will reset the position watcher",
        'handler': self.reset
      },
      {
        'name': 'pos',
        'description': 'Get pos',
        'arguments': [['basic', False]],
        'handler': self.pos
      },
      {
        'name': 'setPos',
        'description': "Set arbitrary position",
        'arguments': [['x', True], ['y', True], ['theta', True]],
        'handler': self.setPos
      },
      {
        'name': 'ignoreXChanges',
        'description': "Arbitrary disable x encoders",
        'arguments': [['val', True]],
        'handler': self.toggleIgnoreXChanges
      },
      {
        'name': 'goto',
        'description': "It's your slave!",
        'arguments': goToArgs,
        'handler': self.goTo
      },
      {
        'name': 'relativeGoto',
        'description': "It's your slave!",
        'arguments': goToArgs,
        'handler': self.relativeGoTo
      },
      {
        'name': 'listScripts',
        'description': 'List files in the script directory',
        'handler': self.listScripts
      },
      {
        'name': 'execScript',
        'description': 'Execute a script, wOw!',
        'arguments': [['name', True]],
        'handler': self.execScript
      },
      # {
      #   'name': 'elevator',
      #   'description': 'Stepper goto or origin',
      #   'arguments': [['steps', True], ['speed', False]],
      #   'handler': self.elevator
      # },
      {
        'name': 'claws',
        'description': 'Set angle of claws servo',
        'arguments': [['side', True], ['angle', True], ['select', False]],
        'handler': self.claws
      },
      {
        'name': 'clawPos',
        'description': 'Set pos of the claw',
        'arguments': [['side', True], ['pos', True]],
        'handler': self.clawPos
      },
      {
        'name': 'clawsAngles',
        'description': 'Set pos of the claw',
        'arguments': [['side', True], ['l', True], ['m', True], ['r', True]],
        'handler': self.clawsAngles
      },
      {
        'name': 'stop',
        'description': 'Will stop the current running script',
        'handler': self.stop
      },
      {
        'name': 'orientTo',
        'description': 'Will orient to the desired angle',
        'arguments': [['theta', True], ['speed', False]],
        'handler': self.orientTo
      },
      {
        'name': 'pauseNavigation',
        'description': 'Will pause the current navigation operation',
        'handler': self.pauseNavigation
      },
      {
        'name': 'resumeNavigation',
        'description': 'Will resume the current navigation operation',
        'handler': self.resumeNavigation
      }
    ]
    def filter(item):
      item.pop('handler', None)
      if 'arguments' not in item:
        item['arguments'] = []
      return item
    self.newCommands = list(map(filter, copy.deepcopy(self.commands)))
    
  def init(self):
    self.positionWatcher = self.container.get('positionWatcher')
    self.leftClaw = self.container.get('leftClaw')
    self.rightClaw = self.container.get('rightClaw')
    self.clawsInstances = {
      'left': self.leftClaw,
      'right': self.rightClaw
    }
    self.navigation = self.container.get('navigation')
    self.platform = self.container.get('platform')
    self.elevator = self.container.get('elevator')
    self.scripts = self.container.get('scripts')
  
  '''
  parse the command and return a string with a format type (text or json)
  '''
  def exec(self, rawCommand):
    components = rawCommand.split(' ')
    components = list(filter(lambda c: len(c) > 0, components))
    if len(components) == 0:
      return ''
    commands = list(filter(lambda c: c['name'] == components[0], self.commands))
    if len(commands) == 0:
      return 'Invalid Command!'
    command = commands[0]
    if 'arguments' not in command:
      command['arguments'] = []
    components = components[1:]
    arguments = {}
    if command['arguments'] != -1:
      requiredArguments = 0
      totalArguments = len(command['arguments'])
      
      for arg in command['arguments']:
        if len(arg) > 1 and arg[1]:
          requiredArguments += 1

      if len(components) < requiredArguments:
        return 'Not enought arguments!'
      if len(components) > totalArguments:
        return 'Too much arguments!'

      i = 0
      for arg in components:
        res = arg.split('=')
        index = 0
        key = ''
        value = ''
        if len(res) == 2:
          key = res[0]
          value = res[1]
        else:
          key = command['arguments'][i][0]
          value = res[0]
        
        try:
          value = float(value)
        except ValueError:
          pass
        else:
          if value.is_integer():
            value = int(value)
        
        arguments[key] = value
        i += 1

      #print(arguments)

    return command['handler'](arguments)
  
  def getCommands(self):
    return self.newCommands

  '''''''''
  Commands handlers
  '''''''''
  
  def help(self, components):
    if 'name' in components:
      selectedCommand = None
      for command in self.newCommands:
        if command['name'] == components['name']:
          selectedCommand = copy.deepcopy(command)
      if selectedCommand == None:
        return "Unkown command, invalid command name!"
      selectedCommand['usage'] = selectedCommand['name']
      for arg in selectedCommand['arguments']:
        if len(arg) > 1 and not arg[1]:
          usage = '[' + arg[0] + ']'
        else:
          usage = '{' + arg[0] + '}'
        selectedCommand['usage'] += ' ' + usage
        
      selectedCommand.pop('arguments', None)
      return selectedCommand

    outputStr = {}
    for command in self.newCommands:
      outputStr[command['name']] = command['description']
    return outputStr

  def ping(self, _):
    return "Pong!"
  
  def listScripts(self, _):
    return self.scripts.list()
  
  def execScript(self, components):
    return self.scripts.run(components['name'])

  def elevator(self, components):
    if 'speed' not in components:
      components['speed'] = 300
    components['speed'] = int(components['speed'])
    if components['steps'] == 'origin':
      self.elevator.reset(components['speed'])
    else:
      components['steps'] = int(components['steps'])
      self.elevator.goTo(components['steps'], components['speed'])
    return 'OK'
  
  def parseClawSide(self, components):
    if 'side' not in components:
      return None
    a = components['side']
    print(a)
    if a not in ['left', 'right']:
      return None
    return self.clawsInstances[components['side']]
  
  def clawPos(self, components):
    instance = self.parseClawSide(components)
    if instance == None:
      return 'ERR'
    components['pos'] = int(components['pos'])
    instance.directGoTo(components['pos'])
    return 'OK'

  def claws(self, components):
    instance = self.parseClawSide(components)
    if instance == None:
      return 'ERR'
    selector = None
    if 'select' in components:
      selector = eval(components['select'])
    if components['angle'] == 'open':
      instance.open(selector)
    elif components['angle'] == 'close':
      instance.close(selector)
    else: 
      instance.setClawsAngle(int(components['angle']), selector)
    return 'OK'
  
  def clawsAngles(self, components):
    instance = self.parseClawSide(components)
    if instance == None:
      return 'ERR'
    self.parseClawSide(components)
    instance.setAll([components['l'], components['m'], components['r']])
    return 'OK'

  def stop(self, _):
    # will stop every thread in the world
    self.scripts.stop()
    self.navigation.stop()
    self.platform.stop()
    self.rightClaw.stop()
    return 'OK'

  def parseAngleArgs(self, args):
    if 'thetaDeg' in args:
      args['theta'] = radians(args['thetaDeg'])
    
    if 'theta' in args:
      args['theta'] = eval(str(args['theta']), { 'pi': pi })
    return args
  
  def goTo(self, args):
    if 'backward' in args:
      args['backward'] = bool(args['backward'])
    args = self.parseAngleArgs(args)
    self.navigation.goTo(**args)
    return 'Done'

  def relativeGoTo(self, args):
    args = self.parseAngleArgs(args)
    self.navigation.relativeGoTo(**args)
    return 'OK'
  
  def orientTo(self, args):
    args = self.parseAngleArgs(args)
    self.navigation.orientTo(**args)
    return 'OK'

  def reset(self, args):
    self.positionWatcher.reset()
    return 'OK'
  
  def pos(self, args):
    data = list(self.positionWatcher.getPos())
    if 'basic' not in args:
      data[2] = [data[2], degrees(data[2])]
    return data
  
  def setPos(self, args):
    args = self.parseAngleArgs(args)
    self.positionWatcher.setPos(args['x'], args['y'], args['theta'])
    return 'OK'
  
  def toggleIgnoreXChanges(self, args):
    self.positionWatcher.setIgnoreXChanges(not self.positionWatcher.ignoreXChanges)
    return 'OK'
  
  def example(self, components):
    return 'OK'
  
  def listCommands(self, components):
    return self.newCommands

  def pauseNavigation(self, _):
    self.navigation.pause()
    return None

  def resumeNavigation(self, _):
    self.navigation.resume()
    return None