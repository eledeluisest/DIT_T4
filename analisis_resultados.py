from collections import Counter
import nltk
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from importlib import reload

TEXTO_LINGUA = 'LINGUATAGGERTEST.txt'
TEXTO_TAGERTREE = 'TAGGERTREETEST.txt'
TEXTO_TAGGED = 'TEST_SOURCECODE.txt'


# Lectura del fichero de texto TEST_SOURCECODE
text_tag = []
with open(TEXTO_TAGGED) as f:
    text = [x for x in [x.replace('\n', '').split(' ') for x in f.readlines()]]
for t in text:
    text_tag.extend(t)
freqdist = nltk.FreqDist()
words = text_tag
fd_tag = nltk.FreqDist(word.lower() for word in words)
print(len(words))

word_df = pd.DataFrame([word.lower() for word in words], columns=['palabra'])
word_df['word'] = word_df['palabra'].apply(lambda x: x.split('/')[0] if '/' in x else None)
word_df['tag'] = word_df['palabra'].apply(lambda x: x.split('/')[1] if '/' in x else None)

# Lectura del resultado de LINGUA
text_tag = []
with open(TEXTO_LINGUA) as f:
    text = [x for x in [x.replace('\n', '').split(' ') for x in f.readlines()]]
for t in text:
    text_tag.extend(t)
freqdist = nltk.FreqDist()
words_lingua = text_tag
fd_tag = nltk.FreqDist(word.lower() for word in words_lingua)
print(len(words_lingua))
# Lectura del resultado de TREETAGER
treetag_df = pd.read_csv(TEXTO_TAGERTREE, sep='\t', names=['word', 'tag', 'lemma'])
treetag_df = treetag_df.loc[treetag_df['tag'] != "''", :]
print(len(treetag_df))
# Tratamiento de datos
treetag_df['palabra'] = treetag_df['word'].str.lower()
treetag_df['key'] = treetag_df['word'] + '/' + treetag_df['tag']

lingue_df = pd.DataFrame([(x.split('/')[0], x.split('/')[1]) for x in words_lingua if x != ''],
                         columns=('palabra', 'tag'))

len(lingue_df['tag'].value_counts())
len(treetag_df['tag'].value_counts())

etiquetas = pd.merge(lingue_df[['tag']].drop_duplicates().assign(lingue=1),
                     treetag_df[['tag']].drop_duplicates().assign(treetag=1), on='tag', how='outer')

etiquetas['tag_copy'] = etiquetas['tag']
etiquetas_no_match = etiquetas.loc[etiquetas.lingue.isnull() | etiquetas.treetag.isnull(), :]
match = etiquetas.loc[~(etiquetas.lingue.isnull() | etiquetas.treetag.isnull()), :].set_index('tag_copy').to_dict()[
    'tag']
mapping = pd.read_csv('mappings.txt', sep='\t', header=0).set_index('tag').to_dict()['treetag']
print(len(match))
print(len(mapping))
mapping.update(match)
print(len(mapping))
lingue_df['etiqueta_lingua'] = lingue_df.tag.map(mapping)
treetag_df['etiqueta_tree'] = treetag_df.tag
del lingue_df['tag']
del treetag_df['tag']

lingue_df['palabra_lingua'] = lingue_df['palabra']
treetag_df['palabra_tree'] = treetag_df['palabra']
del lingue_df['palabra']
del treetag_df['palabra']
del treetag_df['lemma']
del treetag_df['key']
del treetag_df['word']
lingue_df2 = pd.concat(
    [lingue_df.iloc[:125], pd.DataFrame([["``", "``"]], columns=['etiqueta_lingua', 'palabra_lingua']),
     lingue_df.iloc[125:]]).reset_index(drop=True)
lingue_df3 = pd.concat(
    [lingue_df2.iloc[:293], pd.DataFrame([["``", "''"]], columns=['etiqueta_lingua', 'palabra_lingua']),
     lingue_df2.iloc[293:]]).reset_index(drop=True)

total = pd.concat([lingue_df3.reset_index(drop=True), treetag_df.reset_index(drop=True)], axis=1)
# ttg_tmp = treetag_df.loc[treetag_df['tag'].isin(etiquetas_no_match.dropna(subset=['treetag']).tag.values),:].head(100)
outfile = False
if outfile:
    etiquetas_no_match.to_csv('etiquetado_manual.csv', sep=';')
# Eliminamos la fila 40
# total[~(total['palabra_lingua'].str.lower() == total['palabra_tree'])].head(10)


len(total)

map_res = word_df.set_index('word').to_dict()['tag']

total['res'] = total['palabra_tree'].map(map_res)

tags_source = total[['res']].drop_duplicates()
tags_source['res'] = tags_source['res'].str.upper()
tags_source['mapeo'] = total['res'].map(mapping)

tags_source.to_csv('correspondencia_tags.csv',sep=';')
total['etiqueta_tree'].drop_duplicates().to_csv('patron_etiquetas.csv',sep=';')
total.to_csv('resultados.csv',sep=';')

corr_tag = pd.read_csv('correspondencia_tags.csv', sep=';')
mappings =  corr_tag.set_index('res').to_dict()['mapeo']
total['res_mapped'] = total['res'].str.upper().map(mappings)

total.loc[~total.loc[:,'res_mapped'].isna(),'res'] = total.loc[~total.loc[:,'res_mapped'].isna(),'res_mapped']

print((total['etiqueta_lingua'].str.lower() == total['res'].str.lower()).sum()/len(total)*100)
print((total['etiqueta_tree'].str.lower() == total['res'].str.lower()).sum()/len(total)*100)
print(len(total))
total['ok_lingua'] = (total['etiqueta_lingua'] == total['res'])*1
total['ok_tree'] = (total['etiqueta_tree'] == total['res'])*1
del total['res_mapped']
total.to_csv('resultados.csv',sep=';')

# Algunos errores
total.loc[total.ok_lingua == 0,:].tail()
