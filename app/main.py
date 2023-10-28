from tempfile import TemporaryDirectory

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Qdrant
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
import base64

from . import settings
from .models import request_models, respond_models

app = FastAPI()

EMBEDDING_MODEL = OpenAIEmbeddings(
    openai_api_key=settings.OPENAI_API_KEY,
    model="text-embedding-ada-002"
)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

QDRANT_PATH = "localhost"


@app.put("/pdf")
def read_pdf(input_value: request_models.QA_pdf):
    pdf_data = base64.b64decode(input_value.pdf)
    with TemporaryDirectory() as tempdir:
        file_name = f"{input_value.collection_name}.pdf"
        with open(file_name, "wb") as f:
            f.write(pdf_data)
        loader = PyPDFLoader(f"{file_name}")
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        pages = loader.load_and_split(text_splitter)
    qdrant = qdrants_load(input_value.collection_name)
    qdrant.add_documents(pages)

    return "OK"


@app.put("/question")
def question(qa_params: request_models.QA):
    qdrant = qdrants_load(qa_params.collection_name)
    retriever = qdrant.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 10}
    )

    qa = RetrievalQAWithSourcesChain.from_chain_type(
        llm=OpenAI(model_name='gpt-3.5-turbo-16k', openai_api_key=settings.OPENAI_API_KEY),
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=False,
        verbose=False)

    # 10. 質問に対する解答を取得
    result = qa({"question": qa_params.question}, return_only_outputs=True)

    # 12. レスポンスをPUTで返す
    return respond_models.AskQuestionResponse(answer=result['answer'], status="ok")


def qdrants_load(collection_name):
    client = QdrantClient(path=QDRANT_PATH, port=6333)

    # すべてのコレクション名を取得
    collections = client.get_collections().collections
    collection_names = [collection.name for collection in collections]

    # コレクションが存在しなければ作成
    if collection_name not in collection_names:
        # コレクションが存在しない場合、新しく作成します
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
        )
        print('collection created')

    return Qdrant(
        client=client,
        collection_name=collection_name,
        embeddings=EMBEDDING_MODEL
    )
