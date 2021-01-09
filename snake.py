from random import randint
import tkinter as tk
from PIL import Image, ImageTk

move_increment = 20
moves_per_second = 1
game_speed = 1000 // moves_per_second
g_width = 300
g_height = 320


class Snake(tk.Canvas):
    def __init__(self):
        super().__init__(width=g_width, height=g_height, background="black", highlightthickness=0)
        self.snake_positions = [(100, 100), (80, 100), (60, 100)]
        self.food_position = self.set_new_food_position()
        self.bonus_position = self.set_new_bonus_position()
        self.score = 0
        self.directions = "Right"
        self.bind_all("<Key>", self.on_key_press)
        self.load_assets()
        self.create_objects()
        self.after(game_speed, self.perform_actions)

    def load_assets(self):
        try:
            self.snake_body_image = Image.open("./assets/snake.png")
            self.snake_body = ImageTk.PhotoImage(self.snake_body_image)

            self.food_image = Image.open("./assets/food.png")
            self.food = ImageTk.PhotoImage(self.food_image)

            self.bonus_image = Image.open("./assets/bonus.png")
            self.bonus = ImageTk.PhotoImage(self.bonus_image)

        except IOError as error:
            global root
            root.destroy()
            raise

    def create_objects(self):
        self.create_text(
            100, 12, text=f"Score {self.score} (speed: {moves_per_second})",
            tag="score", fill="#fff", font=("TkDefaultFront", 14))

        for x_position, y_position in self.snake_positions:
            self.create_image(x_position, y_position, image=self.snake_body, tag="snake")

        self.create_image(*self.food_position, image=self.food, tag="food")
        self.create_image(*self.bonus_position, image=self.bonus, tag="bonus")

    def move_snake(self):
        global new_head_position
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
        self.after(game_speed, self.perform_actions)

    def check_collisions(self):
        head_x_position, head_y_position = self.snake_positions[0]
        return (head_x_position in (0, g_width)
                or head_y_position in (20, g_height)
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

            if self.score % 1 == 5:
                global moves_per_second
                moves_per_second += 1

            if self.score % 7 == 0:
                rate_grow = 0
                while rate_grow < 7:
                    self.snake_positions.append(self.snake_positions[-1])
                    self.create_image(*self.snake_positions[-1], image=self.snake_body, tag="snake")
                    rate_grow += 1
                    self.score += 1

            self.food_position = self.set_new_food_position()
            self.coords(self.find_withtag("food"), self.food_position)

            score = self.find_withtag("score")
            self.itemconfigure(score, text=f"Score: {self.score} (speed:{moves_per_second})", tag="score")

    def set_new_food_position(self):
        x_position = randint(1, (g_width // 20) - 1) * move_increment
        y_position = randint(3, (g_height // 20) - 1) * move_increment
        food_position = (x_position, y_position)

        if food_position not in self.snake_positions:
            return food_position

    def check_bonus_collision(self):
        if self.snake_positions[0] == self.bonus_position:
            global moves_per_second
            moves_per_second += 10

            self.bonus_position = self.set_new_bonus_position()
            self.coords(self.find_withtag("bonus"), self.bonus_position)

            score = self.find_withtag("score")
            self.itemconfigure(score, text=f"Score: {self.score} (speed:{moves_per_second})", tag="score")

    def set_new_bonus_position(self):
        x_position_b = randint(1, (g_width // 20) - 1) * move_increment
        y_position_b = randint(3, (g_height // 20) - 1) * move_increment
        bonus_position = (x_position_b, y_position_b)
        if bonus_position not in self.snake_positions and bonus_position not in self.food_position:
            return bonus_position

    def end_game(self):
        self.delete(tk.ALL)
        self.create_text(
            self.winfo_width() / 2,
            self.winfo_height() / 2,
            text=f"Game over! You scored {self.score}!",
            fill="#fff",
            font=14)


root = tk.Tk()
root.title("Snake")
root.resizable(False, False)


def start_snake():
    global g_width, g_height
    g_width = int(text1.get())
    g_height = int(text2.get())
    width_lable.grid_forget()
    text1.grid_forget()
    height_lable.grid_forget()
    text2.grid_forget()
    but.grid_forget()
    board = Snake()
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
