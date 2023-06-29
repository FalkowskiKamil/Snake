import tkinter as tk
from config import *
from data_manager import DataManager
from game import GameLogic
import pygame


class SnakeGui:
    def __init__(self):
        self.data = DataManager()
        self.config = Config()
        self.window = tk.Tk()
        self.window
        self.window.resizable(False, False)
        self.logo_image = tk.PhotoImage(file="media/logo.png")
        self.window.iconphoto(False, self.logo_image)

        self.canvas = tk.Canvas(
            self.window,
            bg=BACKGROUND_COLOR,
            height=self.config.area,
            width=self.config.area,
        )
        self.canvas.pack()

        self.recalculate_window_size()
        self.bind_list = []

        pygame.mixer.init()
        self.logo()

    def logo(self):
        # Displaying intro/logo screen
        self.config.play_sound_effect_or_background("media/logo.mp3")
        self.bind("menu")
        self.canvas.create_text(
            self.canvas.winfo_width() / 2,
            (self.canvas.winfo_height() / 12),
            font=("consolas", 50),
            text="Snake",
            fill="red",
            tag="game_over",
        )

        self.canvas.create_image(
            self.canvas.winfo_width() / 2,
            self.canvas.winfo_height() / 2,
            image=self.logo_image,
        )

        self.canvas.create_text(
            self.canvas.winfo_width() / 2,
            self.canvas.winfo_width() - 80,
            font=("consolas", 15),
            text="Press any key to continue",
            fill="white",
            justify=tk.CENTER,
            tags="ranking_restart",
        )

        self.window.mainloop()
        self.main()

    def main(self):
        # Main game flow
        self.bind("main")
        self.data.db_cursor.execute(
            "SELECT username, difficult, sound, area FROM setting ORDER BY rowid DESC LIMIT 1"
        )
        setting = self.data.db_cursor.fetchone()
        # Checking if setting alredy exist
        if setting:
            self.config.username = setting[0]
            self.config.difficult = setting[1]
            self.config.sound = setting[2]
            self.config.area = setting[3]
            self.config.set_area(self.config.area, self.canvas, self.window)
            self.menu()
        else:
            self.setting()

    def menu_control(self, direction):
        # Setting key control in menu and underlining focused option
        current_id = self.current_item
        if current_id in self.items:
            current_index = self.items.index(current_id)
            if direction == "down":
                if current_index < len(self.items) - 1:
                    self.current_item = self.items[current_index + 1]
                else:
                    self.current_item = self.items[0]
            elif direction == "up":
                if current_index != 0:
                    self.current_item = self.items[current_index - 1]
                else:
                    self.current_item = self.items[len(self.items) - 1]
            self.canvas.itemconfigure(current_id, fill="red", font=("consolas", 40))
            self.canvas.focus(self.current_item)
            self.config.underline_on_focus(None, self.canvas, self.current_item)

    def menu(self):
        # Menu view
        self.recalculate_window_size()
        self.config.check_background_music(self.config.sound)
        self.canvas.delete(tk.ALL)
        self.bind("main")
        self.items = []

        start_text = self.canvas.create_text(
            self.canvas.winfo_width() / 2,
            self.canvas.winfo_height() / 2 - 150,
            font=("consolas", 40),
            text="Start",
            fill="red",
            tag="start",
        )
        self.items.append(start_text)

        setting_text = self.canvas.create_text(
            self.canvas.winfo_width() / 2,
            (self.canvas.winfo_height() / 2) - 50,
            font=("consolas", 40),
            text="Setting",
            fill="red",
            tag="setting",
        )
        self.items.append(setting_text)

        ranking_text = self.canvas.create_text(
            self.canvas.winfo_width() / 2,
            (self.canvas.winfo_height() / 2) + 50,
            font=("Consolas", 40),
            text="Ranking",
            fill="red",
            tag="ranking",
        )
        self.items.append(ranking_text)

        exit_text = self.canvas.create_text(
            self.canvas.winfo_width() / 2,
            (self.canvas.winfo_height() / 2) + 150,
            font=("Consolas", 40),
            text="Exit",
            fill="red",
            tag="exit",
        )
        self.items.append(exit_text)

        self.current_item = self.items[0]
        self.canvas.tag_raise(self.current_item)
        self.config.underline_on_focus(None, self.canvas, self.current_item)

    def execute_action(self):
        # Execute enter key from menu
        if self.current_item == self.items[0]:
            self.start_game()
        elif self.current_item == self.items[1]:
            self.setting()
        elif self.current_item == self.items[2]:
            self.ranking()
        elif self.current_item == self.items[3]:
            exit()

    def ranking(self):
        # Ranking view
        self.bind("menu")
        self.canvas.delete("all")
        self.canvas.create_text(
            self.canvas.winfo_width() / 2,
            self.canvas.winfo_height() / 8,
            font=("consolas", 40),
            text="Ranking",
            fill="white",
            justify=tk.CENTER,
            tags="ranking_title",
        )

        self.data.db_cursor.execute(
            "SELECT username, score, difficult, area, date FROM scores ORDER BY score DESC LIMIT 10"
        )
        scores = self.data.db_cursor.fetchall()

        y = self.canvas.winfo_height() / 8 + 60
        for index, (username, score, difficult, area, date) in enumerate(scores):
            self.canvas.create_text(
                self.canvas.winfo_width() / 2,
                y,
                font=("consolas", 25),
                text=f"{index + 1}. {username}: {score} ({difficult}) {area}x{area}",
                fill="white",
                justify=tk.CENTER,
                tags="ranking_scores",
            )
            y += 30

        self.canvas.create_text(
            self.canvas.winfo_width() / 2,
            y + 50,
            font=("consolas", 15),
            text="Press any key to back to menu",
            fill="white",
            justify=tk.CENTER,
            tags="ranking_restart",
        )

    def setting(self):
        # Setting view
        self.bind("menu")

        # Preparing setting window
        setting_window = tk.Toplevel(self.window)
        setting_window.title("Setting")
        setting_window.geometry(
            f"{int(self.screen_width / 6)}x{int(self.screen_height / 2.5)}+{int(self.window_width)}+{int(self.window_height / 2)}"
        )
        setting_window.resizable(False, False)
        canvas = tk.Canvas(setting_window, bg="white")
        canvas.pack(fill=tk.BOTH, expand=True)

        # Username section
        username_frame = tk.Frame(canvas, bg="white")
        username_frame.pack(pady=20)

        label2 = tk.Label(
            username_frame,
            text="Your username:",
            font=("Arial", 14, "bold"),
            bg="white",
        )
        label2.pack(side=tk.LEFT, padx=10)

        entry2 = tk.Entry(username_frame)
        entry2.pack(side=tk.LEFT)

        if self.config.username:
            entry2.insert(0, self.config.username)

        # Difficulty section
        difficulty_frame = tk.Frame(canvas, bg="white")
        difficulty_frame.pack(pady=20)

        label = tk.Label(
            difficulty_frame,
            text="Choose difficulty:",
            font=("Arial", 14, "bold"),
            bg="white",
        )
        label.pack(side=tk.LEFT, padx=10)

        difficulties = [("Easy", "green"), ("Medium", "orange"), ("Hard", "red")]
        self.difficult_buttons = []

        for difficulty, color in difficulties:
            difficult_frame_button = tk.Frame(difficulty_frame, bg="white")
            difficult_frame_button.pack(side=tk.TOP, padx=10)

            difficult_button = tk.Button(
                difficult_frame_button,
                text=difficulty,
                bg=color,
                font=("Arial", 12, "bold"),
                width=20,
                command=lambda diff=difficulty: self.config.set_difficult(
                    diff, self.difficult_buttons
                ),
            )

            if self.config.difficult == difficulty:
                difficult_button.config(font=("Arial", 14, "bold underline"))

            difficult_button.pack()
            self.difficult_buttons.append(difficult_button)
        # Area section
        area_frame = tk.Frame(canvas, bg="white")
        area_frame.pack(pady=20)

        question_label = tk.Label(
            area_frame, text="What area (X.Y)?", font=("Arial", 14, "bold"), bg="white"
        )
        question_label.pack(side=tk.LEFT, padx=10)

        answer_options = [10, 14, 18, 20]
        selected_area = tk.StringVar(canvas)
        selected_area.set(int(self.config.area / 50))
        option_menu_frame = tk.Frame(area_frame, bg="white")
        option_menu_frame.pack(side=tk.LEFT)
        option_menu = tk.OptionMenu(
            area_frame,
            selected_area,
            *answer_options,
            command=lambda value: self.config.set_area(value, self.canvas, self.window),
        )
        option_menu.config(font=("Arial", 12, "bold"))
        option_menu.pack(side=tk.LEFT, padx=5)

        # Music section
        music_frame = tk.Frame(canvas, bg="white")
        music_frame.pack(pady=10)

        label3 = tk.Label(
            music_frame, text="Music", font=("Arial", 14, "bold"), bg="white"
        )
        label3.pack(side=tk.LEFT, padx=10)

        music_var = tk.BooleanVar(value=bool(self.config.sound))
        music = tk.Checkbutton(
            music_frame,
            variable=music_var,
            command=lambda: self.config.check_background_music(music_var.get()),
            bg="white",
        )
        music.pack(side=tk.LEFT, padx=5)

        # control section
        control_frame = tk.Frame(canvas, bg="white")
        control_frame.pack(pady=10)

        label4 = tk.Label(
            control_frame, text="Mouse control", font=("Arial", 14, "bold"), bg="white"
        )
        label4.pack(side=tk.LEFT, padx=10)

        control_var = tk.BooleanVar(value=bool(self.config.control != "keybord"))
        control = tk.Checkbutton(
            control_frame,
            variable=control_var,
            command=lambda: self.config.set_control(control_var.get()),
            bg="white",
        )
        control.pack(side=tk.LEFT, padx=10)

        # Send button
        send_button = tk.Button(
            canvas,
            text="Send",
            font=("Arial", 12, "bold"),
            command=lambda: self.config.set_setting(
                entry2.get(), setting_window, self.menu
            ),
        )
        send_button.pack(pady=10)

    def start_game(self):
        # Preparing start - game
        pygame.mixer.music.stop()
        self.bind(f"game_{self.config.control}")
        self.game_logic = GameLogic(self, self.data)
        self.game_logic.start_game()

    def game_over(self):
        # Game-over view
        self.canvas.delete(tk.ALL)
        self.recalculate_window_size(add=-50)
        self.bind("menu")
        self.canvas.create_text(
            self.canvas.winfo_width() / 2,
            self.canvas.winfo_height() / 2,
            font=("consolas", 70),
            text="GAME OVER",
            fill="red",
            tag="game_over",
        )
        self.canvas.create_text(
            self.canvas.winfo_width() / 2,
            self.canvas.winfo_width() - 100,
            font=("consolas", 15),
            text="Press any key to back to menu",
            fill="white",
            justify=tk.CENTER,
            tags="ranking_restart",
        )
        self.window.bind("<Key>", lambda event: self.menu())

    def recalculate_window_size(self, add=0):
        # Recalculate window size based on area setting
        self.window.update()
        self.window_width = self.window.winfo_width()
        self.window_height = self.window.winfo_height() + add
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()
        x = int((self.screen_width / 2) - (self.window_width / 2))
        y = int((self.screen_height / 2) - (self.window_height / 2))

        self.window.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")

    def bind(self, type=""):
        # Binding delete button
        self.window.protocol("WM_DELETE_WINDOW", lambda: exit())
        # Clear bind
        self.unbind()
        match type:
            case "main":
                self.canvas.tag_bind(
                    "start", "<Button-1>", lambda event: self.start_game()
                )
                self.canvas.tag_bind(
                    "setting", "<Button-1>", lambda event: self.setting()
                )
                self.canvas.tag_bind(
                    "ranking", "<Button-1>", lambda event: self.ranking()
                )
                self.window.bind("<Down>", lambda event: self.menu_control("down"))
                self.window.bind("<Up>", lambda event: self.menu_control("up"))
                self.window.bind("<Return>", lambda event: self.execute_action())
                self.window.bind("<Escape>", lambda event: exit())

                self.bind_list = ["<Return>", "<Escape>", "<Down>", "<Up>"]
            case "game_keybord":
                # Bind when play with keybord
                self.window.bind(
                    "<Left>", lambda event: self.game_logic.change_direction("left")
                )
                self.window.bind(
                    "<Right>", lambda event: self.game_logic.change_direction("right")
                )
                self.window.bind(
                    "<Up>", lambda event: self.game_logic.change_direction("up")
                )
                self.window.bind(
                    "<Down>", lambda event: self.game_logic.change_direction("down")
                )
                self.bind_list = ["<Left>", "<Right>", "<Up>", "<Down>"]
            case "game_mouse":
                # Bind when play with mouse
                self.window.bind(
                    "<Motion>", lambda event: self.game_logic.get_mouse_position(event)
                )
                self.bind_list = ["<Motion>"]

            case "menu":
                self.window.bind("<Key>", lambda event: self.main())
                self.bind_list = ["<Key>"]

    def unbind(self):
        # Clearing all of the bind from bind list
        if len(self.bind_list) > 0:
            for list_element in self.bind_list:
                self.window.unbind(list_element)
            self.bind_list = []
