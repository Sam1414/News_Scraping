from news_scrapping_code import build
from flask import Flask, request, render_template
from waitress import serve
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/input/')
def get_res():
    # Getting Input
    url = request.args.get('url')
    # Getting Result
    data = build(url)
    # Returning Result
    return data


@app.route('/')
def default_page():
    return render_template('home.html')


if __name__ == '__main__':
    app.debug = True
    # app.run()
    serve(app, host='0.0.0.0', port=1500)