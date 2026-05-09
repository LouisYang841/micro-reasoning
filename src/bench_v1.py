import json, os, torch
os.chdir(r"D:\minimind")
from transformers import AutoTokenizer
from model.model_minimind import MiniMindForCausalLM

m = MiniMindForCausalLM.from_pretrained("minimind_pure_micro", trust_remote_code=True, torch_dtype=torch.float16)
t = AutoTokenizer.from_pretrained("minimind_pure_micro", trust_remote_code=True)
m.to("cuda"); m.eval()

with open("micro_test_bench.jsonl", encoding="utf-8") as f:
    test = [json.loads(l) for l in f]

c = {"simple":[0,0],"medium":[0,0],"hard":[0,0]}
for d in test:
    diff = d.get("difficulty","simple")
    p1 = d["entity_map"]+"。"+d["mic"]
    ids1 = t(t.apply_chat_template([{'role':'user','content':p1}], tokenize=False, add_generation_prompt=True), return_tensors="pt").to("cuda")
    out1 = m.generate(**ids1, max_new_tokens=15, temperature=0.1, do_sample=False, pad_token_id=t.eos_token_id)
    if d["answer"] in t.decode(out1[0, ids1['input_ids'].shape[1]:], skip_special_tokens=True).strip(): c[diff][0] += 1
    p2 = d["cn"]
    ids2 = t(t.apply_chat_template([{'role':'user','content':p2}], tokenize=False, add_generation_prompt=True), return_tensors="pt").to("cuda")
    out2 = m.generate(**ids2, max_new_tokens=15, temperature=0.1, do_sample=False, pad_token_id=t.eos_token_id)
    if d["answer"] in t.decode(out2[0, ids2['input_ids'].shape[1]:], skip_special_tokens=True).strip(): c[diff][1] += 1

s,m,h = c["simple"],c["medium"],c["hard"]
tot_mic = s[0]+m[0]+h[0]; tot_cn = s[1]+m[1]+h[1]
open("bench_v1.json","w",encoding="utf-8").write(json.dumps({"MIC":tot_mic,"CN":tot_cn,"S":[s[0],s[1]],"M":[m[0],m[1]],"H":[h[0],h[1]]},ensure_ascii=False))
print(f"v1: MIC={tot_mic} CN={tot_cn} | S:{s[0]}/{s[1]} M:{m[0]}/{m[1]} H:{h[0]}/{h[1]}")
