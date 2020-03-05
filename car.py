class Car:
    """Car class with basic statistics"""
    def __init__(self, car_name, region, number_of_session):
        self.car_name = car_name
        self.region = region
        self.number_of_session = number_of_session

    def __str__(self):
        return f'Car name: {self.car_name}\nRegion: {self.region}'


car = Car('TWN', 'APAC', 234)

print(car)