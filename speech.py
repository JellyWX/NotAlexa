import speech_recognition as sr
import threading
import time
import datetime
import os

r = sr.Recognizer()

months = {
  1 : 'January',
  2 : 'February',
  3 : 'March',
  4 : 'April',
  5 : 'May',
  6 : 'June',
  7 : 'July',
  8 : 'August',
  9 : 'September',
  10 : 'October',
  11 : 'November',
  12 : 'December'
}

class Record(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    self.audio = None

  def run(self):
    while 1:
      with sr.Microphone() as source:
        self.audio = r.listen(source)

class Interpret(threading.Thread):
  def __init__(self, recorder):
    threading.Thread.__init__(self)
    self.recorder = recorder
    self.speech = ['', '']

  def run(self):
    while 1:
      time.sleep(1)
      try:
        self.speech.append(r.recognize_google(self.recorder.audio))
      except AssertionError:
        pass
      except sr.UnknownValueError:
        pass
      except sr.RequestError:
        print('Error in communication. Check your connection')
      except Exception as e:
        print(e)

      if len(self.speech) > 2:
        self.speech.pop(0)

      self.recorder.audio = None

      compiled_voice = ' '.join(self.speech).replace(' ', '').replace('\'', '')

      if 'whatstheday' in compiled_voice:
        os.system('espeak \'The day is {}th of {}\' &'.format(datetime.datetime.now().day, months[datetime.datetime.now().month]))
        self.speech = ['', '']

mic = Record()
i = Interpret(mic)

mic.start()
i.start()
