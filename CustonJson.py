import json
import re
from json import JSONDecoder
from json import JSONEncoder

class CustomDecoder(JSONDecoder):
    """解析非标准 JSON 中的 NumberLong(...)"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, object_hook=self.object_hook, **kwargs)
        self.parse_numberlong = re.compile(r'NumberLong\((\d+)\)')

    def decode(self, s):
        """重写 decode 方法预处理字符串"""
        # 将 NumberLong(123) 转换为合法 JSON 结构
        s = re.sub(
            r'NumberLong\((\d+)\)', 
            r'{"__type__": "NumberLong", "value": \1}', 
            s
        )
        return super().decode(s)

    def object_hook(self, obj):
        """将预处理后的标记替换为 ["NumberLong", value]"""
        if "__type__" in obj and obj["__type__"] == "NumberLong":
            return ["NumberLong", obj["value"]]
        return obj
    
class CustomEncoder(JSONEncoder):
    """生成非标准 JSON 中的 NumberLong(...)"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.indent = kwargs.get("indent", None)

    def preprocess_data(self, data):
        """替换 ['NumberLong',0] 为 "NumberLong(0)" """
        if isinstance(data, dict):
            return {k: self.preprocess_data(v) for k, v in data.items()}
        elif isinstance(data, list):
            if len(data) == 2 and data[0] == "NumberLong":
                return f"NumberLong({data[1]})"
            else:
                return [self.preprocess_data(item) for item in data]
        else:
            return data
        
    def encode(self, obj):
        """重写 encode 方法移除引号"""
        json_str = self.preprocess_data(obj)
        json_str = super().encode(json_str)
        # 去除 "NumberLong(0)" 的双引号
        json_str = re.sub(
            r'"NumberLong\((\d+)\)"',
            r'NumberLong(\1)',
            json_str
        )
        return json_str