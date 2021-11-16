import sys, sqlite3
from math import sin, cos, pi
import time
import datetime
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QListWidget, QMessageBox
from PyQt5.QtWidgets import QLCDNumber, QLabel, QTabWidget, QListWidgetItem, QListWidget, QTableWidget, QTableWidgetItem
from threading import Timer
from PyQt5.QtCore import QTimer, QRect, QPoint
from PyQt5.QtGui import QIcon, QPainter, QPixmap, QPen, QColor, QPalette, QBrush
import sqlite3
from alr_window import Alarm_window


class QStrelka(QLabel):
    def __init__(self, par):
        super(QStrelka, self).__init__(par)
        self.sec = 0
        self.min = 0
        self.hour = 0

    def paintEvent(self, a0: QtGui.QPaintEvent):
        # рисуем стрелки
        p = QPainter(self)

        tt = QPixmap("hen.png")

        # mask = tt.createMaskFromColor(QColor(255, 255, 255), QtCore.Qt.MaskInColor)
        rect = QRect(0, 0, self.width(), self.height())
        p.drawPixmap(rect, tt)  # mask, mask.rect())

        # определяем координаты центра нашего виджета
        yc = int(self.height() / 2)
        xc = int(self.width() / 2)

        # определяем длину стрелок
        l_min_s = float(xc) * 0.7
        l_sec_s = float(xc) * 0.9
        l_hour_s = float(xc) * 0.5

        # Расчитываем координаты минутной стрелки
        # 2*pi/60 =6 градусов между положениями стрелки
        ugol_min = (2 * pi / 60) * self.min
        # координата х конца стредки смещена относительно центра на длинна_стредки*sin(углв стрелки)
        # тоже самое координата Y только косинус
        min_x = int(l_min_s * sin(ugol_min))
        min_y = int(l_min_s * cos(ugol_min))

        # рисуем минутную стрелку

        p.setPen(QPen(QtGui.QColor(0, 0, 0), 3, QtCore.Qt.SolidLine))

        p.drawLine(xc, yc, xc + min_x, yc - min_y)

        # все тоже самое для секундной стрелки и часовой
        ugol_sec = (2 * pi / 60) * self.sec
        sec_x = int(l_sec_s * sin(ugol_sec))
        sec_y = int(l_sec_s * cos(ugol_sec))

        p.setPen(QPen(QtGui.QColor(0, 0, 0), 1, QtCore.Qt.SolidLine))
        p.drawLine(xc, yc, xc + sec_x, yc - sec_y)

        # старая версия часовой стрелки
        ugol_hour = (2 * pi / 12) * self.hour + ((2 * pi / 12) * self.min / 60)
        hour_x = int(l_hour_s * sin(ugol_hour))
        hour_y = int(l_hour_s * cos(ugol_hour))
        p.setPen(QPen(QtGui.QColor(0, 0, 0), 3, QtCore.Qt.SolidLine))
        p.drawLine(xc, yc, xc + hour_x, yc - hour_y)

        # новая версия часовой стрелки
        # надо повернуть изображение сnрелки на угол относительно точки центра стрелки и вывести его в центре

        # hr_bmp = QPixmap("hour_strelka.png")
        # new_hr = QPixmap(hr_bmp.size())
        # new_hr.fill(QColor(0, 0, 0, 0))

        # ph = QPainter(new_hr)
        # ph.translate(hr_bmp.height() / 2, hr_bmp.height() / 2)
        # ph.rotate(ugol_sec*57)
        # ph.translate(hr_bmp.height() / -2, hr_bmp.height() / -2)
        # ph.drawPixmap(0,0, hr_bmp)
        # ph.end()

        # mask2 = new_hr.createMaskFromColor(QColor(0, 0, 0), QtCore.Qt.MaskOutColor)

        # p.drawPixmap(rect,new_hr)


class SETTINGS(QWidget):
    def __init__(self):
        super(SETTINGS, self).__init__()
        self.initUI()
        self.showed = False
        self.col = False

    def initUI(self):
        self.setGeometry(1020, 300, 220, 400)
        self.setWindowTitle("Settings")
        self.setStyleSheet("background-color: rgb(50, 50, 50);")
        self.setStyleSheet("background-image: paku.jpg;")

        self.texted = QLabel(self)
        self.texted.setText('Для настройки времени,')
        self.texted1 = QLabel(self)
        self.texted1.move(0, 10)
        self.texted1.setText('перейдите в настройки устройстова')

    def smen(self):
        if self.col == True:
            self.col = False
            self.setStyleSheet("background-color: rgb(50, 50, 50);")
        else:
            self.col = True
            self.setStyleSheet("background-color: rgb(250, 250, 250);")
            self.clay.setStyleSheet('QPushButton {background-color: gray; color: black;}')


class MAIN_WINDOW1(QWidget):
    def __init__(self):
        super(MAIN_WINDOW1, self).__init__()

        self.database_name = "clockbase.db"
        self.con = sqlite3.connect(self.database_name)
        self.cur = self.con.cursor()

        self.initUI()
        self.timer = QTimer()
        self.timer.timeout.connect(self.tik)
        self.timer.start(200)
        self.a = 0
        self.mode = 0
        self.clock_mode = 0  # режим отображения часов 0 - цифры,  1 - стрелочные
        self.tw_run = False
        self.timer_data = datetime.datetime(2000, 1, 1, 0, 0, 0)
        self.button_size = 20
        self.f = 0
        self.s = 0
        self.proverty = False

        self.tw_timer = QTimer()
        self.tw_timer.setInterval(1000)
        self.tw_timer.timeout.connect(self.tw_update)

        self.countdown_timer = QTimer()
        self.countdown_timer.setInterval(1000)
        self.countdown_timer.timeout.connect(self.ctw_update)
        self.sized = 0
        #  mode режим работы
        #  0  - часы
        #  2  - таймер
        #  3  - будильник

    def tw_update(self):
        self.timer_data += datetime.timedelta(seconds=1)
        self.tw.setText(str(self.timer_data.strftime("%H:%M:%S")))

    def ctw_update(self):
        hour_t = int(self.hour_input.text())
        min_t = int(self.min_input.text())
        sec_t = int(self.sec_input.text())
        next_time = datetime.datetime(year=2000, month=1, day=1, hour=hour_t, minute=min_t,
                                      second=sec_t) - datetime.timedelta(seconds=1)
        self.hour_input.setText(next_time.strftime("%H"))
        self.min_input.setText(next_time.strftime("%M"))
        self.sec_input.setText(next_time.strftime("%S"))
        if sec_t == 0 and min_t == 0 and hour_t == 0:
            self.countdown_timer.stop()
            print('Alarm!!')

    def initUI(self):
        self.setGeometry(300, 300, 700, 400)
        self.setWindowTitle("PROJECT 'Smart Watch'")
        self.setAutoFillBackground(False)
        self.palf = QPalette()
        self.palf.setBrush(QPalette.Background, QBrush(QPixmap("DA.jpg")))
        self.setPalette(self.palf)

        self.settings = QPushButton(self)
        self.settings.resize(50, 50)
        self.settings.move(650, 10)
        self.settings.setIcon(QIcon('sett.png'))
        self.settings.setFont(QtGui.QFont("Times", 25))
        self.settings.pressed.connect(self.open_settings)
        self.settings.setCheckable(True)

        self.main_watch = QLabel(self)
        # self.main_watch.resize(500, 500)
        self.main_watch.setFont(QtGui.QFont("Times", 45))
        self.main_watch.move(252, 240)
        self.main_watch.setText("00:00")

        self.clock = QStrelka(self)
        self.clock.move(240, 30)
        self.clock.resize(200, 200)
        # self.clock.hide()

        # self.blist=QListbox()
        # self.blist.move(0,0)
        # self.blist.resize(300,300)
        # self.blist.addItem("Test")
        # self.blist.addItem("Test2")

        self.clpro = QLabel()
        self.clpro.move(100, 100)
        self.clpro.resize(100, 100)
        self.clpro.setFont(QtGui.QFont("Times", 45))
        # self.clpro.setText(str(self.get_result()))

        self.tw = QLabel(self)
        # self.tw.resize(500, 500)
        self.tw.setFont(QtGui.QFont("Times", 45))
        self.tw.move(220, 130)
        self.tw.hide()
        self.tw.setText("00:00:00")

        self.tw_ss_btn = QPushButton(self)
        self.tw_ss_btn.resize(100, 50)
        self.tw_ss_btn.move(280, 225)
        self.tw_ss_btn.setText("START")
        self.tw_ss_btn.setFont(QtGui.QFont("Times", 25))
        self.tw_ss_btn.pressed.connect(self.tw_ss_press)
        self.tw_ss_btn.setCheckable(True)
        self.tw_ss_btn.hide()

        self.alarm_button = QPushButton(self)
        self.alarm_button.resize(60, 60)
        self.alarm_button.move(160, 330)
        self.alarm_button.setIcon(QIcon('ture.png'))
        self.alarm_button.setFont(QtGui.QFont("Times", 125))
        self.alarm_button.clicked.connect(self.allared)

        self.Timerpage_button = QPushButton(self)
        self.Timerpage_button.resize(60, 60)
        self.Timerpage_button.move(30, 330)
        self.Timerpage_button.setIcon(QIcon('91e.png'))
        self.Timerpage_button.setFont(QtGui.QFont("Times", 125))
        self.Timerpage_button.pressed.connect(self.TimerShow)

        self.puls_button = QPushButton(self)
        self.puls_button.resize(260, 60)
        self.puls_button.move(200, 130)
        self.puls_button.setText('Connecting with sourses')
        self.puls_button.setFont(QtGui.QFont("Times", 12))
        self.puls_button.clicked.connect(self.pulsed)
        self.puls_button.hide()

        self.pre_button = QPushButton(self)
        self.pre_button.resize(260, 60)
        self.pre_button.move(200, 210)
        self.pre_button.setText('Functionality')
        self.pre_button.setFont(QtGui.QFont("Times", 12))
        self.pre_button.clicked.connect(self.presh)
        self.pre_button.hide()

        self.pye = QLabel(self)
        self.pye.move(470, 130)
        self.pye.resize(70, 40)
        self.pye.setText('Normal')
        self.pye.setFont(QtGui.QFont("Times", 15))
        self.pye.hide()

        self.bo = QLabel(self)
        self.bo.move(470, 130)
        self.bo.resize(70, 210)
        self.bo.setText('Normal')
        self.bo.setFont(QtGui.QFont("Times", 15))
        self.bo.hide()

        self.bud = QPushButton(self)
        self.bud.resize(60, 60)
        self.bud.move(420, 330)
        self.bud.setIcon(QIcon('le.png'))
        self.bud.setFont(QtGui.QFont("Times", 125))
        self.bud.pressed.connect(self.moded)

        self.applied = QPushButton(self)
        self.applied.resize(190, 40)
        self.applied.move(235, 220)
        self.applied.setText('START')
        self.applied.setFont(QtGui.QFont("Times", 25))
        self.applied.pressed.connect(self.appilation)
        self.applied.hide()

        self.hour_input = QLineEdit(self)
        self.hour_input.move(215, 140)
        self.hour_input.resize(70, 40)
        self.hour_input.setText('00')
        self.hour_input.setFont(QtGui.QFont("Times", 25))
        self.hour_input.hide()

        self.min_input = QLineEdit(self)
        self.min_input.move(300, 140)
        self.min_input.resize(70, 40)
        self.min_input.setText('00')
        self.min_input.setFont(QtGui.QFont("Times", 25))
        self.min_input.hide()

        self.sec_input = QLineEdit(self)
        self.sec_input.move(385, 140)
        self.sec_input.resize(70, 40)
        self.sec_input.setText('00')
        self.sec_input.setFont(QtGui.QFont("Times", 25))
        self.sec_input.hide()

        self.p = QLabel(self)
        self.p.move(285, 140)
        self.p.resize(70, 40)
        self.p.setText(':')
        self.p.setFont(QtGui.QFont("Times", 25))
        self.p.hide()

        self.p1 = QLabel(self)
        self.p1.move(370, 140)
        self.p1.resize(70, 40)
        self.p1.setText(':')
        self.p1.setFont(QtGui.QFont("Times", 25))
        self.p1.hide()

        self.hg = QLabel(self)
        self.hg.move(230, 170)
        self.hg.resize(70, 40)
        self.hg.setText('hours')
        self.hg.setFont(QtGui.QFont("Times", 15))
        self.hg.hide()

        self.ph = QLabel(self)
        self.ph.move(305, 170)
        self.ph.resize(70, 40)
        self.ph.setText('minute')
        self.ph.setFont(QtGui.QFont("Times", 15))
        self.ph.hide()

        self.sec = QLabel(self)
        self.sec.move(390, 170)
        self.sec.resize(70, 40)
        self.sec.setText('second')
        self.sec.setFont(QtGui.QFont("Times", 15))
        self.sec.hide()

        self.health = QPushButton(self)
        self.health.resize(60, 60)
        self.health.move(570, 330)
        self.health.setIcon(QIcon('black.png'))
        self.health.setFont(QtGui.QFont("Times", 125))
        self.health.clicked.connect(self.ds)

        self.main = QPushButton(self)
        self.main.resize(20, 20)
        self.main.move(320, 350)
        self.main.setIcon(QIcon('ts.png'))
        self.main.setFont(QtGui.QFont("Times", 125))
        self.main.clicked.connect(self.main_press)

        # layout = QGridLayout()

        # layout.addWidget(self.main_watch, 0, 0, 1, 2)
        # layout.addWidget(self.startBtn, 1, 0)
        # layout.addWidget(self.stopBtn, 1, 1)

        # self.setLayout(layout)
        # self.blist = QTabWidget(self)
        # self.blist.resize(100,100)
        # self.blist.move(200,0)

        # self.alarms = QListWidget(self)
        self.alarms = QTableWidget(self)
        self.alarms.resize(550, 220)
        self.alarms.move(50, 50)
        # self.alarms.setText('START')
        self.alarms.setFont(QtGui.QFont("Times", 15))
        # self.alarms.pressed.connect(self.appilation)
        self.alarms.hide()
        # self.alarms.se(False)
        self.alarms.itemDoubleClicked.connect(self.alr_edit)
        # self.alarms.itemClicked.connect(self.alr_edit)
        # self.alarms.doubleClicked.connect(self.alr_edit)
        self.get_result()

        self.alrm_add = QPushButton(self)
        self.alrm_add.resize(100, 30)
        self.alrm_add.move(150, 275)
        self.alrm_add.setText("Добавить")
        self.alrm_add.setFont(QtGui.QFont("Times", 15))
        self.alrm_add.clicked.connect(self.alr_add)
        self.alrm_add.hide()

        self.alrm_del = QPushButton(self)
        self.alrm_del.resize(100, 30)
        self.alrm_del.move(450, 275)
        self.alrm_del.setFont(QtGui.QFont("Times", 15))
        self.alrm_del.setText("Удалить")
        self.alrm_del.clicked.connect(self.alr_del)
        self.alrm_del.hide()

        self.sbros = QPushButton(self)
        self.sbros.resize(60, 30)
        self.sbros.move(215, 245)
        self.sbros.setIcon(QIcon('db.png'))
        self.sbros.setFont(QtGui.QFont("Times", 125))
        self.sbros.clicked.connect(self.sbrosed)
        self.sbros.hide()

    def alr_edit(self):

        row = self.alarms.selectedItems()[0].row()

        ids = self.alarms.item(row, 3).text()
        names = self.alarms.item(row, 0).text()
        times = self.alarms.item(row, 1).text()
        actives = self.alarms.item(row, 2).text()

        wa = Alarm_window()
        wa.name_edit.setText(names)
        wa.time_edit.setText(times)

        print(actives)
        if actives == 'Вкл':
            wa.active_check.setChecked(True)
        else:
            wa.active_check.setChecked(False)

        if wa.exec():
            # Добавление
            mod = {}
            mod["name"] = wa.name_edit.text()
            mod["time"] = wa.time_edit.text()
            if wa.active_check.isChecked() == True:
                mod["activate"] = 1

            else:
                mod["activate"] = 0

            que = "UPDATE id SET "
            que += ",".join([f"{key}='{mod.get(key)}'" for key in mod.keys()])
            que += " WHERE id = " + ids

            cur = self.con.cursor()
            cur.execute(que)
            self.con.commit()

            self.get_result()

    def alr_add(self):
        wa = Alarm_window()
        if wa.exec():
            # Добавление
            cur = self.con.cursor()
            if wa.active_check.isChecked:
                cur.execute(
                    "INSERT INTO id(name,time,activate) VALUES ('" + wa.name_edit.text() + "','" + wa.time_edit.text() + "',1)")
            else:
                cur.execute(
                    "INSERT INTO id(name,time,activate) VALUES ('" + wa.name_edit.text() + "','" + wa.time_edit.text() + "',0)")

            self.con.commit()
            self.get_result()

        else:
            print("cancel")

    def alr_del(self):
        rows = list(set([i.row() for i in self.alarms.selectedItems()]))
        ids = [self.alarms.item(i, 3).text() for i in rows]
        names = [self.alarms.item(i, 0).text() for i in rows]
        valid = QMessageBox.question(
            self, '', "Действительно удалить будильник(и) " + ",".join(names),
            QMessageBox.Yes, QMessageBox.No)
        if valid == QMessageBox.Yes:
            cur = self.con.cursor()
            cur.execute("DELETE FROM id WHERE id IN (" + ", ".join(
                '?' * len(ids)) + ")", ids)
            self.con.commit()
        self.get_result()

    def tw_ss_press(self):
        if self.tw_ss_btn.isChecked():
            self.tw_ss_btn.setText("START")
            self.tw_run = False
            self.tw_timer.stop()
        else:
            self.tw_ss_btn.setText("STOP")
            self.tw_run = True
            self.tw_timer.start()

    def main_press(self):
        self.mode = 0
        self.HideShow()

    def moded(self):
        self.mode = 3
        self.HideShow()

    def TimerShow(self):
        self.mode = 2
        self.HideShow()

    def HideShow(self):
        self.main_watch.hide()
        self.clock.hide()
        self.tw.hide()
        self.tw_ss_btn.hide()
        self.applied.hide()
        self.min_input.hide()
        self.hour_input.hide()
        self.sec_input.hide()
        self.p.hide()
        self.ph.hide()
        self.hg.hide()
        self.alarms.hide()
        self.pre_button.hide()
        self.puls_button.hide()
        self.bo.hide()
        self.pye.hide()
        self.sbros.hide()
        self.main.resize(60, 60)
        self.main.move(300, 330)
        self.health.resize(60, 60)
        self.health.move(570, 330)
        self.bud.resize(60, 60)
        self.bud.move(420, 330)
        self.Timerpage_button.resize(60, 60)
        self.Timerpage_button.move(30, 330)
        self.alarm_button.resize(60, 60)
        self.alarm_button.move(160, 330)
        self.sec.hide()
        self.p1.hide()
        self.alrm_add.hide()
        self.alrm_del.hide()

        if self.mode == 0:
            self.main_watch.show()
            self.clock.show()
            self.main.resize(20, 20)
            self.main.move(320, 350)
        elif self.mode == 2:
            self.tw.show()
            self.tw_ss_btn.show()
            self.sbros.show()
            self.Timerpage_button.resize(20, 20)
            self.Timerpage_button.move(50, 350)
        elif self.mode == 3:
            self.applied.show()
            self.min_input.show()
            self.hour_input.show()
            self.sec_input.show()
            self.sec.show()
            self.p.show()
            self.hg.show()
            self.ph.show()
            self.p1.show()
            self.bud.resize(20, 20)
            self.bud.move(440, 350)
        elif self.mode == 5:
            self.alarms.show()
            self.alarm_button.resize(20, 20)
            self.alarm_button.move(180, 350)
            self.alrm_add.show()
            self.alrm_del.show()

        elif self.mode == 333:
            self.pre_button.show()
            self.puls_button.show()
            self.bo.show()
            self.pye.show()
            self.health.resize(20, 20)
            self.health.move(590, 350)

    def tik(self):
        self.main_watch.setText(str(datetime.datetime.now().strftime("%H:%M")))
        self.clock.min = datetime.datetime.now().minute
        self.clock.sec = datetime.datetime.now().second
        self.clock.hour = datetime.datetime.now().hour

        # проверка срабатывания будильников
        c = self.con.cursor()
        result = c.execute("SELECT name,id FROM id WHERE activate = '1' and time = '" +
                           self.main_watch.text() + "'").fetchall()

        for e in result:
            QMessageBox.question(self, 'Будильник', "Внимание будильник " + e[0],
                                 QMessageBox.Ok)

            que = "UPDATE id SET activate = '0' WHERE id= " + str(e[1])
            print(que)
            c.execute(que)
            self.con.commit()

        self.clock.repaint()

    def open_settings(self):
        if self.a == 0:
            self.a = SETTINGS()
            self.a.show()
            self.a.showed = True
        else:
            if self.a.showed:
                self.a.hide()
                self.a.showed = False
            else:
                self.a.show()
                self.a.showed = True

    def get_result(self):

        result = self.cur.execute("""SELECT name,time,activate,id FROM id 
        ORDER BY time
        """).fetchall()
        self.alarms.clear()
        self.alarms.setRowCount(len(result))
        self.alarms.setColumnCount(4)
        self.alarms.setHorizontalHeaderItem(0, QTableWidgetItem(str("Наименование")))
        self.alarms.setHorizontalHeaderItem(1, QTableWidgetItem(str("Время")))
        self.alarms.setHorizontalHeaderItem(2, QTableWidgetItem(str("Включен")))
        self.alarms.setHorizontalHeaderItem(3, QTableWidgetItem(str("Идент")))

        self.alarms.setColumnWidth(0, 250)
        self.alarms.setColumnWidth(3, 5)
        self.alarms.verticalHeader().hide()

        i = 0
        for e in result:
            self.alarms.setItem(i, 0, QTableWidgetItem(str(e[0])))
            self.alarms.setItem(i, 1, QTableWidgetItem(str(e[1])))
            if e[2] == 1:
                self.alarms.setItem(i, 2, QTableWidgetItem(str("Вкл")))
            else:
                self.alarms.setItem(i, 2, QTableWidgetItem(str("Выкл")))

            self.alarms.setItem(i, 3, QTableWidgetItem(str(e[3])))
            i += 1
            # self.alarms.addItem(str(e[0])+"   "+str(e[1]))
        self.alarms.setColumnWidth(3, 5)

        self.con.commit()

    def appilation(self):
        self.f = int(self.hour_input.text())
        self.s = int(self.min_input.text())
        if self.proverty == True:
            self.applied.setText('START')
            self.proverty = False
            self.countdown_timer.stop()

        else:
            self.applied.setText('STOP')
            self.proverty = True
            self.countdown_timer.start()

    def allared(self):
        self.mode = 5
        self.HideShow()

    def ds(self):
        self.mode = 333
        self.HideShow()

    def pulsed(self):
        pass

    def presh(self):
        pass

    def sbrosed(self):
        self.timer_data = datetime.datetime(year=2000, month=1, day=1, hour=0, minute=0, second=0)
        self.tw.setText(str(self.timer_data.strftime("%H:%M:%S")))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MAIN_WINDOW1()
    w.show()
    sys.exit(app.exec_())