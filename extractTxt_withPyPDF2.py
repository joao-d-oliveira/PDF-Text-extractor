from PyPDF2 import PdfFileWriter, PdfFileReader

COUNT_SKIPS = 1
COUNT_COLS = 4
PDF_FILENAME = 'pdfs/Pessoas Cadastradas 25-03-2021_vacineja_compac.pdf'


def treat_text(txt):
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


def split_files(reader, nsplit):
    n = fileReader.numPages
    #n = 11539 #overwrite page number given pdf is broken and empty after page 11539
    k = n // nsplit
    for i in range(0, n, k):
        writer = PdfFileWriter()
        for d in range(i, min(i + k, n), 1): writer.addPage(reader.getPage(d))

        writer.write(open(f'output/output-{i}_{d}.pdf', 'wb'))


def get_txt_from_page(page):
    cont = page.get('/Contents')
    pageTxt = ""
    for c in cont:
        obj_data = c.getObject().flateEncode().getData()
        obj_data = obj_data.decode('latin', 'replace')
        # print([o for o in obj_data.split('\n') if 'TJ' in o.upper()])

        pageTxt += ";".join([treat_text(o) for o in obj_data.split('\n') if 'TJ' in o.upper()])

    pageTxt = [txt for txt in pageTxt.split(';') if 'Página' not in txt]

    return pageTxt


def get_txt_allpages(pdf):
    n = pdf.numPages
    n = 11539 #overwrite page number given pdf is broken and empty after page 11539
    fullPDFtxt = ""
    for i in range(n):
        fullPDFtxt += get_txt_from_page(pdf.getPage(i))

    return fullPDFtxt


if __name__ == '__main__':
    # creating a pdf reader object
    fileReader = PdfFileReader(open(PDF_FILENAME, 'rb'))

    #fulltxt = get_txt_allpages(fileReader)

    split_files(fileReader, 100)

    print('done analysing')

