import re
import pymongo
from pymongo import MongoClient

# function to exttract data with regex from file


def extract_data(path):
    title_pattern = ('<TITLE>(.)*</TITLE>')
    body_start_pattern = ('<BODY>(.)*')
    body_end_pattern = (r'(.)*</BODY>')

    # opening file
    f = open(path, 'r')
    # reading lines of file
    lines = f.readlines()

    count = 0
    route_count = 0

    body_matched = False

    body_text = ""
    text_array = []
    for line in lines:

        match_title = re.search(title_pattern, line)
        # matching <TITLE> tag---------------------------------------------------------------------------
        if(match_title):
            text_array.append("title")
            stripped_title = match_title.group().replace("<TITLE>", "")
            stripped_title = stripped_title.replace("</TITLE>", "")
            stripped_title = stripped_title.replace("&lt;", "")
            stripped_title = stripped_title.replace(">", "")
            stripped_title = stripped_title.replace("<", "")
            text_array.append(stripped_title)

        # matching start of <BODY> tag--------------------------------------------------------------
        match_body_start = re.search(body_start_pattern, line)
        match_body_end = re.search(body_end_pattern, line)
        if(match_body_start):
            text_array.append("text")

            body_matched = True

            # remove <BODY> tag from matched string
            stripped_string = match_body_start.group().replace("<BODY>", "")
            stripped_string = stripped_string+"\n"

            stripped_string = stripped_string.replace("&lt;", "")
            stripped_string = stripped_string.replace(">", "")

            body_text = body_text+stripped_string
            # text_array.append(stripped_string)

            # -------------------------------------------------count comment
            count = count+1
            continue

        # matching end of <BODY> tag-----------------------------------------------
        if(match_body_end):

            if(match_body_end.group() == "&#3;</BODY>"):
                pass

            body_text = body_text.rstrip("\n")
            text_array.append(body_text)
            body_text = ""
            body_matched = False

        # matching text in <BODY> tag--------------------------------------------------------------
        if(body_matched == True):
            if(" Reuter\n" == line or " REUTER\n" == line):
                route_count = route_count+1

            # any other text content
            else:
                line = line.replace("&lt;", "")
                line = line.replace(">", "")
                body_text = body_text+line
                # text_array.append(line)

        # -------------------------------------------count
        count = count+1

    f.close()

    data = []
    data = Convert(text_array)
    # print(data)
    return data

# function to create data dictionary


def Convert(lst):
    data = []
    for i in range(0, len(lst)-3, 4):
        res_dct = {lst[0]: lst[i+1], lst[i+2]: lst[i+3]}
        data.append(res_dct)
    return data


def store_to_db(data, table_name):
    # connection string
    # mongodb+srv://mihirpatel:<password>@cluster0.d4fsh.mongodb.net/<dbname>?retryWrites=true&w=majority
    cluster = pymongo.MongoClient(
        "mongodb+srv://mihirpatel:mihir@cluster0.d4fsh.mongodb.net/")
    mydb = cluster["ReuterDb"]
    mycol = mydb[table_name]

    mycol.insert_many(data)
    print("No of records inserted: ", len(data))


def document_frequecy_count():
    cluster = pymongo.MongoClient(
        "mongodb+srv://mihirpatel:mihir@cluster0.d4fsh.mongodb.net/")
    mydb = cluster["ReuterDb"]
    mycol = mydb["articles"]

    list = []
    # list for canada frequency per article
    total_words_list = []
    canada_freq_list = []

    x = mycol.find({}, {"_id": 0, "text": 1})
    canada_doc_cont = 0
    rain_doc_cont = 0
    cold_doc_cont = 0
    hot_doc_cont = 0

    doc_count = 0
    '''for data in x:
        text = data['text']
        doc_count = doc_count+1

    print("doc_count:", doc_count)'''

    for data in x:
        text = data['text']
        #print("index: ", count)

        # matching keywords in articles
        modified_text = text.replace('\n', " ")
        modified_text = modified_text.replace('  ', "")
        PERMITTED_CHARS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ \n"
        modified_text = "".join(
            c for c in modified_text if c in PERMITTED_CHARS)
        text_words = modified_text.split(" ")

        total_words_list.append(len(text_words))

        #print("text array: ", text_words)

        # searching for given words in text

        if 'Canada' in text_words:
            canada_doc_cont = canada_doc_cont+1
            canada_freq = 0
            for i in range(0, len(text_words)):
                if(text_words[i] == "Canada"):
                    canada_freq = canada_freq+1
            canada_freq_list.append(canada_freq)
        if 'Canada' not in text_words:
            canada_freq_list.append(0)
        if 'rain' in text_words:
            rain_doc_cont = rain_doc_cont+1

        if 'cold' in text_words:
            cold_doc_cont = cold_doc_cont+1

        if 'hot' in text_words:
            hot_doc_cont = hot_doc_cont+1

        doc_count = doc_count+1

    if(canada_doc_cont == 0):
        canada_div = 0

    else:
        canada_div = doc_count/canada_doc_cont
    if(rain_doc_cont == 0):
        rain_div = 0
    else:
        rain_div = doc_count/rain_doc_cont
    if(cold_doc_cont == 0):
        cold_div = 0
    else:
        cold_div = doc_count/cold_doc_cont
    if(hot_doc_cont == 0):
        hot_div = 0
    else:
        hot_div = doc_count/hot_doc_cont

    # array for documents dict list
    freq_array = [{"search": "Canada", "df": canada_doc_cont, "Total documents(N)/df": str(doc_count)+'/'+str(canada_doc_cont),
                   "Log(N/df)": canada_div},
                  {"search": "rain", "df": rain_doc_cont,
                   "Total documents(N)/df": str(doc_count)+'/'+str(rain_doc_cont), "Log(N/df)": rain_div},
                  {"search": "cold", "df": cold_doc_cont,
                   "Total documents(N)/df": str(doc_count)+'/'+str(cold_doc_cont), "Log(N/df)": cold_div},
                  {"search": "hot", "df": hot_doc_cont,
                   "Total documents(N)/df": str(doc_count)+'/'+str(hot_doc_cont), "Log(N/df)": hot_div}]
    # print(freq_array)
    print("frequency table created")
    store_to_db(freq_array, "frequency table")
    # array for canada dict list
    # print(len(canada_freq_list))
    #print("freq_list:", canada_freq_list)
    # print(len(total_words_list))
    #print("total_words_list:", total_words_list)
    #print("doc count:", doc_count)
    canada_freq_array = []

    # dictionary list made
    for i in range(0, len(total_words_list)):
        res_dct = {"article": i+1,
                   "total_words": total_words_list[i], "frequency": canada_freq_list[i]}

        canada_freq_array.append(res_dct)

    print("Canada frequency table created")
    store_to_db(canada_freq_array, "canada frequency")

    find_highest_freq_article(total_words_list, canada_freq_list)
    return


def find_highest_freq_article(total_words_list, canada_freq_list):
    max_frqency_list = []

    for i in range(0, len(total_words_list)):
        max_frqency_list.append(canada_freq_list[i]/total_words_list[i])

    max_value = max(max_frqency_list)
    max_index = max_frqency_list.index(max_value)
    print("max value:", max_value)
    print("max index:", max_index)

    # Getting article from database
    cluster = pymongo.MongoClient(
        "mongodb+srv://mihirpatel:mihir@cluster0.d4fsh.mongodb.net/")
    mydb = cluster["ReuterDb"]
    mycol = mydb["articles"]

    counter = 0
    list = []

    x = mycol.find({}, {"_id": 0, "text": 1, "title": 1})
    print("Article with the highest frequency of 'Canada':")
    for data in x:

        text = data['text']
        title = data['title']
        if(counter == max_index):

            print("title:", title)
            print("text:", text)

        counter = counter+1
    return


def main():
    #f = open('demoReute.sgm', 'r')
    #f = open('reut2-009.sgm', 'r')
    #f = open('reut2-014.sgm', 'r')

    data = []
    data2 = []
    path1 = input("Enter path for file 1 to extract data from:")

    path2 = input("Enter path for file 2 to extract data from:")

    # Driver code
    data = extract_data(path1)

    data2 = extract_data(path2)

    data.extend(data2)

    #print("data dictionary:", data)
    store_to_db(data, "articles")

    document_frequecy_count()


if __name__ == "__main__":
    main()
