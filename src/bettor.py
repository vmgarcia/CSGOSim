import numpy as np
import pandas as pd
from constants import Constants as const
from matplotlib import pyplot as plt
from game import *

class Bettor(object):
  def __init__(self, strategy):
    self.bankroll = const.BANKROLL
    self.bet_amount = const.BET_AMOUNT
    self.strategy = strategy
    self.history = [(2850, self.bankroll)]

  def bet(self, pop_odds, true_odds, result, match_no):
    if (self.bankroll < self.bet_amount): 
      print "Out of money"
      return 

    # place bet
    self.bankroll -= self.bet_amount
    bet = self.bet_amount
    choice = None
    if (self.strategy == 0):
      choice = pop_odds.index(min(pop_odds))
    elif (self.strategy == 1):
      choice = pop_odds.index(max(pop_odds))
    elif (self.strategy == 2):
      res = np.array(true_odds) - np.array(pop_odds)
      choice = res.tolist().index(max(res))

    if (choice == result): 
      self.bankroll += Bettor.calculate_winnings(pop_odds[choice], bet)
      self.history.append((match_no, self.bankroll))
      return
    else:
      self.history.append((match_no, self.bankroll))
      return

  @staticmethod
  def calculate_winnings(perc, bet):
    return 1/(perc / 100.0) * bet 

  def __str__(self):
    return "Final Bankroll: {0}".format(self.bankroll)

  __rep__ = __str__

def simulate_betting():
  arch = const.MATCH_ARCHIVE
  bettors = [Bettor(0), Bettor(1), Bettor(2)]

  for i in range(len(const.TEAM_NAMES)):
    for j in range(i, len(const.TEAM_NAMES)):
      team_a, team_b = const.TEAM_NAMES[i], const.TEAM_NAMES[j]
      matches = arch[arch["Team A"] == team_a][arch["Team B"] == team_b].append(arch[arch["Team B"] == team_a][arch["Team A"] == team_b])
      if (not matches.empty):
        for index, row in matches.iterrows():
          result = row["Winner"]
          if (result == 0 or result == 1):
            true_stats = game(team_a, team_b)
            for bettor in bettors:
              bettor.bet([float(row["Team A Odds"]), float(row["Team B Odds"])], [true_stats[0], 100 - true_stats[0]], int(row["Winner"]), 
                int(row["Match_No"]))
  for bettor in bettors:
    print bettor
    plt.plot(*zip(*sorted(bettor.history, key = lambda x: x[0])), label=const.STRATEGIES[bettor.strategy])
  plt.legend()
  plt.show()
if __name__ == "__main__":
  simulate_betting()

