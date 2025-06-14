from transformers import pipeline

classifire = pipeline("sentiment-analysis")
result = classifire("I love using transformers for NLP tasks!")
print(result)