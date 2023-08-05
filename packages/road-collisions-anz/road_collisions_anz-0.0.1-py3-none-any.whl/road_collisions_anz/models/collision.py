import os
import tarfile
import glob

import pandas as pd

from road_collisions_base import logger
from road_collisions_base.models.generic import GenericObjects
from road_collisions_base.models.raw_collision import RawCollision


class Collisions(GenericObjects):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('child_class', RawCollision)
        super().__init__(*args, **kwargs)

    @staticmethod
    def from_file(filepath):
        data = None

        ext = os.path.splitext(filepath)[-1]
        if ext == '.tgz' or ext == '.gz':
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
            if os.path.splitext(filename)[-1] not in {'.tgz', '.gz'}:
                continue
           
            collision = Collisions.from_file(
                filename
            )

            collisions.extend(
                collision
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
        import road_collisions_anz
        return Collisions.from_dir(
            os.path.join(road_collisions_anz.__path__[0], 'resources'),
            region='anz'
        )


class Collision(RawCollision):

    __slots__ = [
        'DCA_code',
        'animals',
        'approximate',
        'bicycle',
        'bus',
        'car_4x4',
        'car_sedan',
        'car_station_wagon',
        'car_utility',
        'car_van',
        'casualties',
        'comment',
        'country',
        'crash_id',
        'crash_type',
        'day_of_month',
        'day_of_week',
        'description_id',
        'drugs_alcohol',
        'fatalities',
        'hour',
        'inanimate',
        'intersection',
        'latitude',
        'lighting',
        'local_government_area',
        'longitude',
        'midblock',
        'minor_injuries',
        'month',
        'motor_cycle',
        'pedestrian',
        'road_position_horizontal',
        'road_position_vertical',
        'road_sealed',
        'road_wet',
        'scooter',
        'serious_injuries',
        'severity',
        'speed_limit',
        'state',
        'statistical_area',
        'suburb',
        'taxi',
        'traffic_controls',
        'train',
        'tram',
        'truck_large',
        'truck_small',
        'vehicle_other',
        'weather',
        'year'
    ]

    def __init__(self, **kwargs):
        self.DCA_code = kwargs['DCA_code']
        self.animals = kwargs['animals']
        self.approximate = kwargs['approximate']
        self.bicycle = kwargs['bicycle']
        self.bus = kwargs['bus']
        self.car_4x4 = kwargs['car_4x4']
        self.car_sedan = kwargs['car_sedan']
        self.car_station_wagon = kwargs['car_station_wagon']
        self.car_utility = kwargs['car_utility']
        self.car_van = kwargs['car_van']
        self.casualties = kwargs['casualties']
        self.comment = kwargs['comment']
        self.country = kwargs['country']
        self.crash_id = kwargs['crash_id']
        self.crash_type = kwargs['crash_type']
        self.day_of_month = kwargs['day_of_month']
        self.day_of_week = kwargs['day_of_week']
        self.description_id = kwargs['description_id']
        self.drugs_alcohol = kwargs['drugs_alcohol']
        self.fatalities = kwargs['fatalities']
        self.hour = kwargs['hour']
        self.inanimate = kwargs['inanimate']
        self.intersection = kwargs['intersection']
        self.latitude = kwargs['latitude']
        self.lighting = kwargs['lighting']
        self.local_government_area = kwargs['local_government_area']
        self.longitude = kwargs['longitude']
        self.midblock = kwargs['midblock']
        self.minor_injuries = kwargs['minor_injuries']
        self.month = kwargs['month']
        self.motor_cycle = kwargs['motor_cycle']
        self.pedestrian = kwargs['pedestrian']
        self.road_position_horizontal = kwargs['road_position_horizontal']
        self.road_position_vertical = kwargs['road_position_vertical']
        self.road_sealed = kwargs['road_sealed']
        self.road_wet = kwargs['road_wet']
        self.scooter = kwargs['scooter']
        self.serious_injuries = kwargs['serious_injuries']
        self.severity = kwargs['severity']
        self.speed_limit = kwargs['speed_limit']
        self.state = kwargs['state']
        self.statistical_area = kwargs['statistical_area']
        self.suburb = kwargs['suburb']
        self.taxi = kwargs['taxi']
        self.traffic_controls = kwargs['traffic_controls']
        self.train = kwargs['train']
        self.tram = kwargs['tram']
        self.truck_large = kwargs['truck_large']
        self.truck_small = kwargs['truck_small']
        self.vehicle_other = kwargs['vehicle_other']
        self.weather = kwargs['weather']
        self.year = kwargs['year']

    @staticmethod
    def parse(data):
        if isinstance(data, Collision):
            return data

        return Collision(
            **data
        )

    def serialize(self):
        return {
            'DCA_code': self.DCA_code,
            'animals': self.animals,
            'approximate': self.approximate,
            'bicycle': self.bicycle,
            'bus': self.bus,
            'car_4x4': self.car_4x4,
            'car_sedan': self.car_sedan,
            'car_station_wagon': self.car_station_wagon,
            'car_utility': self.car_utility,
            'car_van': self.car_van,
            'casualties': self.casualties,
            'comment': self.comment,
            'country': self.country,
            'crash_id': self.crash_id,
            'crash_type': self.crash_type,
            'day_of_month': self.day_of_month,
            'day_of_week': self.day_of_week,
            'description_id': self.description_id,
            'drugs_alcohol': self.drugs_alcohol,
            'fatalities': self.fatalities,
            'hour': self.hour,
            'inanimate': self.inanimate,
            'intersection': self.intersection,
            'latitude': self.latitude,
            'lighting': self.lighting,
            'local_government_area': self.local_government_area,
            'longitude': self.longitude,
            'midblock': self.midblock,
            'minor_injuries': self.minor_injuries,
            'month': self.month,
            'motor_cycle': self.motor_cycle,
            'pedestrian': self.pedestrian,
            'road_position_horizontal': self.road_position_horizontal,
            'road_position_vertical': self.road_position_vertical,
            'road_sealed': self.road_sealed,
            'road_wet': self.road_wet,
            'scooter': self.scooter,
            'serious_injuries': self.serious_injuries,
            'severity': self.severity,
            'speed_limit': self.speed_limit,
            'state': self.state,
            'statistical_area': self.statistical_area,
            'suburb': self.suburb,
            'taxi': self.taxi,
            'traffic_controls': self.traffic_controls,
            'train': self.train,
            'tram': self.tram,
            'truck_large': self.truck_large,
            'truck_small': self.truck_small,
            'vehicle_other': self.vehicle_other,
            'weather': self.weather,
            'year': self.year
        }
