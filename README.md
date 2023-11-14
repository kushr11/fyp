# fyp
run strategy.py to generate figures and result excel
# Strategy
For a down market last for 60 days use linear regression to judge）, the price kept moving downward with current trough fell below previous trough. However, the RSI is NOT with the same pattern. That is the current trough of RSI is above the previous trough. That implies a stronger momentum in the stock price even the down trend continue. The most favorable situation is that price kept moving downward with current trough fell below previous trough. However, the current trough of RSI does not fell below the level of 30 and above the previous trough. Then, LONG strategy can be applied (buy)

If price of holding stock increase 5%, then sell
# result
## overall result
result 60.csv is the result of all stocks applying the above strategy from 2021-08-23 to 2023-09-23.

result 30.csv is the result of all stocks applying the above strategy（but down market for 30 days） from 2021-08-23 to 2023-09-23.

1st column: stock symbol; 

2st column: final balance with initial balance=1000000; 

3st column: profit rate= (final balance-initial balance)/initial balance. The higher the better.


## individual result for stocks
./result/plotxxxx.HK.png is the result of one stock applying the above strategy(down market for 60 days) from 2021-08-23 to 2023-09-23.
