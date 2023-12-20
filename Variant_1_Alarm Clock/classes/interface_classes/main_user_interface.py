from PyQt6 import QtWidgets, QtGui, QtCore
from classes.interface_classes.time_ui import TimeUI
from classes.interface_classes.alarm_ui import AlarmUI
from classes.interface_classes.button_ui import ControlButton
from classes.functional_classes.radio import Radio


class AlarmClockInterface(QtWidgets.QMainWindow):
   # определение основных констант
   WINDOW_BACKGROUND_COLOR = "#1F1F1F"

   WINDOW_WIDTH = 640
   WINDOW_HEIGHT = 640

   WINDOW_SHADOW_RADIUS = 20

   WIDGET_WIDTH = WINDOW_WIDTH - WINDOW_SHADOW_RADIUS*2
   WIDGET_HEIGHT = WINDOW_HEIGHT - WINDOW_SHADOW_RADIUS*2

   DIAL_SIZE = 500

   MAIN_TIME_WIDTH = 380

   ALARM_TIME_WIDTH = 100
   ALARM_TIME_OFFSET_Y = 330

   BUTTON_WIDTH = 100
   BUTTON_HEIGHT = 70

   # определение основных  переменных
   main_timeSettingStage = 1
   alarm_timeSettingStage = 1
   alarm_modeStage = 1

   currentTime = [0, 0]

   alarmCalling = False

   alarmIsActive = False


   def __init__(self):
      super().__init__()
      self.setupUi(self)

      self.radio = Radio()

      self.setupConnetcs()

      #установка таймера звонка будильника
      self.alarmCallingTimer = QtCore.QTimer()
      self.alarmCallingTimer.timeout.connect(self.AlarmCallingEnd)

      #установка таймера радио
      self.radioTimer = QtCore.QTimer()
      self.radioTimer.timeout.connect(self.RadioTimerEnd)


   def setupUi(self, Interface): 
      #настройка главного окна приложения
      Interface.setObjectName("MainForm")
      Interface.resize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
      Interface.setBaseSize(QtCore.QSize(0, 0))
      Interface.setWindowTitle("Alarm")

      self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
      self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

      self.setWindowIcon(QtGui.QIcon("resurses\clock.png"))

      #инициализация и определение всех элементов графического интерфейса  
      self.mainWidget = QtWidgets.QWidget(Interface)
      self.mainWidget.setObjectName("mainWidget")
      self.setCentralWidget(self.mainWidget)

      self.mainWidget.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(
         self,
         blurRadius=self.WINDOW_SHADOW_RADIUS,
         color=QtGui.QColor(20,20,20),
         offset=QtCore.QPointF(0.0, 0.0),
      ))

      self.mainFrame = QtWidgets.QFrame(self.mainWidget)
      self.mainFrame.setGeometry(QtCore.QRect(self.WINDOW_SHADOW_RADIUS, self.WINDOW_SHADOW_RADIUS, self.WIDGET_WIDTH, self.WIDGET_HEIGHT))
      self.mainFrame.setStyleSheet(f"""
                                    background-color: {self.WINDOW_BACKGROUND_COLOR};
                                    border-radius: {int(min(self.WIDGET_WIDTH, self.WIDGET_HEIGHT)/2)}px;
                                   """)

      self.resetButton = ControlButton(self.mainFrame, 90, self.BUTTON_HEIGHT, self.BUTTON_WIDTH, self.BUTTON_HEIGHT, 0, "#4A080B", "#370609")
      self.resetButton.setGeometry(int((self.WIDGET_WIDTH - self.DIAL_SIZE)/ 200 * 60), int(self.WIDGET_HEIGHT / 2 - self.BUTTON_WIDTH / 2), self.BUTTON_HEIGHT, self.BUTTON_WIDTH)
      self.resetButton.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(
         self,
         blurRadius=10,
         color=QtGui.QColor(10,10,10),
         offset=QtCore.QPointF(0.0, 0.0),
      ))

      self.timeSettingButton = ControlButton(self.mainFrame, 0, self.BUTTON_HEIGHT, self.BUTTON_WIDTH, 0, 0)
      self.timeSettingButton.setGeometry(int(self.WIDGET_WIDTH / 2 - self.BUTTON_WIDTH / 2), int((self.WIDGET_HEIGHT - self.DIAL_SIZE)/ 200 * 60), self.BUTTON_WIDTH, self.BUTTON_HEIGHT)
      self.timeSettingButton.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(
         self,
         blurRadius=10,
         color=QtGui.QColor(10,10,10),
         offset=QtCore.QPointF(0.0, 0.0),
      ))

      self.alarmSettingButton = ControlButton(self.mainFrame, 90, self.BUTTON_HEIGHT, self.BUTTON_WIDTH, self.BUTTON_HEIGHT, 0)
      self.alarmSettingButton.setGeometry(self.WIDGET_WIDTH - int((self.WIDGET_WIDTH - self.DIAL_SIZE)/ 200 * 60) - self.BUTTON_HEIGHT, int(self.WIDGET_HEIGHT / 2 - self.BUTTON_WIDTH / 2), self.BUTTON_HEIGHT, self.BUTTON_WIDTH)
      self.alarmSettingButton.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(
         self,
         blurRadius=10,
         color=QtGui.QColor(10,10,10),
         offset=QtCore.QPointF(0.0, 0.0),
      ))

      self.modeChangingButton = ControlButton(self.mainFrame, 0, self.BUTTON_HEIGHT, self.BUTTON_WIDTH, 0, 0)
      self.modeChangingButton.setGeometry(int(self.WIDGET_WIDTH / 2 - self.BUTTON_WIDTH / 2), self.WIDGET_HEIGHT - int((self.WIDGET_HEIGHT - self.DIAL_SIZE)/ 200 * 60) - self.BUTTON_HEIGHT, self.BUTTON_WIDTH, self.BUTTON_HEIGHT)
      self.modeChangingButton.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(
         self,
         blurRadius=10,
         color=QtGui.QColor(10,10,10),
         offset=QtCore.QPointF(0.0, 0.0),
      ))

      self.timeFrame = QtWidgets.QFrame(self.mainFrame)
      self.timeFrame.setGeometry(QtCore.QRect(int((self.WIDGET_WIDTH-self.DIAL_SIZE) / 2), int((self.WIDGET_HEIGHT-self.DIAL_SIZE) / 2), self.DIAL_SIZE, self.DIAL_SIZE))
      self.timeFrame.setStyleSheet(f"""
                                    background-color: qradialgradient(cx:0.5, cy:0.5, radius: 0.5, fx:0.5, fy:0.5, stop:0 rgba(50, 50, 50, 1), stop:0.95 rgba(30, 30, 30, 1), stop: 1 rgba(10, 10, 10, 0.1));
                                    border-radius: {int(self.DIAL_SIZE / 2)};
                                   """)
      self.timeFrame.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(
         self,
         blurRadius=50,
         color=QtGui.QColor(0,0,0),
         offset=QtCore.QPointF(0.0, 0.0),
      ))
      self.timeFrame.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)

      self.alarmIconLabel = QtWidgets.QLabel(self.timeFrame)
      self.alarmIconLabel.setGeometry(int(self.DIAL_SIZE / 12 * 8), int(self.DIAL_SIZE / 2  - self.MAIN_TIME_WIDTH / 4), 30, 30)
      self.alarmIconLabel.setStyleSheet(f"""
                                          background: transparent;
                                        """)
      self.alarmIconLabel.setPixmap(QtGui.QPixmap("resurses/alarm_disactive.png"))
      self.alarmIconLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

      self.radioIconLabel = QtWidgets.QLabel(self.timeFrame)
      self.radioIconLabel.setGeometry(int(self.DIAL_SIZE / 12 * 9), int(self.DIAL_SIZE / 2  - self.MAIN_TIME_WIDTH / 4), 30, 30)
      self.radioIconLabel.setStyleSheet(f"""
                                          background: transparent;
                                        """)
      self.radioIconLabel.setPixmap(QtGui.QPixmap("resurses/radio_disactive.png"))
      self.radioIconLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
      
      self.mainTimeWidget = TimeUI(self.timeFrame, self.DIAL_SIZE, self.MAIN_TIME_WIDTH)
      
      self.alarmTimeWidget = AlarmUI(self.timeFrame, self.DIAL_SIZE, self.ALARM_TIME_WIDTH)
      self.alarmTimeWidget.SetPosition(int((self.DIAL_SIZE - self.ALARM_TIME_WIDTH)/2), self.ALARM_TIME_OFFSET_Y)

      self.helpButton = QtWidgets.QPushButton(self.timeFrame)
      self.helpButton.setGeometry(QtCore.QRect(int(self.DIAL_SIZE/100*89), int(self.DIAL_SIZE/100*11), 30, 30))
      self.helpButton.setStyleSheet("""
                                       QPushButton {
                                          background-color: #1F1F1F;
                                          border-radius: 15px;
                                       }
                                       QPushButton:hover:hover {
                                          background-color: #A2B9B9;
                                       }
                                    """)
      self.helpButton.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(
         self,
         blurRadius=10,
         color=QtGui.QColor(10,10,10),
         offset=QtCore.QPointF(0.0, 0.0),
      ))


   def setupConnetcs(self):
      # подключение сигналов всех элементов к соответсвующим слотам
      self.mainTimeWidget.currentTimeChanged_signal.connect(self.CurrentTimeChanged)
      self.timeSettingButton.clicked.connect(self.CurrentTimeSetting)
      self.alarmSettingButton.clicked.connect(self.AlarmTimeSetting)
      self.resetButton.clicked.connect(self.Reset)
      self.modeChangingButton.clicked.connect(self.ChangeMode)
      self.alarmTimeWidget.timeIsOut_signal.connect(self.TimeIsOut)
      self.radio.newsStarted_signal.connect(self.NewsStarted)
      self.helpButton.clicked.connect(self.ViewHelp)


   def ViewHelp(self):
      msg = QtWidgets.QMessageBox()
      msg.setIconPixmap(QtGui.QPixmap("resurses\instruction.png"))
      msg.setWindowTitle("Help")
      msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Cancel)
      msg.setStyleSheet("QPushButton{ width: 460;}")
      msg.exec()


   @QtCore.pyqtSlot(list)
   def CurrentTimeChanged(self, time):
      # сохранение текущего времени
      self.currentTime = time
      

   def CurrentTimeSetting(self):
      # изменение текущего времени
      # настройка шорткатов
      self.alarmTimeWidget.SetTimeChangeButtons("", "")
      self.mainTimeWidget.SetTimeChangeButtons("Up", "Down")

      self.mainTimeWidget.SetTime(self.main_timeSettingStage)

      # проверка текущего этапа установки будильника и времени
      if(self.alarm_timeSettingStage != 1):
         self.alarmTimeWidget.SetTime(4)
         self.alarm_timeSettingStage = 1

         if(self.alarmIsActive):
               self.alarmTimeWidget.ActiveAlarm(self.currentTime)

      if (self.main_timeSettingStage != 3):
         self.main_timeSettingStage += 1
      else:
         self.main_timeSettingStage = 1

         # перезапуск текущего будильника, если он был включен
         if(self.alarmIsActive == True):
            self.currentTime = [self.mainTimeWidget.UIcurrentMinutes, self.mainTimeWidget.UIcurrentHours]

            self.alarmTimeWidget.DisactiveAlarm()
            self.alarmTimeWidget.ActiveAlarm(self.currentTime)


   def AlarmTimeSetting(self):
      # изменение текущего будильника
      # настройка шорткатов
      self.alarmTimeWidget.SetTimeChangeButtons("Up", "Down")
      self.mainTimeWidget.SetTimeChangeButtons("", "")

      self.alarmTimeWidget.SetTime(self.alarm_timeSettingStage)

      # проверка текущего этапа установки времени будильника
      if(self.main_timeSettingStage != 1):
         self.mainTimeWidget.SetTime(4)
         self.main_timeSettingStage = 1

      if (self.alarm_timeSettingStage != 3):
         self.alarm_timeSettingStage += 1
      else:
         self.alarm_timeSettingStage = 1
         self.alarmTimeWidget.DisactiveAlarm()
         self.alarmTimeWidget.ActiveAlarm(self.currentTime)

         self.alarmIconLabel.setPixmap(QtGui.QPixmap("resurses/alarm_active.png"))
         self.radioIconLabel.setPixmap(QtGui.QPixmap("resurses/radio_disactive.png"))

         self.alarmIsActive = True

         self.radio.DisconnectRadio()

         self.radioTimer.stop()
         self.alarm_modeStage = 2


   def Reset(self):
      # действие при нажатии кнопки сброса
      # сброс сигнала будильника если он звенит в данный момент
      if(self.alarmCalling):
         self.alarmCalling = False

         self.alarmTimeWidget.TurnOffCalling()

      else:
         # сброс установки времени будильника
         if(self.alarm_timeSettingStage != 1):
            self.alarmTimeWidget.SetTime(4)
            self.alarm_timeSettingStage = 1

         # сброс установки текущего времени
         if(self.main_timeSettingStage != 1):
            self.mainTimeWidget.SetTime(4)
            self.main_timeSettingStage = 1


   def ChangeMode(self):
      # действия при нажатии на кнопку смены режимов
      if(self.alarm_modeStage != 4):
         self.alarm_modeStage += 1
      else:
         self.alarm_modeStage = 1

      if(self.alarm_modeStage == 1):
         self.alarmIconLabel.setPixmap(QtGui.QPixmap("resurses/alarm_disactive.png"))
         self.radioIconLabel.setPixmap(QtGui.QPixmap("resurses/radio_disactive.png"))

         self.alarmTimeWidget.DisactiveAlarm()
         self.alarmIsActive = False

         self.radio.DisconnectRadio()

         self.radioTimer.stop()

      elif(self.alarm_modeStage == 2):
         self.alarmIconLabel.setPixmap(QtGui.QPixmap("resurses/alarm_active.png"))

         self.alarmTimeWidget.ActiveAlarm(self.currentTime)
         self.alarmIsActive = True

      elif(self.alarm_modeStage == 3):
         self.radioIconLabel.setPixmap(QtGui.QPixmap("resurses/radio_active.png"))

         self.radio.ConnectRadio()

         self.alarmIconLabel.setPixmap(QtGui.QPixmap("resurses/alarm_disactive.png"))

         self.alarmTimeWidget.DisactiveAlarm()
         self.alarmIsActive = False
      
      elif(self.alarm_modeStage == 4):   
         self.alarmTimeWidget.DisactiveAlarm()
         self.alarmIsActive = False

         self.radio.DisconnectRadio()
         self.radio.ConnectRadio()

         self.alarmIconLabel.setPixmap(QtGui.QPixmap("resurses/alarm_disactive.png"))
         self.radioIconLabel.setPixmap(QtGui.QPixmap("resurses/radio_active.png"))


   @QtCore.pyqtSlot(int)
   def TimeIsOut(self, alarm_duration):
      # таймер текущего звонка будильника
      self.alarmCalling = True

      self.alarmIconLabel.setPixmap(QtGui.QPixmap("resurses/alarm_disactive.png"))
      
      self.alarmCallingTimer.start(alarm_duration)


   def NewsStarted(self, radio_duration):
      self.radioTimer.start(radio_duration)

   def AlarmCallingEnd(self):
      # переменная показывающая, что в данный момент тайм аут между звонками будильника
      self.alarmCalling = False


   def RadioTimerEnd(self):
      # отключение таймера радио
      self.radioTimer.stop()

      self.radio.DisconnectRadio()
      self.radioIconLabel.setPixmap(QtGui.QPixmap("resurses/radio_disactive.png"))

      self.alarmTimeWidget.ActiveAlarm(self.currentTime)
      self.alarmIsActive = True