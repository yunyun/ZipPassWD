import zipfile
import itertools
import string
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog


class ZipBruteGUI:
    def __init__(self, master):
        self.master = master
        master.title("ZIP暴力破解工具 v2.0")
        master.geometry("600x450")
        self.running = False
        self.create_widgets()

    def create_widgets(self):
        input_frame = ttk.LabelFrame(self.master, text="参数设置")
        input_frame.pack(padx=10, pady=5, fill="x")

        # ZIP文件路径
        ttk.Label(input_frame, text="ZIP文件:").grid(row=0, column=0)
        self.zip_path = ttk.Entry(input_frame, width=40)
        self.zip_path.grid(row=0, column=1)
        ttk.Button(input_frame, text="浏览", command=self.select_zip).grid(row=0, column=2)

        # 字符集选择
        ttk.Label(input_frame, text="字符集:").grid(row=1, column=0)
        self.charset = ttk.Combobox(input_frame, values=["数字", "小写字母", "大写字母", "混合字符"])
        self.charset.current(0)
        self.charset.grid(row=1, column=1)

        # 密码长度
        ttk.Label(input_frame, text="最小长度:").grid(row=2, column=0)
        self.min_len = ttk.Spinbox(input_frame, from_=1, to=8, width=5)
        self.min_len.set(1)
        self.min_len.grid(row=2, column=1)
        ttk.Label(input_frame, text="最大长度:").grid(row=2, column=2)
        self.max_len = ttk.Spinbox(input_frame, from_=1, to=8, width=5)
        self.max_len.set(3)
        self.max_len.grid(row=2, column=3)

        # 控制按钮
        btn_frame = ttk.Frame(self.master)
        btn_frame.pack(pady=5)
        self.start_btn = ttk.Button(btn_frame, text="开始破解", command=self.toggle_crack)
        self.start_btn.pack(side="left")
        ttk.Button(btn_frame, text="退出", command=self.master.quit).pack(side="left", padx=10)

        # 进度条
        self.progress = ttk.Progressbar(self.master, mode='determinate')
        self.progress.pack(padx=10, fill="x")

        # 日志输出
        log_frame = ttk.LabelFrame(self.master, text="运行日志")
        log_frame.pack(padx=10, pady=5, fill="both", expand=True)
        self.log_area = scrolledtext.ScrolledText(log_frame, height=8)
        self.log_area.pack(fill="both", expand=True)

    def select_zip(self):
        filepath = filedialog.askopenfilename(filetypes=[("ZIP Files", "*.zip")])
        if filepath:
            self.zip_path.delete(0, tk.END)
            self.zip_path.insert(0, filepath)

    def toggle_crack(self):
        if not self.running:
            self.start_crack()
            self.start_btn.config(text="停止破解")
        else:
            self.running = False
            self.start_btn.config(text="开始破解")

    def start_crack(self):
        if not self.zip_path.get().endswith('.zip'):
            self.log("错误：请选择有效的ZIP文件", "red")
            return

        charset_map = {
            "数字": string.digits,
            "小写字母": string.ascii_lowercase,
            "大写字母": string.ascii_uppercase,
            "混合字符": string.digits + string.ascii_letters
        }

        params = {
            'charset': charset_map[self.charset.get()],
            'min_len': int(self.min_len.get()),
            'max_len': int(self.max_len.get())
        }

        self.running = True
        threading.Thread(target=self.crack_thread, args=(params,), daemon=True).start()

    def crack_thread(self, params):
        total = sum(len(params['charset']) ** i for i in range(params['min_len'], params['max_len'] + 1))
        self.progress['maximum'] = total

        try:
            for length in range(params['min_len'], params['max_len'] + 1):
                for pwd_tuple in itertools.product(params['charset'], repeat=length):
                    if not self.running:
                        return
                    pwd = ''.join(pwd_tuple)
                    self.try_password(pwd)
                    self.progress.step(1)
        except Exception as e:
            self.log(f"错误: {str(e)}", "red")
        finally:
            self.running = False

    def try_password(self, pwd):
        try:
            with zipfile.ZipFile(self.zip_path.get()) as zf:
                zf.extractall(path="/tmp", pwd=pwd.encode())
                self.log(f"破解成功！密码是: {pwd}", "green")
                self.running = False
        except RuntimeError as e:
            if 'password' in str(e).lower():
                self.log(f"尝试密码: {pwd}")
        except Exception as e:
            self.log(f"文件错误: {str(e)}", "red")

    def log(self, message, color="black"):
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = ZipBruteGUI(root)
    root.mainloop()
