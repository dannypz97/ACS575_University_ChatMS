"""
# !pip install langchain
# !pip install huggingface_hub
# !pip install faiss-gpu
# !pip install sentence_transformers
# !pip install google.generativeai
# pip install dill
# """

from langchain.llms import GooglePalm
from langchain.embeddings import GooglePalmEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.document_loaders import TextLoader
from langchain.chains.question_answering import load_qa_chain
import traceback
import dill



from dotenv import load_dotenv
load_dotenv()
DEFAULT_DB_DILL_PATH="DB.dill"
DEFAULT_CHAIN_DILL_PATH="CHAIN.dill"


def train(path_to_data,university):
    global DB, CHAIN
    # loader = TextLoader(path_to_data)
    # documents = loader.load()

    # # Convert the content into raw text.
    raw_text = str(path_to_data)
    # for i, doc in enumerate(documents):
    #     text = doc.page_content
    #     if text:
    #         raw_text += text

    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=200,
        chunk_overlap=40,
        length_function=len,
    )
    texts = text_splitter.split_text(raw_text)

    embeddings = GooglePalmEmbeddings()
    DB = FAISS.from_texts(texts,embeddings)
    CHAIN = load_qa_chain(GooglePalm(), chain_type="stuff")
    

    with open("backend/models/"+str(university)+DEFAULT_DB_DILL_PATH, "wb") as f:
        dill.dump(DB, f)
    with open("backend/models/"+str(university)+DEFAULT_CHAIN_DILL_PATH, "wb") as f:
        dill.dump(CHAIN, f)

    return DB, CHAIN


def test(query,university, **kwargs):
    with open("backend/models/"+str(university)+DEFAULT_DB_DILL_PATH, "rb") as f:
        DB = dill.load(f)
    with open("backend/models/"+str(university)+DEFAULT_CHAIN_DILL_PATH, "rb") as f:
        CHAIN = dill.load(f)

    docs = DB.similarity_search(query)
    try:
        result = CHAIN.run(input_documents=docs, question=query).strip()
        return result

    except (IndexError, AttributeError) as e:
        print(traceback.format_exc())
        return None


# DB = CHAIN = None
# with open(DEFAULT_DB_DILL_PATH, "rb") as f:
#     DB = dill.load(f)
# with open(DEFAULT_CHAIN_DILL_PATH, "rb") as f:
#     CHAIN = dill.load(f)
# train()
# test(query)