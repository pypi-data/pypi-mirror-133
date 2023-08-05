from ast import literal_eval
import os
import tarfile
import glob
from math import isnan
from numbers import Number

import pandas as pd

from road_collisions_base import logger
from road_collisions_base.models.generic import GenericObjects
from road_collisions_base.models.raw_collision import RawCollision

from road_collisions_france.models.casualty import Casualties
from road_collisions_france.models.vehicle import Vehicles


class Collisions(GenericObjects):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('child_class', RawCollision)
        super().__init__(*args, **kwargs)

    @staticmethod
    def from_file(filepath):
        data = None

        ext = os.path.splitext(filepath)[-1]
        if ext == '.tgz':
            tar = tarfile.open(filepath, "r:gz")
            tar.extractall(path=os.path.dirname(filepath))
            tar.close()

            data = []
            for sub_file in glob.iglob(os.path.dirname(filepath) + '/**', recursive=True):
                ext = os.path.splitext(sub_file)[-1]
                if ext == '.csv':
                    csv_data = pd.read_csv(
                        sub_file.replace('.csv.tgz', '.csv')
                    ).to_dict(orient='records')
                    data.extend(csv_data)
        else:
            raise Exception()

        collisions = Collisions()
        for collision_dict in data:
            obj = Collision.parse(
                collision_dict
            )

            # TODO: filter the object out here by whatever prop params
            # and save some mem

            collisions.append(obj)

        return collisions

    @staticmethod
    def from_dir(dirpath, region=None):
        collisions = Collisions()
        if region is None:
            search_dir = f'{dirpath}/**'
        else:
            search_dir = f'{dirpath}/{region}/**'

        for filename in glob.iglob(search_dir, recursive=True):
            if os.path.splitext(filename)[-1] not in {'.tgz'}:
                continue
            collisions.extend(
                Collisions.from_file(
                    filename
                )._data
            )

        return collisions

    def filter(self, **kwargs):
        '''
        By whatever props that exist
        '''
        logger.debug('Filtering from %s' % (len(self)))

        filtered = [
            d for d in self if all(
                [
                    getattr(d, attr) == kwargs[attr] for attr in kwargs.keys()
                ]
            )
        ]

        return Collisions(
            data=filtered
        )

    @staticmethod
    def load_all():
        import road_collisions_france
        return Collisions.from_dir(
            os.path.join(road_collisions_france.__path__[0], 'resources'),
            region='fr'
        )


class Collision(RawCollision):

    __slots__ = [
        'num_acc',
        'adr',
        'agg',
        'an',
        'atm',
        'catr',
        'circ',
        'col',
        'com',
        'dep',
        'env1',
        'gps',
        'hrmn',
        'infra',
        'int',
        'jour',
        'larrout',
        'lartpc',
        'lat',
        'long',
        'lum',
        'mois',
        'nbv',
        'plan',
        'pr',
        'pr1',
        'prof',
        'situ',
        'surf',
        'v1',
        'v2',
        'voie',
        'vosp',
        'vehicles',
        'casualties'
    ]

    def __init__(self, **kwargs):
        self.num_acc = kwargs['Num_Acc']
        self.adr = kwargs['adr']
        self.agg = kwargs['agg']

        # TODO: this needs to be normalized. Think it's year
        self.an = int(kwargs['an']) if isinstance(kwargs['an'], Number) and not isnan(kwargs['an']) else None

        self.atm = int(kwargs['atm']) if isinstance(kwargs['atm'], Number) and not isnan(kwargs['atm']) else None
        self.catr = int(kwargs['catr']) if isinstance(kwargs['catr'], Number) and not isnan(kwargs['catr']) else None
        self.circ = int(kwargs['circ']) if isinstance(kwargs['circ'], Number) and not isnan(kwargs['circ']) else None
        self.col = int(kwargs['col']) if isinstance(kwargs['col'], Number) and not isnan(kwargs['col']) else None
        self.com = int(kwargs['com']) if isinstance(kwargs['com'], Number) and not isnan(kwargs['com']) else None
        self.dep = int(kwargs['dep']) if isinstance(kwargs['dep'], Number) and not isnan(kwargs['dep']) else None
        self.env1 = int(kwargs['env1']) if isinstance(kwargs['env1'], Number) and not isnan(kwargs['env1']) else None
        self.gps = kwargs['gps']
        self.hrmn = kwargs['hrmn']
        self.infra = int(kwargs['infra']) if not isnan(kwargs['infra']) else None
        self.int = int(kwargs['int']) if not isnan(kwargs['int']) else None
        self.jour = int(kwargs['jour']) if not isnan(kwargs['jour']) else None
        self.larrout = float(kwargs['larrout']) if kwargs['larrout'] not in {'0.0', '0', '-'} and isinstance(kwargs['larrout'], Number) and not isnan(kwargs['larrout']) else None
        self.lartpc = float(str(kwargs['lartpc']).replace(',', '.')) if kwargs['lartpc'] not in {'0.0', '0', '-'} and isinstance(kwargs['lartpc'], Number) and not isnan(kwargs['lartpc']) else None

        # FIXME: lat and long are all sorts of weird
        self.lat = float(str(kwargs['lat']).replace(',', '.')) if kwargs['lat'] not in {'0.0', '0', '-'} and isinstance(kwargs['lat'], Number) and not isnan(kwargs['lat']) else None
        self.long = float(str(kwargs['long']).replace(',', '.')) if kwargs['long'] not in {'0.0', '0', '-'} and isinstance(kwargs['long'], Number) and not isnan(kwargs['long']) else None

        self.lum = kwargs['lum']
        self.mois = kwargs['mois']
        self.nbv = int(kwargs['nbv']) if not isnan(kwargs['nbv']) else None
        self.plan = int(kwargs['plan']) if not isnan(kwargs['plan']) else None
        self.pr = kwargs['pr']
        self.pr1 = kwargs['pr1']
        self.prof = int(kwargs['prof']) if not isnan(kwargs['prof']) else None
        self.situ = int(kwargs['situ']) if not isnan(kwargs['situ']) else None
        self.surf = int(kwargs['surf']) if not isnan(kwargs['surf']) else None
        self.casualties = Casualties.parse(
            literal_eval(kwargs['usagers'].replace('nan', 'None'))
        )
        self.v1 = int(kwargs['v1']) if not isnan(kwargs['v1']) else None
        self.v2 = kwargs['v2']
        self.vehicles = Vehicles.parse(
            literal_eval(kwargs['vehicules'].replace('nan', 'None'))
        )
        self.voie = kwargs['voie']
        self.vosp = int(kwargs['vosp']) if not isnan(kwargs['vosp']) else None

    @staticmethod
    def parse(data):
        if isinstance(data, Collision):
            return data

        return Collision(
            **data
        )

    def serialize(self):
        return {
            'num_acc': self.num_acc,
            'adr': self.adr,
            'agg': self.agg,
            'an': self.an,
            'atm': self.atm,
            'catr': self.catr,
            'circ': self.circ,
            'col': self.col,
            'com': self.com,
            'dep': self.dep,
            'env1': self.env1,
            'gps': self.gps,
            'hrmn': self.hrmn,
            'infra': self.infra,
            'int': self.int,
            'jour': self.jour,
            'larrout': self.larrout,
            'lartpc': self.lartpc,
            'lat': self.lat,
            'long': self.long,
            'lum': self.lum,
            'mois': self.mois,
            'nbv': self.nbv,
            'plan': self.plan,
            'pr': self.pr,
            'pr1': self.pr1,
            'prof': self.prof,
            'situ': self.situ,
            'surf': self.surf,
            'v1': self.v1,
            'v2': self.v2,
            'voie': self.voie,
            'vosp': self.vosp,
            'vehicles': self.vehicles.serialize(),
            'casualties': self.casualties.serialize()
        }
