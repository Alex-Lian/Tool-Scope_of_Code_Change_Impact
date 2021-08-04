# -*- coding: utf-8 -*-
import sys, json
from collections import defaultdict
from typing import Any, List, Dict, Union

from PyQt5.QtCore import QAbstractItemModel, QModelIndex, QObject, Qt, QFileInfo
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QTreeView, QApplication

first_layer_list = []
for line in open('input.txt', 'r'):  #打开文件
    rs = line.rstrip('\n')  # 移除行尾换行符
    first_layer_list.append(rs)

mapping_test_old = defaultdict(list)
mapping_test_new = defaultdict(list)

json_path_new = "output_new.json"
json_path_old = "output_old.json"
with open(json_path_new) as file:
    document = json.load(file)
    for i in document:
        if i['targetClass'] + '#' + i['targetMethod'] != i['sourceClass'] + '#' + i['sourceMethod']:
            mapping_test_new[i['sourceClass'] + '#' + i['sourceMethod']].append(
                i['targetClass'] + '#' + i['targetMethod'])
with open(json_path_old) as file:
    document = json.load(file)
    for i in document:
        if i['targetClass'] + '#' + i['targetMethod'] != i['sourceClass'] + '#' + i['sourceMethod']:
            mapping_test_old[i['sourceClass'] + '#' + i['sourceMethod']].append(
                i['targetClass'] + '#' + i['targetMethod'])

class TreeItem:
    """A Json item corresponding to a line in QTreeView"""
    Default = 'Default'
    ADD = 'ADD'
    DELETE = 'DELETE'
    CHILDREN_CHANGED = 'CHILDREN_CHANGED'

    def __init__(self, parent: "TreeItem" = None):
        self._parent = parent
        self._key = ""
        self._value = ""
        self._value_type = None
        self._color_type = TreeItem.Default
        self._children = []
        self._is_selected = False
        self._add = 0
        self._delete = 0
        self._total_child = 0

    def totalchild(self):
        return self._total_child

    def appendChild(self, item: "TreeItem"):
        """Add item as a child"""
        self._children.append(item)

    def child(self, row: int) -> "TreeItem":
        """Return the child of the current item from the given row"""
        return self._children[row]

    def parent(self) -> "TreeItem":
        """Return the parent of the current item"""
        return self._parent

    def childCount(self) -> int:
        """Return the number of children of the current item"""
        return len(self._children)

    def row(self) -> int:
        """Return the row where the current item occupies in the parent"""
        return self._parent._children.index(self) if self._parent else 0

    @property
    def key(self) -> str:
        """Return the key name"""
        return self._key

    @key.setter
    def key(self, key: str):
        """Set key name of the current item"""
        self._key = key

    @property
    def value(self) -> str:
        """Return the value name of the current item"""
        return self._value

    @value.setter
    def value(self, value: str):
        """Set value name of the current item"""
        self._value = value

    @property
    def value_type(self):
        """Return the python type of the item's value."""
        return self._value_type

    @value_type.setter
    def value_type(self, value):
        """Set the python type of the item's value."""
        self._value_type = value

    @classmethod
    def load(
            cls, value: Union[List, Dict], parent: "TreeItem" = None, sort=True, time=0, origin=None,
    ) -> "TreeItem":
        """Create a 'root' TreeItem from a nested list or a nested dictonary

        Examples:
            with open("file.json") as file:
                data = json.dump(file)
                root = TreeItem.load(data)

        This method is a recursive function that calls itself.

        Returns:
            TreeItem: TreeItem
        """

        rootItem = TreeItem(parent)
        rootItem.key = "root"
        rootItem._color_type = TreeItem.Default
        if time >= 10:
            return rootItem
        if isinstance(value, dict):
            items = sorted(value.items()) if sort else value.items()

            for key, value in items:
                child = cls.load(value, rootItem, time=time + 1, origin=origin)
                child.key = key
                if type(value) == list:
                    child.value_type = dict
                else:
                    child.value_type = type(value)
                rootItem.appendChild(child)

        elif isinstance(value, list):
            curdict = defaultdict(list)
            for class_method in value:

                cur_class_method = class_method.split('|')[-1]
                if cur_class_method in mapping_test.keys():
                    curdict[class_method] = mapping_test[cur_class_method]
                else:
                    curdict[class_method] = []
            items = sorted(curdict.items()) if sort else curdict.items()
            for key, value in items:
                child = cls.load(value, rootItem, time=time + 1, origin=origin)
                child.key = key
                if type(value) == list:
                    child.value_type = dict
                else:
                    child.value_type = type(value)
                rootItem.appendChild(child)

        else:
            rootItem.value = value
            rootItem.value_type = type(value)

        return rootItem

    def updateColorType(self):
        if self.childCount() == 0:
            if self.key.startswith('ADD-----|'):
                self._color_type = TreeItem.ADD
            elif self.key.startswith('DELETE--|'):
                self._color_type = TreeItem.DELETE
            else:
                self._color_type = TreeItem.Default
        else:
            if self.key.startswith('ADD-----|'):
                self._color_type = TreeItem.ADD
            elif self.key.startswith('DELETE--|'):
                self._color_type = TreeItem.DELETE
            elif self.isChanged():
                self._color_type = TreeItem.CHILDREN_CHANGED
            else:
                self._color_type = TreeItem.Default

    def isChanged(self):
        if self.childCount() == 0:
            return self.key.startswith('ADD-----|') or self.key.startswith('DELETE--|')
        for child in self._children:
            if child.isChanged():
                return True
        return False

    def getStatus(self):
        add_flag = 0
        delete_flag = 0
        if self.key.startswith('ADD-----|'):
            add_flag = 1
        elif self.key.startswith('DELETE--|'):
            delete_flag = 1
        self._add = add_flag
        self._delete = delete_flag
        return add_flag, delete_flag

    def updateStatus(self):
        addSum = 0
        deleteSum = 0
        cur_total_child = 0
        if self.childCount() == 0:
            self._total_child = 1
            return self.getStatus()
        for child in self._children:
            cursum = child.updateStatus()
            addSum += cursum[0]
            deleteSum += cursum[1]
            cur_total_child += child.totalchild()
        self._total_child = cur_total_child
        if addSum != 0:
            self._add = addSum
            self.key += "  (%d/%d) %3.1f%% +" % (self._add, self._total_child, 100*self._add/self._total_child)
        if deleteSum != 0:
            self._delete = deleteSum
            self.key += "  (%d/%d) %3.1f%% -" % (self._delete, self._total_child, 100*self._delete/self._total_child)
        return addSum, deleteSum

    def updateColorTypeAll(self):
        for child in self._children:
            child.updateColorTypeAll()
        self.updateColorType()

    def order_decision(self, elem):
        if elem._total_child > 1 and (elem._add + elem._delete) != 0:
            return float(2 + (elem._add + elem._delete)/elem._total_child)
        elif elem._add + elem._delete != 0:
            return 2.0
        elif elem._total_child > 1:
            return 1.0
        return 0.0

    def updateOrder(self):
        self._children.sort(key=self.order_decision, reverse=True)
        for child in self._children:
            child.updateOrder()

    def get_color_type(self):
        return self._color_type

    def get_is_selected(self):
        return self._is_selected

    def set_is_selected(self, _is_selected):
        self._is_selected = _is_selected


class JsonModel(QAbstractItemModel):
    """ An editable model of Json data """

    def __init__(self, parent: QObject = None):
        super().__init__(parent)

        self._rootItem = TreeItem()
        self._headers = ("Property", "Value")

    def clear(self):
        """ Clear data from the model """
        self.load({})

    def load(self, document: dict, ):
        """Load model from a nested dictionary returned by json.loads()

        Arguments:
            document (dict): JSON-compatible dictionary
        """

        assert isinstance(
            document, (dict, list, tuple)), "`document` must be of dict, list or tuple, not {0:s}".format(
            type(document))

        self.beginResetModel()

        self._rootItem = TreeItem.load(document, origin=document)
        self._rootItem.value_type = type(document)
        self._rootItem.updateColorTypeAll()
        self._rootItem.updateStatus()
        self._rootItem.updateOrder()
        self.endResetModel()

        return True

    def data(self, index: QModelIndex, role: Qt.ItemDataRole) -> Any:
        """Override from QAbstractItemModel

        Return data from a json item according index and role

        """
        if not index.isValid():
            return None

        item = index.internalPointer()

        if role == Qt.DisplayRole:
            if index.column() == 0:
                if '|' in item.key:
                    return item.key.split('|')[1]
                else:
                    return item.key

            if index.column() == 1:
                return item.get_color_type()

        elif role == Qt.EditRole:
            if index.column() == 1:
                return item.value
        elif role == Qt.BackgroundColorRole:
            if item.get_is_selected():
                return QColor('#ffff00')
            else:
                color_type = item.get_color_type()
                if color_type == TreeItem.ADD:
                    return QColor('#00ff00')
                elif color_type == TreeItem.DELETE:
                    return QColor('#ff0000')
                elif color_type == TreeItem.CHILDREN_CHANGED:
                    return QColor('#A9A9A9')
                else:
                    return QColor('#ffffff')

    def setData(self, index: QModelIndex, value: Any, role: Qt.ItemDataRole, __binding__=None):
        """Override from QAbstractItemModel

        Set json item according index and role

        Args:
            index (QModelIndex)
            value (Any)
            role (Qt.ItemDataRole)

        """
        if role == Qt.EditRole:
            if index.column() == 1:
                item = index.internalPointer()
                item.value = str(value)

                if __binding__ in ("PySide", "PyQt4"):
                    self.dataChanged.emit(index, index)
                else:
                    self.dataChanged.emit(index, index, [Qt.EditRole])

                return True

        return False

    def headerData(
            self, section: int, orientation: Qt.Orientation, role: Qt.ItemDataRole
    ):
        """Override from QAbstractItemModel

        For the JsonModel, it returns only data for columns (orientation = Horizontal)

        """
        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            return self._headers[section]

    def index(self, row: int, column: int, parent=QModelIndex()) -> QModelIndex:
        """Override from QAbstractItemModel

        Return index according row, column and parent

        """
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if not parent.isValid():
            parentItem = self._rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()

    def parent(self, index: QModelIndex) -> QModelIndex:
        """Override from QAbstractItemModel

        Return parent index of index

        """

        if not index.isValid():
            return QModelIndex()

        childItem = index.internalPointer()
        parentItem = childItem.parent()

        if parentItem == self._rootItem:
            return QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent=QModelIndex()):
        """Override from QAbstractItemModel

        Return row count from parent index
        """
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self._rootItem
        else:
            parentItem = parent.internalPointer()

        return parentItem.childCount()

    def columnCount(self, parent=QModelIndex()):
        """Override from QAbstractItemModel

        Return column number. For the model, it always return 2 columns
        """
        return 2

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        """Override from QAbstractItemModel

        Return flags of index
        """
        flags = super(JsonModel, self).flags(index)
        return flags

    def to_json(self, item=None):

        if item is None:
            item = self._rootItem

        nchild = item.childCount()

        if item.value_type is dict:
            document = {}
            for i in range(nchild):
                ch = item.child(i)
                document[ch.key] = self.to_json(ch)
            return document

        elif item.value_type == list:
            document = []
            for i in range(nchild):
                ch = item.child(i)
                document.append(self.to_json(ch))
            return document

        else:
            return item.value

    def get_root_item(self):
        return self._rootItem

    def set_selected(self, text):
        root = self.get_root_item()
        if text.split():
            for i, child in enumerate(root._children):
                child.set_is_selected(text in child.key)
                index = self.index(i, 0, self.index(0, 0))
                self.dataChanged.emit(index, index)

def final_mapping(old_mapping, new_mapping):
    result_mapping = dict()
    total_ele = list(set(old_mapping.keys()) | set(new_mapping.keys()))
    for i in total_ele:
        if i in new_mapping.keys() and i not in old_mapping.keys():
            reflag = 'ADD-----|'
            value = new_mapping[i]
            for j in range(len(value)):
                value[j] = reflag + value[j]
            result_mapping[i] = value
        elif i not in new_mapping.keys() and i in old_mapping.keys():
            reflag = 'DELETE--|'
            value = old_mapping[i]
            for j in range(len(value)):
                value[j] = reflag + value[j]
            result_mapping[i] = value
        else:
            value_old = old_mapping[i]
            value_new = new_mapping[i]
            value = []
            for j in list(set(value_new) | set(value_old)):
                if j in value_new and j not in value_old:
                    pre_flag = 'ADD-----|'
                elif j not in value_new and j in value_old:
                    pre_flag = 'DELETE--|'
                else:
                    pre_flag = '----------|'
                value.append(pre_flag + j)
            result_mapping[i] = value
    return result_mapping


mapping_test = final_mapping(mapping_test_old, mapping_test_new)
mapping_test_select = dict()
for i in first_layer_list:
    i = i.split(' ')[-1]
    if i in mapping_test.keys():
        mapping_test_select[i] = mapping_test[i]

if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = QTreeView()
    model = JsonModel()

    view.setModel(model)

    json_path_new = QFileInfo(__file__).absoluteDir().filePath("mapping_new.json")
    json_path_old = QFileInfo(__file__).absoluteDir().filePath("mapping_old.json")

    mapping_test = final_mapping(mapping_test_old, mapping_test_new)

    model.load(mapping_test)
    view.show()
    app.exec_()
