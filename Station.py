from collections import namedtuple
from Equipments import Equipments

class Station:
    def __init__(self, name, type_of_station):
        self.type_of_station = type_of_station
        self.name = name
        self.neighborhood = set()
        self.fatherStation = None
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
            self.distances[other_station] = distance
            other_station.neighborhood.add(self)
            other_station.distances[self] = distance
            other_station.fatherStation = self
        else:
            print("You can\'t link a station to itself")

    def SetChannels2Station(self, target, channels, type="Channels"):
        """
        Uses GetPath method to encounter the path among two stations
        Put channels in the path encountered
        A motherfucking method
        """
        Path = list(self.GetPath(target)) # Returns the path that links the source (self) station to the target station
        ChannelsToAppend = self.ChannelNamedTuple(type, channels)
        i = 0
        while i < len(Path[0])-1:
            SourceStation = Path[0][i]
            neighbor = Path[0][i+1]
            if neighbor not in SourceStation.channels.keys():
                SourceStation.channels[neighbor] = []
                neighbor.channels[SourceStation] = []
                SourceStation.channels[neighbor].append(ChannelsToAppend)
                neighbor.channels[SourceStation].append(ChannelsToAppend)
            elif neighbor in SourceStation.channels.keys():
                changeFlag = False
                for item in SourceStation.channels[neighbor]:
                    if item.Type == type:
                        newItem = SourceStation.ChannelNamedTuple(type, channels + item.Amount)
                        SourceStation.channels[neighbor].insert(SourceStation.channels[neighbor].index(item), newItem)
                        neighbor.channels[SourceStation].insert(neighbor.channels[SourceStation].index(item), newItem)
                        SourceStation.channels[neighbor].pop(SourceStation.channels[neighbor].index(item))
                        neighbor.channels[SourceStation].pop(neighbor.channels[SourceStation].index(item))
                        changeFlag = True
                        break
                    else:
                        continue
                if not(changeFlag):
                    SourceStation.channels[neighbor].append(ChannelsToAppend)
                    neighbor.channels[SourceStation].append(ChannelsToAppend)
                else:
                    pass
            i += 1

            """ Old and useless version
            _______________________________________________________________________________________
            if neighbor not in self.channels.keys():
                self.channels[neighbor] = []
                neighbor.channels[self] = []
                self.channels[neighbor].append(ChannelsToAppend)
                neighbor.channels[self].append(ChannelsToAppend)
            elif neighbor in self.channels.keys():
                changeFlag = False
                for item in self.channels[neighbor]:
                    if item.Type == type:
                        newItem = self.ChannelNamedTuple(type, channels + item.Amount)
                        self.channels[neighbor].insert(self.channels[neighbor].index(item), newItem)
                        neighbor.channels[self].insert(neighbor.channels[self].index(item), newItem)
                        self.channels[neighbor].pop(self.channels[neighbor].index(item))
                        neighbor.channels[self].pop(neighbor.channels[self].index(item))
                        changeFlag = True
                        break
                    else:
                        continue
                if not(changeFlag):
                    self.channels[neighbor].append(ChannelsToAppend)
                    neighbor.channels[self].append(ChannelsToAppend)
                else:
                    pass
            _______________________________________________________________________________________
            """

    def GetPath(self, target_station):
        """
        :param target_station:
        :return: the stations of the path, one by one
        """
        stack = [(self, [self])]
        while stack:
            (vertex, path) = stack.pop()
            for next in vertex.neighborhood - set(path):
                if next == target_station:
                    yield path + [next]
                else:
                    stack.append((next, path + [next]))

    def ShowStation(self):
        """
        Shows the station data:
        """
        print("\nName: {0}, Type: {5}\n"
              "Neighborhood: {1}"
              "\nDistance to (km): {2}"
              "\nChannels to: {3}"
              "\nFather station: {4}".format(self, self.neighborhood,
                                             self.distances,
                                             self.channels,
                                             self.fatherStation,
                                             self.type_of_station))

stationA = Station("Station A", "Digital")
stationB = Station("Station B", "Digital")
stationC = Station("Station C", "Digital")
stationD = Station("Station D", "Digital")
stationE = Station("Station E", "Analog")

stationB.SetNeighbor(stationA, 10)
stationB.SetNeighbor(stationC, 30)
stationB.SetNeighbor(stationE, 18)
stationA.SetNeighbor(stationD, 8)

stationA.SetChannels2Station(stationE, 300)
stationA.SetChannels2Station(stationD, 420)
stationA.SetChannels2Station(stationD, 30, type="LP")
stationD.SetChannels2Station(stationB, 480)
stationB.SetChannels2Station(stationC, 300)
stationC.SetChannels2Station(stationE, 120)
stationC.SetChannels2Station(stationE, 60, type="LP")

stationA.ShowStation()
stationB.ShowStation()
stationC.ShowStation()
stationD.ShowStation()
stationE.ShowStation()