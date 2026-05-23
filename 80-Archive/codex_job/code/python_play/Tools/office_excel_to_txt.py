import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox

from pathlib import Path
ROOT = Path(__file__).resolve().parent

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
        input_path = Path(file_path)
        dir_name = input_path.parent
        pure_name = input_path.stem
        output_path = dir_name / f"{pure_name}.txt"

        # 3. 读取并保存为 Tab 分隔的 TXT
        df = pd.read_excel(file_path)
        df.to_csv(output_path, sep='\t', index=False, encoding='utf-8')

        messagebox.showinfo("成功", f"文件已保存至：\n{output_path}")
    except Exception as e:
        messagebox.showerror("错误", f"转换失败：{e}")

if __name__ == "__main__":
    excel_to_txt_gui()
