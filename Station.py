class Station:
    def __init__(self, name):
        self.name = name
        self.neighborhood = set()
        self.distances = dict()
        self.channels = dict()

    def __repr__(self):
        return self.name

    def Link2Station(self, other_station, distance):
        if other_station != self:
            self.neighborhood.add(other_station)
            for neighbor in self.neighborhood:
                self.distances[neighbor] = distance
            other_station.neighborhood.add(self)
            for neighbor in other_station.neighborhood:
                other_station.distances[neighbor] = distance
        else:
            print("You can\'t link a station to itself")

    def SetChannels(self, neighbor, channels, type = "Normal"):
        self.channels[neighbor] = [type, channels]
        neighbor.channels = [type, channels]

StationA = Station("Station A")
StationB = Station("Station B")

StationA.Link2Station(StationB, 10)
StationA.SetChannels(StationB, 15)

print(StationA.neighborhood)
print(StationA.distances)
print(StationA.channels)
