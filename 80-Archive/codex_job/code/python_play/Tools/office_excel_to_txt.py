import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog, messagebox

def excel_to_txt_gui():
    root = tk.Tk()
    root.withdraw()

    # 1. 选择 Excel 文件
    file_path = filedialog.askopenfilename(
        title="选择要转换的 Excel 文件",
        filetypes=[("Excel files", "*.xlsx *.xls")]
    )

    if not file_path:
        return

    try:
        # 2. 自动生成同源路径
        dir_name = os.path.dirname(file_path)
        pure_name = os.path.splitext(os.path.basename(file_path))[0]
        output_path = os.path.join(dir_name, f"{pure_name}.txt")

        # 3. 读取并保存为 Tab 分隔的 TXT
        df = pd.read_excel(file_path)
        df.to_csv(output_path, sep='\t', index=False, encoding='utf-8')

        messagebox.showinfo("成功", f"文件已保存至：\n{output_path}")
    except Exception as e:
        messagebox.showerror("错误", f"转换失败：{e}")

if __name__ == "__main__":
    excel_to_txt_gui()