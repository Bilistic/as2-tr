import praw
import reddit.Messenger as Messenger
import sys


class RedditClient:

    def __init__(self, secret, id, name, messenger_service):
        self.__client_secret = secret
        self.__client_id = id
        self.__agent = name
        self.__redditStream = None
        self._messenger = messenger_service

    def stream(self, query):
        if self.__redditStream is not None:
            return  # create disconnect function
        self.__redditStream = praw.Reddit(client_id=self.__client_id, client_secret=self.__client_secret,
                                          user_agent=self.__agent)
        for submission in self.__redditStream.subreddit(query).new(limit=None):
            data = {"method": "reddit", "search": query, "text": submission.title, "length": len(submission.title),
                    "Likes": submission.ups}
            self._messenger.send("", "data_stream", str(["save", data]))

if __name__ == "__main__":
    host = "localhost"
    if len(sys.argv) > 1:
        host = sys.argv[1]
    print("Starting Reddit Streaming Service")
    msg = Messenger.Messenger("Reddit Client", host=host)
    r = RedditClient('tYoa1r0zcO4F4LjEa9kv91nVDHs', 'IdgQF_qCp58bxw', 'Bilistic_turtle', msg)
    r.stream("politics")
    msg.close()
