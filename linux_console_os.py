#!/usr/bin/env python3
"""
Консольная Linux-подобная операционная система
"""

import os
import subprocess
import sys
import shlex
from datetime import datetime


class LinuxConsoleOS:
    def __init__(self):
        self.running = True
        self.current_dir = os.getcwd()
        self.prompt = f"user@console-os:~$ "
        
        print("Добро пожаловать в консольную Linux-подобную систему!")
        print(f"Текущая директория: {self.current_dir}")
        print("Доступные команды: ls, pwd, cd, echo, mkdir, touch, cat, rm, rmdir, ps, df, free, date, help, clear, exit")
        print("Для получения справки по команде введите 'help <команда>'")
    
    def run(self):
        while self.running:
            try:
                command = input(self.prompt).strip()
                if command:
                    self.execute_command(command)
            except KeyboardInterrupt:
                print("\nВыход из системы...")
                break
            except EOFError:
                print("\nВыход из системы...")
                break
    
    def execute_command(self, command):
        """Выполнение команды"""
        parts = shlex.split(command)
        if not parts:
            return
        
        cmd = parts[0]
        args = parts[1:] if len(parts) > 1 else []
        
        # Обработка команд
        if cmd == "ls":
            self.ls_command(args)
        elif cmd == "pwd":
            self.pwd_command()
        elif cmd == "cd":
            self.cd_command(args)
        elif cmd == "echo":
            self.echo_command(args)
        elif cmd == "mkdir":
            self.mkdir_command(args)
        elif cmd == "touch":
            self.touch_command(args)
        elif cmd == "cat":
            self.cat_command(args)
        elif cmd == "rm":
            self.rm_command(args)
        elif cmd == "rmdir":
            self.rmdir_command(args)
        elif cmd == "ps":
            self.ps_command()
        elif cmd == "df":
            self.df_command()
        elif cmd == "free":
            self.free_command()
        elif cmd == "date":
            self.date_command()
        elif cmd == "help":
            self.help_command(args)
        elif cmd == "clear":
            self.clear_command()
        elif cmd == "exit":
            self.exit_command()
        else:
            print(f"Команда не найдена: {cmd}")
    
    def ls_command(self, args):
        """Команда ls - список файлов и директорий"""
        try:
            path = args[0] if args else "."
            items = os.listdir(path)
            items.sort()
            for item in items:
                item_path = os.path.join(path, item)
                if os.path.isdir(item_path):
                    print(f"[DIR]  {item}/")
                else:
                    print(f"[FILE] {item}")
        except FileNotFoundError:
            print("Директория не найдена")
        except PermissionError:
            print("Нет доступа к директории")
        except Exception as e:
            print(f"Ошибка: {str(e)}")
    
    def pwd_command(self):
        """Команда pwd - текущая директория"""
        print(os.getcwd())
    
    def cd_command(self, args):
        """Команда cd - смена директории"""
        if not args:
            print("Нужно указать путь")
            return
        
        try:
            os.chdir(args[0])
            self.current_dir = os.getcwd()
            self.prompt = f"user@console-os:{os.path.basename(self.current_dir)}$ "
        except FileNotFoundError:
            print("Директория не найдена")
        except PermissionError:
            print("Нет доступа к директории")
        except Exception as e:
            print(f"Ошибка: {str(e)}")
    
    def echo_command(self, args):
        """Команда echo - вывод текста"""
        print(" ".join(args))
    
    def mkdir_command(self, args):
        """Команда mkdir - создание директории"""
        if not args:
            print("Нужно указать имя директории")
            return
        
        try:
            os.mkdir(args[0])
            print(f"Директория '{args[0]}' создана")
        except FileExistsError:
            print(f"Директория '{args[0]}' уже существует")
        except Exception as e:
            print(f"Ошибка: {str(e)}")
    
    def touch_command(self, args):
        """Команда touch - создание файла"""
        if not args:
            print("Нужно указать имя файла")
            return
        
        try:
            with open(args[0], 'a'):
                pass
            print(f"Файл '{args[0]}' создан")
        except Exception as e:
            print(f"Ошибка: {str(e)}")
    
    def cat_command(self, args):
        """Команда cat - вывод содержимого файла"""
        if not args:
            print("Нужно указать имя файла")
            return
        
        try:
            with open(args[0], 'r', encoding='utf-8') as f:
                content = f.read()
                print(content)
        except FileNotFoundError:
            print("Файл не найден")
        except Exception as e:
            print(f"Ошибка: {str(e)}")
    
    def rm_command(self, args):
        """Команда rm - удаление файла или директории"""
        if not args:
            print("Нужно указать имя файла/директории")
            return
        
        try:
            if os.path.isfile(args[0]):
                os.remove(args[0])
                print(f"Файл '{args[0]}' удален")
            elif os.path.isdir(args[0]):
                import shutil
                shutil.rmtree(args[0])
                print(f"Директория '{args[0]}' удалена")
            else:
                print(f"'{args[0]}' не существует")
        except Exception as e:
            print(f"Ошибка: {str(e)}")
    
    def rmdir_command(self, args):
        """Команда rmdir - удаление пустой директории"""
        if not args:
            print("Нужно указать имя директории")
            return
        
        try:
            os.rmdir(args[0])
            print(f"Директория '{args[0]}' удалена")
        except FileNotFoundError:
            print("Директория не найдена")
        except OSError:
            print(f"Директория '{args[0]}' не пуста")
        except Exception as e:
            print(f"Ошибка: {str(e)}")
    
    def ps_command(self):
        """Команда ps - список процессов (упрощенная)"""
        print("PID    CMD")
        print(f"{os.getpid():<6} python3 linux_console_os.py")
        # В реальной системе здесь был бы список всех запущенных процессов
    
    def df_command(self):
        """Команда df - информация о дисковом пространстве"""
        import shutil
        total, used, free = shutil.disk_usage("/")
        total_gb = total // (1024**3)
        used_gb = used // (1024**3)
        free_gb = free // (1024**3)
        
        print("Файловая система     Размер Использовано  Доступно Использовано% Примонтировано на")
        print(f"/dev/sda1             {total_gb}G      {used_gb}G      {free_gb}G        {int(used/total*100)}% /")
    
    def free_command(self):
        """Команда free - информация об использовании памяти"""
        import psutil
        memory = psutil.virtual_memory()
        total_mb = memory.total // (1024**2)
        available_mb = memory.available // (1024**2)
        used_mb = memory.used // (1024**2)
        percent_used = memory.percent
        
        print("              Общая     Использованная    Доступная     Доступно%")
        print(f"Память:      {total_mb:>6}M      {used_mb:>6}M      {available_mb:>6}M       {percent_used:>4}%")
    
    def date_command(self):
        """Команда date - текущая дата и время"""
        print(f"{datetime.now()}")
    
    def help_command(self, args):
        """Команда help - справка по доступным командам"""
        if not args:
            print("Доступные команды:")
            print("  ls [path]     - список файлов и директорий")
            print("  pwd           - текущая директория")
            print("  cd <path>     - сменить директорию")
            print("  echo <text>   - вывести текст")
            print("  mkdir <name>  - создать директорию")
            print("  touch <file>  - создать файл")
            print("  cat <file>    - вывести содержимое файла")
            print("  rm <file/dir> - удалить файл или директорию")
            print("  rmdir <name>  - удалить пустую директорию")
            print("  ps            - список процессов")
            print("  df            - информация о дисковом пространстве")
            print("  free          - информация об использовании памяти")
            print("  date          - текущая дата и время")
            print("  help          - эта справка")
            print("  help <cmd>    - справка по конкретной команде")
            print("  clear         - очистить экран")
            print("  exit          - выйти из системы")
        else:
            cmd = args[0]
            if cmd == "ls":
                print("ls [path] - показывает список файлов и директорий в указанной директории (по умолчанию текущая)")
            elif cmd == "pwd":
                print("pwd - показывает текущую директорию")
            elif cmd == "cd":
                print("cd <path> - изменяет текущую директорию на указанную")
            elif cmd == "echo":
                print("echo <text> - выводит указанный текст")
            elif cmd == "mkdir":
                print("mkdir <name> - создает новую директорию с указанным именем")
            elif cmd == "touch":
                print("touch <file> - создает новый пустой файл с указанным именем")
            elif cmd == "cat":
                print("cat <file> - выводит содержимое файла")
            elif cmd == "rm":
                print("rm <file/dir> - удаляет файл или директорию")
            elif cmd == "rmdir":
                print("rmdir <name> - удаляет пустую директорию")
            elif cmd == "ps":
                print("ps - показывает список запущенных процессов")
            elif cmd == "df":
                print("df - показывает информацию о дисковом пространстве")
            elif cmd == "free":
                print("free - показывает информацию об использовании памяти")
            elif cmd == "date":
                print("date - показывает текущую дату и время")
            elif cmd == "help":
                print("help - показывает список доступных команд")
            elif cmd == "clear":
                print("clear - очищает экран")
            elif cmd == "exit":
                print("exit - завершает работу системы")
            else:
                print(f"Команда не найдена: {cmd}")
    
    def clear_command(self):
        """Команда clear - очистка экрана"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def exit_command(self):
        """Команда exit - выход из программы"""
        print("Выход из системы...")
        self.running = False


def main():
    os_simulator = LinuxConsoleOS()
    os_simulator.run()


if __name__ == "__main__":
    main()