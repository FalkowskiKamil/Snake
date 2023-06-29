from config import *
import random


class Food:
    def __init__(self, canvas, config):
        self.canvas = canvas
        self.area = config.area
        x = random.randint(0, (self.area / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (self.area / SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]

        self.canvas.create_oval(
            x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food"
        )
