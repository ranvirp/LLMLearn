from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from langchain_unstructured import UnstructuredLoader
from unstructured.cleaners.core import clean_extra_whitespace
#for document loader install
# # base dependencies
# brew install libmagic poppler tesseract
# If parsing xml / html documents:
# brew install libxml2 libxslt
def load_documents(file_paths):
    '''

    :param file_paths: list of document file_paths
    :return:
    '''
    loader = UnstructuredLoader(
        file_paths,
        post_processors=[clean_extra_whitespace],
    )
    docs = loader.load()
    return docs

def create_faiss_vector_store(docs:list[Document]):
    return FAISS.from_documents(documents=docs, embedding=OllamaEmbeddings(model="all-minilm:l12-v2"))

def create_retriever(docs:list[Document]):
    embedder = OllamaEmbeddings(model="all-minilm:l12-v2")
    vector = FAISS.from_documents(documents=docs, embedding=embedder)
    return vector.as_retriever(search_type="similarity", search_kwargs={"k": 3})
def test_vector_search():
    docs = load_documents(['02_english.docx'])
    vector_store = create_faiss_vector_store(docs)
    while True:
        query = input("your query here: ")
        res = vector_store.similarity_search(query, k=2)
        for doc in res:
            print(doc.metadata.get('source','unknown'), ':', doc.page_content)
