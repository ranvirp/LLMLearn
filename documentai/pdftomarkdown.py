import pymupdf4llm
import pathlib
pdf_file = "/Users/ranvirprasad/Downloads/A_Samikshaa_2024_25_Book_29Jan_2025.pdf"
# convert the document to markdown
md_text = pymupdf4llm.to_markdown(pdf_file)

# Write the text to some file in UTF8-encoding
pathlib.Path("output.md").write_bytes(md_text.encode())