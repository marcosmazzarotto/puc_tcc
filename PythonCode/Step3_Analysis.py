#Libraries
import pandas as pd # Pandas - Data manipulation and analysis library
import numpy as np # NumPy - mathematical functions on multi-dimensional arrays and matrices
from textblob import TextBlob # TextBlob - Python library for processing textual data
from wordcloud import WordCloud# WordCloud - Python linrary for creating image wordclouds
import matplotlib.pyplot as plt # Matplotlib - plotting library to create graphs and charts
import seaborn as sns
import plotly.express as px
from sklearn.feature_extraction.text import CountVectorizer

pd.set_option('display.max_colwidth', 500) #tweak column view size

#import ready to use csv file from step 2
df2020 = pd.read_csv('cleansed_tweets_jan_2020.csv', usecols = ['id', 'tweet','date'], dtype={'tweet': str}, parse_dates=['date'])  #read from csv
df2020['tweet'] = df2020['tweet'].astype(str)
df2021 = pd.read_csv('cleansed_tweets_jan_2021.csv', usecols = ['id', 'tweet','date'], dtype={'tweet': str}, parse_dates=['date'])  #read from csv
df2021['tweet'] = df2021['tweet'].astype(str)


#Classes for analysis
class TweetAnalyzer():
    
    def sentiment_polarity(self, Tweets_df):
      tweets_sentiments_list = []
      
    def getTextSubjectivity(self,txt):
        return TextBlob(txt).sentiment.subjectivity

    def getTextPolarity(self,txt):
        return TextBlob(txt).sentiment.polarity
    
    # negative, neutral, positive analysis
    def getTextAnalysis(self,a):
        if a < 0:
            return "Negative"
        elif a == 0:
            return "Neutral"
        else:
            return "Positive"

#CLass Instance
analyzer = TweetAnalyzer()

#chamando a funcao e colocando a ultima coluna como Sentiment, passando o dataframe para ser usado no loop do sentiment_polarity

df2020['Subjectivity'] = df2020['tweet'].apply(analyzer.getTextSubjectivity)
df2020['Polarity'] = df2020['tweet'].apply(analyzer.getTextPolarity)
df2020['Score'] = df2020['Polarity'].apply(analyzer.getTextAnalysis)

df2021['Subjectivity'] = df2021['tweet'].apply(analyzer.getTextSubjectivity)
df2021['Polarity'] = df2021['tweet'].apply(analyzer.getTextPolarity)
df2021['Score'] = df2021['Polarity'].apply(analyzer.getTextAnalysis)


#2020 counts
df2020_totals = pd.DataFrame(columns=['Year','TotalTweets', 'TotalPercentage'])
df2020_totals['TotalTweets'] = df2020['Score'].value_counts() 
df2020_totals['TotalPercentage'] = df2020['Score'].value_counts(normalize=True) 
df2020_totals['Year'] = 2020
#2021 counts
df2021_totals = pd.DataFrame(columns=['Year','TotalTweets', 'TotalPercentage'])
df2021_totals['TotalTweets'] = df2021['Score'].value_counts() 
df2021_totals['TotalPercentage'] = df2021['Score'].value_counts(normalize=True)   
df2021_totals['Year'] = 2021

#merging
dfcounts = df2020_totals.append(df2021_totals)

#Visual for percentage 2020
dfperc = pd.DataFrame(columns=['date','Positive', 'Negative', 'Neutral'])
df = df2020['Score'].value_counts(normalize=True).to_frame(name = 'percent')
df_tr = df.transpose()
dfperc['Positive'] = df_tr['Positive']
dfperc['Negative'] = df_tr['Negative']
dfperc['Neutral'] = df_tr['Neutral']
dfperc['date'] = 2020
#Visual for percentage 2021
dfperc1 = pd.DataFrame(columns=['date','Positive', 'Negative', 'Neutral'])
df = df2021['Score'].value_counts(normalize=True).to_frame(name = 'percent')
df_tr = df.transpose()
dfperc1['Positive'] = df_tr['Positive']
dfperc1['Negative'] = df_tr['Negative']
dfperc1['Neutral'] = df_tr['Neutral']
dfperc1['date'] = 2021

dfperc = dfperc.append(dfperc1)

sns.set(
    rc={'figure.figsize':(7,5)}, 
    style="white" # nicer layout
)
#graphic with visuals for percentage 2020x2021
data = dfperc.melt('date', var_name='Sentiment', value_name='Percentage')
ax=sns.barplot(x='date', y='Percentage', hue='Sentiment', data=data)


#preparing df for graphic - 2020
positive = df2020[df2020['Score'] == 'Positive']
negative = df2020[df2020['Score'] == 'Negative']
neutral = df2020[df2020['Score'] == 'Neutral']

#Dataframe with 2020 values for graphic
dfdsg2020= pd.DataFrame(columns=['date','Positive', 'Negative', 'Neutral'])
df = positive.groupby( [ "date", "Score"] ).size().to_frame(name = 'count').reset_index() #Positive
dfdsg2020['date'] = df['date']
dfdsg2020['Positive'] = df['count']
df = negative.groupby( [ "date", "Score"] ).size().to_frame(name = 'count').reset_index() #Negative
dfdsg2020['Negative'] = df['count']
df = neutral.groupby( [ "date", "Score"] ).size().to_frame(name = 'count').reset_index() #Negative
dfdsg2020['Neutral'] = df['count']

#preparing df for graphic - 2021
positive = df2021[df2021['Score'] == 'Positive']
negative = df2021[df2021['Score'] == 'Negative']
neutral = df2021[df2021['Score'] == 'Neutral']

#Dataframe with 2021 values for graphic
dfdsg2021= pd.DataFrame(columns=['date','Positive', 'Negative', 'Neutral'])
df = positive.groupby( [ "date", "Score"] ).size().to_frame(name = 'count').reset_index() #Positive
dfdsg2021['date'] = df['date']
dfdsg2021['Positive'] = df['count']
df = negative.groupby( [ "date", "Score"] ).size().to_frame(name = 'count').reset_index() #Negative
dfdsg2021['Negative'] = df['count']
df = neutral.groupby( [ "date", "Score"] ).size().to_frame(name = 'count').reset_index() #Negative
dfdsg2021['Neutral'] = df['count']

result = dfdsg2020.append(dfdsg2021)
                                                   
#grafico comparativo para os 2 anos
sns.reset_defaults()
sns.set(
    rc={'figure.figsize':(7,5)}, 
    style="white" # nicer layout
)
#2020
sns.set(color_codes=True)
dx = dfdsg2020.plot(figsize = (10,6),x="date", y=['Positive', 'Negative', 'Neutral'], kind="line", title = "Sentiment Trend 2020")
dx.set_xlabel('Date')
dx.set_ylabel('# Tweets')
dx.tick_params(axis='both', which='both', labelsize=10)

#2021
dx = dfdsg2021.plot(figsize = (10,6),x="date", y=['Positive', 'Negative', 'Neutral'], kind="line", title = "Sentiment Trend 2021")
dx.set_xlabel('Date')
dx.set_ylabel('# Tweets')
dx.tick_params(axis='both', which='both', labelsize=10)

# Creating a word cloud
#Remove Collection Words
words = ' '.join([tweet for tweet in df2021['tweet']])
words = words.replace('veganuary', '')
words = words.replace('vegan', '')
words = words.strip()

wordcloud = WordCloud(width = 800, height = 800,
                background_color ='white',
                min_font_size = 10,collocations=False).generate(words)
  
# plot the WordCloud image                       
plt.figure(figsize = (6, 6), facecolor = None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad = 0)
plt.show()

####Google Trends 
#Dataframe cleansed
df_trends = pd.read_csv('cleansed_google_trends.csv')

import seaborn as sns
sns.set(color_codes=True)
dx = df_trends.plot(figsize = (12,8),x="date", y=['Vegan-US','Veganuary-US'], kind="line", title = "Vegan Google Trends")
dx.set_xlabel('Date')
dx.set_ylabel('Trends Index')
dx.tick_params(axis='both', which='both', labelsize=10)

