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
## Logic of Scam discrimination
We give a role to LLM which is a content moderator for social media platforms, responsible for reviewing various posts to determine whether they involve fraudulent messages. It will first decide what type of Scam this post is, and then determine if it is a fraudulent message with the standard depend on its type.  
1. 判定可能的詐騙種類
   - 判定該貼文是四種類型(情感、工作、投資、賭博)裡面的哪一種貼文:  
   - 情感: 
	- 訊息描述通常較為親密，例如: 我好想你、我愛你等...
	- 可能會是情感上的問題，例如: 分手、難過...
	- 尋找個人的情感關係，例如: 找男/女友、找人聊天、交友軟體...
   - 工作:
	- 提供輕鬆、高報酬、門檻低的工作機會，例如: 保證月入X萬...
	- 訊息提及招聘、求職、兼職等詞彙。
   - 投資:
	- 強調低風險、高回報，例如: 穩賺不賠、只漲不跌... 
	- 訊息提供投資方式，例如: 股票、加密貨幣...
	- 可能會提到投資群組、投資老師、獨家消息、被動收入等關鍵詞。
   - 賭博:
	- 會提供線上線下的賭博管道，例如: 娛樂城/百家樂、運彩...
	- 內容通常提及賭博、下注、彩票、賽事預測，例如: 內部碼、穩賺、獨家賠率...
	- 提及低風險、高回報，例如: 穩賺不賠、高勝率...
	- 為了吸引人參加賭局，提供體驗金、儲值金。
2. 判定是詐騙與否
   - 給出你是否認為該貼文為詐騙訊息的結論（例如：「判定為詐騙」、「疑似詐騙，待進一步調查」、「非詐騙訊息，但存在風險」）。
   - 詳細說明你的審查過程與論據，並標註出所有可疑點及其依據，確保審查過程客觀且具證據支持。
   - 若該貼文字數小於5，盡量將結論停留在非詐騙訊息，但存在風險，因為貼文字數過少能判別詐騙的指標就越不明顯。
   - 情感詐騙: 
    - 涉及「交友、戀愛」等情境，例如：找人聊天、交友軟體認識、遠距離戀愛等。
	- 貼文提及財務、金錢、禮品請求，例如：借錢、代付機票、匯款、幫忙支付醫療費等。
	- 聲稱遇到困難需要幫助，例如：我的信用卡被凍結了，可以先幫我付一下費用嗎？
   - 工作詐騙:
	- 提及不合理且不等價的工作關係，像是輕鬆工作拿到高報酬等。
	- 輕鬆、在家、每天幾小時、無學經歷要求賺取高薪。
	- 要求提前支付費用或提供個資，例如: 入職需繳納保證金、提交身份證註冊...
   - 投資詐騙:
	- 保證高回報、無風險，並強調短期暴利、快速翻倍，會有詐騙之疑慮。
	- 投資老師專家、投資群組，通常是詐騙無誤。
	- 有時是討論股票的價值或未來走勢，如果沒有誘導加入群組或出金投資之意圖，可能不是詐騙。
   - 賭博詐騙: 
	- 強調保證贏錢、必勝技巧，或者是誇大並張貼成功案例，會有詐騙的疑慮。
	- 誘導用戶使用百家樂/娛樂城/球板等賭博平台或加入私人群組，有較大的可能是詐騙。
	- 鼓勵新人免費試玩或送彩金。

## Data Analysis
After data preprocessing, we tried to analyze our data to help us know more features about the data and choose what type of Machine Learning method is more appropriate. Not only this, but it also help us identify which features are most valuable for prediction, and may optimize model performance through feature transformation.
1. Count of labels(0, 1) in four different categories
2. Text length distribution in different text type(origin, chinese, cleaned)
3. Text length comparison in different text type
4. Extract texts with a length less than 10
5. Extract texts with a length more than 500
6. Wordcloud of different categories
7. Frequency of Https and Emojis occurrences for the two labels(0, 1)
8. Calculate top 20 keywords