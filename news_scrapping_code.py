import re
from GoogleNews import GoogleNews
from newspaper import Article
from nltk.stem import PorterStemmer


def pre_process(text):
    lst_stop_words = ["a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "as",
                      "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by",
                      "could", "did", "do", "does", "doing", "down", "during", "each", "few", "for", "from", "further",
                      "had", "has", "have", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers",
                      "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in",
                      "into", "is", "it", "it's", "its", "itself", "let's", "me", "more", "most", "my", "myself", "nor",
                      "of", "on", "once", "only", "or", "other",
                      "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "she", "she'd", "she'll",
                      "she's", "should", "so", "some", "such", "than", "that", "that's", "the", "their", "theirs",
                      "them", "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll", "they're",
                      "they've", "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "we",
                      "we'd", "we'll", "we're", "we've", "were", "what", "what's", "when", "when's", "where", "where's",
                      "which", "while", "who", "who's", "whom", "why", "why's", "with", "would", "you", "you'd",
                      "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves"]
    punctuations = '''!()-[\’\“\”]{—};:'"\,<>./?@#$%^&*_~'''
    ps = PorterStemmer()
    re.sub(r'http\S+', '', text)
    word_lst = text.lower().split()
    new_word_lst = []
    for word in word_lst:
        mod_word = ''.join([char for char in word if char not in punctuations])
        mod_word = ps.stem(mod_word)
        new_word_lst.append(mod_word)
        if mod_word in lst_stop_words:
            new_word_lst.remove(mod_word)
    mod_text = ' '.join(new_word_lst)

    return mod_text


def get_user_data(user_link):
    article = Article(user_link, language='en')
    article.download()
    article.parse()
    article.nlp()
    headline = article.title
    content = article.summary
    image = article.top_image
    keywords = article.keywords
    # print('keywords:', keywords)
    user_d = {'link': user_link, 'keywords': keywords, 'headline': headline,
              'content': content, 'image': image}
    print('user link: ', user_d['link'])
    print('user headline: ', user_d['headline'])
    return user_d


def get_admin_data(user_headline, user_img, user_keywords):
    admin_data = {'link': None, 'headline': None,
                  'content': None, 'image': None}
    google_news = GoogleNews(lang='en')
    google_news.search(user_headline)
    links = google_news.get__links()
    print('No. of links found: ', len(links))
    if len(links) == 0:
        google_news = GoogleNews(lang='en')
        google_news.search(' '.join(user_keywords))
        links2 = google_news.get__links()
        if len(links2) == 0:
            return admin_data
        else:
            links = links2
    if len(links) == 1:
        link_used = links[0]
    else:
        link_used = links[1]

    admin_data['link'] = link_used
    # print(link_used)
    article = Article(link_used)
    article.download()
    article.parse()
    article.nlp()
    admin_data['headline'] = article.title
    admin_data['content'] = article.summary
    if article.top_image is not None:
        admin_data['image'] = article.top_image
    print('admin link: ', admin_data['link'])
    print('admin headline: ', admin_data['headline'])
    return admin_data


def build(user_link):
    # Getting Headline and article from User's Link
    user_data = get_user_data(user_link)

    # Pre-Processing user data
    user_data['content'] = pre_process(user_data['content'])

    # Getting our own data
    admin_data = get_admin_data(
        user_data['headline'], user_data['image'], user_data['keywords'])

    # If no related data is found
    # if admin_data['link'] is None:
    # r = {'stance': 'NONE', 'result': 'Possibly Fake', 'similarity': 0,
    #      'user_data': user_data, 'admin_data': admin_data}
    # return r

    # If data available
    # Pre-Processing our data
    if admin_data['link'] is not None:
        admin_data['content'] = pre_process(admin_data['content'])

    data = {'user_data': user_data, 'admin_data': admin_data}

    print(data)

    return data


# build('https://zeenews.india.com/personal-finance/faceless-assessment-taxpayers-charter-implemented-from-today-faceless-appeal-service-will-be-available-from-september-25-pm-modi-2302453.html')

# Getting Feature Vector
# features, sim = get_feature_vector(
#     user_data['content'], admin_data['content'])

# Prediction on Feature Vector
# stance, result = predict(features)
# r = {'stance': stance, 'result': result, 'similarity': sim * 100,
#      'user_data': user_data, 'admin_data': admin_data}
# return r
