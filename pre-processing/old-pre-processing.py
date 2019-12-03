from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import RegexpStemmer
from nltk.tokenize import word_tokenize
# from nltk.stem.snowball import SnowballStemmer
from nltk.stem.lancaster import LancasterStemmer
import pandas
import json
import re
import timeit

class FeatureSet:
    def __init__( self, document_id, genre):
        self._document_id = document_id
        self._genres = None
        self._genre = genre
        self._terms = {}

    def addGenre( self, genre ):
        self._genres.append( genre )

    def incrementFrequency(self, term):
        if term not in self._terms.keys():
            self._terms.update( { term: 1 } )
        else:
            self._terms[ term ] = self._terms[ term ] + 1


class Token:
    def __init__( self, term):
        self._term = term
        self._documents = []
    def addDocument(self, document):
        if document not in self._documents:
            self._documents.append( document )

data = pandas.read_csv( 'processed-data/movies.csv' )

# iterate through rows and tokenize
# documents_to_process = 1000

documents_to_process = len( data['genres'] )

unique_genres = {}
feature_sets = []

# start timer for pre-processing
start = timeit.default_timer()

# generate vocabulary
vocabulary = {}
print( 'generating feature sets...')
for i in range( documents_to_process ):

    # cast as string even tho its a fucking string
    current_document = str( data.iloc[ i ][ 'genres' ] )

    # replace ' with ", json string encoding
    current_document = current_document.replace('\'', "\"")
    # load json string as python data structures
    genres = json.loads( current_document )
    # process overview string
    overview_string = str( data.iloc[ i ][ 'overview'] )

    # replace non-alpha characters
    overview_string = re.sub( '[^a-z\s]+','', overview_string, flags=re.IGNORECASE )

    # replace multiple spaces with a single one
    overview_string = re.sub('(\s+)',' ', overview_string )

    # converting string to lower case
    overview_string = overview_string.lower()

    # regex to remove punctuation
    tokenizer =  RegexpTokenizer( r'\w+' )

    # initial tokenization
    tokenized_string = tokenizer.tokenize( overview_string )
    # stemmer to remove plurals
    stemmer = RegexpStemmer( 's$|ies$' )

    # remove stop words
    stop_words = set( stopwords.words('english') )
    # tokens = []


    # generate feature set for current document
    document_id = i
    # only account for the first genre
    feature_set = FeatureSet( i, genre['name'][0] )

    # add genres
    # for genre in genres:
    #     feature_set.addGenre( genre['name'][0] )
    #     # add to unique genre list
    #     if genre['name'] not in unique_genres.keys():
    #         unique_genres.update( { genre['name']: 1 } )
    #     else:
    #         unique_genres[ genre['name'] ] = unique_genres[ genre['name'] ] + 1


    # add tokens and their frequency
    # append non stop words to tokens
    # append documents its in

    for word in tokenized_string:
        if word not in stop_words:
            # make plurals singular
            token = stemmer.stem( word )
            # tokens.append( token )
            feature_set.incrementFrequency( token )
            if token not in vocabulary.keys():
                # print( token )
                document_list = []
                vocabulary.update( {token: [ i ] })
            else:
                if i not in vocabulary[ token ]:
                    vocabulary[ token ].append( i )

    feature_sets.append( feature_set )
# print(  vocabulary )
# calculate genre probability
print('generating unique genre info...')
unique_genre_probabilities = {}
for name in unique_genres.keys():
    # calculatioon
    probability = unique_genres[ name ] / documents_to_process
    unique_genre_probabilities.update({ name: { 'total_number_words': unique_genres[ name ], 'probability': probability }})


tokens = {}

print( 'generating term info for vocabulary...')
for word in vocabulary.keys():
    # calculate number of times word appears in each category
    current_frequencies = {}
    for g in unique_genre_probabilities.keys():
        current_frequencies.update( { g: 0 } )

    for g in unique_genre_probabilities.keys():
        for i in vocabulary[ word ]:
            if g in feature_sets[i]._genres:
                current_frequencies[ g ] = current_frequencies[ g ] + feature_sets[i]._terms[ word ]
                    # print( 'word not in current document')
    tokens.update({ word: current_frequencies })



# # document index is the same as document id
data_json = { 'vocabulary_size': len(vocabulary), 'unique_genres': unique_genre_probabilities, 'terms': tokens }
# for _set in feature_sets:
#     data_json[ 'feature_sets']. append( {
#         'document_id': _set._document_id,
#         'genres': _set._genres,
#         'terms': _set._terms,
#     })






# dump json file
with open( 'processed-data/genre_tokens.json', 'w' ) as outfile:
    json.dump( data_json, outfile )


# end timer
stop = timeit.default_timer()

# # open file to test
# with open( 'processed-data/feature_sets.json' ) as json_file:
#     loaded_feature_sets = ( json.load( json_file ) )

# # for item in loaded_feature_sets:
# #     print( item )
# #number of documents

time = stop - start
print(f'\n\n\ntotal documents: { documents_to_process }')
print(f'time to process: {time} seconds')
print( f'vocabulary size: {len(vocabulary)}')
print( f'json file successfully dumped' )
# print( loaded_feature_sets['unique_genres'] )
# print( loaded_feature_sets[0] )

# print( feature_sets )

