import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeView, QVBoxLayout, QPushButton, QWidget, QAbstractItemView, QInputDialog, QFileDialog
from PyQt5.QtCore import Qt, QAbstractItemModel, QModelIndex
from file import FileHandlerFactory

from task3.task3 import TreeItem, TreeModel



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

        self.loadButton = QPushButton("Load")
        self.loadButton.clicked.connect(self.loadFile)

        self.saveButton = QPushButton("Save")
        self.saveButton.clicked.connect(self.saveFile)

        layout = QVBoxLayout()
        layout.addWidget(self.treeView)
        layout.addWidget(self.addButton)
        layout.addWidget(self.removeButton)
        layout.addWidget(self.loadButton)
        layout.addWidget(self.saveButton)

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

    def loadFile(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*);;INI Files (*.ini);;JSON Files (*.json);;XML Files (*.xml)")
        if file_path:
            file_type = file_path.split('.')[-1]
            handler = FileHandlerFactory.get_handler(file_type)
            data = handler.read(file_path)
            self.model.load_from_dict(data)

    def saveFile(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "INI Files (*.ini);;JSON Files (*.json);;XML Files (*.xml)")
        if file_path:
            file_type = file_path.split('.')[-1]
            handler = FileHandlerFactory.get_handler(file_type)
            data = self.model.to_dict()
            handler.write(data, file_path)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
