from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import word_tokenize
import pandas
import json

class TokenData:
    def __init__( self ):
        self._frequency = 1
        self._documents = []

    def incrementFrequency(self):
        self._frequency = self._frequency + 1
    def addDocument( self, doc_id ):
        if doc_id not in self._documents:
            self._documents.append( doc_id )

# read csv
data = pandas.read_csv( 'processed-data/movies.csv' )

# iterate through rows and tokenize
# documents_to_process = 10

documents_to_process = len( data['overview'] )

tokens = {}
for i in range( documents_to_process ):
    current_document = data.iloc[ i ][ 'overview' ]
    print( 'processing document %d' % ( i ) )
    # print( current_document )
    # to lower case
    current_document = current_document.lower()
    # regex to remove punctuation
    tokenizer =  RegexpTokenizer( r'\w+' )
    # tokenize
    current_tokens = tokenizer.tokenize( current_document )
    # stop words to be filtered
    stop_words = set(stopwords.words('english'))
    # filter stop words and check if token is already in list

    for token in current_tokens:
        if token not in stop_words:
            if token not in tokens:
                meta_data = TokenData()
                meta_data.addDocument ( i )
                tokens.update( { token: meta_data } )
                # tokens.append( token )
            else:
                tokens[ token ].incrementFrequency()
                tokens[ token ].addDocument( i )


# generate json file
data_json = {}
data_json[ 'tokens' ] = []

# append token
counter = 0
for token in tokens.keys():

    print( 'token %d added to file' % ( counter ) )
    data_json[ 'tokens' ].append({
        'term': token,
        'frequency': tokens[ token ]._frequency,
        'documents': tokens[ token ]._documents
    })

# dump json file
    with open( 'processed-data/tokens.json', 'w' ) as outfile:
        json.dump( data_json, outfile )
print( 'tokenization completed, json file successfully generated')
print( 'total documents processed: %d' % ( documents_to_process )  )
print( 'unique tokens found: %d' % ( len( tokens ) ) )


