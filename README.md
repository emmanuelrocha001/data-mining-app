# search-engine


Movie search, search plot overviews. <br/> <br/>
### dataset:
https://www.kaggle.com/rounakbanik/the-movies-dataset


### dependancies: <br/>
csv, nltk, numpy, json, flask, pandas

### environment: <br/>
Python 3.7

### how to run
run: python app.py <br/>
runs on localhost:5000 or localhost:5000/search

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
