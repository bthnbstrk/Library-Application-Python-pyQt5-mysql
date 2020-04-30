# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mylibraryismyworld.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import MySQLdb as mdb
import ast
from PyQt5.QtGui import QIntValidator

global LoadData
def MyConverter(mydata):
    def cvt(data):
        try:
            return ast.literal_eval(data)

        except Exception:
            return str(data)

    return tuple(map(cvt,mydata))
    # self.book_table.rowCount(0)

class Ui_myworld(object):

    def addBook(self):
        bn = self.book_name.text()
        cp = self.n_of_pages.text()
        au = self.author.text()
        isb = self.isbn.text()
        con = mdb.connect('localhost', 'root', '', 'library')
        cur = con.cursor()
        cur.execute("INSERT INTO books(book_name, book_pages,book_author,book_isbn)"
                        "VALUES('%s', '%s','%s','%s')" % (''.join(bn),
                                                ''.join(cp),
                                                ''.join(au),
                                                ''.join(isb)
                                               ))
        self.messagebox( 'Connection', 'Data Inserted Successfully')
        con.commit()
        self.book_name.setText("")
        self.n_of_pages.setText("")
        self.author.setText("")
        self.isbn.setText("")
        self.LoadData()

    def messagebox(self,title,message):
        mess=QtWidgets.QMessageBox()
        mess.setWindowTitle(title)
        mess.setText(message)
        mess.setStandardButtons(QtWidgets.QMessageBox.Ok)
        mess.exec()

    def LoadData(self):
        db = mdb.connect('localhost', 'root', '', 'library')
        cur=db.cursor()
        sql="select book_id,book_isbn,book_name,book_pages,book_author from books"
        rows=cur.execute(sql)
        data=cur.fetchall()
        self.book_table.setRowCount((rows/3)-1)
        for row in data:
            self.addTable(MyConverter(row))

        cur.close()

    def addTable(self,colums):
        rowPosition=self.book_table.rowCount()
        self.book_table.insertRow(rowPosition)
        for i,column in enumerate(colums):
            self.book_table.setItem(rowPosition,i,QtWidgets.QTableWidgetItem(str(column)))


    def setupUi(self, myworld):
        myworld.setObjectName("myworld")
        myworld.resize(650, 800)
        self.centralwidget = QtWidgets.QWidget(myworld)
        self.centralwidget.setObjectName("centralwidget")
        self.book_table = QtWidgets.QTableWidget(self.centralwidget)
        self.book_table.setGeometry(QtCore.QRect(70, 290, 530, 251))
        self.book_table.setObjectName("book_table")
        self.book_table.setColumnCount(5)
        self.book_table.setRowCount(100)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(70, 60, 55, 16))
        self.label.setObjectName("label")
        self.isbn = QtWidgets.QLineEdit(self.centralwidget)
        self.isbn.setGeometry(QtCore.QRect(190, 60, 200, 22))
        self.isbn.setObjectName("isbn")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(70, 100, 200, 16))
        self.label_2.setObjectName("label_2")
        self.book_name = QtWidgets.QLineEdit(self.centralwidget)
        self.book_name.setGeometry(QtCore.QRect(190, 100, 200, 22))
        self.book_name.setObjectName("book_name")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(70, 136, 101, 20))
        self.label_3.setObjectName("label_3")
        self.n_of_pages = QtWidgets.QLineEdit(self.centralwidget)
        self.n_of_pages.setGeometry(QtCore.QRect(190, 140, 200, 22))
        self.n_of_pages.setObjectName("n_of_pages")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(70, 180, 55, 16))
        self.label_4.setObjectName("label_4")
        self.author = QtWidgets.QLineEdit(self.centralwidget)
        self.author.setGeometry(QtCore.QRect(190, 180, 200, 22))
        self.author.setObjectName("author")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(240, 10, 211, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.btn_add_book = QtWidgets.QPushButton(self.centralwidget)
        self.btn_add_book.setGeometry(QtCore.QRect(210, 240, 93, 28))
        self.btn_add_book.setObjectName("btn_add_book")
        self.btn_change_properties = QtWidgets.QPushButton(self.centralwidget)
        self.btn_change_properties.setGeometry(QtCore.QRect(60, 560, 141, 28))
        self.btn_change_properties.setObjectName("btn_change_properties")
        self.btn_del_book = QtWidgets.QPushButton(self.centralwidget)
        self.btn_del_book.setGeometry(QtCore.QRect(250, 560, 131, 28))
        self.btn_del_book.setObjectName("btn_del_book")
        myworld.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(myworld)
        self.statusbar.setObjectName("statusbar")
        myworld.setStatusBar(self.statusbar)
        self.btn_add_book.clicked.connect(self.addBook)
        self.btn_change_properties.clicked.connect(self.updateBook)
        self.retranslateUi(myworld)
        QtCore.QMetaObject.connectSlotsByName(myworld)
        self.btn_del_book.clicked.connect(self.deleteBook)
        self.book_table.itemSelectionChanged.connect(self.deleteButtonsHandler)  ##### Silme işlemleri için ID
        self.book_table.resizeColumnsToContents()
        self.onlyInt = QIntValidator()
        self.isbn.setValidator(self.onlyInt)
        self.n_of_pages.setValidator(self.onlyInt)
        regex = QtCore.QRegExp("[a-z-A-Z_]+")
        validator = QtGui.QRegExpValidator(regex)
        self.author.setValidator(validator)


    def deleteButtonsHandler(self):
        if len(self.book_table.selectedItems()) != 0:
            print( self.book_table.selectedItems()[0].text())



    def deleteBook(self):
        if len(self.book_table.selectedItems()) != 0:
            deger=(self.book_table.selectedItems()[0].text(),)
            db = mdb.connect('localhost', 'root', '', 'library')
            cur = db.cursor()
            sql = "DELETE FROM BOOKS WHERE book_id=%s"
            cur.execute(sql,deger)
            db.commit()
            self.messagebox('Connection', 'Data Removed Successfully')
        self.LoadData()

    def updateBook(self):
        if len(self.book_table.selectedItems()) != 0:
            deger = (self.book_table.selectedItems()[0].text(),)
            db = mdb.connect('localhost', 'root', '', 'library')
            cur = db.cursor()
            bn = self.book_name.text()
            cp = self.n_of_pages.text()
            au = self.author.text()
            isb = self.isbn.text()
            sql = "UPDATE books SET book_name = %s,book_pages = %s,book_author=%s,book_isbn=%s WHERE book_id = %s"
            val = (bn, cp,au,isb,deger)
            cur.execute(sql, val)
            db.commit()
            self.messagebox('Connection', 'Data Changed Successfully')
            self.book_name.setText("")
            self.n_of_pages.setText("")
            self.author.setText("")
            self.isbn.setText("")
        self.LoadData()


    def retranslateUi(self, myworld):
        _translate = QtCore.QCoreApplication.translate
        myworld.setWindowTitle(_translate("myworld", "My Library is My World"))
        self.label.setText(_translate("myworld", "ISBN"))
        self.label_2.setText(_translate("myworld", "Book Name"))
        self.label_3.setText(_translate("myworld", "Number of Pages"))
        self.label_4.setText(_translate("myworld", "Author"))
        self.label_5.setText(_translate("myworld", "My Library is My World"))
        self.btn_add_book.setText(_translate("myworld", "Add Book"))
        self.btn_change_properties.setText(_translate("myworld", "Change Properties"))
        self.btn_del_book.setText(_translate("myworld", "Delete Book"))

        self.book_table.setHorizontalHeaderLabels(['Book Id','ISBN', 'Bookname', 'Pages of Count', 'Author'])

        self.LoadData()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    myworld = QtWidgets.QMainWindow()
    ui = Ui_myworld()
    ui.setupUi(myworld)
    myworld.show()
    sys.exit(app.exec_())

