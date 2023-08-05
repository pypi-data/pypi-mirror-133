class Vehicles():

    def __init__(self, *args, **kwargs):
        self._data = kwargs.get('data', [])

    def __getitem__(self, i):
        return self._data[i]

    def __iter__(self):
        return (i for i in self._data)

    def __len__(self):
        return len(self._data)

    def append(self, data):
        self._data.append(data)

    def extend(self, data):
        self._data.extend(data)

    def serialize(self):
        return [
            d.serialize() for d in self
        ]

    @staticmethod
    def parse(data):
        vehicles = Vehicles()
        if isinstance(data, list):
            for d in data:
                if isinstance(d, dict):
                    vehicles.append(
                        Vehicle(
                            **d
                        )
                    )
                else:
                    raise NotImplementedError()
        elif isinstance(data, dict):
            vehicles.append(
                Vehicle(
                    **data
                )
            )
        else:
            raise NotImplementedError()

        return vehicles


class Vehicle():

    __slots__ = [
        'choc',
        'manv',
        'senc',
        'obsm',
        'catv',
        'num_veh',
        'obs',
        'occutc'
    ]

    def __init__(self, *args, **kwargs):
        self.choc = int(kwargs['choc']) if kwargs['choc'] else None
        self.manv = int(kwargs['manv']) if kwargs['manv'] else None
        self.senc = int(kwargs['senc']) if kwargs['senc'] else None
        self.obsm = int(kwargs['obsm']) if kwargs['obsm'] else None
        self.catv = int(kwargs['catv']) if kwargs['catv'] else None
        self.num_veh = kwargs['num_veh']
        self.obs = int(kwargs['obs']) if kwargs['obs'] else None
        self.occutc = int(kwargs['occutc']) if kwargs['occutc'] else None

    def serialize(self):
        return {
            'choc': self.choc,
            'manv': self.manv,
            'senc': self.senc,
            'obsm': self.obsm,
            'catv': self.catv,
            'num_veh': self.num_veh,
            'obs': self.obs,
            'occutc': self.occutc
        }
