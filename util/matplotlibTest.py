import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# 创建Tkinter窗口
root = tk.Tk()
root.title("Matplotlib 柱状图示例")

# 创建一个Notebook式的下拉菜单
dataset_chooser = ttk.Combobox(root, width=20)
dataset_chooser["values"] = ("DataSet1", "DataSet2", "DataSet3")
dataset_chooser.current(0)
dataset_chooser.grid(row=0, column=0)

# 创建一个用于绘图的Figure和Axes
fig, ax = plt.subplots()


# 定义绘图函数
def update_plot(dataset):
    if dataset == "DataSet1":
        data = np.random.rand(5)
    elif dataset == "DataSet2":
        data = np.random.rand(5) * 2
    else:
        data = np.random.rand(5) * 0.5

    ax.clear()
    ax.bar(np.arange(len(data)), data,color="#FF0000")
    ax.set_title(dataset)
    canvas.draw()


# 绑定下拉菜单选择事件到绘图函数
dataset_chooser.bind("<<ComboboxSelected>>", lambda event: update_plot(dataset_chooser.get()))

# 创建一个画布，并将其嵌入到Tkinter窗口中
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().grid(row=1, column=0)

# 启动Tkinter事件循环
root.mainloop()