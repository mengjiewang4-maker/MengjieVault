import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog, messagebox

def txt_to_excel_gui():
    # 1. 初始化并隐藏主窗口
    root = tk.Tk()
    root.withdraw()

    # 2. 弹出文件选择对话框
    file_path = filedialog.askopenfilename(
        title="选择要转换的 TXT 文件",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )

    if not file_path:
        return

    try:
        # 3. 自动计算同源路径
        dir_name = os.path.dirname(file_path)
        pure_name = os.path.splitext(os.path.basename(file_path))[0]
        output_path = os.path.join(dir_name, f"{pure_name}.xlsx")

        # 4. 读取并转换 (默认逗号分隔)
        df = pd.read_csv(file_path, sep=',', engine='python', encoding='utf-8')
        df.to_excel(output_path, index=False)

        # 5. 弹出成功提示
        messagebox.showinfo("成功", f"文件已保存至：\n{output_path}")
    except Exception as e:
        messagebox.showerror("错误", f"转换失败：{e}")

if __name__ == "__main__":
    txt_to_excel_gui()