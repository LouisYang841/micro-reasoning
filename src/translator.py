#!/usr/bin/env python3
"""微语→中文翻译器 — 纯字典规则，0参数"""

# 位置/方向 → 中文
POS_MAP = {"里":"里", "上":"上", "下":"下", "旁":"旁", "处":"处"}

def translate(mic_answer: str, entity_map: str) -> str:
    """
    mic_answer: 微语回答如 "丙里" "戊处" "丙上"
    entity_map: "甲=小明 乙=苹果 丙=书包 丁=学校 戊=老师"
    """
    # 解析实体映射
    entities = {}
    for item in entity_map.split():
        if "=" in item:
            k, v = item.split("=", 1)
            entities[k] = v
    
    result = mic_answer
    # 替换实体符号
    for gan, name in entities.items():
        result = result.replace(gan, name)
    
    return result

# === 测试 ===
if __name__ == "__main__":
    tests = [
        ("丙里", "甲=小明 乙=苹果 丙=书包"),
        ("戊处", "甲=妈妈 乙=水 戊=老师"),
        ("丙上", "甲=小红 乙=书 丙=桌子"),
        ("丙里", "甲=爸爸 乙=手机 丙=抽屉"),
    ]
    for ans, emap in tests:
        print(f"微语: {ans} | 映射: {emap} | → {translate(ans, emap)}")
