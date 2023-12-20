from classes.interface_classes.time_ui import TimeUI
from classes.functional_classes.alarm import Alarm
from PyQt6 import QtCore


class AlarmUI(TimeUI):
   CHANGING_TIME = False

   CURRENT_TIME_COLOR = "#575757"

   ACTIVE_CURRENT_TIME_COLOR = "#B5F8F8"
   DISACTIVE_CURRENT_TIME_COLOR = "#575757"

   isActive = False

   timeIsOut_signal = QtCore.pyqtSignal(int)


   def __init__(self, parent, parent_size: int, width: int):
      
      self.currentAlarm = Alarm()
      self.currentAlarm.timeIsOut_signal.connect(self.AlarmTimeOut)

      super().__init__(parent, parent_size, width, False)

      
   def ActiveAlarm(self, currentTime: list = [0, 0]):
      # изменение интерфейса при активации будильника
      self.CURRENT_TIME_COLOR = self.ACTIVE_CURRENT_TIME_COLOR

      self.minutesLabel.setStyleSheet(f"""
                                          color: {self.CURRENT_TIME_COLOR};
                                       """)
      self.doublePointLabel.setStyleSheet(f"""
                                             color: {self.CURRENT_TIME_COLOR};
                                             padding-bottom: {int(self.WIDTH/100*6)}px;
                                          """)
      self.hoursLabel.setStyleSheet(f"""
                                       color: {self.CURRENT_TIME_COLOR};
                                    """)
      self.currentAlarm.Active(currentTime[0], currentTime[1], self.UIcurrentMinutes, self.UIcurrentHours)


   def DisactiveAlarm(self):
      # изменение интерфейса при выключении будильника
      self.CURRENT_TIME_COLOR = self.DISACTIVE_CURRENT_TIME_COLOR

      self.minutesLabel.setStyleSheet(f"""
                                          color: {self.CURRENT_TIME_COLOR};
                                       """)
      self.doublePointLabel.setStyleSheet(f"""
                                             color: {self.CURRENT_TIME_COLOR};
                                             padding-bottom: {int(self.WIDTH/100*6)}px;
                                          """)
      self.hoursLabel.setStyleSheet(f"""
                                       color: {self.CURRENT_TIME_COLOR};
                                    """)
      self.currentAlarm.Disactive()

   
   def AlarmTimeOut(self, recall: bool, alarm_duration: int):
      # слот срабатывания будильника
      if (not recall):
         self.DisactiveAlarm()
      
      self.timeIsOut_signal.emit(alarm_duration)


   def TurnOffCalling(self):
      # слот выключения сигнала будильника
      self.currentAlarm.TurnOffCalling()