import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
import os

from pathlib import Path
ROOT = Path(__file__).resolve().parent

def refine_signature_pro():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="选择电子签 (精准对比度版)",
        filetypes=[("图片文件", "*.png *.jpg *.jpeg")]
    )
    if not file_path: return

    try:
        img = cv2.imread(file_path)
        # 转灰度
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # --- 核心逻辑：百分比拉伸 ---
        # 找到图像中亮度分布的 2% 和 98% 分界点
        lower_percentile = np.percentile(gray, 2)
        upper_percentile = np.percentile(gray, 98)

        # 将低于 2% 的变黑，高于 98% 的变白，中间的线性拉开
        result = np.clip((gray - lower_percentile) * 255.0 / (upper_percentile - lower_percentile), 0, 255).astype(np.uint8)

        # 如果还是觉得不够黑，进行一次轻微的伽马校正（变深笔迹）
        gamma = 1.2
        invGamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
        result = cv2.LUT(result, table)

        input_path = Path(file_path)
        output_path = input_path.with_name(f"{input_path.stem}_精准修复.png")
        cv2.imwrite(str(output_path), result)
        
        messagebox.showinfo("成功", "修复完成！如果还是不理想，请尝试调整脚本中的百分比数值。")
        os.system(f"open '{output_path}'")

    except Exception as e:
        messagebox.showerror("错误", str(e))

if __name__ == "__main__":
    refine_signature_pro()
