import re
def fn1():
    with open('godaan-chap1-hindi.txt', 'r', encoding='utf-8') as f:
        txt = f.read()
        txt = txt.replace('\n','')
        txt = re.split(r'\।', txt)
        #print(txt)

    with open('godaan-english.txt', 'r', encoding='utf-8') as f1:
        txt1 = f1.read()
        txt1 = txt1.replace("'",'')
        txt1 = txt1.replace('"','')
        txt1 = re.split(r'\.', txt1)
    mylen = max(len(txt1), len(txt))
    for i,t in enumerate(txt):
        if i < len(txt1):
           print(txt[i],'\n',txt1[i])
        else:
            print(txt[i])
    if len(txt1) > len(txt):
        for i in range(len(txt), len(txt1)):
            print(txt1[i])
def is_devanagari(text):
    # Devanagari script Unicode range: U+0900 to U+097F
    devanagari_pattern = re.compile('[\u0900-\u097F]')
    return bool(devanagari_pattern.search(text))

def fn2():
    hindi_line = True
    devanagri_line = ''
    english_line = ''
    hindi_txt = []
    english_txt = []
    with open('godaan-hindi-english-translated.txt', 'r',encoding='utf-8') as f:

        for line in f:
            if is_devanagari(line):
                if not hindi_line:
                   english_txt.append(english_line)
                   english_line = ''
                   hindi_line = True
                devanagri_line += line

            else:
                if hindi_line:
                   hindi_txt.append(devanagri_line)
                   devanagri_line = ''
                   hindi_line = False
                english_line += line
    f.close()
    # The last line in the file is english translation
    english_txt.append(english_line)
    print(len(hindi_txt), len(english_txt))
    for i,t in enumerate(hindi_txt):
        print(hindi_txt[i], english_txt[i])
if __name__ == '__main__':
    fn2()




