import sys

import time
from PyQt5 import QtGui, QtWidgets, uic
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication, QPushButton, QTextEdit, QVBoxLayout, QWidget, QMainWindow

qtCreatorFile = "MainGUI_2.ui"  # Enter file here.




class UpdateLogger(QObject):
    finished = pyqtSignal(str)
    update = pyqtSignal(str)


    def __init__(self, delay,parent = None):
        super().__init__(None)
        self.delay = delay
        self.threadName = QThread.currentThread().objectName()
        print("Thread Name is: " + self.threadName)
        self.threadId = int(QThread.currentThreadId())
        print("Thread ID is: {}".format(self.threadId))
    def running(self):
        x = 0
        print("Thread with Delay {} has started".format(self.delay))
        for x in range(10):
            app.processEvents()
            time.sleep(self.delay/5)
            self.update.emit("{}: Updated".format(self.threadId))
            print("Thread {} has emitted".format(self.threadName))

        self.finished.emit("{}: Finished".format(self.threadId))
        print("thread done")


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow,self).__init__()
        uic.loadUi(qtCreatorFile,self)
        self.threads = []
        mainThreadID = int(QThread.currentThread().currentThreadId())
        print("MainThread ID: {}".format(mainThreadID))
        QThread.currentThread().setObjectName("Thread_Main")

        self.pb1.clicked.connect(self.pb1Action)
        self.pb1Object = UpdateLogger(2)
        self.pb1Thread = QThread()
        self.pb1Thread.setObjectName("Thread_pb1")
        self.threads.append(self.pb1Thread)
        self.pb1Object.moveToThread(self.pb1Thread)
        self.pb1Object.finished.connect(self.updateLogger)
        self.pb1Object.update.connect(self.updateLogger)
        self.pb1Thread.started.connect(self.pb1Object.running)

        self.pb2.clicked.connect(self.pb2Action)
        self.pb2Object = UpdateLogger(3)
        self.pb2Thread = QThread()
        self.pb2Thread.setObjectName("Thread_pb2")
        self.threads.append(self.pb2Thread)
        self.pb2Object.moveToThread(self.pb2Thread)
        print(self.pb2Object.threadName)
        self.pb2Object.finished.connect(self.updateLogger)
        self.pb2Object.update.connect(self.updateLogger)
        self.pb2Thread.started.connect(self.pb2Object.running)

        for t in self.threads:
            print(t.objectName())

        self.pb3.clicked.connect(self.pb3Action)

    def pb1Action(self):
        self.pb1Thread.start()
        self.pb1.setEnabled(False)

    def pb1finished(self):
        self.tbLog.append("Finished: " + self.le1.text())
        self.pb1.setEnabled(True)

    def pb1update(self):
        app.processEvents()
        self.tbLog.append("U " + self.le1.text())

    def pb2Action(self):
        self.pb2Thread.start()
        self.pb2.setEnabled(False)

    def pb2finished(self):
        self.tbLog.append("Finished: " + self.le2.text())
        self.pb2.setEnabled(True)

    def pb2update(self):
        app.processEvents()
        self.tbLog.append("U " + self.le2.text())


    def pb3Action(self):

        self.tbLog.append(self.le3.text())

    @pyqtSlot(str)
    def updateLogger(self, txt="??????"):
        self.tbLog.append(txt)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
