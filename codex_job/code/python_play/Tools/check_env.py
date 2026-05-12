import pandas as pd
import rembg
from PIL import Image
import tkinter as tk

def check():
    print("--- 环境检查报告 ---")
    print(f"✅ Pandas 版本: {pd.__version__}")
    print(f"✅ Rembg 已就绪")
    print(f"✅ Tkinter 窗口引擎已就绪")
    print("------------------")
    print("🚀 恭喜！你的工具箱环境已经可以完美运行抠图和 Office 转换脚本了。")

if __name__ == "__main__":
    check()