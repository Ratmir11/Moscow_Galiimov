import sys
import sqlite3
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QTableWidgetItem
import sqlite3


class CoffeeApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(CoffeeApp, self).__init__()
        uic.loadUi('main.ui', self)
        self.load_data()

    def load_data(self):
        conn = sqlite3.connect('coffee.sqlite')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM coffee")
        rows = cursor.fetchall()
        conn.close()

        self.tableWidget.setRowCount(len(rows))
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(
            ["ID", "Название сорта", "Степень обжарки", "Молотый/в зернах", "Описание вкуса", "Цена", "Объем упаковки"])

        for i, row in enumerate(rows):
            for j, item in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(item)))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = CoffeeApp()
    window.show()
    sys.exit(app.exec())
