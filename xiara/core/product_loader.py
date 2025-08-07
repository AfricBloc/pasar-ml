import os
import json
import pandas as pd
from langchain_core.documents import Document

def load_all_products(data_path: str = "xiara/data") -> list[Document]:
    docs = []

    for filename in os.listdir(data_path):
        filepath = os.path.join(data_path, filename)

        if filename.endswith(".txt"):
            with open(filepath, "r", encoding="utf-8") as f:
                docs.append(Document(page_content=f.read(), metadata={"source": filename}))

        elif filename.endswith(".csv"):
            df = pd.read_csv(filepath)
            for _, row in df.iterrows():
                content = ", ".join(f"{col}: {row[col]}" for col in df.columns)
                docs.append(Document(page_content=content, metadata={"source": filename}))

        elif filename.endswith(".json"):
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    for item in data:
                        content = ", ".join(f"{k}: {v}" for k, v in item.items())
                        docs.append(Document(page_content=content, metadata={"source": filename}))

    return docs
