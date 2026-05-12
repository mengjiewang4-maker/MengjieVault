import os
import re
import pdfplumber
import pandas as pd
import requests
import tkinter as tk
from tkinter import filedialog, messagebox
import warnings
from openpyxl.styles import Alignment # 新增导入，用于稳定设置换行

warnings.filterwarnings("ignore")

def clean_markdown(text):
    text = text.replace("*", "").replace("#", "").replace("_", "")
    text = re.sub(r'\n\s*\n', '\n', text)
    return text.strip()

def ask_qwen_deep_reading(text):
    url = "http://localhost:11434/api/generate"
    prompt = f"你是一个科研专家。请深度阅读以下内容并总结。要求：中文回答，分点列出研究目标、方法、结论和创新点。不要带Markdown符号。内容：{text[:1800]}"
    try:
        response = requests.post(url, json={"model": "qwen2.5:7b", "prompt": prompt, "stream": False}, timeout=60)
        return response.json()['response'].strip()
    except:
        return "解析超时"

def start_mission():
    root = tk.Tk()
    root.withdraw()
    target_dir = filedialog.askdirectory(title="选择论文文件夹")
    if not target_dir: return

    files = [f for f in os.listdir(target_dir) if f.lower().endswith('.pdf')]
    all_results = []

    for file in files:
        path = os.path.join(target_dir, file)
        try:
            with pdfplumber.open(path) as pdf:
                content = "".join([p.extract_text() or "" for p in pdf.pages[:3]])
            print(f"📖 正在解析: {file[:30]}...")
            raw_analysis = ask_qwen_deep_reading(content)
            all_results.append({"文件名": file, "AI 深度报告": clean_markdown(raw_analysis)})
        except Exception as e:
            print(f"❌ 错误: {file} - {e}")

    if all_results:
        df = pd.DataFrame(all_results)
        output_file = os.path.join(target_dir, "00_AI_论文深度总结.xlsx")
        
        # --- 修复后的保存逻辑 ---
        writer = pd.ExcelWriter(output_file, engine='openpyxl')
        df.to_excel(writer, index=False, sheet_name='Summary')
        
        workbook = writer.book
        worksheet = writer.sheets['Summary']
        
        # 设置列宽
        worksheet.column_dimensions['A'].width = 30
        worksheet.column_dimensions['B'].width = 80
        
        # --- 核心修复：使用标准的 openpyxl 方式设置自动换行 ---
        for row in worksheet.iter_rows(min_row=2, max_row=len(all_results)+1, min_col=2, max_col=2):
            for cell in row:
                cell.alignment = Alignment(wrap_text=True, vertical='top')
        
        writer.close()
        print(f"✅ 成功！文件已生成：{output_file}")
        os.system(f"open '{output_file}'")
        messagebox.showinfo("成功", "精读完成！已自动换行处理。")

if __name__ == "__main__":
    start_mission()