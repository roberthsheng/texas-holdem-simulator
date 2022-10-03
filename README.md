# Texas Hold'em Simulator
This is a Python implementation of a Texas Hold'em Monte Carlo Simulator.

Currently, this only simulates heads-up poker. May consider creating option to add more players in the future.

To play, type `$ python simulator.py --iters 5000 --hand Tc2c` in your command line, where `--iters` is the number of iterations you want to run and `--hand` is the hand you want to play. The hand must be in the format `Tc2c` where the first two characters are the rank and suit of the first card and the last two characters are the rank and suit of the second card. The ranks are as follows:

| Rank | Symbol |
|------|--------|
| Ace  | A      |
| Two  | 2      |
| Three| 3      |
| Four | 4      |
| Five | 5      |
| Six  | 6      |
| Seven| 7      |
| Eight| 8      |
| Nine | 9      |
| Ten  | T      |
| Jack | J      |
| Queen| Q      |
| King | K      |

The suits are as follows:
| Suit | Symbol |
|------|--------|
| Clubs| c      |
| Diamonds| d   |
| Hearts| h     |
| Spades| s     |

The output will be the probability of winning, losing, and tying for the given hand.

## Example
```
$ python simulator.py --iters 5000 --hand Tc2c
Running 5000 iterations...
Win: 0.0%
Lose: 100.0%
Tie: 0.0%
```

## TODO
- [ ] Add more players
- [ ] Add more options for betting

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details