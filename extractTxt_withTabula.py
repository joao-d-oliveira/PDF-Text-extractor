import pandas as pd
import tabula
file = "pdfs/vacinacao_covid_COMPLETO_CE_29_03_2021_small.pdf"
BASE_PATH = "/".join(__file__.split('/')[:-1]) + '/'
df = tabula.read_pdf(BASE_PATH + file, pages = '1', multiple_tables = True)
print(df)