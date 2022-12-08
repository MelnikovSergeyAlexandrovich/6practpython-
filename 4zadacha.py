"""
Результаты чемпионата штангистов представлены следующими данными: фамилия,
команда, собственный вес, результат в каждой из трех попыток. Найти чемпиона в каждой
весовой категории, выделяемой с шагом 5 кг. Выполнить сортировку списка.
"""
import csv
from tabulate import tabulate
import os


def input_str(prompt, error_message):
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


def input_weight(prompt, error_message):
    """
    Функция, которая выводит сообщение о ошибке, если неправильно введен вес (Если он меньше  или больше ). В другом случае возвращает введенный вес
    :param prompt:
    :param error_message:
    :return:
    """
    while True:
        try:
            w = float(input(prompt))
            if w >= 75 and w <=90:
                return w
            print(error_message)
        except:
            print(error_message)


def input_result(prompt, error_message):
    """
    Функция, которая выводит сообщение о ошибке, если неправильно введен результат (число, с плавающей запятой). В другом случае возвращает результат
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
    Функция, с помощью которой вводятся все параметры в csv файл, также присутствует цикл для присваивания диапазонов веса.
    Также происходит реализация создания переменной, которая отвечает за максимальный результат.
    В результате в csv файле пишется все введенные параметры + rangeofweight - диапазон, зависящей от веса
    :param file_name:
    :return:
    """
    global rangeofweight
    global maxresult
    surname = input_str("Введите фамилию штангиста: ",
                        "Фамилия штангиста должна состоять из данных в формате string")
    team = input_str("Введите команду штангиста: ",
                 "Команда штангиста должна состоять из данных в формате string")
    weight = input_weight("Введите вес штангиста: ",
                          "Штангист с данным весом не может быть допущен к соревнованиям")
    result1 = input_result("Введите 1 результат данного штангиста: ",
                           "Вы ввели не число")
    result2 = input_result("Введите 2 результат данного штангиста: ",
                           "Вы ввели не число")
    result3 = input_result("Введите 3 результат данного штангиста: ",
                           "Вы ввели не число")
    if result1 > result2 and result1 > result3:
        maxresult = result1
    elif result2 > result1 and result2 > result3:
        maxresult = result2
    elif result3 > result2 and result1 < result3:
        maxresult = result3

    if weight < 76 and weight > 69:
        rangeofweight = "low"
    elif weight < 81 and weight > 75:
        rangeofweight = "middle"
    elif weight < 86 and weight > 80:
        rangeofweight = "big"
    elif weight < 91 and weight > 85:
        rangeofweight = "gigantic"


    with open(file_name, 'a') as f:
        f.write(f"\n{surname},{team},{weight},{rangeofweight},{result1},{result2},{result3},{maxresult}")


def writeresults() -> None:
    """
    Функция, которая создает листы для всех диапазонов веса, далее открывает csv файл, в котором считывает всю информацию.
    Далее она перебирает данные в нашем файле, создаёт словарь для всех значений (в ключах содержится вся введенная из консоли информация).
    Далее создает цикл, который в созданные листы добавляет значения в зависимости от переменной (цикл, связанный с weight, addreadinfo был создан как раз для этого)
    если такого диапазона не существует, то он выведет ошибку. В конце реализуется функция sort , как раз-таки для сортировки листов.
    :return:
    """
    low = []
    middle = []
    big = []
    gigantic = []
    path = 'weightlifters.csv'
    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader)  # Для пропуска шапки
        for row in csv_reader:  # Перебор данных в csv файле
            surname,team,weight,rangeofweight,result1,result2,result3,maxresult  = row
            weightlifter = {"surname": surname, "team": team, "range_of_weight": str(rangeofweight), "result_1": float(result1),
                       "result_2": float(result2), "result_3": float(result3), "maximal_result": float(maxresult)}
            if rangeofweight == "low":
                low.append(weightlifter)
            elif rangeofweight == "middle":
                middle.append(weightlifter)
            elif rangeofweight == "big":
                big.append(weightlifter)
            elif rangeofweight == "gigantic":
                gigantic.append(weightlifter)
            else:
                raise ValueError("unexpected weight range: " + rangeofweight)

    sort(low, "low")  # func
    sort(middle, "middle")  # func
    sort(big, " big")  # func
    sort(gigantic, "gigantic")  # func


def get_sort_key(x) -> int:
    """
    Возвращает ключ -  максимальный результат  , которое дает найти победителя в каждой категории
    :param x:
    :return:
    """
    return x["maximal_result"]


def sort(athletes, header) -> None:
    '''
    Сортировка списка штангистов и вывод полученных значений с шапкой
    '''
    print(header)
    # Cортировка по ключу
    sorted_tuple = sorted(athletes, key=get_sort_key, reverse=True)
    sorted_tuple = [(i, x["surname"], x["maximal_result"]) for i, x in enumerate(sorted_tuple)]
    headers = ["No", "Фамилия", "weight"]  # Создание шапки для таблицы
    print(tabulate(sorted_tuple, headers, tablefmt='grid'))


def main() -> None:
    """
    Функция main, в которой при не существующем файле csv (weightlifters.csv) будет записывать фамилию, диапазон возраста и тд. - создавать новый файл
    Также она является основной функцией - т.к. в с помощью неё реалиуется работа всех функций через консоль
    :return:
    """
    file_name = 'weightlifters.csv'
    if not os.path.exists(file_name):
        with open(file_name, 'w') as f:
            f.write("surname,team,weight,rangeofweight,result1,result2,result3,maxresult")

    while True:

        print("=================================================================")
        op = int(input("1. Ввод фамилии штангиста,команды,1-ой попытки,2-ой попытки,3-ой попытки,\n"
                       "2. Просмотр результатов\n"
                       "3. Выход\n"))
        if op == 1:
            addreadinfo(file_name)
        elif op == 2:
            writeresults()
        elif op == 3:
            return


if __name__ == "__main__":  # Реализуем работу функции main
    main()
