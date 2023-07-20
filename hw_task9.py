# Напишите следующие функции:
# Нахождение корней квадратного уравнения
# Генерация csv файла с тремя случайными числами в каждой строке. 100-1000 строк.
# Декоратор, запускающий функцию нахождения корней квадратного уравнения с каждой тройкой чисел из csv файла.
# Декоратор, сохраняющий переданные параметры и результаты работы функции в json файл.

import csv
import json
import math
import random

def generate_csv(filename, rows):
    """Генерирует csv файл с тремя случайными числами в каждой строке для заданного количества строк."""
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Number 1', 'Number 2', 'Number 3'])  # Записываем заголовок

        for _ in range(rows):
            row = [random.randint(1, 100) for _ in range(3)]
            writer.writerow(row)


def roots_from_csv_decorator(func):
    """Декоратор, запускающий функцию нахождения корней квадратного уравнения с каждой тройкой чисел из csv файла."""

    def wrapper(filename):
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Пропускаем заголовок

            for row in reader:
                a, b, c = map(int, row)
                roots = func(a, b, c)
                print(f"Roots for {a}, {b}, {c}: {roots}")

    return wrapper


def save_to_json_decorator(func):
    """Декоратор, сохраняющий параметры и результаты работы функции в JSON-файл для каждой тройки чисел из numbers.csv."""

    def wrapper(filename):
        results = []
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Пропускаем заголовок

            for row in reader:
                a, b, c = map(int, row)
                result = func(a, b, c)
                data = {
                    'parameters': {
                        'a': a,
                        'b': b,
                        'c': c
                    },
                    'result': result
                }
                results.append(data)

        with open('results.json', 'w') as jsonfile:
            json.dump(results, jsonfile, indent=4)

    return wrapper


@save_to_json_decorator
def find_roots(a, b, c):
    """Функция для нахождения корней квадратного уравнения с заданными параметрами."""
    D = b**2 - 4*a*c

    if D > 0:
        x1 = (-b + math.sqrt(D)) / (2*a)
        x2 = (-b - math.sqrt(D)) / (2*a)
        return x1, x2
    elif D == 0:
        x = -b / (2*a)
        return x
    else:
        return None


# Генерация csv файла
generate_csv('numbers.csv', 100)

# Запуск функции нахождения корней квадратного уравнения с заданными параметрами и сохранение результатов в json файл
find_roots('numbers.csv')