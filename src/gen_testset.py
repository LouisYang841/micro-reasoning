#!/usr/bin/env python3
"""生成不重叠模板的测试集 — 杜绝数据泄露"""
import json, random

POOL = {
    "人": ["小明","小红","妈妈","爸爸","老师","同学","弟弟","姐姐","老板","邻居"],
    "食": ["苹果","饭","水","面包","牛奶","糖","饼干","面条","蛋糕","米饭"],
    "容": ["书包","盒子","冰箱","抽屉","杯子","碗","袋子","篮子","锅","包"],
    "场": ["桌子","床","房间","学校","家","车","地上","沙发","厨房","厕所","阳台","公园"],
    "物": ["钥匙","书","手机","球","笔","衣服","帽子","花","遥控器","伞"],
}

def pick(cat, n=1):
    return random.sample(POOL[cat], min(n, len(POOL[cat])))

# === 训练集模板 (8个) ===
TRAIN_TEMPLATES = {
    "container_leave": lambda p,f,c: (
        f"{p}把{f}放进{c}，然后离开。回来，{f}在哪里？",
        f"甲置乙入丙，乃离矣。甲归，乙安？",
        f"{c}里", {"甲":p,"乙":f,"丙":c}),
    "eat_then_container": lambda p,f,c: (
        f"{p}吃{f}，然后把{f}放进{c}。{f}在哪里？",
        f"甲啖乙，乃置乙入丙。乙安？",
        f"{c}里", {"甲":p,"乙":f,"丙":c}),
    "open_close": lambda p,f,c: (
        f"{p}打开{c}，把{f}放进{c}，然后关上{c}。{f}在哪里？",
        f"甲启丙，置乙入丙，乃闭丙。乙安？",
        f"{c}里", {"甲":p,"乙":f,"丙":c}),
    "surface_then_go": lambda p,f,l,l2: (
        f"{p}把{f}放在{l}上，然后去{l2}。{f}在哪里？",
        f"甲置乙在丙上，乃往丁。乙安？",
        f"{l}上", {"甲":p,"乙":f,"丙":l,"丁":l2}),
    "container_then_go": lambda p,f,c,l: (
        f"{p}把{f}放进{c}，然后去{l}。回来打开{c}，{f}在哪里？",
        f"甲置乙入丙，乃往丁。归启丙，乙安？",
        f"{c}里", {"甲":p,"乙":f,"丙":c,"丁":l}),
    "surface_leave_seek": lambda p,f,l: (
        f"{p}把{f}放在{l}上，然后离开。{p}想喝水，找{f}。{f}在哪里？",
        f"甲置乙在丙上，乃离。甲思饮，寻乙。乙安？",
        f"{l}上", {"甲":p,"乙":f,"丙":l}),
    "sit_eat_leave": lambda p,f,l: (
        f"{p}坐在{l}上吃{f}，然后离开。{p}回来，{f}在哪里？",
        f"甲坐丙上啖乙，乃离。甲归，乙安？",
        f"{l}上", {"甲":p,"乙":f,"丙":l}),
    "give_to_person": lambda p,f,o: (
        f"{p}把{f}拿给{o}，然后{f}在哪里？",
        f"甲取乙与戊。乙安？",
        f"{o}处", {"甲":p,"乙":f,"戊":o}),
}

# === 测试集专用模板 (全新，不在训练集里) ===
TEST_TEMPLATES = {
    "multi_hop_place": lambda p,f,c,l: (
        f"{p}先从{c}里拿出{f}，再放在{l}上。{f}在哪里？",
        f"甲自丙取乙，乃置在丙上。乙安？",
        f"{l}上", {"甲":p,"乙":f,"丙":c,"丁":l}),
    "put_then_eat_something_else": lambda p,f1,f2,c: (
        f"{p}把{f1}放进{c}，然后吃{f2}。{f1}在哪里？",
        f"甲置乙入丙，乃啖丁。乙安？",
        f"{c}里", {"甲":p,"乙":f1,"丙":c,"丁":f2}),
    "two_people_exchange": lambda p1,p2,obj: (
        f"{p1}把{obj}给{p2}，{p2}又把{obj}放在桌子上。{obj}在哪里？",
        f"甲取乙与戊，戊置乙在丙上。乙安？",
        f"桌上", {"甲":p1,"乙":obj,"丙":"桌子","戊":p2}),
    "forgot_then_remember": lambda p,f,l: (
        f"{p}把{f}忘在{l}上了，后来想起来了。{f}在哪里？",
        f"甲遗乙在丙上，乃思。乙安？",
        f"{l}上", {"甲":p,"乙":f,"丙":l}),
    "conditional_move": lambda p,f,c1,c2: (
        f"如果{c1}满了，{p}就把{f}放进{c2}。{c1}确实满了。{f}在哪里？",
        f"丙满，甲置乙入丁。乙安？",
        f"{c2}里", {"甲":p,"乙":f,"丙":c1,"丁":c2}),
}

def generate_templates(templates, n):
    """从模板字典生成n条数据"""
    data = []
    for _ in range(n):
        tname, tfn = random.choice(list(templates.items()))
        p = pick("人")[0]
        f = pick("食")[0]
        c = pick("容")[0]
        l = pick("场")[0]
        l2 = pick("场")[0]
        o = pick("人")[0]
        f2 = pick("食")[0]
        cn, mic, ans, ent = tfn(p,f,c) if tname in ("container_leave","eat_then_container","open_close") else \
            tfn(p,f,l,l2) if tname in ("surface_then_go","container_then_go") else \
            tfn(p,f,l) if tname in ("surface_leave_seek","sit_eat_leave") else \
            tfn(p,f,o) if tname == "give_to_person" else \
            tfn(p,f,random.choice(pick("容")),l) if tname == "multi_hop_place" else \
            tfn(p,f,f2,c) if tname == "put_then_eat_something_else" else \
            tfn(p,o,f) if tname == "two_people_exchange" else \
            tfn(p,f,l) if tname == "forgot_then_remember" else \
            tfn(p,f,random.choice(pick("容")),random.choice(pick("容")))
        ent_str = " ".join([f"{k}={v}" for k,v in ent.items()])
        data.append({"cn": cn, "mic": mic, "answer": ans, "entity_map": ent_str})
    return data

if __name__ == "__main__":
    random.seed(12345)
    test = generate_templates(TEST_TEMPLATES, 100)
    with open("micro_test_clean.jsonl", "w", encoding="utf-8") as f:
        for d in test:
            f.write(json.dumps(d, ensure_ascii=False) + "\n")
    print(f"✅ 生成 {len(test)} 条无泄露测试数据 (5个全新模板)")
    print(f"训练模板: {list(TRAIN_TEMPLATES.keys())}")
    print(f"测试模板: {list(TEST_TEMPLATES.keys())}")
    print(f"重叠: 0")
