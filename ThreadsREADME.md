# ThreadsScamDetector
Taiwan Scam Detection, NLP

## Number of data in each category
*Update on 2/10*
total datas: 15847

## Introduction

## Data Collection
In this study, we conducted two main phases of data collection:
1. Initial Search Using Scrapfly API
    We utilized the Scrapfly API to search for posts that may be related to Scamming on Threads. We conduted preliminary filtering using keywords. Targeted webpages were then crawled to collect textual and related information. At the bottom are phases that we used as keywords:
        Text, Text ID, User profile pictures, Number of replies, Number of likes, Image URLs
2. Large-Scale Data Collection
    To meet the requirements for model training and testing, we conducted additional large-scale data collection. A total of 15847 labeled posts were collected, not using the Scrapfly API but through custom web scraping scripts. 
    The categories and their subtypes are as follow:
    1. Emotional Datting Scams:
        Finding new boyfriend/girlfriend  |找新男友/女友
        Finding people to chat            |找人聊天
        Online Dating App                 |交友軟體
        Adult Videos                      |成人影片
    2. Working Scams: 
        Easy money                        |輕鬆工作、輕鬆賺錢
        Work from home                    |在家工作  
        Chatting for money                |聊天賺錢
        Earn few thousand of money a day  |一天賺幾千塊
    3. Investment Scams:
        Making money investing in cryptocurrencies|投資加密貨幣
        Zero-Risk Investment, Guaranteed Profit   |零風險、穩賺不賠
        Investment Online Group                   |投資群組
        Passive income                            |被動收入
    4. Gambling Scams:
        Online Casinos/Baccarat   |娛樂城/百家樂
        Sports Betting Analysis   |運彩分析
        High Return Rates         |高倍返利
        Free Credits/Top-ups      |贈送儲值金
    during the collection process, we separated the dataset into four categories of Scams using keywords related to each type.
## Data Preprocessing
During data preprocessing stage, we organized files and texts to help our follow-up action more efficient.
1. Text processing:
    First we converted emojis into their text version(English), then we differentiated texts into four types:
        1. Chinese_text: Only chinese words
        2. Cleaned_text: Original text without emojis and URLs
        3. Http_text: Only URLs
        4. Emoji_text: Only emojis in english
2. Calculate numbers and fill in missing label in data:
    We found out that there is some missing label(0, 1) in our data, so we first manually analyzed and filled the missing label to make sure no label are NaN, then we calculated basic data for every type of text, such as text length, explination...
## Data Analysis
After data preprocessing, we tried to analyze our data to help us know more features about the data and choose what type of Machine Learning method is more appropriate. Not only this, but it also help us identify which features are most valuable for prediction, and may optimize model performance through feature transformation.
1. Count of labels(0, 1) in four different categories
2. Text length distribution in different text type(origin, chinese, cleaned)
3. Text length comparison in different text type
4. Extract texts with a length less than 10
5. Extract texts with a length more than 500
6. Wordcloud of different categories
7. Frequency of Https and Emojis occurrences for the two labels(0, 1)