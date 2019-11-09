__author__ = 'user'

#import youtube_comments
import download_comment
import filter
import training
import youtube_stats

import pickle


def calculate_score(pos,neg,likes,dislikes,comments_ratio):
    pos_percent = None
    neg_percent = None

    if pos == 0 and neg == 0:
        pos_percent = 0
        neg_percent = 0
    elif pos == 0:
        pos_percent = 0
        neg_percent = 100
    elif neg == 0:
        pos_percent = 100
        neg_percent = 0
    else:
        pos_percent = (pos/(pos+neg))*100
        neg_percent = 100-pos_percent

    likes_percent = (likes/(likes+dislikes))*100
    dislikes_percent = 100 - likes_percent

    pos_percent = pos_percent * (comments_ratio/100)
    neg_percent = neg_percent * (comments_ratio/100)

    likes_dislikes_ratio = 1-(comments_ratio/100)

    likes_percent *= likes_dislikes_ratio
    dislikes_percent *= likes_dislikes_ratio

    pos_sentiment = pos_percent + likes_percent
    neg_sentiment = neg_percent + dislikes_percent

    #print(pos_sentiment," - ",neg_sentiment)

    if pos_sentiment > 45 and pos_sentiment < 60:
        return "mixed"
    elif pos_sentiment >= 60:
        return "positive"
    else:
        return "negative"


def bag_of_words(words):
    return dict([word, True] for word in words)

def get_sentiment(video_id,comments_ratio):
    #comments = youtube_comments.get_youtube_comments(video_id)
    comments = download_comment.commentExtract(video_id)
    #print("---------comments extracted--------", comments)
    pos = 0
    neg = 0

    positive_comments = []
    negative_comments = []

    for com in comments:
        filtered_comments = filter.filter_comments(com)

        training.train_classifier()
        classifier_f = open("classifier.pickle", "rb")
        classifier = pickle.load(classifier_f)
        classifier_f.close()

        for comment in filtered_comments:
            result = classifier.classify(bag_of_words(comment))
            
            if result == "pos":
                pos += 1
                
            else:
                neg += 1

        if (pos - neg) > 0:
            positive_comments.append(com)
        else:
            negative_comments.append(com)

    no_of_likes , no_of_dislikes = youtube_stats.get_likes_dislikes(video_id)

    #print(no_of_likes," - ",no_of_dislikes)
    dictionary_comments = {'Positive Comments': positive_comments, 'Negative Comments': negative_comments}

    result = calculate_score(pos,neg,no_of_likes,no_of_dislikes,comments_ratio)

    return result,dictionary_comments


