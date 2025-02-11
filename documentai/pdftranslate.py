import json
import pathlib

from langchain_unstructured import UnstructuredLoader


class PDFHindi2English:

    def __init__(self, file_name, fn, pdf=False):
        self.fn = fn
        self.file_name = file_name
        self.docs_local = []
        if pdf:
            loader_local = UnstructuredLoader(
                file_path=file_name,
                strategy="hi_res",
            )

            for doc in loader_local.lazy_load():
                self.docs_local.append(doc)
        if pathlib.Path(file_name + '_tmp').exists():
            print(file_name+'_tmp')
            with open( file_name + '_tmp', 'r') as f:
                try:
                   self.storage_dict = json.load(f)
                   f.close()
                except:
                    raise Exception("prior session does not exist. Set prev_session to False and run again")
        else:
            self.storage_dict = {}
        #print(self.docs_local)
    def serialize_storage_dict(self):
        with open(self.file_name + '_tmp', 'w') as f:
            json.dump(self.storage_dict,f)

    def get_text_from_doc(self, doc):
        return doc.page_content

    def import_from_dict(self):
        i = 0
        total = len(self.docs_local)
        print("total parts to be translated:", total)
        for doc in self.docs_local:
            if str(i) in self.storage_dict:
                doc.page_content = self.storage_dict[str(i)]
            i += 1
    def convert_pdf_intermediate(self,  save_freq = 10,starting=0):
        i = 0
        total = len(self.docs_local)
        print("total parts to be translated:", total)
        for doc in self.docs_local:
            txt = self.get_text_from_doc(doc)
            if i < starting: continue
            if str(i) in self.storage_dict: continue
            self.storage_dict[str(i)] = self.fn(txt)
            i += 1
            print(i, f'/{total}', end='.')
            if (i % save_freq) == 0: self.serialize_storage_dict()



        self.serialize_storage_dict()
if __name__ == '__main__':
    from hindi2englishml import hindi2english
    #word_path = '/Users/ranvirprasad/Downloads/02.docx'
    #lc = LangChainDocx(word_path)
    #print(lc.data)

    file_name = '/Users/ranvirprasad/Downloads/Ch_09_Industry.pdf'
    converter = PDFHindi2English(file_name, pdf=True, fn=hindi2english)
    converter.convert_pdf_intermediate()
