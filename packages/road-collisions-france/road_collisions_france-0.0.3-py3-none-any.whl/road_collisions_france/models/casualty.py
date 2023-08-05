class Casualties():

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
        casualties = Casualties()
        if isinstance(data, list):
            for d in data:
                if isinstance(d, dict):
                    casualties.append(
                        Casualty(
                            **d
                        )
                    )
                else:
                    raise NotImplementedError()
        elif isinstance(data, dict):
            casualties.append(
                Casualty(
                    **data
                )
            )
        else:
            import pdb; pdb.set_trace()
            raise NotImplementedError()

        return casualties


class Casualty():

    __slots__ = [
        'year_of_birth',
        'sex',
        'actp',
        'secu',
        'grav',
        'locp',
        'num_veh',
        'place',
        'catu',
        'etatp',
        'trajet'
    ]

    def __init__(self, *args, **kwargs):
        self.year_of_birth = int(kwargs['an_nais']) if kwargs['an_nais'] else None
        self.sex = int(kwargs['sexe']) if kwargs['sexe'] else None
        self.actp = kwargs['actp']
        self.secu = int(kwargs['secu']) if kwargs.get('secu', None) else None
        self.grav = int(kwargs['grav']) if kwargs['grav'] else None
        self.locp = int(kwargs['locp']) if kwargs['locp'] else None
        self.num_veh = kwargs['num_veh']
        self.place = int(kwargs['place']) if kwargs['place'] else None
        self.catu = int(kwargs['catu']) if kwargs['catu'] else None
        self.etatp = int(kwargs['etatp']) if kwargs['etatp'] else None
        self.trajet = int(kwargs['trajet']) if kwargs['trajet'] else None

    def serialize(self):
        return {
            'year_of_birth': self.year_of_birth,
            'sex': self.sex,
            'actp': self.actp,
            'secu': self.secu,
            'grav': self.grav,
            'locp': self.locp,
            'num_veh': self.num_veh,
            'place': self.place,
            'catu': self.catu,
            'etatp': self.etatp,
            'trajet': self.etatp
        }
