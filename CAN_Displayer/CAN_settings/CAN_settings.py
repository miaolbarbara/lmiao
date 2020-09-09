from CAN_settings.ui_CANsetting import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import qdarkstyle

class CAN_settings(QDialog, Ui_CAN_Setting):

    Signal_Save = pyqtSignal()
    Signal_Reset = pyqtSignal()

    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)
        self.Signal_Def()

    def Signal_Def(self):


        # connect buttons with signals:

        # disable DATA RATE
        self.label_Data.setEnabled(False)
        self.lineEdit_can0_1.setEnabled(False)
        self.label_kBaud1.setEnabled(False)
        self.label_Date1.setEnabled(False)
        self.lineEdit_CAN1_2.setEnabled(False)
        self.label_kBaud4.setEnabled(False)

        # enable BAUD RATE
        self.label_Mode.setEnabled(False)
        self.comboBox_CAN0.setEnabled(False)
        self.label_BaudRate0.setEnabled(False)
        self.lineEdit_can0.setEnabled(False)
        self.label_kBaud0.setEnabled(False)
        self.label_Mode1.setEnabled(False)
        self.comboBox_CAN1.setEnabled(False)
        self.label_BaudRate.setEnabled(False)
        self.lineEdit_CAN1.setEnabled(False)
        self.label_kBaud3.setEnabled(False)


        self.checkBox_CAN0.stateChanged.connect(self._state_CAN0)
        self.checkBox_CAN1.stateChanged.connect(self._state_CAN1)

        self.comboBox_CAN0.currentIndexChanged.connect(self._mode_changed_can0)
        self.comboBox_CAN1.currentIndexChanged.connect(self._mode_changed_can1)

        self.SAVE.clicked.connect(self._save_signal)
        self.RESET.clicked.connect(self._reset_signal)

    def _state_CAN0(self):
        # if checkBox of CAN0 is checked, enable CAN0's parameters
        if self.checkBox_CAN0.isChecked():
            self.comboBox_CAN0.setEnabled(True)
            self.label_Mode.setEnabled(True)
            self.label_kBaud0.setEnabled(True)
            self.label_BaudRate0.setEnabled(True)
            self.lineEdit_can0.setEnabled(True)
        else:
            self.comboBox_CAN0.setEnabled(False)
            self.label_Mode.setEnabled(False)
            self.label_kBaud0.setEnabled(False)
            self.label_BaudRate0.setEnabled(False)
            self.lineEdit_can0.setEnabled(False)
            self.label_Data.setEnabled(False)
            self.lineEdit_can0_1.setEnabled(False)
            self.label_kBaud1.setEnabled(False)


    def _state_CAN1(self):
        # if checkBox of CAN1 is checked, enable CAN1's parameters
        if self.checkBox_CAN1.isChecked():
            self.comboBox_CAN1.setEnabled(True)
            self.label_Mode1.setEnabled(True)
            self.label_BaudRate.setEnabled(True)
            self.lineEdit_CAN1.setEnabled(True)
            self.label_kBaud3.setEnabled(True)
        else:
            self.comboBox_CAN1.setEnabled(False)
            self.label_Mode1.setEnabled(False)
            self.label_BaudRate.setEnabled(False)
            self.lineEdit_CAN1.setEnabled(False)
            self.label_kBaud3.setEnabled(False)
            self.label_Data.setEnabled(False)
            self.lineEdit_can0_1.setEnabled(False)
            self.label_kBaud1.setEnabled(False)

    def _mode_changed_can0(self):
        if self.comboBox_CAN0.currentText() == 'CAN':
            self.label_BaudRate0.setEnabled(True)
            self.lineEdit_can0.setEnabled(True)
            self.label_kBaud0.setEnabled(True)
            self.label_Data.setEnabled(False)
            self.lineEdit_can0_1.setEnabled(False)
            self.label_kBaud1.setEnabled(False)
        else:
            self.label_Data.setEnabled(True)
            self.lineEdit_can0_1.setEnabled(True)
            self.label_kBaud1.setEnabled(True)

    def _mode_changed_can1(self):
        if self.comboBox_CAN1.currentText() == 'CAN':
            self.label_BaudRate.setEnabled(True)
            self.lineEdit_CAN1.setEnabled(True)
            self.label_kBaud3.setEnabled(True)
            self.label_Date1.setEnabled(False)
            self.lineEdit_CAN1_2.setEnabled(False)
            self.label_kBaud4.setEnabled(False)
        else:
            self.label_Date1.setEnabled(True)
            self.lineEdit_CAN1_2.setEnabled(True)
            self.label_kBaud4.setEnabled(True)

    def _save_signal(self):
        self.Signal_Save.emit()

    def _reset_signal(self):
        self.Signal_Reset.emit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    Mainwindow = CAN_settings()
    Mainwindow.show()
    sys.exit(app.exec_())