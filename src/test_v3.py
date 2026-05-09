"""v3 测试 — 纯微语20模板"""
import json, os
os.chdir(r"D:\minimind")
from transformers import AutoTokenizer
from model.model_minimind import MiniMindForCausalLM
import torch

m = MiniMindForCausalLM.from_pretrained("minimind_v3_pure", trust_remote_code=True, torch_dtype=torch.float16)
t = AutoTokenizer.from_pretrained("minimind_v3_pure", trust_remote_code=True)
m.to("cuda"); m.eval()

with open("micro_test_clean.jsonl", encoding="utf-8") as f:
    test = [json.loads(l) for l in f]

def ask(prompt, max_t=20):
    msgs = [{'role':'user','content':prompt}]
    text = t.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
    ids = t(text, return_tensors="pt").to("cuda")
    with torch.no_grad():
        out = m.generate(**ids, max_new_tokens=max_t, temperature=0.1, do_sample=False,
            pad_token_id=t.eos_token_id)
    return t.decode(out[0, ids['input_ids'].shape[1]:], skip_special_tokens=True).strip()

c_mic = c_cn = 0
for d in test:
    if d['answer'] in ask(f"{d['entity_map']}。{d['mic']}"): c_mic += 1
    if d['answer'] in ask(d['cn']): c_cn += 1

print(f"MIC:{c_mic}/{len(test)}={c_mic}% CN:{c_cn}/{len(test)}={c_cn}%")
