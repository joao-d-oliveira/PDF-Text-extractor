import time
import pandas as pd
import tabula
import os

BASEPATH = "/".join(__file__.split('/')[:-1]) + '/'


def process_allfiles_folder(filepath, cols, outpname):
    mergedDF = pd.DataFrame(columns=cols)
    totalLines = 0
    for i, f in enumerate(os.listdir(BASEPATH + filepath)):
        start = time.time()
        if not f.endswith('.pdf'): continue

        dfs = tabula.read_pdf(BASEPATH + filepath + f, pages='all', multiple_tables = True)

        for d, df in enumerate(dfs):
            if df.shape[1] == len(cols) + 1:
                df.iloc[:, 0] = df.apply(lambda x: str(x[0]) if pd.notna(x[0]) else '' + str(x[1]) if pd.notna(x[1]) else '', axis=1)
                df = df.drop(df.columns[1], axis=1)
            elif df.shape[1] == len(cols) - 1:
                df['new'] = ''
                df = df[df.columns[0], 'new', df.columns[-1]]
            elif df.shape[1] != len(cols): print(f'error at nº cols at file {f}, page {d} ({df.shape[1]} cols)')
            tmprow = df.columns

            df.columns = cols
            df = df.append({c:t for c,t in zip(df.columns, tmprow)}, ignore_index=True)
            mergedDF = pd.concat([mergedDF, df], axis=0)
            totalLines += len(df)
        print(f'\rProcessed file # {i:<4} ({f:<25}) took {time.time() - start} seg', end='')

    mergedDF.to_csv(BASEPATH + outpname, index=False)
    print('total lines', totalLines)


def process_file(filename, cols, outpname):
    mergedDF = pd.DataFrame(columns=cols)
    totalLines = 0

    start = time.time()

    dfs = tabula.read_pdf(BASEPATH + filename, pages='all', multiple_tables=True)

    for d, df in enumerate(dfs):
        tmprow = df.columns
        df.columns = cols[:len(df.columns)]
        df = df.append({c: t for c, t in zip(df.columns, tmprow)}, ignore_index=True)
        if len(cols) != len(df.columns):
            k = 0
        mergedDF = pd.concat([mergedDF, df], axis=0)
        totalLines += len(df)
    print(f'\rProcessed file # ({filename:<25}) took {time.time() - start} seg', end='')

    mergedDF.to_csv(BASEPATH + outpname, index=False, encoding='utf_32')
    print('total lines', totalLines)


if __name__ == '__main__':
    filepath = 'output/'
    outppath = 'outputCSV/'
    filename = "pdfs/Nomes Próprios.pdf"
    outpname = "outputCSV/Nomes_Próprios.csv"

    cols = ['Genero', 'Nome', 'empty', 'Genero2', 'Nome2']
    process_file(filename, cols, outpname)
    #process_allfiles_folder(filepath, cols, outpname)