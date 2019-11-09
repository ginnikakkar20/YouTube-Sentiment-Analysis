__author__ = 'user'

#from src 
import sentiment
import re

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
    with open(filepath,'r') as fp:
        youtube_url = fp.readline()
        cnt = 1
        while youtube_url != '':
            print(cnt,"------url--------", youtube_url,"\n")
            video_id = extract_video_id(youtube_url)
            comments_ratio = 100

            if video_id is None:
                print("Invalid URL")

            else:
                result, dictionary_comments = sentiment.get_sentiment(video_id,comments_ratio)
                #print("comments are------------------------", dictionary_comments)
                with open(output_file, 'a') as f:
                    print(youtube_url,":\n", dictionary_comments,"\n", file=f)
            youtube_url = fp.readline()
            print("next youtube url#########", youtube_url)
            cnt += 1