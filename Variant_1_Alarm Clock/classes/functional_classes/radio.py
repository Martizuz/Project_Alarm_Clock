from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget

class Radio(QWidget):
   NEWS_DURATION = 99000

   AUDIO_FILE_PATH = "resurses/news_recording.mp3"

   newsStarted_signal = pyqtSignal(int)

   def __init__(self):
      pygame.mixer.init()

      super().__init__()

   def ConnectRadio(self):
      print("Device was connected to the radio chanel.")
      pygame.mixer.music.load(self.AUDIO_FILE_PATH)
      self.newsStarted_signal.emit(self.NEWS_DURATION)

      pygame.mixer.music.play()

   def DisconnectRadio(self):
      print("Device radio chanel was disconnected.")
      pygame.mixer.music.stop()