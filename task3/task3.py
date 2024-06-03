import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeView, QVBoxLayout, QPushButton, QWidget, QAbstractItemView, \
    QInputDialog
from PyQt5.QtCore import Qt, QAbstractItemModel, QModelIndex


class TreeItem:
    def __init__(self, data, parent=None):
        self.parentItem = parent
        self.itemData = data
        self.childItems = []

    def appendChild(self, item):
        self.childItems.append(item)

    def removeChild(self, item):
        self.childItems.remove(item)

    def child(self, row):
        if 0 <= row < len(self.childItems):
            return self.childItems[row]
        return None

    def childCount(self):
        return len(self.childItems)

    def columnCount(self):
        return len(self.itemData)

    def data(self, column):
        if 0 <= column < len(self.itemData):
            return self.itemData[column]
        return None

    def parent(self):
        return self.parentItem

    def row(self):
        if self.parentItem:
            return self.parentItem.childItems.index(self)
        return 0

    def removeSelfAndChildren(self):
        for child in self.childItems:
            child.removeSelfAndChildren()
        if self.parentItem:
            self.parentItem.removeChild(self)


class TreeModel(QAbstractItemModel):
    def __init__(self, data, parent=None):
        super(TreeModel, self).__init__(parent)
        self.rootItem = TreeItem(("Title",))
        self.setupModelData(data.split('\n'), self.rootItem)

    def columnCount(self, parent=QModelIndex()):
        if parent.isValid():
            return parent.internalPointer().columnCount()
        return self.rootItem.columnCount()

    def data(self, index, role):
        if not index.isValid():
            return None
        if role != Qt.DisplayRole:
            return None
        item = index.internalPointer()
        return item.data(index.column())

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.rootItem.data(section)
        return None

    def index(self, row, column, parent=QModelIndex()):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()
        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()
        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        return QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()
        childItem = index.internalPointer()
        parentItem = childItem.parent()
        if parentItem == self.rootItem or parentItem is None:
            return QModelIndex()
        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent=QModelIndex()):
        if parent.column() > 0:
            return 0
        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()
        return parentItem.childCount()

    def setupModelData(self, lines, parent):
        parents = [parent]
        indentations = [0]
        for line in lines:
            position = 0
            while position < len(line):
                if line[position] != ' ':
                    break
                position += 1
            lineData = line[position:].strip()
            if not lineData:
                continue
            columnData = [lineData]
            if position > indentations[-1]:
                if parents[-1].childCount() > 0:
                    parents.append(parents[-1].child(parents[-1].childCount() - 1))
                    indentations.append(position)
            else:
                while position < indentations[-1] and len(parents) > 0:
                    parents.pop()
                    indentations.pop()
            parent = parents[-1]
            parent.appendChild(TreeItem(columnData, parent))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MVC Example")
        self.setGeometry(300, 100, 600, 400)

        self.model = TreeModel("a\n b\n c\n  d\n e\nf")

        self.treeView = QTreeView()
        self.treeView.setModel(self.model)
        self.treeView.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.treeView.setSelectionMode(QAbstractItemView.SingleSelection)

        self.addButton = QPushButton("Add")
        self.addButton.clicked.connect(self.addItem)

        self.removeButton = QPushButton("Remove")
        self.removeButton.clicked.connect(self.removeItem)

        layout = QVBoxLayout()
        layout.addWidget(self.treeView)
        layout.addWidget(self.addButton)
        layout.addWidget(self.removeButton)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def addItem(self):
        index = self.treeView.selectedIndexes()
        if index:
            selected_index = index[0]
            item = selected_index.internalPointer()
            text, ok = QInputDialog.getText(self, "Add Item", "Enter item name:")
            if ok and text:
                item.appendChild(TreeItem([text], item))
                self.model.layoutChanged.emit()
        else:
            text, ok = QInputDialog.getText(self, "Add Root Item", "Enter item name:")
            if ok and text:
                self.model.rootItem.appendChild(TreeItem([text], self.model.rootItem))
                self.model.layoutChanged.emit()

    def removeItem(self):
        index = self.treeView.selectedIndexes()
        if index:
            selected_index = index[0]
            item = selected_index.internalPointer()
            item.removeSelfAndChildren()
            self.model.layoutChanged.emit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
