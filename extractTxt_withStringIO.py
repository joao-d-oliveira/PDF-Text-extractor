from io import StringIO
from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams

output = StringIO()

with open('pdfs/vacinacao_covid_COMPLETO_CE_29_03_2021_small.pdf', 'rb') as pdf_file:
    extract_text_to_fp(pdf_file, output, laparams=LAParams(), output_type='html', codec=None)
with open('pdfs/vacinacao_covid_COMPLETO_CE_29_03_2021_small.html', 'a') as html_file:
    html_file.write(output.getvalue())
