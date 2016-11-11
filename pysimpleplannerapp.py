#!/usr/bin/python
# -*- coding: utf-8 -*-
#
from PyQt5.QtGui import *
from PyQt5.QtSql import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PySimplePlanner.views.main import Ui_MainWindow
from PySimplePlanner.models.planningmodel import PlanningModel
from PySimplePlanner.utils.ModelTest import ModelTest
from PySimplePlanner.utils.utils import Utils

class PySimplePlanner(QMainWindow, Ui_MainWindow):

    __db = QSqlDatabase
    model_task = QSqlQueryModel
    proj_header = ["Project\n", "Task\n", "Activity\n", "Assignee\n", "WL\n"]

    def __init__(self, parent=None):
        #init parents
        super(PySimplePlanner, self).__init__()

        # Configure UI
        self.setupUi(self)

        #request
        self.__config = Utils.load_config()
        database = self.__config["database_path"]
        self.opendb(database)

        #Connect Actions
        self.actionNew_Project.triggered.connect(self.add_project)
        self.actionEdit_Projects.triggered.connect(self.edit_project)
        self.actionNew_task.triggered.connect(self.add_task)
        self.actionEdit_task.triggered.connect(self.edit_task)
        self.actionNew.triggered.connect(self.create_action)
        self.actionOpen.triggered.connect(self.open_action)
        self.actionToday.triggered.connect(self.focus_today)
        self.actionEdit_Activity.triggered.connect(self.edit_wp)
        self.actionRessources.triggered.connect(self.edit_ressources)
        self.actionAcitivty_Types.triggered.connect(self.edit_activitytype)

    def load_modeltask(self):
        # self.model_task = QStandardItemModel()
        self.model_task = QSqlQueryModel()
        self.model_task.setQuery(Utils.QUERY_MODELTASK)
        # #create the tree from sql models
        # if not self.model_sqltasks:
        #     raise 'SQL Not Initialized'
        # task_item_dic = {}
        # prj_item_dic = {}
        # for i in range(0, self.model_sqltasks.rowCount()):
        #     task = self.model_sqltasks.index(i, 1).data()
        #     prj = self.model_sqltasks.index(i, 2).data()
        #     if task not in task_item_dic:
        #         #create a new element
        #         item_task = QStandardItem(str(task))
        #         task_item_dic[task] = item_task
        #         if prj not in prj_item_dic:
        #             item_prj = QStandardItem(str(task))
        #             item_prj.appendRow(item_task)
        #             prj_item_dic[prj] = item_prj
        #         else:
        #             item_prj = prj_item_dic[prj]
        #             item_prj.appendRow(item_task)
        # for i in range(0, sql_model_task.rowCount()):
        #     task = sql_model_task.index(i, 1).data()
        #     rec = []
        #     #Create the QStandardItem from SQL Item
        #     for j in range(0, sql_model_task.columnCount()):
        #         rec.append(QStandardItem(sql_model_task.index(i,j).data()))
        #     #get the task
        #     root_item = task_item_dic[task]
        #     root_item.appendRow(rec)
        #
        # for key, item in prj_item_dic.items():
        #     self.model_task.appendRow(item)

        for i, elem in enumerate(self.proj_header):
            self.model_task.setHeaderData(i, Qt.Horizontal, elem)

    def refresh_models(self):
        self.refresh_sql_models()
        self.load_modelsandviews()

    def load_sqlmodels(self):
        self.model_sqlproject = QSqlTableModel()
        self.model_sqltasks = QSqlRelationalTableModel()
        self.model_sqlwp = QSqlRelationalTableModel()
        self.model_sqlproject.setTable("project")
        self.model_sqlproject.select()
        self.model_sqlproject.setEditStrategy(QSqlTableModel.OnRowChange)
        self.model_sqltasks.setTable("task")
        self.model_sqltasks.setRelation(2, QSqlRelation("project", "prj_id", "prj_name"))
        self.model_sqltasks.sort(1, Qt.AscendingOrder)
        self.model_sqltasks.select()
        self.model_sqltasks.setEditStrategy(QSqlTableModel.OnRowChange)
        self.model_sqlwp.setTable("workpackage")
        self.model_sqlwp.setRelation(1, QSqlRelation("task", "tsk_id", "tsk_name"))
        self.model_sqlwp.setRelation(2, QSqlRelation("activitytype", "type", "type"))
        self.model_sqlwp.setRelation(3, QSqlRelation("ressources", "id", "name"))
        self.model_sqlwp.select()
        self.model_sqlwp.setEditStrategy(QSqlTableModel.OnRowChange)
        self.model_sqlressource = QSqlTableModel()
        self.model_sqlressource.setTable("ressources")
        self.model_sqlressource.select()
        self.model_sqlactivitytype = QSqlTableModel()
        self.model_sqlactivitytype.setTable("activitytype")
        self.model_sqlactivitytype.select()

    def refresh_sql_models(self):
        self.model_sqlproject.select()
        self.model_sqlactivitytype.select()
        self.model_sqlwp.select()
        self.model_sqltasks.select()
        self.model_sqlressource.select()

    def get_project_max_date(self):
        query = QSqlQuery()
        query.exec_("""SELECT MAX(prj_enddate) FROM project""")
        max_date = Utils.date_to_datetxt(Utils.get_default_max_date())
        while (query.next()):
            if query.value(0) != '':
                max_date = query.value(0)
        return Utils.datetxt_to_date(max_date)

    def get_project_min_date(self):
        query = QSqlQuery()
        query.exec_("""SELECT MIN(prj_startdate) FROM project""")
        min_date = Utils.date_to_datetxt(Utils.get_default_min_date())
        while (query.next()):
            if query.value(0) != '':
                min_date = query.value(0)
        return Utils.datetxt_to_date(min_date)

    def add_project(self):
        text, ok = QInputDialog.getText(self, 'Project Name',
                                              'New Project Name:')

        if ok:
            self.model_sqlproject.database().commit()
            record = self.model_sqlproject.record()
            record.setGenerated(0, False)
            record.setValue(1, text)
            record.setValue(2, Utils.date_to_datetxt())
            record.setValue(3, '')
            self.model_sqlproject.insertRecord(self.model_sqlproject.rowCount(), record)
            print(self.model_sqlproject.lastError().text())

    def add_task(self):
        # dialog =
        return

    def edit_project(self):
        self.call_table_dialog(self.model_sqlproject, True)
        self.refresh_models()
        return

    def edit_task(self):
        self.call_table_dialog(self.model_sqltasks, True)
        self.refresh_models()

    def edit_wp(self):
        self.call_table_dialog(self.model_sqlwp, True)
        self.refresh_models()

    def edit_ressources(self):
        self.call_table_dialog(self.model_sqlressource, False, True)
        self.refresh_models()

    def edit_activitytype(self):
        self.call_table_dialog(self.model_sqlactivitytype, False, True)
        self.refresh_models()

    def create_action(self):
        db = QFileDialog.getSaveFileName(self, 'New database', filter=("*.sqlite"))
        if db[0]:
            dbname = ""
            for txt in db[0]:
                idx = txt.rfind("/")
                if idx > 0:
                    txt = txt[idx+1:]
                dbname += txt
            with open('creation.sql', 'r') as f:
                read_data = f.read()
                queries = read_data.rstrip().split(";")
                qsqlquery = QSqlQuery()
                for query in queries:
                    qsqlquery.exec_(query)
                    print(qsqlquery.lastError().text())
                self.opendb(dbname)

    def open_action(self):
        db = QFileDialog.getOpenFileName(self, 'Open database', filter=("*.sqlite"))
        if db[0]:
            dbname = ""
            for txt in db:
                dbname += txt
            self.opendb(dbname)

    def opendb(self, database):
        # Connect to database
        self.__db = QSqlDatabase.addDatabase("QSQLITE")
        self.__db.setHostName('localhost')
        self.__db.setDatabaseName(database)
        self.__db.setUserName('root')
        self.__db.setPassword('root')
        if not self.__db.open():
            QMessageBox.critical(None, "Database Error",
                                 self.__db.lastError().text())
        #save db in config
        self.__config["database_path"] = database
        Utils.save_config(self.__config)

        #load models
        self.load_modelsandviews()

    def load_modelsandviews(self):
        # Create SQL Models
        self.load_sqlmodels()
        self.load_modeltask()
        self.treeView_projects.setModel(self.model_task)
        self.treeView_projects.hideColumn(5)
        self.treeView_projects.hideColumn(6)
        self.treeView_projects.hideColumn(7)
        for i, elem in enumerate(self.proj_header):
            self.treeView_projects.resizeColumnToContents(i)
        min_date = self.get_project_min_date()
        max_date = self.get_project_max_date()

        self.planning_model = PlanningModel(min_date, max_date, self.model_task)
        self.tableView_planning.setModel(self.planning_model)
        self.tableView_planning.resizeColumnsToContents()
        self.focus_today()

    def call_table_dialog(self, model:QSqlTableModel, hide_id=False, new_line=False):
        dialog = Dialog_MaintainTable(model, hide_id, new_line)
        dialog.exec_()

    def searchTask(self, search_string:str):
        for irow in range(self.model_task.rowCount()):
            task_name = self.model_task.index(irow, 1).data()
            if search_string in task_name:
                self.treeView_projects.clearSelection()
                self.treeView_projects.setCurrentIndex(self.model_task.index(irow, 1))
                return

    def focus_today(self):
        current_idx = self.tableView_planning.currentIndex()
        point = QPoint(current_idx.row(), current_idx.column() + 10)
        index = self.tableView_planning.indexAt(point)
        self.tableView_planning.setCurrentIndex(index)
        if self.tableView_planning.colorCount() >= self.planning_model.today_index + 5:
            self.tableView_planning.selectColumn(self.planning_model.today_index + 5)


class Dialog_MaintainTable(QDialog):

    model = QSqlTableModel

    def __init__(self, model:QSqlTableModel, hide_id, new_line):
        #init parents
        super(Dialog_MaintainTable, self).__init__()
        self.model = model

        #SetupUI
        self.resize(600, 480)
        self.box = QVBoxLayout(self)
        self.setLayout(self.box)
        self.bt_group = QButtonGroup(self)
        self.bt_delline = QPushButton("Delete Line")
        self.bt_addline = QPushButton("Add Line")
        self.bt_group.addButton(self.bt_delline)
        self.bt_group.addButton(self.bt_addline)

        self.tablewidget = QTableView()
        self.tablewidget.setModel(self.model)
        self.tablewidget.setItemDelegate(QSqlRelationalDelegate(self.tablewidget))
        if hide_id:
            self.tablewidget.hideColumn(0)
        self.tablewidget.resizeColumnsToContents()
        if new_line:
            model.insertRow(model.rowCount())
        self.box.addWidget(self.tablewidget)
        self.box.addWidget(self.bt_delline)
        self.box.addWidget(self.bt_addline)

        #Actions
        self.bt_delline.clicked.connect(self.delete_line)
        self.bt_delline.clicked.connect(self.delete_line)
        self.bt_addline.clicked.connect(self.add_line)

    def delete_line(self):
        idx = self.tablewidget.currentIndex()
        if idx:
            self.model.removeRow(idx.row())
            print(self.model.lastError().text())
            self.model.select()

    def add_line(self):
        self.model.insertRow(self.model.rowCount())
        print(self.model.lastError().text())