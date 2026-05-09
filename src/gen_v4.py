#!/usr/bin/env python3
"""密度控制: 35×50 + 20×50 — 全用def"""
import json, random
POOL={"人":["小明","小红","妈妈","爸爸","老师","同学","弟弟","姐姐"],"物":["钥匙","书","手机","球","笔","衣服","帽子","花"],"容":["书包","盒子","冰箱","抽屉","杯子","碗","袋子","篮子"],"场":["桌子","床","房间","学校","家","车","地上","沙发","厨房"]}
def p(c,n=1): return random.sample(POOL[c],min(n,len(POOL[c])))
def ents(d): return " ".join([f"{k}={v}" for k,v in d.items()])

def make_story():
    a,b,c,d,e = p("人")[0],p("物")[0],p("容")[0],p("场")[0],p("人")[0]
    pats = [
        (f"{a}把{b}放进{c}。{b}在哪？","甲置乙入丙。乙安？",f"{c}里",{"甲":a,"乙":b,"丙":c}),
        (f"{a}把{b}放在{c}上。{b}在哪？","甲置乙在丙上。乙安？",f"{c}上",{"甲":a,"乙":b,"丙":c}),
        (f"{a}吃了{b}，剩下放进{c}。{b}在哪？","甲啖乙，置余入丙。乙安？",f"{c}里",{"甲":a,"乙":b,"丙":c}),
        (f"{a}打开{c}放进{b}关上。{b}在哪？","甲启丙，置乙入丙，乃闭丙。乙安？",f"{c}里",{"甲":a,"乙":b,"丙":c}),
        (f"{a}把{b}放进{c}去{d}。{b}在哪？","甲置乙入丙，乃往丁。归，乙安？",f"{c}里",{"甲":a,"乙":b,"丙":c,"丁":d}),
        (f"{a}从{c}取{b}放{d}上。{b}在哪？","甲自丙取乙，置丁上。乙安？",f"{d}上",{"甲":a,"乙":b,"丙":c,"丁":d}),
        (f"{a}坐{c}上吃{b}。{b}在哪？","甲坐丙上啖乙。乙安？",f"{c}上",{"甲":a,"乙":b,"丙":c}),
        (f"{a}把{b}给{e}。{b}在哪？","甲取乙与戊。乙安？",f"{e}处",{"甲":a,"乙":b,"戊":e}),
        (f"{a}把{b}给{e}，{e}放{c}里。{b}在哪？","甲取乙与戊，戊置乙入丙。乙安？",f"{c}里",{"甲":a,"乙":b,"丙":c,"戊":e}),
        (f"{c}满了，{a}把{b}放{d}。{b}在哪？","丙满，甲置乙入丁。乙安？",f"{d}里",{"甲":a,"乙":b,"丙":c,"丁":d}),
        (f"{a}没放{c}，放了{d}。{b}在哪？","甲非置乙入丙，乃置乙入丁。乙安？",f"{d}里",{"甲":a,"乙":b,"丙":c,"丁":d}),
        (f"{a}把{b}放{c}里，{c}放{d}里。{b}在哪？","甲置乙入丙，复置丙入丁。乙安？",f"{c}里",{"甲":a,"乙":b,"丙":c,"丁":d}),
    ]
    return random.choice(pats)

def gen(name, n_tmpl, per_tmpl):
    random.seed(42)
    data = []
    for _ in range(n_tmpl * per_tmpl):
        cn, mic, ans, ent = make_story()
        data.append({"cn":cn,"mic":mic,"answer":ans,"entity_map":ents(ent)})
    with open(f"micro_train_{name}.jsonl","w",encoding="utf-8") as f:
        for d in data: f.write(json.dumps(d,ensure_ascii=False)+"\n")
    print(f"{name}: {len(data)}条")

gen("v4_35x50", 35, 50)
gen("v4_20x50", 20, 50)
