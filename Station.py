from collections import namedtuple

class Station:
    def __init__(self, name):
        self.name = name
        self.neighborhood = set()
        self.distances = dict()
        self.channels = dict()

        self.ChannelNamedTuple = namedtuple("Channel", "Type Amount")

    def __repr__(self):
        return self.name

    def SetNeighbor(self, other_station, distance):
        """
        :param other_station: the station intended to be set as neighbor
        :param distance: distance between the current station and the other_station in km
        """
        if other_station != self:
            self.neighborhood.add(other_station)
            for neighbor in self.neighborhood:
                self.distances[neighbor] = distance

            other_station.neighborhood.add(self)
            for neighbor in other_station.neighborhood:
                other_station.distances[neighbor] = distance
        else:
            print("You can\'t link a station to itself")

    def SetChannels(self, neighbor, channels, type="Normal"):
        ChannelsToAppend = self.ChannelNamedTuple(type, channels)
        if neighbor in self.neighborhood:
            if neighbor not in self.channels.keys():
                self.channels[neighbor] = []
                self.channels[neighbor].append(ChannelsToAppend)
            elif neighbor in self.channels.keys():
                changeFlag = False
                for item in self.channels[neighbor]:
                    if item.Type == type:

                        changeFlag = True
                    else:
                        pass
                if not(changeFlag):
                    self.channels[neighbor].append(ChannelsToAppend)
                else:
                    pass
        else:
            print("You can\'t set channels to a non neighbor station")

    def ShowStation(self):
        """
        Shows the station in following form:
        Name:
        Neighborhood:
        Distances to:
        Channels to:
        """
        print("Name: {0}\n"
              "Neighborhood: {1}"
              "\nDistance to: {2}"
              "\nChannels to: {3}".format(self, self.neighborhood, self.distances, self.channels))


stationA = Station("Station A")
stationB = Station("Station B")
stationC = Station("Station C")

stationA.SetNeighbor(stationB, 50)
stationB.SetNeighbor(stationC, 42)

stationA.SetChannels(stationB, 400, type="Normal")
stationA.SetChannels(stationB, 600, type="Normal")

stationA.SetChannels(stationB, 30, type="LT")
stationA.ShowStation()

