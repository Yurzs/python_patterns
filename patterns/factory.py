import math


class RawMineral:
    mass_kg: int
    process_rate: int

    def __init__(self, mass):
        self.mass_kg = mass

    @classmethod
    def factory_import(cls, mineral_type, mass):

        search_result = list(filter(lambda x: x.__name__.lower() == mineral_type, cls.__subclasses__()))
        if search_result:
            return search_result[0](mass)
        else:
            return None

    def process(self):
        return ProcessedMineral(self)


class Gold(RawMineral):
    process_rate = 0.1


class Silver(RawMineral):
    process_rate = 0.2


class Bronze(RawMineral):
    process_rate = 0.3


class ProcessedMineral:
    mass: int

    def __init__(self, raw: RawMineral):
        self.mass = raw.mass_kg * raw.process_rate

class Order:
    def __init__(self, product: ProcessedMineral, time: int, distance: int, money: int, urgent: bool = False):
        self.product = product
        self.time = time
        self.distance = distance
        self.money = money
        self.urgent = urgent

    def deliver(self):
        stats = {}
        for v_cls in Vehicle.__subclasses__():
            v_count = math.ceil(self.product.mass / v_cls.max_mass_kg)
            price = self.distance * v_cls.price_per_km * v_count
            deliver_time = self.distance / v_cls.speed_kmh
            stats[v_cls] = {
                'count': v_count,
                'price': price,
                'deliver_time': deliver_time
            }
        money_can_buy = list(filter(lambda x: x[1].get('price') < self.money, stats.items()))
        if self.urgent:

            result_vehicles = sorted(money_can_buy, key=lambda x: x[1].get('deliver_time'))
        else:
            result_vehicles = sorted(money_can_buy, key=lambda x: x[1].get('price'))
        if not result_vehicles:
            raise ValueError('Not enough money')
        else:
            return result_vehicles[0][0](result_vehicles[0][1].get('count'))


class Vehicle:
    def __init__(self, count):
        self.count = count

    max_mass_kg: int
    speed_kmh: int
    price_per_km: int
    count: int


class Truck(Vehicle):
    max_mass_kg = 100
    speed_kmh = 90
    price_per_km = 2


class Boat(Vehicle):
    max_mass_kg = 150
    speed_kmh = 40
    price_per_km = 1


class Plane(Vehicle):
    max_mass_kg = 75
    speed_kmh = 800
    price_per_km = 10


class Factory:
    imported_minerals = RawMineral.factory_import('gold', 10_000)
    processed_minerals = imported_minerals.process()
    delivery_order = Order(processed_minerals, 1000, 100, 1000)
    delivery_order.deliver()




