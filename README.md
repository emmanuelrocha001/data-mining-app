# Movie Search Engine


free form search on plot overviews
## Dataset:
https://www.kaggle.com/rounakbanik/the-movies-dataset


## Dependencies:
csv, nltk, numpy, json, flask, pandas <br/>
Python 3.7

## app url
http://emmanuelrocha001.pythonanywhere.com/

## How to run locally:
python app.py <br/> <br/>
runs on localhost:5000
 

## Dataset pre-processing
### Tokenization
  __[1]:__ change casing to lowercase <br/>
  __[2]:__ remove punctuation <br/>
  __[3]:__ filter out stop-words <br/>

### Posting Lists

dataset tokens are processed and a json file is generated with the following data<br/><br/>
__term__: unique word in the dataset<br/>
__frequency__: number of times the term appears in the dataset<br/>
__posting list__: documents in which the word appears<br/><br/>
__example__

| term         | frequency      |  posting list |
| :---         |     :---:      |          ---: |
| led          | 484            | \[0, 218, 372, 443...\]  |

## Document Ranking

### Term frequency
__TF(t):__ ( Number of times term t appears in a document ) / ( Total number of terms in the document )
### Inverse Document Frequency
__IDF(t):__ log ( Total number of documents / Number of documents with term t in it ).
### Term frequency-Inverse document frequency
__TF-IDF(t):__ tf(t) x idf(t)
### Overall Document Score
__Score:__  sum of the tf-idf for each term in the query

## Challenges
