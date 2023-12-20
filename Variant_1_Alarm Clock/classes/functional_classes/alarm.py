from PyQt6.QtCore import QTimer, pyqtSignal
from PyQt6.QtWidgets import QWidget

from classes.functional_classes.alarm_ringing import AlarmRing


class Alarm(QWidget):
   timeIsOut_signal = pyqtSignal(bool, int)

   RECALL_AFTER_CALLING = False
   ALARM_RINGING_DURATION = 0


   def __init__(self):
      self.alarmTimer = QTimer()
      self.alarmTimer.timeout.connect(self.TimeIsOut)
      
      self.alarmRing = AlarmRing()
      self.ALARM_RINGING_DURATION = self.alarmRing.ALARM_RINGING_DURATION

      super().__init__()


   def Active(self, currentMinutes, currentHours, targetMinutes, targetHours):
      # запуск таймера будильника
      self.alarmTimer.stop()
      self.alarmTimer.start(((targetHours - currentHours, 24 - currentHours + targetHours)[targetHours < currentHours] * 60 + targetMinutes - currentMinutes) * 60000)


   def Disactive(self):
      # отключение юудильника
      self.alarmTimer.stop()


   def TimeIsOut(self):
      # событие наступления врмени срабатывания будильника
      self.timeIsOut_signal.emit(self.RECALL_AFTER_CALLING, self.ALARM_RINGING_DURATION)

      self.alarmRing.PlayAlarmSound()
      
      if (not self.RECALL_AFTER_CALLING):
         self.Disactive()


   def TurnOffCalling(self):
      # выключение сигнала будильника
      self.alarmRing.StopAlarmSound()