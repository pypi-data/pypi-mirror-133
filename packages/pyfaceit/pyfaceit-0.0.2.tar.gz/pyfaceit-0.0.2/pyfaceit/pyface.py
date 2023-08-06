import requests
import sys

sys.path.insert(1,'/pyfaceit/games')
import games

if __name__ == "__main__":
    instance = games.Pyfaceit('Ultrafy','de_mirage')
    print(instance.player_stats_map())
    


