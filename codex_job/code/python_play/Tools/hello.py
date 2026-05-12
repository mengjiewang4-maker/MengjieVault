import tkinter as tk
from tkinter import messagebox

def say_hello():
    name = entry.get()  # 获取输入框里的内容
    if name:
        messagebox.showinfo("提示", f"你好，{name}！欢迎来到 Python 世界。")
    else:
        messagebox.showwarning("警告", "你还没输入名字呢！")

# 1. 初始化
window = tk.Tk()
window.title("交互工具")
window.geometry("400x150")

# 2. 摆放零件 (使用 grid 布局)
# 标签
label = tk.Label(window, text="请输入你的名字:", font=("Arial", 12))
label.grid(row=0, column=0, padx=10, pady=20)

# 输入框
entry = tk.Entry(window, font=("Arial", 12))
entry.grid(row=0, column=1, padx=10, pady=20)

# 按钮
btn = tk.Button(window, text="点我打招呼", command=say_hello, bg="lightblue")
btn.grid(row=1, column=0, columnspan=2, pady=10) # columnspan=2 表示横跨两列

# 3. 启动
window.mainloop()