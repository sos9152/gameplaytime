import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import pymysql

conn = pymysql.connect(host='localhost', user='root', password='1234', db='lol', charset='utf8')

curs = conn.cursor()
cur = conn.cursor()

form_class = uic.loadUiType("untitled.ui")[0]

class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.btn_1.clicked.connect(self.append)
        self.btn_2.clicked.connect(self.search)
        self.reset.clicked.connect(self.reset_btn)
    
    def append(self) :
        sql = "insert into game values('{0}','{1}','{2}','{3}')".format(self.game.currentText(), self.date_1.text(), self.name_1.text(), self.time_1.text())
        curs.execute(sql)
        conn.commit()
        QMessageBox.about(self, "message", "추가되었습니다!")
        self.name_1.clear()
        self.time_1.clear()

    def search(self) :
        sql = "select sum(time) from game where name = '{0}' and game = '{1}' group by game".format(self.name_1.text(), self.game.currentText())
        cur.execute(sql)
        rowss = cur.fetchone()
        self.playtime.append("총시간 : {} \n".format(rowss[0]))
        conn.commit()

        curs = conn.cursor(pymysql.cursors.DictCursor)
        sql = "select date, sum(time) from game where name = '{0}' and game = '{1}' group by date".format(self.name_1.text(), self.game.currentText())
        curs.execute(sql)
        rows = curs.fetchall()
        count = len(rows)
        for i in range(count):
            row = list(rows[i].values())
            self.playtime.append("{} : {}".format(row[0], row[1]))
        conn.commit()
        self.name_1.clear()

    def reset_btn(self) :
        self.playtime.clear()


if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()

conn.close()