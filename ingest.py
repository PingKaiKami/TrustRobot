import os
import glob
from dotenv import load_dotenv

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

PERSIST_DIR = "db"

# ✅ 主庫合併 collection（articles + products 共用）
MAIN_COLLECTION = "trust_main"

# ✅ laws 仍然獨立 collection
LAWS_COLLECTION = "trust_laws"

SOURCES = {
    "laws": {
        "pattern": "data/laws/*.txt",
        "collection": LAWS_COLLECTION,
        "chunk_size": 550,
        "chunk_overlap": 120,
    },
    "articles": {
        "pattern": "data/articles/*.txt",
        "collection": MAIN_COLLECTION,  # ✅ 改成主庫
        "chunk_size": 300,
        "chunk_overlap": 80,
    },
    "products": {
        "pattern": "data/products/*.txt",
        "collection": MAIN_COLLECTION,  # ✅ 改成主庫
        "chunk_size": 300,
        "chunk_overlap": 60,
    },
}

def load_documents(mode: str, pattern: str):
    files = sorted(glob.glob(pattern))
    if not files:
        print(f"[WARN] mode={mode} 找不到任何檔案：{pattern}")
        return []

    docs = []
    for path in files:
        loader = TextLoader(path, encoding="utf-8")
        loaded = loader.load()

        if not loaded or not loaded[0].page_content.strip():
            print(f"[WARN] 檔案內容為空，略過：{path}")
            continue

        for d in loaded:
            d.metadata["mode"] = mode
            d.metadata["source"] = os.path.basename(path)
        docs.extend(loaded)

    return docs

def ingest_mode(mode: str, cfg: dict, embeddings: OpenAIEmbeddings):
    docs = load_documents(mode, cfg["pattern"])
    if not docs:
        print(f"[SKIP] mode={mode} 無可用文件")
        return 0, 0

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=cfg["chunk_size"],
        chunk_overlap=cfg["chunk_overlap"],
    )
    chunks = splitter.split_documents(docs)

    if not chunks:
        print(f"[SKIP] mode={mode} 切段後 chunks=0（請檢查文本格式）")
        return len(docs), 0

    # ✅ 先打開指定 collection，再 add（articles/products 會一起進主庫）
    vectordb = Chroma(
        persist_directory=PERSIST_DIR,
        collection_name=cfg["collection"],
        embedding_function=embeddings,
    )
    vectordb.add_documents(chunks)

    print(f"[OK] mode={mode} docs={len(docs)} chunks={len(chunks)} -> collection={cfg['collection']}")
    return len(docs), len(chunks)

def main():
    os.makedirs(PERSIST_DIR, exist_ok=True)
    embeddings = OpenAIEmbeddings()

    total_docs, total_chunks = 0, 0
    for mode, cfg in SOURCES.items():
        d, c = ingest_mode(mode, cfg, embeddings)
        total_docs += d
        total_chunks += c

    print(f"\n[DONE] total_docs={total_docs}, total_chunks={total_chunks}, db_dir={PERSIST_DIR}/")

if __name__ == "__main__":
    main()