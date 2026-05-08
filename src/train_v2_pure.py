"""v2 纯微语训练 — 20模板 2000条"""
import json, random, os
os.chdir(r"D:\minimind")
from transformers import AutoTokenizer
from model.model_minimind import MiniMindForCausalLM
import torch

DEVICE, BATCH, LR, EPOCHS = "cuda", 4, 2e-5, 5

model = MiniMindForCausalLM.from_pretrained("jingyaogong/minimind-3", trust_remote_code=True, torch_dtype=torch.float32)
tok = AutoTokenizer.from_pretrained("jingyaogong/minimind-3", trust_remote_code=True)
if tok.pad_token is None: tok.pad_token = tok.eos_token
model.to(DEVICE); model.train()

with open("micro_train_v2.jsonl", encoding="utf-8") as f:
    raw = [json.loads(l) for l in f]

data = []
for d in raw:
    ids = tok(f"{d['entity_map']}。{d['mic']}{d['answer']}", truncation=True, max_length=80, return_tensors="pt")["input_ids"][0]
    data.append(ids)

split = int(len(data) * 0.9)
train_d, val_d = data[:split], data[split:]
print(f"v2纯微语: {len(train_d)}/{len(val_d)} (20模板)")

opt = torch.optim.AdamW(model.parameters(), lr=LR)
def c(b): ml=max(len(x) for x in b); return torch.stack([torch.nn.functional.pad(x,(0,ml-len(x)),value=tok.pad_token_id) for x in b]).to(DEVICE)

for ep in range(EPOCHS):
    random.shuffle(train_d); tl=0
    for i in range(0,len(train_d),BATCH):
        batch=train_d[i:i+BATCH]; ids=c(batch)
        out=model(input_ids=ids,labels=ids.clone())
        opt.zero_grad(); out.loss.backward(); opt.step()
        tl+=out.loss.item()
        if i%200==0: print(f"  E{ep+1} S{i}/{len(train_d)} loss={out.loss.item():.4f}")
    model.eval(); vl=0
    with torch.no_grad():
        for i in range(0,len(val_d),BATCH):
            ids=c(val_d[i:i+BATCH])
            vl+=model(input_ids=ids,labels=ids.clone()).loss.item()
    model.train()
    print(f"[OK] E{ep+1} train={tl/(len(train_d)/BATCH):.4f} val={vl/(len(val_d)/BATCH):.4f}")

model.save_pretrained("minimind_v2_pure"); tok.save_pretrained("minimind_v2_pure")
print("[OK] v2完成")
