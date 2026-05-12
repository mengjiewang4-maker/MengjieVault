from pathlib import Path
import shutil
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox

import pdfplumber
from docx import Document
from keybert import KeyBERT


SUPPORTED_EXTENSIONS = (".pdf", ".docx")
DEFAULT_CATEGORY = "Others_Unsorted"
MAX_PDF_PAGES = 3
MAX_DOCX_PARAGRAPHS = 50
MIN_TEXT_LENGTH = 100
MAX_CATEGORY_PARTS = 2


def extract_text(filepath: Path) -> str:
    """读取文件的有限内容，避免一次性加载过多文本。"""
    if filepath.suffix.lower() == ".pdf":
        with pdfplumber.open(filepath) as pdf:
            return "".join(
                page.extract_text() or ""
                for page in pdf.pages[:MAX_PDF_PAGES]
            )

    if filepath.suffix.lower() == ".docx":
        doc = Document(filepath)
        return " ".join(
            paragraph.text.strip()
            for paragraph in doc.paragraphs[:MAX_DOCX_PARAGRAPHS]
            if paragraph.text.strip()
        )

    return ""


def sanitize_category_name(name: str) -> str:
    """清洗分类名，避免创建非法或难读的目录名。"""
    cleaned = "".join(
        char if char.isalnum() or char == "_" else "_"
        for char in name.strip()
    )
    collapsed = "_".join(part for part in cleaned.split("_") if part)
    return collapsed[:80] or DEFAULT_CATEGORY


def build_unique_destination(dest_folder: Path, filename: str) -> Path:
    """如目标文件已存在，自动追加序号避免覆盖。"""
    destination = dest_folder / filename
    if not destination.exists():
        return destination

    stem = destination.stem
    suffix = destination.suffix
    counter = 1
    while True:
        candidate = dest_folder / f"{stem}_{counter}{suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def get_ai_category(filepath: Path, model: KeyBERT) -> str:
    """读取文件内容并提取核心关键词作为分类名。"""
    try:
        text = extract_text(filepath)
        if len(text.strip()) >= MIN_TEXT_LENGTH:
            keywords = model.extract_keywords(
                text,
                keyphrase_ngram_range=(1, 2),
                stop_words="english",
                top_n=MAX_CATEGORY_PARTS,
            )
            category = "_".join(
                keyword.title().replace(" ", "")
                for keyword, _score in keywords
                if keyword.strip()
            )
            return sanitize_category_name(category)
    except Exception as e:
        print(f"解析 {filepath.name} 出错: {e}")
    return DEFAULT_CATEGORY


def collect_supported_files(target_dir: Path) -> list[Path]:
    """收集当前目录下可处理的文档文件。"""
    return sorted(
        file_path
        for file_path in target_dir.iterdir()
        if file_path.is_file()
        and not file_path.name.startswith(".")
        and file_path.suffix.lower() in SUPPORTED_EXTENSIONS
    )


def open_folder(target_dir: Path) -> None:
    """在 macOS 上打开结果目录。"""
    try:
        subprocess.run(["open", str(target_dir)], check=False)
    except Exception as e:
        print(f"打开目录失败: {e}")


def start_ai_organizing():
    root = tk.Tk()
    root.withdraw()
    try:
        selected_dir = filedialog.askdirectory(title="选择要 AI 自动整理的文件夹")
        if not selected_dir:
            return

        target_dir = Path(selected_dir)

        print("🤖 正在唤醒 AI 模型，请稍候...")
        kw_model = KeyBERT()

        files_to_process = collect_supported_files(target_dir)

        if not files_to_process:
            messagebox.showinfo("提示", "该文件夹下没有发现 PDF 或 Word 文件。")
            return

        print(f"📂 找到 {len(files_to_process)} 个文件，开始 AI 深度阅读...")

        processed_count = 0
        for path in files_to_process:
            category = get_ai_category(path, kw_model)
            dest_folder = target_dir / category
            dest_folder.mkdir(exist_ok=True)

            destination = build_unique_destination(dest_folder, path.name)
            shutil.move(str(path), str(destination))
            processed_count += 1
            print(f"✨ [{path.name}] -> 已分类至: {category}")

        messagebox.showinfo("成功", f"整理完成！共处理 {processed_count} 个文件。")
        open_folder(target_dir)

    except Exception as e:
        messagebox.showerror("错误", f"运行出错: {e}")
    finally:
        root.destroy()


if __name__ == "__main__":
    start_ai_organizing()
