# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './icon/main_window.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(946, 645)
        MainWindow.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(10, 20, 421, 71))
        self.frame.setStyleSheet("")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.Addfile = QtWidgets.QPushButton(self.frame)
        self.Addfile.setGeometry(QtCore.QRect(0, -10, 84, 71))
        self.Addfile.setMinimumSize(QtCore.QSize(10, 10))
        self.Addfile.setStyleSheet(" QPushButton#Addfile {\n"
"     background-color: transparent;\n"
"     border:none\n"
" }\n"
" QPushButton#Addfile:pressed {\n"
"     background-color: rgb(220,220,220);     \n"
"     border:none\n"
" }\n"
"")
        self.Addfile.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./icon\\toppng.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Addfile.setIcon(icon)
        self.Addfile.setIconSize(QtCore.QSize(80, 80))
        self.Addfile.setObjectName("Addfile")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(10, 50, 71, 16))
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.frame)
        self.lineEdit.setGeometry(QtCore.QRect(72, 50, 161, 20))
        self.lineEdit.setStyleSheet("background-color: transparent;\n"
"border: none")
        self.lineEdit.setObjectName("lineEdit")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(10, 90, 921, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(10, 110, 921, 481))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.log = QtWidgets.QPushButton(self.frame_2)
        self.log.setGeometry(QtCore.QRect(120, 50, 101, 111))
        self.log.setStyleSheet(" QPushButton#log {\n"
"     background-color: transparent;\n"
"     border:none\n"
" }\n"
" QPushButton#log:pressed {\n"
"     background-color: rgb(220,220,220);     \n"
"     border:none\n"
" }\n"
"")
        self.log.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("./icon\\icons8-log-96.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.log.setIcon(icon1)
        self.log.setIconSize(QtCore.QSize(70, 70))
        self.log.setObjectName("log")
        self.line_4 = QtWidgets.QFrame(self.frame_2)
        self.line_4.setGeometry(QtCore.QRect(340, 110, 20, 211))
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.line_7 = QtWidgets.QFrame(self.frame_2)
        self.line_7.setGeometry(QtCore.QRect(470, 350, 41, 41))
        self.line_7.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_7.setObjectName("line_7")
        self.line_8 = QtWidgets.QFrame(self.frame_2)
        self.line_8.setGeometry(QtCore.QRect(460, 90, 20, 281))
        self.line_8.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_8.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_8.setObjectName("line_8")
        self.mode_button = QtWidgets.QPushButton(self.frame_2)
        self.mode_button.setGeometry(QtCore.QRect(340, 140, 121, 161))
        self.mode_button.setStyleSheet("background-color: transparent;\n"
"border:none\n"
"\n"
"")
        self.mode_button.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("./icon\\offline.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon2.addPixmap(QtGui.QPixmap("./icon\\online.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        icon2.addPixmap(QtGui.QPixmap("./icon\\offline.png"), QtGui.QIcon.Selected, QtGui.QIcon.Off)
        icon2.addPixmap(QtGui.QPixmap("./icon\\online.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        self.mode_button.setIcon(icon2)
        self.mode_button.setIconSize(QtCore.QSize(100, 100))
        self.mode_button.setCheckable(True)
        self.mode_button.setObjectName("mode_button")
        self.line_9 = QtWidgets.QFrame(self.frame_2)
        self.line_9.setGeometry(QtCore.QRect(220, 90, 131, 41))
        self.line_9.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_9.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_9.setObjectName("line_9")
        self.line_2 = QtWidgets.QFrame(self.frame_2)
        self.line_2.setGeometry(QtCore.QRect(430, 210, 81, 31))
        self.line_2.setStyleSheet("color: black\n"
"")
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.line_5 = QtWidgets.QFrame(self.frame_2)
        self.line_5.setGeometry(QtCore.QRect(350, 210, 21, 31))
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.log_path = QtWidgets.QPushButton(self.frame_2)
        self.log_path.setGeometry(QtCore.QRect(600, 330, 81, 81))
        self.log_path.setStyleSheet(" QPushButton {\n"
"     background-color: transparent;\n"
"     border:none\n"
" }\n"
" QPushButton:pressed {\n"
"     background-color: rgb(220,220,220);\n"
"     border:none     \n"
" }\n"
"")
        self.log_path.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("./icon\\logging_file.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.log_path.setIcon(icon3)
        self.log_path.setIconSize(QtCore.QSize(80, 80))
        self.log_path.setObjectName("log_path")
        self.print_data = QtWidgets.QPushButton(self.frame_2)
        self.print_data.setGeometry(QtCore.QRect(600, 50, 81, 81))
        self.print_data.setStyleSheet(" QPushButton {\n"
"     background-color: transparent;\n"
"     border:none\n"
" }\n"
" QPushButton:pressed {\n"
"     background-color: rgb(220,220,220);     \n"
" }\n"
"")
        self.print_data.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("./icon\\TRACE.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.print_data.setIcon(icon4)
        self.print_data.setIconSize(QtCore.QSize(70, 70))
        self.print_data.setObjectName("print_data")
        self.CAN_bus = QtWidgets.QPushButton(self.frame_2)
        self.CAN_bus.setGeometry(QtCore.QRect(100, 240, 149, 70))
        self.CAN_bus.setStyleSheet(" QPushButton#CAN_bus {\n"
"     background-color: transparent;\n"
"     border:none\n"
" }\n"
" QPushButton#CAN_bus:pressed {\n"
"     background-color: rgb(220,220,220);     \n"
"     border:none\n"
" }\n"
"")
        self.CAN_bus.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("./icon\\CAN.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.CAN_bus.setIcon(icon5)
        self.CAN_bus.setIconSize(QtCore.QSize(70, 70))
        self.CAN_bus.setObjectName("CAN_bus")
        self.lineEdit_0 = QtWidgets.QLineEdit(self.frame_2)
        self.lineEdit_0.setGeometry(QtCore.QRect(110, 323, 149, 20))
        self.lineEdit_0.setStyleSheet("background-color: transparent;\n"
"border: none")
        self.lineEdit_0.setObjectName("lineEdit_0")
        self.lineEdit_1 = QtWidgets.QLineEdit(self.frame_2)
        self.lineEdit_1.setGeometry(QtCore.QRect(110, 350, 149, 20))
        self.lineEdit_1.setStyleSheet("background-color: transparent;\n"
"border: none")
        self.lineEdit_1.setObjectName("lineEdit_1")
        self.line_10 = QtWidgets.QFrame(self.frame_2)
        self.line_10.setGeometry(QtCore.QRect(290, 300, 61, 41))
        self.line_10.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_10.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_10.setObjectName("line_10")
        self.label_2 = QtWidgets.QLabel(self.frame_2)
        self.label_2.setGeometry(QtCore.QRect(94, 136, 91, 20))
        self.label_2.setObjectName("label_2")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.frame_2)
        self.lineEdit_2.setGeometry(QtCore.QRect(170, 140, 151, 16))
        self.lineEdit_2.setStyleSheet("background-color: transparent;\n"
"border: none")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.line_11 = QtWidgets.QFrame(self.frame_2)
        self.line_11.setGeometry(QtCore.QRect(680, 350, 81, 41))
        self.line_11.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_11.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_11.setObjectName("line_11")
        self.sav_data = QtWidgets.QPushButton(self.frame_2)
        self.sav_data.setGeometry(QtCore.QRect(770, 330, 81, 81))
        self.sav_data.setStyleSheet(" QPushButton {\n"
"     background-color: transparent;\n"
"     border:none\n"
" }\n"
" QPushButton:pressed {\n"
"     background-color: rgb(220,220,220);     \n"
"     border:none\n"
" }\n"
"")
        self.sav_data.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("./icon\\save.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.sav_data.setIcon(icon6)
        self.sav_data.setIconSize(QtCore.QSize(60, 60))
        self.sav_data.setObjectName("sav_data")
        self.add_bus_save = QtWidgets.QPushButton(self.frame_2)
        self.add_bus_save.setGeometry(QtCore.QRect(500, 350, 51, 41))
        self.add_bus_save.setStyleSheet("background-color: transparent;\n"
"border:none\n"
"\n"
"")
        self.add_bus_save.setText("")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("./icon\\add_bus.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.add_bus_save.setIcon(icon7)
        self.add_bus_save.setIconSize(QtCore.QSize(20, 20))
        self.add_bus_save.setCheckable(True)
        self.add_bus_save.setObjectName("add_bus_save")
        self.line_12 = QtWidgets.QFrame(self.frame_2)
        self.line_12.setGeometry(QtCore.QRect(540, 350, 41, 41))
        self.line_12.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_12.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_12.setObjectName("line_12")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.frame_2)
        self.lineEdit_3.setGeometry(QtCore.QRect(590, 420, 141, 16))
        self.lineEdit_3.setStyleSheet("background-color: transparent;\n"
"border: none")
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.add_bus_graphic = QtWidgets.QPushButton(self.frame_2)
        self.add_bus_graphic.setGeometry(QtCore.QRect(500, 200, 51, 41))
        self.add_bus_graphic.setStyleSheet("background-color: transparent;\n"
"border:none\n"
"\n"
"")
        self.add_bus_graphic.setText("")
        self.add_bus_graphic.setIcon(icon7)
        self.add_bus_graphic.setIconSize(QtCore.QSize(20, 20))
        self.add_bus_graphic.setCheckable(True)
        self.add_bus_graphic.setObjectName("add_bus_graphic")
        self.add_bus_trace = QtWidgets.QPushButton(self.frame_2)
        self.add_bus_trace.setGeometry(QtCore.QRect(500, 70, 51, 41))
        self.add_bus_trace.setStyleSheet("background-color: transparent;\n"
"border:none\n"
"\n"
"")
        self.add_bus_trace.setText("")
        self.add_bus_trace.setIcon(icon7)
        self.add_bus_trace.setIconSize(QtCore.QSize(20, 20))
        self.add_bus_trace.setCheckable(True)
        self.add_bus_trace.setObjectName("add_bus_trace")
        self.line_16 = QtWidgets.QFrame(self.frame_2)
        self.line_16.setGeometry(QtCore.QRect(470, 70, 41, 41))
        self.line_16.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_16.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_16.setObjectName("line_16")
        self.line_15 = QtWidgets.QFrame(self.frame_2)
        self.line_15.setGeometry(QtCore.QRect(540, 70, 41, 41))
        self.line_15.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_15.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_15.setObjectName("line_15")
        self.trace_graphic = QtWidgets.QPushButton(self.frame_2)
        self.trace_graphic.setGeometry(QtCore.QRect(600, 180, 81, 81))
        self.trace_graphic.setStyleSheet(" QPushButton {\n"
"     background-color: transparent;\n"
"     border:none\n"
" }\n"
" QPushButton:pressed {\n"
"     background-color: rgb(220,220,220);     \n"
" }\n"
"")
        self.trace_graphic.setText("")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("./icon\\Graphic.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.trace_graphic.setIcon(icon8)
        self.trace_graphic.setIconSize(QtCore.QSize(70, 70))
        self.trace_graphic.setObjectName("trace_graphic")
        self.line_3 = QtWidgets.QFrame(self.frame_2)
        self.line_3.setGeometry(QtCore.QRect(540, 210, 41, 31))
        self.line_3.setStyleSheet("color: black\n"
"")
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.frame_3 = QtWidgets.QFrame(self.centralwidget)
        self.frame_3.setGeometry(QtCore.QRect(450, 20, 481, 71))
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.Run_3 = QtWidgets.QPushButton(self.frame_3)
        self.Run_3.setGeometry(QtCore.QRect(420, 10, 44, 51))
        self.Run_3.setMinimumSize(QtCore.QSize(10, 10))
        self.Run_3.setStyleSheet(" QPushButton#Run_3 {\n"
"     background-color: transparent;\n"
"     border:none\n"
" }\n"
" QPushButton#Run_3:pressed {\n"
"     background-color: rgb(220,220,220);    \n"
"     border:none \n"
" }\n"
"")
        self.Run_3.setText("")
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("./icon\\clean.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Run_3.setIcon(icon9)
        self.Run_3.setIconSize(QtCore.QSize(50, 50))
        self.Run_3.setObjectName("Run_3")
        self.Run_2 = QtWidgets.QPushButton(self.frame_3)
        self.Run_2.setGeometry(QtCore.QRect(360, 10, 44, 51))
        self.Run_2.setMinimumSize(QtCore.QSize(10, 10))
        self.Run_2.setStyleSheet("QPushButton {\n"
"     background-color: transparent;\n"
"     border:none\n"
" }\n"
" QPushButton:pressed {\n"
"     background-color: rgb(220,220,220);  \n"
"     border:none \n"
" }\n"
"")
        self.Run_2.setText("")
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap("./icon\\pause-button.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Run_2.setIcon(icon10)
        self.Run_2.setIconSize(QtCore.QSize(45, 45))
        self.Run_2.setObjectName("Run_2")
        self.Run = QtWidgets.QPushButton(self.frame_3)
        self.Run.setGeometry(QtCore.QRect(290, 10, 44, 51))
        self.Run.setMinimumSize(QtCore.QSize(10, 10))
        self.Run.setStyleSheet(" QPushButton#Run {\n"
"     background-color: transparent;\n"
"     border:none\n"
" }\n"
" QPushButton#Run:pressed {\n"
"     background-color: rgb(220,220,220);    \n"
"     border:none \n"
" }\n"
"")
        self.Run.setText("")
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap("./icon\\toppng(1).png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Run.setIcon(icon11)
        self.Run.setIconSize(QtCore.QSize(40, 40))
        self.Run.setObjectName("Run")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Addfile.setToolTip(_translate("MainWindow", "Add DBC path"))
        self.label.setText(_translate("MainWindow", "DBC path:"))
        self.log.setToolTip(_translate("MainWindow", "load logging file"))
        self.log_path.setToolTip(_translate("MainWindow", "choose logging path"))
        self.log_path.setWhatsThis(_translate("MainWindow", "<html><head/><body><p><br/></p></body></html>"))
        self.print_data.setToolTip(_translate("MainWindow", "open message displayer"))
        self.CAN_bus.setToolTip(_translate("MainWindow", "initial CAN bus"))
        self.lineEdit_0.setText(_translate("MainWindow", "CAN 0    500 kbaud"))
        self.lineEdit_1.setText(_translate("MainWindow", "CAN 1    500 kbaud"))
        self.label_2.setText(_translate("MainWindow", "logging file:"))
        self.sav_data.setToolTip(_translate("MainWindow", "save logging file"))
        self.sav_data.setWhatsThis(_translate("MainWindow", "<html><head/><body><p><br/></p></body></html>"))
        self.trace_graphic.setToolTip(_translate("MainWindow", "show graphics"))
        self.Run_3.setToolTip(_translate("MainWindow", "clean all"))
        self.Run_2.setToolTip(_translate("MainWindow", "stop"))
        self.Run.setToolTip(_translate("MainWindow", "run"))
