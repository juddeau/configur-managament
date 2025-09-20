# vfs_emulator_gui_stage5.py
import tkinter as tk
from tkinter import scrolledtext
import shlex
import argparse
import csv
import base64
import datetime

# --- VFS ---
vfs = {
    "root": {
        "type": "folder",
        "permissions": "rwxr-xr-x",
        "children": {
            "folder1": {
                "type": "folder",
                "permissions": "rwxr-xr-x",
                "children": {
                    "file2.txt": {"type": "file", "content": "Hello from file2", "permissions": "rw-r--r--"}
                }
            },
            "file1.txt": {"type": "file", "content": "Hello from file1", "permissions": "rw-r--r--"}
        }
    }
}
current_path = ["root"]

def get_current_folder():
    folder = vfs
    for p in current_path:
        folder = folder[p]["children"]
    return folder

# --- GUI ---
class VFSEmulatorGUIStage5:
    def __init__(self, vfs_path=None, script_path=None):
        self.vfs_path = vfs_path
        self.script_path = script_path

        # Главное окно
        self.root = tk.Tk()
        self.root.title("VFS Emulator - Stage 5")
        self.root.geometry("800x600")

        # Текстовое поле для вывода
        self.output_area = scrolledtext.ScrolledText(self.root, state='disabled', wrap=tk.WORD)
        self.output_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Поле ввода команд
        self.input_entry = tk.Entry(self.root, font=('Courier New', 12))
        self.input_entry.pack(padx=10, pady=5, fill=tk.X)
        self.input_entry.bind("<Return>", self.process_command)
        self.input_entry.focus()

        # Приветствие и debug
        self.append_output("Welcome to VFS Emulator (Stage 5)")
        self.append_output(f"Debug: VFS Path = {self.vfs_path}")
        self.append_output(f"Debug: Script Path = {self.script_path}")
        self.append_output("Available commands: ls, cd, vfs-save, date, who, uniq, chmod, exit")
        self.append_output("")

        # Запуск скрипта
        if self.script_path:
            self.run_script(self.script_path)

        self.append_output("$ ", newline=False)

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

    # Команда chmod
    def chmod_command(self, mode, name):
        folder = get_current_folder()
        if name in folder:
            folder[name]["permissions"] = mode
            return f"{name} permissions changed to {mode}"
        else:
            return f"chmod: no such file or folder: {name}"

    # Выполнение команды
    def execute_command(self, args):
        global current_path
        if not args:
            return ""
        cmd = args[0]

        if cmd == "ls":
            folder = get_current_folder()
            return "  ".join(folder.keys()) if folder else "(empty)"

        elif cmd == "cd":
            if len(args) < 2:
                return "cd: missing argument"
            folder = get_current_folder()
            if args[1] == "..":
                if len(current_path) > 1:
                    current_path.pop()
                    return f"Current path: {'/'.join(current_path)}"
                else:
                    return "Already at root"
            elif args[1] in folder and folder[args[1]]["type"] == "folder":
                current_path.append(args[1])
                return f"Current path: {'/'.join(current_path)}"
            else:
                return f"cd: no such folder: {args[1]}"

        elif cmd == "vfs-save":
            if len(args) < 2:
                return "vfs-save: missing filename"
            self.save_vfs_csv(args[1])
            return f"VFS saved to {args[1]}"

        elif cmd == "date":
            now = datetime.datetime.now()
            return now.strftime("%Y-%m-%d %H:%M:%S")

        elif cmd == "who":
            return "user1  user2  user3"

        elif cmd == "uniq":
            return "(uniq command placeholder)"

        elif cmd == "chmod":
            if len(args) < 3:
                return "chmod: missing arguments"
            mode, name = args[1], args[2]
            return self.chmod_command(mode, name)

        elif cmd == "exit":
            self.append_output("Exiting...")
            self.root.after(500, self.root.destroy)
            return ""

        else:
            return f"Unknown command: {cmd}"

    # --- Сохранение VFS ---
    def flatten_vfs(self, path, node):
        rows = []
        for name, info in node.items():
            row_path = "/".join(path + [name])
            if info["type"] == "file":
                content = base64.b64encode(info["content"].encode()).decode()
                rows.append([row_path, "file", content, info.get("permissions", "")])
            else:
                rows.append([row_path, "folder", "", info.get("permissions", "")])
                rows.extend(self.flatten_vfs(path + [name], info["children"]))
        return rows

    def save_vfs_csv(self, filename):
        rows = self.flatten_vfs([], vfs)
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["path", "type", "content", "permissions"])
            writer.writerows(rows)

    # --- Скрипты ---
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

    # Обработка ввода пользователя
    def process_command(self, event):
        command_text = self.input_entry.get()
        self.input_entry.delete(0, tk.END)

        self.append_output(f"$ {command_text}")
        args = self.parse_command(command_text)
        result = self.execute_command(args)
        if result:
            self.append_output(result)
        self.append_output("$ ", newline=False)

    # Запуск GUI
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="VFS Emulator GUI Stage 5")
    parser.add_argument("--vfs-path", type=str, help="Path to VFS folder")
    parser.add_argument("--script", type=str, help="Path to startup script")
    args = parser.parse_args()

    emulator = VFSEmulatorGUIStage5(vfs_path=args.vfs_path, script_path=args.script)
    emulator.run()