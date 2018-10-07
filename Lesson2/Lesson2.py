#!/usr/bin/env python

from random import randint


class Car:
    def __init__(self, label='just_another_car', max_speed=180, drag_coef=0.33, time_to_max=50):
        self._specs = {"label": label,
                       "max_speed": max_speed,
                       "drag_coef": drag_coef,
                       "time_to_max": time_to_max}

    def ride(self, ambient_weather, ride_distance):
        _ride_time = 0

        for distance in range(ride_distance):
            _wind_speed = ambient_weather.wind_speed

            if _ride_time == 0:
                _speed = 1
            else:
                _speed = (_ride_time / self._specs["time_to_max"]) * self._specs['max_speed']
                if _speed > _wind_speed:
                    _speed -= (self._specs["drag_coef"] * _wind_speed)

            _ride_time += float(1) / _speed

        return {"label": self._specs["label"], "time": _ride_time}


class Weather:
    def __init__(self, wind_speed=20):
        self._wind_speed = wind_speed

    def get_wind_speed(self):
        return randint(0, self._wind_speed)
    
    wind_speed = property(get_wind_speed)


class Competition:
    instance = None

    def __new__(cls, arg):
        if cls.instance is None:
            cls.instance = super(Competition, cls).__new__(cls)
        return cls.instance

    def __init__(self, distance=10000):
        self._distance = distance

    def start_competition(self, competitor_car, ambient_weather):
        competitors_raiting = []

        for car in competitor_car:
            competitors_raiting.append(car.ride(ambient_weather, self._distance))

        competitors_raiting = sorted(competitors_raiting, key=lambda x: x['time'])

        for car in competitors_raiting:
            print("Car <%s> result: %f" % (car['label'], car['time']))


if __name__ == "__main__":
    ferrary = Car(label='ferrary', max_speed=340,  drag_coef=0.324, time_to_max=26)
    bugatti = Car(label='bugatti', max_speed=407, drag_coef=0.39, time_to_max=32)
    toyota = Car(label='toyota', drag_coef=0.25, time_to_max=40)
    lada = Car(label='lada', drag_coef=0.32, time_to_max=56)
    sx4 = Car(label='sx4', time_to_max=44)

    competitors = (ferrary, bugatti, toyota, lada, sx4)

    weather = Weather(100)

    competition = Competition(9000)
    competition.start_competition(competitors, weather)

