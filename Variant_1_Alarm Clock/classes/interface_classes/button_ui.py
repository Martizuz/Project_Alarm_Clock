from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtCore import QPoint


class ControlButton(QtWidgets.QPushButton):
   ROTATION_ANGLE = 0
   ROTATION_CENTER_X = 0
   ROTATION_CENTER_Y = 0

   WIDTH = 0
   HEIGHT = 0

   DEFAULT_COLOR = ""
   PRESSED_COLOR = ""

   currentColor = ""

   mouseIsOverButton = False


   def __init__(self, parent, rotationAngle: int, height: int, width: int, rotationCenterX: int, rotationCenterY: int, def_color:str = "#141414", press_color: str =  "#333333"):
      super().__init__(parent)

      self.ROTATION_ANGLE = int(rotationAngle)
      self.ROTATION_CENTER_X = int(rotationCenterX)
      self.ROTATION_CENTER_Y = int(rotationCenterY)

      self.WIDTH = int(width)
      self.HEIGHT = int(height)

      self.DEFAULT_COLOR = def_color
      self.PRESSED_COLOR = press_color

      self.currentColor = self.DEFAULT_COLOR


   def paintEvent(self, e):
      # инициализация пэинтера
      self.painter = QPainter()
      self.painter.begin(self)
      self.drawButton()
      self.painter.end()


   def drawButton(self):
      # отрисовка кнопки с заданными параметрами
      color = QColor(0, 0, 0)
      color.setNamedColor(self.currentColor)
      self.painter.setPen(color)

      self.painter.setBrush(color)
      self.painter.translate(QtCore.QPointF(self.ROTATION_CENTER_X, self.ROTATION_CENTER_Y))
      self.painter.rotate(self.ROTATION_ANGLE)

      self.path = QtGui.QPainterPath()
      self.path.addRoundedRect(QtCore.QRectF(0, 0, self.WIDTH, self.HEIGHT), 40, 25)
      self.painter.drawPath(self.path.simplified())
      

   def mousePressEvent(self, event):
      # переопределение нажатия на кнопку
      self.currentColor = self.PRESSED_COLOR
      self.update()
      super().mousePressEvent(event)


   def mouseReleaseEvent(self, event):
      # переопределение отпускания кнопки
      self.currentColor = self.DEFAULT_COLOR
      self.update()
      super().mouseReleaseEvent(event)