"""翻译模型训练 — 微语→中文，双向映射"""
import json, random, os
os.chdir(r"D:\minimind")
from transformers import AutoTokenizer
from model.model_minimind import MiniMindForCausalLM
import torch

DEVICE = "cuda"
BATCH, LR, EPOCHS = 8, 2e-5, 5

model = MiniMindForCausalLM.from_pretrained("jingyaogong/minimind-3", trust_remote_code=True, torch_dtype=torch.float32)
tokenizer = AutoTokenizer.from_pretrained("jingyaogong/minimind-3", trust_remote_code=True)
if tokenizer.pad_token is None: tokenizer.pad_token = tokenizer.eos_token
model.to(DEVICE); model.train()

# 双向翻译数据: 微→中 + 中→微
with open("micro_train.jsonl", encoding="utf-8") as f:
    raw = [json.loads(l) for l in f]

data = []
for d in raw:
    # 微→中: 微语输入, 中文输出 (用明显分隔)
    mic2cn_in = f"{d['entity_map']}\n微语: {d['mic']}\n中文: "
    mic2cn_out = d['cn']
    data.append((mic2cn_in, mic2cn_out))
    # 中→微
    cn2mic_in = f"{d['entity_map']}\n中文: {d['cn']}\n微语: "
    cn2mic_out = d['mic']
    data.append((cn2mic_in, cn2mic_out))

split = int(len(data) * 0.9)
train_d, val_d = data[:split], data[split:]
print(f"翻译训练: {len(train_d)}/{len(val_d)} (双向共{len(data)}条)")

opt = torch.optim.AdamW(model.parameters(), lr=LR)

def c(batch):
    texts = [f"{inp}{out}" for inp, out in batch]
    enc = tokenizer(texts, truncation=True, max_length=120, padding=True, return_tensors="pt")
    return enc["input_ids"].to(DEVICE), enc["attention_mask"].to(DEVICE)

for ep in range(EPOCHS):
    random.shuffle(train_d); tl = 0
    for i in range(0, len(train_d), BATCH):
        batch = train_d[i:i+BATCH]
        ids, mask = c(batch)
        out = model(input_ids=ids, attention_mask=mask, labels=ids.clone())
        opt.zero_grad(); out.loss.backward(); opt.step()
        tl += out.loss.item()
        if i % 100 == 0: print(f"  E{ep+1} S{i}/{len(train_d)} loss={out.loss.item():.4f}")
    
    model.eval(); vl = 0
    with torch.no_grad():
        for i in range(0, len(val_d), BATCH):
            ids, mask = c(val_d[i:i+BATCH])
            vl += model(input_ids=ids, labels=ids.clone()).loss.item()
    model.train()
    print(f"[OK] E{ep+1} train={tl/(len(train_d)/BATCH):.4f} val={vl/(len(val_d)/BATCH):.4f}")

model.save_pretrained("minimind_translator")
tokenizer.save_pretrained("minimind_translator")
print("[OK] 翻译模型完成")
