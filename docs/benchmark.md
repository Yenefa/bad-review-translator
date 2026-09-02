# Benchmark

项目使用三类数据分别验证不同目标，**不混合为单一准确率**。

## 1. mock_100：独立分类 Benchmark

100 条带人工标签，用于比较分类策略。

| Method | Accuracy | Macro-F1 |
|---|---|---|
| Keyword baseline | 93% | 0.93 |
| BGE semantic labels | 86% | 0.86 |
| Hybrid | 88% | 0.88 |
| Frozen BGE + linear classifier (public 6k → mock) | 88% | — |

**结论**：关键词在当前窄域四分类中为极强 baseline，模型价值在长尾与扩展。

## 2. Public Split

6,000 条抽样（4800 train / 1200 val），`BAAI/bge-small-zh-v1.5 → frozen → LogisticRegression`。

- Accuracy 1.000 / Macro-F1 1.000（同分布 validation）
- 用于验证线性可分性，不作为泛化证明

## 3. Real-world Pilot

青竹小轩百货 5 条真实评论：端到端流程验证，不计入准确率 benchmark。

## 可复现

```bash
python backend/app.py
python finetune_bge.py
pytest tests/test_app.py
```
