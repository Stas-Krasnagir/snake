from random import randint
import tkinter as tk
from PIL import Image, ImageTk

move_increment = 20
moves_per_second = 7
game_speed = 1000 // moves_per_second
g_width = 600
g_height = 620


class StartPage:
    def __init__(self):

        self.width_lable = tk.Label(text="Set width:", font="Arial 14")
        self.text1 = tk.Entry()
        self.height_lable = tk.Label(text="Set height:", font="Arial 14")
        self.text2 = tk.Entry()
        self.but = tk.Button(text="Start", font="Arial 20", command=self.start_snake)
        self.lebel = tk.Label(width=27, font=15)

        self.width_lable.grid(column=0, row=0)
        self.text1.grid(column=1, row=0)

        self.height_lable.grid(column=0, row=1)
        self.text2.grid(column=1, row=1)
        self.but.grid(column=1, row=3)

    def start_snake(self):
        global g_width, g_height
        g_width = int(self.text1.get())
        g_height = int(self.text2.get())

        new_window = tk.Toplevel()
        new_window.title("New Window")
        new_window.resizable(False, False)
        new_window.board = Snake()
        #new_window.board.pack()









class Snake(tk.Canvas):  # Создаем класс для записи атрибутов змейки
    # (суперкласс для унаследования атрибутов основного класса)
    # созадли для передачи свойств на холст
    def __init__(self):
        super().__init__(width=g_width, height=g_height, background="black", highlightthickness=0)
        # задали размер и фон окна (толщина святового пятна,
        # highlightthickness - рамка активного окна, если 0 - рамки не видно)

        self.snake_positions = [(100, 100), (80, 100), (60, 100)]
        # задали кортеж с координатами x и y начального положения тела змеи

        self.food_position = self.set_new_food_position()
        # вызываем функцию для нового расположения еды
        self.bonus_position = self.set_new_bonus_position()

        self.score = 0

        self.directions = "Right"
        self.bind_all("<Key>", self.on_key_press)

        self.load_assets()

        self.create_objects()  # метод для размещения элементы на активном окне игры

        self.after(game_speed, self.perform_actions)  # вызываем первый раз

    def load_assets(self):  # метод позволяющий импортировать изображения
        # обработка исключенийй, обернутая конструкция try/except
        try:  # используем try если не закиним ихображения в корень с файлом приложения
            self.snake_body_image = Image.open("./assets/snake.png")  # считываем файл изображения
            self.snake_body = ImageTk.PhotoImage(self.snake_body_image)
            # переменная для втавки в класс изображения тела змеи

            self.food_image = Image.open("./assets/food.png")
            self.food = ImageTk.PhotoImage(self.food_image)

            self.bonus_image = Image.open("./assets/bonus.png")
            self.bonus = ImageTk.PhotoImage(self.bonus_image)

        except IOError as error:
            # IOError – возникает в том случае, когда операция I/O
            # (такая как оператор вывода, встроенная функция open() или метод объекта-файла) не может быть выполнена,
            # по связанной с I/O причине: «файл не найден», или «диск заполнен», иными словами.
            global root
            root.destroy()  # закроет окно приложения в случае ошибки
            raise

    def create_objects(self):
        self.create_text(
            100, 12, text=f"Score {self.score} (speed: {moves_per_second})",
            tag="score", fill="#fff", font=("TkDefaultFront", 14))
        # метод для размещения текста на холсте.
        # Задаем х и у, текст с использованием ф-стринг, устанавливаем цвет текста и его фон, кегель

        for x_position, y_position in self.snake_positions:
            # перебераем занчения х и у для отрисовки змейки на холсте
            self.create_image(x_position, y_position, image=self.snake_body, tag="snake")

        self.create_image(*self.food_position, image=self.food, tag="food")
        # метод для размещения еды на холсте
        # (self.food_position[0], self.food_position[1]) заменили
        # на * для сокращения кода, первая переменная не используется)
        self.create_image(*self.set_new_bonus_position(), image=self.bonus, tag="bonus")

    def move_snake(self):
        global new_head_position
        head_x_position, head_y_position = self.snake_positions[0]
        # связали переменные с координатом головы змейки
        # в зависимости от нажатой клавиши меняем координаты головы змейки
        if self.directions == "Left":
            new_head_position = (head_x_position - move_increment, head_y_position)
        elif self.directions == "Right":
            new_head_position = (head_x_position + move_increment, head_y_position)
        elif self.directions == "Down":
            new_head_position = (head_x_position, head_y_position + move_increment)
        elif self.directions == "Up":
            new_head_position = (head_x_position, head_y_position - move_increment)

        self.snake_positions = [new_head_position] + self.snake_positions[:-1]
        # обнавляем положение тела змейки на холсте с учетом изменений при движении.
        # В "листе" меняем первый элемент на новые координаты положения головы змейки + положение до(- хвост)

        for segment, position in zip(self.find_withtag("snake"), self.snake_positions):
            # цикл для проверки на ограничения (края прямоугольника)

            # zip - Создайте итератор, который объединяет элементы из каждой итерации. Возвращает итератор кортежей,
            # где i-й кортеж содержит i-й элемент из каждой из последовательностей аргументов или итераций.
            # https://docs.python.org/3/library/functions.html#zip

            # find_withtag метод tkinter для поиска объектов по тегу

            self.coords(segment, position)

    def perform_actions(self):
        if self.check_collisions():
            self.end_game()
            return  # наступление крайнего события -> True
        self.move_snake()
        self.check_food_collision()
        self.check_bonus_collision()
        self.after(game_speed, self.perform_actions)  # каждые 75 мс вызывает функцию
        # .after - метод Tkinter, .after(parent, ms, function = None, *args) где:
        # parent: is the object of the widget or main window whichever is using this function.
        # ms: is the time in miliseconds.
        # function: which shall be called.
        # *args: other options.

    def check_collisions(self):  # метод для проверки наступления крайних событий, возвращает boolean
        head_x_position, head_y_position = self.snake_positions[0]
        return (head_x_position in (0, g_width)  # пересечение х
                or head_y_position in (20, g_height)  # пересечение у
                or (head_x_position, head_y_position) in self.snake_positions[1:])  # пересечение тела змейки

    def on_key_press(self, e):
        new_direction = e.keysym
        all_directions = ("Up", "Down", "Left", "Right")
        opposites = ({"Up", "Down"}, {"Left", "Right"})
        if new_direction in all_directions and {new_direction, self.directions} not in opposites:
            # проверка на движение в себя
            self.directions = new_direction

    def check_food_collision(self):
        if self.snake_positions[0] == self.food_position:
            self.score += 1
            self.snake_positions.append(self.snake_positions[-1])
            # добовляет последний элемент тела змейки в конец списка тем самым увеличивая ее размер
            self.create_image(*self.snake_positions[-1], image=self.snake_body, tag="snake")

            if self.score % 5 == 0:
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
        # проверка для респа новой позиции еды вне тела змейки

    def check_bonus_collision(self):
        if self.snake_positions[0] == self.bonus_position:
            global moves_per_second
            moves_per_second += 5
            self.bonus_position = self.set_new_bonus_position()

    def set_new_bonus_position(self):
        x_position = randint(1, (g_width // 20) - 1) * move_increment
        y_position = randint(3, (g_height // 20) - 1) * move_increment
        bonus_position = (x_position, y_position)
        if bonus_position not in self.snake_positions and bonus_position not in self.food_position:
            return bonus_position

    def end_game(self):
        self.delete(tk.ALL)
        # метод ТК, удаляет все с активного окна
        self.create_text(
            self.winfo_width() / 2,
            self.winfo_height() / 2,
            text=f"Game over! You scored {self.score}!",
            fill="#fff",
            font=14)


def main():
    root = tk.Tk()
    root.title("Snake")
    root.resizable(False, False)
    canvas = tk.Canvas()
    app = StartPage()
    # board = Snake()
    # board.pack()
    root.mainloop()

main()
