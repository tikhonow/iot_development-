import threading
import time
import random


class FlowerBed:
    def __init__(self, num_flowers):
        self.flowers = ['wilted'] * num_flowers
        self.lock = threading.Lock()

    def water_flower(self, flower_index):
        with self.lock:
            if self.flowers[flower_index] == 'wilted':
                print(f"Gardener {threading.current_thread().name} is watering flower {flower_index}.")
                self.flowers[flower_index] = 'watered'
                time.sleep(random.uniform(0.1, 0.5))  # Simulate watering time
                print(f"Flower {flower_index} has been watered by gardener {threading.current_thread().name}.")
            else:
                print(f"Gardener {threading.current_thread().name} found flower {flower_index} already watered.")


class Gardener(threading.Thread):
    def __init__(self, flower_bed):
        super().__init__()
        self.flower_bed = flower_bed

    def run(self):
        while True:
            flower_index = random.randint(0, len(self.flower_bed.flowers) - 1)
            self.flower_bed.water_flower(flower_index)
            time.sleep(random.uniform(0.5, 2.0))  # Simulate time between watering attempts


def main():
    n = int(input("Enter the number of flowers: "))
    m = int(input("Enter the number of gardeners: "))

    flower_bed = FlowerBed(n)

    gardeners = [Gardener(flower_bed) for _ in range(m)]

    for gardener in gardeners:
        gardener.start()

    for gardener in gardeners:
        gardener.join()


if __name__ == "__main__":
    main()
