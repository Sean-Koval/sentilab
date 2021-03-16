# Market Sentiment Tools


## Reddit

### wsb

```
command: wsb [-1 N_LIMIT] [-n]
```

Print what the WSB subreddit is talking about.
    * -1: Max number of posts to print (def=10)
    * -n: If True the posts are printed based off recency rather than sccore (def=False)

### watchlist

```
command: watchlist [-l N_LIMIT]
```

Print other users watchlist
  * -l : limit of posts to print (def=5)



### popular

```
command: popular [-l N_LIMIT] [-s S_SUBREDDIT] [-d N_DAYS]
```

Print latest popular tickers. [Source: Reddit]
  * -l : limit of posts retrieved per sub reddit. Default 50.
  * -s : subreddits to look for tickers, e.g. pennystocks, stocks (def=pennystocks), RobinHoodPennyStocks, Daytrading, StockMarket, stocks, investing, wallstreetbets
  * -d : look for the tickers from those n past days (def=1)



### spac_c

```
command: spac_c [-l N_LIMIT] [-p]
```

Print other users SPACs announcement under subreddit "SPACs"
  * -l : limit of posts with SPACs retrieved (def=10)
  * -p : popular flag, if true the posts retrieved are based on score rather than time. Default False


### spac

```
command: spac [-h] [-l N_LIMIT] [-d N_DAYS]
```

Print other users SPACs announcement under subreddit "SPACs"
  * -l : limit of posts with SPACs retrieved (def=5)
  * -d : look for the tickers from those n past days (def=5)