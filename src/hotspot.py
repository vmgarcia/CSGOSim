import simpy
from player import Player
from team import Team
from sides import Sides
class Hotspot(object):
  """Hotspots are the representation for different areas of the map. This is where players 'fight'."""

  def __init__(self):
    self.players = [[], []]


  def move_into(self, player):
    side = player.get_side()
    self.players[side].append(player)
    player.current_location = self

    return 1


  def __eq__(self, other):
    return id(self) == id(other)

  def __hash__(self):
    return id(self)


def tests():
  """Tests to see that hotspot works properly"""
  hotspot_list = []
  for i in range(5):
    hotspot_list.append(Hotspot())

  for spot in hotspot_list:
    team_a = Team("team_a", Sides.CT)
    team_b = Team("team_b", Sides.T)
    spot.move_into(Player(1, team_a, .5, .5))
    spot.move_into(Player(1, team_b, .5, .5))

    print "Hotspot id = {0}".format(id(spot))
    for team in spot.players:
      for player in team:
        print "player = {0} in team {1}".format(player, player.team)

if __name__ == "__main__":
  tests()