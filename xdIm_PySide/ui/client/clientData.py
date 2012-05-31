# -*- coding: utf-8 -*-

'''
Created on 2012-1-10

@author: x00163361
'''

from PySide import QtCore

class friendItem(object):
    '''friend Item '''
    def __init__(self, data, parent=None):
        self.parentItem = parent
        self.itemData = data
        self.childItems = []

    def appendChild(self, item):
        self.childItems.append(item)

    def child(self, row):
        return self.childItems[row]

    def childCount(self):
        return len(self.childItems)

    def columnCount(self):
        return len(self.itemData)

    def data(self, column):
        try:
            return self.itemData[column]
        except IndexError:
            return None

    def parent(self):
        return self.parentItem

    def row(self):
        if self.parentItem:
            return self.parentItem.childItems.index(self)

        return 0


class friendModel(QtCore.QAbstractItemModel):
    def __init__(self, parent=None):
        super(friendModel, self).__init__(parent)
        self.rootItem = friendItem(("", ""))
        self.fItem = friendItem(("Friend", ""),self.rootItem)
        self.rootItem.appendChild(self.fItem)   
        self.childItem=friendItem(("Child", "inline"),self.fItem)
        self.fItem.appendChild(self.childItem)
#        self.frriendItems=[]
#        self.lastIndex=None 
        self.addFriendRow("dd","inline")    
        
#        self.fItem.appendChild(self.rootItem2)
#        self.rootItem.appendChild(self.xfItem)
       
    def addFriendRow(self,friend,status):
        
        friend = friend
        status = status
#        print "1 clientData addFriendRow start"
        
#        self.rowCount(parent)
        indexA = self.index(0, 0, QtCore.QModelIndex())
#        print "2 "+str(indexA)
        indexB = self.index(0, 0, indexA)
#        print "3 "+str(indexB)
#        print "4 "+str(self.data(indexB,QtCore.Qt.DisplayRole))                
        
#        print "3 "+ str(self.data(indexA,QtCore.Qt.DisplayRole))
#        indexA = self.index(0, 1, QtCore.QModelIndex())
#        print "4 "+str(self.data(indexA,QtCore.Qt.DisplayRole))
#        print "5 "+str(indexA)
#        print self.setData(indexA,"test")

        
##        item=friendItem((friend, status),self.fItem)
##        self.frriendItems.append(item)
##        self.fItem.appendChild(item)
#        indexB = self.index(1, 0, indexA);
#        print indexB
#
#        print self.insertRow(1,QtCore.QModelIndex())
#        print "5 "+str(self.insertRow(1,indexA))
#        
#        indexB = self.index(1, 0, indexA);
#        print indexB        
#        self.setData(indexA,"test",QtCore.Qt.EditRole)
        
        
        index1 = self.index(1, 0, indexA)
        index2 = self.index(1, 1, indexA)
        self.setData(index1,"test",QtCore.Qt.EditRole)
        self.setData(index2,"online",QtCore.Qt.EditRole)
                
#        print "6 clientData addFriendRow end"
                     
    def columnCount(self, parent):
        if parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return self.rootItem.columnCount()

    def data(self, index, role):
        if not index.isValid():
            return None

        if role != QtCore.Qt.DisplayRole:
            return None

        item = index.internalPointer()

        return item.data(index.column())

    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.NoItemFlags

        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.rootItem.data(section)

        return None

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()

        childItem = index.internalPointer()
        parentItem = childItem.parent()

        if parentItem == self.rootItem:
            return QtCore.QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        return parentItem.childCount()
    
