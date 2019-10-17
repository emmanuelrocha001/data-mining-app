from flask import Flask, render_template, url_for, request
from search_engine import *


app = Flask( __name__ )
@app.route('/')
@app.route('/search/')
def main():
    # test = query('war machines')
    # print(test)
    return render_template( 'index.html')
    # print( request.form['search-box'] )

@app.route('/results/<q>')
def search( q ):

    result = query( q )

    return render_template( 'results.html', result_data = result)


# # for development
if __name__ == '__main__':
    # app.jinja_env.auto_reload = True
    # app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, use_reloader=True)