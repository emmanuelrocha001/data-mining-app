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


    # if any of the given terms appears in the document add to potential documents
    posting_list_length = len( posting_lists )
    candidate_documents = []
    # print('\nposting lists\n')
    # for item in posting_lists:
    #     print(item)
    # iterate through each posting list
    for l in posting_lists:
        for doc in l.keys():
            # print('item: %s'% ( doc) )
            if doc not in candidate_documents:
                # print( doc )
                candidate_documents.append( doc )
    # print('\ncandidates\n')
    # print( candidate_documents )

    return terms_to_check, candidate_documents
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


def generateRankUtils( query, documents, terms_to_check ):
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
            if term not in terms_to_check:
                term_frequencies[ document ].update({
                    term : 0
                })
            else:
                # when checking see if key exists for that
                # count number in documents
                # tokenize document
                term_appearance_in_document = 0
                for word in filtered_overview:
                    if term == word:
                        term_appearance_in_document = term_appearance_in_document + 1

                # normalize term frequency
                # TF(t) = (Number of times term t appears in a document) / (Total number of terms in the document)

                total_terms_in_document = len( data_tokens )
                # print( 'total terms in document: %d' % ( total_terms_in_document ) )
                current_frequency = ( term_appearance_in_document / total_terms_in_document )

                term_frequencies[ document ].update({
                    term : current_frequency
                })
    # print( term_frequencies )
    ranking_utils.update({'term_frequencies': term_frequencies })


    #calculate document frequency
    inverse_document_frequency = {}
    for term in query:
        # calculate inverse document frequency
        idf = 0
        if term in terms_to_check:
            N = len( movies_csv[ 'overview' ] )
            dft = data_tokens[ term ]['frequency']
            idf = numpy.log10( N / dft )

        inverse_document_frequency.update( {
            term: idf
        })

    # print( inverse_document_frequency )
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

    # print( term_frequency_inverse_document_frequency )
    ranking_utils.update({'tf_idf': term_frequency_inverse_document_frequency })
    # print( ranking_utils )
    return ranking_utils


    # calculate



def calculateScore( tf_idf ):
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
    # print( listofTuples )
    return listofTuples
    # print( tf_idf )
def query( q ):
    # return 'hi from test'
    raw_query = q
    # raw_query = input ( "search: " )

    # start timer of query result
    start = timeit.default_timer()

    query = generateQuery( raw_query )
    # print( query )
    words_to_check, candidate_documents = processQuery( query )
    print( words_to_check )
    if( len( candidate_documents) < 1):
        return ( "0 results found for \"" + str( q )  + "\"" )
    rank_utils = generateRankUtils( query, candidate_documents, words_to_check )
    ranking = calculateScore( rank_utils[ 'tf_idf'] )

    # end timer
    stop = timeit.default_timer()
    print('query time: ', end='')
    print( stop - start )
    time_result = str( stop - start )
    print('\n\nTOP RESULTS\n\n', end='')


    list_length = len( ranking )
    if ( len( ranking ) > 10 ):
        list_length = 10

    for i in range( list_length ):
        # print(rank[0])
        print( movies_csv.iloc[ int( ranking[i][0] ) ][ 'title' ] )
        print('score: %f \n' % ( ranking[i][1] ) )
        # print( rank_utils['inverse_document_frequency'][ ranking[i][0]] )
        print('\n')
        # print( movies_csv.iloc[ int(candidate_key) ][ 'overview' ] )
    # generatePositionalIndexMatrix ( 'andy' )

    return_data = {}
    # append query time
    return_data.update({'time': time_result})
    # number of results
    return_data.update({'results': len( candidate_documents) })
    # number of documents
    return_data.update({'documents': len( movies_csv['title']) })

    # append idf
    return_data.update({'idf': rank_utils['inverse_document_frequency']})
    top_ten = []
    for i in range( list_length ):
        top_ten.append({
            'title': movies_csv.iloc[ int( ranking[i][0] ) ][ 'title' ],
            'overview': movies_csv.iloc[ int( ranking[i][0] ) ][ 'overview' ],
            'tf': rank_utils['term_frequencies'][ ranking[i][0]],
            'tf_idf': rank_utils['tf_idf'][ ranking[i][0]],
            'score': ranking[i][1]
        })
        # add each titles calculation data
    return_data.update({
        'top_ten': top_ten
    })
    print( return_data )
    if len( ranking ) > 0:
        return return_data
    else:
        return ( "0 results found for \"" + str( q )  + "\"" )
    # return 'hi'

# if __name__  == '__main__':
#     main()
#         # print( movies_csv[ 'overview' ] )
