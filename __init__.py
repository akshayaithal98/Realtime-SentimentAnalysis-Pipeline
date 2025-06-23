from flask import Flask

from .reviews_api import post_reviews_file
from .review_sentiment import sentiment_analysis_file

app=Flask(__name__)

app.register_blueprint(post_reviews_file)
app.register_blueprint(sentiment_analysis_file)
