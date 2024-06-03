import json
import xml.etree.ElementTree as ET
from configparser import ConfigParser
from abc import ABC, abstractmethod


class IFileHandler(ABC):
    @abstractmethod
    def read(self, file_path):
        pass

    @abstractmethod
    def write(self, data, file_path):
        pass


class INIFileHandler(IFileHandler):
    def read(self, file_path):
        config = ConfigParser()
        config.read(file_path)
        return {section: dict(config.items(section)) for section in config.sections()}

    def write(self, data, file_path):
        config = ConfigParser()
        for key, value in data.items():
            config[key] = value if isinstance(value, dict) else {'value': value}
        with open(file_path, 'w') as file:
            config.write(file)


class JSONFileHandler(IFileHandler):
    def read(self, file_path):
        with open(file_path, 'r') as file:
            return json.load(file)

    def write(self, data, file_path):
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)


class XMLFileHandler(IFileHandler):
    def read(self, file_path):
        tree = ET.parse(file_path)
        return self.xml_to_dict(tree.getroot())

    def write(self, data, file_path):
        root = self.dict_to_xml('root', data)
        tree = ET.ElementTree(root)
        tree.write(file_path, encoding='utf-8', xml_declaration=True)

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


class FileHandlerFactory:
    @staticmethod
    def get_handler(file_type):
        if file_type == 'ini':
            return INIFileHandler()
        elif file_type == 'json':
            return JSONFileHandler()
        elif file_type == 'xml':
            return XMLFileHandler()
        else:
            raise ValueError("Unsupported file type")
