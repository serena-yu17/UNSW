import re

with open("SMH.html") as f:
    st = f.read()
st=st.replace('\n','')

titles = re.findall('(?:<h\d>.{1,20}<a href=".{1,300}? title=".{1,300}?">)([^<>]{1,300}?)(?:<\/a><\/h\d>)', st)
for line in titles:
    print(line)
