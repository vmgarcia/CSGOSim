import pandas as pd
class Constants(object):
  # the amount of money each player starts with
  STARTING_MONEY = 800

  # the maximum amount of money that can be held by
  # any given player
  MAX_MONEY = 16000

  # every consecutive lost round the team that lost gets
  # a bonus to the amount of money they gain
  LOSS_BONUSES = [1400, 1900, 2400, 2900, 3400]
  MAX_LOSS_STREAK = 5

  # amount of money won by winning a round
  WIN_BONUS = 3250


  # amount of money won when a team wins by planting or defusing
  # the bomb
  BOMB_BONUS = 3500

  KEVLAR_COST = 650

  HELMET_COST = 1000 - 650

  WEAPONS_LIST = pd.read_csv("./res/weapon_stats.tsv", sep = "\t")
  MATCH_ARCHIVE = pd.read_csv("./res/match_archive.tsv", sep = "\t")

  ROUNDS_TO_WIN = 16
  HALF_TIME = 16
  GAMES_TO_PLAY = 50

  ####################
  # BETTING STUFF
  ####################
  TEAM_NAMES = ["Na'Vi", "VP", "Penta", "CLG", "Liquid", "Titan"]
  BANKROLL = 1000
  BET_AMOUNT = 50

  STRATEGIES = ["Underdog", "Overdog", "Simulation"]