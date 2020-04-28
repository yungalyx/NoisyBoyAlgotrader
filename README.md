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
1. The difficult step here is to find a way to stream data if you want to do intraday trading (which was the original purpose of this bot).
2. Secondly, I'm competing to fill trades against the big boys on wall street. So always expect your profit to be less than it actually is, or even the possibility that your entries will be a losing trade just because of that split second difference. (2sigma, jane street, citadel: if you guys are reading this please offer me internship, youre all i want in this world ill treat you right).

Technicals: 
+ Alpaca API
+ pyalgotrade
+ datafeed from external provider

### Dashboard: 
Thought it would nicely wrap up this algotrading system if I incorporated a dashboard that shows the trades i've entered, along with a portfolio that dynamically shows my statistics. 
In integration with the live-trading aspect, I would need to be able to upload all this to a server somewhere so it can run without eating up all the CPU on my laptop. 
