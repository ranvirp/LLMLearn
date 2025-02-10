1. Embeddings - to transform a text into embeddings either use HuggingFace api or download and use ollama
2. Install additional tools as follows:
     - brew install poppler
     - brew install tesseract
     - pip install -qU "unstructured[pdf]"
   ````python
   from langchain_unstructured import UnstructuredLoader
   loader_local = UnstructuredLoader(
    file_path=file_path,
    strategy="hi_res",
    )
   docs_local = []
   for doc in loader_local.lazy_load():
      docs_local.append(doc)
3. convert pdf page into image
 ```python
import base64
import io

import fitz
from PIL import Image


def pdf_page_to_base64(pdf_path: str, page_number: int):
    pdf_document = fitz.open(pdf_path)
    page = pdf_document.load_page(page_number - 1)  # input is one-indexed
    pix = page.get_pixmap()
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")

    return base64.b64encode(buffer.getvalue()).decode("utf-8")
 ```
4. IPython display
```python
from IPython.display import Image as IPImage
from IPython.display import display

base64_image = pdf_page_to_base64(file_path, 11)
display(IPImage(data=base64.b64decode(base64_image)))
 
```
5. ```python

from langchain_core.messages import HumanMessage

query = "What is the name of the first step in the pipeline?"

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
```
   