from pathlib import path
from langchain_community.document_loaders import PyPDFLoader

pdf_path = Path(__file__).parent / "nodejs.pdf"

#Load this file in python

loader = PyPDFLoader(file_path=pdf_path)
docs = loader.load()