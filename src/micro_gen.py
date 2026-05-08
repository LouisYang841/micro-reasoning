#!/usr/bin/env python3
"""微型语言语料生成器 v3 final — 变量映射完全正确"""
import random, json

POOL = {
    "人":  ["小明","小红","妈妈","爸爸","老师","同学","弟弟"],
    "食":  ["苹果","饭","水","面包","牛奶","糖","饼干","面条"],
    "容":  ["书包","盒子","冰箱","抽屉","杯子","碗","袋子"],
    "场":  ["桌子","床","房间","学校","家","车","地上","沙发","厨房"],
    "物":  ["钥匙","书","手机","球","笔","衣服","帽子"],
}

def pick(cat, n=1):
    return random.sample(POOL[cat], min(n, len(POOL[cat])))

def story():
    p = pick("人")[0]  # 甲 = 人
    f = pick("食")[0]  # 乙 = 物品
    c = pick("容")[0]  # 丙 = 容器
    l = pick("场")[0]  # 丁 = 位置
    o = pick("人")[0]  # 戊 = 另一人

    T = [
        # --- 三实体: 甲(人) 乙(物品) 丙(容器) ---
        (f"{p}把{f}放进{c}，然后离开。回来，{f}在哪里？",
         f"甲置乙入丙，乃离矣。甲归，乙安？", f"{c}里",
         {"甲":p, "乙":f, "丙":c}),
        (f"{p}吃{f}，然后把{f}放进{c}。{f}在哪里？",
         f"甲啖乙，乃置乙入丙。乙安？", f"{c}里",
         {"甲":p, "乙":f, "丙":c}),
        (f"{p}打开{c}，把{f}放进{c}，然后关上{c}。{f}在哪里？",
         f"甲启丙，置乙入丙，乃闭丙。乙安？", f"{c}里",
         {"甲":p, "乙":f, "丙":c}),
        # --- 四实体: 甲(人) 乙(物品) 丙(位置) 丁(去向) ---
        (f"{p}把{f}放在{l}上，然后去学校。{f}在哪里？",
         f"甲置乙在丙上，乃往丁。乙安？", f"{l}上",
         {"甲":p, "乙":f, "丙":l, "丁":"学校"}),
        (f"{p}把{f}放进{c}，然后去{l}。回来打开{c}，{f}在哪里？",
         f"甲置乙入丙，乃往丁。归启丙，乙安？", f"{c}里",
         {"甲":p, "乙":f, "丙":c, "丁":l}),
        (f"{p}把{f}放在{l}上，然后离开。{p}想喝水，找{f}。{f}在哪里？",
         f"甲置乙在丙上，乃离。甲思饮，寻乙。乙安？", f"{l}上",
         {"甲":p, "乙":f, "丙":l}),
        (f"{p}坐在{l}上吃{f}，然后离开。{p}回来，{f}在哪里？",
         f"甲坐丙上啖乙，乃离。甲归，乙安？", f"{l}上",
         {"甲":p, "乙":f, "丙":l}),
        # --- 五实体: 甲(人) 乙(物品) 丙(位置) 丁(去向) 戊(另一人) ---
        (f"{p}把{f}拿给{o}，然后{f}在哪里？",
         f"甲取乙与戊。乙安？", f"{o}处",
         {"甲":p, "乙":f, "戊":o}),
    ]

    cn, mic, ans, ent = random.choice(T)
    ent_str = " ".join([f"{k}={v}" for k, v in ent.items()])

    return {"cn": cn, "mic": mic, "answer": ans, "entity_map": ent_str}

def generate(n=500, seed=42):
    random.seed(seed)
    return [story() for _ in range(n)]

if __name__ == "__main__":
    for i, s in enumerate(generate(8)):
        print(f"[{i+1}] {s['entity_map']}")
        print(f"    中: {s['cn']}")
        print(f"    微: {s['mic']}")
        print(f"    答: {s['answer']}")
        print()
    
    # 生成完整数据集
    data = generate(500)
    with open("micro_train.jsonl", "w", encoding="utf-8") as f:
        for d in data:
            f.write(json.dumps(d, ensure_ascii=False) + "\n")
    print(f"✅ 已生成 {len(data)} 条训练数据 → micro_train.jsonl")
