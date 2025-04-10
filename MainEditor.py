import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import gzip,shutil,os,json,winreg,subprocess
import platform
import CustonJson,Selector,NameData

level_day = NameData.level_day
maps_id = NameData.maps_id
level_id = NameData.level_id
artifact_id = NameData.artifact_id
blueprint_id = NameData.blueprint_id
musics_id = NameData.musics_id
text_id = NameData.text_id

#region 全局函数
def get_save_path():
    '''根据系统返回userdata路径'''
    system = platform.system()
    if system == "Windows":
        return os.path.expandvars(r"%HOMEPATH%/AppData/LocalLow/Cuerzor/MinecraftVSZombies2/userdata")
    elif system == "Darwin":  # macOS
        return os.path.expanduser("~/Library/Application Support/Cuerzor/MinecraftVSZombies2/userdata")
    else:  # Linux
        return os.path.expanduser("~/.config/unity3d/Cuerzor/MinecraftVSZombies2/userdata")

def get_language():
    key_path = r"Software\\Cuerzor\\MinecraftVSZombies2"

    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,key_path,0,winreg.KEY_READ)
    i = 0
    while True:
        try:
            name, value, _ = winreg.EnumValue(key, i)
            if name.startswith("Language"):
                value_data=value
                break
            i+=1
        except OSError:
            break
    winreg.CloseKey(key)

    if value_data == b'en-US\x00':
        set_language(False)
    elif value_data == b'zh-Hans\x00':
        set_language(True)
    else:
        choose_language()

def set_language(is_zh):
    global maps_name,artifact_name,blueprint_name,musics_name,text_name,level_name
    if is_zh:
        maps_name = NameData.maps_name_zh
        level_name = NameData.level_name_zh
        artifact_name = NameData.artifact_name_zh
        blueprint_name = NameData.blueprint_name_zh
        musics_name = NameData.musics_name_zh
        text_name = NameData.text_name_zh
    else:
        maps_name = NameData.maps_name_en
        level_name = NameData.level_name_en
        artifact_name = NameData.artifact_name_en
        blueprint_name = NameData.blueprint_name_en
        musics_name = NameData.musics_name_en
        text_name = NameData.text_name_en

def choose_language():
    Selector.LanguageSelector(on_select=set_language)

def get_text(id):
    """获取文本"""
    for text in text_id:
        if id == text:
            return text_name[text_id.index(id)]

def decompress(path):
    '''根据给定路径解压文件，返回解压后的文件'''
    try:
        with gzip.open(path, "rb") as file:
            return file.read()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to decompress: {str(e)}")

def compress(path,file):
    '''压缩文件到给定路径'''
    with gzip.open(path, "wb") as out:
        out.write(file)
#endregion

class ArchiveEditor:
    def __init__(self, root):
        self.root = root
        self.root.title(get_text("title"))

        self.current_file = ""  # 当前操作的文件路径
        self.current_data = None # 当前操作的文件JSON数据
        self.page = 1 # 界面，0为数值编辑器，1为蓝图/制品编辑器


        self.data_wave = tk.StringVar(value="0")
        self.data_flag = tk.StringVar(value="0")
        self.data_energy = tk.StringVar(value="50")
        self.data_maxEnergy = tk.StringVar(value="9990.0")
        self.data_starshardCount = tk.StringVar(value="2")
        self.data_starshardSlotCount = tk.StringVar(value="5")
        self.data_conveyorSlotCount = tk.StringVar(value="10")


        self.get_usersdata() # 自动读取存档
        self.setup_ui() # 创建UI
        self.switch_frame()
 
    # region 创建UI
    def setup_ui(self):
        self.setup_user_frame()
        self.setup_file_frame()
        self.frame_tree = tk.Frame(self.root)
        self.frame_numeric = tk.Frame(self.root)
        self.setup_tree_artifact_frame()
        self.setup_tree_blueprint_frame()
        self.setup_numeric_group_frame()

        # JSON 编辑区
        # self.text_editor = scrolledtext.ScrolledText(self.root, width=60, height=20)
        # self.text_editor.pack(pady=10, padx=10)

        # 状态栏
        self.status = tk.StringVar()
        self.status.set(get_text("status_ready"))
        tk.Label(self.root, textvariable=self.status, bd=1, relief=tk.SUNKEN, anchor=tk.W).pack(fill=tk.X,side=tk.BOTTOM)

        # 保存
        self.output_btn=tk.Button(self.root, text=get_text("btn_save"),command=self.output_file,state="disabled")
        self.output_btn.pack(fill=tk.X,side=tk.BOTTOM)
    # 创建制品/蓝图修改器UI
    def setup_tree_frame(self):
        self.frame_tree.pack(padx=10, fill=tk.BOTH, expand=True)
    # 创建数值修改器UI
    def setup_numeric_frame(self):
        self.frame_numeric.pack(padx=10, fill=tk.BOTH, expand=True)

    def setup_user_frame(self):
        """选择用户，单文件解压缩"""
        self.frame_user = tk.Frame(self.root)
        self.frame_user.pack(pady=10)
        self.username_label = tk.Label(self.frame_user, text=get_text("label_user") + self.username)
        self.username_label.pack(side=tk.LEFT)
        tk.Button(self.frame_user, text=get_text("btn_switch"), command=self.open_user_selector).pack(side=tk.LEFT, padx=5)
        tk.Button(self.frame_user, text=get_text("btn_unzip"), command=self.decompress).pack(side=tk.LEFT, padx=10)
        tk.Button(self.frame_user, text=get_text("btn_zip"), command=self.compress).pack(side=tk.LEFT, padx=5)

    def setup_file_frame(self):
        """存档选择，切换界面"""
        self.frame_file = tk.Frame(self.root)
        self.frame_file.pack(pady=10)
        self.filename_label = tk.Label(self.frame_file, text=get_text("label_lvl_null"))
        self.filename_label.pack(side=tk.LEFT)
        tk.Button(self.frame_file, text=get_text("btn_lvl"), command=self.open_save_selector).pack(side=tk.LEFT, padx=10)
        tk.Button(self.frame_file, text=get_text("btn_open_explorer"), command=self.open_save_explorer).pack(side=tk.LEFT, padx=10)
        tk.Button(self.frame_file, text=get_text("btn_page"), command=self.switch_frame).pack(side=tk.LEFT, padx=10)
        # 混乱选项
        
    def setup_tree_artifact_frame(self):
        """制品"""
        frame_artifact = tk.Frame(self.frame_tree)
        frame_artifact.pack(side=tk.LEFT, padx=10, expand=True)
        # 制品列表
        self.artifact_tree = ttk.Treeview(frame_artifact,columns=("id","name"),show="headings",selectmode="browse")
        self.artifact_tree.heading("id",text="ID")
        self.artifact_tree.column("id",width=28)
        self.artifact_tree.heading("name",text=get_text("tree_artifact"))
        self.artifact_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        # 相关控件
        artifact_control_frame = tk.Frame(frame_artifact)
        artifact_control_frame.pack(side=tk.RIGHT, padx=10)
        self.artifact_box = ttk.Combobox(artifact_control_frame, values=artifact_name, state="disabled", width=18)
        self.artifact_box.pack(pady=(0, 12))
        tk.Button(artifact_control_frame, text=get_text("btn_add"), width=8, command=self.add_artifact).pack(fill=tk.X, pady=12)
        tk.Button(artifact_control_frame, text=get_text("btn_delete"), width=8, command=self.remove_artifact).pack(fill=tk.X, pady=12)

    def setup_tree_blueprint_frame(self):
        """蓝图"""
        frame_blueprint = tk.Frame(self.frame_tree)
        frame_blueprint.pack(side=tk.LEFT, padx=10, expand=True)
        # 蓝图列表
        self.blueprint_tree = ttk.Treeview(frame_blueprint,columns=("id","name"),show="headings",selectmode="browse")
        self.blueprint_tree.heading("id",text="ID")
        self.blueprint_tree.column("id",width=28)
        self.blueprint_tree.heading("name",text=get_text("tree_blueprint"))
        self.blueprint_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        # 相关控件
        blueprint_control_frame = tk.Frame(frame_blueprint)
        blueprint_control_frame.pack(side=tk.RIGHT, padx=10)
        self.blueprint_box = ttk.Combobox(blueprint_control_frame, values=blueprint_name, state="disabled", width=20)
        self.blueprint_box.pack(pady=(0, 12))
        # tk.Button(blueprint_control_frame, text="添加", width=8).pack(fill=tk.X, pady=12)
        tk.Button(blueprint_control_frame, text=get_text("btn_modify"), width=8, command=self.modify_blueprint).pack(fill=tk.X, pady=12)
        # tk.Button(blueprint_control_frame, text="删除", width=8).pack(fill=tk.X, pady=12)

    def setup_numeric_group_frame(self):
        frame_group = tk.Frame(self.frame_numeric)
        frame_group.pack(side=tk.LEFT, padx=10, expand=True)
        tk.Label(frame_group, text=get_text("label_chapter")).grid(row=0, column=0, sticky="e", pady=12)
        self.numeric_stageDefinition_box = ttk.Combobox(frame_group,values=maps_name,state="disable",width=16)
        self.numeric_stageDefinition_box.grid(row=0, column=1, sticky="ew", pady=12)
        self.numeric_stageDefinition_box.set("")
        self.numeric_stageDefinition_box.bind("<<ComboboxSelected>>",self.mix_stageDefinitionID)
        tk.Label(frame_group, text=get_text("label_day")).grid(row=1, column=0, sticky="e", pady=12)
        self.numeric_stageDefinitionID_box = ttk.Combobox(frame_group,values=level_day,state="disable",width=16)
        self.numeric_stageDefinitionID_box.grid(row=1, column=1, sticky="ew", pady=12)
        self.numeric_stageDefinitionID_box.set("")
        self.numeric_stageDefinitionID_box.bind("<<ComboboxSelected>>",self.mix_stageDefinitionID)
        tk.Label(frame_group, text=get_text("label_flag")).grid(row=2, column=0, sticky="e", pady=12)
        self.numeric_flag_input = ttk.Entry(frame_group, state="disable", textvariable=self.data_flag, validate='key',validatecommand=(self.root.register(self.change_flag), '%d', '%i', '%P', '%s', '%v', '%V', '%W'))
        self.numeric_flag_input.grid(row=2, column=1, sticky="ew", pady=12)
        tk.Label(frame_group, text=get_text("label_wave")).grid(row=3, column=0, sticky="e", pady=12)
        self.numeric_wave_input = ttk.Entry(frame_group, state="disable", textvariable=self.data_wave, validate='key',validatecommand=(self.root.register(self.change_wave), '%d', '%i', '%P', '%s', '%v', '%V', '%W'))
        self.numeric_wave_input.grid(row=3, column=1, sticky="ew", pady=12)
        tk.Label(frame_group, text=get_text("label_energy")).grid(row=0, column=2, sticky="e", pady=12)
        self.numeric_energy_input = ttk.Entry(frame_group, state="disable", textvariable=self.data_energy, validate='key',validatecommand=(self.root.register(self.change_energy), '%d', '%i', '%P', '%s', '%v', '%V', '%W'))
        self.numeric_energy_input.grid(row=0, column=3, sticky="ew", pady=12)
        tk.Label(frame_group, text=get_text("label_maxEnergy")).grid(row=1, column=2, sticky="e", pady=12)
        self.numeric_maxEnergy_input = ttk.Entry(frame_group, state="disable", textvariable=self.data_maxEnergy, validate='key',validatecommand=(self.root.register(self.change_maxEnergy), '%d', '%i', '%P', '%s', '%v', '%V', '%W'))
        self.numeric_maxEnergy_input.grid(row=1, column=3, sticky="ew", pady=12)
        tk.Label(frame_group, text=get_text("label_starshard")).grid(row=2, column=2, sticky="e", pady=12)
        self.numeric_starshardCount_input = ttk.Entry(frame_group, state="disable", textvariable=self.data_starshardCount, validate='key',validatecommand=(self.root.register(self.change_starshardCount), '%d', '%i', '%P', '%s', '%v', '%V', '%W'))
        self.numeric_starshardCount_input.grid(row=2, column=3, sticky="ew", pady=12)
        tk.Label(frame_group, text=get_text("label_maxStarshard")).grid(row=3, column=2, sticky="e", pady=12)
        self.numeric_starshardSlotCount_input = ttk.Entry(frame_group, state="disable", textvariable=self.data_starshardSlotCount, validate='key',validatecommand=(self.root.register(self.change_starshardSlotCount), '%d', '%i', '%P', '%s', '%v', '%V', '%W'))
        self.numeric_starshardSlotCount_input.grid(row=3, column=3, sticky="ew", pady=12)
        tk.Label(frame_group, text=get_text("label_conveyor")).grid(row=0, column=4, sticky="e", pady=12)
        self.numeric_isConveyorMode_box = ttk.Combobox(frame_group,values=[get_text("True"),get_text("False")],state="disable",width=16)
        self.numeric_isConveyorMode_box.grid(row=0, column=5, sticky="ew", pady=12)
        self.numeric_isConveyorMode_box.set("")
        self.numeric_isConveyorMode_box.bind("<<ComboboxSelected>>",self.is_ConveyorMode)
        tk.Label(frame_group, text=get_text("label_conveyorslot")).grid(row=1, column=4, sticky="e", pady=12)
        self.numeric_conveyorSlotCount_input = ttk.Entry(frame_group, state="disable", textvariable=self.data_conveyorSlotCount, validate='key',validatecommand=(self.root.register(self.change_conveyorSlotCount), '%d', '%i', '%P', '%s', '%v', '%V', '%W'))
        self.numeric_conveyorSlotCount_input.grid(row=1, column=5, sticky="ew", pady=12)
        tk.Label(frame_group, text=get_text("label_bgm")).grid(row=2, column=4, sticky="e", pady=12)
        self.numeric_musicID_box = ttk.Combobox(frame_group,values=musics_name,state="disable",width=16)
        self.numeric_musicID_box.grid(row=2, column=5, sticky="ew", pady=12)
        self.numeric_musicID_box.set("")
        self.numeric_musicID_box.bind("<<ComboboxSelected>>",self.change_musicID)
        tk.Button(frame_group, text=get_text("btn_about"),command=self.open_about).grid(row=3,column=4,columnspan=2,ipadx=32)

    # endregion

    # region 响应回调
    # region 窗口
    # 处理文件窗口
    def open_save_selector(self):
        """打开存档选择窗口"""
        Selector.SaveFileSelector(
            parent=self.root,
            save_dir=get_save_path() + ("/user%d/mvz2/level"%(self.currentUserIndex)),
            on_select=self.handle_save_selected  # 关键：选择后的回调
        )
        
    def handle_save_selected(self, selected_path):
        """处理选择的存档"""
        try:
            self.current_file = selected_path
            self.current_data = json.loads(decompress(self.current_file).decode("utf-8"),cls=CustonJson.CustomDecoder)
            self.filename_label.config(text=get_text("label_lvl") + os.path.basename(self.current_file))
            self.refresh()
            # print(self.current_data)
            # print(json.dumps(self.current_data,cls=CustonJson.CustomEncoder))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file:\n{str(e)}")
    # 处理用户窗口
    def open_user_selector(self):
        """打开用户选择窗口"""
        Selector.UserSelector(
            parent=self.root,
            metas=self.users['metas'],
            on_select=self.handle_user_selected
        )

    def handle_user_selected(self, selected_user):
        """处理选择的用户"""
        self.currentUserIndex = selected_user
        self.username = self.users['metas'][self.currentUserIndex]['username']
        self.username_label.config(text=get_text("label_user") + self.username)
    # endregion
    # region tree_frame
    # 添加制品
    def add_artifact(self):
        if not self.artifact_box.get():
            return
        # 制品模板
        new_artifact = { 
            "definitionID":artifact_id[artifact_name.index(self.artifact_box.get())],
            "propertyDict": {
                "properties": {}
            },
            "auras": [
                {
                "updateTimer":{},
                "buffs":[]
                },
                {
                "_id":1,
                "updateTimer":{},
                "buffs":[]
                }
            ]
        }
        # print(new_artifact)
        self.current_data['level']['components']['mvz2:artifact']['artifacts']['artifacts'].append(new_artifact)
        self.refresh_artifact()
    # 移除制品
    def remove_artifact(self):
        if not self.artifact_tree.selection():
            return
        selected = self.artifact_tree.item(self.artifact_tree.selection()[0])["values"][0]
        # 先删对应关卡buff
        selected_artifact = self.current_data['level']['components']['mvz2:artifact']['artifacts']['artifacts'][selected]
        if not len(selected_artifact['auras'])==0:
            for auras in selected_artifact['auras']:
                for buff_artifact in auras['buffs']:
                    if not buff_artifact['_t']=="BuffReferenceLevel":
                        continue
                    for buff_level in list(self.current_data['level']['buffs']['buffs']):
                        if buff_level["_id"][1]==buff_artifact['buffId'][1]:
                            self.current_data['level']['buffs']['buffs'].remove(buff_level)
        # 再删制品
        self.current_data['level']['components']['mvz2:artifact']['artifacts']['artifacts'].pop(selected)
        # 刷新列表
        self.refresh_artifact()
    # 添加蓝图

    # 修改蓝图
    def modify_blueprint(self):
        if not self.blueprint_tree.selection():
            return
        selected = self.blueprint_tree.item(self.blueprint_tree.selection()[0])["values"][0]
        self.current_data['level']['seedPacks'][selected]['seedID']=blueprint_id[blueprint_name.index(self.blueprint_box.get())]
        if len(self.current_data['level']['seedPacks'][selected]['auras'])==0:
            self.current_data['level']['seedPacks'][selected]['auras'].append(
                    {
                        "updateTimer": {
                            "maxFrame": 1,
                            "lastFrame": 1,
                            "lastFrameFraction": 0,
                            "frame": 1,
                            "frameFraction": 0,
                            "precision": 2048
                        },
                        "buffs": []
                    }
            )
        self.refresh_blueprint()
    # 移除蓝图

    # endregion
    # region numeric_frame
    # 混乱
    def mix_stageDefinitionID(self,event):
        """处理混乱"""
        mapID = maps_name.index(self.numeric_stageDefinition_box.get())
        isSpecial = (level_day.count(self.numeric_stageDefinitionID_box.get())==0)
        if (mapID != 3):
            if (isSpecial):
                self.numeric_stageDefinitionID_box.config(values=level_day)
                self.numeric_stageDefinitionID_box.set(level_day[0])
            self.current_data['level']['stageDefinitionID'] = maps_id[mapID] + "_" + self.numeric_stageDefinitionID_box.get()
        else:
            if (not isSpecial):
                self.numeric_stageDefinitionID_box.config(values=level_name)
                self.numeric_stageDefinitionID_box.set(level_name[0])
            self.current_data['level']['stageDefinitionID'] = level_id[level_name.index(self.numeric_stageDefinitionID_box.get())]

    # 旗数
    def change_flag(self, action, index, value, prior_value, text, validation_type, trigger_type):
        if value=="":
            self.current_data['level']['currentFlag']=0
            return True
        if value.isdigit():
            self.current_data['level']['currentFlag']=int(value)
            return True
        return False
    # 波数
    def change_wave(self, action, index, value, prior_value, text, validation_type, trigger_type):
        if value=="":
            self.current_data['level']['currentWave']=0
            return True
        if value.isdigit():
            self.current_data['level']['currentWave']=int(value)
            return True
        return False
    # 当前机械能
    def change_energy(self, action, index, value, prior_value, text, validation_type, trigger_type):
        if value=="":
            self.current_data['level']['energy']=0
            return True
        try:
            self.current_data['level']['energy']=float(value)  # 检查浮点数
            return True
        except ValueError:
            return False
    # 机械能上限
    def change_maxEnergy(self, action, index, value, prior_value, text, validation_type, trigger_type):
        if value=="":
            self.current_data['level']['Option']['maxEnergy']=0
            return True
        try:
            self.current_data['level']['Option']['maxEnergy']=float(value)  # 检查浮点数
            return True
        except ValueError:
            return False
    # 星之碎片数
    def change_starshardCount(self, action, index, value, prior_value, text, validation_type, trigger_type):
        if value=="":
            self.current_data['level']['properties']['starshardCount']=0
            return True
        if value.isdigit():
            self.current_data['level']['properties']['starshardCount']=int(value)
            return True
        return False
    # 星之碎片槽
    def change_starshardSlotCount(self, action, index, value, prior_value, text, validation_type, trigger_type):
        if value=="":
            self.current_data['level']['properties']['starshardSlotCount']=0
            return True
        if value.isdigit():
            self.current_data['level']['properties']['starshardSlotCount']=int(value)
            return True
        return False
    # 是否启用传送带
    def is_ConveyorMode(self,event):
        if self.numeric_isConveyorMode_box.get()==get_text("True"):
            self.current_data['level']['components']['mvz2:blueprints']['isConveyorMode'] = True
            self.current_data['level']['properties']['noEnergy'] = True
        else:
            self.current_data['level']['components']['mvz2:blueprints']['isConveyorMode'] = False
            self.current_data['level']['properties']['noEnergy'] = False
    # 传送带槽数
    def change_conveyorSlotCount(self, action, index, value, prior_value, text, validation_type, trigger_type):
        if value=="":
            self.current_data['level']['conveyorSlotCount']=0
            return True
        if value.isdigit():
            self.current_data['level']['conveyorSlotCount']=int(value)
            return True
        return False
    # 背景音乐
    def change_musicID(self,event):
        self.current_data['musicID'] = musics_id[musics_name.index(self.numeric_musicID_box.get())]
    # 关于
    def open_about(self):
        Selector.AboutWindow(self.root)


    # endregion
    # 保存文件
    def output_file(self):
        save_dir=get_save_path() + "/user%d/mvz2/level/"%(self.currentUserIndex) + os.path.basename(self.current_file)
        output=json.dumps(self.current_data,cls=CustonJson.CustomEncoder).encode("utf-8")
        self.status.set(get_text("status_save") + save_dir)
        compress(save_dir,output)
    # 切换界面
    def switch_frame(self):
        if self.page:
            self.page=0
            self.frame_tree.pack_forget()
            self.setup_numeric_frame()
        else:
            self.page=1
            self.frame_numeric.pack_forget()
            self.setup_tree_frame()
            # self.refresh()
    # 打开存档文件夹
    def open_save_explorer(self):
        save_dir=get_save_path() + ("/user%d/mvz2/level"%(self.currentUserIndex))
        subprocess.run(f'explorer "{os.path.normpath(save_dir)}"', shell=True)
    #endregion

    # region 工具
    def get_usersdata(self):
        '''获取用户数据'''
        users_path = get_save_path() + "/users.dat"
        self.users = json.loads(decompress(users_path),cls=CustonJson.CustomDecoder)
        self.currentUserIndex = self.users['currentUserIndex']
        self.username = self.users['metas'][self.currentUserIndex]['username']
    
    def decompress(self):
        '''单文件解压'''
        file_path = filedialog.askopenfilename(
            title="Choose file",
            filetypes=[("Save file", ["*.dat", "*.lvl"])]
        )
        if not file_path:
            return
        try:
            with gzip.open(file_path, "rb") as fin:
                with open(file_path + ".json", "wb") as fout:
                    fout.write(fin.read())
            self.status.set(f"Output: {os.path.basename(file_path)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to decompress: {str(e)}")

    def compress(self):
        '''单文件压缩'''
        file_path = filedialog.askopenfilename(
            title="Choose file",
            filetypes=[("JSON file", "*.json"), ("Any file", "*")]
        )
        if not file_path:
            return
        try:
            with open(file_path, "rb") as fin:
                with gzip.open(file_path + ".lvl", "wb") as fout:
                    shutil.copyfileobj(fin, fout)
            self.status.set(f"Output: {os.path.basename(file_path)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to compress: {str(e)}")
    # endregion

    # region 刷新，获取关卡数据
    def refresh(self):
        """刷新界面"""
        self.artifact_box.config(state="readonly")
        self.artifact_box.set(artifact_name[0])
        self.blueprint_box.config(state="readonly")
        self.blueprint_box.set(blueprint_name[0])
        self.output_btn.config(state="normal")
        self.refresh_artifact()
        self.refresh_blueprint()
        self.refresh_numeric()

    def refresh_artifact(self):
        """刷新制品列表"""
        data_artifact = self.current_data['level']['components']['mvz2:artifact']['artifacts']['artifacts']
        self.artifact_tree.delete(*self.artifact_tree.get_children())
        for i in range(len(data_artifact)):
            if data_artifact[i]:
                self.artifact_tree.insert("", "end", values=(i, artifact_name[artifact_id.index(data_artifact[i]['definitionID'])]))

    def refresh_blueprint(self):
        """刷新蓝图列表"""
        data_blueprint = self.current_data['level']['seedPacks']
        self.blueprint_tree.delete(*self.blueprint_tree.get_children())
        for i in range(len(data_blueprint)):
            if data_blueprint[i]:
                self.blueprint_tree.insert("", "end", values=(i, blueprint_name[blueprint_id.index(data_blueprint[i]['seedID'])]))

    def refresh_numeric(self):
        self.refresh_numeric_map_box()
        self.numeric_flag_input.config(state="normal")
        self.data_flag.set(self.current_data['level']['currentFlag'])
        self.numeric_wave_input.config(state="normal")
        self.data_wave.set(self.current_data['level']['currentWave'])
        self.numeric_energy_input.config(state="normal")
        self.data_energy.set(self.current_data['level']['energy'])
        self.numeric_maxEnergy_input.config(state="normal")
        self.data_maxEnergy.set(self.current_data['level']['Option']['maxEnergy'])
        self.numeric_starshardCount_input.config(state="normal")
        if not ('starshardCount' in self.current_data['level']['properties']):
            self.current_data['level']['properties']['starshardCount']=0
        self.data_starshardCount.set(self.current_data['level']['properties']['starshardCount'])
        self.numeric_starshardSlotCount_input.config(state="normal")
        self.data_starshardSlotCount.set(self.current_data['level']['properties']['starshardSlotCount'])
        self.refresh_boolean_box(self.current_data['level']['components']['mvz2:blueprints']['isConveyorMode'], self.numeric_isConveyorMode_box)
        self.numeric_conveyorSlotCount_input.config(state="normal")
        self.data_conveyorSlotCount.set(self.current_data['level']['conveyorSlotCount'])
        self.numeric_musicID_box.config(state="readonly")
        self.numeric_musicID_box.set(musics_name[musics_id.index(self.current_data['musicID'])])

    def refresh_numeric_map_box(self):
        self.numeric_stageDefinition_box.config(state="readonly")
        self.numeric_stageDefinitionID_box.config(state="readonly")
        if not (level_id.count(self.current_data['level']['stageDefinitionID'])==0):
            self.numeric_stageDefinitionID_box.config(values=level_name)
            self.numeric_stageDefinitionID_box.set(level_name[level_id.index(self.current_data['level']['stageDefinitionID'])])
            self.numeric_stageDefinition_box.set(maps_name[3])
        else:
            self.numeric_stageDefinition_box.set(maps_name[maps_id.index(self.current_data['level']['stageDefinitionID'].split("_")[0])])
            self.numeric_stageDefinitionID_box.set(self.current_data['level']['stageDefinitionID'].split("_")[1])

    def refresh_boolean_box(self, data, box):
        box.config(state="readonly")
        if data:
            box.set(get_text("True"))
        else:
            box.set(get_text("False"))
    # endregion

if __name__ == "__main__":
    # messagebox.showinfo("免责声明",f"使用该软件造成的文件损坏，本人一概不负责")
    get_language()
    root = tk.Tk()
    app = ArchiveEditor(root)
    root.mainloop()