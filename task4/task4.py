import sys
import json
import xml.etree.ElementTree as ET
from configparser import ConfigParser
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeView, QVBoxLayout, QPushButton, QWidget, QAbstractItemView, QInputDialog, QFileDialog
from PyQt5.QtCore import Qt, QAbstractItemModel, QModelIndex

from task3.task3 import TreeItem, TreeModel


class FileHandler:
    def read_ini(self, file_path):
        config = ConfigParser()
        config.read(file_path)
        return config

    def write_ini(self, data, file_path):
        with open(file_path, 'w') as file:
            data.write(file)

    def read_json(self, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data

    def write_json(self, data, file_path):
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

    def read_xml(self, file_path):
        tree = ET.parse(file_path)
        return tree.getroot()

    def write_xml(self, data, file_path):
        tree = ET.ElementTree(data)
        tree.write(file_path, encoding='utf-8', xml_declaration=True)


def convert_to_treeitem(data, parent=None):
    if isinstance(data, dict):
        for key, value in data.items():
            item = TreeItem([key], parent)
            parent.appendChild(item)
            convert_to_treeitem(value, item)
    elif isinstance(data, list):
        for index, value in enumerate(data):
            item = TreeItem([str(index)], parent)
            parent.appendChild(item)
            convert_to_treeitem(value, item)
    else:
        item = TreeItem([str(data)], parent)
        parent.appendChild(item)


def convert_treeitem_to_dict(item):
    if item.childCount() > 0:
        result = {}
        for child in item.childItems:
            result[child.data(0)] = convert_treeitem_to_dict(child)
        return result
    else:
        return item.data(0)

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
            handler = FileHandler()
            if file_path.endswith('.ini'):
                config = handler.read_ini(file_path)
                data = {section: dict(config.items(section)) for section in config.sections()}
                self.model.load_from_dict(data)
            elif file_path.endswith('.json'):
                data = handler.read_json(file_path)
                self.model.load_from_dict(data)
            elif file_path.endswith('.xml'):
                root = handler.read_xml(file_path)
                data = self.xml_to_dict(root)
                self.model.load_from_dict(data)

    def saveFile(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "INI Files (*.ini);;JSON Files (*.json);;XML Files (*.xml)")
        if file_path:
            handler = FileHandler()
            data = self.model.to_dict()
            if file_path.endswith('.ini'):
                config = ConfigParser()
                for key, value in data.items():
                    config[key] = value if isinstance(value, dict) else {'value': value}
                handler.write_ini(config, file_path)
            elif file_path.endswith('.json'):
                handler.write_json(data, file_path)
            elif file_path.endswith('.xml'):
                root = self.dict_to_xml("root", data)
                handler.write_xml(root, file_path)

    def xml_to_dict(self, root):
        result = {}
        for element in root:
            if len(element):
                result[element.tag] = self.xml_to_dict(element)
            else:
                result[element.tag] = element.text
        return result

    def dict_to_xml(self, tag, d):
        elem = ET.Element(tag)
        for key, val in d.items():
            child = ET.SubElement(elem, key)
            if isinstance(val, dict):
                child.extend(self.dict_to_xml(key, val))
            else:
                child.text = str(val)
        return elem


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
