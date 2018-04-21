
import time
from threading import Timer, Thread, Event
from statistics import mean
import gpiozero
from signal import pause
import os


# globals
video_file = r'/home/pi/Videos/video.avi'
ctr = 10


class PulseInput(Thread):
  def __init__(self, event):
    Thread.__init__(self)
    self.stopped = event
    self.button = gpiozero.Button(4)

  def update(self):
    global ctr
    if ctr < 10: 
      ctr = ctr + 2

  def run(self):
    global ctr
    self.update()
    self.button.when_pressed = lambda : self.update()
    while not self.stopped.wait(1):
      while ctr > 0:
        ctr = ctr-1
        time.sleep(0.20)
    


stopFlag = Event()
thread = PulseInput(stopFlag)
thread.daemon = True # kill with ctrl-c
thread.start()

os.system('omxplayer -o hdmi /home/pi/Videos/video.avi &')
is_playing = True



# check activity
while True:
  time.sleep(0.5)
  if ctr == 0:
    if is_playing:
      os.system('omxplayer_dbuscontrol.sh pause')
      is_playing = False 
  else:
    if not is_playing:
      os.system('omxplayer_dbuscontrol.sh pause')
      is_playing = True


#eof
