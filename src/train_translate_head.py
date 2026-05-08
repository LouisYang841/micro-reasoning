"""v2 微语 → 中文翻译头 — 薄翻译层训练"""
import json, random, os
os.chdir(r"D:\minimind")
from transformers import AutoTokenizer
from model.model_minimind import MiniMindForCausalLM
import torch

DEVICE, BATCH, LR, EPOCHS = "cuda", 4, 1e-5, 2  # 只训2 epoch，低LR

# 加载 v2 纯微语模型
model = MiniMindForCausalLM.from_pretrained("minimind_v2_pure", trust_remote_code=True, torch_dtype=torch.float32)
tok = AutoTokenizer.from_pretrained("minimind_v2_pure", trust_remote_code=True)
if tok.pad_token is None: tok.pad_token = tok.eos_token

# 只训最后两层 FFN + lm_head（保护微语推理层）
for name, param in model.named_parameters():
    if "lm_head" in name:
        param.requires_grad = True
    elif "layers" in name:
        parts = name.split(".")
        layer_num = int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else -1
        if layer_num >= 6:  # 只训顶层
            param.requires_grad = True
        else:
            param.requires_grad = False
    else:
        param.requires_grad = False

tp = sum(p.numel() for p in model.parameters())
tr = sum(p.numel() for p in model.parameters() if p.requires_grad)
print(f"翻译头参数: {tr/1e6:.1f}M / {tp/1e6:.1f}M")

model.to(DEVICE); model.train()

# 翻译数据: 微语→中文
with open("micro_train_v2.jsonl", encoding="utf-8") as f:
    raw = [json.loads(l) for l in f]

data = []
for d in raw:
    inp = f"{d['entity_map']}。微语: {d['mic']}\n中文:"
    out = d['cn']
    ids = tok(inp + out, truncation=True, max_length=120, return_tensors="pt")["input_ids"][0]
    data.append(ids)

split = int(len(data) * 0.9)
train_d, val_d = data[:split], data[split:]
print(f"翻译训练: {len(train_d)}/{len(val_d)}")

opt = torch.optim.AdamW(filter(lambda p: p.requires_grad, model.parameters()), lr=LR)
def c(b): ml=max(len(x) for x in b); return torch.stack([torch.nn.functional.pad(x,(0,ml-len(x)),value=tok.pad_token_id) for x in b]).to(DEVICE)

for ep in range(EPOCHS):
    random.shuffle(train_d); tl=0
    for i in range(0,len(train_d),BATCH):
        batch=train_d[i:i+BATCH]; ids=c(batch)
        out=model(input_ids=ids,labels=ids.clone())
        opt.zero_grad(); out.loss.backward(); opt.step()
        tl+=out.loss.item()
        if i%200==0: print(f"  E{ep+1} S{i} loss={out.loss.item():.4f}")
    model.eval(); vl=0
    with torch.no_grad():
        for i in range(0,len(val_d),BATCH):
            ids=c(val_d[i:i+BATCH])
            vl+=model(input_ids=ids,labels=ids.clone()).loss.item()
    model.train()
    print(f"[OK] E{ep+1} train={tl/(len(train_d)/BATCH):.4f} val={vl/(len(val_d)/BATCH):.4f}")

model.save_pretrained("minimind_v2_translate"); tok.save_pretrained("minimind_v2_translate")
print("[OK] 翻译头完成")
