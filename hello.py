# open the file

# Replacing the "wrong" characters
export_file = open("D:\Christine_Work\Literatur\EndNote\Export.txt", "r")
# Assumption: UTF 8 coding of the endnoteoutput.txt file

text = ""

for line in export_file:
    text += line    

text = text.replace(" & ", " \& ")

text = text.replace("\xc3", "")

text = text.replace("\x96", r'\"O')
text = text.replace("\xb6", r'\"o')

text = text.replace("\x84", r'\"A')
text = text.replace("\xA4", r'\"a')

text = text.replace("\x9f", r'\ss')

text = text.replace("\xa6", r'\ae')

text = text.replace("\xb8", r'{\o}')

text = text.replace("\xc2\xb4", "'")

text = text.replace("\xe2\x80\x9c", r"``")
text = text.replace("\xe2\x80\x9d", r"''")

text = text.replace("\xe2\x80\x98", r"`")
text = text.replace("\xe2\x80\x99", r"'")

text = text.replace("\x9c", r'\"U')
text = text.replace("\xBC", r'\"u')

text = text.replace("#", "")

text = text.replace("\xc5\x8d", "{\=o}")

print(text)
# write to the bibtex file
#f = open("D:\Christine_Work\Literatur\EndNote\Export.bib", "w")
#f.write(text)
#f.flush()
#f.close()
