# Sports Betting Arbitrage

Sports betting arbitrage involves taking offsetting positions in different bookmakers with a total cost less than the payout, ensuring risk-free profit.

This uses [The Odds API](https://the-odds-api.com/) to get the odds from various bookmakers for sporting events to find these opportunities.

## Usage
You must have an API Key from The Odds API, and set the environment variable `THE_ODDS_API_KEY`.

Then you can run the file `arb.py` to write the arbitrage opportunities to a file.

## The Math

Suppose that there are two different bookmakers with the following (decimal) odds for an outcome.


|             | Bookmaker1 | Bookmaker2 |
| ----------- | ----------- | --- |
| Outcome1    | $o11$         | $o21$ |
| Outcome2    | $o12$         | $o22$ |

A single bookmaker will ensure that their own reciprocal sum of outcomes is greater than 1, namely $$\frac{1}{o_{11}} + \frac{1}{o_{12}} > 1$$ and $$\frac{1}{o_{21}} + \frac{1}{o_{22}} > 1$$

However if this sum is less than 1, then it means that the bookmakers disagree on the chances of the outcomes and we can profit from the discrepency, namely $$\frac{1}{o_{11}} + \frac{1}{o_{22}} < 1$$ or $$\frac{1}{o_{12}} + \frac{1}{o_{21}} < 1$$

Without loss of generality now suppose that we have $\frac{1}{o_{11}} + \frac{1}{o_{12}} < 1$ and $o_{11} < o_{22}$

Place a bet of \$100 on outcome with the lowest odds (outcome 1 at bookmaker 1), which is $o_{11}$ in our case.  We can bet $100 * \frac{o_{11}}{o_{22}}$ on the other outcome (outcome 2 at bookmaker 2).

Then we're guarenteed to make 

$$100 * o_{11}$$ no matter what happens.

However, we've invested $100(1 + \frac{o_{11}}{o_{22}})$.

Due to some fancy math you could prove that given $\frac{1}{o_{11}} + \frac{1}{o_{12}} < 1$, the inequality  $100(1 + \frac{o_{11}}{o_{22}}) < 100 o_{11}$ always hold, ensuring a risk free profit.

## Shortcomings
In practice, arbitrage opportunities don't exist for a long time as they are quickly taken advantage of, and the possibility for human error when making bets is large. 

However, the percent return on most arbitrage opportunities is pretty small, usually 2-5%.

Also, while legal, bookmakers try to minimize sports betting arbitrage by working together to find arbitragers, so whether you care to use this is up to you.