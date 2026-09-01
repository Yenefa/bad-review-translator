# 差评翻译官 - 三创赛 MVP

## 一键运行（demo）
pip install -r backend/requirements.txt
python backend/app.py  # 先跑通 bge 分类

## 数据
- data/mock_100.xlsx  100条 mock 差评（4类×25），含“真实类别”列仅用于验证
- 后续可替换为 商家导出的真实 Excel

## 接口（待实现）
POST /analyze  上传 Excel -> 返回 {分类饼图, 每条回复(3语气), 周报PDF}

## 技术路线（专业版）
- 清洗 → 复用业界成熟的文本清洗流程
- 分类 → 采用 bge-small-zh 向量相似度分类方案
- 归因 → 基于 UIE 的属性级抽取思路改进
- 回复 → 基于大模型 Prompt 的多语气改写
- 前端 → 参考行业通用的三栏式客服布局
