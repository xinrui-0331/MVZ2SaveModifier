import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import os
import webbrowser

# 存档选择窗口
class SaveFileSelector(tk.Toplevel):
    def __init__(self, parent, save_dir, on_select):
        super().__init__(parent)
        self.parent = parent
        self.save_dir = save_dir
        self.on_select = on_select
        
        # 窗口设置
        self.title("选择存档")
        self.geometry("600x400")
        self.transient(parent)  # 设置为父窗口的临时窗口
        self.grab_set()  # 设置为模态窗口
        
        # 创建组件
        self.create_widgets()
        self.refresh_list()
        
    def create_widgets(self):
        """创建界面组件"""
        # 文件列表
        self.tree = ttk.Treeview(
            self,
            columns=("name", "size", "modified"),
            show="headings",
            selectmode="browse"
        )
        self.tree.heading("name", text="存档名称")
        self.tree.heading("size", text="大小")
        self.tree.heading("modified", text="修改时间")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 操作按钮
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(
            btn_frame,
            text="取消",
            command=self.destroy
        ).pack(side=tk.RIGHT, padx=3)
        
        ttk.Button(
            btn_frame,
            text="选择",
            command=self.confirm_selection
        ).pack(side=tk.RIGHT, padx=3)
        
        ttk.Button(
            btn_frame,
            text="刷新",
            command=self.refresh_list
        ).pack(side=tk.LEFT)
        
    def refresh_list(self):
        """刷新文件列表"""
        self.tree.delete(*self.tree.get_children())
        for f in os.listdir(self.save_dir):
            if f.endswith((".lvl")):
                path = os.path.join(self.save_dir, f)
                stat = os.stat(path)
                self.tree.insert("", "end",
                    values=(
                        f,
                        f"{stat.st_size/1024:.1f} KB",
                        self.format_time(stat.st_mtime)
                    ))
                    
    def format_time(self, timestamp):
        """格式化时间戳"""
        from datetime import datetime
        return datetime.fromtimestamp(timestamp).strftime("%m-%d %H:%M")
        
    def confirm_selection(self):
        """确认选择"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("提示", "你还没有选择存档")
            return
            
        selected_file = os.path.join(
            self.save_dir,
            self.tree.item(selected[0])["values"][0]
        )
            
        # 执行回调并关闭窗口
        self.on_select(selected_file)
        self.destroy()

# 用户选择窗口
class UserSelector(tk.Toplevel):
    def __init__(self, parent, metas, on_select):
        super().__init__(parent)
        self.parent = parent
        self.metas = metas
        self.on_select = on_select

        # 窗口设置
        self.title("选择用户")
        self.geometry("600x400")
        self.transient(parent)  # 设置为父窗口的临时窗口
        self.grab_set()  # 设置为模态窗口
        
        # 用户列表
        self.tree = ttk.Treeview(
            self,
            columns=("id", "name"),
            show="headings",
            selectmode="browse"
        )
        self.tree.heading("id", text="用户存档路径id")
        self.tree.heading("name", text="用户昵称")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        for user in self.metas:
            if user == None:
                continue
            self.tree.insert("", "end", values=(metas.index(user),user['username']))

        # 操作按钮
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(btn_frame, text="取消", command=self.destroy).pack(side=tk.RIGHT, padx=3)
        ttk.Button(btn_frame, text="选择", command=self.confirm_selection).pack(side=tk.RIGHT, padx=3)
                
    def confirm_selection(self):
        """确认选择"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("提示", "你还没有选择用户")
            return
            
        selected_user = self.tree.item(selected[0])["values"][0]
            
        # 执行回调并关闭窗口
        self.on_select(selected_user)
        self.destroy()

class AboutWindow:
    def __init__(self, parent):
        # 创建顶级窗口
        self.window = tk.Toplevel(parent)
        self.window.title("关于")
        self.window.geometry("400x320")
        self.window.resizable(False, False)  # 禁止调整大小
        
        # 设置窗口图标（可选）
        # self.window.iconbitmap("icon.ico")
        
        # 主容器
        container = ttk.Frame(self.window)
        container.pack(padx=20, pady=20, fill="both", expand=True)
        
        # 文字信息
        text_content = """
声明：使用该软件造成的文件损坏，作者本人一概不负责
暂时不支持修改传送带中的蓝图
该修改器由QoZnoS制作
部分代码由Deepseek辅助生成
icon来自MVZ2"""
        
        lbl_info = ttk.Label(
            container,
            text=text_content,
            justify="center",
            wraplength=350
        )
        lbl_info.pack(pady=10)
        
        # 链接按钮容器
        link_frame = ttk.Frame(container)
        link_frame.pack(pady=15)
        
        # 创建链接按钮
        links = [
            ("游戏作者主页", "https://space.bilibili.com/348514"),
            ("修改器作者主页", "https://space.bilibili.com/404359179"),
            ("修改器源码", "https://github.com/QoZnoS/MVZ2SaveModifier")
        ]
        
        for text, url in links:
            btn = ttk.Button(
                link_frame,
                text=text,
                width=12,
                command=lambda u=url: self.open_link(u)  # 使用 lambda 绑定参数
            )
            btn.pack(side="top", pady=5)
        
    def open_link(self, url):
        """打开外部链接"""
        webbrowser.open_new(url)