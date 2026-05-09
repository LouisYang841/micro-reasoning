---
name: micro-reasoning-reproduce
description: Full reproduce pipeline for entity tracking experiment with MiniMind 64M + micro-language
---

# Micro-Reasoning Experiment — Full Reproduce Guide

## Quick Summary
64M MiniMind fine-tuned on 500 micro-language stories with entity binding → entity tracking accuracy 20%→83%.

## Step 1: Environment Setup

### Option A: GPU (4060, recommended)
```bash
# Windows D drive venv
python -m venv D:\minimind_venv
D:\minimind_venv\Scripts\pip install torch transformers datasets accelerate

# Clone MiniMind
git clone https://github.com/jingyaogong/minimind.git D:\minimind --depth 1
```

### Option B: CPU (EC2, slow but works)
```bash
pip3 install --break-system-packages torch --index-url https://download.pytorch.org/whl/cpu
pip3 install --break-system-packages transformers
# MiniMind 64M needs ~800MB RAM for inference, ~1.5GB for training
```

## Step 2: Generate Training Data
```bash
cd minimind/
# Copy micro_lang.py and micro_gen.py from repo
python micro_gen.py  # Outputs micro_train.jsonl (500 stories)
```

## Step 3: Train (GPU)
```bash
python train_cuda.py  # 5 epochs, ~2 minutes on 4060
# Output: minimind_micro_cuda/
```

### Ablation Version (no entity mapping)
```bash
# Generate without entity map:
python -c "
import json
with open('micro_train.jsonl') as f:
    data = [json.loads(l) for l in f]
noent = [{'mic': d['mic'], 'answer': d['answer']} for d in data]
with open('micro_train_noent.jsonl', 'w') as f:
    for d in noent: f.write(json.dumps(d, ensure_ascii=False)+'\n')
"
python train_ablate.py  # 5 epochs without entity mapping
```

## Step 4: Test
```bash
python test_cuda2.py  # Outputs test_results.json
```

## Common Pitfalls

### Windows GBK encoding errors
- Use JSON output instead of print() for Chinese text
- Or set `chcp 65001` before running Python

### C drive full during pip install
- Set `PIP_CACHE_DIR=D:\pip_cache` and `TMP=D:\tmp`
- pip cache can be 2-5GB for torch

### OOM during CPU training
- Use SGD instead of AdamW (saves 2x optimizer memory)
- Train only attention Q/K/V/O projections (14M/64M)
- Surgical unfreezing: bottom layers attention only, top layers attention+FFN

### EC2 /tmp full
- Download to ~/ instead of /tmp
- `pip3 cache purge` regularly

## EC2 v2 (SGD + Surgical) — Best for 1.8GB RAM
```bash
cd minimind/ && python3 train_micro_v2.py
# 29.2M params trainable, SGD, 5 epochs
# Result: train loss 0.87→0.24, but CN accuracy only 17%
# Conclusion: partial unfreezing + SGD insufficient for transfer
```

## Key Results Table
| Condition | CN Accuracy |
|-----------|------------|
| Baseline raw 64M | ~20% |
| 4060 ablation (no map) | 53% |
| 4060 full (with map) 5e | 83% |
| 4060 15e (overfit) | 47% |
| EC2 v2 surgical SGD | 17% |

## Hardware Notes
- **EC2 t4g.small**: ARM CPU, 1.8GB RAM, 29GB disk. Can only do inference or partial training.
- **FlowX13 4060**: 6GB VRAM, D drive 300GB. Recommended for all training.
- **Windows SSH**: `ssh flowx13` (reverse tunnel via localhost:2222)

## V4 Density Control Experiments

To reproduce the sample-density sweet spot finding:

```bash
# Generate data (35 or 20 templates × 50 samples each)
python src/gen_v4.py
# Train both variants
python src/train_v4.py
# Test on bench
python src/bench_v4.py
```

### Key finding (Reform/Format Decoupling)
At 50 samples/template, the model correctly identifies entities ("乙=书包") but fails to produce the right answer format. At 143 samples/template, the output format is correct but reasoning is memorized. ~100 samples/template is the convergence sweet spot where both reasoning and format align.

### Full Result Matrix
| Model | Templates | /template | MIC | Simple | Medium | Hard |
|-------|-----------|-----------|-----|--------|--------|------|
| v1 | 8 | 62 | 28% | 55% | 30% | 0% |
| v2 | 20 | 100 | 36% | 72% | 34% | 1% |
| v4_20x50 | 20 | 50 | 29% | ~0%* | 27% | 2% |
| v4_35x50 | 35 | 50 | 24% | 17% | 6% | 1% |
| v3_fixed | 35 | 143 | 3% | 3% | 3% | 2% |

*Reasoning correct but output format broken
