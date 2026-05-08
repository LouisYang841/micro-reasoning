"""4060 微语模型推理 - 输出JSON"""
import json, random, torch, os
os.chdir(r"D:\minimind")
from transformers import AutoTokenizer
from model.model_minimind import MiniMindForCausalLM

DEVICE = "cuda"
model = MiniMindForCausalLM.from_pretrained("minimind_micro_cuda", trust_remote_code=True, torch_dtype=torch.float16)
tokenizer = AutoTokenizer.from_pretrained("minimind_micro_cuda", trust_remote_code=True)
model.to(DEVICE)
model.eval()

with open("micro_train.jsonl", encoding="utf-8") as f:
    test = random.sample([json.loads(l) for l in f], 30)

def ask(prompt, max_t=15):
    msgs = [{'role':'user','content':prompt}]
    text = tokenizer.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
    ids = tokenizer(text, return_tensors="pt").to(DEVICE)
    with torch.no_grad():
        out = model.generate(**ids, max_new_tokens=max_t, temperature=0.1, do_sample=False,
            pad_token_id=tokenizer.eos_token_id)
    return tokenizer.decode(out[0, ids['input_ids'].shape[1]:], skip_special_tokens=True).strip()

results = []
c_mic = c_cn = 0
for d in test:
    mic_ans = ask(f"{d['entity_map']}。{d['mic']}")
    cn_ans = ask(d['cn'])
    mic_ok = d['answer'] in mic_ans
    cn_ok = d['answer'] in cn_ans
    if mic_ok: c_mic += 1
    if cn_ok: c_cn += 1
    results.append({
        "answer": d['answer'],
        "mic_input": d['mic'],
        "mic_output": mic_ans,
        "mic_correct": mic_ok,
        "cn_input": d['cn'],
        "cn_output": cn_ans,
        "cn_correct": cn_ok,
        "entity_map": d['entity_map'],
    })

summary = {
    "mic_accuracy": f"{c_mic}/{len(test)}={c_mic/len(test)*100:.0f}%",
    "cn_accuracy": f"{c_cn}/{len(test)}={c_cn/len(test)*100:.0f}%",
}
results.append({"SUMMARY": summary})

with open("test_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print(f"MIC:{c_mic}/{len(test)} CN:{c_cn}/{len(test)}")
print("DONE")
