#!/usr/bin/env python3
"""
Простая Linux-подобная операционная система с графическим интерфейсом
"""

import tkinter as tk
from tkinter import scrolledtext, Entry, END
import os
import subprocess
import sys
import threading


class LinuxOSSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Linux-подобная ОС (GUI)")
        self.root.geometry("800x600")
        
        # Создаем текстовое поле для вывода
        self.output_text = scrolledtext.ScrolledText(
            root, 
            wrap=tk.WORD, 
            state='disabled',
            bg="black",
            fg="green",
            font=("Courier", 12)
        )
        self.output_text.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Создаем поле ввода команд
        self.input_frame = tk.Frame(root)
        self.input_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        self.prompt_label = tk.Label(self.input_frame, text="user@simulator:~$ ", font=("Courier", 12), fg="green", bg="black")
        self.prompt_label.pack(side='left')
        
        self.command_entry = Entry(
            self.input_frame, 
            width=70,
            bg="black",
            fg="green",
            insertbackground="green",
            font=("Courier", 12),
            highlightthickness=0,
            borderwidth=0
        )
        self.command_entry.pack(side='left', fill='x', expand=True)
        self.command_entry.bind('<Return>', self.execute_command)
        
        # Отображаем приветственное сообщение
        self.print_to_output("Добро пожаловать в Linux-подобную систему!\n")
        self.print_to_output(f"Текущая директория: {os.getcwd()}\n")
        self.print_to_output("Доступные команды: ls, pwd, cd, echo, mkdir, touch, cat, rm, rmdir, ps, df, free, date, help\n")
        
        # Устанавливаем фокус на поле ввода
        self.command_entry.focus()
    
    def print_to_output(self, text):
        """Вывод текста в окно вывода"""
        self.output_text.config(state='normal')
        self.output_text.insert(tk.END, text)
        self.output_text.config(state='disabled')
        self.output_text.yview(tk.END)  # Автоматическая прокрутка вниз
    
    def execute_command(self, event):
        """Выполнение команды из поля ввода"""
        command = self.command_entry.get().strip()
        self.command_entry.delete(0, END)
        
        if command:
            # Добавляем команду в историю
            self.print_to_output(f"user@simulator:~$ {command}\n")
            
            # Разбиваем команду на части
            parts = command.split()
            if not parts:
                return
            
            cmd = parts[0]
            args = parts[1:] if len(parts) > 1 else []
            
            # Обработка команд
            try:
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
                    self.help_command()
                elif cmd == "clear":
                    self.clear_command()
                elif cmd == "exit":
                    self.exit_command()
                else:
                    self.print_to_output(f"Команда не найдена: {cmd}\n")
            except Exception as e:
                self.print_to_output(f"Ошибка выполнения команды: {str(e)}\n")
    
    def ls_command(self, args):
        """Команда ls - список файлов и директорий"""
        try:
            path = args[0] if args else "."
            items = os.listdir(path)
            items.sort()
            for item in items:
                item_path = os.path.join(path, item)
                if os.path.isdir(item_path):
                    self.print_to_output(f"[DIR]  {item}/\n")
                else:
                    self.print_to_output(f"[FILE] {item}\n")
        except FileNotFoundError:
            self.print_to_output("Директория не найдена\n")
        except PermissionError:
            self.print_to_output("Нет доступа к директории\n")
        except Exception as e:
            self.print_to_output(f"Ошибка: {str(e)}\n")
    
    def pwd_command(self):
        """Команда pwd - текущая директория"""
        self.print_to_output(f"{os.getcwd()}\n")
    
    def cd_command(self, args):
        """Команда cd - смена директории"""
        if not args:
            self.print_to_output("Нужно указать путь\n")
            return
        
        try:
            os.chdir(args[0])
            self.print_to_output(f"Текущая директория: {os.getcwd()}\n")
        except FileNotFoundError:
            self.print_to_output("Директория не найдена\n")
        except PermissionError:
            self.print_to_output("Нет доступа к директории\n")
        except Exception as e:
            self.print_to_output(f"Ошибка: {str(e)}\n")
    
    def echo_command(self, args):
        """Команда echo - вывод текста"""
        self.print_to_output(" ".join(args) + "\n")
    
    def mkdir_command(self, args):
        """Команда mkdir - создание директории"""
        if not args:
            self.print_to_output("Нужно указать имя директории\n")
            return
        
        try:
            os.mkdir(args[0])
            self.print_to_output(f"Директория '{args[0]}' создана\n")
        except FileExistsError:
            self.print_to_output(f"Директория '{args[0]}' уже существует\n")
        except Exception as e:
            self.print_to_output(f"Ошибка: {str(e)}\n")
    
    def touch_command(self, args):
        """Команда touch - создание файла"""
        if not args:
            self.print_to_output("Нужно указать имя файла\n")
            return
        
        try:
            with open(args[0], 'a'):
                pass
            self.print_to_output(f"Файл '{args[0]}' создан\n")
        except Exception as e:
            self.print_to_output(f"Ошибка: {str(e)}\n")
    
    def cat_command(self, args):
        """Команда cat - вывод содержимого файла"""
        if not args:
            self.print_to_output("Нужно указать имя файла\n")
            return
        
        try:
            with open(args[0], 'r', encoding='utf-8') as f:
                content = f.read()
                self.print_to_output(content + "\n")
        except FileNotFoundError:
            self.print_to_output("Файл не найден\n")
        except Exception as e:
            self.print_to_output(f"Ошибка: {str(e)}\n")
    
    def rm_command(self, args):
        """Команда rm - удаление файла или директории"""
        if not args:
            self.print_to_output("Нужно указать имя файла/директории\n")
            return
        
        try:
            if os.path.isfile(args[0]):
                os.remove(args[0])
                self.print_to_output(f"Файл '{args[0]}' удален\n")
            elif os.path.isdir(args[0]):
                import shutil
                shutil.rmtree(args[0])
                self.print_to_output(f"Директория '{args[0]}' удалена\n")
            else:
                self.print_to_output(f"'{args[0]}' не существует\n")
        except Exception as e:
            self.print_to_output(f"Ошибка: {str(e)}\n")
    
    def rmdir_command(self, args):
        """Команда rmdir - удаление пустой директории"""
        if not args:
            self.print_to_output("Нужно указать имя директории\n")
            return
        
        try:
            os.rmdir(args[0])
            self.print_to_output(f"Директория '{args[0]}' удалена\n")
        except FileNotFoundError:
            self.print_to_output("Директория не найдена\n")
        except OSError:
            self.print_to_output(f"Директория '{args[0]}' не пуста\n")
        except Exception as e:
            self.print_to_output(f"Ошибка: {str(e)}\n")
    
    def ps_command(self):
        """Команда ps - список процессов (упрощенная)"""
        self.print_to_output("PID    CMD\n")
        self.print_to_output(f"{os.getpid():<6} python3 linux_os_simulator.py\n")
        # В реальной системе здесь был бы список всех запущенных процессов
    
    def df_command(self):
        """Команда df - информация о дисковом пространстве"""
        import shutil
        total, used, free = shutil.disk_usage("/")
        total_gb = total // (1024**3)
        used_gb = used // (1024**3)
        free_gb = free // (1024**3)
        
        self.print_to_output("Файловая система     Размер Использовано  Доступно Использовано% Примонтировано на\n")
        self.print_to_output(f"/dev/sda1             {total_gb}G      {used_gb}G      {free_gb}G        {int(used/total*100)}% /\n")
    
    def free_command(self):
        """Команда free - информация об использовании памяти"""
        import psutil
        memory = psutil.virtual_memory()
        total_mb = memory.total // (1024**2)
        available_mb = memory.available // (1024**2)
        used_mb = memory.used // (1024**2)
        percent_used = memory.percent
        
        self.print_to_output("              Общая     Использованная    Доступная     Доступно%\n")
        self.print_to_output(f"Память:      {total_mb:>6}M      {used_mb:>6}M      {available_mb:>6}M       {percent_used:>4}%\n")
    
    def date_command(self):
        """Команда date - текущая дата и время"""
        from datetime import datetime
        self.print_to_output(f"{datetime.now()}\n")
    
    def help_command(self):
        """Команда help - справка по доступным командам"""
        self.print_to_output("Доступные команды:\n")
        self.print_to_output("  ls [path]     - список файлов и директорий\n")
        self.print_to_output("  pwd           - текущая директория\n")
        self.print_to_output("  cd <path>     - сменить директорию\n")
        self.print_to_output("  echo <text>   - вывести текст\n")
        self.print_to_output("  mkdir <name>  - создать директорию\n")
        self.print_to_output("  touch <file>  - создать файл\n")
        self.print_to_output("  cat <file>    - вывести содержимое файла\n")
        self.print_to_output("  rm <file/dir> - удалить файл или директорию\n")
        self.print_to_output("  rmdir <name>  - удалить пустую директорию\n")
        self.print_to_output("  ps            - список процессов\n")
        self.print_to_output("  df            - информация о дисковом пространстве\n")
        self.print_to_output("  free          - информация об использовании памяти\n")
        self.print_to_output("  date          - текущая дата и время\n")
        self.print_to_output("  help          - эта справка\n")
        self.print_to_output("  clear         - очистить экран\n")
        self.print_to_output("  exit          - выйти из системы\n")
    
    def clear_command(self):
        """Команда clear - очистка экрана"""
        self.output_text.config(state='normal')
        self.output_text.delete(1.0, END)
        self.output_text.config(state='disabled')
    
    def exit_command(self):
        """Команда exit - выход из программы"""
        self.print_to_output("Выход из системы...\n")
        self.root.after(1000, self.root.destroy)  # Закрытие через 1 секунду


def main():
    root = tk.Tk()
    app = LinuxOSSimulator(root)
    root.mainloop()


if __name__ == "__main__":
    main()