# Movie Search Engine


free form search on a dataset of 44,506 documents( search is done on plot overviews )
## Dataset:
https://www.kaggle.com/rounakbanik/the-movies-dataset


## Dependencies:
csv, nltk, numpy, json, flask, pandas
(requires Python 3.7 )

## How to run:
python app.py <br/> <br/>
( runs on localhost:5000 or localhost:5000/search )


## Dataset pre-processing

## Document Ranking

### Term frequency
__TF(t):__ ( Number of times term t appears in a document ) / ( Total number of terms in the document )
### Inverse Document Frequency
__IDF(t):__ log ( Total number of documents / Number of documents with term t in it ).
### Term frequenct-Inverse document frequency
__TF-IDF(t):__ tf(t) x idf(t)
### Overall document score
__Score:__  sum of the tf-idf for each term in the query

## Challenges
