
import time
import vlc
from threading import Timer, Thread, Event
from statistics import mean


# globals
video_file = r'path/to/file.avi'
t = time.time()


class PulseSimulator(Thread):
  def __init__(self, event):
    Thread.__init__(self)
    self.stopped = event
    self.secs = 0;
    self.time_diffs = [0] * 5

  def run(self):
    global t
    t_prev = time.time()
    while not self.stopped.wait(1): 
      self.secs = self.secs + 1
      if self.secs < 5 or self.secs > 10:
        self.time_diffs.pop(0)
        temp = time.time() - t_prev
        t_prev = time.time() 
        self.time_diffs.append(temp)
        t = mean(self.time_diffs)
      print(t)


stopFlag = Event()
thread = PulseSimulator(stopFlag)
thread.daemon = True # kill with ctrl-c
thread.start()

player = vlc.MediaPlayer(video_file)
player.set_fullscreen(True)

player.play()

# check activity
while True:
  time.sleep(0.8)
  if t > 2:
    if player.is_playing():
      player.pause()
  else:
    player.play()


time.sleep(5)

stopFlag.set()
print(t)
player.pause()
time.sleep(1)
player.stop()
