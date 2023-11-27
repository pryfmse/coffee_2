import sqlite3
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from main_1 import Ui_MainWindow
from addEditCoffeeForm import Ui_Form


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        con = sqlite3.connect('coffee.sqlite')
        self.cur = con.cursor()
        self.data = self.cur.execute('''SELECT * FROM кофе''').fetchall()
        for i, row in enumerate(self.data):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))

        self.pushButton.clicked.connect(self.edit)
        self.pushButton_2.clicked.connect(self.add)

    def edit(self):
        a = []
        for index in self.tableWidget.selectedIndexes():
            a.append(index.row())
        if a:
            self.a = Re(self, int(self.tableWidget.item(a[0], 0).text()))
            self.a.show()

    def add(self):
        self.a = Re(self)
        self.a.show()

    def replace(self):
        for row in reversed(range(self.tableWidget.rowCount())):
            self.tableWidget.removeRow(row)

        self.data = self.cur.execute('''SELECT * FROM кофе''').fetchall()
        for i, row in enumerate(self.data):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))


class Re(QMainWindow, Ui_Form):
    def __init__(self, parent=None, id=None):
        super().__init__(parent)
        self.setupUi(self)
        self.con = sqlite3.connect('coffee.sqlite')
        self.cur = self.con.cursor()
        self.id = id
        self.n = self.cur.execute("SELECT MAX(id) FROM кофе").fetchone()[0]

        self.comboBox.addItem('Молотый')
        self.comboBox.addItem('В зернах')
        if self.id is not None:
            a = self.cur.execute(f"SELECT * FROM кофе WHERE id = {self.id}").fetchone()
            self.plainTextEdit.setPlainText(a[1])
            self.plainTextEdit_2.setPlainText(a[2])
            self.plainTextEdit_3.setPlainText(a[4])
            self.plainTextEdit_4.setPlainText(a[5])

            n = 1 if a[3] == 'В зернах' else 0
            self.comboBox.setCurrentIndex(n)

        self.b = self.cur.execute('''SELECT * FROM кофе''').fetchall()

        self.pushButton.clicked.connect(self.save)

    def save(self):
        if self.save_verdict():
            if self.id is None:
                self.n += 1
                self.cur.execute(f"INSERT INTO кофе(ID, Название, Название_сорта, Молотый_в_зернах, Описание_вкуса,"
                                 f" Объем_упаковки) VALUES ({self.n}, '{self.plainTextEdit.toPlainText()}',"
                                 f" '{self.plainTextEdit_2.toPlainText()}', '{self.comboBox.currentText()}',"
                                 f" '{self.plainTextEdit_3.toPlainText()}', '{self.plainTextEdit_4.toPlainText()}')")

            else:
                self.cur.execute(f"UPDATE кофе SET Название = '{self.plainTextEdit.toPlainText()}',"
                                 f" Название_сорта = '{self.plainTextEdit_2.toPlainText()}', "
                                 f"Молотый_в_зернах = '{self.comboBox.currentText()}', "
                                 f"Описание_вкуса = '{self.plainTextEdit_3.toPlainText()}', "
                                 f"Объем_упаковки = '{self.plainTextEdit_4.toPlainText()}' WHERE id = {int(self.id)}")

            self.con.commit()
            self.parent().replace()
            self.close()

    def save_verdict(self):
        if self.plainTextEdit.toPlainText() and self.plainTextEdit_2.toPlainText() \
                and self.plainTextEdit_3.toPlainText() and self.plainTextEdit_4.toPlainText():
            return True
        return False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())

