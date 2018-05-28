import server.Messenger as Messenger
import server.DataAccessObject as DataAccessObject
import pika
import sys
import datetime
import re
from textblob import TextBlob


class DataAnalysis:

    def clean(self, sentence):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", sentence).split())

    def analyze_sentiment(self, dataframe):
        dataframe["text"] = self.clean(dataframe["text"])
        analysis = TextBlob(dataframe["text"])
        dataframe["sentiment"] = str(analysis.sentiment.polarity)
        dataframe["creation_date"] = datetime.datetime.utcnow()
        return dataframe


class Server:

    def __init__(self, messenger, data_access_object):
        self._messenger = messenger
        self._dao = data_access_object
        self._data_analyzer = DataAnalysis()

    def callback(self, ch, method, props, body):
        body = eval(body.decode("utf-8"))
        if "save" in body[0]:
            body[1] = self._data_analyzer.analyze_sentiment(body[1])
            self._dao.save(body[1])
            print("Saved to mongo -> {}".format(body[1]))
        else:
            return_data = self._dao.get_by_time(int(body[1]))
            for x in return_data:
                del x['_id']
            print("Replying to client -> {}".format(return_data))
            ch.basic_publish(exchange='',
                             routing_key=props.reply_to,
                             properties=pika.BasicProperties(correlation_id=props.correlation_id),
                             body=str(return_data))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def listen(self):
        self._messenger.listen(callback=self.callback)


if __name__ == '__main__':
    host = "localhost"
    mongo_host = "localhost"
    if len(sys.argv) > 1:
        host = sys.argv[1]
        print("using host -> {}".format(host))
    if len(sys.argv) > 2:
        mongo_host = sys.argv[2]
        print("using mongo host -> {}".format(mongo_host))
    server = Server(Messenger.Messenger("Server", host=host), DataAccessObject.DAO(host=mongo_host))
    server.listen()



