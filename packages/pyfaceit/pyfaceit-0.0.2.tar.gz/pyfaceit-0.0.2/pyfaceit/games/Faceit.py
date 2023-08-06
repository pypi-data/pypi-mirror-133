import requests
import sys
sys.path.insert(1,'/pyfaceit/keys')
import keys
class Pyfaceit:

    game_id = "csgo"
    api_header = {"Authorization":"Bearer " + keys.PYFACEIT_API_KEY,"content-type": "application/json"}

    def __init__(self,pname,pmap=None) -> None:
        self.pname = pname
        self._player_id = None
        self.map = pmap

        if '_' not in self.map:
            self.map = 'de_' + self.map

            
    
    
    @property
    def player_id(self) -> str | int | None:
        try:
            player_id_request = requests.get(f"https://open.faceit.com/data/v4/players?nickname={self.pname}&game=CSGO",headers=self.api_header)
            player_id_data = player_id_request.json()
            player_id = player_id_data["player_id"]
            return player_id
        except KeyError:
            print('Error Occured',self.pname,'doesnt exist')
            return None
        
    @player_id.setter
    def player_id(self) -> None:
        print("SETTING PLAYER ID")
        self._player_id = self.player_id()
    

    def player_information(self) -> dict:
        try:
            player_data = requests.get(f"https://open.faceit.com/data/v4/players/{self.player_id}",headers=self.api_header)
            player_data_json = player_data.json()
            return player_data_json
        except Exception:
            return None
    
    def player_stats(self) -> dict:
        try:
            player_stats_request = requests.get(f'https://open.faceit.com/data/v4/players/{self.player_id}/stats/{self.game_id}',headers=self.api_header)
            player_stats_json = player_stats_request.json()
            return player_stats_json
        except Exception:
            return None
    
    def player_stats_map(self) -> dict:
        if self.map == None:
            return None
        
        try:
            pdata = self.player_stats()
            map_data = pdata['segments']
            for map in map_data:
                if map['label'] == self.map:
                    return map

        except Exception:
            return None
            

