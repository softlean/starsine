import json
import math
import requests

class Starsine():
    def __init__(self):
        self.locations = {}
        self.lookup_cache = None
        self.__load_locations()
        
    def get_weather_by_coords(self, lat, lon, max_dist):
        """
        gets weather data for the nearest station by the provided coordinates and a upper bound max_dist for the location lookup
        """ 
        nearest = self.__nearest_station(lat, lon, max_dist)
        
        return nearest
    
    def __nearest_station(self, lat, lon, max_dist):
        """
        calculates the nearest station by the provided latitude and longitude
        """
        nearest = None
        cur_nearest = max_dist
        for key, vals in zip(self.locations.keys(), self.locations.values()):
            dist = self.__haversine(lat, lon, vals["lat"], vals["lon"])
            if dist <= max_dist and dist < cur_nearest and key.startswith("RegionenSommer"):
                new_vals = vals
                new_vals["distance"] = dist
                nearest = {key: new_vals}
                cur_nearest = dist

        return nearest

    def __haversine(self, lat1, lon1, lat2, lon2):
        """
        haversine function to calculate distance in km between coordinates
        """
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        radius = 6371
        distance = radius * c

        return distance

    def __load_locations(self):
        """
        loads all the weather locations from an empty api request
        """
        req = requests.get("https://www.bergfex.at/export/apps/weather.json")
        locations = json.loads(req.text)["WeatherLocations"]["Modified"]
        self.locations = {}
        for loc in locations:
            self.locations[loc["ID"]] = {"Name": loc["Name"], "Hoehe": loc["Hoehe"], "lat": loc["Lat"], "lon": loc["Lng"]}

if __name__ == "__main__":
    stsi = Starsine()
    