from tweepy import OAuthHandler
#import time
import tweepy
import json
import pymongo
from pymongo import MongoClient
import re
import csv


class SearchAPI:
    def __init__(self):
        # Twitter API authentication
        self.auth = OAuthHandler("QKDSF7QvUt8qRBEnDQJsPtcUi",
                                 "oHN4HtMQMzDLmJmIU1YfIfUv2Mxyt9EbpkpokoPMEtcsPbvbBJ")
        self.auth.set_access_token("830842352897912832-kmj4Uv5tc59IQUJEoEzpLkUZEOVbvQ0",
                                   "GnMjF4Ii0L562NEhUd3ZtJfjfsRi6e1M5TOhbShCQejxx")

    # method to get and store data from Search API
    def call_Search_API(self, path):

        filepath = path

        print("Twitter Search API called")
        print("500 posts fetched")
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
        counter = 1

        print(
            "positive-words.txt and negative-words.txt should be there in the same folder")
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

        # Iterating through data
        for i in range(0, 1):
            # wait time after every 100 frames added
            # time.sleep(1)
            print("Wait")
            for status in tweepy.Cursor(api.search, q=search_words, lang="en", tweet_mode="extended").items(510):

                if(counter+1 == 501):
                    break
                tweets.append(status.full_text)
                text_check = status.full_text
                text_check = text_check.replace(" ", "")
                text_check = text_check.strip()

                if(len(text_check) == 0 or text_check == ""):
                    counter = counter-1
                    continue
                # cleaning readable tweet for print
                modified_text = re.sub(url_pattern, "", status.full_text)
                modified_text = re.sub(r'(#\w+)\S', "", modified_text)
                modified_text = re.sub(r'(@\w+)\S', "", modified_text)
                modified_text = modified_text.replace("&amp;", "")
                modified_text = modified_text.replace("&gt;", "")
                modified_text = modified_text.replace('"', "")
                modified_text = modified_text.replace("-", "")
                modified_text = modified_text.replace("\n", " ")
                modified_text = self.modify(modified_text)
                modified_text = modified_text.replace("   ", " ")
                modified_text = modified_text.strip()

                # get_array.append(modified_text)
                # cleaned_tweets are just for print remove them cleaned tweets are already added to get_array for dictionary
                cleaned_tweets.append(modified_text)

                # to remove any special characters from tweets

                PERMITTED_CHARS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ \n"
                cleaned_text = "".join(
                    c for c in modified_text if c in PERMITTED_CHARS)
                sentiment_tweets.append(cleaned_text)

                # to get polarity of tweet sentiments
                positive_matched = []
                negative_matched = []

                cleaned_text_words = cleaned_text.split(" ")
                #print("\ncleaned_text_words:", cleaned_text_words)
                for word in cleaned_text_words:
                    if word.lower() in positive_words:
                        positive_matched.append(word)

                    # positive_words.append(line.strip('\n'))
                for word in cleaned_text_words:
                    if word.lower() in negative_words:
                        negative_matched.append(word)

                get_array2.append("index")
                get_array2.append(counter)
                get_array2.append("tweet")
                get_array2.append(modified_text)
                #print("Tweet:", cleaned_text)
                #print("positive_matched:", positive_matched)
                #print("Negative_matched:", negative_matched)

                get_array2.append("match")
                matched_words = []
                matched_words.extend(positive_matched)
                matched_words.extend(negative_matched)
                if(len(matched_words) == 0):
                    get_array2.append("")
                else:
                    s1 = ""
                    for word in matched_words:
                        s1 = s1+word+", "
                    s1 = s1.strip(", ")
                    get_array2.append(s1)

                get_array2.append("polarity")
                if(len(positive_matched) > len(negative_matched)):
                    get_array2.append("positive")
                if(len(negative_matched) > len(positive_matched)):
                    get_array2.append("negative")
                if(len(negative_matched) == len(positive_matched)):
                    get_array2.append("neutral")

                counter = counter+1

        data1 = []
        data2 = []

        # dictionary created
        for i in range(0, len(get_array2)-7, 8):
            res_dct_sentiment = {get_array2[i]: get_array2[i+1], get_array2[i+2]: get_array2[i+3], get_array2[i+4]: get_array2[i+5],
                                 get_array2[i+6]: get_array2[i+7]}
            data2.append(res_dct_sentiment)

        csv_columns = ["index", "tweet", "match", "polarity"]
        print("data frames created")

        csv_file = path
        try:
            with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                writer.writeheader()
                for data in data2:
                    writer.writerow(data)
            print("No of records inserted in file:", counter)
        except IOError:
            print("I/O error")

        return

    # method to clean emojis

    def modify(self, text):
        regex_pattern = re.compile(pattern="["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"
                                   u"\U00002702-\U000027B0"
                                   u"\U000024C2-\U0001F251""]+", flags=re.UNICODE)
        return regex_pattern.sub(r'', text)


def main():

    api_s1 = SearchAPI()
    path = input("Enter path for csv file generated (with filename):")

    api_s1.call_Search_API(path)


if __name__ == "__main__":
    main()
