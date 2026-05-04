import tkinter as tk
from tkinter import ttk
import random
import string
import json
import os

# Файл для хранения истории паролей
history_file = 'history.json'


# Загружаем историю паролей из файла, если он существует
def load_history():
    if os.path.exists(history_file):
        with open(history_file, 'r') as file:
            return json.load(file)
    return []


# Сохраняем историю паролей в файл
def save_history(history):
    with open(history_file, 'w') as file:
        json.dump(history, file)


# Генерация пароля
def generate_password(length, use_digits, use_letters, use_special):
    password_chars = ""
    if use_digits:
        password_chars += string.digits
    if use_letters:
        password_chars += string.ascii_letters
    if use_special:
        password_chars += string.punctuation

    if password_chars:  # Проверка на наличие символов для генерации
        password = ''.join(random.choice(password_chars) for _ in range(length))
        history.append(password)
        save_history(history)
        update_history_table()
        password_label.config(text=f"Пароль: {password}")
    else:
        password_label.config(text="Выберите хотя бы один тип символов!")


# Обновление таблицы истории
def update_history_table():
    for row in history_table.get_children():
        history_table.delete(row)
    for password in history:
        history_table.insert('', 'end', values=(password,))


# Создание интерфейса
def create_interface():
    global history, password_label, history_table

    history = load_history()

    window = tk.Tk()
    window.title("Random Password Generator")

    # Ползунок длины пароля
    length_label = tk.Label(window, text="Длина пароля:")
    length_label.pack()
    slider = tk.Scale(window, from_=6, to=20, orient=tk.HORIZONTAL)
    slider.pack()

    # Чекбоксы для выбора символов
    options_frame = tk.Frame(window)
    options_frame.pack()
    use_digits = tk.BooleanVar(value=True)
    use_letters = tk.BooleanVar(value=True)
    use_special = tk.BooleanVar(value=True)

    tk.Checkbutton(options_frame, text="Цифры", variable=use_digits).pack(side=tk.LEFT)
    tk.Checkbutton(options_frame, text="Буквы", variable=use_letters).pack(side=tk.LEFT)
    tk.Checkbutton(options_frame, text="Спецсимволы", variable=use_special).pack(side=tk.LEFT)

    # Кнопка генерации
    generate_button = tk.Button(window, text="Сгенерировать пароль",
                                command=lambda: generate_password(slider.get(), use_digits.get(), use_letters.get(),
                                                                  use_special.get()))
    generate_button.pack()

    # Метка для отображения сгенерированного пароля
    password_label = tk.Label(window, text="")
    password_label.pack()

    # Таблица истории
    history_label = tk.Label(window, text="История:")
    history_label.pack()
    history_table = ttk.Treeview(window, columns=("Пароль"), show='headings')
    history_table.heading("Пароль", text="Сгенерированный пароль")
    history_table.pack()

    update_history_table()  # Заполнение таблицы истории

    window.mainloop()


# Запуск интерфейса
create_interface()