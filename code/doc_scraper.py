# -*- coding: utf-8 -*-
# <nbformat>2</nbformat>

# <codecell>

import os
import urllib
import pymongo
import pandas as pd

# <codecell>

doc_file = "../csv/docs_links.csv"
df = pd.read_csv(doc_file)

# <codecell>

def split_bytes(value, divider, position):
    try:
        return value.split(divider)[position]
    except:
        return value

# <codecell>

df['ext_down'] =  df.downloads.apply(lambda x: split_bytes(x, 'bytes/', 1))

# <codecell>

df['ext_doc'] = df.documentation\
.apply(lambda x: split_bytes(x, 'bytes/', 1))\
.apply(lambda x: split_bytes(x, '_metadata', 0))\
.apply(lambda x: split_bytes(x, '.pdf', 0))

# <codecell>

doc_links = df[["documentation","ext_doc"]].dropna()

# <codecell>

c = pymongo.MongoClient('10.154.58.98',27017)
db = c['gis']
collection = db['docs']

# <codecell>

for index, row in doc_links.iterrows():
    try:
        doc_link = row['documentation']
        save_pdf = "../docs/pdf/"+row['ext_doc']+".pdf"
        save_txt = "../docs/txt/"+row['ext_doc']+".txt"
        urllib.urlretrieve(doc_link,save_pdf)
        cmd = """pdftotext {pdf} {txt}""".format(pdf=save_pdf, txt=save_txt)
        os.system(cmd)
        with open(save_txt,"rb") as f:
            collection.insert({'link':doc_link, 'doc':f.read(), 'name':row['ext_doc'] })
    except Exception, e:
        print(e)
        pass

# <codecell>


