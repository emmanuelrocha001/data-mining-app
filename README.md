# search-engine


free form search on a dataset of 44,506 documents( search is done on plot overviews )
### Dataset:
https://www.kaggle.com/rounakbanik/the-movies-dataset


### Dependancies:
csv, nltk, numpy, json, flask, pandas
(requires Python 3.7 )

### How to run:
python app.py <br/> <br/>
( runs on localhost:5000 or localhost:5000/search )

### TF-IDF Calculation

#### Term frequency
__TF(t):__ ( Number of times term t appears in a document ) / ( Total number of terms in the document )
#### Inverse Document Frequency
__IDF(t):__ LOG ( Total number of documents / Number of documents with term t in it ).

t = term (word)

d = document (set of words)

N = count of docs

TF = count of t in d / num words in d

DF = occurence of t in documents

IDF = log(N/(DF +1))

TF-IDF = TF * IDF

### Challenges
