# vfs_emulator_gui_stage2.py
import tkinter as tk
from tkinter import scrolledtext
import shlex
import argparse

class VFSEmulatorGUIStage2:
    def __init__(self, vfs_path=None, script_path=None):
        # Главное окно
        self.root = tk.Tk()
        self.root.title("VFS Emulator - Stage 2")
        self.root.geometry("800x600")

        # Текстовое поле для вывода
        self.output_area = scrolledtext.ScrolledText(self.root, state='disabled', wrap=tk.WORD)
        self.output_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Поле ввода команд
        self.input_entry = tk.Entry(self.root, font=('Courier New', 12))
        self.input_entry.pack(padx=10, pady=5, fill=tk.X)
        self.input_entry.bind("<Return>", self.process_command)
        self.input_entry.focus()

        # Сохраняем параметры
        self.vfs_path = vfs_path
        self.script_path = script_path

        # Приветствие и debug info
        self.append_output("Welcome to VFS Emulator (Stage 2)")
        self.append_output(f"Debug: VFS Path = {self.vfs_path}")
        self.append_output(f"Debug: Script Path = {self.script_path}")
        self.append_output("Available commands: ls, cd, exit")
        self.append_output("")

        # Выполняем стартовый скрипт
        if self.script_path:
            self.run_script(self.script_path)

        self.append_output("$ ", newline=False)

    # Добавление текста в поле вывода
    def append_output(self, text, newline=True):
        self.output_area.configure(state='normal')
        if newline:
            self.output_area.insert(tk.END, text + "\n")
        else:
            self.output_area.insert(tk.END, text)
        self.output_area.configure(state='disabled')
        self.output_area.see(tk.END)

    # Парсинг команд
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

        # Вывод команды
        self.append_output(f"$ {command_text}")

        # Парсинг и выполнение
        args = self.parse_command(command_text)
        result = self.execute_command(args)
        if result:
            self.append_output(result)

        # Новое приглашение
        self.append_output("$ ", newline=False)

    # Выполнение стартового скрипта
    def run_script(self, path):
        try:
            with open(path, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    self.append_output(f"$ {line}")
                    args = self.parse_command(line)
                    result = self.execute_command(args)
                    if result:
                        self.append_output(result)
        except FileNotFoundError:
            self.append_output(f"Script file not found: {path}")

    # Запуск GUI
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="VFS Emulator GUI Stage 2")
    parser.add_argument("--vfs-path", type=str, help="Path to VFS folder")
    parser.add_argument("--script", type=str, help="Path to startup script")
    args = parser.parse_args()

    emulator = VFSEmulatorGUIStage2(vfs_path=args.vfs_path, script_path=args.script)
    emulator.run()