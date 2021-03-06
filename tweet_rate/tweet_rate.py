__author__ = 'admin'

import tornado.httpserver
import tornado.options
import tornado.ioloop
import tornado.web
import tornado.httpclient

import urllib
import json
import datetime
import time

from tornado.options import define,options
define("port",default=8000,help="run on the given port",type=int)

class IndexHandler(tornado.web.RequestHandler):
    #@tornado.httpclient.HTTPClient
    def get(self):
        query = self.get_argument('q')
        client = tornado.httpclient.HTTPClient()
        #from tornado.httpclient import HTTPClient
        #client = HTTPClient()

        response = client.fetch("http://search.twitter.com/search.json?" + \
                                urllib.parse.urlencode({"q":query,"result_type":"recent","rpp":100}))
        body = json.loads(response.body)
        result_count = len(body['results'])
        now = datetime.datetime.utcnow()
        raw_oldest_tweet_at = body['result'][-1]['created_at']
        oldest_tweet_at = datetime.datetime.strptime(raw_oldest_tweet_at,
                                                         "%a, %d %b %Y %H:%M:%S +0000")
        second_diff = time.mktime(now.timetuple()) - \
            time.mktime(oldest_tweet_at.timetuple())
        tweets_per_second = float(result_count)/second_diff
        self.write("""
        <div style="text-align: center">
            <div style="font-size: 72px">%s</div>
            <div style="font-size: 144px">%0.2f</div>
            <div style="font-size: 24px">tweets per second</div>
        </div>""" % (query,tweets_per_second))

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r'/',IndexHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
