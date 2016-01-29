from constants import Constants 
from loadout import Loadout
from sides import Sides
import numpy as np
import simpy
import pdb


class Player(object):
  """ Class that represents a CSGO player"""

  def __init__(self, steam_id, team, acc, hs_percentage):
    # the player's id
    self.steam_id = steam_id
    # percentage of shots that hit, accuracy
    self.acc = acc
    # percentage of hits that hit the head
    self.hs_percentage = hs_percentage

    # the team 
    self.team = team
    # the player's health, this changes when the teams "fight"
    self.health = 100

    # the current hotspot that the player is in
    self.current_location = 0

    self.action = None
    # if the player is alive or dead
    self.is_alive = True
    self.env = None
    self.money = Constants.STARTING_MONEY
    self.loadout = Loadout()

  def respawn(self, env, pistol):
    """ Add the player to the new environment and reset player statistics"""
    self.env = env
    self.action = env.process(self.play(self.env))
    self.health = 100
    self.is_alive = True
    if (pistol):
      self.money = Constants.STARTING_MONEY



  def play(self, env):
    """Process that simulates the player's actions. This is run once every round until
    the round is over"""

    # choose a random time, this will make it so the first to attack is non deterministic
    yield env.timeout(np.random.uniform(0.0, 5.0))
    while(self.is_alive):
      # if self.is_alive == True:
      target = self.choose_target()
      shots_fired = np.random.uniform(0.0, 5.0)
      weapon = self.loadout.get_weapon()
      if (weapon.out_of_ammo()):
        yield env.timeout(weapon.reload())
      elif target == -1:
        yield env.timeout(np.random.uniform(0.0, 5.0))


      else:
        target.inflict_self(self.determine_damage(weapon, shots_fired))        
        yield env.timeout(np.random.uniform(0.0, 5.0))


  def determine_damage(self, weapon, rounds):
    """The amount of damage the player will inflict on the enemy"""
    shots_fired = weapon.fire_burst(rounds)
    shots_hit = np.random.binomial(shots_fired, self.acc)
    head_shots = np.random.binomial(shots_hit, self.hs_percentage)
    body_shots = shots_hit - head_shots
    head_damage = head_shots * weapon.damage * 4
    helmet_damage = head_shots * weapon.helmet_damage
    body_damage = body_shots * weapon.damage
    armour_damage = body_damage * weapon.pen_power
    return [body_damage, head_damage, armour_damage, helmet_damage]


  def choose_target(self):
    """Choose a target to attack from the enemies in the hotspot"""

    # 1 - side converts 0 to 1 and 1 to 0
    enemy_list = self.current_location.players[1 - self.team.side]
    num_enemies = len(enemy_list)

    # if there are no enemies currently in the same location of the player
    # simply return 0
    if num_enemies == 0:
      return -1

    # pick an enemy randomly from the list of enemies and return their object
    return enemy_list[np.random.random_integers(0, num_enemies - 1)]


  def get_side(self):
    return self.team.side

  def inflict_self(self, damage):
    """Inflict damage onto own class. If damage moves health below 0, mark the 
    player as "Dead" and remove them from the map"""
    body_damage = damage[0]
    head_damage = damage[1]
    armour_damage = damage[2]
    helmet_damage = damage[3]
    damage_to_kevlar = body_damage - armour_damage
    through_damage = self.loadout.damage_kevlar(damage_to_kevlar)

    final_damage = 0
    if (self.loadout.helmet == True):
      final_damage = helmet_damage + armour_damage + through_damage
    else:
      final_damage = head_damage + armour_damage + through_damage

    self.health = self.health - final_damage
    if self.health <= 0:
      self.current_location.players[self.team.side].remove(self)
      self.is_alive = False
      self.loadout.clear()

  def charge(self, cost):
    """Subtract cost from the player's money. If the amount of money they have goes
    below 0 throw a NegativeMoneyException"""
    try:
      money = self.money
      money -= cost
      if (money < 0):
        raise NegativeMoneyException()
      else:
        self.money = money
    except NegativeMoneyException as e:
      print "{0} spent more money than they have in their bank\n".format(self.steam_id)
      print e
      print "\n"

  def add_money(self, amount):
    money = self.money + amount
    if (money >= Constants.MAX_MONEY):
      self.money = Constants.MAX_MONEY
    else: 
      self.money = money

  def reset_money(self):
    self.money = Constants.STARTING_MONEY

  def __str__(self):
    return "Steam id: {0}\tIs Alive: {1}\tCurrent Bank: {2}".format(self.steam_id, self.is_alive, self.money)



def tests():
  return

if __name__ == "__main__":
  tests()

class NegativeMoneyException(Exception):
  def __init__(self):
    self.message = "Money has gone below 0"
  def __str__(self):
    return self.message


