from pymongo import MongoClient
from bson.objectid import ObjectId
from models import Quote
import connect
import redis
from redis_lru import RedisLRU


class DB_Session():
    client_mongo = MongoClient(connect.connection_string)
    db = client_mongo.AuthorsDB
    client_redis = redis.StrictRedis(
        host="localhost", port=6379, password=None)
    cache = RedisLRU(client_redis)

    def __init__(self) -> None:
        self.last_execution_result = []

    @cache
    def get_quotes_by_name(self, search_key: str) -> list():
        author = self.db.author.find_one({"fullname": search_key})
        author_id = str(author["_id"])
        quotes = self.db.quote.find({"author": ObjectId(author_id)})
        self.last_execution_result.clear()
        for quote in enumerate(quotes, start=1):
            self.last_execution_result.append(
                f'{quote[0]}. {quote[1]["quote"]}')

    @cache
    def get_quotes_by_tag(self, search_key: str) -> list():
        quotes = self.db.quote.find({"tags.name": "success"})
        self.last_execution_result.clear()
        for quote in enumerate(quotes, start=1):
            self.last_execution_result.append(
                f'{quote[0]}. {quote[1]["quote"]}')

    @cache
    def get_quotes_by_tags(self, search_key: str) -> list():
        search_keys_as_list = search_key.split(",")
        quotes = Quote.objects(tags__name__in=search_keys_as_list)
        self.last_execution_result.clear()
        for quote in enumerate(quotes, start=1):
            self.last_execution_result.append(f'{quote[0]}. {quote[1].quote}')

    def get_handler(self, key_word: str):
        handlers = {
            "name": self.get_quotes_by_name,
            "tag": self.get_quotes_by_tag,
            "tags": self.get_quotes_by_tags
        }
        return handlers.get(key_word, None)

    def close(self):
        DB_Session.client_redis.close()
        DB_Session.client_mongo.close()


if __name__ == "__main__":
    session = DB_Session()
    print("Available DB commands: name:<value>, tag:<value>, tags:<value_1, value_n>.\n")
    user_input = ""
    while True:
        user_input = input(
            "Please enter a command as <key word>:<search criteria>:")
        if user_input == "exit":
            break
        if user_input.find(":") == -1:
            print("Missing separator :")
            continue
        try:
            key_word = user_input.split(":")[0]
            search_key = user_input.split(":")[1]
            if not (key_word and search_key):
                raise IndexError()
        except IndexError:
            print("Missing key word or search criteria.")
        else:
            function = session.get_handler(key_word)
            if function:
                function(search_key)
                for row in session.last_execution_result:
                    print(row)
            else:
                print("Unknown key word.")
    session.close()
