import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox


class FrpcLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("frpc 启动器")

        # 禁止调整窗口大小和禁止最大化窗口
        self.root.resizable(False, False)

        # 用户目录下的配置文件路径
        self.config_file_path = os.path.join(os.path.expanduser("~"), ".frpc.ini")

        # 检查配置文件是否存在，如果不存在则创建
        if not os.path.exists(self.config_file_path):
            self.create_default_config()

        # 读取配置文件中的 frpc 路径
        self.frpc_path = self.read_config()

        # 创建界面元素
        self.label = tk.Label(root, text="选择 frpc 可执行文件：")
        self.label.pack(pady=10)

        self.frpc_path_var = tk.StringVar(value=self.frpc_path)
        self.entry = tk.Entry(root, textvariable=self.frpc_path_var, width=50)
        self.entry.pack()

        self.browse_button = tk.Button(root, text="浏览", command=self.browse_frpc)
        self.browse_button.pack(pady=10)

        # 启动和结束 frpc 的按钮
        button_frame = tk.Frame(root)
        button_frame.pack(pady=20)

        self.start_button = tk.Button(button_frame, text="启动 frpc", command=self.start_frpc)
        self.start_button.grid(row=0, column=0, padx=10)

        self.stop_button = tk.Button(button_frame, text="结束 frpc", command=self.stop_frpc)
        self.stop_button.grid(row=0, column=1, padx=10)

        self.config_button = tk.Button(root, text="修改配置文件", command=self.edit_config)
        self.config_button.pack(pady=20)

        # 用于存储 frpc 进程
        self.frpc_process = None

    def create_default_config(self):
        """创建默认的配置文件"""
        with open(self.config_file_path, "w", encoding="utf-8") as file:
            file.write("[Frpc Start]\n")
            file.write("Frpc = \n")
            file.write("\n")
            file.write("# Powered By ljy2231\n")

    def read_config(self):
        """读取配置文件中的 frpc 路径"""
        config = {}
        with open(self.config_file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
        for line in lines:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                config[key.strip()] = value.strip()
        return config.get("Frpc", "")

    def save_config(self, frpc_path):
        """保存 frpc 路径到配置文件"""
        with open(self.config_file_path, "w", encoding="utf-8") as file:
            file.write("[Frpc Start]\n")
            file.write(f"Frpc = {frpc_path}\n")
            file.write("\n")
            file.write("# Powered By ljy2231\n")

    def browse_frpc(self):
        """选择 frpc 可执行文件"""
        file_path = filedialog.askopenfilename(filetypes=[("Executable files", "*.exe")])
        if file_path:
            self.frpc_path_var.set(file_path)
            self.save_config(file_path)

    def start_frpc(self):
        """启动 frpc"""
        frpc_path = self.frpc_path_var.get()
        if not frpc_path:
            messagebox.showwarning("警告", "请先选择 frpc 可执行文件！")
            return

        if not os.path.exists(frpc_path):
            messagebox.showerror("错误", "指定的 frpc 可执行文件不存在！")
            return

        if self.frpc_process and self.frpc_process.poll() is None:
            messagebox.showwarning("警告", "frpc 已经在运行！")
            return

        try:
            self.frpc_process = subprocess.Popen([frpc_path, "-c", os.path.join(os.path.dirname(frpc_path), "frpc.ini")])
            messagebox.showinfo("成功", "frpc 已启动！")
        except Exception as e:
            messagebox.showerror("错误", f"启动 frpc 时发生错误：{e}")

    def stop_frpc(self):
        """结束 frpc"""
        if self.frpc_process and self.frpc_process.poll() is None:
            try:
                self.frpc_process.terminate()
                self.frpc_process.wait()
                messagebox.showinfo("成功", "frpc 已停止！")
            except Exception as e:
                messagebox.showerror("错误", f"停止 frpc 时发生错误：{e}")
        else:
            messagebox.showwarning("警告", "frpc 没有在运行！")

    def on_closing(self):
        """处理窗口关闭事件"""
        if self.frpc_process and self.frpc_process.poll() is None:
            try:
                self.frpc_process.terminate()
                self.frpc_process.wait()
            except Exception as e:
                messagebox.showerror("错误", f"停止 frpc 时发生错误：{e}")
        self.root.destroy()

    def edit_config(self):
        """编辑 frpc.ini 配置文件"""
        frpc_path = self.frpc_path_var.get()
        if not frpc_path:
            messagebox.showwarning("警告", "请先选择 frpc 可执行文件！")
            return

        config_path = os.path.join(os.path.dirname(frpc_path), "frpc.ini")
        if not os.path.exists(config_path):
            messagebox.showerror("错误", "未找到 frpc.ini 配置文件！")
            return

        self.config_window = tk.Toplevel(self.root)
        self.config_window.title("编辑 frpc.ini 配置文件")
        self.config_window.resizable(False, False)  # 禁止调整子窗口大小

        # 创建表单
        self.common_frame = tk.LabelFrame(self.config_window, text="通用配置")
        self.common_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.tunnel_frame = tk.LabelFrame(self.config_window, text="通道配置")
        self.tunnel_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # 通用配置
        tk.Label(self.common_frame, text="服务器地址：").grid(row=0, column=0, padx=5, pady=5)
        self.server_addr = tk.Entry(self.common_frame, width=30)
        self.server_addr.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.common_frame, text="服务器端口：").grid(row=1, column=0, padx=5, pady=5)
        self.server_port = tk.Entry(self.common_frame, width=30)
        self.server_port.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.common_frame, text="用户：").grid(row=2, column=0, padx=5, pady=5)
        self.user = tk.Entry(self.common_frame, width=30)
        self.user.grid(row=2, column=1, padx=5, pady=5)

        # 通道配置
        tk.Label(self.tunnel_frame, text="通道名称：").grid(row=0, column=0, padx=5, pady=5)
        self.tunnel_name = tk.Entry(self.tunnel_frame, width=30)
        self.tunnel_name.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.tunnel_frame, text="协议类型：").grid(row=1, column=0, padx=5, pady=5)
        self.tunnel_type = tk.Entry(self.tunnel_frame, width=30)
        self.tunnel_type.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.tunnel_frame, text="本地 IP：").grid(row=2, column=0, padx=5, pady=5)
        self.local_ip = tk.Entry(self.tunnel_frame, width=30)
        self.local_ip.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.tunnel_frame, text="本地端口：").grid(row=3, column=0, padx=5, pady=5)
        self.local_port = tk.Entry(self.tunnel_frame, width=30)
        self.local_port.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(self.tunnel_frame, text="远程端口：").grid(row=4, column=0, padx=5, pady=5)
        self.remote_port = tk.Entry(self.tunnel_frame, width=30)
        self.remote_port.grid(row=4, column=1, padx=5, pady=5)

        # 加载现有配置
        self.load_config(config_path)

        # 按钮区域
        button_frame = tk.Frame(self.config_window)
        button_frame.pack(pady=10)

        # 清空配置文件按钮
        self.clear_button = tk.Button(button_frame, text="清空配置文件", command=lambda: self.clear_config(config_path))
        self.clear_button.grid(row=0, column=0, padx=10)

        # 保存配置按钮
        self.save_button = tk.Button(button_frame, text="保存配置", command=lambda: self.save_config_file(config_path))
        self.save_button.grid(row=0, column=1, padx=10)

        # 直接修改配置文件按钮
        self.edit_text_button = tk.Button(button_frame, text="直接修改配置文件", command=lambda: self.open_config_file(config_path))
        self.edit_text_button.grid(row=0, column=2, padx=10)

    def load_config(self, config_path):
        """加载现有配置文件"""
        with open(config_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        config = {}
        for line in lines:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                config[key.strip()] = value.strip()

        # 设置表单内容
        self.server_addr.insert(0, config.get("serverAddr", ""))
        self.server_port.insert(0, config.get("serverport", ""))
        self.user.insert(0, config.get("user", ""))
        self.tunnel_name.insert(0, config.get("name", ""))
        self.tunnel_type.insert(0, config.get("type", ""))
        self.local_ip.insert(0, config.get("localIP", ""))
        self.local_port.insert(0, config.get("localPort", ""))
        self.remote_port.insert(0, config.get("remotePort", ""))

    def clear_config(self, config_path):
        """清空配置文件"""
        try:
            with open(config_path, "w", encoding="utf-8") as file:
                file.write("")  # 清空文件内容
            messagebox.showinfo("成功", "配置文件已清空！")
            # 清空表单内容
            self.server_addr.delete(0, tk.END)
            self.server_port.delete(0, tk.END)
            self.user.delete(0, tk.END)
            self.tunnel_name.delete(0, tk.END)
            self.tunnel_type.delete(0, tk.END)
            self.local_ip.delete(0, tk.END)
            self.local_port.delete(0, tk.END)
            self.remote_port.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("错误", f"清空配置文件时发生错误：{e}")

    def save_config_file(self, config_path):
        """保存配置文件"""
        config = {
            "serverAddr": self.server_addr.get(),
            "serverport": self.server_port.get(),
            "user": self.user.get(),
            "name": self.tunnel_name.get(),
            "type": self.tunnel_type.get(),
            "localIP": self.local_ip.get(),
            "localPort": self.local_port.get(),
            "remotePort": self.remote_port.get()
        }

        try:
            with open(config_path, "w", encoding="utf-8") as file:
                file.write("[common]\n")
                file.write(f"serverAddr = {config['serverAddr']}\n")
                file.write(f"serverport = {config['serverport']}\n")
                file.write(f"user = {config['user']}\n\n")

                file.write("[[tunnels]]\n")
                file.write(f"name = {config['name']}\n")
                file.write(f"type = {config['type']}\n")
                file.write(f"localIP = {config['localIP']}\n")
                file.write(f"localPort = {config['localPort']}\n")
                file.write(f"remotePort = {config['remotePort']}\n")

            messagebox.showinfo("成功", "配置文件已保存！")
            self.config_window.destroy()
        except Exception as e:
            messagebox.showerror("错误", f"保存配置文件时发生错误：{e}")

    def open_config_file(self, config_path):
        """直接在软件内编辑配置文件"""
        self.config_text_window = tk.Toplevel(self.config_window)
        self.config_text_window.title("直接编辑配置文件")
        self.config_text_window.resizable(False, False)  # 禁止调整子窗口大小

        # 创建文本框用于编辑配置文件
        self.config_text = tk.Text(self.config_text_window, height=20, width=60)
        self.config_text.pack(pady=10, padx=10, fill="both", expand=True)

        # 加载配置文件内容
        with open(config_path, "r", encoding="utf-8") as file:
            config_content = file.read()
        self.config_text.insert(tk.END, config_content)

        # 按钮区域
        button_frame = tk.Frame(self.config_text_window)
        button_frame.pack(pady=10)

        # 清空配置文件按钮
        self.clear_text_button = tk.Button(button_frame, text="清空配置文件", command=lambda: self.clear_text_config(config_path))
        self.clear_text_button.grid(row=0, column=0, padx=10)

        # 保存按钮
        self.save_text_button = tk.Button(button_frame, text="保存配置", command=lambda: self.save_text_config(config_path))
        self.save_text_button.grid(row=0, column=1, padx=10)

    def clear_text_config(self, config_path):
        """清空直接编辑的配置文件内容"""
        try:
            with open(config_path, "w", encoding="utf-8") as file:
                file.write("")  # 清空文件内容
            messagebox.showinfo("成功", "配置文件已清空！")
            self.config_text.delete("1.0", tk.END)  # 清空文本框内容
        except Exception as e:
            messagebox.showerror("错误", f"清空配置文件时发生错误：{e}")

    def save_text_config(self, config_path):
        """保存直接编辑的配置文件内容"""
        new_content = self.config_text.get("1.0", tk.END)
        try:
            with open(config_path, "w", encoding="utf-8") as file:
                file.write(new_content)
            messagebox.showinfo("成功", "配置文件已保存！")
            self.config_text_window.destroy()
            self.config_window.destroy()  # 关闭第二页窗口
        except Exception as e:
            messagebox.showerror("错误", f"保存配置文件时发生错误：{e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = FrpcLauncher(root)
    root.mainloop()