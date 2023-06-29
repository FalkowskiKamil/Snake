from datetime import datetime
from config import *
from snake import Snake
from food import Food
import tkinter as tk

currentDateAndTime = datetime.now()


class GameLogic:
    def __init__(self, window, db):
        self.window = window
        self.db = db
        self.score = 0
        self.direction = "down"
        self.speed = self.window.config.speed

    def next_turn(self):
        # Update snake coordinates based on direction
        x, y = self.snake.coordinates[0]

        if self.direction == "up":
            y -= SPACE_SIZE
        elif self.direction == "down":
            y += SPACE_SIZE
        elif self.direction == "left":
            x -= SPACE_SIZE
        elif self.direction == "right":
            x += SPACE_SIZE

        self.snake.coordinates.insert(0, (x, y))
        square = self.window.canvas.create_rectangle(
            x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR
        )
        self.snake.squares.insert(0, square)

        # Check if snake ate the food
        if x == self.food.coordinates[0] and y == self.food.coordinates[1]:
            self.score += 1
            if self.score % 5 == 0:
                self.speed -= 10

            self.label.config(text=f"Score: {self.score}")
            self.window.canvas.delete("food")
            self.window.config.play_sound_effect_or_background("media/food.mp3")
            self.food = Food(self.window.canvas, self.window.config)
        else:
            # Remove last body part of snake
            del self.snake.coordinates[-1]
            self.window.canvas.delete(self.snake.squares[-1])
            del self.snake.squares[-1]

        if self.check_collision():
            self.save_score()
        else:
            self.window.window.after(self.speed, self.next_turn)

    def change_direction(self, new_direction):
        # Change direction if not opposite to current direction
        if new_direction == "left" and self.direction != "right":
            self.direction = new_direction
        elif new_direction == "right" and self.direction != "left":
            self.direction = new_direction
        elif new_direction == "up" and self.direction != "down":
            self.direction = new_direction
        elif new_direction == "down" and self.direction != "up":
            self.direction = new_direction

    def get_mouse_position(self, event):
        # Calculate direction change when playing with mouse
        x, y = self.snake.coordinates[0]
        if abs(event.x - x) > 60:
            if event.x > x:
                self.change_direction("right")
            else:
                self.change_direction("left")
        if abs(event.y - y) > 60:
            if event.y > y:
                self.change_direction("down")
            else:
                self.change_direction("up")

    def check_collision(self):
        # Check if snake is out of game area
        x, y = self.snake.coordinates[0]

        if x < 0 or x >= int(self.window.config.area):
            return True
        elif y < 0 or y >= int(self.window.config.area):
            return True

        # Check if snake collided with itself
        for body_part in self.snake.coordinates[1:]:
            if x == body_part[0] and y == body_part[1]:
                return True

        return False

    def save_score(self):
        # Save score after collision
        self.window.config.play_sound_effect_or_background("media/lose.mp3")
        date = currentDateAndTime.strftime("%d-%m-%Y")
        area = int(self.window.config.area) / 50
        self.db.save_score(
            self.window.config.username,
            self.score,
            self.window.config.difficult,
            area,
            date,
        )
        self.label.pack_forget()
        self.window.game_over()

    def start_game(self):
        # Start a new game and display the scoreboard
        self.score = 0
        self.direction = "down"
        self.window.canvas.delete(tk.ALL)
        self.snake = Snake(self.window.canvas)
        self.food = Food(self.window.canvas, self.window.config)
        self.label = tk.Label(
            self.window.window, text=f"Score: 0", font=("consolas", 40)
        )
        self.label.pack()
        self.window.recalculate_window_size(add=50)
        self.next_turn()
