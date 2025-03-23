import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import gzip,shutil,os,json
import platform
import CustonJson,Selector

maps_name = ["万圣夜","梦境世界","辉针城"]
maps_id = ["mvz2:halloween","mvz2:dream","mvz2:castle"] 
level = ["1","2","3","4","5","6","7","8","9","10","11","endless"]
artifact_name = ["图鉴","锄头","梦境钥匙","怪物的心","安眠枕","槐树树枝","梦蝶","暗物质","智能手机","倒置的镜子","万宝槌仿制品","凋零骷髅头","下界之星","破灯笼"]
artifact_id = ["mvz2:almanac","mvz2:hoe","mvz2:dream_key","mvz2:the_creatures_heart","mvz2:sweet_sleep_pillow","mvz2:pagoda_branch","mvz2:dream_butterfly","mvz2:dark_matter","mvz2:smart_phone","mvz2:inverted_mirror","mvz2:miracle_mallet_replica","mvz2:wither_skeleton_skull","mvz2:nether_star","mvz2:broken_lantern"]
blueprint_name = ["发射器", "熔炉", "黑曜石", "地雷TNT", "小型发射器", "月光传感器", "荧石", "冲击活塞", "TNT", "灵魂熔炉", "银质发射器", "魔术箱", "睡莲", "驱动发射器", "重力板", "漩涡漏斗", "活塞发射器", "图腾发射器", "梦境结晶", "美梦丝", "木制投掷器", "尖刺方块", "石制投掷器", "石护罩", "金苹果", "雷鼓", "磁暴线圈", "巨碗", "传染发射器", "传动力板", "金制投掷器", "钻石尖刺", "铁砧", "随机瓷器", "僵尸", "皮帽僵尸", "铁盔僵尸", "旗帜僵尸", "骷髅", "石像鬼", "幽灵", "木乃伊", "死灵法师", "蜘蛛", "洞穴蜘蛛", "恶魂", "恐怖之母", "恐怖寄生虫", "催眠者", "狂战士", "无头骑士", "地狱战车", "灵魂沙王", "突变僵尸", "超级突变僵尸", "小鬼僵尸", "骨墙", "小幽灵", "反则卫星", "骷髅马", "无头骑士的头", "灵魂沙", "正邪的诅咒人偶", "床战士", "石像鬼雕像", "科学怪人的怪物", "瘦长鬼影", "梦魇收割者", "鬼人正邪", "凋灵", "矿车", "南瓜马车", "彩虹猫", "噩梦猫", "碗车", "红石", "绿宝石", "红宝石", "蓝宝石", "钻石", "通关掉落物", "制品掉落物", "星之碎片", "arrow", "mine_tnt_seed", "snowball", "large_snowball", "flying_tnt", "soulfire_ball", "knife", "bullet", "missile", "fire_charge", "large_arrow", "spike", "spike_ball", "diamond_caltrop", "dart", "poison_javelin", "parabot", "breakout_pearl", "wooden_ball", "cobble", "boulder", "golden_ball", "compelling_orb", "seija_magic_bomb", "seija_bullet", "wither_skull", "miner", "mine_debris", "fragment", "star_particles", "gem_effect", "smoke", "broken_armor", "thunder_bolt", "evocation_star", "shine_ring", "stun_stars", "stunning_flash", "explosion", "soulfire", "soulfire_burn", "soulfire_blast", "mummy_gas", "burning_gas", "heal_particles", "bone_particles", "blood_particles", "smoke_cluster", "rain", "electric_arc", "gore_particles", "frankenstein_jump_trail", "frankenstein_head", "splash_particles", "gear_particles", "pow", "vortex", "giant_spike", "fire_breath", "weakness_gas", "magnetic_line", "hoe", "breakout_board", "nightmare_watching_eye", "nightmare_portal", "dark_matter_particles", "nightmareaper_splash", "nightmareaper_shadow", "slice_spark", "梦魇碾压墙", "nightmareaper_timer", "floating_text", "nightmare_darkness", "nightmare_glass", "spike_particles", "diamond_spike_particles", "mind_control_lines", "mutant_zombie_weapon", "water_lightning_particles", "thunder_cloud", "magic_bomb_explosion", "seija_camera_frame", "seija_faint_effect", "wither_summoners", "castle_twilight"]
blueprint_id = ["mvz2:dispenser", "mvz2:furnace", "mvz2:obsidian", "mvz2:mine_tnt", "mvz2:small_dispenser", "mvz2:moonlight_sensor", "mvz2:glowstone", "mvz2:punchton", "mvz2:tnt", "mvz2:soul_furnace", "mvz2:silvenser", "mvz2:magichest", "mvz2:lily_pad", "mvz2:drivenser", "mvz2:gravity_pad", "mvz2:vortex_hopper", "mvz2:pistenser", "mvz2:totenser", "mvz2:dream_crystal", "mvz2:dream_silk", "mvz2:wooden_dropper", "mvz2:spike_block", "mvz2:stone_dropper", "mvz2:stone_shield", "mvz2:golden_apple", "mvz2:thunder_drum", "mvz2:tesla_coil", "mvz2:giant_bowl", "mvz2:infectenser", "mvz2:force_pad", "mvz2:golden_dropper", "mvz2:diamond_spikes", "mvz2:anvil", "mvz2:random_china", "mvz2:zombie", "mvz2:leather_capped_zombie", "mvz2:iron_helmetted_zombie", "mvz2:flag_zombie", "mvz2:skeleton", "mvz2:gargoyle", "mvz2:ghost", "mvz2:mummy", "mvz2:necromancer", "mvz2:spider", "mvz2:cave_spider", "mvz2:ghast", "mvz2:mother_terror", "mvz2:parasite_terror", "mvz2:mesmerizer", "mvz2:berserker", "mvz2:dullahan", "mvz2:hell_chariot", "mvz2:anubisand", "mvz2:mutant_zombie", "mvz2:mega_mutant_zombie", "mvz2:imp", "mvz2:bone_wall", "mvz2:napstablook", "mvz2:reverse_satellite", "mvz2:skeleton_horse", "mvz2:dullahan_head", "mvz2:soulsand", "mvz2:seija_cursed_doll", "mvz2:bedserker", "mvz2:gargoyle_statue", "mvz2:frankenstein", "mvz2:slenderman", "mvz2:nightmareaper", "mvz2:seija", "mvz2:wither", "mvz2:minecart", "mvz2:pumpkin_carriage", "mvz2:nyan_cat", "mvz2:nyaightmare", "mvz2:bowl_chariot", "mvz2:redstone", "mvz2:emerald", "mvz2:ruby", "mvz2:sapphire", "mvz2:diamond", "mvz2:clear_pickup", "mvz2:artifact_pickup", "mvz2:starshard", "mvz2:arrow", "mvz2:mine_tnt_seed", "mvz2:snowball", "mvz2:large_snowball", "mvz2:flying_tnt", "mvz2:soulfire_ball", "mvz2:knife", "mvz2:bullet", "mvz2:missile", "mvz2:fire_charge", "mvz2:large_arrow", "mvz2:spike", "mvz2:spike_ball", "mvz2:diamond_caltrop", "mvz2:dart", "mvz2:poison_javelin", "mvz2:parabot", "mvz2:breakout_pearl", "mvz2:wooden_ball", "mvz2:cobble", "mvz2:boulder", "mvz2:golden_ball", "mvz2:compelling_orb", "mvz2:seija_magic_bomb", "mvz2:seija_bullet", "mvz2:wither_skull", "mvz2:miner", "mvz2:mine_debris", "mvz2:fragment", "mvz2:star_particles", "mvz2:gem_effect", "mvz2:smoke", "mvz2:broken_armor", "mvz2:thunder_bolt", "mvz2:evocation_star", "mvz2:shine_ring", "mvz2:stun_stars", "mvz2:stunning_flash", "mvz2:explosion", "mvz2:soulfire", "mvz2:soulfire_burn", "mvz2:soulfire_blast", "mvz2:mummy_gas", "mvz2:burning_gas", "mvz2:heal_particles", "mvz2:bone_particles", "mvz2:blood_particles", "mvz2:smoke_cluster", "mvz2:rain", "mvz2:electric_arc", "mvz2:gore_particles", "mvz2:frankenstein_jump_trail", "mvz2:frankenstein_head", "mvz2:splash_particles", "mvz2:gear_particles", "mvz2:pow", "mvz2:vortex", "mvz2:giant_spike", "mvz2:fire_breath", "mvz2:weakness_gas", "mvz2:magnetic_line", "mvz2:hoe", "mvz2:breakout_board", "mvz2:nightmare_watching_eye", "mvz2:nightmare_portal", "mvz2:dark_matter_particles", "mvz2:nightmareaper_splash", "mvz2:nightmareaper_shadow", "mvz2:slice_spark", "mvz2:crushing_walls", "mvz2:nightmareaper_timer", "mvz2:floating_text", "mvz2:nightmare_darkness", "mvz2:nightmare_glass", "mvz2:spike_particles", "mvz2:diamond_spike_particles", "mvz2:mind_control_lines", "mvz2:mutant_zombie_weapon", "mvz2:water_lightning_particles", "mvz2:thunder_cloud", "mvz2:magic_bomb_explosion", "mvz2:seija_camera_frame", "mvz2:seija_faint_effect", "mvz2:wither_summoners", "mvz2:castle_twilight"]


#region 全局函数
def get_save_path():
    '''根据系统返回userdata路径'''
    system = platform.system()
    if system == "Windows":
        return os.path.expandvars(r"C:/Users/%username%/AppData/LocalLow/Cuerzor/MinecraftVSZombies2/userdata")
    elif system == "Darwin":  # macOS
        return os.path.expanduser("~/Library/Application Support/Cuerzor/MinecraftVSZombies2/userdata")
    else:  # Linux
        return os.path.expanduser("~/.config/unity3d/Cuerzor/MinecraftVSZombies2/userdata")

def decompress(path):
    '''根据给定路径解压文件，返回解压后的文件'''
    try:
        with gzip.open(path, "rb") as file:
            return file.read()
    except Exception as e:
        messagebox.showerror("错误", f"解压失败: {str(e)}")

def compress(path,file):
    '''压缩文件到给定路径'''
    with gzip.open(path, "wb") as out:
        out.write(file)
#endregion

class ArchiveEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("MVZ2存档修改器v0.3 by QoZnoS")

        self.current_file = ""  # 当前操作的文件路径
        self.current_data = None # 当前操作的文件JSON数据
        self.data_artifact = None # 制品

        self.get_usersdata() # 自动读取存档
        self.setup_ui() # 创建UI
 
    # region 创建UI
    def setup_ui(self):
        self.setup_user_frame()
        self.setup_file_frame()
        self.setup_artifact_frame()

        # JSON 编辑区
        # self.text_editor = scrolledtext.ScrolledText(self.root, width=60, height=20)
        # self.text_editor.pack(pady=10, padx=10)

        # 保存
        self.output_btn=tk.Button(self.root, text="保存文件",command=self.output_file,state="disabled")
        self.output_btn.pack(fill=tk.X)

        # 状态栏
        self.status = tk.StringVar()
        self.status.set("就绪")
        tk.Label(self.root, textvariable=self.status, bd=1, relief=tk.SUNKEN, anchor=tk.W).pack(fill=tk.X)

    def setup_user_frame(self):
        """选择用户，单文件解压缩"""
        self.frame_user = tk.Frame(self.root)
        self.frame_user.pack(pady=10)
        self.username_label = tk.Label(self.frame_user, text="当前用户：" + self.username)
        self.username_label.pack(side=tk.LEFT)
        tk.Button(self.frame_user, text="切换", command=self.open_user_selector).pack(side=tk.LEFT, padx=5)
        tk.Button(self.frame_user, text="解压 (.dat/.lvl → .json)", command=self.decompress).pack(side=tk.LEFT, padx=10)
        tk.Button(self.frame_user, text="压缩 (.json → .dat)", command=self.compress).pack(side=tk.LEFT, padx=5)

    def setup_file_frame(self):
        """存档选择，混乱"""
        self.frame_file = tk.Frame(self.root)
        self.frame_file.pack(pady=10)
        self.filename_label = tk.Label(self.frame_file, text="当前文件：未选择")
        self.filename_label.pack(side=tk.LEFT)
        tk.Button(self.frame_file, text="选择文件", command=self.open_save_selector).pack(side=tk.LEFT, padx=10)

        # 混乱选项
        self.stageDefinition_box = ttk.Combobox(self.frame_file,values=maps_name,state="disable",width=10)
        self.stageDefinition_box.pack(side=tk.LEFT,padx=10)
        self.stageDefinition_box.set("未选择文件")
        self.stageDefinition_box.bind("<<ComboboxSelected>>",self.mix_stageDefinitionID)
        self.stageDefinitionID_box = ttk.Combobox(self.frame_file,values=level,state="disable",width=8)
        self.stageDefinitionID_box.pack(side=tk.LEFT,padx=2)
        self.stageDefinitionID_box.set("")
        self.stageDefinitionID_box.bind("<<ComboboxSelected>>",self.mix_stageDefinitionID)
        
    def setup_artifact_frame(self):
        """制品"""
        self.frame_artifact = tk.Frame(self.root)
        self.frame_artifact.pack(padx=10, expand=True)
        # 制品列表
        self.artifact_list = []
        self.artifact_tree = ttk.Treeview(self.frame_artifact,columns=("id","name"),show="headings",selectmode="browse")
        self.artifact_tree.heading("id",text="ID")
        self.artifact_tree.column("id",width=20)
        self.artifact_tree.heading("name",text="制品名称")
        self.artifact_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 右侧控制容器
        control_frame = tk.Frame(self.frame_artifact)
        control_frame.pack(side=tk.RIGHT, padx=10)  # 固定在右侧
        self.artifact_box = ttk.Combobox(control_frame, values=artifact_name, state="disabled", width=10)
        self.artifact_box.pack(pady=(0, 12))
        tk.Button(control_frame, text="添加", width=8, command=self.add_artifact).pack(fill=tk.X, pady=12)
        tk.Button(control_frame, text="删除", width=8, command=self.remove_artifact).pack(fill=tk.X, pady=12)

    def setup_blueprint_frame(self):
        """蓝图"""
        self.frame_blueprint = tk.Frame(self.root)

    # endregion

    # region 响应回调
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
            self.filename_label.config(text="当前存档：" + os.path.basename(self.current_file))
            self.refresh()
            # print(self.current_data)
            # print(json.dumps(self.current_data,cls=CustonJson.CustomEncoder))
        except Exception as e:
            messagebox.showerror("错误", f"加载存档失败:\n{str(e)}")
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
        self.username_label.config(text="当前用户：" + self.username)
    # 混乱
    def mix_stageDefinitionID(self,event):
        """处理混乱"""
        self.current_data['level']['stageDefinitionID'] = maps_id[maps_name.index(self.stageDefinition_box.get())] + "_" + self.stageDefinitionID_box.get()
    # 保存文件
    def output_file(self):
        save_dir=get_save_path() + "/user%d/mvz2/level/"%(self.currentUserIndex) + os.path.basename(self.current_file)
        output=json.dumps(self.current_data,cls=CustonJson.CustomEncoder).encode("utf-8")
        self.status.set("已保存到：" + save_dir)
        compress(save_dir,output)
    # 添加制品
    def add_artifact(self):
        if not self.artifact_box.get():
            return
        # 制品模板
        new_artifact = { 
            "definitionID":artifact_id[artifact_name.index(self.artifact_box.get())],
            "propertyDict": {
                "properties": {
                    "glowing": True
                }
            },
            "auras": [
                {
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
            for buff_artifact in selected_artifact['auras'][0]['buffs']:
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

    # 移除蓝图

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
            title="选择存档文件",
            filetypes=[("存档文件", ["*.dat", "*.lvl"])]
        )
        if not file_path:
            return
        try:
            with gzip.open(file_path, "rb") as fin:
                with open(file_path + ".json", "wb") as fout:
                    fout.write(fin.read())
            self.status.set(f"解压完成: {os.path.basename(file_path)}")
        except Exception as e:
            messagebox.showerror("错误", f"解压失败: {str(e)}")

    def compress(self):
        '''单文件压缩'''
        file_path = filedialog.askopenfilename(
            title="选择解压文件",
            filetypes=[("JSON 文件", "*.json"), ("任意文件", "*")]
        )
        if not file_path:
            return
        try:
            with open(file_path, "rb") as fin:
                with gzip.open(file_path + ".lvl", "wb") as fout:
                    shutil.copyfileobj(fin, fout)
            self.status.set(f"压缩完成: {os.path.basename(file_path)}")
        except Exception as e:
            messagebox.showerror("错误", f"压缩失败: {str(e)}")

    # endregion

    # 刷新
    def refresh(self):
        """刷新界面"""
        if not self.current_data:
            self.stageDefinition_box.config(state="disable")
            self.stageDefinition_box.set("未选择文件")
            self.stageDefinitionID_box.config(state="disable")
            self.stageDefinitionID_box.set("")
            self.artifact_box.config(state="disable")
            self.artifact_box.set("")
            self.filename_label.config(text="当前存档：未选择")
            
            self.output_btn.config(state="disabled")
        else:
            self.stageDefinition_box.config(state="readonly")
            self.stageDefinition_box.set(maps_name[maps_id.index(self.current_data['level']['stageDefinitionID'].split("_")[0])])
            self.stageDefinitionID_box.config(state="readonly")
            self.stageDefinitionID_box.set(self.current_data['level']['stageDefinitionID'].split("_")[1])
            self.artifact_box.config(state="readonly")
            self.artifact_box.set("图鉴")

            self.output_btn.config(state="normal")
            self.refresh_artifact()

    def refresh_artifact(self):
        """刷新制品列表"""
        data_artifact = self.current_data['level']['components']['mvz2:artifact']['artifacts']['artifacts']
        self.artifact_tree.delete(*self.artifact_tree.get_children())
        for i in range(len(data_artifact)):
            self.artifact_tree.insert("", "end", values=(i, artifact_name[artifact_id.index(data_artifact[i]['definitionID'])]))






if __name__ == "__main__":
    # messagebox.showinfo("免责声明",f"使用该软件造成的文件损坏，本人一概不负责")
    root = tk.Tk()
    app = ArchiveEditor(root)
    root.mainloop()