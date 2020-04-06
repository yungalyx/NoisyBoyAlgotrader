# NoisyBoyAlgotrader
algorithmic trading strategy

NoisyBoy is an algorithmic trading bot built on top of python with numerous libraries and apis: 
*backtrader - for backtesting and strategy creation 
*alpaca - for live and paper trading 
*pandas and mpl_finance - for storing scraped web-data and conversion into csv files for backtrader datafeed. 

Here are some of the following implementations I want to incorporate: 
1. Portfolio creation...backtesting one or multiple strategies against a randomized portfolio of stocks instead of single stock data feed. 
2. generating alphas (QuantConnect term) to set up entry and exit targets... allowing us to use more advanced market orders
3. implementing non-financial indicators to supplement long-term investment suggestions (fear+greed indicator, google keywords)
4. notification text to user's cellphones when an order is fulfilled, with summary on profits/losses. 
5. hosting / running the algorithm for extended periods on server
