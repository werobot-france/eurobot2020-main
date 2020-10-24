from .WebSocketServerLib import WebsocketServer
import logging
import base64
import json
import re
from .ThreadHelper import Thread

class WebSocketServer:

  def __init__(self, container, listeningPort = 8082, listeningHost = '0.0.0.0'):
    self.container = container
    self.mainThread = None
    self.clients = []
    self.logger = self.container.get('logger').get('WebSocketServer')
    self.server = WebsocketServer(listeningPort, host=listeningHost)
    self.server.onNewClient(self.onClient)
    self.server.onMessageReceived(self.onMessage)
    self.server.onClientLeft(self.onDisconnect)
    self.server.onServerError(lambda e: self.logger.error(e))
    self.server.onServerStarted(lambda p: self.logger.info('Server started on', p))
    self.server.onServerClosed(lambda: self.logger.info('Server closed'))
    self.game = None
    
  def getAddr(self, client):
    return client['address'][0] + ':' + str(client['address'][1])

  def onClient(self, client, _):
    addr = self.getAddr(client)
    if 'identifier' not in client['query']:
      return
    identifier = client['query']['identifier']
    self.logger.info('Got a new client', addr, identifier)

    # remove old client that own the same identifier
    self.clients = list(filter(lambda c: c['identifier'] != identifier, self.clients))
    # add the new client in the list
    self.clients.append({
      'identifier': identifier,
      'addr': addr,
      'subs': [],
      'instance': client
    })
    # print('clients', len(self.clients))

  def onDisconnect(self, client, _):
    addr = self.getAddr(client)
    self.logger.info('Client left', addr)

    # remove the client from the list of connected client
    self.clients = list(filter(lambda c: c['addr'] != addr, self.clients))
    # print('clients', len(self.clients))

  def onMessage(self, client, server, message):
    #self.logger.debug('New message', message)
    addr = self.getAddr(client)
    # We parse the json of the message
    messageParsed = json.loads(message)

    # just a sanity check to check for useless things to check olalalal
    if not ('command' in messageParsed and 'args' in messageParsed):
      self.logger.warn('Invalid message format')
      return

    command = messageParsed['command']
    args = messageParsed['args']
    #print(command, args)
    
    def getClient():
      return list(filter(lambda c: c['addr'] == addr, self.clients))[0]
    
    if command == 'ping':
      self.send(client, 'pong', 'pong')
    
    elif command == 'listCommands':
      self.send(client, 'listCommandsResponse', self.commandsManager.getCommands())
    
    elif command == 'execCommand':
      # interpret a command
      res = self.commandsManager.exec(args['payload'])
      #print(res)
      if res != None:
        self.send(client, 'execCommandResponse', res)
    
    elif command == 'sub':
      c = getClient()
      # register a sub
      self.clients[self.clients.index(c)]['subs'].append(args['topic'])
    
    elif command == 'listSubs':
      # list subs
      c = getClient()
      self.logger.debug('subs asked', c['subs'])
    
    elif command == 'removeSub':
      c = getClient()
      self.clients[self.clients.index(c)]['subs'].remove(args['topic'])
      
    elif command == 'wowo':
      self.send(client, 'pong', 'pong')
    
    elif command == 'arm':
      self.game.arm(args)
    
    elif command == 'abort':
      self.game.abort()
    
    elif command == 'goTo':
      if args['robot'] == 'primary':
        args['x'] = float(args['x'])
        args['y'] = float(args['y'])
        args['speed'] = float(args['speed'])
        args['theta'] = float(args['theta'])
        self.navigation.goTo(**args)
      else:
        # transfert to the secondary robot
        pass

    elif command == 'orientTo':
      if args['robot'] == 'primary':
        args['orientation'] = float(args['orientation'])
        args['speed'] = float(args['speed'])
        self.navigation.orientTo(args['orientation'], args['speed'])
      else:
        # transfert to the secondary robot
        pass

    elif command == 'reset':
      if args['robot'] == 'primary':
        self.positionWatcher.reset()
        pass
      else:
        # transfert to the secondary robot
        pass
    
    else:
      self.send(client, 'error', 'unknown')

  def send(self, client, responseType, data = None):
    if not client['handler'].keep_alive:
      return False
    #print(data)
    toSend = json.dumps({'responseType': responseType, 'data': data})
    # if responseType != 'frame':
    #     print(toSend)
    #print(toSend)
    self.server.send_message(client, toSend)
    return True

  def sendData(self, topic, data):
    if len(self.clients) == 0:
      return False
    
    # send the same message to every client that sub to this topic
    subscribers = list(filter(
      lambda c: len(list(filter(lambda s: s == topic, c['subs']))) > 0,
      self.clients
    ))
    
    #print(topic, data, len(subscribers))
    for sub in subscribers:
      self.send(sub['instance'], topic, data)
    
    return len(subscribers) > 0

  def start(self):
    self.game = self.container.get('game')
    self.positionWatcher = self.container.get('positionWatcher')
    self.navigation = self.container.get('navigation')
    self.commandsManager = self.container.get('commandsManager')

    self.mainThread = Thread(target=self.server.run_forever)
    self.mainThread.start()

  def stop(self):
    self.server.closeServer()
    self.mainThread.stop()