import os
import csv
import tkinter as tk
from tkinter import messagebox

class VisualFixTimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("M4 Research Commander Pro")
        self.root.geometry("520x780")
        self.root.configure(bg="#E0E4E8") 
        
        # 初始示例任务
        self.tasks = [
            ["文献精读", 1500, 1500, False],
            ["COMSOL 仿真", 3600, 3600, False]
        ]
        
        self.setup_ui()
        self.update_tick()

    def setup_ui(self):
        # --- 1. 顶部标题栏 (黑底绿字，绝对清晰) ---
        self.header = tk.Frame(self.root, bg="#1A1C1E", pady=30)
        self.header.pack(fill="x")
        
        self.main_title = tk.Label(
            self.header, text="MULTI-FOCUS DASHBOARD", 
            font=("Helvetica", 22, "bold"), fg="#2ECC71", bg="#1A1C1E"
        )
        self.main_title.pack()

        # --- 2. 输入区域 ---
        self.input_area = tk.Frame(self.root, bg="#E0E4E8", pady=20)
        self.input_area.pack()

        # 任务名
        name_frame = tk.Frame(self.input_area, bg="#E0E4E8")
        name_frame.grid(row=0, column=0, padx=8)
        tk.Label(name_frame, text="任务名称", font=("PingFang SC", 10, "bold"), fg="#2C3E50", bg="#E0E4E8").pack(anchor="w")
        self.name_entry = tk.Entry(name_frame, font=("PingFang SC", 14), width=18, 
                                   bg="#FFFFFF", fg="#000000", insertbackground="#000000",
                                   relief="solid", bd=1)
        self.name_entry.insert(0, "新科研任务")
        self.name_entry.pack(ipady=8)

        # 时间
        time_frame = tk.Frame(self.input_area, bg="#E0E4E8")
        time_frame.grid(row=0, column=1, padx=8)
        tk.Label(time_frame, text="时长(min)", font=("PingFang SC", 10, "bold"), fg="#2C3E50", bg="#E0E4E8").pack(anchor="w")
        self.time_entry = tk.Entry(time_frame, font=("PingFang SC", 14), width=6, 
                                   bg="#FFFFFF", fg="#000000", insertbackground="#000000",
                                   relief="solid", bd=1, justify="center")
        self.time_entry.insert(0, "25")
        self.time_entry.pack(ipady=8)

        # 添加按钮 (深蓝色，白字)
        self.add_btn = tk.Button(
            self.input_area, text="＋ 添加", font=("PingFang SC", 11, "bold"),
            bg="#2980B9", fg="#FFFFFF", activebackground="#1F618D", 
            activeforeground="#FFFFFF", highlightbackground="#E0E4E8",
            relief="raised", width=8, height=2, command=self.add_task_action
        )
        self.add_btn.grid(row=0, column=2, padx=10, sticky="s")

        # --- 3. 任务列表 ---
        self.list_container = tk.Frame(self.root, bg="#FFFFFF")
        self.list_container.pack(fill="both", expand=True, padx=25, pady=10)
        
        self.canvas = tk.Canvas(self.list_container, bg="#FFFFFF", highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.list_container, orient="vertical", command=self.canvas.yview)
        self.scroll_frame = tk.Frame(self.canvas, bg="#FFFFFF")

        self.scroll_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def update_tick(self):
        """核心计时器循环"""
        for task in self.tasks:
            if task[3] and task[2] > 0: # 如果正在运行且有剩余时间
                task[2] -= 1
            elif task[3] and task[2] <= 0:
                task[3] = False
                self.play_alarm(task[0])
        self.render_list()
        self.root.after(1000, self.update_tick)

    def play_alarm(self, name):
        os.system('afplay /System/Library/Sounds/Glass.aiff &')
        messagebox.showinfo("Done", f"【{name}】时间到！")

    def toggle_task(self, idx):
        self.tasks[idx][3] = not self.tasks[idx][3]
        self.render_list()

    def reset_task(self, idx):
        self.tasks[idx][2] = self.tasks[idx][1]
        self.tasks[idx][3] = False
        self.render_list()

    def delete_task(self, idx):
        del self.tasks[idx]
        self.render_list()

    def render_list(self):
        """渲染任务列表"""
        for w in self.scroll_frame.winfo_children():
            w.destroy()
        
        for i, (name, total_sec, remain_sec, is_running) in enumerate(self.tasks):
            bg_color = "#D5F5E3" if is_running else "#FFFFFF"
            f = tk.Frame(self.scroll_frame, bg=bg_color, pady=12, padx=15)
            f.pack(fill="x", pady=2)
            
            # 1. 播放/暂停按钮 (显式指定 fg 颜色，防止变白)
            btn_txt = "⏸" if is_running else "▶"
            btn_bg = "#E74C3C" if is_running else "#27AE60"
            tk.Button(f, text=btn_txt, bg=btn_bg, fg="#FFFFFF", 
                      font=("Arial", 12, "bold"), width=5,
                      activebackground=btn_bg, activeforeground="#FFFFFF",
                      highlightbackground=bg_color, relief="flat",
                      command=lambda idx=i: self.toggle_task(idx)).pack(side="left")
            
            # 2. 任务文字与倒计时
            m, s = divmod(remain_sec, 60)
            tk.Label(f, text=f"{name}", font=("PingFang SC", 12, "bold"), 
                     bg=bg_color, fg="#2C3E50").pack(side="left", padx=(15, 5))
            # 修正了之前的变量名错误 (s 替代了 secs)
            tk.Label(f, text=f"[{m:02d}:{s:02d}]", font=("Courier", 13, "bold"), 
                     bg=bg_color, fg="#16A085").pack(side="left")
            
            # 3. 功能按钮 (重置与删除)
            tk.Button(f, text="↺", bg="#95A5A6", fg="#FFFFFF", width=3,
                      highlightbackground=bg_color, relief="flat",
                      command=lambda idx=i: self.reset_task(idx)).pack(side="right", padx=2)
            
            tk.Button(f, text="✕", fg="#E74C3C", bg=bg_color, font=("Arial", 14, "bold"),
                      highlightbackground=bg_color, relief="flat",
                      command=lambda idx=i: self.delete_task(idx)).pack(side="right", padx=8)
            
            tk.Frame(self.scroll_frame, height=1, bg="#DCDDE1").pack(fill="x")

    def add_task_action(self):
        name = self.name_entry.get().strip()
        mins = self.time_entry.get().strip()
        if name and mins.isdigit():
            sec = int(mins) * 60
            self.tasks.append([name, sec, sec, False])
            self.name_entry.delete(0, tk.END)
            self.render_list()

if __name__ == "__main__":
    root = tk.Tk()
    root.attributes('-topmost', True)
    app = VisualFixTimerApp(root)
    root.mainloop()