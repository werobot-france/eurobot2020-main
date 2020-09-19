
import json
from time import sleep
from .ThreadHelper import Thread
import random
import time
from websocket import create_connection
from websocket import WebSocketConnectionClosedException

class WebSocketClient:

  def __init__(self, uri, identifier = ''):
    self.message = ''
    if uri.find('identifier=') == -1 and identifier == '':
      identifier = 'terminal_' + str(random.randint(1000, 9999)) + '_' + str(round(time.time(), 3))
    self.uri = uri + '?identifier=' +  identifier
    self.ws = None
    self.listenThread = None
    self.callback = None
    self.onTimeCallback = None
    self.lastData = None

  def recv(self):
    res = self.ws.recv()
    data = json.loads(res)['data']
    return data

  def run(self):
    e = True
    while e:
      try:
        self.lastData = self.recv()
      except WebSocketConnectionClosedException:
        e = False
      if self.onTimeCallback != None:
        self.onTimeCallback(self.lastData)
        self.onTimeCallback = None
    sleep(1)
    self.start()

  def start(self):
    try:
      self.ws = create_connection(self.uri)
    except ConnectionRefusedError:
      sleep(1)
      self.start()
    self.listenThread = Thread(target=self.run)
    self.listenThread.start()

  def stop(self):
    self.ws.close()
    self.listenThread.stop()
    self.listenThread = None

  def send(self, command, args = {}, oneTimeCallback = None):
    toSend = json.dumps({'command': command, 'args': args})
    self.ws.send(toSend)
    if oneTimeCallback:
      self.onTimeCallback = None
      self.lastData = None
      while self.lastData == None:
        time.sleep(0.001)
      return self.lastData
    else:
      self.onTimeCallback = oneTimeCallback
      return True
