import PyPDF2
import numpy as np
import pandas as pd

def treatText(txt):
    import re
    out = []
    startedStr = False
    refound = re.findall("-\d{5}.\d", txt)
    if len(refound) > 0:
        for wd in refound: txt = txt.replace(wd, ';')
    for c in txt:
        if c == ')': startedStr = False
        elif c == '(': startedStr = True
        elif startedStr or c == ';': out.append(c)
    return "".join(out)


if __name__ == '__main__':
    COUNT_SKIPS = 1
    COUNT_COLS = 4
    # creating a pdf reader object
    fileReader = PyPDF2.PdfFileReader(open('pdfs/vacinacao_covid_COMPLETO_CE_29_03_2021.pdf', 'rb'))
    # print the number of pages in pdf file
    page = fileReader.getPage(0)

    cont = page.get('/Contents')
    pageTxt = ""
    for c in cont:
        obj_data = c.getObject().flateEncode().getData()
        obj_data = obj_data.decode('latin', 'replace')

        pageTxt += ";".join([treatText(o) for o in obj_data.split('\n') if 'TJ' in o.upper()])

    pageTxt = [txt for txt in pageTxt.split(';') if 'Página' not in txt]

    print(fileReader.numPages)


