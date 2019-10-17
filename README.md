# search-engine


free from search on a dataset of 44,506 documens( search is done on plot overviews )
### Dataset:
https://www.kaggle.com/rounakbanik/the-movies-dataset


### Dependancies: <br/>
csv, nltk, numpy, json, flask, pandas
(requires Python 3.7 )

### How to run:
python app.py <br/>
( runs on localhost:5000 or localhost:5000/search )

TFIDF Calculation
Term Frequency(TF) * Inverse Document Frequency (IDF) = TF-IDF

t = term (word)

d = document (set of words)

N = count of docs

TF = count of t in d / num words in d

DF = occurence of t in documents

IDF = log(N/(DF +1))

TF-IDF = TF * IDF

Challenges
