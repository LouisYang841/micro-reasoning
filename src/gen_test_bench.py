#!/usr/bin/env python3
"""固定测试集: 300题, 分单跳/多跳/转移"""
import json, random

POOL = {
    "人": ["小明","小红","妈妈","爸爸","老师","同学","弟弟","姐姐","老板","邻居"],
    "食": ["苹果","饭","水","面包","牛奶","糖","饼干","面条","蛋糕","茶"],
    "容": ["书包","盒子","冰箱","抽屉","杯子","碗","袋子","篮子","锅","柜子"],
    "场": ["桌子","床","房间","学校","家","车","地上","沙发","厨房","阳台","公园","路边"],
    "物": ["钥匙","书","手机","球","笔","衣服","帽子","花","遥控器","伞","眼镜","钱包"],
}
def p(c,n=1): return random.sample(POOL[c],min(n,len(POOL[c])))
def ents(d): return " ".join([f"{k}={v}" for k,v in d.items()])

# 简单 (100题): 单次放入/放置, 无干扰
SIMPLE = []
for _ in range(100):
    a,b,c=p("人")[0],p("物")[0],p("容")[0]
    SIMPLE.append(dict(cn=f"{a}把{b}放进{c}。{b}在哪？",mic="甲置乙入丙。乙安？",answer=f"{c}里",entity_map=ents({"甲":a,"乙":b,"丙":c}),difficulty="simple"))

# 中等 (100题): 有中间动作, 2-3步
MEDIUM = []
for _ in range(100):
    a,b,c,d=p("人")[0],p("物")[0],p("容")[0],p("场")[0]
    tpl = random.choice([
        (f"{a}把{b}放进{c}，然后去{d}。{b}在哪？", "甲置乙入丙，乃往丁。归，乙安？", f"{c}里"),
        (f"{a}吃了{b}，把剩下的放进{c}。{b}在哪？", "甲啖乙，置余入丙。乙安？", f"{c}里"),
        (f"{a}从{c}里取出{b}放在{d}上。{b}在哪？", "甲自丙取乙，置丁上。乙安？", f"{d}上"),
        (f"{a}把{c}里的{b}倒了出来。{b}在哪？", "甲倾丙，乙出。乙安？", f"{c}旁"),
    ])
    MEDIUM.append(dict(cn=tpl[0],mic=tpl[1],answer=tpl[2],entity_map=ents({"甲":a,"乙":b,"丙":c,"丁":d}),difficulty="medium"))

# 困难 (100题): 人物转移/多跳/嵌套
HARD = []
for _ in range(100):
    a,b=p("人")[0],p("物")[0]
    c,d=p("人")[0],p("人")[0] if random.random()>0.5 else (p("场")[0],p("人")[0])
    tpl = random.choice([
        (f"{a}把{b}给了{d}。{b}在哪？", "甲取乙与戊。乙安？", f"{d}处"),
        (f"{a}和{d}交换了{b}和{c}的东西。{b}在哪？", "甲与戊易乙与丁。乙安？", f"{d}处"),
        (f"{a}把{b}放进箱子里，又把箱子放进柜子。{b}在哪？", "甲置乙入丙，复置丙入丁。乙安？", f"箱子里"),
        (f"{a}本来想把{b}放进抽屉，结果放错放进柜子。{b}在哪？", "甲本欲置乙入丙，误入丁。乙安？", f"柜子里"),
    ])
    HARD.append(dict(cn=tpl[0],mic=tpl[1],answer=tpl[2],entity_map=ents({"甲":a,"乙":b,"戊":c if isinstance(c,str) else d}),difficulty="hard"))

all_test = SIMPLE + MEDIUM + HARD
random.seed(42); random.shuffle(all_test)

with open("micro_test_bench.jsonl","w",encoding="utf-8") as f:
    for d in all_test: f.write(json.dumps(d,ensure_ascii=False)+"\n")
s,m,h = len(SIMPLE), len(MEDIUM), len(HARD)
print(f"固定测试集: {len(all_test)} 题 (简单{s} 中等{m} 困难{h})")
