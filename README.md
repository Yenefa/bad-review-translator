# 差评翻译官

> 面向中小电商商家的评论分析与售后辅助工具：批量识别差评问题、提取具体原因、生成不同语气的客服回复，并输出可复核的分析结果与运营统计。

项目将**本地可复现的分类决策**与**可选的大模型语言生成**分离：核心分类链路可在普通 CPU 环境运行，大模型仅用于增强问题归因与回复表达。

目前系统支持：

- Excel 批量评论导入与清洗
- 物流慢 / 质量差 / 货不对版 / 客服态度差四类问题识别
- BGE Embedding、关键词规则与 Reranker 混合分类
- 低置信度样本人工复核
- 类别约束下的问题原因提取
- 官方 / 共情 / 幽默三种客服回复
- 统计结果与 Excel 周报导出
- FastAPI 接口与 Web Demo

> **设计原则：AI 不负责“显得聪明”，而负责减少可重复工作；无法可靠判断的样本应进入人工复核，而不是强行自动化。**

演示：https://ilove-d5g0gzrpp375112b9-1413557923.tcloudbaseapp.com · 本地：`open frontend/index.html`

---

## Benchmark

项目使用三类数据分别验证**分类能力、模型可学习性与真实业务链路**。不同评测集承担不同目的，因此结果不直接混合比较。

### 1. `mock_100`：独立分类 Benchmark

`mock_100` 包含 100 条带人工标签的电商差评，用于比较不同分类方法。

| Method                         | Accuracy | Macro-F1 | Notes                  |
| ------------------------------ | -------: | -------: | ---------------------- |
| Keyword baseline               |  **93%** |     0.93 | 基于人工定义关键词              |
| BGE semantic labels            |      86% |     0.86 | BGE 与类别描述句相似度          |
| Hybrid                         |      88% |     0.88 | BGE + keyword fallback |
| Frozen BGE + linear classifier |      88% |        — | 公开数据训练后迁移至 mock_100    |

当前结果显示，**在类别数量较少、关键词高度显式的场景中，规则系统仍然是非常强的 baseline**。因此项目并不假设“模型一定优于规则”，而采用可解释的混合策略。

### 2. Public Dataset Experiment

从公开电商评论数据集中抽取 6,000 条样本，并按 80/20 分层划分：

- Training: 4,800
- Validation: 1,200

实验采用：`BAAI/bge-small-zh-v1.5 → frozen embeddings → Logistic Regression`

BGE 编码器参数保持冻结，仅训练轻量线性分类器。

在同分布 validation split 上：

| Metric   | Result |
| -------- | -----: |
| Accuracy |  1.000 |
| Macro-F1 |  1.000 |

该结果主要用于验证 BGE 表征在当前四分类任务上的**线性可分性**，不将其视为对真实电商场景泛化能力的证明。项目以独立 `mock_100` 和真实样本评测衡量泛化表现。

### 3. Real-world Pilot

已使用青竹小轩百货的真实评论样本完成小规模端到端试运行，覆盖：`评论导入 → 分类 → 问题归因 → 回复生成 → 统计 → 周报导出`

目前真实数据规模较小，因此该部分用于验证**业务流程可用性**，暂不作为模型准确率 benchmark。

### 下一步评测

- per-class Precision / Recall / F1
- confusion matrix、multi-label 差评、low-confidence coverage、human-review rate、latency / cost、hard-case error analysis

---

## Architecture

```text
                     ┌──────────────────┐
                     │ Excel / Web Input│
                     └────────┬─────────┘
                              │
                              ▼
                     ┌──────────────────┐
                     │ Text Cleaning    │
                     └────────┬─────────┘
                              │
                              ▼
               ┌──────────────────────────────┐
               │ Issue Classification         │
               │ • Keyword baseline           │
               │ • BGE semantic similarity    │
               │ • Optional Reranker          │
               │ • Hybrid decision            │
               └──────────────┬───────────────┘
                              │
                        confidence
                              │
               ┌──────────────┴───────────────┐
               │                              │
          high confidence                low confidence
               │                              │
               ▼                              ▼
      ┌──────────────────┐          ┌──────────────────┐
      │ Cause Extraction │          │ Human Review     │
      │ Rule constrained │          └────────┬─────────┘
      │ + optional LLM   │                   │
      └────────┬─────────┘                   │
               └──────────────┬──────────────┘
                              ▼
                    ┌──────────────────┐
                    │ Reply Generation │
                    │ Official/Empathetic/Humorous │
                    └────────┬─────────┘
                             │
                             ▼
                   ┌──────────────────┐
                   │ Report / Export  │
                   └──────────────────┘
```

**Classification**：核心决策层，支持关键词基线、BGE语义、Reranker二次排序的混合决策。

**Cause Extraction**：在预测类别约束下进行，基础为关键词证据定位，可选 LLM 提取更自然的属性级短语。

**Reply Generation**：语言表达层，无 API 时使用本地模板，可选 LLM 增强；核心链路离线可用。

**Human Review**：低置信度（阈值 0.55）进入人工复核队列，长期以 `accuracy + automation coverage + human review rate` 衡量系统。

---

## Limitations

1. **分类体系较小**：仅4类，真实场景需层级化 taxonomy。
2. **Single-label**：现实评论可能多问题共现（如“物流慢且客服不回”），当前取主类，未来升级 multi-label。
3. **Benchmark有限**：`mock_100` 样本少，公开集验证为同分布，主要说明可学习性，需扩大独立测试集。
4. **真实数据少**：当前仅用于流程验证，不宣称商业级准确率。
5. **规则依赖**：关键词在隐喻/反讽/长文本/新品类下可能下降，需语义模型补充。
6. **知识库**：当前为店铺知识上下文注入，尚未实现完整检索（chunk→embedding/BM25→Top-K）链路。
7. **LLM**：仅辅助归因与表达，不承诺真实业务事实，需结合店铺规则与人工审核。

## Project Direction

下一步重点：建立更大规模独立测试集、系统化 error analysis、升级 multi-label、引入置信度校准、量化 automation coverage / human-review rate、将知识增强升级为真实检索链路、用更多真实数据验证。

> 最终目标不是“所有差评交给 AI”，而是讓高置信、重复性的工作自动完成，把模糊和高风险的留给人。

---

## 快速开始

```bash
pip install -r backend/requirements.txt
python backend/app.py                  # 100条 → data/mock_100_已分析.xlsx
DEEPSEEK_API_KEY=sk-... python backend/app.py  # 带LLM归因
```

API：`POST /analyze`（FastAPI，已上云 `bad-review-api`）

数据：`data/mock_100.xlsx` / `data/sample_6k.csv` / `data/周报_*.xlsx`

## 可复现性

所有路径已改为 `Path(__file__).resolve().parent` 相对路径，clone 后可直接运行。详见 `docs/benchmark.md`。

许可证：MIT
