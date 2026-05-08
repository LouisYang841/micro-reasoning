#!/usr/bin/env python3
"""MiniMind 微语训练 - Windows 4060 CUDA 版，全量参数"""
import json, random, torch
from transformers import AutoTokenizer
from model.model_minimind import MiniMindForCausalLM
import os, sys

sys.path.insert(0, os.path.dirname(__file__))
from micro_lang import *

MODEL = "jingyaogong/minimind-3"
EPOCHS = 5
BATCH = 4
LR = 2e-5
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

print(f"Device: {DEVICE} | GPU: {torch.cuda.get_device_name(0) if DEVICE=='cuda' else 'CPU'}")
print(f"VRAM: {torch.cuda.get_device_properties(0).total_memory/1e9:.1f}GB")

print("加载模型...")
tokenizer = AutoTokenizer.from_pretrained(MODEL, trust_remote_code=True)
if tokenizer.pad_token is None: tokenizer.pad_token = tokenizer.eos_token
model = MiniMindForCausalLM.from_pretrained(MODEL, trust_remote_code=True, torch_dtype=torch.float32)
model.to(DEVICE)
model.train()

# 全量训练
tp = sum(p.numel() for p in model.parameters())
print(f"参数: {tp/1e6:.1f}M (全量训练)")

# 加载数据
import os
os.chdir(r"D:\minimind")
with open("micro_train.jsonl", encoding="utf-8") as f:
    raw = [json.loads(l) for l in f]

data = []
for d in raw:
    p = f"{d['entity_map']}。{d['mic']}"
    a = d['answer']
    ids = tokenizer(p + a, truncation=True, max_length=80, return_tensors="pt")["input_ids"][0]
    data.append(ids)

# 90/10 split
split = int(len(data) * 0.9)
train_data, val_data = data[:split], data[split:]
print(f"训练: {len(train_data)} | 验证: {len(val_data)}")

opt = torch.optim.AdamW(model.parameters(), lr=LR)

def collate(batch):
    ml = max(len(b) for b in batch)
    ids = torch.stack([torch.nn.functional.pad(b, (0, ml - len(b)), value=tokenizer.pad_token_id) for b in batch])
    return ids.to(DEVICE)

for epoch in range(EPOCHS):
    random.shuffle(train_data)
    tl = 0
    for i in range(0, len(train_data), BATCH):
        batch = train_data[i:i+BATCH]
        ids = collate(batch)
        labels = ids.clone()
        out = model(input_ids=ids, labels=labels)
        loss = out.loss
        opt.zero_grad()
        loss.backward()
        opt.step()
        tl += loss.item()
        if i % 50 == 0:
            print(f"  E{epoch+1} S{i}/{len(train_data)} loss={loss.item():.4f}")
    
    # 验证
    model.eval()
    vl = 0
    with torch.no_grad():
        for i in range(0, len(val_data), BATCH):
            batch = val_data[i:i+BATCH]
            ids = collate(batch)
            out = model(input_ids=ids, labels=ids.clone())
            vl += out.loss.item()
    model.train()
    
    print(f"[OK] Epoch {epoch+1} | train={tl/(len(train_data)/BATCH):.4f} val={vl/(len(val_data)/BATCH):.4f}")

model.save_pretrained("minimind_micro_cuda")
tokenizer.save_pretrained("minimind_micro_cuda")
print("[OK] 保存完成！")
