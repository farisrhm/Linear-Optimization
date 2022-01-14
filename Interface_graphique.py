# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Final.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from Simplex_finale import Simplex

"""Ici, il s'agit du programme de l'interface graphique
lancé le afin de voir l'interface et de pouvoir l'utilisé"""


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(893, 586)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Contrainte = QtWidgets.QTextEdit(self.centralwidget)
        self.Contrainte.setGeometry(QtCore.QRect(30, 310, 256, 191))
        self.Contrainte.setObjectName("Contrainte")
        self.FonctionObjective = QtWidgets.QLineEdit(self.centralwidget)
        self.FonctionObjective.setGeometry(QtCore.QRect(30, 210, 201, 25))
        self.FonctionObjective.setObjectName("FonctionObjective")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(620, 180, 111, 16))
        self.label_4.setObjectName("label_4")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(620, 389, 201, 16))
        self.label_3.setObjectName("label_3")
        self.Solution_simp = QtWidgets.QTextEdit(self.centralwidget)
        self.Solution_simp.setGeometry(QtCore.QRect(620, 409, 201, 121))
        self.Solution_simp.setObjectName("Solution_simp")
        self.Solution_simp.setReadOnly(True)
        self.graphicsView_Simplexe = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView_Simplexe.setGeometry(QtCore.QRect(620, 210, 256, 131))
        self.graphicsView_Simplexe.setObjectName("graphicsView_Simplexe")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 180, 171, 16))
        self.label.setObjectName("label")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(200, 30, 681, 81))
        self.label_5.setObjectName("label_5")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(410, 420, 101, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(30, 280, 231, 16))
        self.label_2.setObjectName("label_2")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(410, 370, 101, 31))
        self.pushButton.setObjectName("pushButton")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(140, 235, 91, 24))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 893, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        
        self.pushButton.clicked.connect(self.simplexe)
       # self.pushButton_2.clicked.connect(self.supprimer)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_4.setText(_translate("MainWindow", "Tableau Simplexe"))
        self.label_3.setText(_translate("MainWindow", "Voici la solution :"))
        self.label.setText(_translate("MainWindow", "Entrer la fonction objective :"))
        self.label_5.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:26pt; font-style:italic;\">Méthode d\'optimistation linéaire : Simplexe</span></p></body></html>"))
        self.pushButton_2.setText(_translate("MainWindow", "Effacer"))
        self.label_2.setText(_translate("MainWindow", "Entrer vos contraintes : (≥ ou ≤)"))
        self.pushButton.setText(_translate("MainWindow", "Calculer"))
        self.comboBox.setItemText(0, _translate("MainWindow", "Maximisation"))
        self.comboBox.setItemText(1, _translate("MainWindow", "Minimisation"))

    #def supprimer(self):
        #self.pushButton_2.clear()
        
   
    def simplexe(self):

            fonction = self.FonctionObjective.text()
            pb = self.comboBox.currentIndex()
            simplex = Simplex(fonction, pb)
            contrainte = self.Contrainte.toPlainText()
            clr = contrainte.split('\n')
            if len(clr) > 0:
                for sa in clr:
                    simplex.ajout_contrainte(sa)
                
                meta = simplex.solve()
                variables = ""
                for var in simplex.coefficients:
                    variables += f"<br/>La valeur de {var} est: {meta[var]}"

                self.Solution_simp.setText(f"<b>La solution optimale est: <span style='color:blue;'>{meta['solution']}</span></b>{variables}")
                
                
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

