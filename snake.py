from tkinter import *

root = Tk()

but_up = Button(root, text="Up", width=7, height=3)
but_down = Button(root, text="Down", width=7, height=3)
but_left = Button(root, text="Left", width=7, height=3)
but_right = Button(root, text="Right", width=7, height=3)

but_up['activebackground'] = '#555555'
but_down['activebackground'] = '#555555'
but_left['activebackground'] = '#555555'
but_right['activebackground'] = '#555555'

but_right.pack(side='right', padx=10, pady=10)
but_left.pack(side='left', padx=10, pady=10)
but_up.pack(side='top', padx=10, pady=10)
but_down.pack(side='bottom', padx=10, pady=10)

root.mainloop()

# Далее, чтобы написать GUI-программу, надо выполнить приблизительно следующее:
# Создать главное окно.
# Создать виджеты и выполнить конфигурацию их свойств (опций).
# Определить события, то есть то, на что будет реагировать программа.
# Описать обработчики событий, то есть то, как будет реагировать программа.
# Расположить виджеты в главном окне.
# Запустить цикл обработки событий.
