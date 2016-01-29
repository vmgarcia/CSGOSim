import networkx as nx
from hotspot import Hotspot
import matplotlib.pyplot as plt
class Game_Map(object):
  """ Generic map that represents general outline of all counter strike maps"""

  def __init__(self):
    self.graph = nx.Graph()
    self.spawns = [Hotspot()]
    self.graph.add_node(self.spawns[0])

  def add_team(team):
    #side = team.side
    side = 0
    for player in team.players:
      self.spawns[side].move_into(player)

  def spawn_team(self, team):
    for player in team.players:
      self.spawns[0].move_into(player)


  def draw(self):
    nx.draw(self.graph)
    plt.show()

def tests():
  """Tests to see that Game_Map class works properly"""
  
  # initialize the map
  gmap = Game_Map()
  gmap.draw()



# if this module is being run explicitly from the command line
# run tests to assure that this module is working properly
if __name__ == "__main__":
  tests()