import random
print('Задание 1')
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
class SportCar(Car):
    def fast_drive(self, km):
        neeg_fuel = (km * self.rate*1.5) / 100
        if neeg_fuel <= self.fuel:
            print((f'Мы проехали {km} км'))
            self.fuel -= neeg_fuel
            self.mileage += km
        else:
            print('Не хватает топлива')
    def competition(self):
        won = random.randint(0, 1)
        if won == 0:
            print('Выиграл')
        else:
            print('Проиграл')

car1 = Car(color='черный', fuel=8, rate=8, mileage=0)
car2 = SportCar(color='черный', fuel=8, rate=8, mileage=0)

print('Первая машина')
for i in range(4):
    car1.drive(30)
print('Вторая машина')
for i in range(4):
    car2.fast_drive(30)

print(car2.competition())

print('Задание 2')
class Programmer:
    def __init__(self, name, post):
        self.name = name
        self.post = post
        self.all_time = 0
        self.all_salary = 0
        self.salary_info = {'Junior': 10, 'Middle': 15, 'Senior': 20}
    def work(self, time):
        self.all_time += time
        if self.post == 'Junior':
            salary = self.salary_info['Junior']
            self.all_salary += time * salary
        elif self.post == 'Middle':
            salary = self.salary_info['Middle']
            self.all_salary += time * salary
        elif self.post == 'Senior':
            salary = self.salary_info['Senior']
            self.all_salary += time * salary
    def rise(self):
        if self.post == 'Junior':
            self.post = 'Middle'
        elif self.post == 'Middle':
            self.post = 'Senior'
        elif self.post == 'Senior':
            self.salary_info['Senior'] += 1

    def info(self):
        print((f'{self.name} {self.post} {self.all_time}ч. {self.all_salary} тугриков'))


programmer = Programmer('Васильев Иван', 'Junior')
programmer.work(750)
print(programmer.info())
programmer.rise()
programmer.work(500)
print(programmer.info())
programmer.rise()
programmer.work(250)
print(programmer.info())
programmer.rise()
programmer.work(250)
print(programmer.info())





