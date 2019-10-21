import pandas

data = pandas.read_csv( 'raw-data/movies_metadata.csv' )

# clean csv
to_drop = ['adult', 'original_title', 'belongs_to_collection', 'production_countries', 'production_companies', 'spoken_languages', 'status','video', 'original_language', 'tagline' ]

# drop unnecessary columns
data.drop( to_drop, inplace=True, axis=1 )

# drop rows with missing data in overview and title
data = data.dropna( subset=[ 'overview', 'title', 'poster_path' ] )

# iterate and drop rows with data mismatch for overview data
# rows_to_process = 50000

print( len( data['overview'] ) )

# for i in range( rows_to_process ):
#     if not isinstance ( data.iloc[0][ 'overview' ], str ):
#         print ( data.iloc[0][ 'overview' ] )

# generate cleaned csv
data.to_csv( 'processed-data/movies.csv', index=False )