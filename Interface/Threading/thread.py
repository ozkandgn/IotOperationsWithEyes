import threading
import time


class ThreadRefresh (threading.Thread):
   def __init__(self, function, delay):
      threading.Thread.__init__(self)
      self.function = function
      self.delay = delay
      self.threadLock = threading.Lock()

   def run(self):
      print ("Starting ")
      # Get lock to synchronize threads
      self.threadLock.acquire()
      run_func(self.function, self.delay)
      # Free lock to release next thread
      self.threadLock.release()

def run_func(function, delay):
	while True:
	    time.sleep(delay)
	    function()