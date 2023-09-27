# Will the Fed ruin my S&P500 investments?
Fed announcements have an impact on the market. Can these events ruin investments in the S&P 500?

## Data
In the following experiment, I used the S&P500 returns and the Fed conference calendar from 2017-01-01 through 2023-09-25. This information was extracted from the following [link](https://www.federalreserve.gov/newsevents/calendar.htm).

In the next figure, one can see the evolution of the cumulative returns of the S&P500 and the days in which the Fed gave a press conference.

***S&P500 Index (SPY) evolution + Fed Press Conference Days***
![SP500 and Fed Conference Days](https://github.com/Jaldekoa/Will-the-Fed-ruin-my-S-P500-investments/blob/main/img/Plot%201.jpg?raw=true)

## Strategy
To test whether Fed announcements have a negative impact on S&P500 returns, the following strategy is followed:
 - Our portfolio is invested (100%) in the S&P500 if there are no Fed press conferences scheduled in the next 2 days.
 - If there is a press conference the next day, the current day or the day before, our portfolio is not invested (0%) in the S&P500.

With this simple strategy, we can deduce what the effect of Fed press conferences is on the value of the index.

## Results
In the following figure you can see the evolution of the portfolio applying the strategy compared to the S&P500.
![Strategy vs SP500](https://github.com/Jaldekoa/Will-the-Fed-ruin-my-S-P500-investments/blob/main/img/Plot%202.jpg?raw=true)

## References
***This project is based on the following article:***
- *Will the Fed ruin my S&P500 investments?: [https://quantdare.com/will-the-fed-ruin-my-sp500-investments/](https://quantdare.com/will-the-fed-ruin-my-sp500-investments/)*
