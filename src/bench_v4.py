import json, os, torch
os.chdir(r"D:\minimind")
from transformers import AutoTokenizer
from model.model_minimind import MiniMindForCausalLM

for name in ["v4_20x50","v4_35x50"]:
    m = MiniMindForCausalLM.from_pretrained(f"minimind_{name}", trust_remote_code=True, torch_dtype=torch.float16)
    t = AutoTokenizer.from_pretrained(f"minimind_{name}", trust_remote_code=True)
    m.to("cuda"); m.eval()
    with open("micro_test_bench.jsonl", encoding="utf-8") as f:
        test = [json.loads(l) for l in f]
    c = {"simple":[0,0],"medium":[0,0],"hard":[0,0]}
    for d in test:
        diff = d.get("difficulty","simple")
        ids = t(t.apply_chat_template([{'role':'user','content':d["entity_map"]+"。"+d["mic"]}], tokenize=False, add_generation_prompt=True), return_tensors="pt").to("cuda")
        out = m.generate(**ids, max_new_tokens=15, temperature=0.1, do_sample=False, pad_token_id=t.eos_token_id)
        if d["answer"] in t.decode(out[0, ids['input_ids'].shape[1]:], skip_special_tokens=True).strip(): c[diff][0] += 1
        ids = t(t.apply_chat_template([{'role':'user','content':d["cn"]}], tokenize=False, add_generation_prompt=True), return_tensors="pt").to("cuda")
        out = m.generate(**ids, max_new_tokens=15, temperature=0.1, do_sample=False, pad_token_id=t.eos_token_id)
        if d["answer"] in t.decode(out[0, ids['input_ids'].shape[1]:], skip_special_tokens=True).strip(): c[diff][1] += 1
    s,m,h = c["simple"],c["medium"],c["hard"]
    print(f"{name}: MIC={s[0]+m[0]+h[0]} CN={s[1]+m[1]+h[1]} | S:{s[0]}/{s[1]} M:{m[0]}/{m[1]} H:{h[0]}/{h[1]}")
