from pptx import Presentation
from docx import Document
from pptx.util import Pt
from langchain_community.document_loaders import UnstructuredWordDocumentLoader


class DOCXPPTHindi2English:

    def __init__(self, file_name, fn, docx=False):
        self.fn = fn
        if docx:
            self.prs = None
            self.docx = Document(file_name)
        else:
            self.prs = Presentation(file_name)


    def convert_word(self, save_as=None, save_freq = 10, starting=0):
        i = 0
        for paragraph in self.docx.paragraphs:
            i += 1
            if i < starting: continue
            paragraph.text = self.fn(paragraph.text)
            print('\r',i,'.')
            if (i % save_freq) == 0: self.docx.save(save_as)

        for tbl in self.docx.tables:
            for col in tbl.columns:
                for cell in col.cells:
                    for paragraph in cell.paragraphs:
                            i += 1
                            if i < starting: continue
                            paragraph.text = self.fn(paragraph.text)
                            print('\r', i, '.')
                            if save_as:
                                if (i % save_freq) == 0:self.docx.save(save_as)

        if save_as:
             self.docx.save(save_as)


    def convert(self, save_as=None):
        i = 0
        for slide in self.prs.slides:
            i += 1
            #print(f'slide no {i}')
            for shape in slide.shapes:
                if shape.has_table:
                    #print("table found")
                    for row in shape.table.rows:
                        for cell in row.cells:
                            for paragraph in cell.text_frame.paragraphs:
                                paragraph.text = self.fn(paragraph.text)
                if not shape.has_text_frame:
                    continue
                for paragraph in shape.text_frame.paragraphs:
                    paragraph.text = self.fn(paragraph.text)
        if save_as: self.prs.save(save_as)

    def save(self, file_name):
        if file_name: self.prs.save(file_name)

class LangChainDocx:
    def __init__(self, path):
        loader = UnstructuredWordDocumentLoader(path)
        self.data = loader.load()
if __name__ == '__main__':
    from hindi2englishml import hindi2english
    #word_path = '/Users/ranvirprasad/Downloads/02.docx'
    #lc = LangChainDocx(word_path)
    #print(lc.data)


    converter = DOCXPPTHindi2English('All_Chap_english.docx', docx=True, fn=hindi2english)
    converter.convert_word(save_as='All_Chap_english.docx', starting=61)
    #converter1 = PPTKruti2Unicode('/Users/ranvirprasad/Downloads/Rahul Gahlot Shikayat Aakhya New - Final.docx', docx=True)
    #converter1.convert_word('converted_word2.docx')
