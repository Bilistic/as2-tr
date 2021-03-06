import os
import sys
import datetime

import web.TimerClient as TimerClient
from flask import Flask, render_template, send_from_directory

app = Flask(__name__)
time = 15
host = "localhost"
#  Change the time value to alter the tweet accounted for min = 1
#  dont forget a running server is required


def get_tweets(time_minutes):
    client = TimerClient.TweetRPCClient("web-client", host=host)
    tweets = eval(client.call(time_minutes).decode("utf-8"))
    client.close()
    return tweets


def get_key(entry):
    return float(entry.get("sentiment"))


def group_by(li):
    di = dict()
    for x in li:
        y = di.get(x.get("method"), list())
        y.append(x)
        di[x.get("method")] = y
    for key, value in di.items():
        di[key] = sorted(value, key=get_key, reverse=True)[:5]
    return di


@app.route('/favicon.ico/')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/')
def message():
    return "append /index/ to your url (I could of just re routed you but...)"


@app.route('/<string:page_name>/')
def render_static(page_name):
    print("{} : connected".format(page_name))
    tweets = get_tweets(time)
    grouped = group_by(tweets)
    tweets = sorted(tweets, key=get_key, reverse=True)
    pos = tweets[:10]
    neg = tweets[-10:]
    if len(tweets) > 0:
        score = sum([float(tweet.get("sentiment")) for tweet in tweets]) / len(tweets)  #
    else:
        score = 0.00
    return render_template('%s.html' % page_name, time=time, entries=pos, neg_entries=neg, score=score, methods=grouped)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        host = sys.argv[1]
    app.run(host='0.0.0.0', debug=True)
    #  app.run()
