import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import os

# 请用户输入要读取的子文件夹名称
subdir_name = input("请输入要读取的子文件夹名称/Please enter the name of the subfolder you want to read：")

# 定义log文件夹的路径
log_dir = 'log'

# 读取指定子文件夹下所有txt文件
log_files = os.listdir(os.path.join(log_dir, subdir_name))
log_data = []
for file_name in log_files:
    if file_name.endswith('.txt'):
        with open(os.path.join(log_dir, subdir_name, file_name), 'r') as f:
            lines = f.readlines()
            cpu_usage = float(lines[0].split(':')[1].strip().replace('%', ''))
            mem_usage = float(lines[1].split(':')[1].strip().replace('%', ''))
            log_data.append([file_name.split('.')[0], cpu_usage, mem_usage])

# 将数据转为pandas的DataFrame格式
df = pd.DataFrame(log_data, columns=['Time', 'CPU Usage', 'Memory Usage'])
df = df.set_index('Time')

# 定义百分比格式化函数
def to_percent(y, position):
    return str(int(y)) + '%'

# 画折线图
plt.figure(figsize=(10, 8))
plt.plot(df.index, df['CPU Usage'], label='CPU Usage')
plt.plot(df.index, df['Memory Usage'], label='Memory Usage')
x_ticks = df.index[::2]
plt.xticks(x_ticks, rotation=90)  # 设置x轴刻度文字旋转90度
plt.ylabel('Usage')
plt.title('System Usage')
plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percent))  # 设置y轴标签为百分比形式
plt.legend()
plt.tight_layout()  # 自动调整子图参数，避免超出边界
plt.show()
