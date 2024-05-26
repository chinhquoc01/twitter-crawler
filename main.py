
import twitterbot as tb
import secretss, sys
from flask import Flask, jsonify

app = Flask(__name__)
 
# fetches the credentials dictionary
# using get_credentials function
credentials = secretss.get_credentials()
# initialize the bot with your credentials
bot = tb.Twitterbot(credentials['email'], credentials['password'])
# logging in
bot.login()


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/tweets/<hashtag>")
def tweets(hashtag):
    # calling crawl_data function
    data = bot.crawl_data(hashtag)
    return jsonify(data)