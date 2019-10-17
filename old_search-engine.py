from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import word_tokenize
import pandas
import json
import numpy
import timeit

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

# print( data_tokens[ 'andy' ]['posting_list'][str( 0 )] )


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

def processQuery( query ):
    # for document_id in data_tokens[ current_term ]['documents']:
    # print( movies_csv.iloc[ document_id ][ 'posting_list' ] )
    # print( current_term )
    document_candidates = []
    # generate current postings lists
    terms_to_check = []
    posting_lists = []
    for word in query:
        if word in data_tokens.keys():
            terms_to_check.append( word )
            posting_lists.append( data_tokens[ word ][ 'posting_list' ] )
    # sort list by increasing length
    posting_lists.sort( key=len )
    # print(len(posting_lists ))
    # print( posting_lists )
    # check for dcoument candidates based on document id
    shortest_length = len( posting_lists[0] )
    
    
    posting_list_length = len( posting_lists )
    candidate_documents = []
    for candidate_key in posting_lists[0].keys():
        # check if term is documents
        potential_document = True
        for i in range( 1, posting_list_length ):
            if candidate_key not in posting_lists[i]:
                potential_document = False
            # for item in posting_lists[i]:
            #     print(type(item))
            #     print(item)
            if ( potential_document ):
                candidate_documents.append( candidate_key )
        
    return candidate_documents
    # unranked_documents = []
    # proximity_treshold = 1
    # for document in candidate_documents:
    #     append_to_unrakend_documents = True
    #     print( 'checking document' )
    #     for indece in data_tokens[ terms_to_check[0] ]['posting_list'][str(document)]:
    #         # append to unranked documents
    #         for i in range(1,len( terms_to_check )):
    #             current_indeces = data_tokens[ terms_to_check[i] ]['posting_list'][str(document)]
    #             # calculate indece
    #             expected_indece = indece + (i*1)
    #             print('expected indece ')
    #             print( expected_indece )
    #             # check if expected indece is present 
    #             if expected_indece not in current_indeces:
    #                 append_to_unrakend_documents = False
                
    #     if ( append_to_unrakend_documents ):
    #         unranked_documents.append( document)

    # print('unraked documents')
    # print( unranked_documents )


def generateTermFrequencies( query, documents ):
    #document: term:frequency, term
    ranking_utils = {}

    # calculate term frequencies 
    term_frequencies = {}
    for document in documents:
        term_frequencies.update({
            document: {}
        })

        # tokenize overview for given document
        # to lowercase
        overview = movies_csv.iloc[ int(document) ][ 'overview' ]
        overview = overview.lower()
        # regex to remove punctuation
        tokenizer =  RegexpTokenizer( r'\w+' )
        # tokenize
        unfiltered_overview = tokenizer.tokenize( overview )
        # stop words to be filtered
        stop_words = set(stopwords.words('english'))

        # processed query
        filtered_overview = []
        for token in unfiltered_overview:
            if token not in stop_words:
                    filtered_overview.append( token )
        # print( filtered_overview )

        for term in query:
            if term not in data_tokens.keys():
                term_frequencies[ document ].update({
                    term : 0
                })
            else:
                # when checking see if key exists for that
                # count number in documents
                # tokenize document
                current_frequency = 0
                for word in filtered_overview:
                    if term == word:
                        current_frequency = current_frequency + 1

                # normalize term frequency
                current_frequency = numpy.log10( current_frequency ) + 1

                term_frequencies[ document ].update({
                    term : current_frequency
                })
    ranking_utils.update({'term_frequencies': term_frequencies })


    #calculate document frequency
    inverse_document_frequency = {}
    for term in query: 
        # calculate inverse document frequency
        N = len( movies_csv[ 'overview' ] )
        dft = data_tokens['term']['frequency']
        idf = numpy.log10( N / dft ) 

        inverse_document_frequency.update( {
            term: idf
        })
    
    ranking_utils.update({'inverse_document_frequency': inverse_document_frequency })

    # calculate inverse document term frequency
    term_frequency_inverse_document_frequency = {}

    for document in documents:
        term_frequency_inverse_document_frequency.update({
            document: {}
        })

        for term in term_frequencies[document]:
            # calculate tf-idf
            tf_idf = inverse_document_frequency[ term ] * term_frequencies[document][term]
            term_frequency_inverse_document_frequency[document].update({
                term: tf_idf
            })
    
    ranking_utils.update({'tf_idf': term_frequency_inverse_document_frequency })
    # print( term_frequency_inverse_document_frequency )
    return ranking_utils


    # calculate 

    return ranking_utils


def calculateDotProduct( tf_idf ):
    document_scores = {}
    for document in tf_idf.keys():
        # print( tf_idf[ document ] )
        score = 0
        # print( type( tf_idf[ document ] ) ) 
        for term in tf_idf[ document ].keys():
            # print( term )
            score = score + tf_idf[ document ][term]
        document_scores.update({
            document: score
        })
        # print( 'hello' )
    # print( sorted( ))
    listofTuples = sorted( document_scores.items() , reverse=True, key=lambda x: x[1] )
    return listofTuples
    # print( tf_idf )
def main():

    # thing = importData()
    # promp user for query
    # print( data_tokens[0] )
    while( 1 ):
        raw_query = input ( "search: " )

        # start timer of query result
        start = timeit.default_timer()

        query = generateQuery( raw_query ) 
        # print( query )
        candidate_documents = processQuery( query ) 
        rank_utils = generateTermFrequencies( query, candidate_documents )
        ranking = calculateDotProduct( rank_utils[ 'tf_idf'] )

        # end timer 
        stop = timeit.default_timer()
        print('query time: ', end='')
        print( stop - start )
        print('\n\nTOP RESULTS\n\n', end='')


        list_length = len( ranking )
        if ( len( ranking ) > 10 ):
            list_length = 10
            

        for i in range( list_length ):
            # print(rank[0])
            print( movies_csv.iloc[ int( ranking[i][0] ) ][ 'title' ] )
            print('score: %f \n' % ( ranking[i][1] ) )
            # print( movies_csv.iloc[ int(candidate_key) ][ 'overview' ] )
        # generatePositionalIndexMatrix ( 'andy' )

        # print( movies_csv[ 'overview' ] )

if __name__  == '__main__':
    main()