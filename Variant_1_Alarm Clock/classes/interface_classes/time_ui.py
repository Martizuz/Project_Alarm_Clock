from PyQt6 import QtWidgets, QtGui, QtCore


class TimeUI(QtWidgets.QWidget):
   # определение констант
   CURRENT_TIME_COLOR = "#DBDBDB"
   BLINKING_COLOR = "#8D9696"

   MAIN_TIME_SHADOW_COLOR = QtGui.QColor(223,252,252)
   
   TIME_SHADOW_RADIUS = 0

   HEIGHT = 0
   WIDTH = 0

   PARENT_SIZE = 0

   FONT_SIZE = 0

   BLINKING = False
   BLINKING_INTERVAL = 500

   CHANGING_TIME = True
   CURRENT_TIME_CHANGING_INTERVAL = 60000

   # определение управляющих переменных
   itemBlinked = False
   timeSettingStep = 3

   UIcurrentMinutes = 0
   UIcurrentHours = 0

   UItemporaryMinutes = 0
   UItemporaryHours = 0

   currentTimeChanged_signal = QtCore.pyqtSignal(list)


   def __init__(self, parent, parent_size: int, width: int, blinking: bool = True):
      super().__init__(parent)

      # инициализация части констант в конструкторе
      self.WIDTH = int(width)
      self.HEIGHT = int(width / 2)
      self.PARENT_SIZE = parent_size
      self.FONT_SIZE = int(width/100*36)
      self.BLINKING = blinking
      self.TIME_SHADOW_RADIUS = int(width / 100 * 10)

      self.currentTimeTimer = QtCore.QTimer()

      self.blinkingTimer = QtCore.QTimer()
      self.blinkingTimer.timeout.connect(self.Blink)

      # запуск таймера мерцания двоеточия

      if (self.BLINKING):
         self.blinkingTimer.start(self.BLINKING_INTERVAL)         

      # запуск таймера изменения времени

      if(self.CHANGING_TIME):
         self.currentTimeTimer.start(self.CURRENT_TIME_CHANGING_INTERVAL)
         self.currentTimeTimer.timeout.connect(self.ChangeCurrentTime)

      self.setupUi()


   def setupUi(self):
      # определение интерфейсной части времени
      self.setBaseSize(self.WIDTH, self.HEIGHT)

      self.centralFrame = QtWidgets.QFrame(self)
      self.centralFrame.setGeometry(QtCore.QRect(int((self.PARENT_SIZE-self.WIDTH) / 2), int((self.PARENT_SIZE-self.HEIGHT) / 2), self.WIDTH, self.HEIGHT))
      self.centralFrame.setStyleSheet(f"""
                                       background-color: transparent;
                                       color: {self.CURRENT_TIME_COLOR};
                                       font-size: {self.FONT_SIZE}px;
                                    """)
      
      self.hoursLabel = QtWidgets.QLabel(self.centralFrame)
      self.hoursLabel.setGeometry(QtCore.QRect(0, 0, int(self.WIDTH/100*45), self.HEIGHT))
      self.hoursLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
      self.hoursLabel.setText("{:02}".format(self.UIcurrentHours))
      self.hoursLabel.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(
         self,
         blurRadius=self.TIME_SHADOW_RADIUS,
         color=QtGui.QColor(self.MAIN_TIME_SHADOW_COLOR),
         offset=QtCore.QPointF(0.0, 0.0),
      ))

      self.doublePointLabel = QtWidgets.QLabel(self.centralFrame)
      self.doublePointLabel.setGeometry(QtCore.QRect(int(self.WIDTH/100*45), 0, self.WIDTH-int(self.WIDTH/100*45)*2, self.HEIGHT))
      self.doublePointLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
      self.doublePointLabel.setText(":")
      self.doublePointLabel.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(
         self,
         blurRadius=self.TIME_SHADOW_RADIUS,
         color=QtGui.QColor(self.MAIN_TIME_SHADOW_COLOR),
         offset=QtCore.QPointF(0.0, 0.0),
      ))
      self.doublePointLabel.setStyleSheet(f"""
                                             padding-bottom: {int(self.WIDTH/100*6)}px;
                                          """)
      
      self.minutesLabel = QtWidgets.QLabel(self.centralFrame)
      self.minutesLabel.setGeometry(QtCore.QRect(self.WIDTH-int(self.WIDTH/100*45), 0, int(self.WIDTH/100*45), self.HEIGHT))
      self.minutesLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
      self.minutesLabel.setText("{:02}".format(self.UIcurrentMinutes))
      self.minutesLabel.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(
         self,
         blurRadius=self.TIME_SHADOW_RADIUS,
         color=QtGui.QColor(self.MAIN_TIME_SHADOW_COLOR),
         offset=QtCore.QPointF(0.0, 0.0),
      ))

      self.setTimeUpButton = QtWidgets.QPushButton(self.centralFrame)
      self.setTimeUpButton.setGeometry(0, 0, 0, 0)

      self.setTimeDownButton = QtWidgets.QPushButton(self.centralFrame)
      self.setTimeDownButton.setGeometry(0, 0, 0, 0)

      self.setTimeUpButton.clicked.connect(self.IncreaseTime)
      self.setTimeDownButton.clicked.connect(self.ReduceTime)


   def ChangeCurrentTime(self):
      if(self.UIcurrentMinutes == 59):
         self.UIcurrentMinutes = 0
         if(self.UIcurrentHours == 23):
            self.UIcurrentHours = 0
         else:
            self.UIcurrentHours += 1
      else:
         self.UIcurrentMinutes +=1

      self.minutesLabel.setText("{:02}".format(self.UIcurrentMinutes))
      self.hoursLabel.setText("{:02}".format(self.UIcurrentHours))

      self.currentTimeChanged_signal.emit([self.UIcurrentMinutes, self.UIcurrentHours])


   def SetPosition(self, offsetX: int, offsetY: int):
      # изменение позиционирования извне класса 
      self.centralFrame.setGeometry(QtCore.QRect(int(offsetX), int(offsetY), self.WIDTH, self.HEIGHT))


   def Blink(self):
      # мерцание минут/двоеточия/часов
      if(self.timeSettingStep == 1):
         self.minutesLabel.setStyleSheet(f"""
                                          color: {(self.BLINKING_COLOR, self.CURRENT_TIME_COLOR)[self.itemBlinked]};
                                         """)
         
      elif(self.timeSettingStep == 2):
         self.hoursLabel.setStyleSheet(f"""
                                          color: {(self.BLINKING_COLOR, self.CURRENT_TIME_COLOR)[self.itemBlinked]};
                                       """)
         
      elif(self.timeSettingStep == 3):
         self.doublePointLabel.setStyleSheet(f"""
                                                color: {(self.BLINKING_COLOR, self.CURRENT_TIME_COLOR)[self.itemBlinked]};
                                                padding-bottom: {int(self.WIDTH/100*6)}px;
                                             """)

      self.itemBlinked =  not self.itemBlinked


   def SetTime(self, step: int):
      # установка времени в несколько этапов
      self.timeSettingStep = step

      if(self.timeSettingStep == 1): 
         if(not self.BLINKING):
            self.blinkingTimer.start(self.BLINKING_INTERVAL)
            
         self.currentTimeTimer.stop()

         self.UItemporaryMinutes = self.UIcurrentMinutes 

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
         
      elif(self.timeSettingStep == 2):
         self.UItemporaryHours = self.UIcurrentHours

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
         
      elif(self.timeSettingStep == 3 or self.timeSettingStep == 4):
         self.currentTimeTimer.start(self.CURRENT_TIME_CHANGING_INTERVAL)

         if (not self.BLINKING):
            self.blinkingTimer.stop()

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
         
         if(self.timeSettingStep == 3):
            self.UIcurrentMinutes = self.UItemporaryMinutes
            self.UIcurrentHours = self.UItemporaryHours

         self.timeSettingStep = 3

         self.minutesLabel.setText("{:02}".format(self.UIcurrentMinutes))
         self.hoursLabel.setText("{:02}".format(self.UIcurrentHours))

      self.currentTimeChanged_signal.emit([self.UIcurrentMinutes, self.UIcurrentHours])


   def ReduceTime(self):
      # слот нажатия на кнопку увеличения текущего значения
      if(self.timeSettingStep == 1):
         if(self.UItemporaryMinutes > 0):
            self.UItemporaryMinutes -= 1
         else:
            self.UItemporaryMinutes = 59
         self.minutesLabel.setText("{:02}".format(self.UItemporaryMinutes))

      elif(self.timeSettingStep == 2):
         if(self.UItemporaryHours > 0):
            self.UItemporaryHours -= 1
         else:
            self.UItemporaryHours = 23
         self.hoursLabel.setText("{:02}".format(self.UItemporaryHours))


   def IncreaseTime(self):
      # слот нажатия на кнопку уменьшения текущего значения
      if(self.timeSettingStep == 1):
         if(self.UItemporaryMinutes < 59):
            self.UItemporaryMinutes += 1
         else:
            self.UItemporaryMinutes = 0
         self.minutesLabel.setText("{:02}".format(self.UItemporaryMinutes))

      elif(self.timeSettingStep == 2):
         if(self.UItemporaryHours < 23):
            self.UItemporaryHours += 1
         else:
            self.UItemporaryHours = 0
         self.hoursLabel.setText("{:02}".format(self.UItemporaryHours))

   
   def SetTimeChangeButtons(self, upBtn: str, downBtn: str):
      self.setTimeUpButton.setShortcut(upBtn)
      self.setTimeDownButton.setShortcut(downBtn)