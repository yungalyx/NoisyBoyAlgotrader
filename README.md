## NoisyBoyAlgotrader

Noisyboy serves is a 3-part finance robot with a 
  1. backtesting/research environment
  2. integration with live/paper-trading 
  3. dashboard frontend for simple tracking

### Backtesting:
arguably the most important component of building a trading bot is making sure that your bot makes money and is a more worthwhile investment than any alternative financial instrument. The strategies I created here have worked quite well in the past, Sharpe: 1.6, Accuracy: 85% trades successful, Annual Return: 150%

Some finance theories I have integrated into my code are: 
+ Modern Portfolio Theory
+ Kelly Criterion
+ testing against Monte Carlo Simulations (Robustness/Stress Testing)

Technicals:
+ pyalgotrade library 
+ backtrader library

![Image of stonks](/stonks.png)

### Live/Paper trading:
There's two ways to get data: 
1. HTTP Requests on 'historical data', the bot doesn't see what happens for 1 full minute until that candle closes (totally viable, a little easier to do in all honesty), but you're behind by 1 minute. 
2. Stream data via a WEBSOCKET, with Tiingo, IEXcloud, or Polygon. 

Secondly, the difficulty is finding a way to continously start this algorithim exactly at 9:30 AM EST, and have it run/capture data throughout the day. (I never want to wake up at 6:30 to trade stocks ever in my life please). Next steps is finding a way to host program on a server. 

Technicals: 
+ ALPACA API (HTTP)
+ TIINGO DATA STREAM - BOOK OF ORDERS (WEBSOCKET)

### Dashboard: 
Thought it would nicely wrap up this algotrading system if I incorporated a dashboard that shows the trades i've entered, along with a portfolio that dynamically shows my statistics. 
In integration with the live-trading aspect, I would need to be able to upload all this to a server somewhere so it can run without eating up all the CPU on my laptop. 

Technicals: 
+ DASH Library with PLOTLY and CSV. 
++ save streamed data to a CSV, deploy CSV to PYPLOY, run PYPLOY on JavaScript somewhere. 
