import json
import sys
import os

from project_manager_pro import main
from colorama import init, Fore, Back, Style

init(autoreset=True)

VERSION = '2022.01.03.0'


# стартовая точка
def run():
    args = sys.argv[1:]

    # вызов команды без параметров
    if len(args) == 0 or args[0] == '-h' or args[0] == '--help':
        cmd_help()
        return

    # проверка версии
    elif args[0] == '-v' or args[0] == '--version':
        cmd_version()
        return

    # вывод списка проектов
    elif args[0] == 'find':

        path = '.'
        format_out = 'none'

        if '-l' in args:
            format_out = 'long'

        if '-s' in args:
            format_out = 'short'

        if '-p' in args:
            path = args[args.index('-p') + 1]

        projects = main.get_list(path=path, format_out=format_out)

        if format_out != 'none':
            main.print_list(projects=projects, format_out=format_out)

        cache_catalog_path = os.path.join(os.path.dirname(__file__), 'cache')
        cache_catalog_file = os.path.join(cache_catalog_path, 'projects.json')

        if os.path.exists(cache_catalog_path) is False:
            os.mkdir(cache_catalog_path)

        with open(cache_catalog_file, 'w', encoding='utf-8') as file:
            file.write(json.dumps(projects, ensure_ascii=False))

    # просмотр закешированных проектов
    elif args[0] == 'list':
        format_out = 'short'

        if '-l' in args:
            format_out = 'long'

        # загрузка файла
        cache_catalog_path = os.path.join(os.path.dirname(__file__), 'cache')
        cache_catalog_file = os.path.join(cache_catalog_path, 'projects.json')

        if os.path.exists(cache_catalog_path) and os.path.exists(cache_catalog_file):
            file = open(os.path.join(cache_catalog_file))
            projects = json.load(file)

            main.print_list(projects=projects, format_out=format_out)
        else:
            print(Style.BRIGHT + Fore.RED + 'Поиск проектов еще не производился')

    # управление командами открытия проектов
    elif args[0] == 'command':

        command_path = os.path.join(os.path.dirname(__file__), 'command')
        command_file = os.path.join(command_path, 'command.json')

        if os.path.exists(command_path) is False:
            os.mkdir(command_path)

            file = open(command_file, 'w')
            file.write('{}')

        if '-a' in args:
            file = open(os.path.join(command_file), 'r', encoding='utf-8')
            commands = json.load(file)

            index = args.index('-a')

            alias = args[index + 1]
            command = args[index + 2]

            commands[alias] = command

            print(Fore.GREEN + 'Добавлена команда ' + alias + ' \"' + commands[alias] + '\"')

            with open(os.path.join(command_file), 'w', encoding='utf-8') as f:
                f.write(json.dumps(commands, ensure_ascii=False))

        elif '-d' in args:
            file = open(os.path.join(command_file), 'r', encoding='utf-8')
            commands = json.load(file)

            index = args.index('-d')

            if len(args) <= index + 1:
                print(Style.BRIGHT + Fore.RED + 'Неверный формат команды, возможно отсутствует псевдоним после -d')
                return

            alias = args[index + 1]

            if args[index+1] in commands:
                print(Fore.GREEN + 'Удалена команда ' + alias + ' \"' + commands[alias] + '\"')
                commands.pop(alias)
            else:
                print(Style.BRIGHT + Fore.RED + 'Команда с псвевдонимом ' + alias + ' не найдена')

            with open(os.path.join(command_file), 'w', encoding='utf-8') as f:
                f.write(json.dumps(commands, ensure_ascii=False))

        elif '-l' in args:
            file = open(os.path.join(command_file), 'r', encoding='utf-8')
            commands = json.load(file)

            if len(commands) == 0:
                print(Style.BRIGHT + Fore.RED + 'Не найдено ни одной команды')
            else:
                print(Style.BRIGHT + Fore.GREEN + 'Список команд:')

                for command in commands:

                    alias = Style.BRIGHT + Fore.RED + command
                    text = Style.RESET_ALL + Fore.CYAN + commands[command].replace('$', Style.BRIGHT + Fore.MAGENTA + '$')

                    print('%-20s%-100s' % (alias, text))

                print('')

        else:

            print(Style.BRIGHT + Fore.RED + 'Неверный формат команды')
            print(Fore.YELLOW + 'Ожидался один из параметров: -a, -d, -l')

    # открытие проекта
    else:

        if len(args) < 2:
            print(Style.BRIGHT + Fore.RED + 'Неверный формат команды')
            print(Fore.YELLOW + 'Ожидалась команда pmp [alias] [project]')
            return

        alias = args[0]
        name = args[1]

        # загрузка команд
        command_path = os.path.join(os.path.dirname(__file__), 'command')
        command_file = os.path.join(command_path, 'command.json')

        file = open(os.path.join(command_file), 'r', encoding='utf-8')
        commands = json.load(file)

        command = ''

        if alias in commands:
            command = commands[alias]
        else:
            print(Style.BRIGHT + Fore.RED + 'Команда с псевдонимом ' + alias + ' не найдена')
            return

        # загрузка файла
        cache_catalog_path = os.path.join(os.path.dirname(__file__), 'cache')
        cache_catalog_file = os.path.join(cache_catalog_path, 'projects.json')

        if os.path.exists(cache_catalog_path) and os.path.exists(cache_catalog_file):
            file = open(os.path.join(cache_catalog_file))
            projects = json.load(file)

            for project in projects:
                if project['name'] == name or str(project['hash']) == name:

                    command = command.replace('$', project['path'])

                    print(Fore.GREEN + 'run ' + Fore.CYAN + command)
                    os.system(command)
                    return

            print(Style.BRIGHT + Fore.RED + 'Проект с именем (хешем) ' + name + ' не найден')

        else:
            print(Style.BRIGHT + Fore.RED + 'Поиск проектов еще не производился')


# ---- здесь можно реализовывать функции поведения для соответствующих команд
def cmd_help():
    print('----------------------------------------------------------------------')
    print(Style.BRIGHT + Fore.RED + 'Project Manager Pro ' + VERSION)
    print('')

    print(Fore.YELLOW + 'ddd.dungeon@gmail.com')
    print(Fore.YELLOW + 'https://github.com/FullDungeon/python_pip')
    print('')

    print('Данный пакет предназначен для открытия проектов в любой IDE прямо из ')
    print('терминала, и отображения списка проектов в удобном виде с указанием')
    print('полезной информации о них.')
    print('')

    print('Настроить и подготовить к работе менеджер можно всего за три шага:')
    print('1. Создать в своих проектах файл z.json:')
    print(Fore.CYAN + '{')
    print(Fore.CYAN + '    \"name\": \"Project name\",')
    print(Fore.CYAN + '    \"type\": \"Application\",')
    print(Fore.CYAN + '    \"state\": \"active\",')
    print(Fore.CYAN + '    \"description\": \"Long full description\",')
    print(Fore.CYAN + '    \"tags\": [')
    print(Fore.CYAN + '        \"Python\", \"Pip\"')
    print(Fore.CYAN + '    ]')
    print(Fore.CYAN + '}')
    print('')
    print('2. Произвести поиск проектов на диске с сохранением информации о них:')
    print(Fore.CYAN + 'pmp find -p ./projects/')
    print('')
    print('3. Добавить в конфигурацию пакета способы запуска проектов:')
    print(Fore.CYAN + 'pmp command -a code \"code $\"')
    print('')

    print('Теперь все проекты, которые были найдены, можно запускать с помощью')
    print('команды ' + Fore.CYAN + 'pmp [alias] [project]' + Style.RESET_ALL + '. Подробнее об этом написано ниже.')
    print('')

    print('----------------------------------------------------------------------')
    print(Style.BRIGHT + Fore.RED + 'Список команд:', end='\n\n')

    print(Style.BRIGHT + Fore.MAGENTA + '-h  --help              ', end='')
    print('как этим пользоваться (открывает этот список)', end='\n\n')

    print(Style.BRIGHT + Fore.MAGENTA + '-v  --version           ', end='')
    print('текущая версия', end='\n\n')

    # find
    print(Style.BRIGHT + Fore.MAGENTA + 'find -l (-s) -p [path]  ', end='')
    print('поиск проектов в каталоге и его подкаталогах и')
    print('                        сохранение информации.')
    print('')

    print(Fore.CYAN + '                        -l, -s')
    print(Fore.YELLOW + '                        подробный или краткий вывод списка проектов')
    print(Fore.YELLOW + '                        (по умолчанию ничего не выводится).')
    print('')

    print(Fore.CYAN + '                        -p [path]')
    print(Fore.YELLOW + '                        указание каталога для поиска, по умолчанию')
    print(Fore.YELLOW + '                        используется текущий каталог.')
    print('')

    # list
    print(Style.BRIGHT + Fore.MAGENTA + 'list -l                 ', end='')
    print('вывод списка проектов, сохраненных в кэш, в')
    print('                        краткой форме.')
    print('')

    print(Fore.CYAN + '                        -l')
    print(Fore.YELLOW + '                        подробный вывод списка проектов (по умолчанию')
    print(Fore.YELLOW + '                        краткий)')
    print('')

    # command
    print(Style.BRIGHT + Fore.MAGENTA + 'command                 ', end='')
    print('управление командами запуска проектов')
    print('')

    print(Fore.CYAN + '                        -a [alias] [command]')
    print(Fore.YELLOW + '                        добавление команды command с псевдонимом alias')
    print(Fore.YELLOW + '                        для открытия проекта в конфигурацию пакета.')
    print(Fore.YELLOW + '                        Команда должна содержать символ $, который будет')
    print(Fore.YELLOW + '                        заменяться путем к проекту')
    print('')

    print(Fore.CYAN + '                        -d [alias]')
    print(Fore.YELLOW + '                        удаление команды с псевдонимом alias')
    print('')

    print(Fore.CYAN + '                        -l')
    print(Fore.YELLOW + '                        список команд')
    print('')

    # open
    print(Style.BRIGHT + Fore.MAGENTA + '[alias] [project]       ', end='')
    print('открытие проекта с именем project командой с псведонимом alias')
    print('')

    print(Fore.CYAN + '                        [alias]')
    print(Fore.YELLOW + '                        любой ранее добавленный псевдоним в конфигурацию')
    print('')

    print(Fore.CYAN + '                        [project]')
    print(Fore.YELLOW + '                        имя или хэш любого существующего проекта')
    print('')


def cmd_version():
    print(VERSION)

