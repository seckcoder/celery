class enum(object):
    def __init__(self, def_enums, nonvalid=-1):
        self.enum_map = {}    # enum - name
        self.enums = []  # used to record the order of the enums
        self.name_map = def_enums  # name - enum
        self.enum_map = dict((v,k) for k,v in self.name_map.iteritems())
        self.enums = sorted(self.name_map.itervalues())
        self.nonvalid = nonvalid

    def __getitem__(self, idx):
        return self.enums[idx]

    def __getattr__(self, attr):
        if attr in self.name_map:
            return self.name_map[attr]
        else:
            raise AttributeError()

    def __len__(self):
        return len(self.enums)

    def next(self):
        for e in self.enums:
            yield e

    def iternames(self):
        for e in self.enums:
            yield self.enum_map[e]

    def iteritems(self):
        for e in self.enums:
            yield e, self.enum_map[e]

    def human(self, value):
        return self.enum_map[value]

    def contain(self, value):
        return value in self.enum_map
