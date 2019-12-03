import pandas
import json



data = pandas.read_csv( 'raw-data/movies_metadata.csv' )

# clean csv
to_drop = ['adult', 'original_title', 'belongs_to_collection', 'production_countries', 'production_companies', 'spoken_languages', 'status','video', 'original_language', 'tagline' ]

# drop unnecessary columns
data.drop( to_drop, inplace=True, axis=1 )

# drop rows with missing data in overview and title
data = data.dropna( subset=[ 'overview', 'title', 'poster_path', 'genres' ] )

# iterate and drop rows with data mismatch for overview data
# rows_to_process = 50000

# print( len( data['overview'] ) )
documents_size = len(data)

# drop tables without genres
rows_to_drop = []
# genres = data.iloc[ i ][ 'genres' ]

# if len( genres ) < 1:
#     print( genres )
for i in range( documents_size ):
    # genres = json.load( str( data.iloc[ i ][ 'genres' ] ) )
    # cast as string even tho its a fucking string
    current_document = str( data.iloc[ i ][ 'genres' ] )

    # replace ' with ", json string encoding
    current_document = current_document.replace('\'', "\"")
    # load json string as python data structures
    genres = json.loads( current_document )
    if i == 32:
        print( type( genres ) )
    if len( genres ) < 1:
        rows_to_drop.append( i )

    # if len( genres ) < 1:
    #     print( genres )
    # try:
    #     if( i%1000 == 0 ):
    #         print( data['genres'][i])
    #     data['genres'][i]['name']
    #     # print( data['genres'] )
    # except:

    #     # print( data['genres'][i] )
    #     # print( data['genres'] )
    #     print( data['title'][i])
    #     print( data['genres'][i])
    #     rows_to_drop.append( i )

# for row in rows_to_drop:
data = data.drop( data.index[ rows_to_drop ] )
print( len( rows_to_drop ))
print( len( data ))
# for i in range( rows_to_process ):
#     if not isinstance ( data.iloc[0][ 'overview' ], str ):
#         print ( data.iloc[0][ 'overview' ] )

# generate cleaned csv
data.to_csv( 'processed-data/movies.csv', index=False )