import os
import json
import pandas as pd
from langchain_core.documents import Document
from typing import Optional, List

def load_all_products(data_path: Optional[str] = None) -> List[Document]:
    """Load all product documents from the data directory."""
    if data_path is None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(current_dir, '..', 'data')

    docs = []

    if not os.path.exists(data_path):
        print(f" Data directory not found: {data_path}. Continuing without loading products.")
        return docs  # Just return empty

    try:
        files = os.listdir(data_path)
    except Exception as e:
        print(f" Cannot access data directory {data_path}: {e}")
        return docs

    for filename in files:
        filepath = os.path.join(data_path, filename)
        if not os.path.isfile(filepath):
            continue
        try:
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
        except Exception as e:
            print(f" Failed to process file {filename}: {e}")

    if not docs:
        print(f" No documents loaded from {data_path}. Check file formats and content.")

    return docs
