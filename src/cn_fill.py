"""补测CN: v4_20x50, v4_35x50, v3_fixed"""
import json, os, torch
os.chdir(r"D:\minimind")
from transformers import AutoTokenizer
from model.model_minimind import MiniMindForCausalLM

with open("micro_test_bench.jsonl", encoding="utf-8") as f:
    test = [json.loads(l) for l in f]

for name in ["v4_20x50","v4_35x50","v3_fixed"]:
    m = MiniMindForCausalLM.from_pretrained(f"minimind_{name}", trust_remote_code=True, torch_dtype=torch.float16)
    t = AutoTokenizer.from_pretrained(f"minimind_{name}", trust_remote_code=True)
    m.to("cuda"); m.eval()
    c = {"simple":0,"medium":0,"hard":0}
    for d in test:
        ids = t(t.apply_chat_template([{'role':'user','content':d["cn"]}], tokenize=False, add_generation_prompt=True), return_tensors="pt").to("cuda")
        out = m.generate(**ids, max_new_tokens=15, temperature=0.1, do_sample=False, pad_token_id=t.eos_token_id)
        if d["answer"] in t.decode(out[0, ids['input_ids'].shape[1]:], skip_special_tokens=True).strip():
            c[d.get("difficulty","simple")] += 1
    tot = sum(c.values())
    print(f"{name} CN: {tot} | S:{c['simple']} M:{c['medium']} H:{c['hard']}")
