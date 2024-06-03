import sys
import threading
import random
import time
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit, QGridLayout, QHBoxLayout, QInputDialog
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from PyQt5.QtGui import QPixmap

class FlowerBed(QObject):
    flower_watered = pyqtSignal(int, str)

    def __init__(self, num_flowers):
        super().__init__()
        self.flowers = ['wilted'] * num_flowers
        self.lock = threading.Lock()

    def water_flower(self, flower_index):
        with self.lock:
            if self.flowers[flower_index] == 'wilted':
                self.flowers[flower_index] = 'watered'
                self.flower_watered.emit(flower_index, "Watered")
                time.sleep(random.uniform(0.1, 0.5))
            else:
                self.flower_watered.emit(flower_index, "Already watered")

    def reset_flowers(self):
        with self.lock:
            self.flowers = ['wilted'] * len(self.flowers)
            for i in range(len(self.flowers)):
                self.flower_watered.emit(i, "Reset")

class Gardener(threading.Thread):
    def __init__(self, flower_bed):
        super().__init__()
        self.flower_bed = flower_bed
        self._stop_event = threading.Event()

    def run(self):
        while not self._stop_event.is_set():
            flower_index = random.randint(0, len(self.flower_bed.flowers) - 1)
            self.flower_bed.water_flower(flower_index)
            time.sleep(random.uniform(0.5, 2.0))

    def stop(self):
        self._stop_event.set()

class FlowerApp(QWidget):
    def __init__(self):
        super().__init__()

        self.num_flowers, ok_pressed = QInputDialog.getInt(self, "Enter number of flowers", "Number of flowers:", 10, 1, 100, 1)
        if not ok_pressed:
            sys.exit()

        self.num_gardeners, ok_pressed = QInputDialog.getInt(self, "Enter number of gardeners", "Number of gardeners:", 2, 1, 10, 1)
        if not ok_pressed:
            sys.exit()

        self.flower_bed = FlowerBed(self.num_flowers)
        self.flower_bed.flower_watered.connect(self.update_flower_status)

        self.gardeners = [Gardener(self.flower_bed) for _ in range(self.num_gardeners)]

        self.initUI()
        self.start_gardeners()

    def initUI(self):
        self.setWindowTitle('Flower Garden')
        self.setGeometry(100, 100, 600, 600)

        main_layout = QVBoxLayout()

        self.grid = QGridLayout()
        self.flower_labels = []

        for i in range(len(self.flower_bed.flowers)):
            label = QLabel(self)
            label.setPixmap(QPixmap('bad.png').scaled(50, 50, Qt.KeepAspectRatio))
            self.grid.addWidget(label, i // 5, i % 5)
            self.flower_labels.append(label)

        main_layout.addLayout(self.grid)

        self.sun_button = QPushButton('Sun', self)
        self.sun_button.clicked.connect(self.reset_flowers)
        main_layout.addWidget(self.sun_button)

        self.log = QTextEdit(self)
        self.log.setReadOnly(True)
        main_layout.addWidget(self.log)

        self.setLayout(main_layout)

    def start_gardeners(self):
        for gardener in self.gardeners:
            gardener.start()

    def stop_gardeners(self):
        for gardener in self.gardeners:
            gardener.stop()

    def reset_flowers(self):
        self.flower_bed.reset_flowers()
        self.log.append("All flowers reset by the sun button.")

    def update_flower_status(self, index, status):
        if status == "Watered":
            self.flower_labels[index].setPixmap(QPixmap('good.png').scaled(50, 50, Qt.KeepAspectRatio))
            self.log.append(f"Flower {index} has been watered.")
        elif status == "Already watered":
            self.log.append(f"Flower {index} was already watered.")
        elif status == "Reset":
            self.flower_labels[index].setPixmap(QPixmap('bad.png').scaled(50, 50, Qt.KeepAspectRatio))
            self.log.append(f"Flower {index} has been reset.")

def main():
    app = QApplication(sys.argv)
    flower_app = FlowerApp()
    flower_app.show()
    sys.exit(app.exec_())

    flower_app.stop_gardeners()

if __name__ == "__main__":
    main()
