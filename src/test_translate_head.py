"""测试翻译头模型 — 微语+中文双指标"""
import json, os
os.chdir(r"D:\minimind")
from transformers import AutoTokenizer
from model.model_minimind import MiniMindForCausalLM
import torch

m = MiniMindForCausalLM.from_pretrained("minimind_v2_translate", trust_remote_code=True, torch_dtype=torch.float16)
t = AutoTokenizer.from_pretrained("minimind_v2_translate", trust_remote_code=True)
m.to("cuda"); m.eval()

with open("micro_test_clean.jsonl", encoding="utf-8") as f:
    test = [json.loads(l) for l in f]

def ask(prompt, max_t=30):
    msgs = [{'role':'user','content':prompt}]
    text = t.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
    ids = t(text, return_tensors="pt").to("cuda")
    with torch.no_grad():
        out = m.generate(**ids, max_new_tokens=max_t, temperature=0.1, do_sample=False,
            pad_token_id=t.eos_token_id)
    return t.decode(out[0, ids['input_ids'].shape[1]:], skip_special_tokens=True).strip()

c_mic = c_cn = 0
for i, d in enumerate(test):
    # 微语推理: 保持原有格式
    mic_ok = d['answer'] in ask(f"{d['entity_map']}。{d['mic']}")
    # 中文: 测试翻译能力
    cn_ok = d['answer'] in ask(d['cn'])
    if mic_ok: c_mic += 1
    if cn_ok: c_cn += 1
    if i < 5:
        print(f"[{i+1}] ans={d['answer']} mic={'Y' if mic_ok else 'N'} cn={'Y' if cn_ok else 'N'}")

print(f"\nMIC:{c_mic}/{len(test)}={c_mic}% CN:{c_cn}/{len(test)}={c_cn}%")
