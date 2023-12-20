from PyQt6.QtWidgets import QApplication
import sys

from classes.interface_classes.main_user_interface import AlarmClockInterface as Interface

if __name__ == "__main__":
   # создание виджета приложения и его запуск
   application = QApplication(sys.argv)
   window = Interface()
   window.show()
   sys.exit(application.exec())