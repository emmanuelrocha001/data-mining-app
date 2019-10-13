from flask import Flask, render_template, url_for
from search-engine import tokenize

app = Flask( __name__ )

@app.route('/')
@app.route('/search')
def search_engine():
    return render_template( 'index.html' )


# for development
# if __name__ == '__main__':
#     app.run( debug=True )