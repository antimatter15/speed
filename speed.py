
import os, sys, time
t = 0
drift = 999
speaking = True

buf = ""
start = 0
end = 0

#based loosely off http://wiki.videolan.org/How_to_use_VLC_for_transcription_in_linux
def vlc(s):
  #for some reason subprocess.Popen/communicate isn't working for me
  #from my limited google-fu skills, i can tell this 
  return os.popen('echo "'+s+'" | nc -U ~/vlc.sock').readlines()

#http://stackoverflow.com/a/8351793/205784
#takes an SRT time and turns it into an int for seconds
def srt_time_to_seconds(time):
    major = time.replace(" ","").split(',')[0].split(':')
    #print major
    return int(major[0])*3600 + int(major[1])*60 + int(major[2])

#query vlc for number of seconds elapsed in playback
def update_t():
  global t
  try:
    et = int(vlc('get_time')[0].strip())
    print "Time Delta", et - t
    t = et
  except Exception:
    print "Error parsing time delta"



def has_t(s):
  #check if within transcript range
  global buf, start, end
  #print s, end
  while s > end:
    while '-->' not in buf:
      buf = sys.stdin.readline()
    start, end = buf.split('-->')
    start = srt_time_to_seconds(start)
    end = srt_time_to_seconds(end) 
    #print buf, start, end
    buf = ''
  if start - 5 < s < end + 2:
    return True
  return False

def set_speed(s):
  if s:
    vlc('normal')
  else:
    vlc('faster')
    vlc('faster')
    vlc('faster')
    

while True:
  if drift > -1:
    update_t()
    drift = 0
  inrange = has_t(t)
  print "is speaking", inrange, "at time",t
  if inrange != speaking:
    speaking = inrange
    set_speed(speaking)
  time.sleep(1) #maybe a better timing mechanism, but whatever
  t += 1
  drift += 1
