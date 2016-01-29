from constants import Constants
from sides import Sides
from weapon import Weapon
from loadout import Loadout
from player import Player
import numpy as np
class Market(object):

  @staticmethod
  def loadout_player(player, pistol = False):
    """Depending on how much money the player has, buy them weapons and armor"""
    weapons_list = Constants.WEAPONS_LIST
    side = player.get_side()
    cost = 0
    primary = player.loadout.primary
    secondary = player.loadout.secondary
    if (side  == Sides.CT):
      # if it is the pistol round, give the players standard pistol round loadout
      secondary = Weapon("USP-S")

      if (pistol):
        kevlar = 100
        player.loadout.secondary = secondary
        cost += player.loadout.check_kevlar()
      elif(player.money >= 4200):
        cost += player.loadout.check_helmet_kevlar()
        new_weapon = Weapon("M4A1-S")
        if (player.loadout.check_primary(new_weapon)):
          primary = new_weapon
          cost += primary.price

      elif(player.money >= 3250):
        cost += player.loadout.check_helmet_kevlar()
        new_weapon = Weapon("FAMAS")
        if (player.loadout.check_primary(new_weapon)):
          primary = new_weapon
          cost += primary.price

      elif(player.money >= 1500):
        # 25% of the time they will force buy, the rest of the time they will save
        result = np.random.binomial(1, .25)
        if (result == 1):
          new_weapon = Weapon("Five-SeveN")
          if (player.loadout.check_secondary(new_weapon)):
            secondary = new_weapon
            cost += secondary.price
          cost += player.loadout.check_helmet_kevlar()

    else:
      secondary = Weapon("Glock-18")


      if (pistol):
        kevlar = 100 
        cost += player.loadout.check_kevlar()
      elif(player.money >= 3700):
        cost += player.loadout.check_helmet_kevlar()
        new_weapon = Weapon("AK-47")
        if (player.loadout.check_primary(new_weapon)):
          primary = new_weapon
          cost += primary.price

      elif(player.money >= 3000 ):
        cost += player.loadout.check_helmet_kevlar()
        primary = Weapon("Galil AR")
        cost += primary.price

      elif(player.money >= 1500):
        # 25% of the time they will force buy, the rest of the time they will save
        result = np.random.binomial(1, .25)
        if (result == 1):
          new_weapon = Weapon("Tec-9")
          if (player.loadout.check_secondary(new_weapon)):
            secondary = new_weapon
            cost += secondary.price
          cost += player.loadout.check_helmet_kevlar()
      
    player.loadout.primary = primary
    player.loadout.secondary = secondary
    player.charge(cost)


