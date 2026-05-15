import whisper
import os
import tkinter as tk
from tkinter import filedialog, messagebox

def whisper_transcribe():
    # 1. 初始化 tkinter 并隐藏主窗口
    root = tk.Tk()
    root.withdraw()

    # 2. 弹出文件选择对话框 (选择音频文件)
    file_path = filedialog.askopenfilename(
        title="选择要识别的音频文件",
        filetypes=[("Audio files", "*.mp3 *.wav *.m4a *.flac"), ("All files", "*.*")]
    )

    if not file_path:
        return

    # 3. 自动计算保存路径 (同源路径，后缀为 .txt)
    dir_name = os.path.dirname(file_path)
    pure_name = os.path.splitext(os.path.basename(file_path))[0]
    output_path = os.path.join(dir_name, f"{pure_name}_transcription.txt")

    try:
        # 弹出“加载中”提示 (避免用户以为死机)
        messagebox.showinfo("提示", "正在加载 AI 模型，首次运行需下载 (约 1.5GB)。请耐心等待终端显示进度...")
        
        print(f"正在加载 Whisper 模型 ('small' 版本，平衡速度与精度)...")
        # 4. 加载模型 (你可以根据电脑性能改为 'tiny', 'base', 'medium', 'large')
        model = whisper.load_model("small")
        
        print(f"正在识别: {file_path} ... (这可能需要几分钟，取决于音频长度)")
        
        # 5. 执行识别 (自动检测语言，也可指定 language='Chinese')
        result = model.transcribe(file_path, fp16=False) # fp16=False 解决部分 Mac 的兼容性问题
        
        # 6. 保存结果
        transcription_text = result["text"]
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(transcription_text)
            
        # 7. 成功提示
        print(f"成功保存至: {output_path}")
        messagebox.showinfo("成功", f"识别完成！\n文本已保存为:\n{output_path}")
        
        # Mac 特色功能：自动用文本编辑打开结果
        os.system(f"open '{output_path}'")
        
    except Exception as e:
        messagebox.showerror("错误", f"识别失败：\n{e}")

if __name__ == "__main__":
    whisper_transcribe()