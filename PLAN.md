# 实体追踪微语实验 — Workshop Paper Plan

## 目标会议
- **BabyLM Challenge** @ EMNLP 2026 (7月截止)
- ICLR Tiny Papers (备选)
- Neuro-Symbolic Workshops (备选)

## 核心发现（5条 → 1个统一论题）

> 64M模型的符号推理能力对训练数据的结构极度敏感，在绑定方式、模板多样性、样本密度三个维度上存在明确甜点区。推理能力和输出格式是独立的学习目标，在小样本预算下互相竞争。

## 已完成
- [x] 假说验证 (20%→36% cross-template)
- [x] 消融实验 (entity map +30pp)
- [x] 300题分层bench (simple 72% / medium 34% / hard 1%)
- [x] 模板scaling (8→20→35, syntax drift确诊)
- [x] 密度控制 (50/100/143 per-tmpl, sweet spot ~100)
- [x] 推理/格式解耦 (v4_20x50: 推理对但格式错)
- [x] Emoji pipeline (translator.py + translator_emoji.py)
- [x] GitHub repo + Zenodo DOI + v0.3 release
- [x] 6个 HuggingFace 模型
- [x] LaTeX 论文 (含density sweet spot section)
- [x] 复现指南 + Reviewer notes

## 论文结构
1. **Introduction**: 自然语言瓶颈 → 显式绑定假说
2. **Method**: 微语设计 + 数据生成 + 训练配置
3. **Experiments**:
   - 3.1 Main Results (跨模板36%)
   - 3.2 Ablation (entity map +30pp)
   - 3.3 Depth-Accuracy Wall (72/34/1)
   - 3.4 Template Scaling (8→20→35)
   - 3.5 Density Sweet Spot (50/100/143)
   - 3.6 Error Analysis
4. **Discussion**: 三维度甜点 + 解耦证据 → 模块化推理架构
5. **Conclusion**: 结构化输入 = 涌现捷径

## 待办
- [ ] Claude 模拟审稿
- [ ] 最终提交
