import xml.etree.ElementTree as ET
import random
import shutil
import os
import ast
import re
import unidecode
import pickle

from django.core.management.base import BaseCommand, CommandError
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import classify, NaiveBayesClassifier
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB,BernoulliNB
from sklearn.linear_model import LogisticRegression,SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from nltk.classify import ClassifierI
from statistics import mode

from core.settings import (TASS_FILES_LIST)

class bcolors:
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    ENDC = '\033[0m'

class VoteClassifier(ClassifierI):
    def __init__(self, *classifiers):
        self._classifiers = classifiers

    def classify(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        return mode(votes)

    def confidence(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        choice_votes = votes.count(mode(votes))
        conf = choice_votes / len(votes)
        return conf

class Command(BaseCommand):
    help = 'To train Classifiers and Vote Classifier for Sentiment Analysis in twitter_search endpoint'

    def clean_tweet(self,tweet):
        '''
        Method to clean tweets (with regex, translate, unidecode) 
        and remove stop words (with nltk)
        '''
        # Define some regex rules
        url_regex = re.compile(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''')
        numeric_regex = re.compile('(\\d+)')
        mentions_regex = re.compile("@[A-Za-z0-9]+")
        brackets_regex = re.compile("\[[^)]*\]")
        parenthesis_regex = re.compile   ("\([^)]*\)")
        punctuation_signs = re.compile(r'[^\w\s]')
        # Remove Hiperlinks
        tweet = url_regex.sub('', tweet)
        # Remove @mentions
        tweet = mentions_regex.sub('', tweet)
        # Remove text between brackets and parenthesis, like [Video] or [Photos]
        tweet = brackets_regex.sub('', tweet)
        tweet = parenthesis_regex.sub('', tweet)
        # Remove punctuations
        tweet = punctuation_signs.sub('', tweet)
        # Remove punctuations
        tweet = numeric_regex.sub('', tweet)
        # Remove white spaces
        tweet = " ".join(tweet.split())
        # Remove accents
        tweet = unidecode.unidecode(tweet)
        # Convert to lowercase
        tweet = tweet.lower()
        # Remove stop words
        list_position = 0
        tweet_cleaned = ''
        for word in tweet.split():
            if word not in set(stopwords.words("spanish")):
                if list_position == 0:
                    tweet_cleaned = word
                else:
                    tweet_cleaned = tweet_cleaned + ' ' + word
                list_position += 1
        return tweet_cleaned

    def get_tweets_for_model(self,cleaned_tokens_list):
        yield dict([token, True] for token in cleaned_tokens_list)

    def handle(self, *args, **options):
        print (bcolors.OKBLUE + "Training Classifier Models" + bcolors.ENDC)
        files = ast.literal_eval(TASS_FILES_LIST)

        lines=[]

        # Concatenating all the TASS XML files
        for i,filename in enumerate(files):
           readFile = open(os.getcwd()+'/tass/'+filename)
           if(i==0):
              lines = readFile.readlines()[:-1]
           elif(i==len(files)-1):
              lines = lines + readFile.readlines()[1:]
           else:
              lines = lines + readFile.readlines()[1:-1]
           readFile.close()

        file = open(os.getcwd()+'/tass/unified_tass_dataset.xml','w')
        file.writelines([item for item in lines])
        file.close()

        tree = ET.parse(os.getcwd()+'/tass/unified_tass_dataset.xml')
        root = tree.getroot()

        positive_tweet_list = []
        negative_tweet_list = []
        neutral_tweet_list = []
        none_tweet_list = []
        count_tweets=0
        print (bcolors.OKBLUE + "Processing Tweets, this step will take a few minutes..." + bcolors.ENDC)

        # Getting tweets data of the unified XML file dataset
        for tweet_index,tweets in enumerate(root):
            count_tweets+=1
            properties_tweet = {}
            properties_tweet['tweetid'] = tweets[0].text
            properties_tweet['user'] = tweets[1].text
            properties_tweet['tweet'] = tweets[2].text
            properties_tweet['tweet_cleaned'] = word_tokenize(Command().clean_tweet(tweets[2].text))
            properties_tweet['date'] = tweets[3].text
            properties_tweet['language'] = tweets[4].text
            properties_tweet['sentiment'] = tweets[5][0][0].text

            if tweets[5][0][0].text == 'P':
                positive_tweet_list.append(properties_tweet)
            elif tweets[5][0][0].text == 'N':
                negative_tweet_list.append(properties_tweet)
            # elif tweets[5][0][0].text == 'NEU':
            #     neutral_tweet_list.append(properties_tweet)
            # elif tweets[5][0][0].text == 'NONE':
            #     none_tweet_list.append(properties_tweet)

        print (bcolors.OKBLUE + "Total of tweets processed: " + str(count_tweets) + bcolors.ENDC)
        print (bcolors.OKBLUE + "Total of tweets processed for training data: " + str(len(positive_tweet_list)+len(negative_tweet_list)) + bcolors.ENDC)

        positive_tokens_for_model_aux = []
        negative_tokens_for_model_aux = []
        #neutral_tokens_for_model_aux = []
        #none_tokens_for_model_aux = []

        # Generating lists of positive and negative tweets
        for properties_tweet in positive_tweet_list:
            positive_tokens_for_model_aux.append(list(Command().get_tweets_for_model(properties_tweet['tweet_cleaned'])))
        '''
        positive_tokens_for_model_aux[0]
		[{'word1': True, 'word2': True...}]
        '''
        for properties_tweet in negative_tweet_list:
            negative_tokens_for_model_aux.append(list(Command().get_tweets_for_model(properties_tweet['tweet_cleaned'])))

        # for properties_tweet in neutral_tweet_list:
        #     neutral_tokens_for_model_aux.append(list(Command().get_tweets_for_model(properties_tweet['tweet_cleaned'])))

        # for properties_tweet in none_tweet_list:
        #     none_tokens_for_model_aux.append(list(Command().get_tweets_for_model(properties_tweet['tweet_cleaned'])))

        # Setting structure needed for Bayesian Classifier
        positive_dataset = [(tweet_dict[0], "Positive") for tweet_dict in positive_tokens_for_model_aux]
        '''
        positive_dataset[0]
        ({'word1': True, 'word2': True...}, 'Positive')
        '''

        negative_dataset = [(tweet_dict[0], "Negative") for tweet_dict in negative_tokens_for_model_aux]

        # neutral_dataset = [(tweet_dict[0], "Neutral") for tweet_dict in neutral_tokens_for_model_aux]
        # none_dataset = [(tweet_dict[0], "None") for tweet_dict in none_tokens_for_model_aux]

        dataset = positive_dataset + negative_dataset    # + neutral_dataset + none_dataset

        random.shuffle(dataset)

        slice_size = round(len(dataset)*70/100)

        train_data, test_data = dataset[:slice_size], dataset[slice_size:]

        original_bayesian_classifier = NaiveBayesClassifier.train(train_data)

        print (bcolors.OKGREEN + "Accuracy of Naives Bayes Classifier:", str(classify.accuracy(original_bayesian_classifier, test_data)*100) + bcolors.ENDC)
        # print(original_bayesian_classifier.show_most_informative_features(10))
        # Saving Naives Bayes trained
        f = open('sentiment_classifiers/original_naives_bayes_classifier.pickle', 'wb')
        pickle.dump(original_bayesian_classifier, f)
        f.close()

        MNB_classifier = SklearnClassifier(MultinomialNB())
        MNB_classifier.train(train_data)
        print (bcolors.OKGREEN + "MNB_classifier accuracy percent:", str(classify.accuracy(MNB_classifier, test_data)*100) + bcolors.ENDC)
        # Saving MNB classifier trained
        f = open('sentiment_classifiers/MNB_sentiment_classifier.pickle', 'wb')
        pickle.dump(MNB_classifier, f)
        f.close()

        BernoulliNB_classifier = SklearnClassifier(BernoulliNB())
        BernoulliNB_classifier.train(train_data)
        print (bcolors.OKGREEN + "BernoulliNB_classifier accuracy percent:", str(classify.accuracy(BernoulliNB_classifier, test_data)*100) + bcolors.ENDC)
        # Saving BernoulliNB classifier trained
        f = open('sentiment_classifiers/BernoulliNB_sentiment_classifier.pickle', 'wb')
        pickle.dump(BernoulliNB_classifier, f)
        f.close()

        LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
        LogisticRegression_classifier.train(train_data)
        print (bcolors.OKGREEN + "LogisticRegression_classifier accuracy percent:", str(classify.accuracy(LogisticRegression_classifier, test_data)*100) + bcolors.ENDC)
        # Saving LogisticRegression classifier trained
        f = open('sentiment_classifiers/LogisticRegression_sentiment_classifier.pickle', 'wb')
        pickle.dump(LogisticRegression_classifier, f)
        f.close()

        # SGDClassifier_classifier = SklearnClassifier(SGDClassifier())
        # SGDClassifier_classifier.train(train_data)
        # print (bcolors.OKGREEN + "SGDClassifier_classifier accuracy percent:", str(classify.accuracy(SGDClassifier_classifier, test_data)*100) + bcolors.ENDC)
        # # Saving SGDClassifier classifier trained
        # f = open('sentiment_classifiers/SGDClassifier_sentiment_classifier.pickle', 'wb')
        # pickle.dump(SGDClassifier_classifier, f)
        # f.close()

        # SVC_classifier = SklearnClassifier(SVC(probability=True))
        # SVC_classifier.train(train_data)
        # print (bcolors.OKGREEN + "SVC_classifier accuracy percent:", str(classify.accuracy(SVC_classifier, test_data)*100) + bcolors.ENDC)
        # # Saving SVC classifier trained
        # f = open('sentiment_classifiers/SVC_sentiment_classifier.pickle', 'wb')
        # pickle.dump(SVC_classifier, f)
        # f.close()

        # LinearSVC_classifier = SklearnClassifier(LinearSVC())
        # LinearSVC_classifier.train(train_data)
        # print (bcolors.OKGREEN + "LinearSVC_classifier accuracy percent:", str(classify.accuracy(LinearSVC_classifier, test_data)*100) + bcolors.ENDC)
        # Saving LinearSVC classifier trained
        # f = open('sentiment_classifiers/LinearSVC_sentiment_classifier.pickle', 'wb')
        # pickle.dump(LinearSVC_classifier, f)
        # f.close()

        NuSVC_classifier = SklearnClassifier(NuSVC(probability=True))
        NuSVC_classifier.train(train_data)
        print (bcolors.OKGREEN + "NuSVC_classifier accuracy percent:", str(classify.accuracy(NuSVC_classifier, test_data)*100) + bcolors.ENDC)
        # Saving NuSVC classifier trained
        f = open('sentiment_classifiers/NuSVC_sentiment_classifier.pickle', 'wb')
        pickle.dump(NuSVC_classifier, f)
        f.close()

        voted_classifier = VoteClassifier(original_bayesian_classifier,
                                          #SVC_classifier,
                                          #LinearSVC_classifier,
                                          NuSVC_classifier,
                                          #SGDClassifier_classifier,
                                          MNB_classifier,
                                          BernoulliNB_classifier,
                                          LogisticRegression_classifier)
        print (bcolors.OKGREEN + "Voted_classifier accuracy percent:", str(classify.accuracy(voted_classifier, test_data)*100) + bcolors.ENDC)
        #print (bcolors.OKGREEN + "Classification:", str(voted_classifier.classify(test_data[0][0])), "Confidence %:", str(voted_classifier.confidence(test_data[0][0])*100) + bcolors.ENDC)
