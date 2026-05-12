import os
import tkinter as tk
from tkinter import filedialog, messagebox
from rembg import remove
from PIL import Image

def run_remove_bg():
    root = tk.Tk()
    root.withdraw()

    # 1. 选择图片
    file_path = filedialog.askopenfilename(
        title="选择要抠图的照片",
        filetypes=[("Image files", "*.jpg *.jpeg *.png")]
    )

    if not file_path:
        return

    # 2. 准备输出路径 (保存为 png)
    dir_name = os.path.dirname(file_path)
    pure_name = os.path.splitext(os.path.basename(file_path))[0]
    output_path = os.path.join(dir_name, f"{pure_name}_transparent.png")

    try:
        print(f"正在抠图: {file_path}...")
        input_image = Image.open(file_path)
        
        # 3. 核心功能
        output_image = remove(input_image)
        output_image.save(output_path)
        
        # 4. Mac 特色功能：自动用预览打开结果
        os.system(f"open '{output_path}'")
        
        messagebox.showinfo("成功", f"抠图完成！\n结果已保存至同目录。")
    except Exception as e:
        messagebox.showerror("错误", f"出错了：{e}")

if __name__ == "__main__":
    run_remove_bg()