from news_scrapping_code import build
from flask import Flask, request

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
    return '<html><body><h3>Enter URL in the following format:</h3><p><b>http://127.0.0.1:5000</b><i>/input/?url=</i><u>https://www.your_news_link.com</u></p></body></html>'


if __name__ == '__main__':
    app.debug = True
    app.run()
