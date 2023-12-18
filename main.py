# Импорт библиотеки tkinter под псевдонимом tk.
import tkinter as tk
# Импорт класса Label из модуля tkinter.
from tkinter import Label
# Импорт класса Button из модуля tkinter. 
from tkinter import Button
# Импорт всех объектов из модуля tkinter.
from tkinter import *
# Импорт всех объектов из модуля tkinter.
from tkinter import ttk
from tkinter import *
import socket
from subprocess import call
import time
from threading import Thread
import pickle


def start_server(n: int):
    if n == 0:
        call(['python', 'server1.py'])
    elif n == 1:
        call(['python', 'server2.py'])


def status_server(n: int):
    with open('status', 'rb') as file:
        status = pickle.load(file)

    if status[n]:
        Thread(target=start_server, args=(n,), daemon=True).start()
        print('Запуск')
        status[n] = False
        with open('status', 'wb') as file:
            pickle.dump(status, file)


def server1(event):
    status_server(0)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 5434))
    client.send('Получен запрос.'.encode('utf-8'))
    data = client.recv(1024).decode('utf-8')
    label_result.config(text='Результат: ' + data)


def server2(event):
    status_server(1)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 3333))
    client.send('Получен запрос.'.encode('utf-8'))
    data = client.recv(1024).decode('utf-8')
    label_result.config(text='Результат:\n' + data)


# Создание окна приложения.
window = tk.Tk()
# Установка заголовка окна.
window.title('Client')
# Установка заголовка окна.
window.geometry('400x300')
# Запрет изменения размеров.
window.resizable(False, False)

# Создание кнопки "Server 1" с определенными параметрами.
button_1 = tk.Button(
    text="Server 1",
    width=27,
    height=10,
    bg="white",
    fg="black",

)

# Создание кнопки "Server 2" с определенными параметрами.
button_2 = tk.Button(
    text="Server 2",
    width=27,
    height=10,
    bg="black",
    fg="white",

)

# Размещение кнопки "Server 1" в окне.
button_1.place(x=1, y=0)
# Размещение кнопки "Server 2" в окне.
button_2.place(x=200, y=0)
button_1.bind('<Button-1>', server1)
button_2.bind('<Button-1>', server2)
# Создание метки с текстом "Результат:" и заданным шрифтом.
label_result = Label(window, text='Результат:', font=("Times New Roman", 30))
# Размещение метки в окне на определенных координатах.
label_result.place(x=0, y=180)

# Запуск главного цикла обработки событий окна.
window.mainloop()

status = [True, True]

with open('status', 'wb') as file:
    pickle.dump(status, file) 
