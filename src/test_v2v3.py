"""双模型对比 v2 vs v3"""
import json, os
os.chdir(r"D:\minimind")
from transformers import AutoTokenizer
from model.model_minimind import MiniMindForCausalLM
import torch

with open("micro_test_bench.jsonl", encoding="utf-8") as f:
    test = [json.loads(l) for l in f]

for name, path in [("v2","minimind_v2_pure"),("v3","minimind_v3_pure")]:
    m = MiniMindForCausalLM.from_pretrained(path, trust_remote_code=True, torch_dtype=torch.float16)
    t = AutoTokenizer.from_pretrained(path, trust_remote_code=True)
    m.to("cuda"); m.eval()
    
    c = {"simple":[0,0],"medium":[0,0],"hard":[0,0]}
    for d in test:
        diff = d.get("difficulty","simple")
        # MIC
        prompt = d["entity_map"] + "。" + d["mic"]
        msgs = [{'role':'user','content':prompt}]
        text = t.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
        ids = t(text, return_tensors="pt").to("cuda")
        with torch.no_grad():
            out = m.generate(**ids, max_new_tokens=15, temperature=0.1, do_sample=False, pad_token_id=t.eos_token_id)
        ans_mic = t.decode(out[0, ids['input_ids'].shape[1]:], skip_special_tokens=True).strip()
        if d["answer"] in ans_mic: c[diff][0] += 1
        
        # CN
        msgs2 = [{'role':'user','content':d["cn"]}]
        text2 = t.apply_chat_template(msgs2, tokenize=False, add_generation_prompt=True)
        ids2 = t(text2, return_tensors="pt").to("cuda")
        with torch.no_grad():
            out2 = m.generate(**ids2, max_new_tokens=15, temperature=0.1, do_sample=False, pad_token_id=t.eos_token_id)
        ans_cn = t.decode(out2[0, ids2['input_ids'].shape[1]:], skip_special_tokens=True).strip()
        if d["answer"] in ans_cn: c[diff][1] += 1
    
    s,m,h = c["simple"],c["medium"],c["hard"]
    tot_mic = s[0]+m[0]+h[0]; tot_cn = s[1]+m[1]+h[1]
    print(f"{name}: MIC={tot_mic} CN={tot_cn} | Smic:{s[0]} M:{m[0]} H:{h[0]} | Scn:{s[1]} M:{m[1]} H:{h[1]}")
    with open(f"bench_{name}.json","w",encoding="utf-8") as f:
        json.dump(c,f,ensure_ascii=False)
print("DONE")
