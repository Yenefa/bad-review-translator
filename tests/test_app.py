import sys
sys.path.insert(0, r'C:\Users\fuker\Desktop\workspace\差评翻译官')
from backend.app import clean, classify, classify_batch, extract_issue, build_prompt, generate_replies, LABELS

def test_clean():
    assert clean("  http://a.com  加微信  😀 hello  ") == "hello"
    assert clean("   ") == ""
    assert clean("加微信领券 刷单") == ""
    assert clean("物流太慢  https://xxx") == "物流太慢"

def test_classify_keyword():
    # 关键词兜底在mock上应准
    assert classify("等了5天才到，物流太慢了")["label"] == "物流慢"
    assert classify("面料起球严重")["label"] == "质量差"
    assert classify("图片是红色发来是暗红")["label"] == "货不对版"
    assert classify("客服半天不回机器人")["label"] == "客服态度差"
    # 空
    assert classify("")["label"] == "质量差"

def test_classify_batch():
    texts = ["物流太慢", "质量差", "色差太大", "客服不回"]
    res = classify_batch(texts)
    assert len(res) == 4
    assert all("label" in r and "score" in r for r in res)
    assert res[0]["label"] == "物流慢"

def test_extract_issue():
    assert extract_issue("物流太慢，等了5天", "物流慢")["primary"] in ["物流慢","等了","快递慢"]
    assert extract_issue("客服半天不回", "客服态度差")["primary"] == "不回"
    # 约束：不在该类关键词时回退label
    assert extract_issue("完全不相关文本", "质量差")["primary"] == "质量差"

def test_build_prompt():
    p = build_prompt("物流太慢", "物流慢", "共情")
    assert "共情" in p and "物流" in p and "参考示例" in p
    assert len(p) > 50

def test_generate_replies():
    reps = generate_replies("物流太慢", "物流慢")
    assert set(reps.keys()) == {"官方","共情","幽默"}
    assert all(len(v) > 10 for v in reps.values())

def test_labels():
    assert len(LABELS) == 4
    assert "物流慢" in LABELS
