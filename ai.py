import os
import glob
from groq import Groq

client = Groq(api_key="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")

def summarize(text):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # бесплатная мощная модель
        messages=[
            {"role": "system", "content": "Ты помощник. Сделай краткое саммари подкаста на русском языке."},
            {"role": "user", "content": text[:8000]}  # обрезаем если очень длинный
        ]
    )
    return response.choices[0].message.content

# Обрабатываем все .txt файлы в папке
for filepath in glob.glob("./Kosorukov/**/*.md"):
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()
    
    summary = summarize(text)
    
    out_path = filepath.replace("transcripts/", "summaries/").replace(".md", "_summary.md")
    os.makedirs("summaries", exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(summary)
    
    print(f"✓ {filepath}")