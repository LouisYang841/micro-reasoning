# Micro-Reasoning: 64M MiniMind Entity Tracking via Micro-Language

> Explicit object binding enables entity tracking in 64M language models.
> Cross-template accuracy: 20% → 36%, with clear sweet spots in three structural dimensions.
>
> 📜 [Paper](paper.tex) · 🤗 [Models](https://huggingface.co/LouisYang841) · 📦 [Zenodo v0.1](https://doi.org/10.5281/zenodo.20089724)

## Overview

Large language models acquire reasoning abilities only at billion-parameter scales. We show that **explicit entity binding**—declaring `甲=小明 乙=苹果` before reasoning in a custom **micro-language**—enables a 64M model to track entities it otherwise cannot.

## Core Findings

1. **Explicit binding works**: Entity maps contribute +30pp cross-template (ablation)
2. **Reasoning depth ceiling**: Simple 72% → Medium 34% → Hard 1% on 300-question stratified bench
3. **Template diversity sweet spot**: 20 templates optimal (vs 8 weak, 35 syntax drift)
4. **Density sweet spot**: ~100 samples/template optimal (50→format broken, 143→memorization)
5. **Reasoning/format decoupling**: At 50/tmpl, model identifies entities correctly but fails output format—proving reasoning and generation are separable objectives

## Unified Bench (300 Questions)

| Model | Templates | /tmpl | MIC | Simple | Medium | Hard | CN |
|-------|-----------|-------|-----|--------|--------|------|-----|
| v1 | 8 | 62 | 28% | 55% | 30% | 0% | 29% |
| **v2** | **20** | **100** | **36%** | **72%** | **34%** | **1%** | 10% |
| v4_20x50 | 20 | 50 | 29% | ~0%* | 27% | 2% | — |
| v4_35x50 | 35 | 50 | 24% | 17% | 6% | 1% | — |
| v3_fixed | 35 | 143 | 3% | 3% | 3% | 2% | — |

*\*v4_20x50: reasoning correct ("乙=书包") but answer format broken*

### Density Sweet Spot Table

| /Template | Behavior | Observation |
|-----------|----------|-------------|
| 50 | Format broken | Entity identification works, output format fails |
| **100** | **Sweet spot** | Both reasoning and format aligned |
| 143 | Memorization | Format correct, reasoning collapsed |

### Depth-Accuracy Wall (v2)

| Difficulty | Accuracy | Interpretation |
|------------|----------|----------------|
| Simple (1-hop) | 72% | Single container/placement |
| Medium (2-hop) | 34% | Multi-step with distractors |
| Hard (multi-hop) | 1% | Person transfer, nesting |

## Micro-Language

```
中文: 小明把苹果放进书包，然后离开。回来，苹果在哪里？
微语: 甲置乙入丙，乃离矣。甲归，乙安？
映射: 甲=小明 乙=苹果 丙=书包
答案: 丙里 → 书包里
```

- **Entities**: 甲,乙,丙... (天干 = variable names)
- **Actions**: 置(put), 入(into), 离(leave), 归(return), 啖(eat), 寻(find)
- **Logic**: 乃(then), 矣(done), 安(where)
- **Translation**: 0-param Python dict (`translator.py` + `translator_emoji.py`)

## 🤗 Models

| Model | HF Repo | Description |
|-------|---------|-------------|
| **v2** | [micro-reasoning-v2](https://huggingface.co/LouisYang841/micro-reasoning-v2) | Best: 20 tmpl, 100/tmpl |
| v1 | [micro-reasoning-v1](https://huggingface.co/LouisYang841/micro-reasoning-v1) | Baseline: 8 tmpl |
| ablation | [micro-reasoning-ablation](https://huggingface.co/LouisYang841/micro-reasoning-ablation) | No entity mapping |
| v3-overfit | [micro-reasoning-v3-overfit](https://huggingface.co/LouisYang841/micro-reasoning-v3-overfit) | 35 tmpl memorization |
| v4-20x50 | [micro-reasoning-v4-20x50](https://huggingface.co/LouisYang841/micro-reasoning-v4-20x50) | Format broken |
| v4-35x50 | [micro-reasoning-v4-35x50](https://huggingface.co/LouisYang841/micro-reasoning-v4-35x50) | Density control |

All fine-tuned from `jingyaogong/minimind-3` (Apache 2.0).

## Reproduce

```bash
git clone https://github.com/LouisYang841/micro-reasoning.git
pip install torch transformers
python src/micro_gen.py          # Generate v1 training data
python src/train_pure_micro.py   # Train v1
python src/test_v2v3.py          # Run bench evaluation
```

Full guide: [REPRODUCE.md](REPRODUCE.md)

## Citation

```bibtex
@misc{yang2026micro,
  title={Micro-Reasoning: Explicit Object Binding for Entity Tracking in 64M Language Models},
  author={Yang, Jiaxuan},
  year={2026},
  doi={10.5281/zenodo.20089724},
  url={https://github.com/LouisYang841/micro-reasoning}
}
```
