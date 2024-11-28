import sys
import sqlite3
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QTableWidgetItem
import sqlite3


def create_table():
    conn = sqlite3.connect('coffee.sqlite')
    cursor = conn.cursor()

    # Создание таблицы coffee
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS coffee (
        id INTEGER PRIMARY KEY,
        name TEXT,
        roast_degree TEXT,
        ground_or_beans TEXT,
        taste_description TEXT,
        price REAL,
        package_volume REAL
    )
    ''')

    # Вставка начальных данных
    cursor.execute('''
    INSERT INTO coffee (name, roast_degree, ground_or_beans, taste_description, price, package_volume)
    VALUES ('Arabica', 'Medium', 'Ground', 'Smooth and balanced', 10.99, 250)
    ''')

    cursor.execute('''
    INSERT INTO coffee (name, roast_degree, ground_or_beans, taste_description, price, package_volume)
    VALUES ('Robusta', 'Dark', 'Beans', 'Strong and bold', 12.99, 500)
    ''')

    cursor.execute('''
    INSERT INTO coffee (name, roast_degree, ground_or_beans, taste_description, price, package_volume)
    VALUES ('Liberica', 'Light', 'Ground', 'Mild and sweet', 9.99, 300)
    ''')

    conn.commit()
    conn.close()


create_table()


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
