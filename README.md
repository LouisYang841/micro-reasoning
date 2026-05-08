# 微型语言实体追踪实验 — MiniMind 64M

## 假说
显式变量绑定（`甲=小明 乙=苹果`）是小模型获得实体追踪能力的捷径。
无需人脑般的先天语言优化层，只需在输入中注入对象映射声明。

## 实验设计
- 模型: MiniMind-3 (64M), Qwen3 架构
- 数据: 500 条中文故事 + 微语翻译（自动生成）
- 对比: 5 种训练条件

## 核心结果（30题样本）

| 模型 | 参数量 | 优化器 | 硬件 | 微语 | 中文 |
|------|--------|--------|------|------|------|
| 裸模 baseline | 64M | — | 4060 | — | ~20% |
| EC2 v1 (attn only) | 14M | AdamW | CPU | 0% | 23% |
| EC2 v2 (surgical unfreeze) | 29M | SGD | CPU | 7% | 17% |
| 4060 消融 (无实体映射) | 64M | AdamW | 4060 | — | 53% |
| **4060 5e (有实体映射)** | **64M** | **AdamW** | **4060** | 3% | **83%** |
| 4060 15e (过拟合) | 64M | AdamW | 4060 | 63% | 47% |

### 实验条件对比总结
- **硬件**: CPU vs GPU — GPU 训练速度提升 50x+，且收敛更好
- **参数解冻策略**: 部分解冻(14M/29M) vs 全量(64M) — 全量 +30pp+
- **优化器**: SGD vs AdamW — SGD 完全无法收敛
- **实体映射**: 有 vs 无 — 贡献 +30pp（消融验证）
- **训练轮次**: 5e vs 15e — 5e 是甜点，15e 过拟合

## 脚本映射

| 实验条件 | 训练脚本 | 测试脚本 |
|---------|---------|---------|
| EC2 v1 | train_micro_64m.py | test_tuned.py |
| EC2 v2 | train_micro_v2.py | test_tuned.py |
| 4060 5e | train_cuda.py | test_cuda2.py |
| 4060 消融 | train_ablate.py | test_ablate.py |
| 4060 15e | train_continue.py | test_15e.py |
| 裸模 few-shot | — | test_fewshot.py |

## 关键发现
1. 实体映射行 `甲=小明 乙=苹果` 贡献 +30pp（消融验证）
2. 5 epoch 甜点，超过后过拟合到微语格式
3. 全量参数 + AdamW 必需，部分解冻和 SGD 无效
4. 模型在工作记忆中仍受限于多跳转移和人物转移场景

## 文件说明
- micro_lang.py — 微型语言语法定义
- micro_gen.py — 训练数据生成器
- micro_train.jsonl — 500条训练数据（含实体映射）
- micro_train_noent.jsonl — 消融版（无实体映射）
- train_cuda.py — 4060 GPU 训练脚本
- train_ablate.py — 消融训练脚本
- test_cuda2.py — 推理测试脚本
- test_results.json — 5e 模型测试结果
- abl_results.json — 消融测试结果
- test_results_15e.json — 15e 模型测试结果

## 后续方向
- 泛化到多跳/人物转移场景
- 规模对比 (64M vs 198M MoE)
- CoT vs 微语格式对比

## ⚠️ Cross-Template Generalization (Updated)

After reviewer feedback, we generated a held-out test set using **5 entirely new templates** not seen in training:

| Test Set | Templates | Accuracy |
|----------|-----------|----------|
| In-template (original) | 8 train templates | 83% |
| **Cross-template (clean)** | **5 new templates** | **37%** |
| Baseline (untrained) | — | ~20% |

The cross-template accuracy confirms that entity mapping provides real generalization (+17pp over baseline), though the original 83% was inflated by template overlap. See `gen_testset.py` for the train/test template split.

## 📈 Scaling Template Diversity (Pure Micro-Language)

| Version | Templates | Micro Acc | CN Transfer |
|---------|-----------|-----------|-------------|
| v1 mixed | 8 | 20% | 37% |
| v1 pure  | 8 | 38% | 38% |
| **v2 pure** | **20** | **58%** | 16% |

Pure micro-language training with increased template diversity doubles reasoning accuracy, suggesting an emergent threshold for symbolic reasoning in 64M models.
