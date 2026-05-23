import pandas as pd
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from pathlib import Path
ROOT = Path(__file__).resolve().parent

def start_conversion():
    # 1. 获取用户选择的模式
    mode = mode_combo.get()
    
    # 2. 弹出文件选择框
    if "TXT 转 Excel" in mode:
        file_path = filedialog.askopenfilenames(title="选择 TXT 文件", filetypes=[("Text files", "*.txt")])
    else:
        file_path = filedialog.askopenfilenames(title="选择 Excel 文件", filetypes=[("Excel files", "*.xlsx *.xls")])

    if not file_path:
        return

    try:
        # 3. 路径处理
        input_path = Path(file_path)
        dir_name = input_path.parent
        pure_name = input_path.stem
        
        # 4. 根据模式执行逻辑
        if mode == "TXT 转 Excel":
            output_path = dir_name / f"{pure_name}.xlsx"
            # 这里默认逗号分隔，你可以根据需要修改
            df = pd.read_csv(file_path, sep=',', engine='python', encoding='utf-8')
            df.to_excel(output_path, index=False)
        else:
            output_path = dir_name / f"{pure_name}.txt"
            df = pd.read_excel(file_path)
            df.to_csv(output_path, sep='\t', index=False, encoding='utf-8')

        messagebox.showinfo("成功", f"转换完成！\n保存位置：{output_path}")
    except Exception as e:
        messagebox.showerror("错误", f"处理失败：\n{e}\n请检查文件编码或格式。")

# --- UI 界面部分 ---
root = tk.Tk()
root.title("万能 Office 转换器")
root.geometry("400x250")

# 设置内边距
main_frame = tk.Frame(root, padx=20, pady=20)
main_frame.pack(expand=True, fill="both")

# 标题标签
tk.Label(main_frame, text="请选择转换模式：", font=("微软雅黑", 12)).pack(pady=10)

# 1. 创建下拉列表 (Combobox)
mode_combo = ttk.Combobox(main_frame, font=("微软雅黑", 10), state="readonly")
# 设置选项内容
mode_combo['values'] = ("TXT 转 Excel", "Excel 转 TXT")
# 设置默认选第一个
mode_combo.current(0)
mode_combo.pack(pady=10, fill="x")



# 2. 转换按钮
convert_btn = tk.Button(
    main_frame, 
    text="选择文件并开始转换", 
    command=start_conversion,
    bg="#4CAF50", # 绿色按钮
    fg="white",
    font=("微软雅黑", 11, "bold"),
    height=2
)
convert_btn.pack(pady=20, fill="x")

# 说明文字
tk.Label(main_frame, text="* 转换后的文件将保存在原文件所在目录", fg="gray").pack()

root.mainloop()
