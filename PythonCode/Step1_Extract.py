#Library Section
import pandas as pd # Pandas - Data manipulation and analysis library
import twint #twitter extract
import pytrends #Google trends
from pytrends.request import TrendReq
import nest_asyncio #solve issue with loop


################################################################################################
#TWEETER SECTION
################################################################################################
#function to fix loop error
nest_asyncio.apply()

#twint start
c = twint.Config()
c.Search = "vegan OR govegan OR veganuary"
c.Store_object = True
c.Lang = "en"
c.Since="2020-01-01" 
c.Until="2020-02-03" 
c.Store_csv = True
c.Output = 'tweets_jan_20.csv'

#run twint with Paramns on c
twint.run.Search(c)

print("Creating dataframes from CSVs")
#creating a dataframe 
df2020 = pd.read_csv('tweets_jan_20.csv', usecols = ['id', 'tweet','date'])  #read from csv
df2021 = pd.read_csv('tweets_jan_21.csv', usecols = ['id', 'tweet','date'])  #read from csv

#total check
df2020.count()
df2021.count()

#day check
day_group_2020 = df2020.groupby('date')['date'].count()
day_group_2021 = df2021.groupby('date')['date'].count()

day_group_2020
day_group_2021

######################################################################################################
#Google Trends Section
######################################################################################################
pytrend = TrendReq() 

#Identify exact keywords to avoid ambiguity
keywords = ['vegan','veganuary'] #defining keywords
keywords_codes = [pytrend.suggestions(keyword=i)[0] for i in keywords] #extract suggestion 
df_codes = pd.DataFrame(keywords_codes) #move to df
df_codes

EXACT_KEYWORDS=df_codes['mid'].to_list()
DATE_INTERVAL='2020-01-01 2021-01-31'
COUNTRY=["US"] #Use this link for iso country code
CATEGORY=0 # Use this link to select categories
SEARCH_TYPE='' #default is 'web searches',others include 'images','news','youtube','froogle'

Individual_EXACT_KEYWORD = list(zip(*[iter(EXACT_KEYWORDS)]*1))
Individual_EXACT_KEYWORD = [list(x) for x in Individual_EXACT_KEYWORD]
dicti = {}
i = 1
for Country in COUNTRY:
    for keyword in Individual_EXACT_KEYWORD:
        pytrend.build_payload(kw_list=keyword, 
                              timeframe = DATE_INTERVAL, 
                              geo = Country, 
                              cat=CATEGORY,
                              gprop=SEARCH_TYPE) 
        dicti[i] = pytrend.interest_over_time()
        i+=1
df_trends = pd.concat(dicti, axis=1)

df_trends.columns = df_trends.columns.droplevel(0) #drop outside header
#df_trends.to_csv (r'google_trends_extract.csv', index = False, header=True)
df_trends.to_csv (r'google_trends_extract.csv')

df_trends.count()







