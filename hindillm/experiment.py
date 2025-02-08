import re
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
print(len(txt1), len(txt))
for i,t in enumerate(txt):
   print(txt[i],txt1[i])