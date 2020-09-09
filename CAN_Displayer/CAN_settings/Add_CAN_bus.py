import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qdarkstyle

class Add_CAN_bus(QDialog):
    '''
    Signal_load_DBC：oad DBC file；
    Signal_Parser_CAN：if get_message =1, parser can message
    '''
    Signal_add_can_0 = pyqtSignal()
    Signal_add_can_1 = pyqtSignal()
    Signal_Save_bus = pyqtSignal()

    def __init__(self,parent=None):
        super(Add_CAN_bus, self).__init__(parent)
        self.SetUI()

    def SetUI(self):
        self.setWindowTitle("Add CAN bus")
        # self.resize(500,200)
        self.Font = QFont()
        self.Font.setPixelSize(20)
        self.FixedHeight = 15

        self.Add_CAN_0 = QCheckBox('CAN 0')
        self.Add_CAN_1 = QCheckBox('CAN 1')
        self.Add_CAN_0.setChecked(True)
        self.Add_CAN_1.setChecked(True)
        self.Save = QPushButton('Save for all')
        self.Close = QPushButton('Save and close')

        self.CheckBox = QVBoxLayout()
        self.CheckBox.addWidget(self.Add_CAN_0)
        self.CheckBox.addWidget(self.Add_CAN_1)

        self.ButtonGroup = QVBoxLayout()
        self.ButtonGroup.addWidget(self.Close)
        self.ButtonGroup.addWidget(self.Save)

        self.total = QHBoxLayout()
        self.total.addLayout(self.CheckBox)
        self.total.addLayout(self.ButtonGroup)
        self.setLayout(self.total)

        self.Add_CAN_0.stateChanged.connect(self._add_can_0)
        self.Add_CAN_1.stateChanged.connect(self._add_can_1)
        self.Save.clicked.connect(self._save_bus)
        self.Close.clicked.connect(self._close_window)

    def _add_can_0(self):
        self.Signal_add_can_0.emit()

    def _add_can_1(self):
        self.Signal_add_can_1.emit()

    def _save_bus(self):
        self.Signal_Save_bus.emit()

    def _close_window(self):
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    Mainwindow = Add_CAN_bus()
    Mainwindow.show()
    sys.exit(app.exec_())