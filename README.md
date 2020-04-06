# NoisyBoyAlgotrader
algorithmic trading strategy

NoisyBoy is an algorithmic trading bot built on top of python with numerous libraries and apis: 
*backtrader - for backtesting and strategy creation 
*alpaca - for live and paper trading 
*pandas and mpl_finance - for storing scraped web-data and conversion into csv files for backtrader datafeed. 

Here are some of the following implementations I want to incorporate: 
1. robustness and stress testing of trading strategies (validation) prior to implementing live trading
2. Portfolio creation...backtesting one or multiple strategies against a randomized portfolio of stocks instead of single stock data feed. 
3. generating alphas to set up entry and exit targets... allowing us to use more advanced market orders
4. implementing non-financial indicators to supplement long-term investment suggestions (fear+greed indicator, google keywords)
5. notification text to user's cellphones when an order is fulfilled, with summary on profits/losses. 
6. hosting / running the algorithm for extended periods on server
