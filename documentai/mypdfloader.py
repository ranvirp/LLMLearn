import json
import os
import streamlit as st
from langchain.chains.combine_documents.stuff import StuffDocumentsChain, create_stuff_documents_chain
from langchain.chains.llm import LLMChain
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import OllamaEmbeddings #, HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.messages import HumanMessage

import base64
import io
import fitz
from PIL import Image
async def get_pages_from_pdf(file_path):
    '''

    :param file_path: path of pdf file
    :return: list of langchain Document which has params page_content and metadata
    '''
    loader = PyPDFLoader(file_path)
    pages = []
    async for page in loader.alazy_load():
        pages.append(page)
    return pages
def inmemory_vector_search_using_ollama(pages, query, k=2, model_name="llama3:8b", embeddings_model="all-minilm:l12-v2"):
    embeddings = OllamaEmbeddings(model_name=embeddings_model)
    vector_store = InMemoryVectorStore.from_documents(pages, embeddings)
    docs = vector_store.similarity_search(query, k=k)
    for doc in docs:
        print(f'Page {doc.metadata["page"]}: {doc.page_content[:300]}\n')

def pdf_page_to_base64(pdf_path: str, page_number: int):
    pdf_document = fitz.open(pdf_path)
    page = pdf_document.load_page(page_number - 1)  # input is one-indexed
    pix = page.get_pixmap()
    img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")

    return base64.b64encode(buffer.getvalue()).decode("utf-8")

def build_prompt():
    prompt = """
    1. Use the following context to answer the question.
    2. If you don't know the answer, say "I don't know."
    3. Keep the answer concise (3-4 sentences).

    Context: {context}

    Question: {question}

    Helpful Answer:"""
    return PromptTemplate.from_template(prompt)

def build_qa_chain(retriever, llm):
    prompt = build_prompt()
    llm_chain = LLMChain(llm=llm, prompt=prompt, verbose=True)
    document_prompt = PromptTemplate(
        input_variables=["page_content", "source"],
        template="Context:\ncontent:{page_content}\nsource:{source}",
    )
    combine_documents_chain = StuffDocumentsChain(
        llm_chain=llm_chain,
        document_variable_name="context",
        document_prompt=document_prompt,
    )
    return RetrievalQA(
        combine_documents_chain=combine_documents_chain,
        retriever=retriever,
        return_source_documents=True,
    )
def create_retriever(strs:list, source="PDF"):
    #docs = json.loads(docs_json)
    #embedder = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    embedder = OllamaEmbeddings(model_name="all-minilm:l12-v2")
    vector = FAISS.from_texts(
        strs,
        embedder,
        metadatas=[{"source": source} for _ in strs]
    )
    return vector.as_retriever(search_type="similarity", search_kwargs={"k": 3})
def chunk_documents(docs):
    '''

    :param docs: Array of langchain.base.Document
    :return:
    '''
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return text_splitter.split_documents(docs)

def get_llm(model="llama3:8b"):
    return OllamaLLM(model=model)


def load_pdf(file):
    with open("temp.pdf", "wb") as f:
        f.write(file.getvalue())
    loader = PyPDFLoader("temp.pdf")
    return loader.load()

def infer_from_image_llm(llm, query,  base64_image):
    #query = "What is the name of the first step in the pipeline?"
    '''
    messages = [
        {
            "role": "user",
            "content": [{
                "type": "text",
                "text": 'You are a helpful assistant. Answer the following user query in 1 or 2 sentences: ' + user_query
            },
            {
                "type": "image_url",
                "image_url": {
                "url": f"data:image/jpeg;base64,{image}",
                }
            }]
        }
    ]

    :param llm:
    :param query:
    :param uri:
    :param uritype:
    :return:
    '''
    message = HumanMessage(
        content=[
            {"type": "text", "text": query},
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
            },
        ],
    )
    response = llm.invoke([message])
    print(response.content)

def summarize(llm, docs):
    # Define prompt
    prompt = ChatPromptTemplate.from_messages(
        [("system", "Write a concise summary of the following:\\n\\n{context}")]
    )

    # Instantiate chain
    chain = create_stuff_documents_chain(llm, prompt)

    # Invoke chain
    result = chain.invoke({"context": docs})
    print(result)
def process_pdf(file):
    loaded_pdf = load_pdf(file)
    print(loaded_pdf)
async def get_docs_pdf(pdf_file):
    docs = await get_pages_from_pdf(pdf_file)
    return docs
def get_response_from_ollama(model,query):
    import requests
    headers = {"Content-Type":"application/json"}
    params = {"model":model, "prompt":query, "stream":False}
    resp = requests.post('http://localhost:11434/api/generate',headers=headers, data=json.dumps(params))
    print(resp.text)
get_response_from_ollama("llama3:8b", "why is sky blue?")
#import asyncio
#pdf_file = '/Users/ranvirprasad/Downloads/cbjescco10.pdf'
#docs = asyncio.run(get_docs_pdf(pdf_file))
#llm = get_llm()
#summarize(llm, docs)
