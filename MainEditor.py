import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import gzip,shutil,os,json,winreg,subprocess
import platform
import CustonJson,Selector

maps_name_zh = ["万圣夜","梦境世界","辉针城"]
maps_name_en = ["Halloween","Dream","Castle"]
maps_name = None
maps_id = ["mvz2:halloween","mvz2:dream","mvz2:castle"] 

level = ["1","2","3","4","5","6","7","8","9","10","11","endless"]

artifact_name_zh = ["图鉴","锄头","梦境钥匙","怪物的心","安眠枕","槐树树枝","梦蝶","暗物质","智能手机","倒置的镜子","万宝槌仿制品","凋零骷髅头","下界之星","破灯笼"]
artifact_name_en = ["almanac","hoe","dream_key","the_creatures_heart","sweet_sleep_pillow","pagoda_branch","dream_butterfly","dark_matter","smart_phone","inverted_mirror","miracle_mallet_replica","wither_skeleton_skull","nether_star","broken_lantern"]
artifact_name = None
artifact_id = ["mvz2:almanac","mvz2:hoe","mvz2:dream_key","mvz2:the_creatures_heart","mvz2:sweet_sleep_pillow","mvz2:pagoda_branch","mvz2:dream_butterfly","mvz2:dark_matter","mvz2:smart_phone","mvz2:inverted_mirror","mvz2:miracle_mallet_replica","mvz2:wither_skeleton_skull","mvz2:nether_star","mvz2:broken_lantern"]

blueprint_name_zh = ["发射器", "熔炉", "黑曜石", "地雷TNT", "小型发射器", "月光传感器", "荧石", "冲击活塞", "TNT", "灵魂熔炉", "银质发射器", "魔术箱", "睡莲", "驱动发射器", "重力板", "漩涡漏斗", "活塞发射器", "图腾发射器", "梦境结晶", "美梦丝", "木制投掷器", "尖刺方块", "石制投掷器", "石护罩", "金苹果", "雷鼓", "磁暴线圈", "巨碗", "传染发射器", "传动力板", "金制投掷器", "钻石尖刺", "铁砧", "随机瓷器", "僵尸", "皮帽僵尸", "铁盔僵尸", "旗帜僵尸", "骷髅", "石像鬼", "幽灵", "木乃伊", "死灵法师", "蜘蛛", "洞穴蜘蛛", "恶魂", "恐怖之母", "恐怖寄生虫", "催眠者", "狂战士", "无头骑士", "地狱战车", "灵魂沙王", "突变僵尸", "超级突变僵尸", "小鬼僵尸", "骨墙", "小幽灵", "反则卫星", "骷髅马", "无头骑士的头", "灵魂沙", "正邪的诅咒人偶", "床战士", "石像鬼雕像", "科学怪人的怪物", "瘦长鬼影", "梦魇收割者", "鬼人正邪", "凋灵", "矿车", "南瓜马车", "彩虹猫", "噩梦猫", "碗车", "红石", "绿宝石", "红宝石", "蓝宝石", "钻石", "通关掉落物", "制品掉落物", "星之碎片", "arrow", "mine_tnt_seed", "snowball", "large_snowball", "flying_tnt", "soulfire_ball", "knife", "bullet", "missile", "fire_charge", "large_arrow", "spike", "spike_ball", "diamond_caltrop", "dart", "poison_javelin", "parabot", "breakout_pearl", "wooden_ball", "cobble", "boulder", "golden_ball", "compelling_orb", "seija_magic_bomb", "seija_bullet", "wither_skull", "miner", "mine_debris", "fragment", "star_particles", "gem_effect", "smoke", "broken_armor", "thunder_bolt", "evocation_star", "shine_ring", "stun_stars", "stunning_flash", "explosion", "soulfire", "soulfire_burn", "soulfire_blast", "mummy_gas", "burning_gas", "heal_particles", "bone_particles", "blood_particles", "smoke_cluster", "rain", "electric_arc", "gore_particles", "frankenstein_jump_trail", "frankenstein_head", "splash_particles", "gear_particles", "pow", "vortex", "giant_spike", "fire_breath", "weakness_gas", "magnetic_line", "hoe", "breakout_board", "nightmare_watching_eye", "nightmare_portal", "dark_matter_particles", "nightmareaper_splash", "nightmareaper_shadow", "slice_spark", "梦魇碾压墙", "nightmareaper_timer", "floating_text", "nightmare_darkness", "nightmare_glass", "spike_particles", "diamond_spike_particles", "mind_control_lines", "mutant_zombie_weapon", "water_lightning_particles", "thunder_cloud", "magic_bomb_explosion", "seija_camera_frame", "seija_faint_effect", "wither_summoners", "castle_twilight"]
blueprint_name_en = ["dispenser", "furnace", "obsidian", "mine_tnt", "small_dispenser", "moonlight_sensor", "glowstone", "punchton", "tnt", "soul_furnace", "silvenser", "magichest", "lily_pad", "drivenser", "gravity_pad", "vortex_hopper", "pistenser", "totenser", "dream_crystal", "dream_silk", "wooden_dropper", "spike_block", "stone_dropper", "stone_shield", "golden_apple", "thunder_drum", "tesla_coil", "giant_bowl", "infectenser", "force_pad", "golden_dropper", "diamond_spikes", "anvil", "random_china", "zombie", "leather_capped_zombie", "iron_helmetted_zombie", "flag_zombie", "skeleton", "gargoyle", "ghost", "mummy", "necromancer", "spider", "cave_spider", "ghast", "mother_terror", "parasite_terror", "mesmerizer", "berserker", "dullahan", "hell_chariot", "anubisand", "mutant_zombie", "mega_mutant_zombie", "imp", "bone_wall", "napstablook", "reverse_satellite", "skeleton_horse", "dullahan_head", "soulsand", "seija_cursed_doll", "bedserker", "gargoyle_statue", "frankenstein", "slenderman", "nightmareaper", "seija", "wither", "minecart", "pumpkin_carriage", "nyan_cat", "nyaightmare", "bowl_chariot", "redstone", "emerald", "ruby", "sapphire", "diamond", "clear_pickup", "artifact_pickup", "starshard", "arrow", "mine_tnt_seed", "snowball", "large_snowball", "flying_tnt", "soulfire_ball", "knife", "bullet", "missile", "fire_charge", "large_arrow", "spike", "spike_ball", "diamond_caltrop", "dart", "poison_javelin", "parabot", "breakout_pearl", "wooden_ball", "cobble", "boulder", "golden_ball", "compelling_orb", "seija_magic_bomb", "seija_bullet", "wither_skull", "miner", "mine_debris", "fragment", "star_particles", "gem_effect", "smoke", "broken_armor", "thunder_bolt", "evocation_star", "shine_ring", "stun_stars", "stunning_flash", "explosion", "soulfire", "soulfire_burn", "soulfire_blast", "mummy_gas", "burning_gas", "heal_particles", "bone_particles", "blood_particles", "smoke_cluster", "rain", "electric_arc", "gore_particles", "frankenstein_jump_trail", "frankenstein_head", "splash_particles", "gear_particles", "pow", "vortex", "giant_spike", "fire_breath", "weakness_gas", "magnetic_line", "hoe", "breakout_board", "nightmare_watching_eye", "nightmare_portal", "dark_matter_particles", "nightmareaper_splash", "nightmareaper_shadow", "slice_spark", "crushing_walls", "nightmareaper_timer", "floating_text", "nightmare_darkness", "nightmare_glass", "spike_particles", "diamond_spike_particles", "mind_control_lines", "mutant_zombie_weapon", "water_lightning_particles", "thunder_cloud", "magic_bomb_explosion", "seija_camera_frame", "seija_faint_effect", "wither_summoners", "castle_twilight"]
blueprint_name = None
blueprint_id = ["mvz2:dispenser", "mvz2:furnace", "mvz2:obsidian", "mvz2:mine_tnt", "mvz2:small_dispenser", "mvz2:moonlight_sensor", "mvz2:glowstone", "mvz2:punchton", "mvz2:tnt", "mvz2:soul_furnace", "mvz2:silvenser", "mvz2:magichest", "mvz2:lily_pad", "mvz2:drivenser", "mvz2:gravity_pad", "mvz2:vortex_hopper", "mvz2:pistenser", "mvz2:totenser", "mvz2:dream_crystal", "mvz2:dream_silk", "mvz2:wooden_dropper", "mvz2:spike_block", "mvz2:stone_dropper", "mvz2:stone_shield", "mvz2:golden_apple", "mvz2:thunder_drum", "mvz2:tesla_coil", "mvz2:giant_bowl", "mvz2:infectenser", "mvz2:force_pad", "mvz2:golden_dropper", "mvz2:diamond_spikes", "mvz2:anvil", "mvz2:random_china", "mvz2:zombie", "mvz2:leather_capped_zombie", "mvz2:iron_helmetted_zombie", "mvz2:flag_zombie", "mvz2:skeleton", "mvz2:gargoyle", "mvz2:ghost", "mvz2:mummy", "mvz2:necromancer", "mvz2:spider", "mvz2:cave_spider", "mvz2:ghast", "mvz2:mother_terror", "mvz2:parasite_terror", "mvz2:mesmerizer", "mvz2:berserker", "mvz2:dullahan", "mvz2:hell_chariot", "mvz2:anubisand", "mvz2:mutant_zombie", "mvz2:mega_mutant_zombie", "mvz2:imp", "mvz2:bone_wall", "mvz2:napstablook", "mvz2:reverse_satellite", "mvz2:skeleton_horse", "mvz2:dullahan_head", "mvz2:soulsand", "mvz2:seija_cursed_doll", "mvz2:bedserker", "mvz2:gargoyle_statue", "mvz2:frankenstein", "mvz2:slenderman", "mvz2:nightmareaper", "mvz2:seija", "mvz2:wither", "mvz2:minecart", "mvz2:pumpkin_carriage", "mvz2:nyan_cat", "mvz2:nyaightmare", "mvz2:bowl_chariot", "mvz2:redstone", "mvz2:emerald", "mvz2:ruby", "mvz2:sapphire", "mvz2:diamond", "mvz2:clear_pickup", "mvz2:artifact_pickup", "mvz2:starshard", "mvz2:arrow", "mvz2:mine_tnt_seed", "mvz2:snowball", "mvz2:large_snowball", "mvz2:flying_tnt", "mvz2:soulfire_ball", "mvz2:knife", "mvz2:bullet", "mvz2:missile", "mvz2:fire_charge", "mvz2:large_arrow", "mvz2:spike", "mvz2:spike_ball", "mvz2:diamond_caltrop", "mvz2:dart", "mvz2:poison_javelin", "mvz2:parabot", "mvz2:breakout_pearl", "mvz2:wooden_ball", "mvz2:cobble", "mvz2:boulder", "mvz2:golden_ball", "mvz2:compelling_orb", "mvz2:seija_magic_bomb", "mvz2:seija_bullet", "mvz2:wither_skull", "mvz2:miner", "mvz2:mine_debris", "mvz2:fragment", "mvz2:star_particles", "mvz2:gem_effect", "mvz2:smoke", "mvz2:broken_armor", "mvz2:thunder_bolt", "mvz2:evocation_star", "mvz2:shine_ring", "mvz2:stun_stars", "mvz2:stunning_flash", "mvz2:explosion", "mvz2:soulfire", "mvz2:soulfire_burn", "mvz2:soulfire_blast", "mvz2:mummy_gas", "mvz2:burning_gas", "mvz2:heal_particles", "mvz2:bone_particles", "mvz2:blood_particles", "mvz2:smoke_cluster", "mvz2:rain", "mvz2:electric_arc", "mvz2:gore_particles", "mvz2:frankenstein_jump_trail", "mvz2:frankenstein_head", "mvz2:splash_particles", "mvz2:gear_particles", "mvz2:pow", "mvz2:vortex", "mvz2:giant_spike", "mvz2:fire_breath", "mvz2:weakness_gas", "mvz2:magnetic_line", "mvz2:hoe", "mvz2:breakout_board", "mvz2:nightmare_watching_eye", "mvz2:nightmare_portal", "mvz2:dark_matter_particles", "mvz2:nightmareaper_splash", "mvz2:nightmareaper_shadow", "mvz2:slice_spark", "mvz2:crushing_walls", "mvz2:nightmareaper_timer", "mvz2:floating_text", "mvz2:nightmare_darkness", "mvz2:nightmare_glass", "mvz2:spike_particles", "mvz2:diamond_spike_particles", "mvz2:mind_control_lines", "mvz2:mutant_zombie_weapon", "mvz2:water_lightning_particles", "mvz2:thunder_cloud", "mvz2:magic_bomb_explosion", "mvz2:seija_camera_frame", "mvz2:seija_faint_effect", "mvz2:wither_summoners", "mvz2:castle_twilight"]

musics_name_zh = ['疯狂戴夫', '选择你的种子', '草地行走', '莱克死灵之书-关卡', '莱克死灵之书-地图', '狂人的愉悦', '终极之战', '莱克死灵之书-首领', '破碎的童话-关卡', '破碎的童话-地图', '悬念', '以撒的结合', '忏悔', '飞翔于宇宙的不可思议巫女', 'Pandemonic Planet（前段）', 'Pandemonic Planet（后段）', '青空之影', '记忆的回响', '沉默空洞的辉针城', '凋灵舞曲', '有只僵尸在你的手机里', 'Reverse Ideology', '针折线断的天守阁', '辉光之针的小人族 ~ Little Princess', '惊疑星球-首领']
musics_name_en = ["Crazy Dave", "Choose Your Seeds", "Grasswalk", "Lexonomicon Level", "Lexonomicon Map", "Loon Boon","Utimate Battle", "Lexonomicon Boss", "Fractured Fairytales Level", "Fractured Fairytales Map", "Suspension", "The Binding of Isaac", "Repentant", "The Mysterious Shrine Maiden Flying Through", "Pandemonic Planet (1st part)", "Pandemonic Planet (2nd part)", "A Shadow in the Blue Sky","Fading Echoes of Memory","The Shining Needle Castle Sinking to the Void", "Witherstep", "Zombies in your phone", "Reverse Ideology", "The Exacerbated Castle Keep", "Inchlings of the Shining Needle ~ Little Princess", "Astounding Planet Boss"]
musics_name = None
musics_id = ['mvz2:mainmenu', 'mvz2:choosing', 'mvz2:day', 'mvz2:halloween', 'mvz2:halloween_map', 'mvz2:minigame', 'mvz2:ultimate_battle', 'mvz2:halloween_boss', 'mvz2:dream_level', 'mvz2:dream_map', 'mvz2:suspension', 'mvz2:nightmare_map', 'mvz2:nightmare_level', 'mvz2:nightmare_final', 'mvz2:nightmare_boss', 'mvz2:nightmare_boss2', 'mvz2:gensokyo_map', 'mvz2:distress', 'mvz2:castle_map', 'mvz2:castle_level', 'mvz2:phone_ring', 'mvz2:seija', 'mvz2:sad_shinmyoumaru', 'mvz2:castle_final', 'mvz2:wither_boss']

text_name_zh = ["MVZ2存档修改器 v1.2 by QoZnoS", "就绪", "保存文件", "当前用户：", "切换", "解压 (.dat/.lvl → .json)", "压缩 (.json → .lvl)", "当前文件：未选择", "选择文件", "切换界面", "制品名称", "添加", "删除", "蓝图名称", "修改", "当前文件：", "章节：", "关卡：", "旗数：", "波数：", "当前机械能：", "机械能上限：", "星之碎片数：", "星之碎片槽：", "启用传送带：", "传送带槽数：", "背景音乐：", "关于修改器", "是", "否", "已保存到：", "打开存档文件夹"]
text_name_en = ["MVZ2SaveModifier v1.2 by QoZnoS", "Ready", "Execute the modification", "current user: ", "switch", "Decompress(.dat/.lvl → .json)", "Compress(.json → .lvl)", "current level: empty", "Select level file", "Another page", "Artifact name", "Add", "Delete", "Blueprint name", "Modify", "current level: ", "Chapter: ", "Day: ", "Flag: ", "Wave: ", "Energy: ", "maxEnergy: ", "Starshard: ", "maxStarshard: ", "ConveyorMode: ", "ConveyorSlot: ", "BGM: ", "About SaveModifier", "True", "False", "Save to: ", "View in Explorer"]
text_name = None
text_id = ["title","status_ready","btn_save","label_user","btn_switch","btn_unzip","btn_zip","label_lvl_null","btn_lvl","btn_page","tree_artifact","btn_add","btn_delete","tree_blueprint","btn_modify","label_lvl","label_chapter","label_day","label_flag","label_wave","label_energy","label_maxEnergy","label_starshard","label_maxStarshard","label_conveyor","label_conveyorslot","label_bgm","btn_about","True","False","status_save","btn_open_explorer"]

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
    global maps_name,artifact_name,blueprint_name,musics_name,text_name
    if is_zh:
        maps_name = maps_name_zh
        artifact_name = artifact_name_zh
        blueprint_name = blueprint_name_zh
        musics_name = musics_name_zh
        text_name = text_name_zh
    else:
        maps_name = maps_name_en
        artifact_name = artifact_name_en
        blueprint_name = blueprint_name_en
        musics_name = musics_name_en
        text_name = text_name_en

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
        self.numeric_stageDefinitionID_box = ttk.Combobox(frame_group,values=level,state="disable",width=16)
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
        self.current_data['level']['stageDefinitionID'] = maps_id[maps_name.index(self.numeric_stageDefinition_box.get())] + "_" + self.numeric_stageDefinitionID_box.get()
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
            self.refresh()
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

    # region 刷新
    def refresh(self):
        """刷新界面"""
        if not self.current_data:
            self.artifact_box.config(state="disabled")
            self.artifact_box.set("")
            self.blueprint_box.config(state="disabled")
            self.blueprint_box.set("")

            self.filename_label.config(text=get_text("label_lvl_null"))
            self.output_btn.config(state="disabled")
        else:
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
        if not self.current_data:
            self.numeric_stageDefinition_box.config(state="disabled")
            self.numeric_stageDefinition_box.set("")
            self.numeric_stageDefinitionID_box.config(state="disabled")
            self.numeric_stageDefinitionID_box.set("")
            self.numeric_flag_input.config(state="disable")
            self.numeric_wave_input.config(state="disable")
            self.numeric_energy_input.config(state="disable")
            self.numeric_maxEnergy_input.config(state="disable")
            self.numeric_starshardCount_input.config(state="disable")
            self.numeric_starshardSlotCount_input.config(state="disable")
            self.numeric_isConveyorMode_box.config(state="disable")
            self.numeric_conveyorSlotCount_input.config(state="disable")
            self.numeric_musicID_box.config(state="disable")
            self.numeric_musicID_box.set("")
        else:
            self.numeric_stageDefinition_box.config(state="readonly")
            self.numeric_stageDefinition_box.set(maps_name[maps_id.index(self.current_data['level']['stageDefinitionID'].split("_")[0])])
            self.numeric_stageDefinitionID_box.config(state="readonly")
            self.numeric_stageDefinitionID_box.set(self.current_data['level']['stageDefinitionID'].split("_")[1])
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
            self.numeric_isConveyorMode_box.config(state="readonly")
            if self.current_data['level']['components']['mvz2:blueprints']['isConveyorMode']:
                self.numeric_isConveyorMode_box.set(get_text("True"))
            else:
                self.numeric_isConveyorMode_box.set(get_text("False"))
            self.numeric_conveyorSlotCount_input.config(state="normal")
            self.data_conveyorSlotCount.set(self.current_data['level']['conveyorSlotCount'])
            self.numeric_musicID_box.config(state="readonly")
            self.numeric_musicID_box.set(musics_name[musics_id.index(self.current_data['musicID'])])
    # endregion

if __name__ == "__main__":
    # messagebox.showinfo("免责声明",f"使用该软件造成的文件损坏，本人一概不负责")
    get_language()
    root = tk.Tk()
    app = ArchiveEditor(root)
    root.mainloop()