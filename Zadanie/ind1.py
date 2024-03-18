#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import json
import datetime
import jsonschema


def select(line, humans):
    # Функция выбора человека по дате рождения
    nom = input('Введите дату рождения: ')
    count = 0
    print(line)
    print(
        f'| {"№":^4} | {"Ф.И.О.":^20} | {"знак зодиака":^15} | {"Дата рождения":^16} |')
    print(line)

    for i, num in enumerate(humans, 1):
        if nom == num.get('daytime', ''):
            count += 1
            print(
                '| {:<4} | {:<20} | {:<15} | {:<16} |'.format(
                    count,
                    num.get('name', ''),
                    num.get('zodiac', ''),
                    num.get('daytime', 0)))
    print(line)

    if count == 0:
        print('Таких людей нет')


def table(line, humans):
    # Функция вывода списка людей
    print(line)
    print(
        '| {:^4} | {:^20} | {:^15} | {:^16} |'.format(
            "№",
            "Ф.И.О.",
            "Знак зодиака",
            "Дата рождения"))
    print(line)
    for i, num in enumerate(humans, 1):
        print(
            '| {:<4} | {:<20} | {:<15} | {:<16} |'.format(
                i,
                num.get('name', ''),
                num.get('zodiac', ''),
                num.get('daytime', 0)
            )
        )
    print(line)


def add(humans):
    # Функция добавления новых людей
    daytime = input('Введите дату рождения: ')
    zodiac = input('Введите знак зодиака: ')
    name = input('Введите Ф.И.О.: ')
    date = datetime.datetime.strptime(daytime, '%d/%m/%Y').date()
    air = {
        'zodiac': zodiac,
        'name': name,
        'daytime': daytime
    }

    humans.append(air)
    if len(humans) > 1:
        humans.sort(key=lambda x: x.get('daytime', ''))


def save_to_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file)


def load_from_json(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            validate_data(data)  # Вызываем функцию валидации
            return data
    except FileNotFoundError:
        return []


def validate_data(data):
    schema = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "zodiac": {"type": "string"},
                "daytime": {"type": "string", "format": "date"}
            },
            "required": ["name", "zodiac", "daytime"]
        }
    }

    jsonschema.validate(data, schema)


def main():
    # Основная функция программы
    humans = load_from_json('humans.json')
    print('Список комманд: \n exit - Завершить работу'
          ' \n add - Добавить человека \n'
          ' list - Показать список людей'
          ' \n select - Выбрать знак зодиака по дате рождения')
    line = '+-{}-+-{}-+-{}-+-{}-+'.format(
        '-' * 4,
        '-' * 20,
        '-' * 15,
        '-' * 16
    )
    while True:
        com = input('Введите команду: ').lower()
        if com == 'exit':
            save_to_json('humans.json', humans)  # Сохраняем данные перед завершением
            break
        elif com == "add":
            add(humans)
        elif com == 'list':
            table(line, humans)
        elif com == 'select':
            select(line, humans)
        else:
            print(f"Неизвестная команда {com}", file=sys.stderr)


if __name__ == '__main__':
    main()
