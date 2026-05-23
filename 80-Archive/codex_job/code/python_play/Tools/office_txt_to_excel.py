import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox

from pathlib import Path
ROOT = Path(__file__).resolve().parent

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
        input_path = Path(file_path)
        dir_name = input_path.parent
        pure_name = input_path.stem
        output_path = dir_name / f"{pure_name}.xlsx"

        # 4. 读取并转换 (默认逗号分隔)
        df = pd.read_csv(file_path, sep=',', engine='python', encoding='utf-8')
        df.to_excel(output_path, index=False)

        # 5. 弹出成功提示
        messagebox.showinfo("成功", f"文件已保存至：\n{output_path}")
    except Exception as e:
        messagebox.showerror("错误", f"转换失败：{e}")

if __name__ == "__main__":
    txt_to_excel_gui()
