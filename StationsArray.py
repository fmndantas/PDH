from Station import Station

# station1 = Station("Station 1")
# station2 = Station("Station 2")

class StationsArray:
    def __init__(self):
        self.Stations = []

    def __add__(self, new_station):
        if type(new_station) == Station:
            self.Stations.append(new_station)
        else:
            print("You can add only Stations here")

    def __repr__(self):
        return self.Stations.__repr__()

    def StationFromString(self, target):
        for Station in self.Stations:
            if Station.__repr__() == target:
                return Station
            else:
                pass
        return None

    def ReturnLastItem(self):
        return self.Stations[-1].__repr__()


# stations_arr = StationsArray()
# stations_arr + station1
# stations_arr + station2
# print(stations_arr)
# print(stations_arr.Index("Station 3"))

