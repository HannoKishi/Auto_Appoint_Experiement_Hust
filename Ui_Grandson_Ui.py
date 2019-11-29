# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'e:\python_project\qt_gui\Grandson_Ui.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(384, 275)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.centralwidget.setFont(font)
        self.centralwidget.setObjectName("centralwidget")
        self.stop_Button = QtWidgets.QPushButton(self.centralwidget)
        self.stop_Button.setGeometry(QtCore.QRect(30, 80, 131, 91))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.stop_Button.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/ac15.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.stop_Button.setIcon(icon)
        self.stop_Button.setIconSize(QtCore.QSize(64, 64))
        self.stop_Button.setObjectName("stop_Button")
        self.quit_Button = QtWidgets.QPushButton(self.centralwidget)
        self.quit_Button.setGeometry(QtCore.QRect(210, 80, 131, 91))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.quit_Button.setFont(font)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/a2_36.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.quit_Button.setIcon(icon1)
        self.quit_Button.setIconSize(QtCore.QSize(64, 64))
        self.quit_Button.setObjectName("quit_Button")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Running Scripts"))
        self.stop_Button.setText(_translate("MainWindow", "终止"))
        self.stop_Button.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.quit_Button.setText(_translate("MainWindow", "退出"))
        self.quit_Button.setShortcut(_translate("MainWindow", "Ctrl+Q"))
import button_rc
