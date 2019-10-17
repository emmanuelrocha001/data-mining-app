from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import word_tokenize
import pandas
import json

class TokenData:
    def __init__( self ):
        self._frequency = 1
        # self._documents = []
        self._posting_list = {}

    def incrementFrequency(self):
        self._frequency = self._frequency + 1

    # def addDocument( self, doc_id ):
    #     if doc_id not in self._documents:
    #         self._documents.append( doc_id )

    def updatePostingList( self, doc_id, index ):
        if doc_id not in self._posting_list.keys():
            
            self._posting_list.update( { doc_id: [index] } )
        else:
            self._posting_list[ doc_id ].append( index )

# read csv
data = pandas.read_csv( 'processed-data/movies.csv' )

# iterate through rows and tokenize
# documents_to_process = 1000

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
    index = 0
    for token in current_tokens:
        if token not in stop_words:
            # print( token )
            if token not in tokens:
                meta_data = TokenData()
                # meta_data.addDocument ( i )
                # update posting list: i: doc_id, index
                meta_data.updatePostingList( i, index )
                tokens.update( { token: meta_data } )

            else:
                tokens[ token ].incrementFrequency()
                # tokens[ token ].addDocument( i )
                tokens[ token ].updatePostingList( i, index )
            index = index + 1
            # print( tokens[ token ]._posting_list  )
# for token in tokens.keys():
# print( tokens['andy']._posting_list )
# generate json file 
data_json = {}
data_json[ 'tokens' ] = []

# token info
# append term name
# append token frequency
# append document apperances and indices 

counter = 0
for token in tokens.keys():
    print( 'token %d added to file' % ( counter ) )
    counter = counter + 1
    data_json[ 'tokens' ].append({
        'term': token,
        'frequency': tokens[ token ]._frequency,
        'posting_list': tokens[ token ]._posting_list
    })


# dump json file
with open( 'processed-data/tokens.json', 'w' ) as outfile:
    json.dump( data_json, outfile )
print( 'tokenization completed, json file successfully generated')
print( 'total documents processed: %d' % ( documents_to_process )  )
print( 'unique tokens found: %d' % ( len( tokens ) ) )


