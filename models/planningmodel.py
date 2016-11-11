#!/usr/bin/python
# -*- coding: utf-8 -*-
#
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSql import *
from datetime import timedelta, date
from PySimplePlanner.utils.utils import Utils

class PlanningModel(QAbstractTableModel):

    __data = None
    __idx_wp_id = {}

    def __init__(self, min_date, max_date, modeltask:QStandardItemModel, parent=None):
        # init parents
        super(PlanningModel, self).__init__()

        #Store the model task
        self.modeltask = modeltask

        #Create list of weeks
        self.header_data = []
        date = min_date
        delta = timedelta(days=1)
        while date <= max_date:
            date += delta
            header = str(date.isocalendar()[0]) + '\n' + str(date.isocalendar()[1])
            if header not in self.header_data:
                self.header_data.append(header)

        # get current day index
        today = date.today()
        toady_header = str(today.isocalendar()[0]) + '\n' + str(today.isocalendar()[1])
        self.today_index = self.header_data.index(toady_header)

        #create index of WP_ID indexes
        for irow in range(modeltask.rowCount()):
            idx = modeltask.index(irow, 5)
            wp_id = idx.data()
            if wp_id:
                self.__idx_wp_id[wp_id] = irow

        #create date array 2D
        self.__data = Utils.make2dList(modeltask.rowCount(),len(self.header_data))
        self.__imputdata = self.load_db()

    def load_db(self):
        query = QSqlQuery()
        query.exec_("""SELECT * FROM imputations""")
        while (query.next()):
            wp_id = query.value(0)
            date = Utils.datetxt_to_date(query.value(2))
            wl = query.value(1)
            #get the wp_id_line
            if wp_id in self.__idx_wp_id:
                i = self.__idx_wp_id[wp_id]
            #get the date column
            j = self.header_data.index(str(date.isocalendar()[0]) + '\n' + str(date.isocalendar()[1]))
            self.__data[i][j]=wl

    def columnCount(self, parent=None, *args, **kwargs):
        return len(self.header_data)

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.__data)

    def headerData(self, p_int, Qt_Orientation, role=None):
        if Qt_Orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.header_data[p_int])
        return QVariant()

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable

    def update(self, dataIn):
        print('Updating Model')
        #TODO
        return

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            try:
                wl = self.__data[index.row()][index.column()]
                if wl > 0:
                    return wl
            except:
                return QVariant()
        elif role == Qt.BackgroundRole:
            if index.column() < self.today_index:
                return QBrush(QColor(Utils.COLOR_BLUE))
            value = int(self.__data[index.row()][index.column()])
            if value == 5:
                return QBrush(QColor(Utils.COLOR_GREEN))
            elif value > 5:
                return QBrush(QColor(Utils.COLOR_RED))
            elif value > 0:
                return QBrush(QColor(Utils.COLOR_LIGHT))
        elif role == Qt.ForegroundRole:
                return  QBrush(QColor(Utils.COLOR_BLACK))
        elif role == Qt.FontRole:
            if index.column() <self.today_index:
                return QFont("Calibri", 9, -1, True)
        else:
            return QVariant()

    def setData(self, modelIndex:QModelIndex, variant, role=Qt.EditRole):
        # not length or filepath and editing
        if role == Qt.EditRole:
            i = modelIndex.row()
            j = modelIndex.column()
            try:
                wl = int(variant)
                if 0<=wl<=7:
                    self.save_value(i, j, wl)
                ans = True
            except:
                ans = False
            else:
                # self.dataChanged.emit(modelIndex, modelIndex)
                ans = True
        else:
            ans = QAbstractTableModel.setData(self, modelIndex, variant, role)
        return ans

    def save_value(self, i, j, value):
        self.__data[i][j] = value
        self.save_valuedb(i, j, value)


    def save_valuedb(self, i, j, value):
        wp_id = wp_id = self.modeltask.index(i, 5).data()
        header = self.header_data[j]
        t_h = header.split('\n')
        date = Utils.iso_to_gregorian(int(t_h[0]), int(t_h[1]), 1)
        datetxt = Utils.date_to_datetxt(date)
        query_str = "INSERT OR REPLACE INTO imputations \
        (imp_wp_id, imp_date, imp_wl) VALUES ('%s', '%s', %s) \
                            " % (wp_id, datetxt, str(value))
        query_str_del = "DELETE FROM imputations WHERE imp_wl = 0"
        query = QSqlQuery()
        query.exec_(query_str_del)
        query.exec_(query_str)
        print(query.lastError().text())