from news_scrapping_code import build
from flask import Flask, request, render_template

app = Flask(__name__)


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
    app.run()
