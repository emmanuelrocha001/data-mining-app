from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import word_tokenize
import pandas
import json


# import pre-processed data
data_tokens = {}
# read csv
print( 'loading dataset...' )
movies_csv = pandas.read_csv( './pre-processing/processed-data/movies.csv' )

print( 'loading parsed tokens...' )
# read json and convert back to dictionary
with open( './pre-processing/processed-data/tokens.json' ) as json_file:
    data = ( json.load( json_file ) )['tokens']

# iterate through tokens
for i in range( len(data) ):
    data_tokens.update( { data[i][ 'term' ]: {
        'frequency': data[i][ 'frequency' ],
        'posting_list': data[i][ 'posting_list' ],
    } } )

print( data_tokens[ 'andy' ]['posting_list']['0'] )


def generateQuery( raw_query ):
    print ( raw_query )

    # to lowercase
    raw_query = raw_query.lower()
    # regex to remove punctuation
    tokenizer =  RegexpTokenizer( r'\w+' )
    # tokenize
    tokens = tokenizer.tokenize( raw_query )
    # stop words to be filtered
    stop_words = set(stopwords.words('english'))

    # processed query
    query = []
    for token in tokens:
        if token not in stop_words:
            if token not in query:
                query.append( token )

    return query

def generatePositionalIndexMatrix( current_term ):
    pos_matrix = {}

    for document_id in data_tokens[ current_term ]['documents']:
        print( movies_csv.iloc[ document_id ][ 'overview' ] )
        # print( type( document ) )
        #  movies_csv.iloc[  ][ 'overview' ]

    # # if 'andy' not in data_tokens.keys():
    # #     print( 'not in keys' )
    # for token in data_tokens.keys():
    #     print( token )

def main():

    # thing = importData()
    # promp user for query
    # print( data_tokens[0] )
    raw_query = input ("search: ")
    query = generateQuery( raw_query ) 
    print( query )
    # for word in query:
    #     generatePositionalIndexMatrix( word )


    # generatePositionalIndexMatrix ( 'andy' )

    # print( movies_csv[ 'overview' ] )

if __name__  == '__main__':
    main()