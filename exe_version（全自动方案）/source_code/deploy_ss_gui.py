"""
@Author  : Jilin Zhou
@Email   : zhoujilin.bupt@hotmail.com
@Date    : 2025/9/9
@Software: PyCharm
"""
import tkinter as tk
from tkinter import messagebox, scrolledtext
import paramiko, json, threading
import webbrowser  # 导入webbrowser模块以打开客户端下载链接

class WizardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Shadowsocks 自动化部署向导")
        self.root.geometry("650x500")

        self.current_step = 0
        self.steps = [self.welcome_page, self.notice_page, self.form_page, self.deploy_page]

        self.frame = tk.Frame(self.root)
        self.frame.pack(fill="both", expand=True)
        self.steps[self.current_step]()  # 初始化第一页

    def clear_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    def next_step(self):
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self.clear_frame()
            self.steps[self.current_step]()

    def prev_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.clear_frame()
            self.steps[self.current_step]()

    # Step 1: 欢迎页面
    def welcome_page(self):
        tk.Label(self.frame, text="欢迎使用 Shadowsocks 自动化部署工具",
                 font=("Arial", 16)).pack(pady=20)
        tk.Label(self.frame, text="本工具将引导您在服务器上自动安装和配置 Shadowsocks。",
                 font=("Arial", 12)).pack(pady=10)
        tk.Button(self.frame, text="下一步", command=self.next_step).pack(pady=20)

    # Step 2: 使用须知
    def notice_page(self):
        text = (
            "⚠️ 使用须知\n\n"
            "请先在您的云服务商控制台（安全组/防火墙设置）中：\n"
            "1. 开放 Shadowsocks 使用的端口（默认 8388）。\n"
            "2. 协议需同时开放 TCP 和 UDP。\n"
            "3. 来源地址请设置为 0.0.0.0/0。\n\n"
            "常见云厂商路径(要么叫安全组，要么叫防火墙，自行找到对应的即可)：\n"
            "- 安全组 → 配置规则\n"
            "- 防火墙规则 → 添加规则\n"
            "- EC2 安全组 → Inbound Rules\n"
        )
        tk.Label(self.frame, text=text, justify="left").pack(padx=20, pady=20)
        tk.Button(self.frame, text="上一步", command=self.prev_step).pack(side="left", padx=50, pady=20)
        tk.Button(self.frame, text="下一步", command=self.next_step).pack(side="right", padx=50, pady=20)

    # Step 3: 塬写信息
    def form_page(self):
        tk.Label(self.frame, text="请输入服务器与 Shadowsocks 配置信息",
                 font=("Arial", 14)).pack(pady=10)

        self.ip_entry = self.add_entry("服务器 IP:")
        self.user_entry = self.add_entry("SSH 用户名 (默认 root):")
        self.pwd_entry = self.add_entry("SSH 密码:", show="*")
        self.port_entry = self.add_entry("Shadowsocks 端口 (默认 8388):")
        self.ss_pwd_entry = self.add_entry("Shadowsocks 密码:", show="*")

        tk.Button(self.frame, text="上一步", command=self.prev_step).pack(side="left", padx=50, pady=20)
        tk.Button(self.frame, text="开始部署", command=self.start_deploy).pack(side="right", padx=50, pady=20)

    def add_entry(self, label, show=None):
        tk.Label(self.frame, text=label).pack()
        entry = tk.Entry(self.frame, width=40, show=show)
        entry.pack()
        return entry

    # Step 4: 部署日志
    def deploy_page(self):
        tk.Label(self.frame, text="部署进度", font=("Arial", 14)).pack(pady=10)
        self.log_widget = scrolledtext.ScrolledText(self.frame, width=70, height=20)
        self.log_widget.pack(padx=10, pady=10)

        # 添加客户端下载按钮
        tk.Button(self.frame, text="自己的电脑用的客户端下载地址", command=self.open_client_download).pack(pady=10)

    def log(self, msg):
        self.log_widget.insert(tk.END, msg + "\n")
        self.log_widget.see(tk.END)
        self.log_widget.update()

    def open_client_download(self):
        # 打开浏览器，访问 Shadowsocks Windows 客户端的下载页面
        webbrowser.open("https://github.com/shadowsocks/shadowsocks-windows", new=2)

    def start_deploy(self):
        ip = self.ip_entry.get()
        user = self.user_entry.get() or "root"
        passwd = self.pwd_entry.get()
        port = self.port_entry.get() or "8388"
        ss_passwd = self.ss_pwd_entry.get()

        if not ip or not passwd or not ss_passwd:
            messagebox.showwarning("提示", "请完整填写必填项！")
            return

        self.next_step()
        threading.Thread(target=self.deploy_task, args=(ip, user, passwd, port, ss_passwd)).start()

    def deploy_task(self, ip, user, passwd, port, ss_passwd):
        try:
            self.log("[*] 正在连接服务器...")
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip, username=user, password=passwd)

            def run_cmd(cmd, step=""):
                stdin, stdout, stderr = ssh.exec_command(cmd)
                out, err = stdout.read().decode(), stderr.read().decode()
                if step:
                    self.log(f"[*] {step}")
                if out:
                    self.log(out.strip())
                if err:
                    self.log("[错误] " + err.strip())

            # 部署流程
            run_cmd("yum install -y epel-release", "安装 epel 源")
            run_cmd("yum install -y python3-pip", "安装 python3-pip")
            run_cmd("pip3 install --upgrade pip", "检查pip更新")
            run_cmd("pip3 install shadowsocks", "安装 shadowsocks")

            config = {
                "server": "0.0.0.0",
                "server_port": int(port),
                "local_address": "127.0.0.1",
                "local_port": 1080,
                "password": ss_passwd,
                "timeout": 300,
                "method": "aes-256-cfb",
                "fast_open": False
            }
            config_json = json.dumps(config, indent=4)
            run_cmd(f"echo '{config_json}' > /etc/shadowsocks.json", "写入配置文件")
            run_cmd("chmod 600 /etc/shadowsocks.json", "设置运行权限")
            run_cmd("ssserver -c /etc/shadowsocks.json -d start", "启动 Shadowsocks")

            ssh.close()
            self.log("\n 部署完成 \n请在本地开启代理并自行登录一些网站进行验证，过程中的报错和warning一般无影响 \n如果仍未成功，请首先检查防火墙,然后用cat指令检查shadowsocks.json文件是否正确写入")
            messagebox.showinfo("完成", "Shadowsocks 部署成功！")

        except Exception as e:
            self.log(f"[失败] {str(e)}")
            messagebox.showerror("错误", f"部署失败：{e}")

# 运行程序
if __name__ == "__main__":
    root = tk.Tk()
    app = WizardApp(root)
    root.mainloop()
