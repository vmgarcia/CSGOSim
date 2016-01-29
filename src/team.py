from player import Player
from market import Market
from sides import Sides 
from constants import Constants
import pandas as pd

class Team(object):
  """Class that holds critical team information"""
  def __init__(self, name, side):
    self.round_wins = 0
    self.total_round_wins = 0
    self.players = []
    self.name = name
    self.side = side
    self.generate_team(name)
    self.loss_streak = 0
    self.game_wins = 0
  

  def all_dead(self):
    count = 0
    for player in self.players:
      if player.is_alive == False:
        count += 1
    if count == 5:
      return True
    else: 
      return False

  def respawn_players(self, env, pistol):

    for player in self.players:
      if (pistol):
        player.reset_money()

      player.respawn(env, pistol)
      Market.loadout_player(player, pistol)

  def win(self):
    self.round_wins += 1
    self.total_round_wins += 1
    self.loss_streak = 0

    for player in self.players:
      player.add_money(Constants.WIN_BONUS)


  def loss(self):
    for player in self.players:
      player.add_money(Constants.LOSS_BONUSES[self.loss_streak])

    if (self.loss_streak < Constants.MAX_LOSS_STREAK - 1):
      self.loss_streak += 1




  def generate_team(self, name):
    td = pd.read_csv("res/team_stats.tsv", sep="\t")
    team_data = td[td["Team Name"] == name]

    for index, row in team_data.iterrows():

      self.players.append(Player(row["Steam ID"], self, row["Accuracy"], row["HS Percentage"]))



  def __str__(self):
    rep = "Team: {0}, Round Wins: {1}\nGame Wins: {2}\n".format(self.name, self.total_round_wins, self.game_wins)
    for player in self.players:
      rep += player.__str__() + '\n'

    return rep

  __rep__ = __str__


def test():
  player = Player(1, Team("Na'Vi", Sides.CT), .5, .2)
  Market.loadout_player(player, True)
  print player.loadout
  player.money += 4400
  Market.loadout_player(player, False)
  print player.loadout
if __name__ == "__main__":
  test()


