from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import word_tokenize
from nltk.stem import RegexpStemmer
from nltk.stem.lancaster import LancasterStemmer

import re
import pandas
import json
import numpy
import timeit
import os
import operator
import math

# import pre-processed data
CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))
data_tokens = {}

# read csv
print( 'loading dataset...' )

movies_csv = pandas.read_csv( os.path.join( CURRENT_FOLDER, 'pre-processing/processed-data/movies.csv' ) )
print( 'loading pre-processed data...' )

# read json and convert back to dictionary
with open( os.path.join( CURRENT_FOLDER, 'pre-processing/processed-data/genre_tokens.json' ) ) as json_file:
    data = ( json.load( json_file ) )

genre_tokens = data['terms']
unique_genres = data['unique_genres']
vocabulary_size = data['vocabulary_size']
# print( unique_genres )
def cleanText( raw_text ):
    text = raw_text

    # replace non-alpha characters
    text = re.sub( '[^a-z\s]+','', text, flags=re.IGNORECASE )

    # replace multiple spaces with a single one
    text = re.sub('(\s+)',' ', text )

    # converting string to lower case
    text = text.lower()

    # regex to remove punctuation
    tokenizer =  RegexpTokenizer( r'\w+' )

    # initial tokenization
    tokenized_text = tokenizer.tokenize( text )
    # stemmer to remove plurals
    stemmer = RegexpStemmer( 's$|ies$' )

    # remove stop words
    stop_words = set(['whom', 'that', 'those', "needn't", 'where', 'has', 'same', 'had', 'we', 'my', 'hers', 'does', 'they', 'the', 'only', "doesn't", 'be', 'mightn', 'her', 'wasn', 'being', 'am', 'but', 'themselves', 'during', "don't", 'into', 'its', 'isn', 'of', 'won', 'few', 'as', 'own', 'more', "shouldn't", 'myself', "mightn't", 'after', 'below', "didn't", "you've", 'wouldn', 'any', 'his', 'in', 'hasn', "weren't", 'him', 'she', 'will', "won't", 'it', 'y', 'he', 'now', 'such', 'haven', 'most', 'who', 'an', 'shan', 'at', "she's", 'were', 'weren', 'do', 'did', 've', 'all', 'between', 'above', "you're", 'no', "you'll", 'which', 'i',
'been', 'doesn', "hasn't", 'each', 'some', 'don', "aren't", 'should', 'mustn', 'our', "wouldn't", 'their', 'your', 'yours', 'doing', 'why', "hadn't", 'down', 'so', 'for', 'while', 'this', "shan't", 'there', 'needn', 'up', 'shouldn', 'by', "mustn't", 'have', 'yourself', "you'd", 'd', "haven't", 'about', 'ain', 'or', 'ourselves', 'when', "couldn't", 'is', 'with', "that'll", 'these', 'further', "should've", 'if', 'than', 'just', "wasn't", 'other', "isn't", 'you',
'then', 'how', 'too', 'until', 'very', 'are', 'to', 'itself', 'aren', 't', 'a', 'before', 'm', 'can', 'out', 'and', 'under', 'here', 'o', 'on', 'theirs', 'ma', 'couldn', 'having', 'himself', 'against', 'again', 'll', 'nor', 'hadn', 'ours', 'through', 'both', 'because', 'what', 's', 'them', 'not', 'off', 'me', "it's", 'once', 'over', 'didn', 'was', 're', 'from', 'yourselves', 'herself'])
    clean_text = []
    for word in tokenized_text:
        if word not in stop_words:
            # make plurals singular
            token = stemmer.stem( word )
            clean_text.append( token )

    return clean_text


def calculateProbabilities( text ):
    calculations= {}
    probabilities_words = {}
    probabilities = {}
    for word in text:
        # calculate probability of word being in the current genre
        genre_probabilities = {}
        calculations.update({ word: {} })
        for genre in unique_genres.keys():

            # number of apperances of the word in the current genre
            if( genre_tokens.get( word ) != None ):
                word_apperances_in_genre = ( genre_tokens[ word ][ genre ] )
                # print(f'{word} apperances in { genre }: {word_apperances_in_genre}')
            else:
                word_apperances_in_genre = 0
                # print(f'{word} apperances in { genre }: {word_apperances_in_genre}')

            # total number of words in current genre
            total_words_in_genre = ( unique_genres[ genre ][ 'total_number_words'] )
            # print(f'total words in {genre}: {total_words_in_genre}')


            # calculate the probability of the current word for the given genre
            probability = ( word_apperances_in_genre + 1 ) / ( total_words_in_genre + vocabulary_size )
            # print(f'probability { word} is in {genre}: {probability}')
            log_probability = math.log10( probability )
            genre_probabilities.update({ genre: probability })

            calculations[word].update({ genre: { 'tf_in_genre': word_apperances_in_genre, 'total_terms_in_genre': total_words_in_genre, 'vocab_size': vocabulary_size, 'raw_probability': probability, 'log_probability': log_probability } })


        # print( genre_probabilities )
        probabilities_words.update({ word: genre_probabilities })
    # print( calculations )
    # use log to prevent underflow
    for genre in unique_genres.keys():
        probability = 0
        for word in text:
            probability = probability + math.log10( probabilities_words[word][genre] )
        # probability = probability * sum_probability
        probabilities.update({ genre: probability })


        # probabilities.update({ word: genre_probabilities })
    # print( max(probabilities.items(), key = lambda x: x[1]) )
    # print( probabilities )

    # sorted_d = dict( sorted(probabilities.items(), key=operator.itemgetter(0),reverse=True))
    sorted_x = sorted(probabilities.items(), key=operator.itemgetter(1),reverse=True)
    percentages = {}
    total_class_probabilities = 0
    for genre in probabilities.keys():
        total_class_probabilities = total_class_probabilities + math.pow(10, probabilities[genre])

    # for genre in probabilities.keys():
    # print( f'\n\npredicted category: {sorted_x[0][0]}\n')

    # info to return
    # append calculations for predicted genre only
    predicted_genre = sorted_x[0][0]
    calculation = { 'terms': {} }
    for t in text:
        calculation['terms'].update( { t: { 'tf_in_genre': calculations[t][predicted_genre]['tf_in_genre'], 'total_terms_in_genre': calculations[t][predicted_genre]['total_terms_in_genre'], 'vocab_size': calculations[t][predicted_genre]['vocab_size'], 'raw_probability': calculations[t][predicted_genre]['raw_probability'], 'log_probability': calculations[t][predicted_genre]['log_probability'] } } )
    results = { 'results': [], 'calculation': calculation }
    for i in range( len( sorted_x ) ):
        genre = sorted_x[i][0]
        current_percentage = round( ( ( math.pow(10,probabilities[genre]) / total_class_probabilities ) * 100 ),2 )
        # append category result info
        results['results'].append({
            'genre': genre, 'score': probabilities[genre], 'percentage': current_percentage,
        })
    print( results )
    return results


def predictGenre( text ):
    clean_text = cleanText( text )
    results = calculateProbabilities( clean_text )
    # append original text to results
    results.update({ 'text': text})
    return results

# text = "the future is filled with machines at war"
# print( predictGenre( text ) )