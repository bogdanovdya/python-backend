class PrototypeCar:

    def __init__(self):
        self._objects = {}

    def register_object(self, name, obj):
        """Register an object"""
        self._objects[name] = obj

    def unregister_object(self, name):
        """Unregister an object"""
        del self._objects[name]

    def clone(self, name, **attr):
        """Clone a registered object and update inner attributes dictionary"""
        obj = copy.deepcopy(self._objects.get(name))
        obj.__dict__.update(attr)
        return obj




    ferrary = prototype_car.clone('object_car', label='ferrary', max_speed=340,  drag_coef=0.324, time_to_max=26)
    bugatti = prototype_car.clone('object_car', label='bugatti', max_speed=407, drag_coef=0.39, time_to_max=32)
    toyota = prototype_car.clone('object_car', label='toyota', drag_coef=0.25, time_to_max=40)
    lada = prototype_car.clone('object_car', label='lada', drag_coef=0.32, time_to_max=56)
    sx4 = prototype_car.clone('object_car', label='sx4', time_to_max=44)
    just_another_car = prototype_car.clone('object_car')