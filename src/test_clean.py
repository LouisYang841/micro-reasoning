"""无泄露测试 — 全新模板，100题"""
import json, random, os
os.chdir(r"D:\minimind")
from transformers import AutoTokenizer
from model.model_minimind import MiniMindForCausalLM
import torch

DEVICE = "cuda"
model = MiniMindForCausalLM.from_pretrained("minimind_micro_cuda", trust_remote_code=True, torch_dtype=torch.float16)
tok = AutoTokenizer.from_pretrained("minimind_micro_cuda", trust_remote_code=True)
model.to(DEVICE); model.eval()

with open("micro_test_clean.jsonl", encoding="utf-8") as f:
    test = [json.loads(l) for l in f]

def ask(prompt, max_t=20):
    msgs = [{'role':'user','content':prompt}]
    text = tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
    ids = tok(text, return_tensors="pt").to(DEVICE)
    with torch.no_grad():
        out = model.generate(**ids, max_new_tokens=max_t, temperature=0.1, do_sample=False,
            pad_token_id=tok.eos_token_id)
    return tok.decode(out[0, ids['input_ids'].shape[1]:], skip_special_tokens=True).strip()

results = []
c_mic = c_cn = 0
for d in test:
    mic_ok = d['answer'] in ask(f"{d['entity_map']}。{d['mic']}")
    cn_ok = d['answer'] in ask(d['cn'])
    if mic_ok: c_mic += 1
    if cn_ok: c_cn += 1
    results.append({"answer": d['answer'], "mic_ok": mic_ok, "cn_ok": cn_ok,
                    "mic": d['mic'], "cn": d['cn']})

results.append({"SUMMARY": {"mic": f"{c_mic}/100={c_mic}%", "cn": f"{c_cn}/100={c_cn}%"}})
with open("test_clean_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print(f"MIC:{c_mic}/100 CN:{c_cn}/100 DONE")
