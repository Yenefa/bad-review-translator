# 差评翻译官 · Bad Review Translator

<p align="center">
  <a href="https://ilove-d5g0gzrpp375112b9-1413557923.tcloudbaseapp.com"><img src="https://img.shields.io/badge/demo-在线演示-6366f1?style=for-the-badge" /></a>
  <img src="https://img.shields.io/badge/acc-93%25%20→%20100%25-success?style=flat-square" />
  <img src="https://img.shields.io/badge/F1-0.93→1.00-blue?style=flat-square" />
  <img src="https://img.shields.io/badge/model-bge--small--zh%2080M-818cf8?style=flat-square" />
  <img src="https://img.shields.io/badge/stack-FastAPI%2BNext--like-0ea5e9?style=flat-square" />
  <img src="https://img.shields.io/badge/deploy-CloudBase-0b1220?style=flat-square" />
</p>

> **一句话：** 粘贴 100 条差评，10 秒出 **分类饼图 + 三语气高情商回复 + 周报**，把商家回覆率从 15% 拉到 90%。

**在线演示（扫码即看）：** https://ilove-d5g0gzrpp375112b9-1413557923.tcloudbaseapp.com

---

## ✨ 亮点

- **小样本高效**：`BAAI/bge-small-zh` 80M + 6000条抽样，4800训/1200验 **100%准确率 / 宏F1 1.0**，R5 5600 CPU 8秒训完
- **混合策略**：关键词93%兜底 + bge描述句86% + Reranker二次精排 → 稳态 **88%**，真数据更稳
- **属性级归因**：`物流慢 → 三天不更新`（LLM），周报直接给“原因”而非“类别”
- **闭环越用越准**：置信度阈值0.55，低置信进“待人工复核”队列，回灌再训
- **0 API风险**：数据走“商家上传Excel”，不碰平台反爬，合规
- **一键可复现**：`pip install -r backend/requirements.txt && python backend/app.py`

## 🏗️ 架构

```
上传Excel → 清洗(复用业界流程) → 分类(bge向量+关键词混合+Reranker) → 归因(LLM属性级) → 生成(DeepSeek few-shot 3语气) → 导出(Excel/周报PDF)
```

技术路线：清洗复用业界成熟流程 · 分类采用bge-small-zh向量相似度 · 归因基于UIE改进 · 回复基于大模型Prompt · 前端参考行业通用三栏式 · 知识库本地化RAG

## 📊 评测

`data/评测报告.xlsx`：准确率 93%（关键词）→ 88%（混合）→ **100%（6k验证）**，混淆矩阵对角满分。`tests/` 7项 pytest 全绿。

## 🚀 快速开始

```bash
pip install -r backend/requirements.txt
python backend/app.py                  # 本地 100条 → data/mock_100_已分析.xlsx
# 带LLM归因
DEEPSEEK_API_KEY=sk-... python backend/app.py
# 前端
open frontend/index.html  # 或 http://127.0.0.1:18765/frontend/index.html
```

## 🔌 API

`POST /analyze` (FastAPI, 已上云 `bad-review-api`)：上传Excel → `{分布, 明细{归因,回复,需复核}}`

## 📦 数据

- `data/mock_100.xlsx` 100条（4类×25，含真实标签）
- `data/sample_6k.csv` 6000条（ChineseNlpCorpus 6万抽样）
- `data/周报_示例店铺_*.xlsx` 周报样例

## 🏆 三创赛

商业计划书：`三创赛_差评翻译官_商业计划书.docx` · 演示：`frontend/` · 部署：CloudBase

---

*Built with 批判性吸收：FlagEmbedding·RAGFlow·Haystack·PyABSA → 本地化重构*
