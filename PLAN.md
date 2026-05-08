# 实体追踪微语实验 — Workshop Paper Plan

## 目标会议
- **BabyLM Challenge** (EMNLP/CoNLL) — 小模型+小数据的语法逻辑
- **ICLR Tiny Papers Track** — 2页核心，鼓励算力有限的聪明发现
- **Neuro-Symbolic Workshops** — 神经网络+符号逻辑的变量绑定

## 论文结构

### 1. Introduction (引言)
- 痛点：小模型缺乏逻辑推理能力（LLM涌现需要billions）
- 假说：自然语言的语法噪音+缺乏显式对象绑定是瓶颈
- 解法：微型语言 + 实体映射声明

### 2. Methodology (方法)
- 微语字典：动作(置 入 离 归)、疑问(安)、逻辑(乃 矣)
- 数据构造：500条中文故事→微语翻译（自动模板）
- 训练：MiniMind-3 64M, AdamW, 5 epoch

### 3. Experiments (实验)
- 核心表：裸模20% → 消融53% → 完整83%
- 消融证明实体映射行贡献+30pp
- 错误分析：多跳转移是主要失败模式
- Epoch U型曲线：5e甜点，15e过拟合

### 4. Conclusion & Future Work
- 双子星架构：推理模型(64M) + 翻译模型(64M) = 128M
- 合计128M实现自然语言推理闭环

## 已完成工作
- [x] 假说验证 (20%→83%)
- [x] 消融实验 (+30pp归因)
- [x] 错误分析 (工作记忆瓶颈)
- [x] 全量归档 push
- [ ] 翻译模型 (双子星下半)
- [ ] 泛化测试 (新模板)
- [ ] LaTeX 写作
