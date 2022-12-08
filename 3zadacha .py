"""
Известны данные о результатах лыжного забега: фамилии участников, возраст, время
старта и время финиша. По возрасту выделены 3 возрастные категории, заданные
диапазонами. Найти чемпиона по каждой возрастной категории. Выполнить сортировку
списка.
Всего будет 6 спортсменов
"""
import csv
from tabulate import tabulate
import os


def input_str(prompt, error_message) -> str:
    """
    Функция, которая выводит сообщение о ошибке, если неправильно введенна строка. В другом случае возвращает введенную строку
    :param prompt:
    :param error_message:
    :return:
    """
    while True:
        _str = input(prompt)
        if str.isalpha(_str):
            return _str
        print(error_message)


def input_age(prompt, error_message):
    """
    Функция, которая выводит сообщение о ошибке, если неправильно введен возраст (Если он меньше 9 или больше 18). В другом случае возвращает введенный возраст
    :param prompt:
    :param error_message:
    :return:
    """
    while True:
        try:
            n = float(input(prompt))
            if n >= 9 and n <= 18:
                return n
            print(error_message)
        except:
            print(error_message)


def input_float(prompt, error_message):
    """
    Функция, которая выводит сообщение о ошибке, если неправильно введенно время (число, с плавающей запятой). В другом случае возвращает введенное время
    :param prompt:
    :param error_message:
    :return:
    """
    while True:
        try:
            return float(input(prompt))
        except:
            print(error_message)


def addreadinfo(file_name) -> None:
    """
    Функция, с помощью которой вводятся все параметры в csv файл, также присутствует цикл для присваивания диапазонов возрастов.
    В результате в csv файле пишется все введенные параметры + rangeofage - диапазон, зависящей от возраста
    :param file_name:
    :return:
    """
    global rangeofage
    surname = input_str("Введите фамилию лыжника: ",
                        "Фамилия спортсмена должна состоять из данных в формате string")
    age = input_age("Введите возраст спортсмена: ",
                    "Возраст должен быть числом в диапазоне от 9 до 18")
    startinfo = input_float("Введите время старта: ",
                            "Время старта должно быть в формате float")
    finishinfo = input_float("Введите время финиша : ",
                             "Время  должно быть в формате float")

    if age < 12 and age > 9:
        rangeofage = "children"
    elif age < 15 and age > 11:
        rangeofage = "juniors"
    if age < 18 and age > 14:
        rangeofage = "seniors"

    with open(file_name, 'a') as f:
        f.write(f"\n{surname},{rangeofage},{age},{startinfo},{finishinfo},{finishinfo - startinfo}")


def writeresults() -> None:
    """
    Функция, которая создает листы для всех диапазонов возрастов, далее открывает csv файл, в котором считывает всю информацию.
    Далее она перебирает данные в нашем файле, создаёт словарь для всех значений (в ключах содержится вся введенная из консоли информация).
    Далее создает цикл, который в созданные листы добавляет значения в зависимости от переменной (цикл, связанный с age, addreadinfo был создан как раз для этого)
    если такого диапазона не существует, то он выведет ошибку. В конце реализуется функция sort , как раз-таки для сортировки листов.
    :return:
    """
    children = []
    juniors = []
    seniors = []
    path = 'competitors.csv'
    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader) # Для пропуска
        for row in csv_reader:  # Перебор данных в csv файле
            surname,rangeofage,age,start,finish,time = row
            athlete = {"surname" : surname,"rangeofage" : rangeofage,"age" : float(age),"startinfo" :float(start) ,"finish" : float(finish), "time" : (float(time))}
            if rangeofage == "children":
                children.append(athlete)
            elif rangeofage == "juniors":
                juniors.append(athlete)
            elif rangeofage == "seniors":
                seniors.append(athlete)
            else:
                raise ValueError("unexpected age range: " + rangeofage)
             
    sort(children, "children")  # func
    sort(juniors, "juniors")  # func
    sort(seniors, "seniors")  # func


def get_sort_key(x) -> int:
    """
    Возвращает ключ - время, которое дает найти победителя в каждой категории
    :param x:
    :return:
    """
    return x["time"]

def sort(athletes, header) -> None:
    '''
    Сортировка списка спортсменов и вывод полученных значений с шапкой
    '''
    print(header)
    # Cортировка по ключу
    sorted_tuple = sorted(athletes, key=get_sort_key)
    sorted_tuple = [(i, x["surname"], x["time"]) for i, x in enumerate(sorted_tuple)]
    headers = ["No", "Фамилия", "time"]  # Создание шапки для таблицы
    print(tabulate(sorted_tuple, headers, tablefmt='grid'))


def main() -> None:
    """
    Функция main, в которой при не существующем файле csv (competitors.csv) будет записывать фамилию, диапазон возраста и тд.
    Также она является основной функцией - т.к. в с помощью неё реалиуется работа всех функций через консоль
    :return:
    """
    file_name = 'competitors.csv'
    if not os.path.exists(file_name):
        with open(file_name, 'w') as f:
            f.write("surname,rangeofage,age,start,finish,time")

    while True:

        print("=================================================================")
        op = int(input("1. Ввод фамилии участника,возраст, время старта и время финиша\n"
                       "2. Просмотр результатов\n"
                       "3. Выход\n"))
        if op == 1:
            addreadinfo(file_name)
        elif op == 2:
            writeresults()
        elif op == 3:
            return


if __name__ == "__main__": #Реализуем работу функции main
    main()
