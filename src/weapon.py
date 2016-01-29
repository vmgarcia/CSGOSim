from constants import Constants

class Weapon(object):
  """This class is the model representation of a weapon from CSGO. It will be held in
  the player's loadout"""
  def __init__(self, name):
    weapon = Constants.WEAPONS_LIST[Constants.WEAPONS_LIST.Name == name].iloc[0]
    full_auto = True
    if (weapon["Hold to Shoot"] == 'No'):
      full_auto = False
    self.name = name
    self.damage = float(weapon["Damage"])
    self.helmet_damage = float(weapon["Helmet Damage"])
    self.price = float(weapon["Price"][1:].replace(',', ''))
    self.kill_award = float(weapon["Kill Award"][1:].replace(',', ''))
    self.pen_power = float(weapon["Armor Penetration"][:-1]) / 100
    self.reload_time = float(weapon["Reload (Fire Ready)"])
    self.mag_size  = float(weapon["Magazine Size"])
    self.ammo_count = self.mag_size
    self.reserve_ammo = float(weapon["Ammo in Reserve"])
    self.firerate = float(weapon["Firerate (RPM)"])
    self.full_auto = full_auto


  def __str__(self):
    part1 = "Weapon name: {0}\nDamage: {1}\nPrice: {2}\nKill Award: {3}\nPenetration Power: {4}\n".format(self.name, 
      self.damage, self.price, self.kill_award, self.pen_power)
    part2 = "Reload Time: {0}\nMagazine Size: {1}\nReserve Ammo: {2}\nFirerate: {3}\nFull Auto: {4}\n".format(self.reload_time,
      self.mag_size, self.reserve_ammo, self.firerate, self.full_auto)

    return part1 + part2

  def fire_burst(self, rounds):
    ammo_count = self.ammo_count
    if ((ammo_count - rounds) == 0):
      self.ammo_count = 0
      return ammo_count
    else:
      self.ammo_count -= rounds
      return rounds

  def reload(self):
    self.ammo_count = self.mag_size
    return self.reload_time

  def out_of_ammo(self):
    if (self.ammo_count == 0):
      return True
    else:
      return False

def test():
  usp = Weapon("USP-S")
  print usp
  ak = Weapon("AK-47")
  print ak
  awp = Weapon("AWP")
  print awp

if __name__ == '__main__':
  test()