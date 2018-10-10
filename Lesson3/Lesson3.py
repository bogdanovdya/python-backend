#!/usr/bin/env python

from random import randint


class Car:

    def __init__(self, label, max_speed=180,  drag_coef=0.33, time_to_max=50):
        self._label = label
        self._max_speed = max_speed
        self._drag_coef = drag_coef
        self._time_to_max = time_to_max

    def print_params(self):
        print(self._label,
              ' max_speed =', self._max_speed,
              ' drag_coef =', self._drag_coef,
              ' time_to_max =', self._time_to_max)

    def ride(self, ambient_weather, ride_distance):
        _ride_time = 0

        for distance in range(ride_distance):
            _wind_speed = ambient_weather.wind_speed

            if _ride_time == 0:
                _speed = 1
            else:
                _speed = (_ride_time / self._time_to_max) * self._max_speed
                if _speed > _wind_speed:
                    _speed -= (self._drag_coef * _wind_speed)

            _ride_time += float(1) / _speed

        return {"label": self._label, "time": _ride_time}


class Weather:

    def __init__(self, wind_speed=20):
        self._wind_speed = wind_speed

    def get_wind_speed(self):
        return randint(0, self._wind_speed)
    
    wind_speed = property(get_wind_speed)


class Competition:

    _instance = None

    def __new__(cls, distance=10000, wind_speed=100):
        if cls._instance is None:
            cls._instance = super(Competition, cls).__new__(cls)
        return cls._instance

    def __init__(self, distance=10000, wind_speed=100):
        self._distance = distance
        self._weather = Weather(wind_speed)
        self._competitors = []

    def set_distance(self, distance):
        self._distance = distance

    def get_distance(self):
        return self._distance

    def set_weather(self, wind_speed):
        self._weather = Weather(wind_speed)

    def add_competitor(self, label, max_speed=180,  drag_coef=0.33, time_to_max=50):
        new_car = Car(label, max_speed, drag_coef, time_to_max)
        self._competitors.append(new_car)

    def clear_competitors(self):
        self._competitors = []

    def print_competitors(self):
        for car in self._competitors:
            car.print_params()

    def start_competition(self):
        competitors_raiting = []

        for car in self._competitors:
            competitors_raiting.append(car.ride(self._weather, self._distance))

        competitors_raiting = sorted(competitors_raiting, key=lambda x: x['time'])

        for car in competitors_raiting:
            print("Car <%s> result: %f" % (car['label'], car['time']))


if __name__ == "__main__":
    competition = Competition(distance=1000, wind_speed=10)
    competition.add_competitor(label='ferrary', max_speed=340,  drag_coef=0.324, time_to_max=26)
    competition.add_competitor(label='bugatti', max_speed=407, drag_coef=0.39, time_to_max=32)
    competition.add_competitor(label='toyota', drag_coef=0.25, time_to_max=40)
    competition.add_competitor(label='lada', drag_coef=0.32, time_to_max=56)
    competition.add_competitor(label='sx4', time_to_max=44)
    competition.start_competition()
