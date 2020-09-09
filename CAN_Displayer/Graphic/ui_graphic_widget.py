# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './icon/graphic_widget.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1108, 856)
        self.ToolFrame = QtWidgets.QFrame(Form)
        self.ToolFrame.setGeometry(QtCore.QRect(10, 10, 701, 41))
        self.ToolFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.ToolFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.ToolFrame.setObjectName("ToolFrame")
        self.toolButton = QtWidgets.QToolButton(self.ToolFrame)
        self.toolButton.setGeometry(QtCore.QRect(0, 0, 41, 41))
        self.toolButton.setObjectName("toolButton")
        self.toolButton_2 = QtWidgets.QToolButton(self.ToolFrame)
        self.toolButton_2.setGeometry(QtCore.QRect(50, 0, 41, 41))
        self.toolButton_2.setObjectName("toolButton_2")
        self.toolButton_3 = QtWidgets.QToolButton(self.ToolFrame)
        self.toolButton_3.setGeometry(QtCore.QRect(100, 0, 41, 41))
        self.toolButton_3.setObjectName("toolButton_3")
        self.toolButton_4 = QtWidgets.QToolButton(self.ToolFrame)
        self.toolButton_4.setGeometry(QtCore.QRect(150, 0, 41, 41))
        self.toolButton_4.setObjectName("toolButton_4")
        self.toolButton_5 = QtWidgets.QToolButton(self.ToolFrame)
        self.toolButton_5.setGeometry(QtCore.QRect(200, 0, 41, 41))
        self.toolButton_5.setObjectName("toolButton_5")
        self.toolButton_6 = QtWidgets.QToolButton(self.ToolFrame)
        self.toolButton_6.setGeometry(QtCore.QRect(250, 0, 41, 41))
        self.toolButton_6.setObjectName("toolButton_6")
        self.toolButton_7 = QtWidgets.QToolButton(self.ToolFrame)
        self.toolButton_7.setGeometry(QtCore.QRect(300, 0, 41, 41))
        self.toolButton_7.setObjectName("toolButton_7")
        self.toolButton_8 = QtWidgets.QToolButton(self.ToolFrame)
        self.toolButton_8.setGeometry(QtCore.QRect(350, 0, 41, 41))
        self.toolButton_8.setObjectName("toolButton_8")
        self.toolButton_9 = QtWidgets.QToolButton(self.ToolFrame)
        self.toolButton_9.setGeometry(QtCore.QRect(400, 0, 41, 41))
        self.toolButton_9.setObjectName("toolButton_9")
        self.horizontalLayoutWidget = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 60, 1091, 791))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.toolButton.setText(_translate("Form", "fit in"))
        self.toolButton_2.setText(_translate("Form", "zoom in"))
        self.toolButton_3.setText(_translate("Form", "zoom out"))
        self.toolButton_4.setToolTip(_translate("Form", "move signal down(Ctrl+Down)"))
        self.toolButton_4.setText(_translate("Form", "move down"))
        self.toolButton_4.setShortcut(_translate("Form", "Ctrl+Down"))
        self.toolButton_5.setToolTip(_translate("Form", "move signal up(Ctrl+Up)"))
        self.toolButton_5.setText(_translate("Form", "move up"))
        self.toolButton_5.setShortcut(_translate("Form", "Ctrl+Up"))
        self.toolButton_6.setToolTip(_translate("Form", "scroll left(Ctrl+Left)"))
        self.toolButton_6.setText(_translate("Form", "scroll left"))
        self.toolButton_6.setShortcut(_translate("Form", "Ctrl+Left"))
        self.toolButton_7.setToolTip(_translate("Form", "scroll right(Ctrl+Right)"))
        self.toolButton_7.setText(_translate("Form", "scroll right"))
        self.toolButton_7.setShortcut(_translate("Form", "Ctrl+Right"))
        self.toolButton_8.setText(_translate("Form", "seperate window"))
        self.toolButton_9.setText(_translate("Form", "export"))
