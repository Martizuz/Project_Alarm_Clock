from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
from PyQt6.QtCore import QTimer

class AlarmRing():
   REPEAT_INTERVAL = 300000

   AUDIO_FILE_PATH = "resurses/alarm_ring.mp3"

   alarmTurnedOff = True

   ALARM_SOUND_DURATION = 2000
   ALARM_RINGING_LOOPS = 10
   ALARM_RINGING_DURATION = ALARM_SOUND_DURATION * ALARM_RINGING_LOOPS 


   def __init__(self):
      pygame.mixer.init()

      # таймер на повторение сигнала через промежуток времени, если он не будет выключен
      self.ringRepeatTimer = QTimer()
      self.ringRepeatTimer.timeout.connect(self.PlayAlarmSound)


   def PlayAlarmSound(self):
      # запуск сигнала 
      pygame.mixer.music.load(self.AUDIO_FILE_PATH)
      pygame.mixer.music.play(self.ALARM_RINGING_LOOPS)

      if(self.alarmTurnedOff):
         self.ringRepeatTimer.start(self.REPEAT_INTERVAL)
         
         self.alarmTurnedOff = False

   
   def StopAlarmSound(self):
      # отключение сигнала будильника
      self.ringRepeatTimer.stop()

      pygame.mixer.music.stop()
      
      self.alarmTurnedOff = True