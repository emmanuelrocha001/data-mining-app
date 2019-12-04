from flask import Flask, render_template, url_for, request
from search_engine  import *
from classifier import *

app = Flask( __name__ )
@app.route('/')
def main():
    # test = query('war machines')
    # print(test)

    return render_template( 'index.html')
    # print( request.form['search-box'] )

@app.route('/search/results/<q>')
def search( q ):

    result = query( q )

    return render_template( 'results.html', result_data = result)


@app.route( '/classifier/' )
def classifier():
    return render_template( 'classifier.html')


@app.route('/classifier/results/<q>')
def classify( q ):

    result = predictGenre( q )

    return render_template( 'classifier-results.html', result_data = result)





# for development
if __name__ == '__main__':
    # app.jinja_env.auto_reload = True
    # app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, use_reloader=True)