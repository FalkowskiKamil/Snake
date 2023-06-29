# First run config
GAME_WIDTH = 700
GAME_HEIGHT = 700
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"
USERNAME = "Anonim"
DIFFICULT = "Easy"
SOUND = True
SPEED = 100
CONTROL = "keybord"
import pygame
from data_manager import DataManager


class Config:
    def __init__(self):
        self.difficult = DIFFICULT
        self.username = USERNAME
        self.speed = SPEED
        self.area = GAME_WIDTH
        self.sound = SOUND
        self.control = CONTROL
        self.data = DataManager()

    def play_sound_effect_or_background(self, sound_file, background=False):
        # Play sound / background music
        if background:
            pygame.mixer.music.load("media/background.mp3")
            pygame.mixer.music.play(-1)
        else:
            sound = pygame.mixer.Sound(sound_file)
            sound.play()

    def check_background_music(self, config_sound):
        # Checking and changing config setting
        if config_sound:
            self.sound = True
            self.play_sound_effect_or_background(
                "media/background.mp3", background=True
            )
        else:
            self.sound = False
            pygame.mixer.music.stop()

    def underline_on_focus(self, event, canvas, current_item):
        # Underline menu option
        canvas.itemconfigure(
            current_item, fill="orange", font=("consolas", 40, "underline")
        )

    def set_control(self, mouse_control):
        # Setting control with mouse or keyboard
        if mouse_control:
            self.control = "mouse"
        else:
            self.control = "keyboard"

    def set_setting(self, username, setting_window, menu):
        # Save change of setting
        self.username = username
        self.data.add_setting(
            self.username,
            self.difficult,
            self.sound,
            int(self.area / 50),
            self.control,
        )
        setting_window.destroy()
        menu()

    def set_area(self, selected_area, canvas, window):
        # Setting play area and window size
        area = int(selected_area) * 50
        self.area = area
        canvas.config(width=area, height=area)
        window.geometry(f"{area}x{area}")

    def set_difficult(self, difficult, difficult_buttons):
        # Setting difficult
        self.difficult = difficult
        # Change difficult button font size and changing underline
        for difficult_button in difficult_buttons:
            if difficult_button["text"] == self.difficult:
                difficult_button.config(font=("Arial", 14, "bold underline"))
            else:
                difficult_button.config(font=("Arial", 12, "bold"))
