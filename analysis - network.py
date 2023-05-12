import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import os


# 请用户输入要读取的子文件夹名称
subdir_name = input("请输入要读取的子文件夹名称/Please enter the name of the subfolder you want to read：")

# 定义log文件夹的路径
log_dir = 'log'

# 读取指定子文件夹下所有txt文件的Network Usage部分
log_data = []
log_files = os.listdir(os.path.join(log_dir, subdir_name))
for file_name in log_files:
    if file_name.endswith('.txt'):
        with open(os.path.join(log_dir, subdir_name, file_name), 'r') as f:
            lines = f.readlines()
            network_usage = lines[2].split(':')[1].strip()
            if 'KB' in network_usage:
                network_usage = float(network_usage.replace('KB', '').strip()) * 1024
            elif 'MB' in network_usage:
                network_usage = float(network_usage.replace('MB', '').strip()) * 1024 * 1024
            else:
                network_usage = float(network_usage.replace('B', '').strip())

            log_data.append([file_name.split('.')[0], network_usage])

# 将数据转为pandas的DataFrame格式
df = pd.DataFrame(log_data, columns=['Time', 'Network Usage'])
df = df.set_index('Time')

# 定义字节(Byte)转换为MB或KB的函数
def to_MB_or_KB(x, pos):
    if x > 1024 * 1024:
        return '%1.2fMB' % (x / 1024 / 1024)
    else:
        return '%1.2fKB' % (x / 1024)

# 画折线图
plt.figure(figsize=(10, 8))
plt.plot(df.index, df['Network Usage'], label='Network Usage')
plt.xlabel('Time')
x_ticks = df.index[::2]  # 每隔10个时间点显示一个刻度
plt.xticks(x_ticks, rotation=90)  # 设置x轴刻度文字旋转90度
plt.ylabel('Usage')
plt.title('Network Usage')
plt.gca().yaxis.set_major_formatter(FuncFormatter(to_MB_or_KB))  # 设置y轴标签为MB或KB形式
plt.legend()
plt.tight_layout()  # 自动调整子图参数，避免超出边界
plt.show()
