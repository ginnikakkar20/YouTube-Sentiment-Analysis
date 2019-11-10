__author__ = 'user'

#from src 
import sentiment
import re
import json
from os import listdir
from os.path import isfile, join
import pandas as pd
import numpy

def extract_video_id(url):
    pattern1  = "^https://www\.youtube\.com/watch\?v=.*$"
    pattern2  = "www\.youtube\.com/watch\?v=.*$"
    if re.match(pattern1,url) or re.match(pattern2,url):
        index = url.find('=')
        video_id = url[index+1:]
        return video_id
    else:
        return None


if __name__ == "__main__":

    filepath = 'video_ids.txt'
    output_file = 'output_analysis.txt'
    DATA_PATH = 'Comments_Youtube'
    FILE = "Output/Output.%s.json"

    comment_files = [join(DATA_PATH, f) for f in listdir(DATA_PATH) if (isfile(join(DATA_PATH, f)) and "json" in f)]
    #print(comment_files)

    for f in comment_files:
        #print(f)
        with open(f, 'r') as outfile:
            data = json.load(outfile)
            data = pd.DataFrame(data)
            #print("----data-----",data)
            #print("-------2==-------", data['text'])
            dictionary_comments = sentiment.get_sentiment(data['text'],100)
            print("-----dictionary----", dictionary_comments)

            video_id = f[26:37]
            #print("-----vid is----", video_ids)
            with open(FILE % video_id, "w") as f:
                print("------output file now--------------")
                f.write(json.dumps(dictionary_comments))

    #data['author_replied'] = data['author_replied'].astype(int)


    # with open(filepath,'r') as fp:
    #     youtube_url = fp.readline()
    #     cnt = 1
    #     while youtube_url != '':
    #         print(cnt,"------url--------", youtube_url,"\n")
    #         video_id = extract_video_id(youtube_url)
    #         comments_ratio = 100

    #         if video_id is None:
    #             print("Invalid URL")

    #         else:
    #             dictionary_comments = sentiment.get_sentiment(video_id,comments_ratio)
    #             #print("comments are------------------------", dictionary_comments)
    #             with open(output_file, 'a') as f:
    #                 print(youtube_url,":\n", dictionary_comments,"\n", file=f)
    #         youtube_url = fp.readline()
    #         print("next youtube url#########", youtube_url)
    #         cnt += 1