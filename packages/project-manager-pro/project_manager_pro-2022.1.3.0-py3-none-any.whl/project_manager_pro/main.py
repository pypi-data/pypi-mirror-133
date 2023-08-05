import os
import json

from project_manager_pro import hash_b
from colorama import Style, Fore, Back


def get_list(path, format_out):
    # список проектов (в виде словарей)
    projects = []

    # обзор каталога path, поиск проектов
    for root, catalogs, elements in os.walk(path):

        # поиск файла с информацией о проекте в каталоге root
        if 'z.json' in (catalogs + elements):
            print('project: ' + Fore.CYAN + root)

            file = open(os.path.join(root, 'z.json'))

            # проверка файла на валидность
            try:
                data = json.load(file)
            except ValueError as e:
                print(Fore.YELLOW + 'Файл '
                      + Fore.CYAN + os.path.join(root, 'z.json')
                      + Fore.YELLOW + ' содержит синтаксическую ошибку(и).')

                print(Fore.RED + 'Проект не будет добавлен!')
                print('')

                continue

            if 'name' not in data \
                    or 'type' not in data \
                    or 'description' not in data \
                    or 'tags' not in data \
                    or 'state' not in data:

                print(Fore.YELLOW + 'Файл '
                      + Fore.CYAN + os.path.join(root, 'z.json')
                      + Fore.YELLOW + ' содержит ошибку(и):')

                if 'name' not in data:
                    print(Fore.RED + 'отсутствует поле \"name\"')

                if 'type' not in data:
                    print(Fore.RED + 'отсутствует поле \"type\"')

                if 'description' not in data:
                    print(Fore.RED + 'отсутствует поле \"description\"')

                if 'tags' not in data:
                    print(Fore.RED + 'отсутствует поле \"tags\"')

                if 'state' not in data:
                    print(Fore.RED + 'отсутствует поле \"state\"')

                print(Fore.RED + 'Проект не будет добавлен!')
                print('')

                continue

            uid = str(hash_b.hash_2(data['name'] + data['type'] + root))
            while len(uid) < 4:
                uid = '0' + uid

            project = {
                'name': data['name'],
                'hash': uid,
                'type': data['type'],
                'state': data['state'],
                'description': data['description'],
                'path': root,
                'tags': data['tags']
            }

            print(Fore.GREEN + 'Проект ' + project['name'] + ' добавлен.')
            print('')

            projects.append(project)

    return projects


def print_list(projects, format_out):
    # вывод списка проектов
    if len(projects) == 0:
        print(Style.BRIGHT + Fore.RED + 'Не найдено ни одного проекта')
    else:

        # ---- формирование массива кортежей для сортировки
        projects_sorted = []

        for project in projects:
            projects_sorted.append((
                project['hash'],
                project['name'],
                project['state'],
                project['type'],
                project['tags'],
                project['path'],
                project['description']
            ))

        projects_sorted.sort(key=lambda i: (i[2], i[3]))

        print(Style.BRIGHT + Fore.GREEN + 'Список проектов:')

        # ---- формат строки для вывода заголовка
        # ширина полей для вывода
        wn = 0  # название проекта
        wt = 0  # тип
        wp = 0  # состояние
        ws = 0  # теги

        for project in projects_sorted:
            temp_ws = 0
            for tag in project[3]:
                temp_ws += 1 + len(tag)

            wn = max(wn, len(project[1]))
            wt = max(wt, len(project[3]))
            wp = max(wp, len(project[2]))
            ws = max(ws, temp_ws)

        format_header = '%-' + str(wn + 12) + 's%-' + str(wp + 15) + 's%-' + str(wt + 14) + 's%-' + str(ws + 10) + 's'

        # ---- вывод списка проектов
        prev = None

        for project in projects_sorted:

            if prev is not None and prev[2] != project[2]:
                print('')

            prev = project

            # подготовка данных для вывода
            uid = Fore.BLUE + str(project[0]) + Style.RESET_ALL + '  '
            name = Style.BRIGHT + Fore.RED + project[1]
            state = Style.BRIGHT + Fore.CYAN + project[2]
            type = Style.RESET_ALL + Style.BRIGHT + Fore.MAGENTA + project[3]

            tags = ' '
            for tag in project[4]:
                tags += ' ' + Style.BRIGHT + Fore.YELLOW + tag

            # вывод
            print('')
            print(uid + Style.RESET_ALL + " ", end='')
            print(format_header % (name, state, type, tags), end='')

            # если формат вывода "подробный"
            if format_out == 'long':
                path = project[5]
                description = project[6]

                print('')
                print(path)
                print(description)
                print('')

    print('')
    print('')
