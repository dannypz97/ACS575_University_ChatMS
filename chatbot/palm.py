"""
# !pip install langchain
# !pip install huggingface_hub
# !pip install faiss-gpu
# !pip install sentence_transformers
# !pip install google.generativeai
# pip install dill
# """
import dill
from langchain.llms import GooglePalm
from langchain.embeddings import GooglePalmEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
import traceback
import uuid


from dotenv import load_dotenv
load_dotenv()

DEFAULT_DB_DILL_PATH_TEMPLATE = "./resources/{}_DB.dill"
DEFAULT_CHAIN_DILL_PATH_TEMPLATE = "./resources/{}_CHAIN.dill"


def train(data, model_id):
    raw_text = str(data)

    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=200,
        chunk_overlap=40,
        length_function=len,
    )
    texts = text_splitter.split_text(raw_text)

    embeddings = GooglePalmEmbeddings()
    db = FAISS.from_texts(texts, embeddings)
    chain = load_qa_chain(GooglePalm(), chain_type="stuff")

    with open(DEFAULT_DB_DILL_PATH_TEMPLATE.format(model_id), "wb") as f:
        dill.dump(db, f)
    with open(DEFAULT_CHAIN_DILL_PATH_TEMPLATE.format(model_id), "wb") as f:
        dill.dump(chain, f)

    return model_id


def test(query, model_id, **kwargs):
    with open(DEFAULT_DB_DILL_PATH_TEMPLATE.format(model_id), "rb") as f:
        db = dill.load(f)
    with open(DEFAULT_CHAIN_DILL_PATH_TEMPLATE.format(model_id), "rb") as f:
        chain = dill.load(f)

    docs = db.similarity_search(query)
    try:
        result = chain.run(input_documents=docs, question=query).strip()
        return result

    except (IndexError, AttributeError) as e:
        print(traceback.format_exc())
        return None