from random import randint
import tkinter as tk
from PIL import Image, ImageTk

move_increment = 20


class Snake(tk.Canvas):
    def __init__(self, width, height):
        super().__init__(width=width, height=height, background="black", highlightthickness=0)
        self.width = width
        self.height = height

        self.snake_positions = [(100, 100), (80, 100), (60, 100)]

        self.food_position = self.set_new_food_position()

        self.bonus_position = [-100, -100]
        self.bonus_food_position = [-100, -100]

        self.score = 0
        self.game_speed = 200
        self.directions = "Right"
        self.bind_all("<Key>", self.on_key_press)
        self.load_assets()
        self.create_objects()
        self.waiting_time = 10000
        self.after(self.waiting_time, self.init_bonus)
        self.after(self.game_speed, self.perform_actions)

    def load_assets(self):
        try:
            self.snake_body_image = Image.open("./assets/snake.png")
            self.snake_body = ImageTk.PhotoImage(self.snake_body_image)

            self.food_image = Image.open("./assets/food.png")
            self.food = ImageTk.PhotoImage(self.food_image)

            self.bonus_image = Image.open("./assets/bonus_speed.png")
            self.bonus_speed = ImageTk.PhotoImage(self.bonus_image)

            self.bonus_food_image = Image.open("./assets/bonus_food.png")
            self.bonus_food = ImageTk.PhotoImage(self.bonus_food_image)

        except IOError as error:
            root.destroy()
            raise

    def create_objects(self):
        self.create_text(
            100, 12, text=f"Score {self.score} (speed: {self.game_speed})",
            tag="score", fill="#fff", font=("TkDefaultFront", 14))

        for x_position, y_position in self.snake_positions:
            self.create_image(x_position, y_position, image=self.snake_body, tag="snake")

        self.create_image(*self.food_position, image=self.food, tag="food")
        self.create_image(*self.bonus_position, image=self.bonus_speed, tag="bonus")
        self.create_image(*self.bonus_food_position, image=self.bonus_food, tag="bonus_food")

    def move_snake(self):
        head_x_position, head_y_position = self.snake_positions[0]
        if self.directions == "Left":
            new_head_position = (head_x_position - move_increment, head_y_position)
        elif self.directions == "Right":
            new_head_position = (head_x_position + move_increment, head_y_position)
        elif self.directions == "Down":
            new_head_position = (head_x_position, head_y_position + move_increment)
        elif self.directions == "Up":
            new_head_position = (head_x_position, head_y_position - move_increment)

        self.snake_positions = [new_head_position] + self.snake_positions[:-1]

        for segment, position in zip(self.find_withtag("snake"), self.snake_positions):
            self.coords(segment, position)

    def perform_actions(self):
        if self.check_collisions():
            self.end_game()
            return
        self.move_snake()
        self.check_food_collision()
        self.check_bonus_collision()
        self.check_bonus_food_collision()
        self.after(self.game_speed, self.perform_actions)

    def check_collisions(self):
        head_x_position, head_y_position = self.snake_positions[0]
        return (head_x_position in (0, self.width)
                or head_y_position in (20, self.height)
                or (head_x_position, head_y_position) in self.snake_positions[1:])

    def on_key_press(self, e):
        new_direction = e.keysym
        all_directions = ("Up", "Down", "Left", "Right")
        opposites = ({"Up", "Down"}, {"Left", "Right"})
        if new_direction in all_directions and {new_direction, self.directions} not in opposites:
            self.directions = new_direction

    def check_food_collision(self):
        if self.snake_positions[0] == self.food_position:
            self.score += 1
            self.snake_positions.append(self.snake_positions[-1])
            self.create_image(*self.snake_positions[-1], image=self.snake_body, tag="snake")

            if self.score % 5 == 0:
                self.game_speed -= 1

            self.food_position = self.set_new_food_position()
            self.coords(self.find_withtag("food"), self.food_position)

            score = self.find_withtag("score")
            self.itemconfigure(score, text=f"Score: {self.score} (speed:{self.game_speed})", tag="score")

    def set_new_food_position(self):
        x_position = randint(1, (self.width // 20) - 1) * move_increment
        y_position = randint(3, (self.height // 20) - 1) * move_increment
        food_position = (x_position, y_position)

        if food_position not in self.snake_positions:
            return food_position

    def check_bonus_collision(self):
        if self.snake_positions[0] == self.bonus_position:
            self.game_speed -= 75
            self.bonus_position = [-100, -100]
            self.coords(self.find_withtag("bonus"), self.bonus_position)

            score = self.find_withtag("score")
            self.itemconfigure(score, text=f"Score: {self.score} (speed:{self.game_speed})", tag="score")
            self.after(10000, self.del_bonus_speed)

    def del_bonus_speed(self):
        self.game_speed += 75
        score = self.find_withtag("score")
        self.itemconfigure(score, text=f"Score: {self.score} (speed:{self.game_speed})", tag="score")

    def set_new_bonus_position(self):
        x_position_b = randint(1, (self.width // 20) - 1) * move_increment
        y_position_b = randint(3, (self.height // 20) - 1) * move_increment
        bonus_position = (x_position_b, y_position_b)
        if bonus_position not in self.snake_positions and bonus_position not in self.food_position:
            return bonus_position

    def check_bonus_food_collision(self):
        if self.snake_positions[0] == self.bonus_food_position:
            rate_grow = 0
            while rate_grow < 10:
                self.snake_positions.append(self.snake_positions[-1])
                self.create_image(*self.snake_positions[-1], image=self.snake_body, tag="snake")
                rate_grow += 1
                self.score += 2

            self.bonus_food_position = [-100, -100]
            self.coords(self.find_withtag("bonus_food"), self.bonus_food_position)

            score = self.find_withtag("score")
            self.itemconfigure(score, text=f"Score: {self.score} (speed:{self.game_speed})", tag="score")
            self.after(10000, self.del_bonus_food)

    def del_bonus_food(self):
        rate_grow = 0
        while rate_grow < 10:
            self.snake_positions.pop()
            rate_grow += 1
        self.delete(tk.ALL)
        self.create_objects()

    def set_new_bonus_food_position(self):
        x_position_bf = randint(1, (self.width // 20) - 1) * move_increment
        y_position_bf = randint(3, (self.height // 20) - 1) * move_increment
        bonus_food_position = (x_position_bf, y_position_bf)
        if bonus_food_position not in self.snake_positions \
                and bonus_food_position not in self.food_position \
                and bonus_food_position not in self.bonus_position:
            return bonus_food_position

    def end_game(self):
        self.delete(tk.ALL)
        self.create_text(
            self.winfo_width() / 2,
            self.winfo_height() / 2,
            text=f"Game over! You scored {self.score}!",
            fill="#fff",
            font=14)
        self.button_restart = tk.Button(root, text="Try again", font="Arial 20", command=self.restart)
        self.button_restart.grid()

    def restart(self):
        self.button_restart.grid_forget()
        self.destroy()
        start_snake()

    def init_bonus(self):
        self.bonus_position = self.set_new_bonus_position()
        self.coords(self.find_withtag("bonus"), self.bonus_position)
        self.bonus_food_position = self.set_new_bonus_food_position()
        self.coords(self.find_withtag("bonus_food"), self.bonus_food_position)
        self.after((self.waiting_time * 2), self.init_bonus)


root = tk.Tk()
root.title("Snake")
root.resizable(False, False)


def start_snake():
    width = int(text1.get())
    height = int(text2.get())
    if width < 300:
        width = 300
    if height < 320:
        height = 320
    width_lable.grid_forget()
    text1.grid_forget()
    height_lable.grid_forget()
    text2.grid_forget()
    but.grid_forget()
    board = Snake(width, height)
    board.grid()


width_lable = tk.Label(root, text="Set width:", font="Arial 14")
text1 = tk.Entry(root)
height_lable = tk.Label(root, text="Set height:", font="Arial 14")
text2 = tk.Entry(root)
but = tk.Button(root, text="Start", font="Arial 20", command=start_snake)
lebel = tk.Label(root, width=27, font=15)

width_lable.grid(column=0, row=0)
text1.grid(column=1, row=0)

height_lable.grid(column=0, row=1)
text2.grid(column=1, row=1)
but.grid(column=1, row=3)

canvas = tk.Canvas()
root.mainloop()
