import sys
from PyQt5.QtGui import QIcon, QTextCursor
from PyQt5.QtCore import Qt,QThread,QObject,pyqtSignal,QMetaType
from PyQt5.QtWidgets import QProgressBar, QWidget, QTextEdit, QApplication, QPushButton, QComboBox, QDialog, QFileDialog, QFormLayout,QLineEdit, QGridLayout, QCheckBox, QLabel, QGroupBox, QVBoxLayout, QHBoxLayout

import ssplib
from time import sleep
from serial.serialutil import SerialException
import serialutils
import serial
class Worker(QObject):
    def __init__(self,sendBut,log,ser,pBar):
        super(Worker, self).__init__()
        self.sendBut = sendBut
        self.ser = ser
        self.log = log
        self.pBar = pBar

    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def run(self):
        sendBut.setEnabled(False)

        all_bytes = []

        temp_data = []
        data_data = []
        i=0
        updatePBar = 0

        fnames = ["GyroX.bias.aprox", "GyroX.scale.aprox", "GyroX.grad.aprox",
                    "GyroY.bias.aprox", "GyroY.scale.aprox", "GyroY.grad.aprox",
                    "GyroZ.bias.aprox", "GyroZ.scale.aprox", "GyroZ.grad.aprox",
                    "AccelX.bias.aprox", "AccelX.scale.aprox",
                    "AccelY.bias.aprox", "AccelY.scale.aprox",
                    "AccelZ.bias.aprox", "AccelZ.scale.aprox"]
        try:
            getattr(self.ser, 'open')
        except AttributeError:
            self.log.append("COM не выбран")
        else:
            self.ser.write( bytearray(ssplib.SSP_PUT(100,0,99,[0xA5,0xA5,0xA5,0xA5])))
            sleep(1)
            self.log.append("Разрешение записи ПНСК40-044")
            self.ser.write( bytearray(ssplib.SSP_PUT(100,0,37,[0x65,0x64,0x1F,0x00])))
            sleep(1)
            self.log.append("Разрешение работы ПНСК40-014 X")
            self.ser.write( bytearray(ssplib.SSP_PUT(100,0,38,[0x66,0x64,0x1F,0x00])))
            sleep(1)
            self.log.append("Разрешение работы ПНСК40-014 Y")
            self.ser.write( bytearray(ssplib.SSP_PUT(100,0,39,[0x67,0x64,0x1F,0x00])))
            sleep(1)
            self.log.append("Разрешение работы ПНСК40-014 Z")

            self.ser.write( bytearray(ssplib.SSP_PUT(101,0,99,[0xA5,0xA5,0xA5,0xA5])))
            sleep(1)
            self.log.append("Разрешение записи ПНСК40-014 X")
            self.ser.write( bytearray(ssplib.SSP_PUT(102,0,99,[0xA5,0xA5,0xA5,0xA5])))
            sleep(1)
            self.log.append("Разрешение записи ПНСК40-014 Y")
            self.ser.write( bytearray(ssplib.SSP_PUT(103,0,99,[0xA5,0xA5,0xA5,0xA5])))
            sleep(1)
            self.log.append("Разрешение записи ПНСК40-014 Z")

            for num_files in range(len(fnames)):
                sspAdr = 0
                selfAdr = 0
                fname = dir + "/" + fnames[num_files]


                selfAdr,sspAdr = ssplib.guess(fname)

                try:
                    with open(fname) as f:
                        self.log.append("Отправляю " + fnames[num_files])
                        data = f.readlines()
                        for line in data:
                            temp_data.append(line.strip().split("  ")[1])
                            data_data.append(line.strip().split("  ")[3])
                            #self.log.append(str(temp_data[i]) + "\t" + str(data_data[i]))

                            temp_data[i] = 100 * float(temp_data[i])

                            all_bytes.extend (int(temp_data[i]).to_bytes(2, byteorder='little',signed=True))
                            all_bytes.extend (int(data_data[i]).to_bytes(2, byteorder='little',signed=True))
                            i = i + 1#Обнуление?

                        get = []

                        send = ssplib.SSP_WRITE(selfAdr,0,sspAdr,all_bytes)

                        if (len(send) > 347):
                            self.log.append("Количество точек превышает 12\n")

                            continue
                        self.ser.write( bytearray(ssplib.SSP_PING(selfAdr,0)))
                        sleep(1)
                        self.ser.write( bytearray(ssplib.SSP_PING(selfAdr,0)))
                        sleep(1)
                        self.ser.write( bytearray(ssplib.SSP_PING(selfAdr,0)))
                        sleep(1)


                        self.ser.write( bytearray( send ) )
                        sleep(1)

                        #self.log.append("Отправлено " + str(len(send)) + " байт на " + str(selfAdr) + " ssp адрес " + str(sspAdr))

                        all_bytes = []

                        f.close()

                except OSError:
                    self.log.append("Файл " + fname + " не найден")

            self.finished.emit()

class MainWindow(QDialog):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
# INTERFACE
        self.setWindowTitle('PNSK40-044')
        self.setFixedWidth(300)
        self.setWindowIcon(QIcon('icon.ico'))
        global log
        log = QTextEdit()
        log.setReadOnly(True)


        global pBar
        pBar = QProgressBar(self)
        pBar.setMaximum(100)
        pBar.setTextVisible(False)

        grid = QGridLayout()
        grid.addWidget(self.comGroup(), 0, 0)
        grid.addWidget(self.Table(), 0, 1)
        grid.addWidget(pBar, 2, 0, 1, 2)
        grid.addWidget(log, 3, 0, 2, 2)#fromRow,  fromColumn,  rowSpan,  columnSpan
        self.setLayout(grid)
        log.append("выберите скорость и COM")




    def comGroup(self):
        groupbox = QGroupBox('COM')

        ports_list = QComboBox()
        for portname in serialutils.enumerate_serial_ports():
            ports_list.addItem(portname)

        global baud
        global conBut
        baud = QComboBox()
        baud.addItems(["115200", "460800", "921600"])

        conBut = QPushButton('Connected')
        conBut.setEnabled(False)
        conBut.setStyleSheet('background-color: lightgray')



        flay = QFormLayout()
        flay.addRow(QLabel("Baud"),baud)
        flay.addRow(QLabel("Port:"),ports_list)


        vbox = QVBoxLayout()
        vbox.addLayout(flay, 1)
        vbox.addWidget(conBut)
        vbox.addStretch(2)

        groupbox.setLayout(vbox)

        conBut.clicked.connect(self.con_clicked)
        ports_list.activated[str].connect(self.onActivated)
        return groupbox

    def Table(self):
        groupbox = QGroupBox('Папка')

        global table

        fileBut = QPushButton("Обзор")
        global sendBut
        sendBut = QPushButton("Отправить")
        sendBut.setEnabled(False)

        flay = QFormLayout()
        #flay.addRow(QLabel("Множитель:"), multLine)
        flay.addRow(QLabel("Aprox files:"),fileBut)

        vbox = QVBoxLayout()
        vbox.addLayout(flay, 1)
        vbox.addWidget(sendBut)
        vbox.addStretch(2)
        groupbox.setLayout(vbox)
        fileBut.clicked.connect(self.getfile)
        sendBut.clicked.connect(self.sendmes)



        return groupbox
# END INTERFACE

    def getfile(self):
        global dir

        dir = QFileDialog.getExistingDirectory(self, "Выберите папку Approx", 'c://', QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        log.append("выбрана папка "+str(dir))
        sendBut.setEnabled(True)

    def reportProgress(self, n):
        pBar.setValue(n)
        return n+1


    def sendmes(self):

        self.thread = QThread() #Create a QThread object
        self.worker = Worker(sendBut,log,ser,pBar)  #Create a worker object
        self.worker.moveToThread(self.thread) #move worker to thread

        self.thread.started.connect(self.worker.run)#connect signals
        self.worker.progress.connect(self.reportProgress)
        self.worker.finished.connect(self.thread.quit)
        self.thread.finished.connect(lambda: sendBut.setEnabled(True))
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start() #Start the thread



#close opened port
    def con_clicked (self):
        if self.serCheck == 1:
            ser.close()
            log.append("COM отключен")
            conBut.setStyleSheet("background-color: lightgray")
            conBut.setEnabled(False)

    def onActivated(self, text):
        cur_item = text
        if cur_item is not None:
            fullname = serialutils.full_port_name(str(cur_item))

            try:
                global ser
                ser = serial.Serial( fullname, int(baud.currentText()), timeout=1 )
                self.serCheck = 1
                ser.close()
                ser.open()
                log.append("%s подключен" % cur_item + " " + baud.currentText() )
                log.append("Выберите папку с .approx файлами с помощью кнопки \"Обзор\"\n")
                conBut.setStyleSheet("background-color: lime")
                conBut.setEnabled(True)
            except (SerialException): log.append('Не смог открыть %s' % (cur_item))


if __name__ == "__main__":
    app = QApplication([])
    form = MainWindow()
    form.show()
    app.setWindowIcon(QIcon('icon.ico'))
    form.setWindowIcon(QIcon('icon.ico'))
    app.exec_()
