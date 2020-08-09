import threading
import time
import inspect
import ctypes

class WrapperThread(threading.Thread):
  def __init__(self, target):
    super().__init__()
    self.target = target

  def run(self):
    self.target()
    
class Thread:
  def __init__(self, target):
    self.target = target
    self.thread = None

  def start(self):
    self.thread = WrapperThread(self.target)
    self.thread.start()
    
  def stop(self):
    print(self.thread.isAlive())
    if not self.thread.isAlive():
      return
    tid = self.thread.ident
    exctype = SystemExit

    """Raises an exception in the threads with id tid"""
    if not inspect.isclass(exctype):
      raise TypeError("Only types can be raised (not instances)")
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
      ctypes.c_long(tid),
      ctypes.py_object(exctype)
    )
    if res == 0:
      raise ValueError("invalid thread id")
    elif res != 1:
      # """if it returns a number greater than one, you're in trouble,
      # and you should call it again with exc=NULL to revert the effect"""
      ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
      raise SystemError("PyThreadState_SetAsyncExc failed")