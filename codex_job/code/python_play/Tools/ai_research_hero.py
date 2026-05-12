import os
import shutil
import requests
import pdfplumber
import tkinter as tk
from tkinter import filedialog, messagebox
import warnings

# 1. 屏蔽 PDF 字体解析的冗余警告
warnings.filterwarnings("ignore")

def ask_qwen_smart(filename, doc_title, content_summary):
    """
    调用本地 Ollama (Qwen 2.5:7b)，采用优先级逻辑进行分类
    """
    url = "http://localhost:11434/api/generate"
    
    # 提示词：强制 AI 区分文件类型
    prompt = f"""
    你是一个专业的文件档案管理员。请根据以下信息，为文件生成一个规范的中文文件名并分类。

    【优先级规则】
    1. 观察『文档首行』和『原始文件名』。如果包含“成绩单”、“证明”、“通知”、“申请表”、“简历”等词汇，务必分类为“个人资料”或“行政办公”。
    2. 如果首行是学术题目（如：Quantum...），则识别为“科研论文”。
    
    【输入信息】
    - 原始文件名：{filename}
    - 文档首行/标题：{doc_title}
    - 正文摘要：{content_summary[:800]}
    
    【输出要求】
    - 格式：[年份或日期]_[分类标签]_[具体描述]
    - 示例：2024_个人资料_物理成绩单、2023_量子力学_能带结构研究
    - 限制：只返回结果，不要任何解释，不要包含特殊字符。
    """
    
    try:
        response = requests.post(url, json={
            "model": "qwen2.5:7b",
            "prompt": prompt,
            "stream": False
        }, timeout=20)
        return response.json()['response'].strip().replace("。", "").replace("/", "_").replace('"', '')
    except Exception as e:
        print(f"⚠️ AI 响应异常: {e}")
        return f"未分类_{filename[:10]}"

def start_smart_library():
    # 初始化 GUI
    root = tk.Tk()
    root.withdraw()
    
    target_dir = filedialog.askdirectory(title="选择要深度整理的文件夹 (包含子文件夹)")
    if not target_dir: return

    # 建立结果总目录
    result_base = os.path.join(target_dir, "00_Smart_Library_Results")
    
    all_files = []
    for root_path, _, files in os.walk(target_dir):
        if "00_Smart_Library_Results" in root_path: continue
        for file in files:
            if file.lower().endswith('.pdf'):
                all_files.append(os.path.join(root_path, file))

    if not all_files:
        messagebox.showinfo("提示", "未找到 PDF 文件。")
        return

    print(f"🧬 M4 引擎启动：正在深度解析 {len(all_files)} 个文档...")

    for path in all_files:
        original_name = os.path.basename(path)
        try:
            with pdfplumber.open(path) as pdf:
                # --- 提取逻辑升级 ---
                first_page_text = pdf.pages[0].extract_text() or ""
                lines = [l.strip() for l in first_page_text.split('\n') if l.strip()]
                
                # 抓取第一行作为潜在标题
                doc_title = lines[0] if lines else "无法提取标题"
                
                # 抓取前两页作为内容背景
                content_summary = ""
                for i in range(min(2, len(pdf.pages))):
                    content_summary += pdf.pages[i].extract_text() or ""

            # --- 调用 AI ---
            print(f"🔍 正在阅读: {original_name[:30]}...")
            smart_name = ask_qwen_smart(original_name, doc_title, content_summary)
            
            # --- 自动归类逻辑 ---
            # 假设 smart_name 为 "2024_个人资料_成绩单"，提取 "个人资料" 作为文件夹名
            parts = smart_name.split("_")
            category = parts[1] if len(parts) > 1 else "综合未分类"
            
            dest_folder = os.path.join(result_base, category)
            if not os.path.exists(dest_folder): os.makedirs(dest_folder)
            
            # 移动并重命名
            new_full_path = os.path.join(dest_folder, f"{smart_name}.pdf")
            shutil.move(path, new_full_path)
            print(f"✨ 归档成功: {smart_name}")
            
        except Exception as e:
            print(f"❌ 处理失败 {original_name}: {e}")

    # 清理空文件夹
    print("🧹 正在清理多余空目录...")
    for root_path, dirs, files in os.walk(target_dir, topdown=False):
        if "00_Smart_Library_Results" in root_path: continue
        if not os.listdir(root_path):
            try:
                os.rmdir(root_path)
            except: pass

    messagebox.showinfo("任务完成", "AI 已经重新梳理了您的文库！")
    os.system(f"open '{result_base}'")

if __name__ == "__main__":
    start_smart_library()