from tweepy import OAuthHandler
import tweepy
import csv
from datetime import datetime


class SearchAPI:
    def __init__(self):
        # Twitter API authentication
        self.auth = OAuthHandler("QKDSF7QvUt8qRBEnDQJsPtcUi",
                                 "oHN4HtMQMzDLmJmIU1YfIfUv2Mxyt9EbpkpokoPMEtcsPbvbBJ")
        self.auth.set_access_token("830842352897912832-kmj4Uv5tc59IQUJEoEzpLkUZEOVbvQ0",
                                   "GnMjF4Ii0L562NEhUd3ZtJfjfsRi6e1M5TOhbShCQejxx")

    # method to get and store data from Search API
    def call_Search_API(self, path):

        print("Twitter Search API called")
        api = tweepy.API(self.auth, wait_on_rate_limit=True)
        search_words = (
            "Storm OR Winter OR Canada OR Tempereature OR Flu OR Snow OR Indoor OR Safety -filter:retweets")

        get_array = []
        count = 0
        tweets = []
        cleaned_tweets = []
        url_pattern = r"https(.+)\S+"
        sentiment_tweets = []
        get_array2 = []
        counter = 0

        # Getting list of positive and negative words
        file1 = open("positive-words.txt", "r")
        file2 = open("negative-words.txt", "r")
        # print(file.read())
        positive_words = []
        negative_words = []
        for line in file1:
            positive_words.append(line.strip('\n'))
        for line in file2:
            negative_words.append(line.strip('\n'))
        print("wait")
        # Iterating through data
        for i in range(0, 1):
            for status in tweepy.Cursor(api.search, q=search_words, lang="en", tweet_mode="extended").items(500):
                get_array.append("created_at")
                #print("created_at:", status.created_at)
                timestamp = datetime.timestamp(status.created_at)
                #print("timestamp:", timestamp)
                get_array.append(timestamp)

                counter = counter+1

        data1 = []

        # dictionary created
        for i in range(0, len(get_array)-1, 2):
            res_dct = {get_array[i]: get_array[i+1]}
            data1.append(res_dct)

        #print("Tweets:", data1)

        csv_columns = ["created_at"]
        print("data frames created")

        csv_file = path+"timestamp.csv"
        try:
            with open(csv_file, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                writer.writeheader()
                for data in data1:
                    writer.writerow(data)
            print("No of records added to csv file:", counter)
        except IOError:
            print("I/O error")


def main():

    api_s1 = SearchAPI()
    path = input("Enter file path:")
    api_s1.call_Search_API(path)


if __name__ == "__main__":
    main()
