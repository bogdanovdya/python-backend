#!/usr/bin/env python

from random import randint


class Car:
    def __init__(self, **kwargs):
        self.__specs = {"label": 'just_another_car', "max_speed": 160, "drag_coef": 0.33, "time_to_max": 50}
        self.__specs.update(kwargs)

    def get_specs(self):
        return self.__specs

##Реализовать доступ к функции получения скорости ветра как к переменной экземпляра класса
##Не смог разобраться в этом
class Weather:
    def __init__(self, wind_speed=20):
        self.__wind_speed = wind_speed

    def get_wind_speed(self):
        return randint(0, self.__wind_speed)


class Competition:

    instance = None

    def __new__(cls, distance=10000):
        if cls.instance is None:
            cls.instance = super(Competition, cls).__new__(cls)
            cls.__distance = distance
        return cls.instance

    def start_competition(self, competitors, weather):
        for competitor_name in competitors:
            competitor_time = 0
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

            print("Car <%s> result: %f" % (car["label"], competitor_time))


ferrary = Car(label='ferrary', max_speed=340,  drag_coef=0.324, time_to_max=26)
bugatti = Car(label='bugatti', max_speed=407, drag_coef=0.39, time_to_max=32)
toyota = Car(label='toyota', max_speed=180, drag_coef=0.25, time_to_max=40)
lada = Car(label='lada', max_speed=180, drag_coef=0.32, time_to_max=56)
sx4 = Car(label='sx4', max_speed=180, drag_coef=0.33, time_to_max=44)

competitors = (ferrary, bugatti, toyota, lada, sx4)

weather = Weather(100)

competition = Competition(9000)
competition.start_competition(competitors, weather)
competition2 = Competition(90)
competition2.start_competition(competitors, weather)
