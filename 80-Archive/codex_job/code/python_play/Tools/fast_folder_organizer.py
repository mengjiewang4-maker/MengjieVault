import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
import pdfplumber
from docx import Document
from sklearn.feature_extraction.text import TfidfVectorizer
import warnings

# 忽略 PDF 字体小报错
warnings.filterwarnings("ignore")

def get_fast_keywords(text):
    if len(text.strip()) < 50: return "Others"
    try:
        vectorizer = TfidfVectorizer(stop_words='english', max_features=10)
        tfidf_matrix = vectorizer.fit_transform([text])
        feature_names = vectorizer.get_feature_names_out()
        scores = tfidf_matrix.toarray()[0]
        top_indices = scores.argsort()[-2:][::-1]
        # 提取关键词并限制长度
        keywords = [feature_names[i].capitalize()[:15] for i in top_indices]
        return "_".join(keywords)
    except:
        return "Unclassified"

def extract_text(filepath):
    text = ""
    try:
        if filepath.endswith('.pdf'):
            with pdfplumber.open(filepath) as pdf:
                for page in pdf.pages[:2]:
                    text += page.extract_text() or ""
        elif filepath.endswith('.docx'):
            doc = Document(filepath)
            text = " ".join([p.text for p in doc.paragraphs[:20]])
    except: pass
    return text

def start_ultimate_clean():
    root = tk.Tk()
    root.withdraw()
    target_dir = filedialog.askdirectory(title="选择要深度清理的总文件夹")
    if not target_dir: return

    # 定义结果总目录（放在所选目录下）
    result_base = os.path.join(target_dir, "00_AI_Organized_Results")
    
    all_files = []
    # 1. 深度扫描所有文件
    for root_path, dirs, files in os.walk(target_dir):
        # 跳过我们自己创建的结果目录，防止套娃
        if "00_AI_Organized_Results" in root_path: continue
        
        for file in files:
            if file.lower().endswith(('.pdf', '.docx')) and not file.startswith('.'):
                all_files.append(os.path.join(root_path, file))

    if not all_files:
        messagebox.showinfo("提示", "没发现需要整理的文件。")
        return

    print(f"🕵️ 深度扫描完成，发现 {len(all_files)} 个文件，开始搬家...")

    # 2. 移动文件并分类
    for path in all_files:
        filename = os.path.basename(path)
        content = extract_text(path)
        category = get_fast_keywords(content)
        
        dest_folder = os.path.join(result_base, category)
        if not os.path.exists(dest_folder): os.makedirs(dest_folder)
        
        try:
            shutil.move(path, os.path.join(dest_folder, filename))
            print(f"🚚 已搬家: {filename} -> {category}")
        except Exception as e:
            print(f"❌ 移动失败 {filename}: {e}")

    # 3. 递归删除空文件夹（这是最爽的一步）
    print("🧹 正在清理空的子文件夹...")
    # topdown=False 表示从最深处往回删，这样才能删掉嵌套的空文件夹
    for root_path, dirs, files in os.walk(target_dir, topdown=False):
        if "00_AI_Organized_Results" in root_path: continue
        
        # 如果这个文件夹里既没文件也没子文件夹，就删了它
        if not os.listdir(root_path):
            os.rmdir(root_path)
            print(f"🗑️ 已删除空文件夹: {os.path.basename(root_path)}")

    messagebox.showinfo("大功告成", f"清理完毕！所有文件已归类至 '00_AI_Organized_Results'。")
    os.system(f"open '{result_base}'")

if __name__ == "__main__":
    start_ultimate_clean()