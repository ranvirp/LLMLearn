import re
with open('godaan-chap1-hindi.txt', 'r', encoding='utf-8') as f:
    txt = f.read()
    txt = re.split(r'\?|\।', txt)

with open('godaan-english.txt', 'r', encoding='utf-8') as f1:
    txt1 = f1.read()
    txt1 = re.split(r'\?|\.', txt1)
for i,t in enumerate(txt1):
  print(txt[i].strip(), txt1[i].strip())