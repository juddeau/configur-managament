# python3 vfs_emulator.py
import tkinter as tk
from tkinter import scrolledtext
import shlex
import sys

class VFSEmulatorGUI:
    def __init__(self):
        # Создаем главное окно
        self.root = tk.Tk()
        self.root.title("VFS Emulator - Stage 1")
        self.root.geometry("800x600")

        # Текстовое поле для вывода
        self.output_area = scrolledtext.ScrolledText(self.root, state='disabled', wrap=tk.WORD)
        self.output_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Поле для ввода команд
        self.input_entry = tk.Entry(self.root, font=('Courier New', 12))
        self.input_entry.pack(padx=10, pady=5, fill=tk.X)
        self.input_entry.bind("<Return>", self.process_command)
        self.input_entry.focus()

        # Приветственное сообщение
        self.append_output("Welcome to VFS Emulator (REPL prototype)")
        self.append_output("Available commands: ls, cd, exit")
        self.append_output("")
        self.append_output("$ ", newline=False)

    # Функция добавления текста в окно
    def append_output(self, text, newline=True):
        self.output_area.configure(state='normal')
        if newline:
            self.output_area.insert(tk.END, text + "\n")
        else:
            self.output_area.insert(tk.END, text)
        self.output_area.configure(state='disabled')
        self.output_area.see(tk.END)

    # Парсинг команд с shlex
    def parse_command(self, command_line):
        try:
            return shlex.split(command_line)
        except ValueError as e:
            return ["error", str(e)]

    # Выполнение команды
    def execute_command(self, args):
        if not args:
            return ""
        cmd = args[0]
        if cmd == "ls" or cmd == "cd":
            return f"Command: {cmd}, Args: {args[1:]}"
        elif cmd == "exit":
            self.append_output("Exiting...")
            self.root.after(500, self.root.destroy)
            return ""
        else:
            return f"Unknown command: {cmd}"

    # Обработка ввода пользователя
    def process_command(self, event):
        command_text = self.input_entry.get()
        self.input_entry.delete(0, tk.END)

        # Вывод команды в текстовое поле
        self.append_output(f"$ {command_text}")

        # Парсинг и выполнение
        args = self.parse_command(command_text)
        result = self.execute_command(args)
        if result:
            self.append_output(result)

        # Новое приглашение
        self.append_output("$ ", newline=False)

    # Запуск GUI
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    emulator = VFSEmulatorGUI()
    emulator.run()
