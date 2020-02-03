# Vamos a describir el texto de prueba, miraremos:
# 1.- Número de palabras diferentes
# 2.- Número de etiquetas diferentes
# 3.- Número de palabras iguales con dos o más etiquetas diferentes

TEXTO = "TEST.txt"
TEXTO_TAGGED = "TEST_SOURCECODE.txt"

import nltk
import pandas as pd

# sys.setdefaultencoeding('utf8')
# Lectura del fichero de texto TEST
text_notag = []
with open(TEXTO) as f:
    text = [x for x in [x.replace('\n', '').split(' ') for x in f.readlines()]]
for t in text:
    text_notag.extend(t)

freqdist = nltk.FreqDist()
words = text_notag
fd = nltk.FreqDist(word.lower() for word in words)
print(len(words))

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
# 5 Palabras con ambigüedad
palabras = word_df.dropna().groupby(['word'])['tag'].nunique().sort_values().tail(5).index.values
print(word_df.groupby(['word', 'tag']).count().reset_index().loc[
      word_df.groupby(['word', 'tag']).count().reset_index().word.isin(palabras), :])

print(' TOTAL PALABRAS DIFERENTES')
print(len(word_df.dropna().groupby(['word']).count()))
print(' TOP PALABRAS ')
print(word_df.dropna().groupby(['word']).count().sort_values(by='tag', ascending=False).head(10))
print('-*' * 50)
print(' TOTAL ETIQUETAS DIFERENTES')
print(len(word_df.dropna().groupby(['tag']).count()))
print(' TOP ETIQUETAS ')
print(word_df.dropna().groupby(['tag']).count().sort_values(by='word', ascending=False).head(10))
