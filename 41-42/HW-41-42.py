class Car:
    def __init__(self, color, fuel, rate, mileage=0):
        self.color = color
        self.fuel = fuel
        self.rate = rate
        self.mileage = mileage
    def drive(self, km):
        neeg_fuel = (km*self.rate)/100
        if neeg_fuel <= self.fuel:
            print((f'Мы проехали {km} км'))
            self.fuel -= neeg_fuel
            self.mileage += km
        else:
            print('Не хватает топлива')
    def get_mileage(self):
        return self.mileage



