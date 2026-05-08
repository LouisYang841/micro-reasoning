#!/usr/bin/env python3
"""微语→Emoji翻译器 — 展示用"""

EMOJI_ENTITIES = {
    "小明":"👦","小红":"👧","妈妈":"👩","爸爸":"👨","老师":"👨‍🏫","同学":"🧑‍🎓","弟弟":"👦",
    "苹果":"🍎","饭":"🍚","水":"💧","面包":"🍞","牛奶":"🥛","糖":"🍬","饼干":"🍪","面条":"🍜",
    "书包":"🎒","盒子":"📦","冰箱":"🧊","抽屉":"🗄","杯子":"🥤","碗":"🥣","袋子":"🛍","桌子":"🪑",
    "床":"🛏","房间":"🏠","学校":"🏫","车":"🚗","厨房":"🍳","沙发":"🛋",
    "钥匙":"🔑","书":"📚","手机":"📱","球":"⚽","笔":"✏","衣服":"👕","帽子":"🎩","花":"🌸",
}

EMOJI_POS = {"里":"📥", "上":"⬆", "下":"⬇", "旁":"↔", "处":"📍"}
EMOJI_GAN = {"甲":"1️⃣","乙":"2️⃣","丙":"3️⃣","丁":"4️⃣","戊":"5️⃣"}

def translate_emoji(mic_answer: str, entity_map: str) -> str:
    entities = {}
    for item in entity_map.split():
        if "=" in item:
            k, v = item.split("=", 1)
            entities[k] = v
    
    result = mic_answer
    for gan, name in entities.items():
        emoji = EMOJI_ENTITIES.get(name, name)
        result = result.replace(gan, emoji)
    for pos, epos in EMOJI_POS.items():
        result = result.replace(pos, epos)
    
    return result

# === 展示 ===
if __name__ == "__main__":
    from translator import translate
    tests = [
        ("丙里", "甲=小明 乙=苹果 丙=书包"),
        ("戊处", "甲=妈妈 乙=水 戊=老师"),
        ("丙上", "甲=小红 乙=书 丙=桌子"),
    ]
    for ans, emap in tests:
        cn = translate(ans, emap)
        em = translate_emoji(ans, emap)
        print(f"微语: {ans} → 中文: {cn} → Emoji: {em}")


def story_to_emoji(text: str) -> str:
    """把中文故事变成 emoji 版"""
    result = text
    for cn, em in sorted(EMOJI_ENTITIES.items(), key=lambda x: -len(x[0])):
        result = result.replace(cn, em)
    return result
