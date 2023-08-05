import datetime
import os
import glob
import csv
import tarfile

from pandas import DataFrame
import pandas as pd

from road_collisions_base import logger
from road_collisions_base.models.raw_collision import RawCollision
from road_collisions_base.models.generic import GenericObjects

from road_collisions_us.utils import extract_tgz


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
        import road_collisions_us
        return Collisions.from_dir(
            '/opt/road_collisions/',
            region='us'
        )


class Collision(RawCollision):

    __slots__ = [
        'id',
        'severity',
        'start_time',
        'end_time',
        'start_lat',
        'start_lng',
        'end_lat',
        'end_lng',
        'distance',
        'description',
        'number',
        'street',
        'side',
        'city',
        'county',
        'state',
        'zipcode',
        'country',
        'timezone',
        'airport_code',
        'weather_timestamp',
        'temperature',
        'wind_chill',
        'humidity',
        'pressure',
        'visibility',
        'wind_direction',
        'wind_speed',
        'precipitation',
        'weather_condition',
        'amenity',
        'bump',
        'crossing',
        'give_way',
        'junction',
        'no_exit',
        'railway',
        'roundabout',
        'station',
        'stop',
        'traffic_calming',
        'traffic_signal',
        'turning_loop',
        'sunrise_sunset',
        'civil_twilight',
        'nautical_twilight',
        'astronomical_twilight'
    ]

    def __init__(self, **kwargs):
        self.id = kwargs['ID']
        self.severity = kwargs['Severity']
        self.start_time = kwargs['Start_Time']
        self.end_time = kwargs['End_Time']
        self.start_lat = kwargs['Start_Lat']
        self.start_lng = kwargs['Start_Lng']
        self.end_lat = kwargs['End_Lat']
        self.end_lng = kwargs['End_Lng']
        self.distance = kwargs['Distance(mi)']
        self.description = kwargs['Description']
        self.number = kwargs['Number']
        self.street = kwargs['Street']
        self.side = kwargs['Side']
        self.city = kwargs['City']
        self.county = kwargs['County']
        self.state = kwargs['State']
        self.zipcode = kwargs['Zipcode']
        self.country = kwargs['Country']
        self.timezone = kwargs['Timezone']
        self.airport_code = kwargs['Airport_Code']
        self.weather_timestamp = kwargs['Weather_Timestamp']
        self.temperature = kwargs['Temperature(F)']
        self.wind_chill = kwargs['Wind_Chill(F)']
        self.humidity = kwargs['Humidity(%)']
        self.pressure = kwargs['Pressure(in)']
        self.visibility = kwargs['Visibility(mi)']
        self.wind_direction = kwargs['Wind_Direction']
        self.wind_speed = kwargs['Wind_Speed(mph)']
        self.precipitation = kwargs['Precipitation(in)']
        self.weather_condition = kwargs['Weather_Condition']
        self.amenity = kwargs['Amenity']
        self.bump = kwargs['Bump']
        self.crossing = kwargs['Crossing']
        self.give_way = kwargs['Give_Way']
        self.junction = kwargs['Junction']
        self.no_exit = kwargs['No_Exit']
        self.railway = kwargs['Railway']
        self.roundabout = kwargs['Roundabout']
        self.station = kwargs['Roundabout']
        self.stop = kwargs['Stop']
        self.traffic_calming = kwargs['Traffic_Calming']
        self.traffic_signal = kwargs['Traffic_Signal']
        self.turning_loop = kwargs['Turning_Loop']
        self.sunrise_sunset = kwargs['Sunrise_Sunset']
        self.civil_twilight = kwargs['Civil_Twilight']
        self.nautical_twilight = kwargs['Nautical_Twilight']
        self.astronomical_twilight = kwargs['Astronomical_Twilight']

    @staticmethod
    def parse(data):
        if isinstance(data, Collision):
            return data

        return Collision(
            **data
        )

    def serialize(self):
        return {
            'id': self.id,
            'severity': self.severity,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'start_lat': self.start_lat,
            'start_lng': self.start_lng,
            'end_lat': self.end_lat,
            'end_lng': self.end_lng,
            'distance': self.distance,
            'description': self.description,
            'number': self.number,
            'street': self.street,
            'side': self.side,
            'city': self.city,
            'county': self.county,
            'state': self.state,
            'zipcode': self.zipcode,
            'country': self.country,
            'timezone': self.timezone,
            'airport_code': self.airport_code,
            'weather_timestamp': self.weather_timestamp,
            'temperature': self.temperature,
            'wind_chill': self.wind_chill,
            'humidity': self.humidity,
            'pressure': self.pressure,
            'visibility': self.visibility,
            'wind_direction': self.wind_direction,
            'wind_speed': self.wind_speed,
            'precipitation': self.precipitation,
            'weather_condition': self.weather_condition,
            'amenity': self.amenity,
            'bump': self.bump,
            'crossing': self.crossing,
            'give_way': self.give_way,
            'junction': self.junction,
            'no_exit': self.no_exit,
            'railway': self.railway,
            'roundabout': self.roundabout,
            'station': self.station,
            'stop': self.stop,
            'traffic_calming': self.traffic_calming,
            'traffic_signal': self.traffic_signal,
            'turning_loop': self.turning_loop,
            'sunrise_sunset': self.sunrise_sunset,
            'civil_twilight': self.civil_twilight,
            'nautical_twilight': self.nautical_twilight,
            'astronomical_twilight': self.astronomical_twilight
        }
