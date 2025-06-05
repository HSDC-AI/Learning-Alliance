# RAGAS 评测 Demo
# 自动检测可用指标对象，结构清晰，适合教学和实际使用

from ragas import evaluate
import ragas.metrics

# 构造样本数据
samples = [
    {
        "question": "大模型是什么？",
        "answer": "大模型是指包含大量参数的神经网络模型，通常用于自然语言处理任务。",
        "context": "大模型是指包含大量参数的神经网络模型，通常用于自然语言处理任务。",
        "ground_truth": "大模型是LLM"
    }
]

#from ragas import evaluate
# 假设 data 为包含问题、参考答案、检索内容、生成答案的数据集
results = evaluate(samples, metrics=["faithfulness", "context_relevance", "answer_relevance"])
print(results.summary())













