import os
import time
import json
from dotenv import load_dotenv
from flask import Flask, render_template, request, Response, jsonify

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

PERSIST_DIR = "db"

# 三個 collection 名稱（要跟 ingest_all.py 一致）
COLLECTIONS = {
    "laws": "trust_laws",
    "main": "trust_main",
}

# ===== 全域單例（效能更好）=====
EMBEDDINGS = OpenAIEmbeddings()
LLM = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 向量庫連線（按 collection cached）
_VECTORDB_CACHE = {}


def json_response(obj, status: int = 200) -> Response:
    return Response(
        json.dumps(obj, ensure_ascii=False, indent=2),
        status=status,
        content_type="application/json; charset=utf-8",
    )


def get_vectordb(collection_name: str) -> Chroma:
    if collection_name not in _VECTORDB_CACHE:
        _VECTORDB_CACHE[collection_name] = Chroma(
            persist_directory=PERSIST_DIR,
            collection_name=collection_name,
            embedding_function=EMBEDDINGS,
        )
    return _VECTORDB_CACHE[collection_name]


def normalize_user_profile(user_profile):
    """
    支援：
    - 字串："小明，25歲..."
    - 物件：{"summary":"...","age":25,...}
    回傳一個 summary 字串
    """
    if not user_profile:
        return ""
    if isinstance(user_profile, str):
        return user_profile.strip()
    if isinstance(user_profile, dict):
        s = (user_profile.get("summary") or "").strip()
        return s
    # 其他型別就轉字串
    return str(user_profile).strip()


def dedup_results(results, need_k: int):
    """
    results: list of (Document, score)
    去重後回傳 contexts, sources（最多 need_k 筆）
    """
    seen = set()
    contexts = []
    sources = []

    for doc, score in results:
        content = (doc.page_content or "").strip()
        if not content:
            continue
        key = (doc.metadata.get("source", "unknown"), content)
        if key in seen:
            continue
        seen.add(key)

        contexts.append(content)
        sources.append(
            {
                "source": doc.metadata.get("source", "unknown"),
                "score": float(score),
                "excerpt": content[:220],
            }
        )

        if len(sources) >= need_k:
            break

    return contexts, sources


def retrieve(collection: str, query: str, top_k: int):
    """
    從指定 collection 檢索 top_k（含去重）
    """
    vectordb = get_vectordb(collection)
    fetch_k = max(top_k, min(top_k + 4, 10))  # 多抓一些給去重
    results = vectordb.similarity_search_with_relevance_scores(query, k=fetch_k)
    return dedup_results(results, top_k)


def build_prompt(
    user_profile_summary: str,
    question: str,
    main_contexts: list[str],
    law_contexts: list[str],
) -> str:
    main_ctx = "\n\n---\n\n".join(main_contexts) if main_contexts else ""
    law_ctx = "\n\n---\n\n".join(law_contexts) if law_contexts else ""

    user_part = f"【使用者背景】\n{user_profile_summary}\n\n" if user_profile_summary else ""

    return f"""你是永豐銀行「信託小學堂」助理，同時需要信託知識普及以及信託產品推廣的功能。請用繁體中文回答。
回答規則：
1) 請以一般人看得懂的方式回答，可做合理推論與補充說明，但不得捏造不存在於資料中的具體數字、費率、法條內容或承諾。
2) 涉及「規範、限制、義務、權利、合規」時，請參考【法規/規範】提供合規提醒；若與資料衝突，以【法規/規範】為準。
3) 若資料不足以給出具體結論，請先提供一般性建議，並列出需要使用者補充的資訊。
4) 回答的最後請提出永豐銀行可以針對使用者提問問題提供的協助。

{user_part}【問題】
{question}


{main_ctx}

【法規/規範】
{law_ctx}

【回答】
"""


@app.route('/get_response', methods=['POST'])
def get_response():
    data = request.json

    question = (data.get("question") or "").strip()
    if not question:
        return json_response(
            {"error": {"code": "EMPTY_QUESTION", "message": "question is required"}},
            status=400,
        )
    
    print(f"收到使用者訊息: {question}")
    # top_k（可選）
    main_k = int(data.get("main_top_k") or data.get("top_k") or 3)
    laws_k = int(data.get("laws_top_k") or 2)

    # 1) 主庫檢索（articles 或 products）
    main_collection = COLLECTIONS["main"]
    main_contexts, main_sources = retrieve(main_collection, question, main_k)

    # 2) 法規必查
    law_collection = COLLECTIONS["laws"]
    law_contexts, law_sources = retrieve(law_collection, question, laws_k)

    prompt = build_prompt("", question, main_contexts, law_contexts)
    answer = LLM.invoke(prompt).content

    # sources = main_sources + law_sources
    
    return jsonify({
        "reply": f"{answer}"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)