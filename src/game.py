from player import Player
from game_map import Game_Map
from team import Team
from sides import Sides
from constants import Constants
import simpy
import pdb
import sys

def game(team_name1, team_name2):

  team_a = Team(team_name1, Sides.CT)
  team_b = Team(team_name2, Sides.T)
  for i in range(Constants.GAMES_TO_PLAY):
    pistol = True
    for j in range(30):
      gmap = Game_Map()

      env = simpy.Environment()
      if (j == 16):
        switch_sides(team_a, team_b)
        pistol = True

      if (team_a.side == Sides.CT):
        team_a.respawn_players(env, pistol)
        team_b.respawn_players(env, pistol)
      else:
        team_b.respawn_players(env, pistol)
        team_a.respawn_players(env, pistol)
      pistol = False



      gmap.spawn_team(team_a)
      gmap.spawn_team(team_b)
      env.run(env.process(round(team_a, team_b, env)))

      if (team_a.round_wins == 16 or team_b.round_wins == 16):
        break
    game_over(team_a, team_b)
  print team_a
  print team_b
  return [float(team_a.game_wins)/float(team_a.game_wins + team_b.game_wins)*100, 
    float(team_a.total_round_wins)/ float(team_a.total_round_wins + team_b.total_round_wins) * 100]

def game_over(team_a, team_b):
  if (team_a.round_wins == 16):
    team_a.game_wins += 1
    team_a.round_wins = 0
    team_b.round_wins = 0
  elif (team_b.round_wins == 16):
    team_b.game_wins += 1
    team_a.round_wins = 0
    team_b.round_wins = 0
  else:
    team_a.game_wins += .5
    team_b.game_wins += .5
    team_a.round_wins = 0
    team_b.round_wins = 0



def round(team_a, team_b, env):
  """ The representation of a round of counterstrike. Will poll every
  5 simulated seconds to see if conditions have been met for a round to be over."""
  while True:
    if team_a.all_dead():
      team_a.loss()
      team_b.win()

      # print team_a
      # print team_b

      env.exit()
    
    if team_b.all_dead():
      team_a.win()
      team_b.loss()


      # print team_a
      # print team_b

      env.exit()
    yield env.timeout(5)


def switch_sides(team_a, team_b):
  """Switch team sides and start pistol round again"""

  # arithmetic trick to switch sides
  team_a.side = ~team_a.side + 2
  team_b.side = ~team_b.side + 2




if __name__ == "__main__":
  print game("Na'Vi", "Penta")