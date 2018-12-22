class Equipments:
    def __init__(self, name, price, **kwargs):
        self.price = price
        self.name = name
        self.keys = list(kwargs.keys())
        self.values = list(kwargs.values())
        for key in self.keys:
            setattr(self, key, self.values[self.keys.index(key)])

    def __repr__(self):
        PrintStr = "Equipment name: {0}\n" \
                   "Price: {1}\n".format(self.name, self.price)
        for key in self.keys:
            PrintStr += "{0}: {1}\n".format(key, str(getattr(self, key)))
        return PrintStr