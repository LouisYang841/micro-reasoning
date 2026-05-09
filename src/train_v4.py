import json, random, os, torch
os.chdir(r"D:\minimind")
from transformers import AutoTokenizer
from model.model_minimind import MiniMindForCausalLM

for name in ["v4_20x50","v4_35x50"]:
    model = MiniMindForCausalLM.from_pretrained("jingyaogong/minimind-3", trust_remote_code=True, torch_dtype=torch.float32)
    tok = AutoTokenizer.from_pretrained("jingyaogong/minimind-3", trust_remote_code=True)
    if tok.pad_token is None: tok.pad_token = tok.eos_token
    model.to("cuda"); model.train()
    with open(f"micro_train_{name}.jsonl", encoding="utf-8") as f:
        raw = [json.loads(l) for l in f]
    data = [tok(f"{d['entity_map']}。{d['mic']}{d['answer']}", truncation=True, max_length=80, return_tensors="pt")["input_ids"][0] for d in raw]
    split = int(len(data)*0.9); td, vd = data[:split], data[split:]
    print(f"{name}: {len(td)}/{len(vd)}")
    opt = torch.optim.AdamW(model.parameters(), lr=2e-5); B=2
    def c(b): ml=max(len(x) for x in b); return torch.stack([torch.nn.functional.pad(x,(0,ml-len(x)),value=tok.pad_token_id) for x in b]).to("cuda")
    for ep in range(5):
        random.shuffle(td); tl=0
        for i in range(0,len(td),B):
            ids=c(td[i:i+B]); out=model(input_ids=ids,labels=ids.clone())
            opt.zero_grad(); out.loss.backward(); opt.step(); tl+=out.loss.item()
            if i%300==0: print(f"  E{ep+1} S{i}")
        model.eval(); vl=0
        with torch.no_grad():
            for i in range(0,len(vd),B): ids=c(vd[i:i+B]); vl+=model(input_ids=ids,labels=ids.clone()).loss.item()
        model.train()
        print(f"E{ep+1} loss={tl/(len(td)/B):.4f} val={vl/(len(vd)/B):.4f}")
    model.save_pretrained(f"minimind_{name}"); tok.save_pretrained(f"minimind_{name}")
    print(f"{name} DONE")
