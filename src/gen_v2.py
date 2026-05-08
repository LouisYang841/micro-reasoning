#!/usr/bin/env python3
"""扩增训练模板 — 8→20 模板, 2000条数据"""
import json, random

POOL = {
    "人": ["小明","小红","妈妈","爸爸","老师","同学","弟弟","姐姐","老板","邻居"],
    "食": ["苹果","饭","水","面包","牛奶","糖","饼干","面条","蛋糕","米饭"],
    "容": ["书包","盒子","冰箱","抽屉","杯子","碗","袋子","篮子","锅","包"],
    "场": ["桌子","床","房间","学校","家","车","地上","沙发","厨房","厕所","阳台","公园"],
    "物": ["钥匙","书","手机","球","笔","衣服","帽子","花","遥控器","伞","玩具"],
}

def p(c, n=1): return random.sample(POOL[c], min(n, len(POOL[c])))

TEMPLATES = {}

# === 基础模板 (原8个 + 新12个) ===

def t1():  # container_leave
    a,b,c=p("人")[0],p("人")[0],p("人")[0];d=p("食")[0];e=p("容")[0]
    return (f"{a}把{d}放进{e}，然后离开。回来，{d}在哪里？",
            f"甲置乙入丙，乃离矣。甲归，乙安？", f"{e}里", {"甲":a,"乙":d,"丙":e})
TEMPLATES["container_leave"] = t1

def t2():  # eat_then_container
    a=p("人");c=p("食");d=p("容")
    return (f"{a}吃{c}，然后把{c}放进{d}。{c}在哪里？",
            f"甲啖乙，乃置乙入丙。乙安？", f"{d}里", {"甲":a,"乙":c,"丙":d})
TEMPLATES["eat_then_container"] = t2

def t3():  # open_close
    a=p("人");c=p("食");d=p("容")
    return (f"{a}打开{d}，把{c}放进{d}，然后关上{d}。{c}在哪里？",
            f"甲启丙，置乙入丙，乃闭丙。乙安？", f"{d}里", {"甲":a,"乙":c,"丙":d})
TEMPLATES["open_close"] = t3

def t4():  # surface_then_go
    a=p("人")[0];c=p("食")[0];d,e=p("场",2)
    return (f"{a}把{c}放在{d}上，然后去{e}。{c}在哪里？",
            f"甲置乙在丙上，乃往丁。乙安？", f"{d}上", {"甲":a,"乙":c,"丙":d,"丁":e})
TEMPLATES["surface_then_go"] = t4

def t5():  # container_then_go
    a=p("人");c=p("食");d=p("容");e=p("场")
    return (f"{a}把{c}放进{d}，然后去{e}。回来打开{d}，{c}在哪里？",
            f"甲置乙入丙，乃往丁。归启丙，乙安？", f"{d}里", {"甲":a,"乙":c,"丙":d,"丁":e})
TEMPLATES["container_then_go"] = t5

def t6():  # surface_leave_seek
    a=p("人");c=p("食");d=p("场")
    return (f"{a}把{c}放在{d}上，然后离开。{a}想喝{c}，找{c}。{c}在哪里？",
            f"甲置乙在丙上，乃离。甲思饮，寻乙。乙安？", f"{d}上", {"甲":a,"乙":c,"丙":d})
TEMPLATES["surface_leave_seek"] = t6

def t7():  # sit_eat_leave
    a=p("人");c=p("食");d=p("场")
    return (f"{a}坐在{d}上吃{c}，然后离开。{a}回来，{c}在哪里？",
            f"甲坐丙上啖乙，乃离。甲归，乙安？", f"{d}上", {"甲":a,"乙":c,"丙":d})
TEMPLATES["sit_eat_leave"] = t7

def t8():  # give_to_person
    a,b,c=p("人",3)
    return (f"{a}把{random.choice(p('物'))}拿给{c}，然后这件东西在哪里？",
            f"甲取物与戊。物安？", f"{c}处", {"甲":a,"戊":c})
TEMPLATES["give_to_person"] = t8

# === 新模板 (12个) ===

def t9():  # take_from_container
    a=p("人");c=p("食");d=p("容");e=p("场")
    return (f"{a}从{d}里取出{c}，放在{e}上。{c}在哪里？",
            f"甲自丙取乙，置在丁上。乙安？", f"{e}上", {"甲":a,"乙":c,"丙":d,"丁":e})
TEMPLATES["take_from_container"] = t9

def t10():  # two_items
    a=p("人");c,d=p("食",2);e=p("容")
    return (f"{a}先把{c}放进{e}，然后把{d}也放进{e}。{c}在哪里？",
            f"甲先置乙入丙，乃置丁入丙。乙安？", f"{e}里", {"甲":a,"乙":c,"丙":e,"丁":d})
TEMPLATES["two_items"] = t10

def t11():  # eat_partial
    a=p("人");c=p("食");d=p("容")
    return (f"{a}吃了一部分{c}，然后把剩下的{c}放进{d}。{c}在哪里？",
            f"甲啖乙半，乃置余入丙。乙安？", f"{d}里", {"甲":a,"乙":c,"丙":d})
TEMPLATES["eat_partial"] = t11

def t12():  # move_between_containers
    a=p("人");c=p("食");d,e=p("容",2)
    return (f"{a}把{c}从{d}里移到{e}里。{c}在哪里？",
            f"甲移乙自丙入丁。乙安？", f"{e}里", {"甲":a,"乙":c,"丙":d,"丁":e})
TEMPLATES["move_between"] = t12

def t13():  # put_on_multiple
    a=p("人");c=p("物");d,e=p("场",2)
    return (f"{a}把{c}先放在{d}上，想了想又放到{e}上。{c}在哪里？",
            f"甲初置乙在丙上，乃改置在丁上。乙安？", f"{e}上", {"甲":a,"乙":c,"丙":d,"丁":e})
TEMPLATES["put_on_multiple"] = t13

def t14():  # look_for_missing
    a=p("人");c=p("物");d=p("场")
    return (f"{a}找不到{c}了，翻遍了{d}，最后在{d}上找到了。{c}在哪里？",
            f"甲寻乙无果，觅得丙上有乙。乙安？", f"{d}上", {"甲":a,"乙":c,"丙":d})
TEMPLATES["look_for_missing"] = t14

def t15():  # give_then_put
    a,b,c=p("人",3);d=p("物");e=p("场")
    return (f"{a}把{d}给{c}，{c}把{d}放在了{e}上。{d}在哪里？",
            f"甲取乙与戊，戊置乙在丙上。乙安？", f"{e}上", {"甲":a,"乙":d,"丙":e,"戊":c})
TEMPLATES["give_then_put"] = t15

def t16():  # conditional
    a=p("人");c=p("食");d,e=p("容",2)
    return (f"{d}满了，{a}就把{c}放进了{e}。{c}在哪里？",
            f"丙满，甲置乙入丁。乙安？", f"{e}里", {"甲":a,"乙":c,"丙":d,"丁":e})
TEMPLATES["conditional"] = t16

def t17():  # negate
    a=p("人");c=p("食");d=p("容");e=p("场")
    return (f"{a}没有把{c}放进{d}，而是放在了{e}上。{c}在哪里？",
            f"甲非置乙入丙，乃置在丁上。乙安？", f"{e}上", {"甲":a,"乙":c,"丙":d,"丁":e})
TEMPLATES["negate"] = t17

def t18():  # sequential_actions
    a=p("人");c,d=p("食",2);e=p("容");f=p("场")
    return (f"{a}先吃{c}，然后把{d}放进{e}，最后去{f}。{d}在哪里？",
            f"甲先啖乙，乃置丙入丁，末往戊。丙安？", f"{e}里", {"甲":a,"乙":c,"丙":d,"丁":e,"戊":f})
TEMPLATES["sequential"] = t18

def t19():  # put_inside_something_inside
    a=p("人");c=p("食");d=p("容");e=p("容")
    return (f"{a}把{c}放进{d}，然后把{d}放进{e}。{c}在哪里？",
            f"甲置乙入丙，乃置丙入丁。乙安？", f"{d}里", {"甲":a,"乙":c,"丙":d,"丁":e})
TEMPLATES["nested"] = t19

def t20():  # forget_location
    a=p("人");c=p("物");d=p("场")
    return (f"{a}把{c}忘在{d}上了。后来想起来，{c}还在那里。{c}在哪里？",
            f"甲遗乙在丙上，后忆及。乙安？", f"{d}上", {"甲":a,"乙":c,"丙":d})
TEMPLATES["forget"] = t20

# === 生成 ===
def generate(n=2000, seed=42):
    random.seed(seed)
    data = []
    for _ in range(n):
        name, fn = random.choice(list(TEMPLATES.items()))
        cn, mic, ans, ent = fn()
        ent_str = " ".join([f"{k}={v}" for k,v in ent.items()])
        data.append({"cn":cn, "mic":mic, "answer":ans, "entity_map":ent_str})
    return data

if __name__ == "__main__":
    D = generate(2000)
    with open("micro_train_v2.jsonl", "w", encoding="utf-8") as f:
        for d in D: f.write(json.dumps(d, ensure_ascii=False)+"\n")
    print(f"✅ 生成 {len(D)} 条 (20个模板)")
    print(f"模板: {list(TEMPLATES.keys())}")
