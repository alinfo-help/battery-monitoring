import sys
from PyQt5.QtWidgets import QApplication
from ui import BatteryMonitoringSystem

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BatteryMonitoringSystem()
    window.show()
    sys.exit(app.exec_())
