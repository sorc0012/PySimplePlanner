if __name__ == '__main__':

    import sys
    from PyQt5.QtWidgets import QApplication, QStyleFactory
    from PySimplePlanner.pysimpleplannerapp import PySimplePlanner
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("fusion"))
    mainwindow = PySimplePlanner()
    mainwindow.show()
    sys.exit(app.exec_())