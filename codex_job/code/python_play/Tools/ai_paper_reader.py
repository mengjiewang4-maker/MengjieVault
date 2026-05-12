import os
import pdfplumber
import pandas as pd
import requests
import tkinter as tk
from tkinter import filedialog, messagebox

def ask_qwen_deep_reading(text):
    url = "http://localhost:11434/api/generate"
    # 恢复刚才那个“有灵魂”的提示词
    prompt = f"""
    你是一个资深的物理学博士后，请深度阅读以下论文片段并总结。
    要求：用中文回答，专业且深刻，分点列出：
    1. 研究的核心目标是什么？
    2. 关键的实验/计算方法（包括软件、参数、设备）。
    3. 最重要的物理结论或数据发现。
    4. 这篇文章最大的创新点在哪里？

    内容：
    {text[:1800]}
    """
    try:
        response = requests.post(url, json={
            "model": "qwen2.5:7b",
            "prompt": prompt,
            "stream": False
        }, timeout=45)
        return response.json()['response'].strip()
    except:
        return "AI 思考太久，请求超时了。"

def start_mission():
    root = tk.Tk()
    root.withdraw()
    target_dir = filedialog.askdirectory(title="选择论文文件夹")
    if not target_dir: return

    files = [f for f in os.listdir(target_dir) if f.lower().endswith('.pdf')]
    all_results = []

    print(f"🧬 M4 恢复“深度模式”，正在精读 {len(files)} 篇论文...")

    for file in files:
        path = os.path.join(target_dir, file)
        try:
            with pdfplumber.open(path) as pdf:
                content = "".join([p.extract_text() or "" for p in pdf.pages[:3]])
            
            print(f"📖 正在深度解析: {file}")
            # 获取那个“话多且专业”的回答
            deep_analysis = ask_qwen_deep_reading(content)
            
            all_results.append({
                "文件名": file,
                "AI 深度报告 (双击单元格查看详情)": deep_analysis
            })
        except Exception as e:
            print(f"❌ 错误: {file} - {e}")

    if all_results:
        df = pd.DataFrame(all_results)
        output_file = os.path.join(target_dir, "00_AI_论文深度总结报表.xlsx")
        
        # 优化 Excel 显示：自动换行
        writer = pd.ExcelWriter(output_file, engine='openpyxl')
        df.to_excel(writer, index=False, sheet_name='Sheet1')
        
        # 让表格列宽一点，方便阅读
        worksheet = writer.sheets['Sheet1']
        worksheet.column_dimensions['A'].width = 30
        worksheet.column_dimensions['B'].width = 80
        writer.close()
        
        os.system(f"open '{output_file}'")
        messagebox.showinfo("完成", "深度报告已生成！")

if __name__ == "__main__":
    start_mission()