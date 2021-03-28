#Library Section
import pandas as pd # Pandas - Data manipulation and analysis library
import re # Regular Expression Python module
from nltk.tokenize import word_tokenize #Natural Processing Toolkit to remove repeated characters
from string import punctuation 
from nltk.corpus import stopwords 
import numpy as np

#Cleansing methods
def remove_content(text):
    text = re.sub(r"http\S+", "", text) #remove urls
    text=re.sub(r'\S+\.com\S+','',text) #remove urls
    text=re.sub(r'\@\w+','',text) #remove mentions
    text =re.sub(r'\#\w+','',text) #remove hashtags
    text =re.sub(r'amp','',text) #remove weird text
    return text
def process_text(text, stem=False): #clean text
    text=remove_content(text)
    text = re.sub('[^A-Za-z]', ' ', text.lower()) #remove non-alphabets
    tokenized_text = word_tokenize(text) #tokenize
    clean_text = [
         word for word in tokenized_text
         if word not in stopwords.words('english')
    ]
    if stem:
        clean_text=[stemmer.stem(word) for word in clean_text]
    return ' '.join(clean_text)

#Reading the csv into the dataframe
df2020 = pd.read_csv('tweets_jan_20_final.csv', usecols = ['id', 'tweet','date'], parse_dates=['date'], engine='python')
df2020 = df2020.astype({'tweet': str })

df2021 = pd.read_csv('tweets_jan_21_final.csv', usecols = ['id', 'tweet','date'], parse_dates=['date'], engine='python')
df2021 = df2021.astype({'tweet': str })


#Jan-2020 dataset cleanse           
df2020['tweet']=df2020['tweet'].apply(lambda x: process_text(x))
#Jan-2021 dataset cleanse
df2021['tweet']=df2021['tweet'].apply(lambda x: process_text(x))

df2020[df2020.tweet != '']

#move the cleansed df to a new csv to be used in the analysis step
df2020.to_csv (r'cleansed_tweets_jan_2020.csv', index = False, header=True)
df2021.to_csv (r'cleansed_tweets_jan_2021.csv', index = False, header=True)

##########################################################################################################
#Google Trends
df_trends = pd.read_csv('google_trends_extract.csv')

#remove columns and rename
df_trends = df_trends.drop('isPartial', axis = 1) #drop "isPartial"
df_trends = df_trends.drop('isPartial.1', axis = 1) #drop "isPartial.1"
df_trends.columns=['date','Vegan-US','Veganuary-US'] #Change column names

#generate final .csv file
df_trends.to_csv (r'cleansed_google_trends.csv')

