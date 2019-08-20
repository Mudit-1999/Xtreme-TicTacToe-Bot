# Xtreme TicTacToe Bot

## Team Members
* Divyesh Jain - 20171171
* Mudit Agarwal - 20171090

## Result 
 In the tournament of bots, in which a total of 70+ bots participated ( 150+ participants), we reached to the semifinals of the tournament.

## Strengths of our Bot 

Some strengths of our bot are that might have set it apart from the bots it beat are:

### Quiescence search - 
Human players usually have enough intuition to decide whether to abandon a bad-looking move, or search a promising move to a great depth. A quiescence search attempts to emulate this behavior by instructing a computer to search "interesting" positions to a greater depth than "quiet" ones to make sure there are no hidden traps and to get a better estimate of its value.

### Weighted Action 
Our bot used pre-calculated values(from experiments) about the probability of winning the game for all cells, which would have helped in predicting better moves. Our heuristic also had larger negative values for unfavorable situations, which might have been helpful in avoiding them.

### Behave Greedily towards the end of game 
In case of multiple possible winning moves in close vicinity(within search depth), our bot chooses the closest one. Removing this condition can result in the bot losing despite having the winning move at depth 1. So, this can help the bot during later stages of the game.

## Expectations
We don’t know about the other bots, so our bot may or may not finish in top 2, but we are quite sure that it will reach the semi-finals.
