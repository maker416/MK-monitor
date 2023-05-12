import psutil
import datetime
import time
import os
from tkinter import *
from tkinter import ttk
from tkinter import font

# 创建UI界面
root = Tk()
root.title("系统监控")
root.geometry("420x400")
root.resizable(0, 0)

# 设置窗口背景颜色
root.configure(background="#F0F0F0")
frame = Frame(root, bg="#F0F0F0")
frame.pack(fill=BOTH, expand=True)

# 设置字体样式
title_font = font.Font(family="Microsoft YaHei", size=20, weight="bold")
label_font = font.Font(family="Microsoft YaHei", size=12, weight="bold")

# 设置标题标签
title_label = Label(frame, text="系统监控", font=title_font, bg="#F0F0F0")
title_label.pack(pady=10)

# 创建三个进度条控件和对应的标签控件
cpu_label = Label(frame, text="CPU使用率", font=label_font, bg="#F0F0F0")
mem_label = Label(frame, text="内存使用率", font=label_font, bg="#F0F0F0")
net_label = Label(frame, text="网络使用量", font=label_font, bg="#F0F0F0")

cpu_progress = ttk.Progressbar(frame, variable=DoubleVar(), length=300, mode="determinate")
mem_progress = ttk.Progressbar(frame, variable=DoubleVar(), length=300, mode="determinate")
net_progress = ttk.Progressbar(frame, variable=DoubleVar(), length=300, mode="determinate")

cpu_percent_label = Label(frame, text="0%", font=label_font, bg="#F0F0F0")
mem_percent_label = Label(frame, text="0%", font=label_font, bg="#F0F0F0")
net_percent_label = Label(frame, text="0%", font=label_font, bg="#F0F0F0")

# 将控件放置到UI界面上
cpu_label.pack(padx=10, pady=5, anchor=W)
cpu_progress.pack(padx=10, pady=5)
cpu_percent_label.pack(padx=10, pady=5, anchor=W)

mem_label.pack(padx=10, pady=5, anchor=W)
mem_progress.pack(padx=10, pady=5)
mem_percent_label.pack(padx=10, pady=5, anchor=W)

net_label.pack(padx=10, pady=5, anchor=W)
net_progress.pack(padx=10, pady=5)
net_percent_label.pack(padx=10, pady=5, anchor=W)

# 设置进度条颜色
style = ttk.Style()
style.theme_use("clam")
style.configure("TProgressbar", foreground="#0066CC", background="#CCE5FF")

# 实时获取CPU、内存、网络占用率
def get_system_info():
    cpu_usage = psutil.cpu_percent()
    mem_usage = psutil.virtual_memory().percent
    net_usage = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv
    time.sleep(1)
    net_usage = (psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv - net_usage) / 1024
    return cpu_usage, mem_usage, net_usage

# 更新进度条控件和对应的标签控件的数值
def update_progressbars():
    while True:
        cpu_usage, mem_usage, net_usage = get_system_info()
        cpu_progress["value"] = cpu_usage
        mem_progress["value"] = mem_usage
        net_progress["value"] = net_usage

        cpu_percent_label.configure(text="{}%".format(cpu_usage))
        mem_percent_label.configure(text="{}%".format(mem_usage))
        net_percent_label.configure(text="{}KB".format(round(net_usage, 2)))

        time.sleep(1)

# 创建一个线程来更新进度条控件
import threading
update_thread = threading.Thread(target=update_progressbars)
update_thread.start()

# 确保log文件夹存在
if not os.path.exists("log"):
    os.mkdir("log")

# 每10秒记录当前各项数值到txt文档
def save_system_info():
    while True:
        now = datetime.datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H-%M-%S")
        cpu_usage, mem_usage, net_usage = get_system_info()
        folder_name = os.path.join("log", date_str)
        if not os.path.exists(folder_name):
            os.mkdir(folder_name)
        with open(os.path.join(folder_name, "{}.txt".format(time_str)), "w") as f:
            f.write("CPU usage: {}%\n".format(cpu_usage))
            f.write("Memory usage: {}%\n".format(mem_usage))
            f.write("Network usage: {}KB\n".format(round(net_usage, 2)))
        time.sleep(10)

# 创建一个线程来保存系统信息
save_thread = threading.Thread(target=save_system_info)
save_thread.start()

# 运行UI界面
root.mainloop()