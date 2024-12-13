import sys
import sqlite3
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox


class CoffeeApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(CoffeeApp, self).__init__()
        uic.loadUi('main.ui', self)
        self.load_data()
        self.addButton.clicked.connect(self.add_coffee)
        self.editButton.clicked.connect(self.edit_coffee)

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

    def add_coffee(self):
        form = AddEditCoffeeForm(self)
        if form.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            self.load_data()

    def edit_coffee(self):
        selected_items = self.tableWidget.selectedItems()
        if selected_items:
            row = selected_items[0].row()
            coffee_id = int(self.tableWidget.item(row, 0).text())
            form = AddEditCoffeeForm(self, coffee_id)
            if form.exec() == QtWidgets.QDialog.DialogCode.Accepted:
                self.load_data()
        else:
            QMessageBox.warning(self, "Предупреждение", "Выберите запись для редактирования.")



class AddEditCoffeeForm(QtWidgets.QDialog):
    def __init__(self, parent, coffee_id=None):
        super(AddEditCoffeeForm, self).__init__(parent)
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.coffee_id = coffee_id
        self.buttonBox.accepted.connect(self.save_coffee)
        self.buttonBox.rejected.connect(self.reject)

        if self.coffee_id:
            self.load_coffee_data()

    def load_coffee_data(self):
        conn = sqlite3.connect('coffee.sqlite')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM coffee WHERE id=?", (self.coffee_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            self.nameEdit.setText(row[1])
            self.roastDegreeEdit.setText(row[2])
            self.groundOrBeansEdit.setText(row[3])
            self.tasteDescriptionEdit.setText(row[4])
            self.priceEdit.setText(str(row[5]))
            self.packageVolumeEdit.setText(str(row[6]))

    def save_coffee(self):
        name = self.nameEdit.text()
        roast_degree = self.roastDegreeEdit.text()
        ground_or_beans = self.groundOrBeansEdit.text()
        taste_description = self.tasteDescriptionEdit.text()
        price = self.priceEdit.text()
        package_volume = self.packageVolumeEdit.text()

        conn = sqlite3.connect('coffee.sqlite')
        cursor = conn.cursor()

        if self.coffee_id:
            cursor.execute(
                "UPDATE coffee SET name=?, roast_degree=?, ground_or_beans=?,"
                " taste_description=?, price=?, package_volume=? WHERE id=?",
                (name, roast_degree, ground_or_beans, taste_description, price, package_volume, self.coffee_id))
        else:
            cursor.execute(
                "INSERT INTO coffee (name, roast_degree, ground_or_beans, taste_description,"
                " price, package_volume) VALUES (?, ?, ?, ?, ?, ?)",
                (name, roast_degree, ground_or_beans, taste_description, price, package_volume))

        conn.commit()
        conn.close()
        self.accept()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = CoffeeApp()
    window.show()
    sys.exit(app.exec())
