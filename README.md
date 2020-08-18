## NoisyBoyAlgotrader

NoisyBoy is the first bot in the Algotrader projects, this bot focuses on backtesting and strategy creation. 

### Backtesting:
arguably the most important component of building a trading bot is making sure that your bot makes money and is a more worthwhile investment than any alternative financial instrument. The current strategy employed is a consecutive 2-day Bollinger Band mean reversion strat. Sharpe: 1.6, Accuracy: 85% trades successful.

Some finance theories I have integrated into my code are: 
+ Modern Portfolio Theory (no overexposure to any single asset or industry)
+ Kelly Criterion (dynamic position sizing based on expected returns to optimize profits)

Technicals:
+ pyalgotrade library 
+ backtrader library

![Image of stonks](/stonks.png)

