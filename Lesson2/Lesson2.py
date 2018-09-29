#!/usr/bin/env python

from random import randint

class Car:
    def __init__(self, label, max_speed = 100, drag_coef = 0.33, time_to_max = 60):
        self.__specs = {"label": label,"max_speed": max_speed,
                      "drag_coef": drag_coef, "time_to_max": time_to_max}

    def get_specs(self):
        return self.__specs


class Weather:
    def __init__(self, wind_speed = 20):
        self.__wind_speed = wind_speed

    def get_wind_speed(self):
        return randint(0, self.__wind_speed)


class Competition:
    def __init__(self, distance = 10000):
        self.__distance = distance

    def start_competition(self, competitors, weather):
        for competitor_name in competitors:
            competitor_time = 0
            competitor_speed = 0
            car = competitor_name.get_specs()

            for distance in range(self.__distance):
                _wind_speed = weather.get_wind_speed()

                if competitor_time == 0:
                    _speed = 1
                else:
                    _speed = (competitor_time / car["time_to_max"]) * car['max_speed']
                    if _speed > _wind_speed:
                        _speed -= (car["drag_coef"] * _wind_speed)

                competitor_time += float(1) / _speed

            print ("Car <%s> result: %f" % (car["label"], competitor_time))


ferrary = Car('ferrary', 340,  0.324, 26)
bugatti = Car('bugatti', 407, 0.39, 32)
toyota = Car('toyota', 180, 0.25, 40)
lada = Car('lada', 180, 0.32, 56)
sx4 = Car('sx4', 180, 0.33, 44)
competitors = (ferrary, bugatti, toyota, lada, sx4)

weather = Weather(100)
competition = Competition(99999)

competition.start_competition(competitors, weather)

