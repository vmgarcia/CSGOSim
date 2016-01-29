from bs4 import BeautifulSoup
from socket import error as SocketError
from time import sleep
import errno
import urllib2 as url
import pandas as pd



def get_match_data(match_number):
  base_url = "http://csgolounge.com/match?m={0}"
  try:
    html = url.urlopen(base_url.format(match_number)).read()
    soup = BeautifulSoup(html)
    teams = soup.find("section").find_all("b")
    odds = soup.find("section").find_all("i")
    team_a = teams[0].contents[0].encode("ascii", "ignore")
    team_b = teams[1].contents[0].encode("ascii", "ignore")
    team_a_odds = odds[0].contents[0].encode("ascii", "ignore").replace("%", "").strip()
    team_b_odds = odds[1].contents[0].encode("ascii", "ignore").replace("%", "").strip()
    winner = -1 
    if (team_a.find("(win)") != -1):
      winner = 0
      team_a = team_a.replace("(win)", "").strip()
      team_b = team_b.strip()
    elif (team_b.find("(win)") != -1):
      winner = 1
      team_b = team_b.replace("(win)", "").strip()
      team_a = team_a.strip()

    return pd.DataFrame({"Team A": team_a, "Team A Odds": team_a_odds, "Team B": team_b, "Team B Odds": team_b_odds, "Winner": winner}, 
      index = [match_number])
  except IndexError as e:
    print "Index Error"
  except SocketError as e:
    print "Socket reset"
    if e.errno != errno.ECONNRESET:
      print "socket problem"
  return pd.DataFrame()

def generate_archive():
  newest_match = 3283
  oldest_match = 2900
  data = pd.DataFrame()
  for match_no in range(oldest_match, newest_match+1):
    row = get_match_data(match_no)
    if (not row.empty):
      data = data.append(row)
    sleep(.5)


  #df.append(data, ignore_index=True)
  file_name = "./res/match_archive.tsv"

  data = data.sort(ascending=False)
  data.to_csv(file_name, sep="\t")
  return data


if __name__ == "__main__":
  print generate_archive()
